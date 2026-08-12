#!/usr/bin/env python3
"""SPEC-0114: tools resolve their inputs from the repository root, not the caller's
working directory.

The regression fixture for the signing-session failure: a tool invoked from the
wrong directory failed on paths rather than on anything about the corpus. Every
tool below is run from the repository root, from platform/, and from an arbitrary
subdirectory, and must succeed identically in all three — same exit status, and for
atom-lint the same subject digest, since the corpus does not change just because the
caller stood somewhere else.

Run from anywhere: python3 tools/test_paths.py
"""
import re
import subprocess
import sys

from paths import PLATFORM, REPO

TOOLS = [
    ("atom_lint (default arg)", ["tools/atom_lint.py"]),
    ("atom_lint (bare 'corpus')", ["tools/atom_lint.py", "corpus"]),
    ("atom-lint fixtures", ["tools/test_atom_lint.py"]),
    ("one-algebra static check", ["tools/test_one_algebra.py"]),
    ("grammar property suite", ["tools/test_grammar.py"]),
]

CWDS = [("repo root", REPO), ("platform/", PLATFORM),
        ("arbitrary subdir", PLATFORM / "corpus")]

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + detail}")
    if not ok:
        failures.append(name)


def run(argv, cwd):
    return subprocess.run([sys.executable, str(PLATFORM / argv[0])] + argv[1:],
                          cwd=str(cwd), capture_output=True, text=True)


for label, argv in TOOLS:
    results = {}
    for cwd_label, cwd in CWDS:
        r = run(argv, cwd)
        results[cwd_label] = r
    ok = all(r.returncode == 0 for r in results.values())
    detail = "; ".join(f"{k}: exit={v.returncode} {v.stderr.strip()[-120:]}"
                       for k, v in results.items() if v.returncode != 0)
    check(f"{label} succeeds from all three directories", ok, detail)

# The corpus is one corpus regardless of where the caller stood: the subject digest
# must be identical across invocations. A digest that moves with cwd would mean the
# tool was reading a different set of files depending on where it was run.
digests = {}
for cwd_label, cwd in CWDS:
    r = run(["tools/atom_lint.py"], cwd)
    m = re.search(r"corpus@([0-9a-f]+)#atoms=(\d+)", r.stdout)
    digests[cwd_label] = m.groups() if m else None
check("atom-lint reports one subject digest from every directory",
      len(set(digests.values())) == 1 and None not in digests.values(), str(digests))

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0114 path-resolution suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
