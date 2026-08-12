# ARCHITECT RESPONSE 004 — rename, enactment mechanics; dispositions D21–D25

STORY-0004 acceptance acknowledged in full: SPEC-0094–0099 plus
SPEC-0106, and BLK-0001 v1.2.0 carrying `resolved_by` against a
committed, resolvable EVID row. On merge, DEC-0001 is unblocked. The
STORY-0002 constraint noted in the report — the handoff is single-use
because init unlinks it — is correct, valuable, and worth capturing as a
MEM- atom (context_class: relevant, keywords: [handoff, single-use,
respawn]) so it survives into the STORY-0002 session's injection set.

---

## D21 — REPOSITORY RENAME: republic_semantic_mesh → republic (owner-executed, precedes enactment)

Ruled: the repository renames to `tecthulhu/republic` BEFORE enactment,
so the founding signature names the permanent home. GitHub redirects
cover all existing clones and links; governed atoms do not lean on
redirects (SPEC-0094 lineage), so:

1. Owner renames the repo in GitHub settings.
2. Worker runs one grep pass for the old name across the tree; expected
   hits are exactly: `tracker_ref` fields in STORY-0001…0008 and any
   hardcoded string in the CI workflow (the workflow should use the
   `github.repository` context and carry no literal). Prose mentions in
   correspondence files are historical record — true-at-T — and are NOT
   edited.
3. All `tracker_ref` corrections land as story re-versions in ONE commit
   under SPEC-0110 (added to STORY-0008's acceptance by story
   re-version), together with the worker's local remote update.
4. Issue numbers survive a rename unchanged; `#N` refs stay valid.

Only after SPEC-0110 is green does D22 (below) execute, with
`tecthulhu/republic` in the signing message.

## D22 — THE ENACTMENT COMMIT (owner-executed, exact mechanics)

The self-reference problem: `process_ref` = "its own hash" cannot
literally contain the hash of the commit that introduces it. Resolution:
**reference by tag, which is knowable before the commit exists.**

1. On current main (post-merge), edit in one commit:
   - `DEC-0001.md`: `state: ratified`, `authorized_by: DEC-0001`
     (self, as the founding decision), `process_ref:
     "git-tag:dec-0001-enacted"`, version → 1.1.0, fresh
     `instantiated_at`.
   - `DOC-0000_ontology.md` and `DOC-0005_entity_ontology.md`
     frontmatter: `state: ratified`, `authorized_by: DEC-0001`,
     patch-version bump, fresh `instantiated_at` (a lifecycle
     transition is a new instance per ONT-015; prior instances remain
     true-at-T in git history).
2. Commit message (your authorship, your act per ENT-79/D8):

       Enact DEC-0001: ratify the substrate corpus

       Repository: tecthulhu/republic at time of signing.
       Effects applied: DOC-0000 -> ratified, DOC-0005 -> ratified.
       Process: git-tag dec-0001-enacted marks this commit.

       Decision: DEC-0001

3. `git tag -a dec-0001-enacted -m "DEC-0001 enactment" && git push
   --follow-tags`
4. Run lint; the run's EVID row (committed to acta/ per D17) is the
   first evidence emitted under ratified law.

From that push forward the corpus is law, the pre-ratification asterisk
retires, and `dangling_claims` (active-definition) becomes a live number
instead of a definitional zero — expect it to jump as claims activate,
which is the correct behavior of the meter, not a regression.

## D23 — Issue #3 open against merged reality: close it; adopt the convention

Correct catch under ONT-044 — the tracker is the status of record, so an
open issue for evidenced-and-merged work is the tracker asserting a
falsehood. No new story needed: closing #3 is the completion act of
STORY-0003, which authorized the work. Owner or worker closes it with a
comment linking PR #7 and the closing EVID subject. Standing convention
from here, recorded in CLAUDE.md's loop at next touch: **every story
PR body carries `Closes #N`** so tracker state transitions ride the
merge, mechanically, instead of by memory.

## D24 — Duplicate caveat algebra: confirmed defect, STORY-0008

The report's framing is exact: CTRL-0002 currently proves properties
about code no citizen executes — a second implementation of the algebra
is axiom 5 in executable form, and PA-006 already rules one
implementation. Disposition (SPEC-0108): `base/l0/chainverify.py` is the
sole algebra; `tools/test_grammar.py` becomes a consumer that imports it
and runs P1–P6 against the citizen implementation; the duplicate algebra
is deleted. The property suite's evidence then attests the code that
ships, which is the entire point of CTRL-0002.

## D25 — Evidence rows and ONT-085: yes they embed; batch-with-gate is the interim posture

Ruling on the D17 follow-on. Evidence atoms are atoms; ONT-085 does not
exempt record types, and searchable provenance is half the value of the
semantic substrate ("what has failed before like this" is a retrieval
query). Mechanics (SPEC-0109):

- The embedder's discovery set extends to `platform/acta/*.json`; the
  coverage query (ONT-089) spans them.
- In bootstrap there is no streaming persistence pipeline — controls
  write acta rows directly, so synchronous embed-at-persistence cannot
  hold yet. Interim posture, explicitly labeled: **batch embedding with
  coverage-zero as the gate condition** — the standing-query report is
  the meter, and a non-empty coverage gap is a red condition for
  enactment-grade runs, satisfied by running the embedder before the
  report. ONT-085's "non-optional side effect" is honored by the gate
  until the Acta consumer (PA-007) makes it synchronous, at which point
  this posture retires by decision.
- Embedding rows for evidence remain derived (index/, ignored) — the
  record/derived split of D17 is unchanged; evidence is truth, its
  vectors are measurements of it.

---

<!-- atom:begin id=STORY-0008 -->
```yaml
id: STORY-0008
type: story
scope: platform
state: proposed
version: 1.1.0
instantiated_at: "2026-08-11T14:50:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "One algebra, embedded evidence: D23/D24 executed"
tags: [corpus-integrity, post-enactment]
tracker_ref: "gh:tecthulhu/republic#11"
acceptance: [SPEC-0108, SPEC-0109, SPEC-0110]
```
v1.1.0 corrects tracker_ref from #8, which is the merged STORY-0001 pull
request: GitHub numbers issues and pull requests from one sequence. Second
occurrence of that pattern after STORY-0007/#7, so the number is now taken
from the created issue rather than assigned at cut time.

SPEC-0110 executes pre-enactment with the rename; SPEC-0108/0109
post-enactment, pre-STORY-0002 preferred (STORY-0002's spawn gate leans
on chainverify, and the algebra should be singular before the risky hop
exercises it).
<!-- atom:end id=STORY-0008 -->

<!-- atom:begin id=SPEC-0108 -->
```yaml
id: SPEC-0108
type: specification
scope: story:story-0008
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-architect
authorized_by: DEC-0003
title: "CTRL-0002 exercises the citizen algebra; duplicate deleted"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0008
```
tools/test_grammar.py imports the algebra exclusively from
base/l0/chainverify.py; no second implementation of predicate
evaluation, union composition, or chain walk exists in the tree (static
check); P1–P6 pass against the citizen implementation; CTRL-0002's
evidence subject names the chainverify module digest.
<!-- atom:end id=SPEC-0108 -->

<!-- atom:begin id=SPEC-0109 -->
```yaml
id: SPEC-0109
type: specification
scope: story:story-0008
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-architect
authorized_by: DEC-0003
title: "Acta rows embed; coverage spans records; batch-with-gate posture recorded"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0008
```
The embedder discovers platform/acta/*.json; a fresh build yields
coverage gap zero including evidence atoms; withholding one acta row
from the index makes the gap non-empty; the interim batch-with-gate
posture is recorded as a governed posture atom naming its retirement
condition (Acta consumer synchronous pipeline, PA-007).
<!-- atom:end id=SPEC-0109 -->

<!-- atom:begin id=SPEC-0110 -->
```yaml
id: SPEC-0110
type: specification
scope: story:story-0008
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-architect
authorized_by: DEC-0003
title: "Rename executed: republic; tracker refs re-versioned in one commit"
tags: [acceptance-criterion, rename]
binding: checked
check: machine
story_ref: STORY-0008
```
The repository is tecthulhu/republic; a whole-tree grep for
republic_semantic_mesh matches only historical correspondence prose and
prior atom versions; every story's current-version tracker_ref reads
gh:tecthulhu/republic#N and each referenced issue exists; the CI
workflow contains no hardcoded repository name (uses the repository
context); whole-tree lint green after the re-version commit.
<!-- atom:end id=SPEC-0110 -->
