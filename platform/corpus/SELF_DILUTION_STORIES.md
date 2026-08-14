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

**There is nothing to pin to yet.** SPEC-0081–0086 — the whole of STORY-0002's
acceptance set — are `proposed` with `authorized_by: null`. No acceptance spec in this
corpus has ever been floor-touched, and the spawn gate persists no act record naming
the acceptance set it spawned against. Hardening 2 therefore has a prerequisite:
STORY-0014 must make the spawn act durable before it can pin anything to it, and a
ratifying decision must exist before any revision can be measured against a touch.
This is a finding, not an objection — but a pin implemented against an empty baseline
would report green while pinning nothing.

---

<!-- atom:begin id=SPEC-0126 -->
```yaml
id: SPEC-0126
type: specification
scope: story:story-0014
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Acceptance grading resolves to the last floor-touched instance, not the current one"
tags: [acceptance-criterion, integrity, self-dilution, class-iii]
binding: checked
check: machine
story_ref: STORY-0014
```
The evidence-grading query resolves a story's acceptance set to the acceptance-spec
instances **as of the last floor touch**: the instance pinned by the story's
spawn-authorizing act for initial criteria, or the most recent instance carrying a
floor ratification for revisions. Agent-authored revisions after spawn remain
recordable and remain in the corpus — they are not refused — but they do not move the
graded baseline until a floor touch moves it.

The spawn act becomes durable as part of this: spawning a story is a floor or
floor-delegated touch of its initial criteria, so the act record must name the
acceptance-spec instances it spawned against. Without that record the initial
baseline has no anchor and the "author the initial specs weak" variant stays open.

Fixtures demonstrate, on an in-flight story: an agent-authored weakening graded
against the pinned set rather than the weakened one; a merge that would pass against
the weakened set failing against the pin; a floor-touched revision moving the
baseline; and a story whose spawn act is missing refused rather than graded against
whatever is current.
<!-- atom:end id=SPEC-0126 -->

<!-- atom:begin id=RULE-0086 -->
```yaml
id: RULE-0086
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
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
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Acceptance-baseline pinning: grade against what the floor touched"
tags: [integrity, self-dilution, class-iii, floor-ruled]
acceptance: [SPEC-0126]
relations:
  - { rel: advances, target: SPRINT-0001 }
```
The load-bearing half of the mitigation. The lint (STORY-0015) makes the pending
state visible; the pin is what actually stops the weakened set from being graded
against.

Build floor-touch **minimally** here, per the floor's cousin-primitive note: the
spawn act pins initial criteria, an explicit floor ratification moves the baseline
for revisions, and nothing is pre-unified with STORY-0010's human-evidence record.
<!-- atom:end id=STORY-0014 -->

---

<!-- atom:begin id=SPEC-0127 -->
```yaml
id: SPEC-0127
type: specification
scope: story:story-0015
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
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
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
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
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Declared posture: the SPEC-0122/SPEC-0123 composition and its time-boxed mitigation"
tags: [acceptance-criterion, declared-posture, interim-posture, integrity, class-iii, d42]
binding: checked
check: machine
story_ref: STORY-0016
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

Time-boxed: the posture carries a retirement date as well as a retirement condition,
and passing the date without either superseding it or restating it is itself a
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
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
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
version: 1.0.0
instantiated_at: "2026-08-14T04:40:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "The composition posture: declare the Class III gap and its time-boxed mitigation"
tags: [integrity, self-dilution, class-iii, declared-posture, floor-ruled]
acceptance: [SPEC-0128]
relations:
  - { rel: advances, target: SPRINT-0001 }
```
Sequenced last of the three: the posture asserts the pin and the lint are active, so
it cannot be declared truthfully before they exist. Declaring it first would be the
same error STORY-0013 caught in POST-0001 — an atom describing machinery that is not
there.

One reference in the floor ruling does not resolve here: "R6's interim-posture rule".
DEC-0001's R6 ratifies the limiter grammar sections and says nothing about postures,
so the time-boxing above is written from the ruling's own words rather than from a
cited rule. If R6 belongs to the spine's numbering rather than this corpus, the
citation needs redirecting before STORY-0016 builds against it.
<!-- atom:end id=STORY-0016 -->
