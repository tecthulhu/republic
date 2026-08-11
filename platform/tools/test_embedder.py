#!/usr/bin/env python3
"""CTRL-0007: embedder pipeline suite (SPEC-0098).

Scoped to what the B0 lexical instrument can honestly assert:
  - every index row carries the complete ONT-088 measurement tuple
  - the atom is the chunk (ONT-087): row count equals lint's parsed atom count
  - coverage (ONT-089) reads empty on a fresh build, non-empty when a row is withheld
  - no vectors in authored content (ONT-086 negative)
  - the generation digest is the instrument manifest, not the tool file (D15):
    a whitespace refactor leaves it unchanged, a parameter change moves it

Semantic-quality assertions are deliberately absent — they are unmeasurable
until a semantic instrument resolves into the band. Requires the pinned deps:
  .venv/bin/python tools/test_embedder.py
"""
import json, shutil, subprocess, sys, tempfile, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import datetime
from atom_lint import lint
from embedder import build, queries, instrument_manifest, manifest_digest, resolve_instrument, PROVENANCE_FIELDS

SCHEMA = "schemas/atoms-1.0.0.json"
failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + detail}")
    if not ok: failures.append(name)


idx, vec, M, rows = build(["corpus"])
atoms, lint_errors = lint(["corpus"], SCHEMA)

# 1 — ONT-088: full measurement provenance on every row
missing = [(r["atom_id"], f) for r in rows for f in PROVENANCE_FIELDS if not r.get(f)]
check("every row carries the ONT-088 provenance tuple", not missing, str(missing[:5]))
check("every row pins the instrument by digest",
      all(r["embedding_model_digest"] == idx["model_generation"] for r in rows),
      "rows disagree with the index generation")
check("no row carries a model literal in place of a band",
      all(r["embedding_model_band"] in ("B0", "B1", "B2", "B3") for r in rows),
      str({r["embedding_model_band"] for r in rows}))

# 2 — ONT-087: the atom is the chunk
check("row count equals lint's parsed atom count", len(rows) == len(atoms),
      f"{len(rows)} rows vs {len(atoms)} atoms")
check("row ids are exactly the parsed atom ids", {r["atom_id"] for r in rows} == set(atoms),
      "row id set differs from lint's")

# 3 — ONT-089: coverage query behaviour
rep = queries(["corpus"], idx)
check("coverage gap is empty on a fresh build", rep["embedding_coverage_gap"] == [],
      str(rep["embedding_coverage_gap"][:5]))
withheld = dict(idx, rows=[r for r in rows if r["atom_id"] != rows[0]["atom_id"]])
rep_withheld = queries(["corpus"], withheld)
check("coverage gap is non-empty when a row is withheld",
      rep_withheld["embedding_coverage_gap"] == [rows[0]["atom_id"]],
      str(rep_withheld["embedding_coverage_gap"][:5]))

# 4 — ONT-086: vectors are generated, never authored
authored = [p for p in pathlib.Path("corpus").rglob("*.md")
            if any(k in p.read_text() for k in ("\nvector:", "\nembedding:"))]
check("no vectors in authored corpus files", not authored, str(authored))
check("vectors exist in the generated index", all(isinstance(r.get("vector"), list) for r in rows),
      "index rows lack vectors")

# 5 — D15: the generation boundary is the instrument manifest, not the tool file
base = instrument_manifest("B0")
check("generation digest is a pure function of the manifest",
      resolve_instrument("B0")[1].endswith(manifest_digest(base)),
      f"{resolve_instrument('B0')[1]} vs {manifest_digest(base)}")
moved = instrument_manifest("B0", params={**base["params"], "max_features": 256})
check("a parameter change moves the generation", manifest_digest(base) != manifest_digest(moved),
      "digest unchanged across a parameter change")
check("the manifest names class, params and library version",
      all(k in base for k in ("class", "params", "library")), json.dumps(base))

with tempfile.TemporaryDirectory() as td:
    for f in ("atom_lint.py", "embedder.py"):
        shutil.copy(pathlib.Path("tools", f), pathlib.Path(td, f))
    refactored = pathlib.Path(td, "embedder.py")
    refactored.write_text(refactored.read_text() + "\n\n# whitespace refactor, no instrument change\n")
    probe = ("import sys; sys.path.insert(0, %r)\n"
             "from embedder import resolve_instrument\n"
             "print(resolve_instrument('B0')[1])\n" % td)
    r = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, cwd=".")
    check("a whitespace refactor leaves the generation unchanged",
          r.returncode == 0 and r.stdout.strip() == resolve_instrument("B0")[1],
          f"exit={r.returncode} out={r.stdout.strip()!r} err={r.stderr.strip()[:200]}")

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
evid = {"id": f"EVID-ctrl0007-{now[:19].replace(':','')}", "type": "evidence", "scope": "platform",
        "state": "active", "version": "1.0.0", "instantiated_at": now,
        "author": "ctrl-0007", "authorized_by": None,
        "title": f"embedder pipeline suite: {len(rows)} rows, {len(failures)} failure(s)",
        "control_ref": "CTRL-0007",
        "subject": f"corpus@{idx['corpus_digest']}#atoms={len(rows)}@{idx['model_generation']}",
        "verdict": "pass" if not failures else "fail", "checked_at": now, "checker": "ctrl-0007-embedder-suite"}
pathlib.Path("index").mkdir(exist_ok=True)
pathlib.Path(f"index/{evid['id']}.json").write_text(json.dumps(evid, indent=1))

print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0007 embedder pipeline suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
print(f"evidence {evid['id']} (subject {evid['subject']})")
sys.exit(1 if failures else 0)
