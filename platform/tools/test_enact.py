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

from enact import effects_plan, load, reconcile_plan, report  # noqa: E402
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

    p = effects_plan("DEC-9001", atoms, "2026-01-02T00:00:00Z")
    steps = {s["id"]: s for s in p["steps"]}

    # Effects: exactly the decision's enumerated targets, and nothing else (D34).
    check("every effect target becomes a transition step", len(steps) == 6, str(sorted(steps)))
    check("the effects plan proposes no activations", "activations" not in p,
          "a signed act must not carry activations")
    check("proposed -> ratified recorded with authorized_by",
          steps["SPEC-9001"]["to"] == "ratified"
          and steps["SPEC-9001"]["authorized_by"] == "DEC-9001", json.dumps(steps["SPEC-9001"]))
    # Versioning conventions: 0.x on first ratification goes to 1.0.0, else minor bump.
    check("first ratification of a 0.x atom takes it to 1.0.0",
          steps["SPEC-9001"]["version"] == "1.0.0", steps["SPEC-9001"]["version"])
    check("first ratification of a 1.x atom takes a minor bump",
          steps["SPEC-9002"]["version"] == "1.1.0", steps["SPEC-9002"]["version"])

    # Eligibility, computed by the reconciler against the post-effects corpus.
    projected = {aid: (dict(a[0]), a[1], a[2]) for aid, a in atoms.items()}
    for s in p["steps"]:
        if s["action"] == "transition":
            projected[s["id"]][0]["state"] = s["to"]
    rp = reconcile_plan(projected, "2026-01-02T00:00:00Z")
    acts = {a["id"]: a for a in rp["activations"]}
    held = {b["id"]: b for b in rp["blocked"]}

    check("a claim bound by a rule is eligible", "SPEC-9001" in acts,
          f"activations={sorted(acts)} held={sorted(held)}")
    check("a claim nothing binds is held ratified", "SPEC-9002" in held
          and "ONT-031" in held["SPEC-9002"]["reason"], json.dumps(held.get("SPEC-9002")))
    check("a control whose implementation resolves is eligible", "CTRL-9001" in acts,
          json.dumps(acts.get("CTRL-9001")))
    check("a control whose implementation does not resolve is held ratified",
          "CTRL-9002" in held and "ONT-033" in held["CTRL-9002"]["reason"],
          json.dumps(held.get("CTRL-9002")))
    check("rules and enforcements are eligible on ratification",
          "RULE-9001" in acts and "ENF-9001" in acts, f"acts={sorted(acts)}")

    # A dry run must leave the tree byte-identical.
    before = (corpus / "fixture.md").read_text()
    r = subprocess.run([sys.executable, str(PLATFORM / "tools" / "enact.py"),
                        "--decision", "DEC-9001", "--corpus", str(corpus),
                        "--dry-run", "--no-evidence"], capture_output=True, text=True)
    check("dry run exits clean", r.returncode == 0, r.stdout[-300:] + r.stderr[-300:])
    check("dry run writes nothing", (corpus / "fixture.md").read_text() == before,
          "the fixture file changed during a dry run")

    # Apply the effects. Nothing should activate: a signature ratifies, and only that.
    r = subprocess.run([sys.executable, str(PLATFORM / "tools" / "enact.py"),
                        "--decision", "DEC-9001", "--corpus", str(corpus),
                        "--apply", "--no-evidence"], capture_output=True, text=True)
    check("apply exits clean and lints green", r.returncode == 0 and "PASS" in r.stdout,
          r.stdout[-400:] + r.stderr[-400:])

    after, errors_after = load([str(corpus)])
    check("written tree lints clean", not errors_after, str(errors_after[:3]))
    states = {aid: (after[aid][0]["state"], after[aid][0]["version"]) for aid in
              ("SPEC-9001", "SPEC-9002", "CTRL-9001", "CTRL-9002", "RULE-9001", "ENF-9001")}
    check("the ceremony ratifies and activates nothing (D34)",
          all(s == "ratified" for s, _v in states.values()), json.dumps(states))
    check("authorized_by is set on ratified atoms",
          after["SPEC-9002"][0].get("authorized_by") == "DEC-9001",
          str(after["SPEC-9002"][0].get("authorized_by")))
    check("first ratification of the 0.x atom wrote 1.0.0",
          states["SPEC-9001"][1] == "1.0.0", str(states["SPEC-9001"]))

    # Reconcile: the law operating, separately attributed.
    r = subprocess.run([sys.executable, str(PLATFORM / "tools" / "enact.py"),
                        "--reconcile", "--corpus", str(corpus),
                        "--apply", "--no-evidence"], capture_output=True, text=True)
    check("reconcile exits clean and lints green", r.returncode == 0 and "PASS" in r.stdout,
          r.stdout[-400:] + r.stderr[-400:])
    rec, rec_errors = load([str(corpus)])
    check("reconciled tree lints clean", not rec_errors, str(rec_errors[:3]))
    check("SPEC-9001 is now active", rec["SPEC-9001"][0]["state"] == "active",
          str(rec["SPEC-9001"][0]["state"]))
    check("SPEC-9002 remains ratified", rec["SPEC-9002"][0]["state"] == "ratified",
          str(rec["SPEC-9002"][0]["state"]))
    check("CTRL-9001 is now active", rec["CTRL-9001"][0]["state"] == "active",
          str(rec["CTRL-9001"][0]["state"]))
    check("CTRL-9002 remains ratified — ONT-033 holds it",
          rec["CTRL-9002"][0]["state"] == "ratified", str(rec["CTRL-9002"][0]["state"]))
    check("activation is attributed to the law, not to the signer",
          rec["SPEC-9001"][0]["author"] == "ont-060-reconciliation",
          str(rec["SPEC-9001"][0]["author"]))
    check("the ratifying decision survives in authorized_by",
          rec["SPEC-9001"][0]["authorized_by"] == "DEC-9001",
          str(rec["SPEC-9001"][0].get("authorized_by")))

    # Both modes at once is a refusal, not a guess about which was meant.
    r = subprocess.run([sys.executable, str(PLATFORM / "tools" / "enact.py"),
                        "--decision", "DEC-9001", "--reconcile", "--corpus", str(corpus),
                        "--dry-run"], capture_output=True, text=True)
    check("asking for both modes is refused", r.returncode == 2, f"exit={r.returncode}")

    # Re-running either mode must converge rather than bumping versions forever.
    v_before = rec["SPEC-9001"][0]["version"]
    subprocess.run([sys.executable, str(PLATFORM / "tools" / "enact.py"),
                    "--reconcile", "--corpus", str(corpus), "--apply", "--no-evidence"],
                   capture_output=True, text=True)
    again, _ = load([str(corpus)])
    check("re-reconciling is idempotent", again["SPEC-9001"][0]["version"] == v_before,
          f"{v_before} -> {again['SPEC-9001'][0]['version']}")

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0111 ceremony suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
