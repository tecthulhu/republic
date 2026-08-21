# The self-dilution composition — charter for the integrity fix

**Source:** `FLOOR_RESPONSE_whitepaper_currency_and_dilution.md`, Block 2. The floor
ruled the mitigation and ruled it **ahead of STORY-0010**: an agent grading its own
work against criteria it weakened is an integrity gap, and an integrity gap outranks
a capability gap.

## The attack

SPEC-0122 (spawn admits a pre-ratified story) and SPEC-0123 (agent authorship is
mandate-unbounded) are each correct alone and compose into a hole. An agent authors a
weakening of its own in-flight acceptance specs; the gate grades the work against the
current specs; green passes against criteria no human ever touched. Every individual
signal stays green — the authorship is valid, the story resolves, the gate graded the
specs it found, the merge passed — which is the same shape as the buffering adapter
and the unenforced egress pin, one layer up. The absent property is *a human
authorized what "passing" means*, and nothing was checking for it because nothing
names it.

The fix reverses neither posture. The bootstrap spawn rule stands; authorship stays
open pending the Magistracy D1 lane. What changes is that the grading baseline stops
moving on agent authority alone.

**Provenance worth keeping.** This was findable only because both postures were
declared honestly — the disclosure recruited the reviewer into the security analysis.
The postures were written in STORY-0013 to close a documentation seam; the composition
fell out of having them side by side, where neither was visible alone.

## Two readings this charter makes explicit

Both are the builder's reading, recorded so STORY-0014 does not re-derive them
silently, and flagged so the floor can correct them cheaply.

**"Floor-touched instance."** In this corpus the floor's signature is the owner's
merge (PA-002, ENT-079) and its durable trace is `authorized_by` naming a decision.
So the reading is: an acceptance-spec instance is floor-touched when it carries a
non-null `authorized_by`, or when it is the instance the story's spawn act pinned.
This is deliberately *not* unified with STORY-0010's human-evidence primitive — both
mean "a human deliberately touched this", but a floor touch is a ratification act and
human evidence is an evidence record. Two accidental mechanisms for one idea is the
anti-pattern; STORY-0010 may unify them later if they turn out to be one thing.

**There was nothing to pin to.** SPEC-0081–0086 — the whole of STORY-0002's
acceptance set — were `proposed` with `authorized_by: null`; no acceptance spec in
this corpus had ever been floor-touched, and the spawn gate persisted no act record
naming the acceptance set it spawned against. A pin implemented against an empty
baseline would have reported green while pinning nothing.

Both halves are now answered, and the floor accepted the finding on each:

- **DEC-0005** ratifies STORY-0002 and its six criteria — the first floor touch of
  acceptance criteria in the corpus's history, and the event the pin anchors to for
  initial criteria.
- **SPEC-0129** makes the spawn act durable, and the floor ordered it *first* in
  STORY-0014 rather than folded into the pin as this charter originally had it.

What remains unanswered is narrower and worth keeping visible: STORY-0013's own
acceptance set (SPEC-0122–0125) is equally green and equally untouched, and
DEC-0005 deliberately does not reach it.

---

<!-- atom:begin id=SPEC-0126 -->
```yaml
id: SPEC-0126
type: specification
scope: story:story-0014
state: active
version: 1.3.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Acceptance grading resolves to the last floor-touched instance, not the current one"
tags: [acceptance-criterion, integrity, self-dilution, class-iii]
binding: checked
check: machine
story_ref: STORY-0014
relations:
  - { rel: derives, target: SPEC-0129 }
```
The evidence-grading query resolves a story's acceptance set to the acceptance-spec
instances **as of the last floor touch**: the instance named by the story's durable
spawn-act record (SPEC-0129) for initial criteria, or the most recent instance
carrying a floor ratification for revisions. Agent-authored revisions after spawn
remain recordable and remain in the corpus — they are not refused — but they do not
move the graded baseline until a floor touch moves it.

Fixtures demonstrate, on an in-flight story: an agent-authored weakening graded
against the pinned set rather than the weakened one; a merge that would pass against
the weakened set failing against the pin; a floor-touched revision moving the
baseline; and a story whose spawn-act record is missing **refused rather than graded
against whatever is current** — a pin with no anchor must fail closed, because the
alternative is a pin that silently degrades into grading the present.

*v1.1.0 — the durable spawn-act record moved out of this criterion and into
SPEC-0129, per floor Direction 2. It was folded in here as a clause, which read as a
detail of the pin rather than as its prerequisite; the floor ruled it a criterion in
its own right and ordered it first. The amendment is floor-directed and floor-touched
by the same merge that signs DEC-0005 — a widening of the criteria, not a narrowing,
and not one an agent made on its own authority.*
<!-- atom:end id=SPEC-0126 -->

<!-- atom:begin id=SPEC-0129 -->
```yaml
id: SPEC-0129
type: specification
scope: story:story-0014
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Every spawn persists a durable record of what it was authorized against"
tags: [acceptance-criterion, integrity, self-dilution, class-iii, spawn]
binding: checked
check: machine
story_ref: STORY-0014
relations:
  - { rel: derives, target: SPEC-0122 }
```
A spawn writes an immutable record naming the story instance it resolved to — id,
version, `instantiated_at` — and a digest over the acceptance-set instances in force
at that moment. The record is the spawn act, and it is what the baseline pin anchors
to.

**This is first because without it the pin has nothing to hold.** The gate resolves a
story (SPEC-0122) and then forgets: it mints, injects and starts a container, and
persists nothing about the criteria the work was authorized against. A pin built on
top of that would compute a baseline from an empty set and grade against it, which is
a green check standing in for a property that is not there — the buffering-proxy
defect class, one layer up in the governance plane.

The record is a record, not derived data: it is committed under `acta/` (D17) and
addressable like any other, because a baseline recomputed at grading time from
whatever the corpus currently says is not a baseline.

Fixtures demonstrate: a spawn producing a record whose story instance and
acceptance digest match the corpus at spawn time; the record surviving the container
it describes; a corpus edit after spawn leaving the record unchanged; and the record
being refused rather than written when the story resolves to nothing.
<!-- atom:end id=SPEC-0129 -->

<!-- atom:begin id=RULE-0094 -->
```yaml
id: RULE-0094
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Bind SPEC-0129 via CTRL-0005"
tags: [binding, integrity]
claim: SPEC-0129
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0129 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0094 -->

<!-- atom:begin id=RULE-0086 -->
```yaml
id: RULE-0086
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Bind SPEC-0126 via CTRL-0005"
tags: [binding, integrity]
claim: SPEC-0126
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0126 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0086 -->

<!-- atom:begin id=STORY-0014 -->
```yaml
id: STORY-0014
type: story
scope: platform
state: proposed
version: 1.1.0
instantiated_at: "2026-08-14T05:10:00Z"
author: agent-worker-dec-0005
authorized_by: null
title: "Acceptance-baseline pinning: grade against what the floor touched"
tags: [integrity, self-dilution, class-iii, floor-ruled]
tracker_ref: "gh:tecthulhu/republic#26"
acceptance: [SPEC-0129, SPEC-0126]
relations:
  - { rel: advances, target: SPRINT-0001 }
```
The load-bearing half of the mitigation. The lint (STORY-0015) makes the pending
state visible; the pin is what actually stops the weakened set from being graded
against.

**Build order is part of the charter, not an implementation detail.** SPEC-0129
first: the durable spawn-act record, because a pin with no anchor computes a baseline
from an empty set and grades against it. SPEC-0126 second: the pin itself. The
acceptance list is written in that order for the same reason.

Build floor-touch **minimally** here, per the floor's cousin-primitive note: the
spawn-act record pins initial criteria, an explicit floor ratification moves the
baseline for revisions, and nothing is pre-unified with STORY-0010's human-evidence
record.

*v1.1.0 — acceptance widened from one criterion to two on floor Direction 2, which
accepted the finding that Hardening 2 had an unbuilt prerequisite. Floor-directed and
floor-touched by the same merge that signs DEC-0005, which matters here more than
usual: this is an amendment to the acceptance set of the very story that exists to
stop acceptance sets moving on agent authority. It widens rather than narrows, and it
is not an agent's own call.*
<!-- atom:end id=STORY-0014 -->

---

<!-- atom:begin id=SPEC-0127 -->
```yaml
id: SPEC-0127
type: specification
scope: story:story-0015
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "The build gate flags every non-floor edit to an in-flight acceptance spec"
tags: [acceptance-criterion, integrity, self-dilution, atom-lint]
binding: checked
check: machine
story_ref: STORY-0015
```
CTRL-0001 flags **any** non-floor-authored diff to an acceptance-spec atom belonging
to an in-flight story — removal, threshold change, or pure rewrite alike — and names
the pending-floor-touch state. It does not classify whether the edit weakens.

That refusal to classify is the specification, not a shortcut. A "loosens" predicate
needs a mechanically decidable definition of looser, and without one the lint either
over-fires on every edit or is walked past by a semantic weakening dressed as a
rewrite. The pin (SPEC-0126) does the load-bearing work; this makes the pending state
visible, and an oracle nobody has to write is an oracle nobody can attack.

Fixtures demonstrate a non-floor acceptance edit flagged, a floor-touched edit clean,
a pure rewrite with no criterion change flagged all the same, and an edit to a spec
on a story that is not in flight left alone.
<!-- atom:end id=SPEC-0127 -->

<!-- atom:begin id=RULE-0087 -->
```yaml
id: RULE-0087
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Bind SPEC-0127 via CTRL-0001"
tags: [binding, integrity]
claim: SPEC-0127
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0127 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0087 -->

<!-- atom:begin id=STORY-0015 -->
```yaml
id: STORY-0015
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Weakening-diff lint: make the pending-floor-touch state visible at the build gate"
tags: [integrity, self-dilution, class-iii, floor-ruled]
tracker_ref: "gh:tecthulhu/republic#27"
acceptance: [SPEC-0127]
relations:
  - { rel: advances, target: SPRINT-0001 }
```
Rides STORY-0014's window or its own; the two are separable and the pin is the one
that must land.
<!-- atom:end id=STORY-0015 -->

---

<!-- atom:begin id=SPEC-0128 -->
```yaml
id: SPEC-0128
type: specification
scope: story:story-0016
state: active
version: 1.3.0
instantiated_at: "2026-08-21T03:00:00Z"
author: agent-worker-dec-0010
authorized_by: DEC-0010
title: "Declared posture: the SPEC-0122/SPEC-0123 composition and its time-boxed mitigation"
tags: [acceptance-criterion, declared-posture, interim-posture, integrity, class-iii, d42]
binding: checked
check: machine
story_ref: STORY-0016
retirement_date: "2026-10-20"
relations:
  - { rel: derives, target: SPEC-0122 }
  - { rel: derives, target: SPEC-0123 }
```
A declared posture in the D42 family, sibling to SPEC-0122, naming three things: the
composition attack, the SPEC-0126 + SPEC-0127 mitigation standing in for a mandate
mechanism, and the retirement condition — the Magistracy D1 authorship-mandate lane
going live, at which point mandate-bounded authorship supersedes floor-touch pinning
for mandated scopes.

Self-failing condition: a check asserts the pin and the lint are both **active** for
as long as this posture stands. A posture that hedges on a mitigation being in place
must fail the moment the mitigation is removed or demoted; otherwise the hedge
outlives the thing it was hedging about, which is the failure mode PRIN-0005 exists
to prevent.

Time-boxed: **`retirement_date: 2026-10-20`**, ruled by the floor on 2026-08-21, sixty
days out. On that date the posture must be re-ratified, superseded, or retired by an
explicit floor act; it does not silently persist past it. CTRL-0005 asserts the date is
present and fails the tree once it passes without such an act — the time-box enforced
rather than decorative, which is the difference between a deadline and a wish.

v1.3.0 carries the date. v1.2.0 did not, and STORY-0016 proved by blocked attempt that
no agent could add it: SPEC-0113 refused the in-place edit, and SPEC-0127 flagged the
lawful new instance as an untouched change to an in-flight story's criteria. The doors
that refused the agent open to the floor's signed act, and that asymmetry is the whole
of what the mitigation is for.

Passing the date without either superseding it or restating it is itself a
failure. Silence is not renewal.

**This is the atom the whitepaper cites.** rc9 §7's account of the composition should
name SPEC-0128 by id once STORY-0016 lands; until then "posture atom pending
(SPEC-0128 reserved)" is the honest form.
<!-- atom:end id=SPEC-0128 -->

<!-- atom:begin id=RULE-0088 -->
```yaml
id: RULE-0088
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Bind SPEC-0128 via CTRL-0005"
tags: [binding, declared-posture, integrity]
claim: SPEC-0128
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0128 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0088 -->

<!-- atom:begin id=STORY-0016 -->
```yaml
id: STORY-0016
type: story
scope: platform
state: proposed
version: 1.1.0
instantiated_at: "2026-08-14T05:10:00Z"
author: agent-worker-dec-0005
authorized_by: null
title: "The composition posture: declare the Class III gap and its time-boxed mitigation"
tags: [integrity, self-dilution, class-iii, declared-posture, floor-ruled]
tracker_ref: "gh:tecthulhu/republic#28"
acceptance: [SPEC-0128]
relations:
  - { rel: advances, target: SPRINT-0001 }
```
Sequenced last of the three: the posture asserts the pin and the lint are active, so
it cannot be declared truthfully before they exist. Declaring it first would be the
same error STORY-0013 caught in POST-0001 — an atom describing machinery that is not
there.

*v1.1.0 — the R6 citation is dropped, per floor Direction 3. DEC-0001's R6 ratifies
the limiter grammar sections and says nothing about interim postures, so the
time-boxing had been written from the ruling's words against a rule that does not
support them. The floor accepted the finding and ruled that the retirement condition —
mandate-bounded authorship going live — stands on its own as a declared self-failing
posture and needs no citation. A borrowed citation that does not resolve is weaker
than no citation, because it invites the reader to stop checking.*
<!-- atom:end id=STORY-0016 -->
