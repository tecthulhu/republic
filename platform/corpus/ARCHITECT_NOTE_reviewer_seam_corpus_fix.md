# ARCHITECT NOTE — closing the reviewers' seam in the corpus (two governed items)

**2026-08-13 — chat-plane — for the republic dev agent — authorizes nothing until admitted and ratified**

Independent reviewers (whitepaper round) cross-checked the repository against the
paper and found a seam: the paper describes postures the corpus does not declare.
The paper-side fix (language: "no story, no spawn" → "no *resolvable* story, no
spawn") is delivered separately. This note supplies the **republic-side** fix —
two governed atoms so the corpus carries the postures the paper describes, rather
than the paper asserting governance that exists nowhere in the corpus (a
two-sources-of-truth seam, the class the program rules against).

Both are small. Fold them into STORY-0010's window or cut as their own item.
Neither blocks the approved queue.

## Why these exist

At HEAD, STORY-0002 and SPEC-0081–0086 read `proposed / authorized_by: null`
while their acceptance is green and merged. That is serialization lag — activation
is caused by `enact.py --reconcile`, not by the merge (D34) — and the reconcile
pass (queue step 1) moves them. But the reviewers correctly surfaced two facts the
corpus does not currently *declare*:

1. The spawn gate admits a spawn against a **resolvable** story, not a **ratified**
   one. This is correct and necessary (bootstrap circularity, below), but it lives
   only in the gate's behavior — undocumented law.
2. An agent (`agent-worker-story-0008`) authored a story revision under **no
   mandate check**. ONT-013 keeps it honest (author ≠ authority), but the corpus
   does not distinguish mandated agent authorship from free agent authorship.

Both should be governed, not left as behavior a reviewer rediscovers.

---

<!-- proposed-atom POST-0001 — quoted as delivered, not admitted as written.
     Admitted as SPEC-0122; see the admission record at the foot of this file. -->
```yaml
id: POST-0001
type: posture
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-13T21:30:00Z"
author: consul-architect
authorized_by: null
title: "Spawn requires a resolvable story reference, not a ratified one"
tags: [spawn, bootstrap, declared-posture, reviewer-seam]
source_refs: [SPEC-0081, DOC-0005]
```
The spawn gate (SPEC-0081) admits a spawn whose story reference **resolves to a
real story atom**; it does not require that story to be in state `active` or
`ratified`. This is a declared posture, not an oversight, and its rationale is
bootstrap circularity: a story is necessarily `proposed` while the work that
produces its acceptance evidence is in flight, and ratification *follows* green
acceptance (it cannot precede it). Requiring `active` or `ratified` law to spawn
the work that earns activation would be a circular gate under which nothing could
ever be built. Therefore: **resolvability is the spawn precondition; lifecycle
state is not.** The paper's invariant reads "no *resolvable* story, no spawn."

Self-failing condition: if a future policy ever requires ratified-story spawns for
a defined class of work (e.g. production spawns outside bootstrap), this posture is
superseded for that class by the decision that establishes the requirement, and a
check asserts the gate enforces the stricter precondition for that class. Until
such a decision exists, resolvable-not-ratified is the governed rule.
<!-- end proposed-atom POST-0001 -->

<!-- proposed-atom OPEN-0001 — quoted as delivered, not admitted as written.
     Admitted as SPEC-0123; see the admission record at the foot of this file. -->
```yaml
id: OPEN-0001
type: open-item
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-13T21:30:00Z"
author: consul-architect
authorized_by: null
title: "Agent authorship is currently mandate-unbounded (de facto Magistracy-D1)"
tags: [authorship, magistracy, d1, reviewer-seam, emergence]
source_refs: [DOC-0005]
relations:
  - { rel: depends-on, target: "magistracy-d1-lane" }
```
An agent identity (e.g. `agent-worker-story-0008`) has authored story-atom content
revisions. ONT-013 keeps this honest: `author` records who wrote the atom;
`authorized_by` records who gave it force; an agent authoring content does not
grant force, and the human floor still ratifies. **But** the corpus does not
currently distinguish *mandated* agent authorship (an agent permitted, under a
scoped rubric, to author atoms of a given type) from *free* agent authorship —
there is no `authored_by`-attenuation check binding an agent's authorship to a
granted scope.

This is a de facto Magistracy-D1 act (bounded authorship within a ratified rubric)
with no D1 mechanism enforcing the bound yet — the emergence-before-naming pattern
the Magistracy emergence analysis documented: the agent is *already* acting as a
magistrate-of-authorship. Recorded here as a declared open item, not a silent gap,
so a reviewer finds a governed acknowledgment rather than an undeclared practice.

Disposition: resolves when the Magistracy D1 lane ratifies a mandate mechanism —
at which point agent authorship of governed atom types requires a scoped authorship
mandate, and this open item closes by reference to that decision. Until then, agent
authorship remains permitted-but-unbounded, and that state is *declared*, not
assumed.
<!-- end proposed-atom OPEN-0001 -->

---

## Notes for admission

- If `posture` and `open-item` are not yet atom types in the schema, the cleaner
  path is to fold POST-0001 into the existing posture mechanism (the same one
  SPEC-0120 uses) and OPEN-0001 into whatever open-item/tracker convention the
  corpus already carries — do not mint new types casually; reuse the D42
  self-failing-posture machinery for POST-0001 since it already exists.
- Both are `proposed` and `authorized_by: null` — they ratify on the next
  reconcile/decision like any other governed content. POST-0001 is a declared
  operating posture (low band); OPEN-0001 is a record of a known gap (informational
  until the D1 lane exists). Neither is D3.
- The paper cites POST-0001 by ID for the "no resolvable story, no spawn" claim, so
  the paper's honest description points at governed law, closing the two-sources
  seam.

---

## Admission record — 2026-08-14, STORY-0013

Admitted with both proposed atom blocks **demoted to quotations**. Neither was
admissible as written: `posture` and `open-item` are not among the seventeen types
in `schemas/atoms-1.0.0.json`, the `POST-`/`OPEN-` prefixes are not in the id
pattern, and `depends-on` is not in the relation vocabulary. Left as atoms they took
the corpus red on four findings, which in turn blocked `enact.py --reconcile` — the
floor's own queue step 1 — because the ceremony tool refuses to run over a corpus
that does not parse.

Delivered instead through the machinery the note itself pointed at, per its
instruction *"do not mint new types casually; reuse the D42 self-failing-posture
machinery for POST-0001 since it already exists"*:

| proposed | admitted as | mechanism |
|---|---|---|
| POST-0001 | **SPEC-0122** | declared posture, `binding: checked`, checked by CTRL-0005 |
| OPEN-0001 | **SPEC-0123** | declared posture, `binding: checked`, checked by CTRL-0002 |

Both live in `REVIEWER_SEAM_POSTURES.md`. A posture in this corpus *is* a
specification with a checked binding — that is what D42 and PRIN-0005 established,
and SPEC-0120 is the worked example. Minting a `posture` type would have created a
second way to say the thing the specification type already says, which is the
two-sources shape this note exists to close.

**The IDs are the ones the paper should cite.** POST-0001 and OPEN-0001 resolve to
nothing in this corpus and will keep resolving to nothing; rc9 §7 should cite
SPEC-0122 and SPEC-0123.

**One correction to the note's premise.** POST-0001 described the spawn gate as
admitting "a spawn whose story reference resolves to a real story atom". It did not.
`check()` required only that `story_ref` be a non-empty string — it never resolved
it, so *any* plausible string passed and "no story, no spawn" was enforced against
the empty string alone. Declaring the posture as drafted would have recorded
behaviour the gate did not have, opening a fresh two-sources seam rather than
closing one. The gate was made resolvable-checking first (`resolve_story()` in
`harness/spawn.py`, asserted by CTRL-0005); SPEC-0122 then describes what is there.
