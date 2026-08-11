#!/usr/bin/env python3
"""SPEC-0092 fixture suite: atom-lint accepts file arguments and fails closed on
empty input. Run from the platform root: python3 tools/test_atom_lint.py

This is a self-test of CTRL-0001's implementation, not a governed control: it
emits no evidence of its own. Its subject is the checker, not the corpus.
"""
import json, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from atom_lint import lint

SCHEMA = "schemas/atoms-1.0.0.json"
VACUOUS = "tools/fixtures/vacuous.md"
SINGLE = "corpus/MEMORIES_SEED.md"
failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + detail}")
    if not ok: failures.append(name)


# A — a file argument parses that file, not zero (previously: rglob over a file → 0 atoms)
atoms, errors = lint([SINGLE], SCHEMA)
check("file argument parses the file", len(atoms) == 1 and "MEM-0001" in atoms,
      f"parsed {len(atoms)} atoms: {sorted(atoms)}")
check("valid single-atom file yields no findings", not errors, str(errors[:3]))

# B — zero atoms is a finding, not a pass
atoms, errors = lint([VACUOUS], SCHEMA)
check("vacuous file parses zero atoms", len(atoms) == 0, f"parsed {sorted(atoms)}")
check("zero atoms raises empty-input", any("empty-input" in e for e in errors), str(errors))

# C — the previously-vacuous invocation, end to end: non-zero exit, FAIL evidence row
before = {p.name for p in pathlib.Path("index").glob("EVID-lint-*.json")} if pathlib.Path("index").is_dir() else set()
r = subprocess.run([sys.executable, "tools/atom_lint.py", VACUOUS], capture_output=True, text=True)
check("vacuous invocation exits non-zero", r.returncode != 0, f"exit={r.returncode}\n{r.stdout}")
new = [p for p in pathlib.Path("index").glob("EVID-lint-*.json") if p.name not in before]
if not new:
    check("vacuous invocation emits an evidence row", False, "no new EVID- row in index/")
else:
    row = json.loads(sorted(new)[-1].read_text())
    check("evidence verdict is fail", row.get("verdict") == "fail", json.dumps(row))
    check("evidence reason is empty-input", row.get("reason") == "empty-input", json.dumps(row))
    check("evidence subject carries the atom count", row.get("subject", "").endswith("#atoms=0"),
          row.get("subject", ""))

# D — the corpus itself still lints clean through the changed code path
atoms, errors = lint(["corpus"], SCHEMA)
check("corpus still parses and passes", len(atoms) > 100 and not errors,
      f"{len(atoms)} atoms, {len(errors)} findings: {errors[:3]}")

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0092 fixture suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
