# ARCHITECT RESPONSE 002 — dispositions for STORY-0003 report

STORY-0003 standing: SPEC-0092 and SPEC-0093 accepted as green; the
fixture suite on the previously-vacuous invocation and the
environment-scoped embedder evidence are exactly what was asked. BLK-0001
cut and STORY-0003 v1.1.0 accepted. SPEC-0091's deletion list is
**approved as tabled** — root DOC-0002/0003/0004, DEC-0001, ONTOLOGY,
ENTITY_ONTOLOGY, SPAWN_CONTRACT_STORIES deleted with platform/corpus
winning unconditionally, plus platform/CLAUDE.md deleted per D4. The
permission gate is the owner's to click, and stopping at it was correct;
owner: approve the `git rm` when relayed.

Findings 1–7 dispositioned as D9–D16. One new story (STORY-0004) carries
everything not closable inside STORY-0003, so STORY-0003 closes on
SPEC-0091's execution without scope creep. DOC-0006 is delivered
alongside this response (`DOC-0006_liveness_extension.md`, frontmatter
already carrying `instantiated_at`) — commit it under STORY-0004 /
SPEC-0099.

---

## D9 — Finding 1 (D5 re-versioning had no story): correct; STORY-0004 / SPEC-0094

"No work without a story" applied to the architect's own directive —
right call. The SPEC-0072 v1.1.0 / SPEC-0081 v1.1.0 amendments execute
under SPEC-0094, not as a drive-by.

## D10 — Finding 2 (blocker field mismatch): schema wins, prose amended

Both texts are mine; the schema's `blocks_refs` is the later, deliberate
encoding and the correct one — a field named `blocks` would shadow the
`blocks` relation type, and one token meaning two things in the same
vocabulary is a defect waiting to be automated. Ruling: `blocks_refs`
stands; DOC-0000 §4.3 blocker prose is amended to match under
SPEC-0095. BLK-0001 as cut (schema-conformant) is already correct.

## D11 — Finding 3 (evidence subject digests IDs, not content): confirmed defect

An evidence subject that doesn't change when content changes cannot
anchor "current evidence against current subject" (ONT-046/080), and it
made D1's environment-independence accidental — both observations
correct. Fix under SPEC-0096: subject digest = sha256 over the sorted
sequence of (id, version, canonical-serialized atom body) — content-
addressed, so any textual change to any governed atom moves the digest.
Historical evidence rows stand as true-at-T against their stated
subjects; no backfill (the HO-5 pattern: no rewriting history to match
improved instruments).

## D12 — Finding 4 (dangling_claims overcounts vs. definition): implement the definition, add the bootstrap line

ONT-031/080 define the query over `active` claims; the implementation
counts all states. The definition stands — pre-ratification, the true
active-dangling count is zero, and the query should say so. But the
bootstrap-phase signal is real and useful, so SPEC-0097 requires both
lines, explicitly labeled: `dangling_claims` (per definition, active
only) and `dangling_claims_all_states` (bootstrap visibility). Two
different questions, two names — never one number wearing two meanings.

## D13 — Finding 5 (LIVENESS_EXTENSION missing): delivered with this response

Confirmed: the document existed only in the drafting session's delivery
outputs and never reached the repo — a delivery omission compounding the
D2 premise error. `DOC-0006_liveness_extension.md` accompanies this
response; commit as `platform/corpus/DOC-0006_liveness_extension.md`
under SPEC-0099. It enters at `draft` (DEC-0001's effects do not touch
it; PA-021 keeps the suite parked); ENT-080's citation becomes
resolvable-to-a-draft, which is legal — references resolve to instances
regardless of state.

## D14 — Finding 6 (CTRL-0007 has no implementation): build the minimal honest suite

Correct per ONT-033: CTRL-0007 cannot reach `active` with a dangling
implementation ref. SPEC-0098 delivers `tools/test_embedder.py` scoped to
what the B0 instrument can honestly assert: every index row carries the
complete ONT-088 provenance tuple; per-atom chunking matches lint's
parse (row count == parsed atom count); coverage query returns empty
against a fresh build and non-empty when a row is withheld; vectors are
absent from all authored files (ONT-086 negative). Semantic-quality
assertions are explicitly out of scope until a semantic instrument
resolves into the band.

## D15 — Finding 7 (tool edit moved the model generation): correct behavior, boundary needs narrowing

The digest moving when the tool changed is the versioned-measurement
discipline working — but hashing the whole tool file makes every
refactor a re-embedding campaign, which conflates *instrument identity*
with *harness code*. Ruling, folded into SPEC-0098: the generation
digest narrows to the instrument boundary — vectorizer class +
parameters + library version (and, later, model digest for semantic
instruments) — serialized and hashed as the instrument manifest. Tool
refactors that don't touch the manifest don't move the generation;
anything that does move it is a real instrument change requiring
re-embedding, as it should. The current B0 rows re-embed once under the
manifest-based digest and that churn ends.

## D16 — Sequencing to enactment (restated with this round folded in)

1. Owner approves SPEC-0091 deletions → STORY-0003 evidence green →
   BLK-0001 `resolved_by` set.
2. STORY-0004 executes (SPEC-0094…0099) — all corpus-text and tool
   corrections land pre-ratification so the ratified corpus is whole.
3. Repo transfer to the tecthulhu org happens before tracker refs are
   corrected; SPEC-0094 writes `gh:tecthulhu/republic_semantic_mesh#N`
   once, and the three issues are created there.
4. Owner signs D7 (Wolfi recommended) and D8 → enactment commit,
   `process_ref` = its own hash, effects applied.
5. STORY-0001 resumes on ratified law.

---

## Cut: STORY-0004 and acceptance

<!-- atom:begin id=STORY-0004 -->
```yaml
id: STORY-0004
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T00:00:00Z"
author: consul-architect
authorized_by: null
title: "Pre-ratification corrections: findings 1–7 of report 002"
tags: [corpus-integrity, pre-ratification]
tracker_ref: "gh:tecthulhu/republic_semantic_mesh#4"
acceptance: [SPEC-0094, SPEC-0095, SPEC-0096, SPEC-0097, SPEC-0098, SPEC-0099]
```
Carries every correction surfaced by worker report 002 that STORY-0003
does not cover, so STORY-0003 closes clean and the corpus DEC-0001
ratifies is whole. Tracker ref assumes the tecthulhu transfer (D16-3);
if the transfer is deferred, this ref is corrected in the same commit
that corrects the others.
<!-- atom:end id=STORY-0004 -->

<!-- atom:begin id=SPEC-0094 -->
```yaml
id: SPEC-0094
type: specification
scope: story:story-0004
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T00:00:00Z"
author: consul-architect
authorized_by: null
title: "D5 amendments executed; tracker refs corrected to the real repo"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0004
```
SPEC-0072 v1.1.0 narrows to BASE-AC-15/16; SPEC-0081 v1.1.0 absorbs
BASE-AC-9/17; SPRINT-0001 gate prose names the full seventeen.
STORY-0001/0002/0003/0004 tracker_ref values point at the repo's actual
org/name and the referenced issues exist.
<!-- atom:end id=SPEC-0094 -->

<!-- atom:begin id=SPEC-0095 -->
```yaml
id: SPEC-0095
type: specification
scope: story:story-0004
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T00:00:00Z"
author: consul-architect
authorized_by: null
title: "Blocker field reconciled: schema blocks_refs wins, prose amended"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0004
```
DOC-0000 §4.3 blocker delta reads blocks_refs; no governed text
describes a blocker field named blocks; lint plus a grep fixture confirm
no field/relation name collision remains in the vocabulary.
<!-- atom:end id=SPEC-0095 -->

<!-- atom:begin id=SPEC-0096 -->
```yaml
id: SPEC-0096
type: specification
scope: story:story-0004
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T00:00:00Z"
author: consul-architect
authorized_by: null
title: "Evidence subjects are content-addressed"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0004
```
atom_lint's subject digest hashes the sorted sequence of (id, version,
canonical atom body); a fixture edits one atom's prose without touching
ids and demonstrates the digest moves. Historical evidence rows are not
rewritten.
<!-- atom:end id=SPEC-0096 -->

<!-- atom:begin id=SPEC-0097 -->
```yaml
id: SPEC-0097
type: specification
scope: story:story-0004
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T00:00:00Z"
author: consul-architect
authorized_by: null
title: "Dangling query per definition plus labeled bootstrap line"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0004
```
Standing report emits dangling_claims (active-state claims only, per
ONT-031) and dangling_claims_all_states as a separately named line;
pre-ratification the former reads zero and the latter carries today's
23-class signal.
<!-- atom:end id=SPEC-0097 -->

<!-- atom:begin id=SPEC-0098 -->
```yaml
id: SPEC-0098
type: specification
scope: story:story-0004
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T00:00:00Z"
author: consul-architect
authorized_by: null
title: "CTRL-0007 suite exists; instrument-manifest generation boundary"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0004
```
tools/test_embedder.py exists and passes: full ONT-088 tuple per row,
row count equals parsed atom count, coverage query empty/non-empty
behavior, ONT-086 negative. Generation digest derives from the
instrument manifest (class + parameters + library version), not the tool
file hash; a whitespace refactor of embedder.py leaves the generation
unchanged and a parameter change moves it.
<!-- atom:end id=SPEC-0098 -->

<!-- atom:begin id=SPEC-0099 -->
```yaml
id: SPEC-0099
type: specification
scope: story:story-0004
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T00:00:00Z"
author: consul-architect
authorized_by: null
title: "DOC-0006 delivered; ENT-080 citation resolves"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0004
```
platform/corpus/DOC-0006_liveness_extension.md exists, lints green, and
whole-tree resolution finds no unresolvable document citations; DOC-0006
remains state draft and no DEC-0001 effect references it.
<!-- atom:end id=SPEC-0099 -->
