#!/usr/bin/env python3
"""The merge gate's attribution check (SPEC-0084, PA-004).

Every commit a session produces must be attributable to the leaf that produced it, and
the gate must be able to refuse one that is not.

**A reading, stated rather than assumed.** SPEC-0084 says commits are "signed with a
key enrolled under the leaf". The obvious implementation is git's own signing, which
needs a signing key inside the container — and L0-011 is emphatic that payload code
never touches key material, which is why signing happens behind the agentd socket. So
the leaf attests each commit instead: it publishes a signed envelope naming the
commit's identity, and the gate requires a chain-verifiable attestation for every
commit under review. The attestation is the signature; the chain walk is the
enrolment check. Git-native signing would need a fifth secret in the container and a
second key hierarchy beside the identity chain, which is the thing the identity model
exists to avoid — but this is a reading, and the architect may want the git-native
form instead.

An attestation is an ordinary ES-010 envelope, so it verifies by the ordinary path: no
second verification mechanism, and no second implementation of one (PA-006).
"""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "base" / "l0"))

from chainverify import VerificationError  # noqa: E402
from envelope import verify as verify_envelope  # noqa: E402

ATTESTATION_KIND = "commit.attestation"


class MergeRefused(Exception):
    """ENF-0001's on_fail, as an outcome the caller can report."""


def commit_identity(repo, rev):
    """What an attestation names: the commit and the tree it produced.

    Both, deliberately. The commit hash alone would let an attestation be reused for a
    rewritten commit with identical content; the tree alone would not distinguish two
    commits with the same result.
    """
    out = subprocess.run(["git", "-C", str(repo), "show", "-s", "--format=%H %T", rev],
                         capture_output=True, text=True, check=True).stdout.split()
    return {"commit": out[0], "tree": out[1]}


def attestations_from(envelopes):
    """Pull commit attestations out of a session's observed wire traffic."""
    found = {}
    for env in envelopes:
        payload = env.get("payload")
        if isinstance(payload, dict) and payload.get("kind") == ATTESTATION_KIND:
            data = payload.get("data") or {}
            if data.get("commit"):
                found[data["commit"]] = env
    return found


def verify_commits(repo, revs, envelopes, chain, facts=None):
    """The gate. Returns the verdict per commit; raises nothing — a refusal is data.

    A commit passes only when an attestation exists for it, that attestation's envelope
    verifies per ES-013 (signature, chain walk to root, act token), and the tree it
    names matches the tree the commit actually produced.
    """
    facts = dict(facts or {})
    facts.setdefault("action", "publish")
    attested = attestations_from(envelopes)
    verdicts = []
    for rev in revs:
        ident = commit_identity(repo, rev)
        env = attested.get(ident["commit"])
        if env is None:
            verdicts.append({**ident, "ok": False,
                             "reason": "no attestation for this commit — unattributed "
                                       "work cannot merge (SPEC-0084)"})
            continue
        try:
            verify_envelope(env, chain, facts)
        except VerificationError as e:
            verdicts.append({**ident, "ok": False,
                             "reason": f"attestation does not verify to the leaf: {e}"})
            continue
        claimed = (env.get("payload") or {}).get("data", {}).get("tree")
        if claimed != ident["tree"]:
            verdicts.append({**ident, "ok": False,
                             "reason": f"attestation names tree {claimed}, commit "
                                       f"produced {ident['tree']}"})
            continue
        verdicts.append({**ident, "ok": True,
                         "reason": "attested by a leaf that walks to root"})
    return verdicts


def gate(repo, revs, envelopes, chain, facts=None):
    """Merge-gate entry point: green, or a refusal naming every commit that failed."""
    verdicts = verify_commits(repo, revs, envelopes, chain, facts)
    bad = [v for v in verdicts if not v["ok"]]
    if bad:
        raise MergeRefused("; ".join(f"{v['commit'][:8]}: {v['reason']}" for v in bad))
    return verdicts
