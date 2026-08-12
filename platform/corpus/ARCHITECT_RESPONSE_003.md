# ARCHITECT RESPONSE 003 — evidence storage ruling; road to enactment

STORY-0001 acceptance acknowledged: CTRL-0004 green against hello-citizen
(15 pass, BASE-AC-9/17 correctly skipped per SPEC-0081 v1.1.0), the
violating fixture failing the suite as required, the run gated in CI on
protected merge. SPEC-0071/0072/0073 evidenced. PR #8 merge is the
owner's click. Dispositions D17–D20.

---

## D17 — RULING: evidence rows are records, not derived data; interim Acta is committed

The finding at the end of the report is correct and the defect is the
architect's: `.gitignore` classed all of `index/` as generated-derived,
but the index holds two different truth classes:

- **Derived** (regenerable from the corpus at any time): embedding rows,
  standing-query reports. Correctly git-ignored per ONT-016 — losing
  them loses nothing.
- **Records** (truth-at-T, ONT-014/046, born once, never regenerable):
  `EVID-` rows. Git-ignoring these was a misclassification — a record
  that lives only in an ignored directory or an expiring CI artifact is
  provenance with a countdown timer, which is not provenance. The
  report's own observation that the CI artifact expired is the symptom
  proving the ruling.

Disposition: **interim Acta directory** at `platform/acta/`, committed.
Evidence rows write there (JSON, one file per row, append-only —
filenames already carry the EVID id). `index/` keeps only derived data
and stays ignored. atom_lint learns to load `platform/acta/*.json` as
atoms for schema validation and reference resolution — evidence becomes
resolvable corpus content, which is what ONT-046/048 always implied.
CI-produced evidence is committed by the PR that produced it (the gate
job writes acta rows into the workspace; the author commits them on the
story branch) — CI artifacts may additionally exist as conveniences but
are never the record. When the real Acta consumer exists (data-access
citizen, PA-007), `platform/acta/` becomes its bootstrap backfill and
retires by decision — the interim label is explicit, per the standing
interim-posture discipline.

This is executed as SPEC-0106 under STORY-0004's successor scope (below)
— it is corpus-adjacent tooling plus a .gitignore change plus a lint
extension, story-sized.

## D18 — BLK-0001 resolution mechanics

With D17 executed, the STORY-0003 evidence rows land in
`platform/acta/`, their EVID ids resolve under lint, and BLK-0001
v1.2.0 sets `resolved_by` to the EVID row of the closing STORY-0003 run.
The blocker's whole lifecycle — raised, blocking DEC-0001, resolved by
referenced evidence — then survives in the committed record, which is
what the blocker type was for. No schema change needed; the schema was
right and the storage was wrong.

## D19 — Actions deprecation bump: own story, agreed

checkout@v4 / setup-python@v5 Node 20 deprecation: the report's instinct
is correct — it changes a gate, so it is never a drive-by. STORY-0007 is
cut below as a parked, non-blocking story; it runs whenever convenient
and its acceptance is simply the same CTRL-0004 double-fixture run green
under the bumped actions with the bump recorded as a versioned
measurement of the CI substrate.

## D20 — Sequencing to enactment, final form

1. Owner merges PR #8 (STORY-0001 lands).
2. SPEC-0106 executes: acta/ split, lint extension, evidence committed —
   including re-homing the STORY-0003/0004 and CTRL-0004 rows that
   currently exist only in ignored/expired locations and can be
   re-emitted by re-running their suites (re-runs are new true-at-T
   rows; nothing is backdated).
3. BLK-0001 v1.2.0 resolved per D18.
4. Owner signs D8: enactment commit — DEC-0001, `process_ref` = its own
   hash, org/repo named in the message, effects applied.
5. STORY-0002 opens on ratified law: the spawn contract, the risky hop,
   with BASE-AC-9/17 waiting in SPEC-0081 v1.1.0 where they belong.

---

<!-- atom:begin id=SPEC-0106 -->
```yaml
id: SPEC-0106
type: specification
scope: story:story-0004
state: deprecated
version: 1.2.0
instantiated_at: "2026-08-12T18:55:45.957379+00:00"
author: consul-architect
authorized_by: DEC-0004
title: "Interim Acta: evidence committed, derived stays ignored, EVID resolvable"
tags: [acceptance-criterion, d17]
binding: checked
check: machine
story_ref: STORY-0004
```
platform/acta/ exists and is tracked; evidence writers target it;
index/ holds only embeddings and query reports and remains ignored;
atom_lint loads acta/*.json for validation and reference resolution; a
fixture BLK- with resolved_by referencing a committed EVID row lints
green, and one referencing a nonexistent EVID id fails resolution.
STORY-0004's acceptance list gains this SPEC by story re-version.
<!-- atom:end id=SPEC-0106 -->

<!-- atom:begin id=STORY-0007 -->
```yaml
id: STORY-0007
type: story
scope: platform
state: proposed
version: 1.1.0
instantiated_at: "2026-08-11T14:50:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "CI substrate bump: actions checkout/setup-python off deprecated Node"
tags: [ci, parked, non-blocking]
tracker_ref: "gh:tecthulhu/republic#9"
acceptance: [SPEC-0107]
```
Parked until convenient; never rides another story's commit because it
changes a gate.

v1.0.0 as cut carried tracker_ref #7, which is the merged STORY-0003 pull
request: GitHub numbers issues and pull requests from one sequence, so #7 was
never available. Corrected to #9 under SPEC-0094, which owns tracker-ref
accuracy.
<!-- atom:end id=STORY-0007 -->

<!-- atom:begin id=SPEC-0107 -->
```yaml
id: SPEC-0107
type: specification
scope: story:story-0007
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T06:00:00Z"
author: consul-architect
authorized_by: null
title: "Bumped actions: double-fixture CTRL-0004 green, bump recorded"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0007
```
Under the bumped action versions, hello-citizen passes and the violating
fixture fails exactly as before; no deprecation warnings in the run log;
the action versions are recorded in the workflow as pinned versions with
the bump noted as a CI-substrate measurement change in the commit.
<!-- atom:end id=SPEC-0107 -->
