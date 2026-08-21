#!/usr/bin/env python3
"""CTRL-0011 — the CLI pin check (SPEC-0086).

SPEC-0086 says the agent CLI is a *versioned measurement*: pinned, and re-verified on
every bump. The pin has ridden every evidence row this platform emits since STORY-0002
and nothing has ever asserted it. It was the deliberate unbound claim — named in
DEC-0005, carried openly in `unbound_claims`, and deferred twice. This is its control.

**What "pinned" means here, and why it is the binary and not the package version.**
The CLI is an npm wrapper whose real executable is a platform-specific optional
dependency, so pinning the wrapper leaves the binary floating. SPEC-0086 v1.1.0 settled
that the pin is *the executed binary's hash* — and the binary hash is measured at build,
not declarable in the Dockerfile. So the check works both ways round: declaration
against measurement for the version, and measurement against measurement for the
binary, since one declared version must resolve to exactly one binary. A wrapper bump
that silently swaps the executable is then a finding rather than a version string that
still looks right.

The check is deliberately narrow. It does not run the CLI, start a container, or reach
the network: it compares the declaration in the build to the measurement in the record.
A control that had to boot a citizen to check a pin would not run in the tree gate, and
a pin nobody checks in the tree gate is the state this control exists to end.

Usage:
    python3 tools/cli_pin_check.py [--evidence-dir acta]
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from paths import ACTA, PLATFORM  # noqa: E402

DOCKERFILE = PLATFORM / "base" / "agent" / "Dockerfile"
# What the build *declares*: the version and the platform package's npm integrity.
# The executed binary's sha256 is *measured* at build and recorded into the image, so
# it is not declarable here — and that asymmetry is the whole of SPEC-0086's problem.
# A declared version can stay fixed while the binary underneath it changes, which is
# exactly the two-pin defect v1.1.0 closed by ruling that the pin is the binary.
#
# So the check compares declaration to measurement where it can, and measurement to
# measurement where it cannot: every row at a given declared version must agree on the
# binary hash. Two rows that agree on the version and disagree on the binary are the
# defect, caught without needing the Dockerfile to state a value the build computes.
DECLARED = {
    "version": re.compile(r'^\s*ARG\s+CLI_VERSION=([^\s]+)', re.M),
    "platform_integrity": re.compile(r'^\s*ARG\s+CLI_PLATFORM_INTEGRITY=(sha\d+-[^\s]+)', re.M),
}
failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:280]}")
    if not ok:
        failures.append(name)
    return ok


def declared_pin(dockerfile=None):
    """The pin the build declares. Absent file or absent field is a finding, never a
    default — a check that invents the value it is checking against passes always."""
    p = pathlib.Path(dockerfile or DOCKERFILE)
    if not p.is_file():
        return None, f"no agent Dockerfile at {p}"
    text = p.read_text()
    found = {}
    for field, pattern in DECLARED.items():
        m = pattern.search(text)
        if not m:
            return None, f"{p.name} declares no {field} — the pin is not declared, so no row can be checked against it"
        found[field] = m.group(1)
    return found, None


def rows_with_pin(acta_dir=None):
    """Evidence rows that carry a `cli_pin`. Rows that carry none are out of scope:
    the corpus controls do not spawn a citizen and have no pin to report."""
    out = []
    for f in sorted(pathlib.Path(acta_dir or ACTA).rglob("EVID-*.json")):
        try:
            row = json.loads(f.read_text())
        except ValueError:
            continue
        if isinstance(row.get("cli_pin"), dict):
            out.append((f.name, row["cli_pin"]))
    return out


def run(acta_dir=None, dockerfile=None):
    declared, err = declared_pin(dockerfile)
    if not check("the build declares a CLI pin", declared is not None, err):
        return

    print(f"  declared: v{declared['version']} integrity "
          f"{declared['platform_integrity'][:24]}…")
    rows = rows_with_pin(acta_dir)

    # SPEC-0092's law: a check over nothing is not a pass. If no row carries a pin, the
    # claim that every row carries it is unsupported rather than satisfied.
    if not check("at least one evidence row carries a CLI pin", bool(rows),
                 "no EVID- row carries cli_pin — nothing to check the declaration against"):
        return
    print(f"  {len(rows)} row(s) carry a pin")

    missing = [n for n, p in rows if not p.get("binary_sha256")]
    check("every pin-bearing row records the executed binary's hash", not missing,
          f"{len(missing)} row(s) carry a pin with no binary_sha256: {missing[:3]} — "
          f"a package version without the binary hash is the two-pin defect SPEC-0086 "
          f"v1.1.0 closed")

    # The binary is measured, not declared, so the invariant is agreement: one declared
    # version must map to exactly one binary. A second hash under the same version means
    # the pin stopped pinning while the version string kept looking correct.
    by_version = {}
    for n, pin in rows:
        if pin.get("binary_sha256"):
            by_version.setdefault(pin.get("version"), {}).setdefault(
                pin["binary_sha256"], []).append(n)
    split = {v: {h: len(ns) for h, ns in hs.items()}
             for v, hs in by_version.items() if len(hs) > 1}
    check("each declared CLI version maps to exactly one binary hash", not split,
          f"a version resolves to more than one binary — the pin is not pinning: {split}")
    for v, hs in sorted(by_version.items()):
        for h, ns in hs.items():
            print(f"  v{v} -> {h[:16]}…  ({len(ns)} row(s))")

    ver_drift = [(n, p.get("version")) for n, p in rows
                 if p.get("version") and p["version"] != declared["version"]]
    check("no row's CLI version drifts from the declared pin", not ver_drift,
          f"{len(ver_drift)} row(s): {ver_drift[:3]} against declared {declared['version']}")


def emit(out_dir):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    declared, _err = declared_pin()
    rows = rows_with_pin()
    evid = {"id": f"EVID-ctrl0011-{now[:19].replace(':', '')}", "type": "evidence",
            "scope": "platform", "state": "active", "version": "1.0.0",
            "instantiated_at": now, "author": "ctrl-0011", "authorized_by": None,
            "title": f"CLI pin: declaration and {len(rows_with_pin())} pin-bearing row(s) "
                     f"{'agree' if not failures else 'disagree'}",
            "control_ref": "CTRL-0011",
            "subject": f"cli-pin@v{(declared or {}).get('version', 'undeclared')}",
            "verdict": "pass" if not failures else "fail",
            "checked_at": now, "checker": "ctrl-0011-cli-pin",
            "declared": declared, "failing": failures}
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    return evid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence-dir", default=str(ACTA))
    ap.add_argument("--no-evidence", action="store_true")
    a = ap.parse_args()
    print("CTRL-0011 CLI pin check (SPEC-0086)")
    run()
    if not a.no_evidence:
        ev = emit(a.evidence_dir)
        print(f"  evidence {ev['id']} (subject {ev['subject']})")
    print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0011"
          f"{'' if not failures else ': ' + ', '.join(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
