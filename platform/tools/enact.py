#!/usr/bin/env python3
"""enact.py — the ceremony tool (SPEC-0111, D31).

Applies a decision's effects mechanically, then computes ONT-060 activation
eligibility across the corpus and re-versions eligible atoms. Two properties are
deliberate and load-bearing:

**Eligibility is computed, never decreed.** ONT-060 already contains the logic:
`ratified -> active` is triggered by binding completeness — a claim needs an active
rule binding it, a control needs an implementation that resolves, everything else
activates on ratification. A blanket "activate everything" would violate ONT-033
the moment it touched a control whose suite does not exist yet. Ineligible atoms
stay `ratified` and become meter lines, because the honest partial state is the
thing worth reading.

**The tool never commits.** It writes the working tree and prints a report; the
owner's PR-and-merge is the signature (PA-002, ENT-079). A tool that could commit a
ratification would be an unsigned actor performing a signed act.

Usage:
    python3 tools/enact.py --decision DEC-0003 --dry-run
    python3 tools/enact.py --decision DEC-0003 --apply
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from atom_lint import PREFIX, expand_inputs, lint, parse_file  # noqa: E402
from paths import ACTA, CORPUS, PLATFORM, SCHEMA  # noqa: E402

# Versioning conventions now on record: first ratification takes an atom to 1.0.0
# (0.x means pre-release), later transitions take a minor bump.
FIRST_RATIFIED = "1.0.0"

CLAIM_TYPES = ("specification", "restriction")

# Forward progress only (ONT-060 defines no backwards edge). Terminal states are
# absent deliberately: a decision that wants to deprecate or supersede says so as
# its own effect, and never as a side effect of re-running an older ceremony.
STATE_ORDER = {"draft": 0, "proposed": 1, "ratified": 2, "active": 3}


def load(dirs=None):
    dirs = dirs or [str(CORPUS)]
    atoms, errors = lint(dirs, str(SCHEMA))
    return atoms, errors


def ref_id(r):
    return r if isinstance(r, str) else (r or {}).get("id")


def bump(version, first_ratification):
    """Version for the instance that records a transition."""
    if first_ratification and version.startswith("0."):
        return FIRST_RATIFIED
    major, minor, patch = (version.split(".") + ["0", "0"])[:3]
    return f"{major}.{int(minor) + 1}.0"


def activation_eligible(atom, atoms, active_rule_claims):
    """ONT-060's trigger, computed. Returns (eligible, reason)."""
    t = atom.get("type")
    if t in CLAIM_TYPES:
        if atom["id"] in active_rule_claims:
            return True, "bound by an active rule"
        return False, "no active rule binds this claim (ONT-031)"
    if t == "control":
        impl = str(atom.get("implementation", ""))
        target = PLATFORM / impl.split("#")[0]
        if impl and target.exists():
            return True, f"implementation resolves: {impl}"
        return False, f"implementation does not resolve: {impl or '(none)'} (ONT-033)"
    # Rules, enforcements, principles, and the rest: ratification implies activation.
    return True, "ratification implies activation for this type"


def effects_plan(decision_id, atoms, now):
    """What a signature attests: exactly the decision's enumerated effects (D34).

    Activation is deliberately absent. ONT-060's ratified -> active trigger is
    binding-completeness, a computed property of the corpus — no decision's effects
    list contains "activate" and no signature confers it. Folding activation into a
    ceremony would record, under someone's signature, lifecycle movements the law
    caused rather than the signer. A licence signature must never read as having
    moved the ontology's lifecycle.
    """
    dec = atoms.get(decision_id)
    if dec is None:
        raise SystemExit(f"{decision_id} not found in the corpus")
    dec = dec[0]
    if dec.get("type") != "decision":
        raise SystemExit(f"{decision_id} is a {dec.get('type')}, not a decision")

    steps = []
    for eff in dec.get("effects") or []:
        tid, transition = ref_id(eff.get("target")), eff.get("transition")
        if tid not in atoms:
            steps.append({"id": tid, "action": "error",
                          "reason": f"effect target {tid} not in corpus"})
            continue
        a = atoms[tid][0]
        here, want = STATE_ORDER.get(a.get("state")), STATE_ORDER.get(transition)
        if here is not None and want is not None and here >= want:
            steps.append({"id": tid, "action": "already", "state": a.get("state")})
            continue
        steps.append({"id": tid, "action": "transition", "from": a.get("state"),
                      "to": transition,
                      "version": bump(str(a.get("version", "1.0.0")),
                                      transition == "ratified"),
                      "authorized_by": decision_id})
    return {"mode": "effects", "decision": decision_id, "steps": steps, "at": now}


def reconcile_plan(atoms, now):
    """The law operating, not an act anyone signs (D34).

    Computes ONT-060 eligibility corpus-wide and proposes ratified -> active for
    every eligible atom. Needs no fresh decision: DEC-0001's ratification of ONT-060
    is the standing authorization, and each run is that ratified law operating, on
    the record. Forward-only — demotion has no trigger in the table, and
    reconciliation must not invent one.
    """
    current = {aid: dict(a[0]) for aid, a in atoms.items()}
    # A rule reaching `ratified` in the same pass will be active by the end of it, so
    # its claim counts as bound; otherwise reaching a stable state would take two runs.
    active_rule_claims = {ref_id(a.get("claim")) for a in current.values()
                          if a.get("type") == "rule"
                          and a.get("state") in ("active", "ratified")}

    activations, blocked = [], []
    for aid, a in sorted(current.items()):
        if a.get("state") != "ratified":
            continue
        eligible, reason = activation_eligible(a, current, active_rule_claims)
        record = {"id": aid, "type": a.get("type"), "reason": reason,
                  "version": bump(str(a.get("version", "1.0.0")), False)}
        (activations if eligible else blocked).append(record)
    return {"mode": "reconcile", "steps": [], "activations": activations,
            "blocked": blocked, "at": now}


def rewrite(atom_id, new_state, new_version, authorized_by, now, atoms, author=None):
    """Edit the atom's serialized record in place in its host file.

    In-place *file* editing, not in-place *instance* editing: the prior instance
    stays addressable in git history, which is what makes history the immutability
    mechanism (PA-002). The version and timestamp move, so this is a new instance by
    ONT-015, not a mutation of the old one.
    """
    _atom, src, _body = atoms[atom_id]
    path = pathlib.Path(src.split("::")[0])
    text = path.read_text()

    if src.endswith("::frontmatter"):
        end = text.find("\n---\n", 4)
        head, rest = text[:end], text[end:]
    else:
        m = re.search(rf"<!-- atom:begin id={atom_id} -->(.*?)<!-- atom:end id={atom_id} -->",
                      text, re.S)
        block = m.group(1)
        ym = re.search(r"```yaml\n(.*?)```", block, re.S)
        head, rest = ym.group(1), None

    def set_field(body, field, value):
        pattern = rf"^{field}:.*$"
        if re.search(pattern, body, re.M):
            return re.sub(pattern, f"{field}: {value}", body, count=1, flags=re.M)
        return body.rstrip("\n") + f"\n{field}: {value}\n"

    new = set_field(head, "state", new_state)
    new = set_field(new, "version", new_version)
    new = set_field(new, "instantiated_at", f'"{now}"')
    if authorized_by:
        new = set_field(new, "authorized_by", authorized_by)
    if author:
        new = set_field(new, "author", author)

    if rest is not None:
        path.write_text(new + rest)
    else:
        path.write_text(text.replace(head, new, 1))


def report(p, verbose=True):
    if p["mode"] == "effects":
        lines = [f"ceremony plan for {p['decision']} at {p['at']}",
                 "  (effects only — activation is reconciliation's job, D34)", ""]
        lines.append(f"  effects: {len(p['steps'])}")
        for s in p["steps"]:
            if s["action"] == "transition":
                lines.append(f"    {s['id']}  {s['from']} -> {s['to']}  v{s['version']}")
            else:
                lines.append(f"    {s['id']}  ({s['action']}: "
                             f"{s.get('reason', s.get('state'))})")
        return "\n".join(lines)

    lines = [f"reconciliation plan at {p['at']}",
             "  (authorized by ONT-060 via DEC-0001; no fresh decision needed)", ""]
    lines.append(f"  activations: {len(p['activations'])}")
    if verbose:
        for a in p["activations"][:8]:
            lines.append(f"    {a['id']} ({a['type']}) — {a['reason']}")
        if len(p["activations"]) > 8:
            lines.append(f"    … and {len(p['activations']) - 8} more")
    lines.append(f"  ratified but not eligible: {len(p['blocked'])}")
    for b in p["blocked"][:12]:
        lines.append(f"    {b['id']} ({b['type']}) — {b['reason']}")
    if len(p["blocked"]) > 12:
        lines.append(f"    … and {len(p['blocked']) - 12} more")
    return "\n".join(lines)


def emit_evidence(p, applied, digest):
    now = p["at"]
    if p["mode"] == "effects":
        title = (f"{p['decision']} ceremony: {len(p['steps'])} effects applied"
                 f"{'' if applied else ' (dry run)'}")
        extra = {"decision": p["decision"],
                 "transitions": [s["id"] for s in p["steps"] if s["action"] == "transition"]}
        eid = f"EVID-enact-{now[:19].replace(':', '')}"
    else:
        title = (f"reconciliation: {len(p['activations'])} activated, "
                 f"{len(p['blocked'])} held ratified"
                 f"{'' if applied else ' (dry run)'}")
        # The authorization is the ratified lifecycle law, not a signature. Recorded
        # here so the ledger shows the law as the cause (D34).
        extra = {"authorization": "ONT-060 (ratified by DEC-0001)",
                 "activated": [a["id"] for a in p["activations"]],
                 "held_ratified": [{"id": b["id"], "reason": b["reason"]}
                                   for b in p["blocked"]]}
        eid = f"EVID-reconcile-{now[:19].replace(':', '')}"
    evid = {"id": eid, "type": "evidence", "scope": "platform", "state": "active",
            "version": "1.0.0", "instantiated_at": now,
            "author": "ont-060-reconciliation" if p["mode"] == "reconcile" else "enact-ceremony",
            "authorized_by": None, "title": title, "control_ref": "CTRL-0003",
            "subject": f"corpus@{digest}", "verdict": "pass", "checked_at": now,
            "checker": "enact-reconcile" if p["mode"] == "reconcile" else "enact-ceremony",
            "applied": applied, **extra}
    ACTA.mkdir(exist_ok=True)
    (ACTA / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    return evid


def main():
    ap = argparse.ArgumentParser(
        description="enact.py — decision ceremonies and lifecycle reconciliation")
    ap.add_argument("--decision", default=None,
                    help="apply this decision's enumerated effects (scoped, D34)")
    ap.add_argument("--reconcile", action="store_true",
                    help="compute ONT-060 eligibility corpus-wide and activate "
                         "eligible atoms; authorized by the ratified law, not by a "
                         "signature")
    ap.add_argument("--apply", action="store_true",
                    help="write the working tree (still never commits)")
    ap.add_argument("--dry-run", action="store_true", help="report only (default)")
    ap.add_argument("--no-evidence", action="store_true")
    ap.add_argument("--corpus", default=None,
                    help="corpus directory to operate on (default: the platform "
                         "corpus). Exists so the ceremony can be exercised against "
                         "fixtures.")
    a = ap.parse_args()

    if bool(a.decision) == bool(a.reconcile):
        print("choose exactly one: --decision <ID> (a signed act) or --reconcile "
              "(the law operating). They are separate commits with separate "
              "attributions — see D34.")
        return 2

    dirs = [a.corpus] if a.corpus else None
    atoms, errors = load(dirs)
    if errors:
        print(f"refusing to run over a red corpus: {len(errors)} finding(s)")
        for e in errors[:5]:
            print("  •", e)
        return 1

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = (effects_plan(a.decision, atoms, now) if a.decision
         else reconcile_plan(atoms, now))
    print(report(p))

    if [s for s in p["steps"] if s.get("action") == "error"]:
        print("\nrefusing: unresolvable effect targets")
        return 1

    from atom_lint import corpus_digest
    if not a.apply:
        print("\ndry run — nothing written. Re-run with --apply to write the tree.")
        if not a.no_evidence:
            emit_evidence(p, False, corpus_digest(atoms))
        return 0

    if p["mode"] == "effects":
        for s in p["steps"]:
            if s["action"] == "transition":
                rewrite(s["id"], s["to"], s["version"], s["authorized_by"], now,
                        atoms, author=None)
    else:
        for act in p["activations"]:
            # author moves to the reconciler: this instance is the law's record of a
            # transition it caused, not a re-authoring of the atom's content. The
            # ratifying decision stays in authorized_by, untouched.
            rewrite(act["id"], "active", act["version"], None, now, atoms,
                    author="ont-060-reconciliation")

    atoms, errors = load(dirs)
    if errors:
        print(f"\nFAIL — the written tree does not lint ({len(errors)} findings)")
        for e in errors[:5]:
            print("  •", e)
        return 1

    digest = corpus_digest(atoms)
    if not a.no_evidence:
        ev = emit_evidence(p, True, digest)
        print(f"\nevidence {ev['id']}")
    print(f"\nPASS — tree written and lints green: corpus@{digest}")
    print("committed nothing: the merge is the signature." if p["mode"] == "effects"
          else "committed nothing: commit this separately from any signed act (D34).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
