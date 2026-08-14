# Reviewer-seam postures — declaring what the machinery already does

**STORY-0013.** Source: `ARCHITECT_NOTE_reviewer_seam_corpus_fix.md` (items 1 and 2)
and `FLOOR_RESPONSE_whitepaper_currency_and_dilution.md` (queue steps 2 and 3).

Four things were true of the running platform and absent from the corpus. Each was
findable by reading the code and none was findable by reading the law, which is the
two-sources-of-truth shape the program rules against — with the aggravating detail
that the *paper* described three of them, so the honest external description was
carrying governance the corpus did not hold.

All four are declared here as specifications with `binding: checked`. A posture in
this corpus is not a separate kind of thing: D42 and PRIN-0005 established that a
posture is a claim whose *enabling condition is itself checked*, so that the
condition becoming false fails a control and forces supersession. SPEC-0120 is the
worked example. Minting a `posture` type would have been a second way to say what
`specification` already says — a two-sources seam introduced by the atoms written to
close one.

Three of the four assert an **absence**. That is deliberate and it is the whole
mechanism: an absence nobody checks is how a hedge outlives its reason.

---

## The spawn precondition

<!-- atom:begin id=SPEC-0122 -->
```yaml
id: SPEC-0122
type: specification
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Spawn requires a resolvable story reference, not a ratified one"
tags: [declared-posture, interim-posture, spawn, bootstrap, reviewer-seam, d42]
binding: checked
check: machine
story_ref: STORY-0013
relations:
  - { rel: derives, target: SPEC-0081 }
```
The spawn gate admits a request whose story reference **resolves to a story atom**.
It does not require that story to be `ratified` or `active`, and it refuses a
reference that resolves to nothing, to a non-story atom, or to nothing readable
because the corpus does not parse.

The leniency is load-bearing rather than lax. A story is necessarily pre-ratified
while the work producing its acceptance evidence is in flight, and ratification
follows green acceptance — it cannot precede it. A gate demanding ratified law
before spawning the work that earns ratification is circular, and nothing would ever
be built through it. So: **resolvability is the spawn precondition; lifecycle state
is not.** The paper's invariant reads "no *resolvable* story, no spawn."

What was *not* true when this posture was proposed: the gate did not resolve
anything. `check()` required only that `story_ref` be a non-empty string, so "no
story, no spawn" was enforced against the empty string and a typo spawned happily.
The gate was made to resolve first (`resolve_story()` in `harness/spawn.py`) and this
atom then describes it — declaring the posture against the old gate would have
recorded behaviour that did not exist, opening a seam rather than closing one.

Self-failing condition (PRIN-0005): CTRL-0005 asserts that a **pre-ratified** story
in the corpus is admitted. If a future decision requires ratified-story spawns for
some class of work, that assertion goes red and the only way back to green is to
supersede this posture with the decision that established the requirement. The
subject is selected from the corpus at check time rather than pinned to one story,
so the check does not go red on the day a particular story is legitimately ratified —
a fixture failing for the one reason that is not the retirement condition teaches the
next reader to ignore it.
<!-- atom:end id=SPEC-0122 -->

<!-- atom:begin id=RULE-0082 -->
```yaml
id: RULE-0082
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Bind SPEC-0122 via CTRL-0005"
tags: [binding, declared-posture]
claim: SPEC-0122
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0122 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0082 -->

---

## The authorship gap

<!-- atom:begin id=SPEC-0123 -->
```yaml
id: SPEC-0123
type: specification
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Interim posture: agent authorship of governed atoms is mandate-unbounded"
tags: [declared-posture, interim-posture, authorship, magistracy-d1, reviewer-seam, d42]
binding: checked
check: machine
story_ref: STORY-0013
```
Agent identities author governed atoms — this atom among them — and nothing binds
that authorship to a granted scope. ONT-013 keeps it honest as far as it goes:
`author` records who wrote an atom, `authorized_by` records who gave it force, and
writing does not confer force. But the corpus does not distinguish *mandated* agent
authorship (an agent permitted, under a ratified rubric, to author atoms of a given
type) from *free* agent authorship. There is no attenuation check between an
authoring identity and a granted scope, and the human floor's ratification is the
only thing standing between agent-authored text and governed law.

This is a de facto Magistracy-D1 act — bounded authorship within a ratified rubric —
with no D1 mechanism enforcing the bound: emergence before naming, the agent already
acting as a magistrate-of-authorship. It is recorded here as a declared state rather
than a silent practice, so a reviewer finds an acknowledgment instead of a discovery.
Its composition with SPEC-0122 is a live integrity gap and is addressed separately
(STORY-0014/0015/0016).

Self-failing condition (PRIN-0005): CTRL-0001 asserts that no `MAND-` atom carries an
authorship imperium. The first one turns the corpus red, and the only way back to
green is to supersede this posture and bind authorship to the granted scope. The
check is guarded on this atom's own presence and state — supersede it and the guard
goes with it, because a corpus that no longer makes the claim has nothing here to
keep honest.

Retirement condition: the Magistracy D1 lane ratifying an authorship-mandate
mechanism. Until then, agent authorship is permitted-but-unbounded, and that is
*declared*, not assumed.
<!-- atom:end id=SPEC-0123 -->

<!-- atom:begin id=RULE-0083 -->
```yaml
id: RULE-0083
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Bind SPEC-0123 via CTRL-0001"
tags: [binding, declared-posture]
claim: SPEC-0123
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0123 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
CTRL-0001 rather than CTRL-0002. The claim is a property of the corpus's authorship,
not of the caveat algebra, and atom-lint is the corpus control — the same control the
floor's weakening-diff lint (STORY-0015) will extend. SPEC-0120's absence-assertion
lives in CTRL-0002 because *its* subject is the chain verifier's surface; putting a
corpus claim there because that is where the last posture went would widen a
control's remit by habit.
<!-- atom:end id=RULE-0083 -->

---

## Where SPEC-0085's acceptance evidence comes from

<!-- atom:begin id=SPEC-0124 -->
```yaml
id: SPEC-0124
type: specification
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Interim posture: SPEC-0085's acceptance evidence is locally produced, not CI-produced"
tags: [declared-posture, interim-posture, spec-0085, ci, d42]
binding: checked
check: machine
story_ref: STORY-0013
relations:
  - { rel: derives, target: SPEC-0085 }
```
SPEC-0085 is the only acceptance criterion that spends a model credential, and the
conformance workflow holds none. Its rows were produced on an operator workstation
and its CI step records `skip`. Every other criterion in CTRL-0005 is green in CI on
every change; this one is green somewhere a reader cannot see, and "CTRL-0005 green"
does not distinguish the two without this atom.

The qualification is narrow and worth stating precisely: the *code path* is the one
CI runs — supervision is exercised through `suite/gates/run.py` like everything else,
not through a bespoke local script. What CI cannot supply is the credential at the
far end of the adapter, so the criterion does not execute there.

Self-failing condition (PRIN-0005): CTRL-0005 asserts that no workflow file under
`.github/workflows/` supplies a provider credential. The day a scoped key is added
this turns red, and the correct response is to supersede this posture — at that point
the evidence *is* CI-produced and the hedge has become a false statement rather than
a true one.

Open to the floor: whether SPEC-0085 should stay locally-evidenced under this
declared posture, or whether CI should get a scoped, spend-capped key. This atom
takes no position on which; it makes the current answer visible so the choice is one
someone makes rather than one that persists by default.
<!-- atom:end id=SPEC-0124 -->

<!-- atom:begin id=RULE-0084 -->
```yaml
id: RULE-0084
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Bind SPEC-0124 via CTRL-0005"
tags: [binding, declared-posture]
claim: SPEC-0124
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0124 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0084 -->

---

## Provider portability

<!-- atom:begin id=SPEC-0125 -->
```yaml
id: SPEC-0125
type: specification
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Supervision is provider-agnostic, and every evidence row names its provider"
tags: [portability, spec-0085, ont-039, adapter-boundary]
binding: checked
check: machine
story_ref: STORY-0013
relations:
  - { rel: derives, target: SPEC-0085 }
```
Unlike the three above, this is a standing claim rather than an interim posture: it
names a property the platform should keep, not a gap it should close.

The supervisor speaks to the CLI and the CLI speaks to whatever the adapter points
at, so no provider endpoint appears anywhere on the session path — the credential and
the upstream both live behind the D47 adapter boundary. Acceptance evidence is
produced against the pinned configuration; the *identical* code path is re-run
against a second provider as a portability check.

Both halves are checked, and the second is what keeps the first honest. "Supervision
works" and "supervision works against the provider this platform pins" are different
sentences, and a row that does not name its provider silently asserts the stronger
one. So CTRL-0005 asserts that `harness/supervise.py` carries no endpoint literal on
an executable line, that an acceptance provider and a portability provider are
configured against distinct upstreams, and that the model measurement on every row is
a band and a digest — never the identifier (ONT-039). The literal-leak assertion runs
over *every* configured provider: the previous version of this check scanned with a
pattern that matched one vendor's identifiers and passed the other's through.
<!-- atom:end id=SPEC-0125 -->

<!-- atom:begin id=RULE-0085 -->
```yaml
id: RULE-0085
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Bind SPEC-0125 via CTRL-0005"
tags: [binding, portability]
claim: SPEC-0125
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0125 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0085 -->

---

## The story

<!-- atom:begin id=STORY-0013 -->
```yaml
id: STORY-0013
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T04:30:00Z"
author: agent-worker-story-0013
authorized_by: null
title: "Reviewer seam: declare the postures the machinery already runs on"
tags: [reviewer-seam, declared-posture, corpus]
tracker_ref: "gh:tecthulhu/republic#25"
acceptance: [SPEC-0122, SPEC-0123, SPEC-0124, SPEC-0125]
relations:
  - { rel: advances, target: SPRINT-0001 }
```
Chartered from the reviewer-seam note (items 1–2) and widened by the floor response,
which routes its queue step 2 — the SPEC-0085 locality posture and the
provider-portability atom — immediately alongside step 3. Same class of work: four
properties true of the running platform and absent from the law.

Not in scope, and deliberately: the composition of SPEC-0122 and SPEC-0123 is an
integrity gap the floor has ruled on separately, and it is chartered as
STORY-0014/0015/0016 rather than folded in here. Declaring a gap and closing it are
different acts and should be separately reviewable — particularly this gap, where the
declaration is what made the attack findable.
<!-- atom:end id=STORY-0013 -->
