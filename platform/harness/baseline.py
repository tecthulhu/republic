#!/usr/bin/env python3
"""The acceptance baseline (SPEC-0129, SPEC-0126) — STORY-0014.

SPEC-0122 lets a spawn run against a pre-ratified story, and SPEC-0123 leaves agent
authorship mandate-unbounded. Each is correct alone. Composed, they open the Class III
hole: an agent authors a weakening of its own in-flight acceptance criteria, the gate
grades the work against whatever the corpus currently says, and green passes against
criteria no human ever touched. Every individual signal stays green — the authorship
is valid, the story resolves, the gate graded the specs it found, the merge passed —
and the absent property is *a human authorized what passing means*.

Two halves, and the order matters.

**SPEC-0129, the spawn act.** The gate resolved a story and then forgot: it minted,
injected, started a container, and persisted nothing about the criteria the work was
authorized against. A pin layered on that would compute a baseline from an empty set
and grade against it — a green check standing in for a property that is not there. So
a spawn now writes an immutable record of the story instance it resolved to and the
acceptance-spec instances in force at that moment. It is a record, not derived data:
committed under `acta/` (D17), because a baseline recomputed at grading time from
whatever the corpus currently says is not a baseline.

**SPEC-0126, the pin.** Grading resolves each criterion to its last floor-touched
instance — the instance the spawn act pinned, or a later one carrying a floor
ratification. Agent revisions after the spawn stay in the corpus and are refused
nothing; they simply do not move what the work is graded against.

*"Floor-touched" is read narrowly and deliberately:* an acceptance-spec instance is
floor-touched when it carries a non-null `authorized_by` — the durable trace of a
ratifying act, whose signature is the owner's merge (PA-002/ENT-079) — or when it is
the instance a spawn act pinned. This is **not** unified with STORY-0010's
human-evidence primitive. Both mean "a human deliberately touched this", but a floor
touch is a ratification and human evidence is an evidence record, and two accidental
mechanisms for one idea is the anti-pattern the floor warned about.
"""
import datetime
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

from paths import ACTA  # noqa: E402

SPAWN_ACT_PREFIX = "PROV-spawn-"


class BaselineUnanchored(Exception):
    """No spawn act pins this story's criteria, so there is nothing to grade against.

    A refusal, never a fallback. Grading against "whatever the corpus currently says"
    is precisely the behaviour the pin exists to remove, so the absence of an anchor
    must stop the grader rather than quietly restore the thing it replaced.
    """


def instance_of(atom):
    """The identity of a published instance: what makes it *this* one (ONT-015)."""
    return {"id": atom["id"], "version": str(atom.get("version", "")),
            "instantiated_at": str(atom.get("instantiated_at", ""))}


def acceptance_digest(pinned):
    """One digest over the pinned instance identities, order-independent."""
    return hashlib.sha256(
        json.dumps(sorted(pinned, key=lambda p: p["id"]),
                   sort_keys=True).encode()).hexdigest()[:16]


def ref_id(r):
    return r if isinstance(r, str) else (r or {}).get("id")


# ------------------------------------------------------------------ SPEC-0129
def build_spawn_act(story_id, atoms, actor):
    """The record a spawn must leave: what story, at what instance, against what
    criteria. Raises if the story does not resolve — a record of a spawn that could
    not happen would be a false provenance entry."""
    entry = atoms.get(story_id)
    if entry is None or entry[0].get("type") != "story":
        raise BaselineUnanchored(
            f"{story_id!r} resolves to no story atom — refusing to write a spawn act "
            f"for a spawn that cannot lawfully happen (SPEC-0122)")
    story = entry[0]
    pinned = []
    for r in story.get("acceptance") or []:
        aid = ref_id(r)
        spec = atoms.get(aid)
        if spec is None:
            raise BaselineUnanchored(
                f"{story_id} names acceptance criterion {aid} that resolves to nothing "
                f"— the baseline would pin a reference to no instance")
        pinned.append(instance_of(spec[0]))

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "id": f"{SPAWN_ACT_PREFIX}{story['id']}-{now[:19].replace(':', '')}",
        "type": "provenance-link", "scope": "platform", "state": "active",
        "version": "1.0.0", "instantiated_at": now,
        "author": actor, "authorized_by": None,
        "title": f"spawn act: {story['id']} pinned at v{story.get('version')} "
                 f"with {len(pinned)} acceptance instance(s)",
        "directive": f"spawn against {story['id']}",
        "actor": actor,
        "story_ref": instance_of(story),
        # The pinned instances, and a digest over them so a reader can compare two
        # spawn acts without diffing lists.
        "artifacts": [f"{p['id']}@{p['version']}@{p['instantiated_at']}" for p in pinned],
        "acceptance_pinned": pinned,
        "acceptance_digest": acceptance_digest(pinned),
    }


def write_spawn_act(record, acta_dir=None):
    out = pathlib.Path(acta_dir or ACTA)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{record['id']}.json").write_text(json.dumps(record, indent=1))
    return record


def spawn_acts_for(story_id, acta_dir=None):
    """Every spawn act pinning this story, oldest first."""
    out = []
    for f in sorted(pathlib.Path(acta_dir or ACTA).glob(f"{SPAWN_ACT_PREFIX}*.json")):
        try:
            rec = json.loads(f.read_text())
        except ValueError:
            continue
        if ref_id(rec.get("story_ref")) == story_id:
            out.append(rec)
    return sorted(out, key=lambda r: r.get("instantiated_at", ""))


# ------------------------------------------------------------------ SPEC-0126
def graded_acceptance(story_id, atoms, acta_dir=None):
    """The criteria this story's work is graded against, and where each came from.

    Three cases per criterion, and the middle one is the whole point:

    - **floor-touched since the spawn** — the current instance carries a non-null
      `authorized_by`, so a ratifying act moved the baseline. Graded against current.
    - **revised by an agent since the spawn** — the current instance differs from the
      pinned one and carries no floor touch. Graded against the **pinned** instance;
      the revision stays in the corpus and moves nothing.
    - **untouched** — pinned and current are the same instance.

    A criterion the current story lists but no spawn act pinned is *not* graded: a
    story cannot enlarge or replace its own criteria mid-flight. It is reported, so
    the addition is visible rather than silently ignored.
    """
    acts = spawn_acts_for(story_id, acta_dir)
    if not acts:
        raise BaselineUnanchored(
            f"no spawn act pins {story_id} — grading would fall back to whatever the "
            f"corpus currently says, which is the behaviour the pin replaces "
            f"(SPEC-0126). Spawn against the story, or record the act.")
    act = acts[-1]
    pinned = {p["id"]: p for p in act.get("acceptance_pinned", [])}

    graded, provenance = {}, []
    for aid, pin in sorted(pinned.items()):
        entry = atoms.get(aid)
        current = instance_of(entry[0]) if entry else None
        touched = bool(entry and entry[0].get("authorized_by"))
        if current == pin:
            graded[aid], why = pin, "unchanged since the spawn act pinned it"
        elif touched:
            graded[aid], why = current, (
                f"floor-touched: authorized_by={entry[0].get('authorized_by')}")
        else:
            graded[aid], why = pin, (
                f"revised to v{(current or {}).get('version')} with no floor touch — "
                f"graded against the pinned v{pin['version']}")
        provenance.append({"id": aid, "graded": graded[aid], "basis": why,
                           "pinned": pin, "current": current})

    story = atoms.get(story_id)
    listed = {ref_id(r) for r in ((story[0].get("acceptance") if story else []) or [])}
    added = sorted(listed - set(pinned))
    return {"story": story_id, "spawn_act": act["id"],
            "acceptance_digest": act.get("acceptance_digest"),
            "graded": graded, "provenance": provenance,
            # Reported, never silently dropped: a criterion appearing after the spawn
            # is either a floor act that needs a fresh pin, or the attack.
            "added_since_spawn": added}


def grade(story_id, atoms, evidence_ids, acta_dir=None):
    """Green only when every *graded* criterion has evidence. The set is the pinned
    one, so weakening the corpus cannot shrink what has to be satisfied."""
    base = graded_acceptance(story_id, atoms, acta_dir)
    have = set(evidence_ids)
    missing = sorted(a for a in base["graded"] if a not in have)
    return {**base, "satisfied": not missing, "missing": missing}
