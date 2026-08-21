#!/usr/bin/env python3
"""CTRL-0011 fixtures (SPEC-0086): the pin check must be able to fail.

It passes against the real Acta — 855 rows, one version, one binary. A check that only
ever passes against a consistent corpus is indistinguishable from a constant, so each
way the pin can stop pinning is built and must go red.

Run from anywhere: python3 tools/test_cli_pin.py
"""
import json
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import cli_pin_check as pin  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:280]}")
    if not ok:
        failures.append(name)


DOCKERFILE = 'ARG CLI_VERSION=2.1.228\nARG CLI_PLATFORM_INTEGRITY=sha512-AAAA==\n'
GOOD = {"version": "2.1.228", "platform_package": "pkg@2.1.228",
        "binary_sha256": "d" * 64}


def run(rows, dockerfile=DOCKERFILE):
    """Drive the check over a synthetic Acta and Dockerfile; return its findings."""
    with tempfile.TemporaryDirectory() as td:
        acta = pathlib.Path(td, "acta")
        acta.mkdir()
        for i, pin_row in enumerate(rows):
            body = {"id": f"EVID-fixture-{i:02d}", "type": "evidence"}
            if pin_row is not None:
                body["cli_pin"] = pin_row
            (acta / f"EVID-fixture-{i:02d}.json").write_text(json.dumps(body))
        df = pathlib.Path(td, "Dockerfile")
        df.write_text(dockerfile)
        pin.failures = []
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            pin.run(acta_dir=acta, dockerfile=df)
        return list(pin.failures)


print("CTRL-0011 fixtures — every way the pin stops pinning\n")

check("a consistent Acta passes", not run([GOOD, GOOD]), run([GOOD, GOOD]))

# The two-pin defect: a version recorded with no binary behind it.
no_binary = {"version": "2.1.228", "platform_package": "pkg@2.1.228"}
found = run([GOOD, no_binary])
check("a row with a version but no binary hash is caught",
      any("executed binary" in f for f in found), found)

# The defect SPEC-0086 v1.1.0 exists for: same version, different binary.
swapped = {**GOOD, "binary_sha256": "e" * 64}
found = run([GOOD, swapped])
check("one version resolving to two binaries is caught",
      any("exactly one binary hash" in f for f in found), found)

# A row from a different CLI version than the build declares.
old = {**GOOD, "version": "2.0.0"}
found = run([GOOD, old])
check("a row drifting from the declared version is caught",
      any("version drifts" in f for f in found), found)

# Nothing to check is not a pass (SPEC-0092).
found = run([None, None])
check("an Acta with no pin-bearing row fails rather than passing vacuously",
      any("carries a CLI pin" in f for f in found), found)

# An undeclared pin cannot be checked against, and must not default to anything.
found = run([GOOD], dockerfile="FROM scratch\n")
check("an undeclared pin fails closed", any("declares a CLI pin" in f for f in found),
      found)

print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0011 fixture suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
