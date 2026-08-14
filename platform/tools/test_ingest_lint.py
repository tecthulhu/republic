#!/usr/bin/env python3
"""CTRL-0010 fixture suite (SPEC-0131): every error the floor hit by hand, caught.

The lint passes against the real ingest tree, and a lint that only ever passes is a
constant saying "valid". So each error class is built as a tree and must go red, and
the corrected tree must go green — both directions, because a check that cannot
distinguish them is measuring nothing.

Run from anywhere: python3 tools/test_ingest_lint.py
"""
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import ingest_lint  # noqa: E402
from ingest_lint import coherence_findings, findings_for, scan  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:280]}")
    if not ok:
        failures.append(name)


def tree(td, files):
    """Build an ingest tree. `files` maps 'folder/name.md' -> marker (or None)."""
    root = pathlib.Path(td)
    for rel, marker in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        head = f"<!-- ingest: {marker} -->\n\n" if marker else ""
        p.write_text(f"{head}# {p.stem}\n\nbody\n")
    return findings_for(scan(root))


def fired(found, needle):
    return [f for f in found if needle in f]


print("CTRL-0010 fixture suite — the hand-made errors, mechanically caught\n")

VALID = {"proposed/A.md": "instruction", "active/B.md": "instruction",
         "executed/C.md": "decision", "parked/D.md": "plan",
         "artifacts/paper.md": "artifact"}

with tempfile.TemporaryDirectory() as td:
    check("a well-formed tree passes", not tree(td, VALID), tree(td, VALID))

# 1 — cross-state duplicate. One instruction, one state.
with tempfile.TemporaryDirectory() as td:
    found = tree(td, {**VALID, "executed/A.md": "instruction"})
    check("the same instruction in two lifecycle states is caught",
          fired(found, "present in 2 lifecycle states"), found)

with tempfile.TemporaryDirectory() as td:
    # An artifact sharing a name with an instruction is not a state duplicate:
    # artifacts/ is not a lifecycle folder, so the two are different kinds of thing.
    found = tree(td, {**VALID, "artifacts/A.md": "artifact"})
    check("a same-named artifact is not a lifecycle duplicate", not found, found)

# 2 — category error, both directions.
with tempfile.TemporaryDirectory() as td:
    found = tree(td, {**VALID, "executed/paper2.md": "artifact"})
    check("an artifact filed in a lifecycle folder is caught",
          fired(found, "does not move through the instruction lifecycle"), found)

with tempfile.TemporaryDirectory() as td:
    found = tree(td, {**VALID, "artifacts/order.md": "instruction"})
    check("an instruction filed under artifacts/ is caught",
          fired(found, "has no instruction lifecycle"), found)

# The marker itself: absent, and unrecognised.
with tempfile.TemporaryDirectory() as td:
    found = tree(td, {**VALID, "proposed/E.md": None})
    check("a file with no type marker is caught", fired(found, "no `<!-- ingest:"), found)

with tempfile.TemporaryDirectory() as td:
    found = tree(td, {**VALID, "proposed/E.md": "memo"})
    check("an unknown type marker is caught", fired(found, "unknown ingest type"), found)

with tempfile.TemporaryDirectory() as td:
    # Front matter means the front. A marker further down is not what a reader sees.
    root = pathlib.Path(td)
    (root / "proposed").mkdir(parents=True)
    (root / "proposed" / "F.md").write_text("# title\n" + "\nfiller\n" * 20
                                            + "<!-- ingest: instruction -->\n")
    found = findings_for(scan(root))
    check("a marker buried below the head is not front matter",
          fired(found, "no `<!-- ingest:"), found)

# 3 — unclassified: at the root, or in a folder nobody declared.
with tempfile.TemporaryDirectory() as td:
    root = pathlib.Path(td)
    root.mkdir(exist_ok=True)
    (root / "stray.md").write_text("<!-- ingest: instruction -->\n\n# stray\n")
    found = tree(td, VALID)
    check("a file at the ingest root is caught", fired(found, "sits at the ingest root"),
          found)

with tempfile.TemporaryDirectory() as td:
    found = tree(td, {**VALID, "maybe/G.md": "instruction"})
    check("a file in an undeclared folder is caught",
          fired(found, "is not a known ingest state"), found)

# 4 — the bulk-move case, and the honest limit of what this check can see.
with tempfile.TemporaryDirectory() as td:
    # A sweep that copies rather than moves leaves the same name in two states.
    found = tree(td, {"proposed/A.md": "instruction", "executed/A.md": "instruction",
                      "proposed/B.md": "instruction", "executed/B.md": "instruction"})
    check("a bulk move that duplicates across states is caught",
          len(fired(found, "present in 2 lifecycle states")) == 2, found)

with tempfile.TemporaryDirectory() as td:
    # But a CLEAN sweep — `mv proposed/* executed/` — leaves no duplicate. The files
    # are simply in the wrong state, and nothing structural distinguishes that from
    # work that genuinely finished. This check cannot see it, and saying otherwise
    # would be the "wildcard-safe" claim overreaching.
    found = tree(td, {"executed/A.md": "instruction", "executed/B.md": "instruction",
                      "artifacts/paper.md": "artifact"})
    check("a CLEAN sweep is invisible here — the gap SPEC-0133 closes",
          not found,
          f"expected no structural finding for a clean sweep, got: {found}")

# 5 — counts are reported, not judged.
with tempfile.TemporaryDirectory() as td:
    found = tree(td, {"active/A.md": "instruction", "active/B.md": "instruction",
                      "active/C.md": "instruction", "artifacts/p.md": "artifact"})
    check("an empty proposed/ and a crowded active/ are both legal", not found, found)

# ---------------------------------------------------------------- SPEC-0133
# State coherence. The PR resolver is substituted: the subject is the rule, not
# GitHub's uptime, and a fixture that needed a permanently-open PR to exist would rot
# the first time somebody tidied up.
def coherence(td, files, refs, pr_states):
    root = pathlib.Path(td)
    for rel, marker in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        ref = f"<!-- ingest-ref: {refs[rel]} -->\n" if rel in refs else ""
        p.write_text(f"<!-- ingest: {marker} -->\n{ref}\n# {p.stem}\n")
    real = ingest_lint.pr_state
    ingest_lint.pr_state = lambda n, repo: pr_states.get(n, (None, f"HTTP 404 for PR#{n}"))
    try:
        return coherence_findings(scan(root), "owner/name")
    finally:
        ingest_lint.pr_state = real


OPEN = {"33": ("open", None)}
MERGED = {"33": ("merged", None)}

with tempfile.TemporaryDirectory() as td:
    found = coherence(td, {"executed/A.md": "instruction"},
                      {"executed/A.md": "STORY-0017 PR#33"}, OPEN)
    check("executed/ against an OPEN pr is false-executed",
          fired(found, "false-executed"), found)

with tempfile.TemporaryDirectory() as td:
    found = coherence(td, {"executed/A.md": "instruction"},
                      {"executed/A.md": "STORY-0017 PR#33"}, MERGED)
    check("the same file, once its pr merges, is green", not found, found)

with tempfile.TemporaryDirectory() as td:
    found = coherence(td, {"active/A.md": "instruction"},
                      {"active/A.md": "PR#33"}, MERGED)
    check("active/ against a merged pr is stale-active", fired(found, "stale-active"), found)

with tempfile.TemporaryDirectory() as td:
    found = coherence(td, {"proposed/A.md": "instruction"},
                      {"proposed/A.md": "PR#33"}, OPEN)
    check("proposed/ against work already under way is caught",
          fired(found, "already open"), found)

with tempfile.TemporaryDirectory() as td:
    found = coherence(td, {"executed/A.md": "instruction"},
                      {"executed/A.md": "PR#999"}, {})
    check("an unresolvable pr fails closed rather than passing",
          fired(found, "cannot resolve"), found)

with tempfile.TemporaryDirectory() as td:
    found = coherence(td, {"executed/A.md": "instruction", "proposed/B.md": "instruction"},
                      {}, OPEN)
    check("reference-free files are exempt from state coherence", not found, found)

# A story-only reference cannot settle done-ness in THIS corpus: SPEC-0122 keeps
# stories pre-ratified while their work is in flight and after it merges, so the
# corpus would call every finished instruction unfinished. Only a claim of doneness
# is a problem; the other folders are honest about not knowing yet.
with tempfile.TemporaryDirectory() as td:
    found = coherence(td, {"executed/A.md": "instruction"},
                      {"executed/A.md": "STORY-0014"}, {})
    check("executed/ on a story-only reference is caught (no done-signal exists)",
          fired(found, "not a done-signal"), found)

with tempfile.TemporaryDirectory() as td:
    found = coherence(td, {"proposed/A.md": "instruction", "active/B.md": "instruction"},
                      {"proposed/A.md": "STORY-0014", "active/B.md": "STORY-0014"}, {})
    check("story-only references in proposed/ and active/ are fine", not found, found)

print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0010 fixture suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
