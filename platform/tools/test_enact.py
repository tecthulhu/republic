#!/usr/bin/env python3
"""SPEC-0111 fixture suite for the ceremony tool.

A purpose-built fixture corpus exercises every transition class in one pass,
including the case the ruling cares most about: a control whose implementation does
not resolve must be left `ratified`, never forced `active`, because ONT-033 says a
control that cannot be invoked is not an active control. A ceremony that activated
it anyway would produce a green meter over a check that cannot run.

Run from anywhere: python3 tools/test_enact.py
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from enact import load, plan, report  # noqa: E402
from paths import PLATFORM  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + detail}")
    if not ok:
        failures.append(name)


def atom(aid, typ, extra, state="proposed", version="1.0.0", authorized_by="null"):
    # A ratified atom must carry authorized_by (schema, ONT-010): the fixture has to
    # be a legal corpus, or the ceremony rightly refuses to run over it.
    lines = [f"id: {aid}", f"type: {typ}", "scope: platform", f"state: {state}",
             f"version: {version}", 'instantiated_at: "2026-01-01T00:00:00Z"',
             "author: fixture", f"authorized_by: {authorized_by}", f'title: "fixture {aid}"'] + extra
    return (f"<!-- atom:begin id={aid} -->\n```yaml\n" + "\n".join(lines)
            + f"\n```\nfixture body\n<!-- atom:end id={aid} -->\n")


FIXTURE = "".join([
    # The decision under ceremony: it ratifies a claim, two controls, and a rule.
    atom("DEC-9001", "decision", [
        "question: fixture", "outcome: fixture",
        "effects:",
        "  - { target: SPEC-9001, transition: ratified }",
        "  - { target: SPEC-9002, transition: ratified }",
        "  - { target: CTRL-9001, transition: ratified }",
        "  - { target: CTRL-9002, transition: ratified }",
        "  - { target: RULE-9001, transition: ratified }",
        "  - { target: ENF-9001, transition: ratified }",
    ], state="ratified", authorized_by="DEC-9001"),
    # A claim that a rule binds -> should activate.
    atom("SPEC-9001", "specification", ["binding: checked", "check: machine"], version="0.1.0"),
    # A claim nothing binds -> must stay ratified (ONT-031).
    atom("SPEC-9002", "specification", ["binding: checked", "check: machine"]),
    # A control whose implementation exists -> should activate.
    atom("CTRL-9001", "control", ["target: codebase", "implementation: tools/atom_lint.py"]),
    # A control whose implementation does not resolve -> must stay ratified (ONT-033).
    atom("CTRL-9002", "control", ["target: runtime", "implementation: suite/does-not-exist"]),
    atom("ENF-9001", "enforcement", ["on_fail: block-merge"]),
    atom("RULE-9001", "rule", ["claim: SPEC-9001", "control: CTRL-9001",
                               "enforcement: ENF-9001"]),
])


def fixture_corpus(td):
    d = pathlib.Path(td, "corpus")
    d.mkdir(parents=True)
    (d / "fixture.md").write_text(FIXTURE)
    return d


with tempfile.TemporaryDirectory() as td:
    corpus = fixture_corpus(td)
    atoms, errors = load([str(corpus)])
    check("fixture corpus lints clean", not errors, str(errors[:3]))

    p = plan("DEC-9001", atoms, "2026-01-02T00:00:00Z")
    steps = {s["id"]: s for s in p["steps"]}
    acts = {a["id"]: a for a in p["activations"]}
    held = {b["id"]: b for b in p["blocked"]}

    # Effects
    check("every effect target becomes a transition step", len(steps) == 6, str(sorted(steps)))
    check("proposed -> ratified recorded with authorized_by",
          steps["SPEC-9001"]["to"] == "ratified"
          and steps["SPEC-9001"]["authorized_by"] == "DEC-9001", json.dumps(steps["SPEC-9001"]))
    # Versioning conventions: 0.x on first ratification goes to 1.0.0, else minor bump.
    check("first ratification of a 0.x atom takes it to 1.0.0",
          steps["SPEC-9001"]["version"] == "1.0.0", steps["SPEC-9001"]["version"])
    check("first ratification of a 1.x atom takes a minor bump",
          steps["SPEC-9002"]["version"] == "1.1.0", steps["SPEC-9002"]["version"])

    # Activation eligibility — the heart of D31.
    check("a claim bound by a rule activates", "SPEC-9001" in acts,
          f"activations={sorted(acts)} held={sorted(held)}")
    check("a claim nothing binds is held ratified", "SPEC-9002" in held
          and "ONT-031" in held["SPEC-9002"]["reason"], json.dumps(held.get("SPEC-9002")))
    check("a control whose implementation resolves activates", "CTRL-9001" in acts,
          json.dumps(acts.get("CTRL-9001")))
    check("a control whose implementation does not resolve is held ratified",
          "CTRL-9002" in held and "ONT-033" in held["CTRL-9002"]["reason"],
          json.dumps(held.get("CTRL-9002")))
    check("rules and enforcements activate on ratification",
          "RULE-9001" in acts and "ENF-9001" in acts, f"acts={sorted(acts)}")

    # A dry run must leave the tree byte-identical.
    before = (corpus / "fixture.md").read_text()
    r = subprocess.run([sys.executable, str(PLATFORM / "tools" / "enact.py"),
                        "--decision", "DEC-9001", "--corpus", str(corpus),
                        "--dry-run", "--no-evidence"], capture_output=True, text=True)
    check("dry run exits clean", r.returncode == 0, r.stdout[-300:] + r.stderr[-300:])
    check("dry run writes nothing", (corpus / "fixture.md").read_text() == before,
          "the fixture file changed during a dry run")

    # Apply, then verify the written tree.
    r = subprocess.run([sys.executable, str(PLATFORM / "tools" / "enact.py"),
                        "--decision", "DEC-9001", "--corpus", str(corpus),
                        "--apply", "--no-evidence"], capture_output=True, text=True)
    check("apply exits clean and lints green", r.returncode == 0 and "PASS" in r.stdout,
          r.stdout[-400:] + r.stderr[-400:])

    after, errors_after = load([str(corpus)])
    check("written tree lints clean", not errors_after, str(errors_after[:3]))
    states = {aid: (after[aid][0]["state"], after[aid][0]["version"]) for aid in
              ("SPEC-9001", "SPEC-9002", "CTRL-9001", "CTRL-9002", "RULE-9001", "ENF-9001")}
    check("SPEC-9001 is active", states["SPEC-9001"][0] == "active", str(states["SPEC-9001"]))
    check("SPEC-9002 remains ratified", states["SPEC-9002"][0] == "ratified",
          str(states["SPEC-9002"]))
    check("CTRL-9001 is active", states["CTRL-9001"][0] == "active", str(states["CTRL-9001"]))
    check("CTRL-9002 remains ratified", states["CTRL-9002"][0] == "ratified",
          str(states["CTRL-9002"]))
    check("authorized_by is set on ratified atoms",
          after["SPEC-9002"][0].get("authorized_by") == "DEC-9001",
          str(after["SPEC-9002"][0].get("authorized_by")))
    check("versions moved on every transition",
          all(v != "1.0.0" or aid == "SPEC-9001" for aid, (s, v) in states.items()),
          json.dumps(states))
    # Re-running must converge rather than bumping versions forever.
    r2 = subprocess.run([sys.executable, str(PLATFORM / "tools" / "enact.py"),
                         "--decision", "DEC-9001", "--corpus", str(corpus),
                         "--apply", "--no-evidence"], capture_output=True, text=True)
    again, _ = load([str(corpus)])
    check("re-running the ceremony is idempotent for already-active atoms",
          again["SPEC-9001"][0]["version"] == after["SPEC-9001"][0]["version"],
          f"{after['SPEC-9001'][0]['version']} -> {again['SPEC-9001'][0]['version']}")

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0111 ceremony suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
