#!/usr/bin/env python3
"""SPEC-0127 fixtures — every non-floor edit to in-flight criteria, flagged.

The check deliberately does not judge whether an edit *weakens*, so the fixtures have
to prove two things that pull against each other: that it fires on edits a weakening
would hide behind (a pure rewrite changing nothing a grader notices), and that it stays
silent where editing is ordinary work (a floor-touched revision, a story not in flight).

A check that fired on everything and a check that fired on nothing would both look
green in a suite that only tested one direction.

Run from anywhere: python3 tools/test_acceptance_edit.py
"""
import json
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import atom_lint  # noqa: E402
from atom_lint import acceptance_edit_findings, atom_content_hash  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:280]}")
    if not ok:
        failures.append(name)


def spec(aid, story, body="the criterion, as pinned", version="1.0.0",
         authorized_by=None, title="fixture criterion"):
    return {"id": aid, "type": "specification", "scope": "platform", "state": "proposed",
            "version": version, "instantiated_at": "2026-01-01T00:00:00Z",
            "author": "agent-worker", "authorized_by": authorized_by, "title": title,
            "binding": "checked", "check": "machine", "story_ref": story}, body


def story_atom(sid, state="proposed"):
    return {"id": sid, "type": "story", "scope": "platform", "state": state,
            "version": "1.0.0", "instantiated_at": "2026-01-01T00:00:00Z",
            "author": "fixture", "authorized_by": None, "title": f"{sid} fixture",
            "acceptance": ["SPEC-9101"]}


def run(before_pairs, after_pairs, story_state="proposed", spawn_act=True):
    """Drive the check over a before/after corpus with a controlled Acta."""
    with tempfile.TemporaryDirectory() as td:
        acta = pathlib.Path(td)
        if spawn_act:
            (acta / "PROV-spawn-fixture.json").write_text(json.dumps({
                "id": "PROV-spawn-fixture", "type": "provenance-link",
                "story_ref": {"id": "STORY-9100", "version": "1.0.0",
                              "instantiated_at": "2026-01-01T00:00:00Z"},
                "acceptance_pinned": [{"id": "SPEC-9101", "version": "1.0.0",
                                       "instantiated_at": "2026-01-01T00:00:00Z"}]}))
        real = atom_lint.ACTA
        atom_lint.ACTA = acta
        try:
            atoms = {a["id"]: (a, f"fixture::{a['id']}", b)
                     for a, b in list(after_pairs) + [(story_atom("STORY-9100",
                                                                  story_state), "")]}
            before = {a["id"]: (a, b) for a, b in before_pairs}
            return acceptance_edit_findings(atoms, before)
        finally:
            atom_lint.ACTA = real


print("SPEC-0127 fixtures — the pending-floor-touch flag\n")

PINNED = spec("SPEC-9101", "STORY-9100")

# No change at all: silence.
check("an untouched criterion is not flagged",
      not run([PINNED], [PINNED]), run([PINNED], [PINNED]))

# A substantive edit with no floor touch: flagged.
edited = spec("SPEC-9101", "STORY-9100", body="the criterion, quietly relaxed",
              version="2.0.0")
found = run([PINNED], [edited])
check("a non-floor edit to in-flight criteria is flagged",
      any("pending floor touch" in f for f in found), found)

# A PURE REWRITE — same requirement, different words. This is the case a "does it
# weaken?" oracle would wave through, and the reason this check refuses to judge.
reworded = spec("SPEC-9101", "STORY-9100",
                body="The criterion, as pinned.", version="2.0.0")
found = run([PINNED], [reworded])
check("a pure rewrite is flagged too — the check does not judge weakening",
      any("pending floor touch" in f for f in found),
      f"content hash moved: "
      f"{atom_content_hash(PINNED[0], PINNED[1]) != atom_content_hash(*reworded)}; {found}")

# A floor-touched revision: clean. The mechanism must not obstruct the very act it
# exists to require.
touched = spec("SPEC-9101", "STORY-9100", body="revised under a decision",
               version="2.0.0", authorized_by="DEC-9999")
check("a floor-touched revision is clean", not run([PINNED], [touched]),
      run([PINNED], [touched]))

# A story that is not in flight: ordinary corpus work, left alone.
check("an edit on a concluded story is left alone",
      not run([PINNED], [edited], story_state="active"),
      run([PINNED], [edited], story_state="active"))

# A story with no spawn act is not in flight here — and that is not a hole, because
# SPEC-0126 refuses to grade it at all. The two checks divide the space.
check("a story with no spawn act is not policed by this check",
      not run([PINNED], [edited], spawn_act=False),
      run([PINNED], [edited], spawn_act=False))

# A criterion appearing after the spawn: a story may not enlarge its own criteria.
added = spec("SPEC-9102", "STORY-9100", body="a criterion nobody pinned")
found = run([PINNED], [PINNED, added])
check("a criterion added mid-flight is flagged as unpinnable",
      any("SPEC-9102" in f and "enlarge its own criteria" in f for f in found), found)

# And the flag names what to do about it, not merely that something happened.
found = run([PINNED], [edited])
check("the finding names the atom, the story, and the remedy",
      found and "SPEC-9101" in found[0] and "STORY-9100" in found[0]
      and "authorized_by" in found[0], found)

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0127 fixture suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
