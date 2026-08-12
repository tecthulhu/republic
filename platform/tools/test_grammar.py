#!/usr/bin/env python3
"""CTRL-0002: grammar property suite (SPEC-0108).

P1–P6 over the caveat algebra of ENT-091–095. The algebra itself lives in
`base/l0/chainverify.py` and is imported, never restated: PA-006 rules one
implementation, and a property suite that carries its own copy proves properties
about code no citizen executes (D24). Every verdict below comes from the citizen
implementation — this module supplies inputs and expectations only.

Per D33, fixture construction is not implementation: the suite may *build*
credential trees and revocation sets, because it authored them and therefore knows
their shape. What it may not do is compute a verification result independently to
compare against `chainverify` — a shadow oracle is a second implementation wearing
a test's clothes.
"""
import datetime
import hashlib
import json
import pathlib
import random
import sys

# The algebra ships in the base image; locate it from this file rather than the
# caller's cwd (the direction SPEC-0114 generalizes to every tool).
L0 = pathlib.Path(__file__).resolve().parents[1] / "base" / "l0"
sys.path.insert(0, str(L0))

from chainverify import (  # noqa: E402  — the one algebra (PA-006)
    FACTS,
    VerificationError,
    verify_caveats,
    well_formed_caveats,
)

from paths import ACTA  # noqa: E402 — repo-root resolution (SPEC-0114)


def holds(caveats, facts):
    """Bool adapter over the citizen verifier. Not a second implementation: the
    decision is `verify_caveats`', this only converts its raising into a value."""
    try:
        verify_caveats(caveats, facts)
        return True
    except VerificationError:
        return False


def rand_pred(r):
    f = r.choice(sorted(FACTS - {"subject", "action", "resource", "audience",
                                 "parent_id", "lease_id"}))
    return [f, r.choice(["<", "<=", ">", ">=", "="]), r.randint(0, 100)]


def run():
    r = random.Random(42)
    failures = []
    N = 200000

    # P1 — attenuation monotonicity (ENT-003/093): adding caveats never grants.
    for _ in range(N // 4):
        parent = [[rand_pred(r) for _ in range(r.randint(0, 3))]]
        child = parent + [[rand_pred(r) for _ in range(r.randint(1, 3))]]
        facts = {f: r.randint(0, 100) for f in FACTS}
        if holds(child, facts) and not holds(parent, facts):
            failures.append(("P1-attenuation", parent, child, facts))
            break

    # P2 — fail closed on unknown facts (ENT-094).
    for _ in range(N // 4):
        chain = [[["unknown_fact_" + str(r.randint(0, 9)), "=", 1]]]
        if holds(chain, {f: 1 for f in FACTS}):
            failures.append(("P2-unknown-fact", chain))
            break

    # P3 — no else: a failing predicate always denies; nothing recovers it.
    for _ in range(N // 4):
        chain = [[["lease_age", "<", 10]], [rand_pred(r) for _ in range(2)]]
        facts = {f: r.randint(0, 100) for f in FACTS}
        facts["lease_age"] = 50
        if holds(chain, facts):
            failures.append(("P3-no-else", chain, facts))
            break

    # P4 — layer separation (ENT-095/ONT-057): exception constructs are not
    # representable in a credential. The verdict is well_formed_caveats'.
    layer_cases = [
        ([{"given": "RULE-0001", "when": "x", "then": "suspend"}], False),
        ([[["given", "=", "RULE-0001"]]], False),
        ([{"lease_age": ["<", 48]}], False),
        ([[["action", "=", "read"]]], True),
        ([[["lease_age", "<", 48], ["action", "in", ["read"]]]], True),
    ]
    for caveats, expected in layer_cases:
        if well_formed_caveats(caveats) != expected:
            failures.append(("P4-layer-separation", caveats, expected))
    # A malformed caveat set must also deny outright, not merely report unwell.
    if holds([{"given": "RULE-0001", "then": "suspend"}], {f: 1 for f in FACTS}):
        failures.append(("P4-malformed-denies",))

    # P5 — downward revocation (ENT-051): revoking a node kills its subtree only.
    #
    # Fixture-only by D33. `chainverify` implements no revocation, so there is no
    # citizen oracle to consult and nothing to duplicate: the tree and the
    # expectations are both this suite's own data. Recorded honestly — this
    # property attests a design rule, not shipped behaviour, and it converts to a
    # real check when revocation lands in the verifier.
    tree = {"root": None, "persona": "root", "lease": "persona",
            "leafA": "lease", "leafB": "lease", "sibling": "persona"}

    def reachable_from_revoked(node, revoked):
        while node is not None:
            if node in revoked:
                return True
            node = tree[node]
        return False

    revoked = {"lease"}
    expected_dead = {"leafA", "leafB", "lease"}
    actual_dead = {n for n in tree if reachable_from_revoked(n, revoked)}
    if actual_dead != expected_dead:
        failures.append(("P5-revocation-fixture", sorted(actual_dead)))

    # SPEC-0120 — the revocation posture, checked so it cannot linger as stale prose.
    # P5 above tests a tree this suite built, because the verifier has no revocation
    # surface to test. Asserting that absence makes the posture self-retiring: when
    # STORY-0011 implements revocation this fails, forcing the posture's supersession
    # instead of leaving a false claim of behaviour-attestation standing.
    import chainverify as _cv
    revocation_surface = [n for n in dir(_cv)
                          if "revoke" in n.lower() or "revocation" in n.lower()]
    if revocation_surface:
        failures.append(("SPEC-0120-posture-stale", revocation_surface,
                         "chainverify now exposes revocation: supersede SPEC-0120 and "
                         "move P5 onto the verifier (SPEC-0118)"))

    # P6 — the decay ladder is expressible in the vocabulary (ENT-074).
    ladder = [[["lease_age", "<", 48]],
              [["lease_age", "<", 72], ["action", "=", "read"]]]
    fresh = {**{f: 0 for f in FACTS}, "lease_age": 10, "action": "write"}
    stale = {**{f: 0 for f in FACTS}, "lease_age": 60, "action": "read"}
    dead = {**{f: 0 for f in FACTS}, "lease_age": 80, "action": "read"}
    if (not holds([ladder[0]], fresh) or holds(ladder, fresh)
            or not holds([ladder[1]], stale) or holds([ladder[1]], dead)):
        failures.append(("P6-decay",))

    # SPEC-0108: the evidence subject names the algebra that was actually exercised,
    # so a change to chainverify is visibly a change to what CTRL-0002 attested.
    module_digest = hashlib.sha256((L0 / "chainverify.py").read_bytes()).hexdigest()[:16]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    evid = {"id": f"EVID-grammar-{now[:19].replace(':', '')}", "type": "evidence",
            "scope": "platform", "state": "active", "version": "1.0.0",
            "instantiated_at": now, "author": "ctrl-0002", "authorized_by": None,
            "title": f"grammar property suite over the citizen algebra "
                     f"(chainverify@{module_digest})",
            "control_ref": "CTRL-0002",
            "subject": f"caveat-algebra@ENT-091..095#chainverify:{module_digest}",
            "verdict": "pass" if not failures else "fail", "checked_at": now,
            "checker": "ctrl-0002-grammar-suite"}
    ACTA.mkdir(exist_ok=True)
    (ACTA / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))

    print(f"properties P1–P6 over ~{N} generated cases against "
          f"chainverify@{module_digest}: {'PASS' if not failures else 'FAIL'}")
    for f in failures:
        print("  •", f)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    run()
