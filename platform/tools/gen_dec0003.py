#!/usr/bin/env python3
"""Generate DEC-0003's enumerated effects (SPEC-0112).

The ref grammar has no wildcards (ONT-016), so a decision that ratifies the
extracted corpus must enumerate it — which is exactly the kind of work a machine
should do and a human should sign. This tool writes the atom; the owner's merge
ratifies it. Machine-written, human-signed.

Scope is D31's, taken literally:
  - the REQUIREMENTS_REGISTER, CONTROLS and ENFORCEMENT_RULES atom sets
  - the story-scoped acceptance SPECs of *closed* stories

Closed-ness comes from the tracker, because the tracker is the status of record
(ONT-044) — not from a hand-maintained list here, which would be a second source of
truth for the same fact. Pass --closed to state it explicitly when the tracker is
unreachable; the value used is recorded in the decision's prose either way.

    python3 tools/gen_dec0003.py --closed STORY-0001 STORY-0003 STORY-0004 STORY-0008
"""
import argparse
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from atom_lint import corpus_digest, lint  # noqa: E402
from paths import CORPUS, SCHEMA  # noqa: E402

SCOPE_FILES = ("REQUIREMENTS_REGISTER.md", "CONTROLS.md", "ENFORCEMENT_RULES.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--closed", nargs="+", required=True,
                    help="story ids whose acceptance SPECs are in scope")
    ap.add_argument("--out", default=str(CORPUS / "DEC-0003.md"))
    a = ap.parse_args()

    atoms, errors = lint([str(CORPUS)], str(SCHEMA))
    if errors:
        print(f"refusing to generate against a red corpus: {len(errors)} finding(s)")
        for e in errors[:5]:
            print("  •", e)
        return 1

    digest = corpus_digest(atoms)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    in_registers, acceptance, skipped = [], [], []
    closed = set(a.closed)
    for aid, (atom, src, _body) in sorted(atoms.items()):
        source_file = pathlib.Path(src.split("::")[0]).name
        state = atom.get("state")
        if source_file in SCOPE_FILES:
            (in_registers if state == "proposed" else skipped).append((aid, state))
            continue
        story = atom.get("story_ref")
        if (atom.get("type") == "specification" and story in closed
                and "acceptance-criterion" in (atom.get("tags") or [])):
            (acceptance if state == "proposed" else skipped).append((aid, state))

    effects = [aid for aid, _ in in_registers] + [aid for aid, _ in acceptance]
    lines = [
        "# DEC-0003 — Activate the extracted rule set",
        "",
        "Enumerated by `tools/gen_dec0003.py` against a named corpus digest and signed",
        "by the owner's merge: machine-written, human-ratified, which is the division of",
        "labour this platform argues for. The reference grammar has no wildcards",
        "(ONT-016), so ratifying the extracted corpus means naming every atom.",
        "",
        "**This decision ratifies. It does not activate.** Activation is triggered by",
        "binding-completeness under ONT-060 and is therefore caused by the law rather",
        "than by any signature (D34); it lands in a separate commit attributed to",
        "ONT-060. A signature attests exactly its own effects.",
        "",
        f"Scope, per D31, computed at `corpus@{digest}`:",
        "",
        f"- {len(in_registers)} atoms from the extracted registers"
        f" ({', '.join(SCOPE_FILES)})",
        f"- {len(acceptance)} story-scoped acceptance specifications of closed stories"
        f" ({', '.join(sorted(closed))}), closed-ness read from the tracker (ONT-044)",
        "",
        "Open stories' acceptance stays `proposed`: a criterion activating before its",
        "story completes would be a claim standing ahead of its implementation.",
        "",
        "<!-- atom:begin id=DEC-0003 -->",
        "```yaml",
        "id: DEC-0003",
        "type: decision",
        "scope: platform",
        "state: proposed",
        # 0.x means pre-release; the ceremony writes 1.0.0 as the first
        # ratified version, so the number agrees with the lifecycle state.
        "version: 0.1.0",
        f'instantiated_at: "{now}"',
        "author: agent-worker-story-0009",
        "authorized_by: null",
        'title: "Activate the extracted rule set"',
        "tags: [activation, machine-enumerated]",
        "question: >",
        "  Does the extracted corpus — the requirements register, the controls, the",
        "  enforcement rules, and the acceptance criteria of completed stories — move",
        "  from proposed to ratified, so that the launch-readiness meters measure",
        "  ratified law instead of a definitional zero?",
        "outcome: >",
        "  Ratified as enumerated. Activation follows separately under ONT-060 where",
        "  binding-completeness holds; atoms whose binding is incomplete remain",
        "  ratified and are reported by the standing queries, which is the honest",
        "  partial state this decision exists to make legible.",
        f'process_ref: "git-merge:DEC-0003"',
        "effects:",
        "  - { target: DEC-0003, transition: ratified }",
    ]
    for aid in effects:
        lines.append(f"  - {{ target: {aid}, transition: ratified }}")
    lines += [
        "```",
        f"Enumerated against `corpus@{digest}` at {now}. Every target was `proposed` at",
        "computation time; the ceremony refuses to move anything backwards, so a target",
        "already ratified by the time this is signed is satisfied rather than re-applied.",
        "",
        f"Targets: {len(effects) + 1} atoms (including this decision, which ratifies",
        "itself as DEC-0002 does).",
        "<!-- atom:end id=DEC-0003 -->",
        "",
    ]
    pathlib.Path(a.out).write_text("\n".join(lines))
    print(f"wrote {a.out}")
    print(f"  registers:  {len(in_registers)}")
    print(f"  acceptance: {len(acceptance)}  (closed: {', '.join(sorted(closed))})")
    print(f"  effects:    {len(effects) + 1} including DEC-0003 itself")
    print(f"  digest:     corpus@{digest}")
    if skipped:
        print(f"  not proposed, so out of scope: {len(skipped)}")
        for aid, st in skipped[:6]:
            print(f"    {aid} ({st})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
