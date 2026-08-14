#!/usr/bin/env python3
"""SPEC-0129 / SPEC-0126 fixtures — the Class III attack, run and refused.

The pin is only worth having if the weakened set actually loses. So the attack is
performed here rather than described: an agent revises its own in-flight acceptance
criteria, and the grade is taken both ways. Against the corpus it passes; against the
pin it fails. If those two ever agree, this suite is measuring nothing.

Run from anywhere: python3 harness/test_baseline.py
"""
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from baseline import (  # noqa: E402
    BaselineUnanchored, build_spawn_act, grade, graded_acceptance, write_spawn_act,
)

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:280]}")
    if not ok:
        failures.append(name)


def atom(aid, atype, version="1.0.0", when="2026-01-01T00:00:00Z", **kw):
    return {"id": aid, "type": atype, "scope": "platform", "state": "proposed",
            "version": version, "instantiated_at": when, "author": "fixture",
            "authorized_by": None, "title": f"{aid} fixture", **kw}


def corpus(*atoms):
    return {a["id"]: (a, f"fixture::{a['id']}", "body") for a in atoms}


def world(spec_kw=(), story_kw=None):
    """A story with two acceptance criteria."""
    s1 = atom("SPEC-9001", "specification", binding="checked", check="machine",
              **dict(spec_kw))
    s2 = atom("SPEC-9002", "specification", binding="checked", check="machine")
    st = atom("STORY-9000", "story", acceptance=["SPEC-9001", "SPEC-9002"],
              **(story_kw or {}))
    return corpus(s1, s2, st)


print("SPEC-0129/0126 fixtures — the pin, and the attack it exists for\n")

# ---------------------------------------------------------------- SPEC-0129
with tempfile.TemporaryDirectory() as td:
    atoms = world()
    rec = write_spawn_act(build_spawn_act("STORY-9000", atoms, "harness"), td)
    check("a spawn act pins the story instance and its criteria",
          rec["story_ref"] == {"id": "STORY-9000", "version": "1.0.0",
                               "instantiated_at": "2026-01-01T00:00:00Z"}
          and len(rec["acceptance_pinned"]) == 2 and rec["acceptance_digest"],
          rec)

    # The record is a record: a later corpus edit must not reach back into it.
    before = dict(rec)
    atoms["SPEC-9001"][0]["version"] = "9.9.9"
    again = graded_acceptance("STORY-9000", atoms, td)
    check("a corpus edit after the spawn leaves the record untouched",
          again["acceptance_digest"] == before["acceptance_digest"], again)

with tempfile.TemporaryDirectory() as td:
    try:
        build_spawn_act("STORY-NOPE", corpus(), "harness")
        check("a spawn act for an unresolvable story is refused", False, "written anyway")
    except BaselineUnanchored as e:
        check("a spawn act for an unresolvable story is refused", True, str(e))

with tempfile.TemporaryDirectory() as td:
    # A criterion that resolves to nothing would pin a reference to no instance.
    atoms = corpus(atom("STORY-9000", "story", acceptance=["SPEC-MISSING"]))
    try:
        build_spawn_act("STORY-9000", atoms, "harness")
        check("a criterion resolving to nothing is refused", False, "written anyway")
    except BaselineUnanchored as e:
        check("a criterion resolving to nothing is refused", True, str(e))

# ---------------------------------------------------------------- SPEC-0126
with tempfile.TemporaryDirectory() as td:
    try:
        graded_acceptance("STORY-9000", world(), td)
        check("grading with no spawn act fails closed", False, "graded anyway")
    except BaselineUnanchored as e:
        check("grading with no spawn act fails closed", True, str(e))

# The attack, performed. An agent revises its own in-flight criterion after the spawn.
with tempfile.TemporaryDirectory() as td:
    atoms = world()
    write_spawn_act(build_spawn_act("STORY-9000", atoms, "harness"), td)

    # The agent rewrites SPEC-9001 — new instance, no floor touch — and drops SPEC-9002
    # from the story's acceptance list entirely. Both are things an agent may author.
    atoms["SPEC-9001"][0].update(version="2.0.0", instantiated_at="2026-02-01T00:00:00Z",
                                 author="agent-worker-story-9000")
    atoms["STORY-9000"][0]["acceptance"] = ["SPEC-9001"]

    base = graded_acceptance("STORY-9000", atoms, td)
    check("an agent revision does not move the graded instance",
          base["graded"]["SPEC-9001"]["version"] == "1.0.0",
          base["provenance"][0])
    check("a criterion dropped from the story is still graded",
          "SPEC-9002" in base["graded"], sorted(base["graded"]))

    # The two gradings must disagree — that disagreement is the whole mechanism.
    evidence_the_agent_produced = {"SPEC-9001"}      # only the surviving criterion
    against_pin = grade("STORY-9000", atoms, evidence_the_agent_produced, td)
    against_corpus = set(atoms["STORY-9000"][0]["acceptance"]) <= evidence_the_agent_produced
    check("the weakened set would have passed", against_corpus, "it did not pass")
    check("the pinned set fails the same evidence",
          not against_pin["satisfied"] and against_pin["missing"] == ["SPEC-9002"],
          against_pin)

# A floor touch does move the baseline — otherwise the pin would freeze the story.
with tempfile.TemporaryDirectory() as td:
    atoms = world()
    write_spawn_act(build_spawn_act("STORY-9000", atoms, "harness"), td)
    atoms["SPEC-9001"][0].update(version="2.0.0", instantiated_at="2026-03-01T00:00:00Z",
                                 authorized_by="DEC-9999")
    base = graded_acceptance("STORY-9000", atoms, td)
    check("a floor-touched revision moves the baseline",
          base["graded"]["SPEC-9001"]["version"] == "2.0.0"
          and "floor-touched" in base["provenance"][0]["basis"], base["provenance"][0])

# A criterion added after the spawn is reported, not silently graded or ignored.
with tempfile.TemporaryDirectory() as td:
    atoms = world()
    write_spawn_act(build_spawn_act("STORY-9000", atoms, "harness"), td)
    atoms["SPEC-9003"] = (atom("SPEC-9003", "specification", binding="checked",
                               check="machine"), "fixture", "body")
    atoms["STORY-9000"][0]["acceptance"] = ["SPEC-9001", "SPEC-9002", "SPEC-9003"]
    base = graded_acceptance("STORY-9000", atoms, td)
    check("a criterion added after the spawn is reported and not graded",
          base["added_since_spawn"] == ["SPEC-9003"] and "SPEC-9003" not in base["graded"],
          base["added_since_spawn"])

# The newest spawn act governs: re-spawning re-pins.
with tempfile.TemporaryDirectory() as td:
    atoms = world()
    # Both acts are stamped explicitly. Letting one take the wall clock and giving the
    # other a fixed date made the "second" act older than the first, which is a fixture
    # bug that reads exactly like an ordering bug in the code.
    first = build_spawn_act("STORY-9000", atoms, "harness")
    first["instantiated_at"] = "2026-04-01T00:00:00Z"
    write_spawn_act(first, td)
    atoms["SPEC-9001"][0].update(version="2.0.0", instantiated_at="2026-04-15T00:00:00Z",
                                 authorized_by="DEC-9999")
    second = build_spawn_act("STORY-9000", atoms, "harness")
    second["instantiated_at"] = "2026-05-01T00:00:00Z"
    second["id"] = second["id"] + "-b"
    write_spawn_act(second, td)
    atoms["SPEC-9001"][0]["authorized_by"] = None       # floor touch withdrawn later
    base = graded_acceptance("STORY-9000", atoms, td)
    check("the newest spawn act is the anchor",
          base["spawn_act"].endswith("-b")
          and base["graded"]["SPEC-9001"]["version"] == "2.0.0", base["spawn_act"])

print(f"\n{'PASS' if not failures else 'FAIL'} — SPEC-0129/0126 fixture suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
