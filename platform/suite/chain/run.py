#!/usr/bin/env python3
"""CTRL-0006 — the chain verifier suite (ES-040).

Two fixture sets, as DOC-0004 requires: a golden set that must verify, and a rogue set
where every member must fail. The rogue set is the load-bearing half — a verifier that
accepts everything passes a golden set perfectly.

Exercises the citizen implementation directly (`base/l0/chainverify.py`), not a model
of it: the one-algebra rule (PA-006, SPEC-0108) means there is nothing else to
exercise. No containers, no bus, no credential — this is the algebra and the walk.

Usage:
    python3 suite/chain/run.py
"""
import argparse
import copy
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "base" / "l0"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "harness"))

import mint as minting  # noqa: E402
import subjects  # noqa: E402
from chainverify import VerificationError, verify_boot, walk  # noqa: E402
from envelope import build as build_envelope, verify as verify_envelope  # noqa: E402
from keys import signer_from_seed  # noqa: E402

CITIZEN, STORY = "chain-probe", "story-0002"
failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:240]}")
    if not ok:
        failures.append(name)


def denies(fn, name, detail_on_pass="accepted what it should have refused"):
    """A rogue fixture is only evidence if the verifier says no."""
    try:
        fn()
        check(name, False, detail_on_pass)
    except VerificationError as e:
        check(name, True, str(e))
    except Exception as e:  # noqa: BLE001 — a crash is not a refusal
        check(name, False, f"raised {type(e).__name__} rather than refusing: {e}")


def minted(**kw):
    return minting.mint(CITIZEN, STORY, **kw)


def envelope_for(m, subject=None, payload="hello"):
    return build_envelope(subject or f"acta.{CITIZEN}.{STORY}.output", payload,
                          m["pubs"]["leaf"], m["chain"]["chain_head"], m["token"],
                          signer_from_seed(m["seeds"]["leaf"]), 1, payload_type="text")


# ------------------------------------------------------------------ golden
def golden():
    print("\ngolden set — these must verify")
    m = minted()
    try:
        used = verify_boot(m["chain"]["chain"], m["token"], m["pubs"]["leaf"], STORY)
        check("a well-formed chain walks to root at boot", True,
              f"depth={used.get('depth')}")
    except VerificationError as e:
        check("a well-formed chain walks to root at boot", False, str(e))

    try:
        verify_envelope(envelope_for(m), m["chain"]["chain"], {"action": "publish"})
        check("a leaf-signed envelope verifies per ES-013", True)
    except VerificationError as e:
        check("a leaf-signed envelope verifies per ES-013", False, str(e))

    # ES-021: the effective caveat set is the union along the chain, so a fresh lease
    # inside its window admits while the same chain past TTL does not (tested below).
    fresh = minted(lease_age_hours=1, lease_ttl_hours=48)
    try:
        verify_boot(fresh["chain"]["chain"], fresh["token"], fresh["pubs"]["leaf"], STORY)
        check("a lease inside its window admits", True)
    except VerificationError as e:
        check("a lease inside its window admits", False, str(e))
    return m


# ------------------------------------------------------------------- rogue
def rogue(m):
    print("\nrogue set — every one of these must fail")

    # Bad canonicalization / tampered content: the signature covers the JCS form, so
    # any edit invalidates it (ES-011).
    tampered = copy.deepcopy(m)
    tampered["token"]["minted_at"] = "2099-01-01T00:00:00Z"
    denies(lambda: verify_boot(tampered["chain"]["chain"], tampered["token"],
                               tampered["pubs"]["leaf"], STORY),
           "a token edited after signing fails (ES-011)")

    # ENT-095 / ES-020: an exception construct smuggled into a credential.
    smuggled = copy.deepcopy(m)
    smuggled["token"]["caveats"] = [{"given": "RULE-0001", "when": "x", "then": "suspend"}]
    denies(lambda: verify_boot(smuggled["chain"]["chain"], smuggled["token"],
                               smuggled["pubs"]["leaf"], STORY),
           "an exception construct inside a credential fails (ENT-095)")

    # A caveat block carrying an object rather than predicate triples.
    objectish = copy.deepcopy(m)
    objectish["token"]["caveats"] = [[{"fact": "audience", "op": "=", "value": STORY}]]
    denies(lambda: verify_boot(objectish["chain"]["chain"], objectish["token"],
                               objectish["pubs"]["leaf"], STORY),
           "a caveat block of objects rather than triples fails (ES-020)")

    # ENT-093: attenuation is algebraic. A child cannot drop an inherited caveat — the
    # union is evaluated, so removing it from the child changes nothing.
    widened = minted(lease_ttl_hours=48)
    widened["chain"]["chain"][0]["token"]["caveats"] = [[["lease_age", "<", 1]]]
    widened_expired = minting.mint(CITIZEN, STORY, lease_age_hours=5, lease_ttl_hours=48)
    widened_expired["chain"]["chain"][0]["token"]["caveats"] = [[["lease_age", "<", 1]]]
    denies(lambda: verify_boot(widened_expired["chain"]["chain"], widened_expired["token"],
                               widened_expired["pubs"]["leaf"], STORY),
           "a child cannot escape a parent caveat by omitting it (ENT-093)")

    # ENT-072: lease TTL is checked at every hop, not once at the leaf.
    expired = minted(lease_age_hours=72, lease_ttl_hours=48)
    denies(lambda: verify_boot(expired["chain"]["chain"], expired["token"],
                               expired["pubs"]["leaf"], STORY),
           "an expired lease fails at the walk (ENT-072)")

    # ENT-094: fail closed on a fact outside the vocabulary.
    unknown = minted(leaf_caveats=[[["audience", "=", STORY]], [["kind", "=", "silicon"]]])
    denies(lambda: verify_boot(unknown["chain"]["chain"], unknown["token"],
                               unknown["pubs"]["leaf"], STORY),
           "a predicate over a fact outside the vocabulary fails closed (ENT-094)")

    # ES-020: the audience binds the token to one context. Another story's leaf is not
    # this story's leaf, however valid its chain.
    denies(lambda: verify_boot(m["chain"]["chain"], m["token"], m["pubs"]["leaf"],
                               "story-9999"),
           "a token audience-bound elsewhere fails for this story (ES-020)")

    # ENT-002: a chain that does not terminate at a root is not a chain.
    rootless = copy.deepcopy(m)
    rootless["chain"]["chain"] = [n for n in rootless["chain"]["chain"] if n["id"] != "root"]
    denies(lambda: verify_boot(rootless["chain"]["chain"], rootless["token"],
                               rootless["pubs"]["leaf"], STORY),
           "a chain that never reaches root fails (ENT-002)")

    # ENT-004: authority is granted, never asserted. A token empowering a different key
    # does not empower the presenter.
    stranger = minting.mint("other-citizen", STORY)
    denies(lambda: verify_boot(m["chain"]["chain"], stranger["token"],
                               m["pubs"]["leaf"], STORY),
           "a token empowering another leaf does not empower this one (ENT-004)")

    # ES-023: single-use. The verifier evaluates use_count against the ledger's answer;
    # a second presentation is denied once the ledger reports the first.
    single = minted(leaf_caveats=[[["audience", "=", STORY]], [["use_count", "<", 1]]])
    facts_first = {"now": "2026-01-01T00:00:00Z", "leaf": single["pubs"]["leaf"],
                   "action": "boot", "audience": STORY, "subject": "", "resource": "",
                   "use_count": 0}
    try:
        walk(single["chain"]["chain"], single["token"], facts_first)
        check("a single-use token verifies on first presentation", True)
    except VerificationError as e:
        check("a single-use token verifies on first presentation", False, str(e))
    denies(lambda: walk(single["chain"]["chain"], single["token"],
                        {**facts_first, "use_count": 1}),
           "the same single-use token is denied on replay (ES-023)")

    # ES-002: the taxonomy is closed, and agentd refuses off-taxonomy subjects before
    # the bus. Checked here as the grammar it is.
    check("a subject outside the closed taxonomy is not in the grammar (ES-002)",
          not subjects.in_taxonomy("totally.invented.subject")
          and subjects.in_taxonomy(f"acta.{CITIZEN}.{STORY}.output"),
          "taxonomy accepted an invented subject")

    # An envelope signed by a key outside the chain.
    outsider = minting.mint(CITIZEN, STORY)
    forged = envelope_for(m)
    forged["sender"]["leaf"] = outsider["pubs"]["leaf"]
    denies(lambda: verify_envelope(forged, m["chain"]["chain"], {"action": "publish"}),
           "an envelope whose sender is not the signer fails (ES-013)")


# ------------------------------------------------------- projection (ES-003)
def projection():
    print("\nprojection — the transport grant is derived, never widened")
    grant = minting.transport_grant(CITIZEN, STORY)
    check("every granted subject is inside the closed taxonomy",
          all(subjects.in_taxonomy(s) for s in grant), grant)
    check("the grant names only this citizen and this story",
          all(CITIZEN in s for s in grant)
          and all(STORY in s or s.startswith("mesh.") for s in grant), grant)
    check("the grant carries no work.* or another citizen's acta.*",
          not any(s.startswith("work.") for s in grant)
          and not any("other" in s for s in grant), grant)


def emit_evidence(out_dir, rows_failed):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    module = pathlib.Path(__file__).resolve().parents[2] / "base" / "l0" / "chainverify.py"
    import hashlib
    digest = hashlib.sha256(module.read_bytes()).hexdigest()[:16]
    evid = {"id": f"EVID-ctrl0006-{now[:19].replace(':', '')}", "type": "evidence",
            "scope": "platform", "state": "active", "version": "1.0.0",
            "instantiated_at": now, "author": "ctrl-0006", "authorized_by": None,
            "title": f"chain verifier suite: golden set verified, rogue set refused "
                     f"({rows_failed} failing)",
            "control_ref": "CTRL-0006",
            "subject": f"chain-verifier@chainverify:{digest}",
            "verdict": "pass" if not rows_failed else "fail",
            "checked_at": now, "checker": "ctrl-0006-chain-suite",
            # ES-023's ledger is a data-access responsibility and data-access does not
            # exist yet, so the suite supplies use_count directly. Recorded rather than
            # implied: the predicate is proven, the ledger behind it is not.
            "posture": "use_count supplied by the suite; the replay ledger awaits "
                       "the data-access citizen (ES-023, PA-030 step 7)"}
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    return evid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence-dir", default="acta")
    a = ap.parse_args()
    print("CTRL-0006 chain verifier suite")
    m = golden()
    rogue(m)
    projection()
    ev = emit_evidence(a.evidence_dir, len(failures))
    print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0006"
          f"{'' if not failures else ': ' + ', '.join(failures)}")
    print(f"evidence {ev['id']} (subject {ev['subject']})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
