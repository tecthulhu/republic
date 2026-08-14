#!/usr/bin/env python3
"""CTRL-0009 — the merge-enforcement probe (SPEC-0130).

A CI job that detects a violation is a **control**. A repository rule that refuses
the merge when that control is red is **enforcement**. Republic's binding triple
keeps those separate everywhere else, and then the most load-bearing public claim
this repository makes — *a red suite blocks merge* — rested on the control half
alone. The workflow is publicly walkable; the rule that makes it binding was not
pointed at by anything, so a reviewer could verify detection and had to take
enforcement on trust. That is the one-hop gap the whitepaper warns about, sitting on
the sentence a reader is most likely to test.

This probe closes it by making the enforcement state a governed, timestamped
evidence record derived from the live setting.

**Captured, never asserted.** Every fact below comes from the GitHub API on each
run. A constant saying "yes, it is enforced" would be precisely the attestational
theater the paper attacks — a document about a system rather than a constraint
inside it. If the setting changes, the next capture says so.

**Anonymous by default, and that is the point.** The rules endpoint answers without
a credential, so anyone can re-run this against the public repository and get the
same answer. Evidence a reader cannot reproduce is a second thing to trust.

Usage:
    python3 suite/enforcement/run.py [--repo owner/name] [--branch main]
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))

import yaml  # noqa: E402
from paths import REPO  # noqa: E402

API = "https://api.github.com"
# The contexts the claim depends on. Named here so a check being dropped from the
# ruleset is a failure rather than a smaller list quietly passing.
CLAIMED_CONTEXTS = ("corpus-controls", "citizenship-conformance")
# Where committed captures are read from when this run cannot observe the bypass scope
# itself. Module-level so the fixture suite can point it at a temp tree.
ACTA_DIR = pathlib.Path(REPO) / "platform" / "acta"
failures = []
facts = {}


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:300]}")
    if not ok:
        failures.append(name)
    return ok


def get(path, token=None):
    """One GET. Returns (payload, error) — a refusal is data, not an exception."""
    req = urllib.request.Request(f"{API}{path}",
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": "republic-ctrl-0009"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} on {path}"
    except Exception as e:  # noqa: BLE001 — network shape varies; the message is the datum
        return None, f"{type(e).__name__} on {path}: {e}"


def published_contexts(repo_root):
    """The check names the workflows actually publish.

    The ruleset names contexts as strings, and a string that matches nothing is a
    required check that can never report — which reads as *permanently pending*, not
    as a failure, so the merge button simply stays disabled and nobody learns why.
    Reading both sides and comparing them is what makes the binding real: rename a
    job without updating the ruleset, or the reverse, and this goes red.
    """
    names = set()
    wf = pathlib.Path(repo_root) / ".github" / "workflows"
    for f in sorted(wf.glob("*.yml")) + sorted(wf.glob("*.yaml")):
        doc = yaml.safe_load(f.read_text()) or {}
        for job_id, job in (doc.get("jobs") or {}).items():
            names.add((job or {}).get("name") or job_id)
    return names


def attested_bypass_check(unreadable):
    """The bypass fact, carried by a committed capture when this run cannot see it.

    Anonymous runs cannot read `bypass_actors`, so without this the claim would rest on
    nothing for exactly the fact most worth checking. An operator run with a credential
    writes the observation into the Acta, and every later run requires that record to
    exist and to say the scope is empty. The unobserved run therefore asserts something
    real — *somebody with sight of it recorded no bypass* — rather than staying silent.

    It is weaker than a live read and the difference is time: this cannot notice a
    bypass actor added since the last authenticated capture. That gap is the reason the
    row records `bypass_observed: false`, and closing it needs a stored credential,
    which is an owner's decision rather than a worker's.
    """
    rows = []
    for f in sorted(pathlib.Path(ACTA_DIR).glob("EVID-ctrl0009-*.json")):
        try:
            row = json.loads(f.read_text())
        except ValueError:
            continue
        if (row.get("observed") or {}).get("bypass_observed") and row.get("credential") == "authenticated":
            rows.append(row)
    if not rows:
        check("an authenticated capture of the bypass scope is on record", False,
              f"this run could not observe the bypass scope ({unreadable}) and no "
              f"committed EVID-ctrl0009 row observed it either — the enforcement claim "
              f"has nothing behind it. Run this with a credential and commit the row.")
        return
    newest = max(rows, key=lambda r: r.get("checked_at", ""))
    actors = (newest.get("observed") or {}).get("bypass_actors") or []
    check("an authenticated capture of the bypass scope is on record and shows none",
          not actors,
          f"{newest['id']} ({newest.get('checked_at')}) recorded bypass actors: {actors}")
    facts["bypass_attested_by"] = newest["id"]
    facts["bypass_attested_at"] = newest.get("checked_at")


def probe(repo, branch, token):
    """Capture the live enforcement state and assert the load-bearing facts."""
    rules, err = get(f"/repos/{repo}/rules/branches/{branch}", token)
    if err:
        check(f"the enforcement state of {branch} is readable", False, err)
        return
    check(f"the enforcement state of {branch} is readable without a credential",
          True, f"{len(rules)} rule(s) apply")

    by_type = {r["type"]: r.get("parameters") or {} for r in rules}
    facts["rules"] = sorted(by_type)
    facts["ruleset_ids"] = sorted({r.get("ruleset_id") for r in rules if r.get("ruleset_id")})

    # 1 — the branch is governed at all.
    check(f"{branch} is governed by at least one rule", bool(rules), "no rules apply")

    # 2/3 — status checks are required, and by the names the claim depends on.
    sc = by_type.get("required_status_checks")
    required = [c.get("context") for c in (sc or {}).get("required_status_checks", [])]
    facts["required_contexts"] = sorted(required)
    check("merging requires status checks to pass", sc is not None,
          "no required_status_checks rule — a red suite would not block the merge")
    missing = [c for c in CLAIMED_CONTEXTS if c not in required]
    check("both conformance contexts are required by name", not missing,
          f"missing from the ruleset: {missing}; required: {required}")

    # 4 — the required names resolve to jobs that exist. A required context nothing
    # publishes never reports, which blocks silently rather than enforcing loudly.
    published = published_contexts(REPO)
    facts["published_contexts"] = sorted(published)
    unpublished = [c for c in required if c not in published]
    check("every required context is published by a workflow job", not unpublished,
          f"required but never reported: {unpublished}; published: {sorted(published)}")

    # 5 — the merge is the only way in. A required check is decoration if the branch
    # accepts a direct push.
    check("main cannot be pushed to directly (pull request required)",
          "pull_request" in by_type, "no pull_request rule: a direct push bypasses checks")
    check("main cannot be force-pushed or deleted",
          "non_fast_forward" in by_type and "deletion" in by_type,
          f"present: {sorted(by_type)}")

    # 6 — bypass scope, stated rather than assumed. "Enforced" and "enforced except
    # for four people" are different claims and only one of them is this repo's.
    ids = facts["ruleset_ids"]
    bypass, unreadable = [], []
    for rid in ids:
        detail, err = get(f"/repos/{repo}/rulesets/{rid}", token)
        actors = (detail or {}).get("bypass_actors") if detail else None
        if err or actors is None:
            unreadable.append(f"{rid}: {err or 'bypass_actors not returned'}")
        else:
            bypass += [f"{rid}:{a.get('actor_type')}:{a.get('actor_id')}" for a in actors]
    facts["bypass_actors"] = sorted(bypass) if not unreadable else None
    facts["bypass_unreadable"] = unreadable
    if not unreadable:
        facts["bypass_observed"] = True
        check("no actor may bypass the ruleset, administrators included", not bypass,
              f"bypass actors configured: {bypass}")
    else:
        # Unobserved, and said so — never assumed empty. `administration: read` is a
        # PAT scope and not a GITHUB_TOKEN workflow permission, so the Actions runner
        # cannot see this however the workflow is written. Failing here would redden
        # the required check on every run and take the merge gate down with it, which
        # is a worse outcome than a precisely stated limit.
        #
        # The claim stays whole through the Acta instead: an authenticated operator
        # capture is committed, and this run requires one to exist.
        facts["bypass_observed"] = False
        print(f"  NOTE  bypass scope unobservable with this credential ({unreadable}) — "
              f"falling back\n        to the committed authenticated capture")
        attested_bypass_check(unreadable)

    # Recorded, not asserted: real qualifications on the claim that are not failures.
    facts["strict_required_status_checks_policy"] = \
        (sc or {}).get("strict_required_status_checks_policy")
    facts["do_not_enforce_on_create"] = (sc or {}).get("do_not_enforce_on_create")
    facts["required_approving_reviews"] = \
        by_type.get("pull_request", {}).get("required_approving_review_count")
    if facts["strict_required_status_checks_policy"] is False:
        print("  NOTE  branches need not be up to date with the base before merging, so a "
              "green check\n        can describe a base the merge result never had — "
              "recorded in the evidence, not\n        failed, because it narrows the "
              "claim rather than falsifying it")


def emit(repo, branch, out_dir, token_used):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Content-addressed over the captured state, so an unchanged setting yields a
    # stable subject and a changed one is visible as a different subject (SPEC-0096).
    digest = hashlib.sha256(
        json.dumps(facts, sort_keys=True).encode()).hexdigest()[:16]
    evid = {"id": f"EVID-ctrl0009-{now[:19].replace(':', '')}", "type": "evidence",
            "scope": "platform", "state": "active", "version": "1.0.0",
            "instantiated_at": now, "author": "ctrl-0009", "authorized_by": None,
            "title": f"merge enforcement on {repo}@{branch}: "
                     f"{'configured as claimed' if not failures else 'does not match the claim'}",
            "control_ref": "CTRL-0009",
            "subject": f"github:{repo}@{branch}#ruleset:{digest}",
            "verdict": "pass" if not failures else "fail",
            "checked_at": now, "checker": "ctrl-0009-merge-enforcement",
            # Provenance of the measurement itself: which endpoints, when, and whether
            # a credential was involved — so a reader can repeat exactly this capture.
            "source": [f"GET {API}/repos/{repo}/rules/branches/{branch}"]
                      + [f"GET {API}/repos/{repo}/rulesets/{r}" for r in facts.get("ruleset_ids", [])],
            "credential": "authenticated" if token_used else "anonymous",
            "observed": facts,
            "failing": failures}
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    return evid


def default_repo():
    r = subprocess.run(["git", "-C", str(REPO), "remote", "get-url", "origin"],
                       capture_output=True, text=True)
    url = r.stdout.strip()
    if url.endswith(".git"):
        url = url[:-4]
    return "/".join(url.replace(":", "/").split("/")[-2:]) if url else "tecthulhu/republic"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None, help="owner/name (default: the origin remote)")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--evidence-dir", default="acta")
    a = ap.parse_args()
    repo = a.repo or default_repo()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    print(f"CTRL-0009 merge-enforcement probe against {repo}@{a.branch} "
          f"({'authenticated' if token else 'anonymous'})")
    probe(repo, a.branch, token)
    ev = emit(repo, a.branch, a.evidence_dir, bool(token))
    print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0009"
          f"{'' if not failures else ': ' + ', '.join(failures)}")
    print(f"evidence {ev['id']} (subject {ev['subject']})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
