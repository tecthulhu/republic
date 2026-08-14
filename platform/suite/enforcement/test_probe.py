#!/usr/bin/env python3
"""CTRL-0009 fixture suite (SPEC-0130): the probe must be able to fail.

The live probe passes against the real repository, and a probe that only ever passes
is indistinguishable from a constant saying "enforced" — which is the exact thing
SPEC-0130 exists to rule out. So each way enforcement can be weakened is played back
through the same code path with a substituted API response, and each must go red.

No network: `get` is replaced with a table lookup, because the subject here is the
probe's judgement, not GitHub's uptime. The live capture is the other half and runs
in `run.py`.

Run from anywhere: python3 suite/enforcement/test_probe.py
"""
import contextlib
import importlib.util
import io
import json
import tempfile
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ctrl0009", HERE / "run.py")
probe_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe_mod)

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:300]}")
    if not ok:
        failures.append(name)


REAL_RULES = [
    {"type": "deletion", "ruleset_id": 1},
    {"type": "non_fast_forward", "ruleset_id": 1},
    {"type": "pull_request", "parameters": {"required_approving_review_count": 0},
     "ruleset_id": 1},
    {"type": "required_status_checks", "ruleset_id": 1, "parameters": {
        "strict_required_status_checks_policy": False,
        "do_not_enforce_on_create": True,
        "required_status_checks": [{"context": "corpus-controls"},
                                   {"context": "citizenship-conformance"}]}},
]


def acta_with(rows, td):
    """A throwaway Acta holding the given committed captures."""
    d = pathlib.Path(td)
    d.mkdir(parents=True, exist_ok=True)
    for i, r in enumerate(rows):
        (d / f"EVID-ctrl0009-fixture-{i:02d}.json").write_text(json.dumps(r))
    return d


def attested_row(bypass_actors, checked_at="2026-01-01T00:00:00Z", credential="authenticated"):
    return {"id": f"EVID-ctrl0009-{checked_at}", "checked_at": checked_at,
            "credential": credential,
            "observed": {"bypass_observed": True, "bypass_actors": list(bypass_actors)}}


def run_against(rules, bypass_actors=(), ruleset_readable=True, published=None,
                acta=None):
    """Drive the probe over a substituted API and return its findings."""
    def fake_get(path, token=None):
        if "/rules/branches/" in path:
            return (rules, None) if rules is not None else (None, "HTTP 404")
        if "/rulesets/" in path:
            if not ruleset_readable:
                return None, "HTTP 403 on rulesets"
            return {"bypass_actors": list(bypass_actors)}, None
        return None, f"unexpected path {path}"

    real_get, real_pub = probe_mod.get, probe_mod.published_contexts
    real_acta = probe_mod.ACTA_DIR
    probe_mod.get = fake_get
    if published is not None:
        probe_mod.published_contexts = lambda _root: set(published)
    if acta is not None:
        probe_mod.ACTA_DIR = acta
    probe_mod.failures, probe_mod.facts = [], {}
    try:
        # The probe narrates its own PASS/FAIL lines. Interleaved with this suite's
        # they read as this suite failing, which is the opposite of what a red line
        # inside a weakening fixture means.
        with contextlib.redirect_stdout(io.StringIO()):
            probe_mod.probe("owner/name", "main", token="t")
        return list(probe_mod.failures), dict(probe_mod.facts)
    finally:
        probe_mod.get, probe_mod.published_contexts = real_get, real_pub
        probe_mod.ACTA_DIR = real_acta
        probe_mod.failures, probe_mod.facts = [], {}


DEFAULT_PUBLISHED = ["corpus-controls", "citizenship-conformance"]

print("CTRL-0009 fixture suite — every way enforcement weakens must go red\n")

# The configuration as it actually stands must pass, or the failing cases below prove
# nothing: a probe that rejects everything is as useless as one that accepts everything.
found, facts = run_against(REAL_RULES, published=DEFAULT_PUBLISHED)
check("the real configuration passes", not found, found)
check("the qualifications are recorded, not failed",
      facts.get("strict_required_status_checks_policy") is False
      and facts.get("required_approving_reviews") == 0
      and not found,
      f"strict={facts.get('strict_required_status_checks_policy')} found={found}")

# Weakening 1 — a required check is dropped from the ruleset. This is the meta-control
# case: the actor being graded removes the binding that grades it.
dropped = [r for r in REAL_RULES if r["type"] != "required_status_checks"] + [
    {"type": "required_status_checks", "ruleset_id": 1, "parameters": {
        "required_status_checks": [{"context": "corpus-controls"}]}}]
found, _ = run_against(dropped, published=DEFAULT_PUBLISHED)
check("dropping a required context is caught",
      any("required by name" in f for f in found), found)

# Weakening 2 — the whole status-check requirement is removed.
none_required = [r for r in REAL_RULES if r["type"] != "required_status_checks"]
found, _ = run_against(none_required, published=DEFAULT_PUBLISHED)
check("removing the status-check requirement entirely is caught",
      any("requires status checks" in f for f in found), found)

# Weakening 3 — the ruleset names a context no workflow publishes. It never reports,
# so the merge button stays disabled forever and reads as pending, not as enforcement.
found, _ = run_against(REAL_RULES, published=["corpus-controls"])
check("a required context no job publishes is caught",
      any("published by a workflow job" in f for f in found), found)

# Weakening 4 — a bypass actor appears. "Enforced" and "enforced except for one team"
# are different claims.
found, facts = run_against(REAL_RULES, bypass_actors=[{"actor_type": "Team", "actor_id": 7}],
                           published=DEFAULT_PUBLISHED)
check("a bypass actor is caught", any("bypass" in f for f in found), found)
check("the bypass actor is named in the captured facts",
      facts.get("bypass_actors") == ["1:Team:7"], facts.get("bypass_actors"))

# Weakening 5 — the bypass scope cannot be read. This is the CI case and not a
# hypothetical: `administration: read` is a PAT scope, not a GITHUB_TOKEN workflow
# permission, so the runner can never see it. Silence must not become an assumption of
# emptiness; the run falls back to a committed authenticated capture and asserts
# against that, which is weaker than a live read and is recorded as such.
with tempfile.TemporaryDirectory() as td:
    clean = acta_with([attested_row([])], pathlib.Path(td, "clean"))
    found, facts = run_against(REAL_RULES, ruleset_readable=False,
                               published=DEFAULT_PUBLISHED, acta=clean)
    check("an unobservable bypass scope falls back to the committed capture",
          not found, found)
    check("the fallback is recorded as unobserved, never as observed-empty",
          facts.get("bypass_observed") is False and facts.get("bypass_actors") is None
          and facts.get("bypass_attested_by"),
          f"observed={facts.get('bypass_observed')} actors={facts.get('bypass_actors')} "
          f"attested_by={facts.get('bypass_attested_by')}")

    dirty = acta_with([attested_row(["1:Team:7"])], pathlib.Path(td, "dirty"))
    found, _ = run_against(REAL_RULES, ruleset_readable=False,
                           published=DEFAULT_PUBLISHED, acta=dirty)
    check("a committed capture showing a bypass actor is caught",
          any("bypass scope is on record" in f for f in found), found)

    empty = acta_with([], pathlib.Path(td, "empty"))
    found, _ = run_against(REAL_RULES, ruleset_readable=False,
                           published=DEFAULT_PUBLISHED, acta=empty)
    check("unobservable with no committed capture at all fails",
          any("on record" in f for f in found), found)

    # An anonymous capture is not an attestation of something anonymous runs cannot see.
    anon = acta_with([attested_row([], credential="anonymous")], pathlib.Path(td, "anon"))
    found, _ = run_against(REAL_RULES, ruleset_readable=False,
                           published=DEFAULT_PUBLISHED, acta=anon)
    check("an anonymous row does not count as an authenticated capture",
          any("on record" in f for f in found), found)

    # The newest authenticated capture governs: a later one showing a bypass actor is
    # not excused by an older clean one.
    both = acta_with([attested_row([], checked_at="2026-01-01T00:00:00Z"),
                      attested_row(["1:User:9"], checked_at="2026-06-01T00:00:00Z")],
                     pathlib.Path(td, "both"))
    found, _ = run_against(REAL_RULES, ruleset_readable=False,
                           published=DEFAULT_PUBLISHED, acta=both)
    check("the newest committed capture governs, not the cleanest",
          any("bypass scope is on record" in f for f in found), found)

# Weakening 6 — direct pushes allowed. A required check is decoration on a branch that
# accepts a push.
no_pr = [r for r in REAL_RULES if r["type"] != "pull_request"]
found, _ = run_against(no_pr, published=DEFAULT_PUBLISHED)
check("allowing direct pushes is caught",
      any("pushed to directly" in f for f in found), found)

no_ff = [r for r in REAL_RULES if r["type"] != "non_fast_forward"]
found, _ = run_against(no_ff, published=DEFAULT_PUBLISHED)
check("allowing force-push is caught",
      any("force-pushed or deleted" in f for f in found), found)

# Weakening 7 — protection removed altogether.
found, _ = run_against([], published=DEFAULT_PUBLISHED)
check("an unprotected branch is caught",
      any("governed by at least one rule" in f for f in found), found)

# And an unreadable branch state is a failure, not an empty pass.
found, _ = run_against(None, published=DEFAULT_PUBLISHED)
check("an unreadable branch state fails closed",
      any("readable" in f for f in found), found)

print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0009 fixture suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
