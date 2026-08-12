#!/usr/bin/env python3
"""SPEC-0108 static check: exactly one caveat algebra exists in the tree.

PA-006 rules a single implementation of the §9 grammar, embedded everywhere it is
needed. This check enforces that structurally so the rule cannot decay back into
two copies the next time a suite finds it convenient to have its own.

Scope per D33 — logic, not test data. Outside `base/l0/`, no module may evaluate
caveat predicates or walk credential chains. Building trees and caveat sets as
fixtures is exempt: a test that authored a tree knows its shape without walking
it. What is forbidden is a shadow oracle — anything that computes a verification
result independently in order to compare it against `chainverify`.

Run from the platform root: python3 tools/test_one_algebra.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALGEBRA_HOME = ROOT / "base" / "l0" / "chainverify.py"

# Signatures of the algebra itself, not of using it.
SIGNATURES = [
    ("operator-table over caveat comparison ops",
     re.compile(r"""["']prefix-of["']\s*:""")),
    ("predicate evaluator", re.compile(r"def\s+check_predicate\s*\(")),
    ("caveat well-formedness", re.compile(r"def\s+well_formed_caveats\s*\(")),
    ("caveat union evaluator", re.compile(r"def\s+verify_caveats\s*\(")),
    ("credential chain walk", re.compile(r"def\s+walk\s*\(")),
    ("fact vocabulary definition",
     re.compile(r"FACTS\s*=\s*(frozenset|set|\{)")),
]

# The checker exempts itself, necessarily: a file whose job is to describe the
# signatures of the algebra contains those signatures, so scanning itself makes it
# report its own vocabulary as a violation. (It did exactly that on first run — a
# prose comment quoting a signature was enough.) This is not a loophole: the
# checker implements no algebra, and the one-algebra claim is about implementations.
EXEMPT = {ALGEBRA_HOME.resolve(), pathlib.Path(__file__).resolve()}
failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + detail}")
    if not ok:
        failures.append(name)


# The algebra exists where PA-006 says it does.
check("the algebra lives in base/l0/chainverify.py", ALGEBRA_HOME.is_file(),
      f"{ALGEBRA_HOME} absent")

# Scanned roots are our own source only. Two reasons, both learned the hard way:
# third-party packages define `def walk(` freely, so scanning an installed
# environment would false-flag constantly; and a virtualenv contains files that are
# not UTF-8, which crashed the naive whole-tree read. A check that cannot be trusted
# to mean what it says is worse than no check.
SOURCE_ROOTS = ("base", "tools", "suite")
sources = [p for r in SOURCE_ROOTS for p in (ROOT / r).rglob("*.py")
           if "__pycache__" not in p.parts
           and not any(part.startswith(".") for part in p.parts)]
check("python sources discovered under " + ", ".join(SOURCE_ROOTS),
      len(sources) > 5, f"only {len(sources)} files")

for label, pattern in SIGNATURES:
    offenders = [str(p.relative_to(ROOT)) for p in sources
                 if p.resolve() not in EXEMPT
                 and pattern.search(p.read_text(encoding="utf-8", errors="replace"))]
    check(f"no second {label}", not offenders, ", ".join(offenders))

# The property suite must import the algebra rather than restate it: an import is
# the observable difference between exercising the citizen code and shadowing it.
suite = (ROOT / "tools" / "test_grammar.py").read_text()
check("CTRL-0002 imports the algebra from chainverify",
      "from chainverify import" in suite, "no import of chainverify found")
check("CTRL-0002 records the algebra digest in its subject",
      "chainverify:" in suite, "evidence subject does not name the module digest")

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0108 one-algebra static check"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
