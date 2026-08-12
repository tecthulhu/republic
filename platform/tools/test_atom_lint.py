#!/usr/bin/env python3
"""atom-lint fixture suite (SPEC-0092, SPEC-0095, SPEC-0096).

SPEC-0092: file arguments parse; empty input fails closed.
SPEC-0095: no `blocks` field/relation name collision in the vocabulary.
SPEC-0096: evidence subjects are content-addressed.
Run from the platform root: python3 tools/test_atom_lint.py

This is a self-test of CTRL-0001's implementation, not a governed control: it
emits no evidence of its own. Its subject is the checker, not the corpus.
"""
import json, re, shutil, subprocess, sys, tempfile, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from atom_lint import lint, corpus_digest

from paths import ACTA, PLATFORM, SCHEMA as SCHEMA_PATH  # noqa: E402
SCHEMA = str(SCHEMA_PATH)
VACUOUS = str(PLATFORM / "tools" / "fixtures" / "vacuous.md")
SINGLE = str(PLATFORM / "corpus" / "MEMORIES_SEED.md")
CORPUS_DIR = str(PLATFORM / "corpus")
LINT = str(PLATFORM / "tools" / "atom_lint.py")
failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + detail}")
    if not ok: failures.append(name)


# A — a file argument parses that file, not zero (previously: rglob over a file → 0 atoms)
atoms, errors = lint([SINGLE], SCHEMA)
# Asserts the file's atoms are parsed, not an exact count. The seed file legitimately
# gains atoms, and a fixture that breaks when the corpus grows is testing the wrong
# thing: what matters is that a file argument yields that file's contents, not zero.
check("file argument parses the file", "MEM-0001" in atoms and len(atoms) >= 1,
      f"parsed {len(atoms)} atoms: {sorted(atoms)}")
check("valid atom file yields no findings", not errors, str(errors[:3]))

# B — zero atoms is a finding, not a pass
atoms, errors = lint([VACUOUS], SCHEMA)
check("vacuous file parses zero atoms", len(atoms) == 0, f"parsed {sorted(atoms)}")
check("zero atoms raises empty-input", any("empty-input" in e for e in errors), str(errors))

# C — the previously-vacuous invocation, end to end: non-zero exit, FAIL evidence row
# The row is located by mtime, not by name-diffing: EVID- ids are second-granular,
# so a run landing in the same second as a previous one reuses its filename. That
# collision is a real defect against ONT-046 (evidence is append-only) and is
# reported, not worked around — this test simply must not depend on it.
r = subprocess.run([sys.executable, LINT, VACUOUS], capture_output=True, text=True)
check("vacuous invocation exits non-zero", r.returncode != 0, f"exit={r.returncode}\n{r.stdout}")
rows = sorted(ACTA.glob("EVID-lint-*.json"), key=lambda p: p.stat().st_mtime)
if not rows:
    check("vacuous invocation emits an evidence row", False, "no EVID- row in index/")
else:
    row = json.loads(rows[-1].read_text())
    check("evidence verdict is fail", row.get("verdict") == "fail", json.dumps(row))
    check("evidence reason is empty-input", row.get("reason") == "empty-input", json.dumps(row))
    check("evidence subject carries the atom count", row.get("subject", "").endswith("#atoms=0"),
          row.get("subject", ""))

# D — the corpus itself still lints clean through the changed code path
atoms, errors = lint([CORPUS_DIR], SCHEMA)
check("corpus still parses and passes", len(atoms) > 100 and not errors,
      f"{len(atoms)} atoms, {len(errors)} findings: {errors[:3]}")

# E — SPEC-0095: no field/relation name collision on `blocks`
FIELD_DECL = re.compile(r"^\s*blocks:\s", re.M)
offenders = [str(p) for p in (PLATFORM / "corpus").rglob("*.md") if FIELD_DECL.search(p.read_text())]
check("no governed text declares a blocker field named `blocks`", not offenders, str(offenders))
blk = [a for a, *_ in [(v[0],) for v in atoms.values()] if a.get("type") == "blocker"]
check("blocker atoms carry blocks_refs", blk and all("blocks_refs" in a and "blocks" not in a for a in blk),
      json.dumps(blk))
with tempfile.TemporaryDirectory() as td:
    pathlib.Path(td, "bad.md").write_text(
        "<!-- atom:begin id=BLK-9999 -->\n```yaml\n"
        "id: BLK-9999\ntype: blocker\nscope: platform\nstate: active\nversion: 1.0.0\n"
        'instantiated_at: "2026-01-01T00:00:00Z"\nauthor: fixture\nauthorized_by: null\n'
        'title: "misnamed impediment field"\nraised_by: fixture\nblocks: [DEC-0001]\n'
        "escalation: platform-owner\n```\n<!-- atom:end id=BLK-9999 -->\n")
    _, errs = lint([td], SCHEMA)
    check("a blocker using `blocks` fails lint", any("blocks_refs" in e for e in errs), str(errs))

# F — SPEC-0096: the evidence subject is content-addressed
with tempfile.TemporaryDirectory() as td:
    shutil.copytree(CORPUS_DIR, pathlib.Path(td, "corpus"))
    a1, e1 = lint([f"{td}/corpus"], SCHEMA)
    before = corpus_digest(a1)
    seed = pathlib.Path(td, "corpus", "MEMORIES_SEED.md")
    seed.write_text(seed.read_text().replace(
        "Learned during first lint run", "Learned during the first lint run"))
    a2, e2 = lint([f"{td}/corpus"], SCHEMA)
    after = corpus_digest(a2)
    check("prose-only edit leaves the id set unchanged", sorted(a1) == sorted(a2), "id set moved")
    check("prose-only edit moves the subject digest", before != after, f"{before} == {after}")
    check("identical content yields a stable digest", corpus_digest(a2) == after, "digest is unstable")

# G — SPEC-0106: committed evidence rows are resolvable references
acta_rows = sorted(ACTA.glob("EVID-*.json")) if ACTA.is_dir() else []
check("acta/ holds committed evidence rows", bool(acta_rows), "no EVID- rows under acta/")
atoms, errors = lint([CORPUS_DIR, str(ACTA)], SCHEMA)
evid_atoms = [a for a, *_ in ((v[0],) for v in atoms.values()) if a.get("type") == "evidence"]
check("evidence rows load as atoms and validate", bool(evid_atoms) and not errors,
      f"{len(evid_atoms)} evidence atoms, {len(errors)} findings: {errors[:3]}")

if acta_rows:
    real_evid = json.loads(acta_rows[-1].read_text())["id"]
    blk = ("<!-- atom:begin id=BLK-9998 -->\n```yaml\n"
           "id: BLK-9998\ntype: blocker\nscope: platform\nstate: active\nversion: 1.0.0\n"
           'instantiated_at: "2026-01-01T00:00:00Z"\nauthor: fixture\nauthorized_by: null\n'
           'title: "resolved_by fixture"\nraised_by: fixture\nblocks_refs: [DEC-0001]\n'
           "escalation: platform-owner\nresolved_by: %s\n```\n<!-- atom:end id=BLK-9998 -->\n")
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(CORPUS_DIR, pathlib.Path(td, "corpus"))
        shutil.copytree(str(ACTA), pathlib.Path(td, "acta"))
        pathlib.Path(td, "corpus", "blk_fixture.md").write_text(blk % real_evid)
        _, errs = lint([f"{td}/corpus", f"{td}/acta"], SCHEMA)
        check("blocker resolved_by a committed EVID row lints green",
              not any("BLK-9998" in e for e in errs), str([e for e in errs if "BLK-9998" in e]))
        pathlib.Path(td, "corpus", "blk_fixture.md").write_text(blk % "EVID-does-not-exist-0000")
        _, errs = lint([f"{td}/corpus", f"{td}/acta"], SCHEMA)
        check("blocker resolved_by a nonexistent EVID id fails resolution",
              any("EVID-does-not-exist-0000" in e for e in errs), str(errs[:2]))

# Evidence must not drift the subject digest: a record of a check is not the thing
# checked. Adding a row leaves the corpus subject exactly where it was.
with tempfile.TemporaryDirectory() as td:
    shutil.copytree(CORPUS_DIR, pathlib.Path(td, "corpus"))
    shutil.copytree(str(ACTA), pathlib.Path(td, "acta"))
    a1, _ = lint([f"{td}/corpus", f"{td}/acta"], SCHEMA)
    d1 = corpus_digest(a1)
    pathlib.Path(td, "acta", "EVID-fixture-9999.json").write_text(json.dumps({
        "id": "EVID-fixture-9999", "type": "evidence", "scope": "platform", "state": "active",
        "version": "1.0.0", "instantiated_at": "2026-01-01T00:00:00Z", "author": "fixture",
        "authorized_by": None, "title": "digest stability fixture", "control_ref": "CTRL-0001",
        "subject": "fixture", "verdict": "pass", "checked_at": "2026-01-01T00:00:00Z",
        "checker": "fixture"}))
    a2, _ = lint([f"{td}/corpus", f"{td}/acta"], SCHEMA)
    check("a new evidence row does not move the corpus subject digest",
          corpus_digest(a2) == d1 and "EVID-fixture-9999" in a2,
          f"{d1} -> {corpus_digest(a2)}")

print(f"\n{'PASS' if not failures else 'FAIL'} — atom-lint fixture suite (SPEC-0092/0095/0096/0106)"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
