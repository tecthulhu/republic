# Spawn Contract Stories — the risky hop, papered

Work orders for build-order steps 4–5 (PA-030): the containerized,
supervised CLI-session agent. These stories transcribe the spawn-contract
acceptance criteria as story atoms with story-scoped acceptance
specifications (DEC-0001 R3: acceptance criteria are SPEC- atoms at story
scope, tagged). STORY-0001 is the gold base (Document 3's deliverable);
STORY-0002 is the spawn contract proper — the hop no adjacent capability
substitutes for. Tracker refs are placeholders until reflected to GitHub
Issues by the Quaestor path.

The CLI version pin is recorded as a versioned measurement in SPEC-0086
and applies to every acceptance run in STORY-0002: results are valid
against the pinned version only, and any version bump re-runs the full set.

---

<!-- atom:begin id=STORY-0001 -->
```yaml
id: STORY-0001
type: story
scope: platform
state: proposed
version: 1.2.0
instantiated_at: "2026-08-11T14:50:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Gold base image with citizenship conformance green"
tags: [step-4, l0]
tracker_ref: "gh:tecthulhu/republic#1"
acceptance: [SPEC-0071, SPEC-0072, SPEC-0073]
relations:
  - { rel: derives, target: DOC-0003 }
```
Build the L0 gold base per Document 3: pinned upstream, hardening pins,
`/l0/init` + `/l0/agentd`, conformance suite runnable, hello-citizen and
violating fixtures.
<!-- atom:end id=STORY-0001 -->

<!-- atom:begin id=SPEC-0071 -->
```yaml
id: SPEC-0071
type: specification
scope: story:story-0001
state: proposed
version: 1.0.0
instantiated_at: "2026-08-10T14:00:00Z"
author: consul-draft
authorized_by: null
title: "hello-citizen fixture passes BASE-AC-1 through BASE-AC-13"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0001
```
BASE-AC-14 (resolve/recall) enters per L0 open item (c) as a declared
interim posture if stubbed; all other identity, hardening, and citizenship
ACs green with evidence rows against the fixture image digest.
<!-- atom:end id=SPEC-0071 -->

<!-- atom:begin id=SPEC-0072 -->
```yaml
id: SPEC-0072
type: specification
scope: story:story-0001
state: proposed
version: 1.1.0
instantiated_at: "2026-08-11T01:20:00Z"
author: agent-worker-story-0004
authorized_by: null
title: "Violating fixture fails BASE-AC-15 and BASE-AC-16"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0001
```
The deliberately non-conformant image (shell restored, capability
re-added, root regained, missing or mismatched base label) fails the
suite on every count — the sealing claims proven falsifiable.

v1.1.0 (D5): narrowed to the image-level negatives, which are runnable
inside STORY-0001. BASE-AC-9 (host bind/volume refused) and BASE-AC-17
(over-ceiling caveat request refused) are harness-tested, and the harness
is STORY-0002's deliverable; they move to SPEC-0081 v1.1.0, where they
always belonged, and SPRINT-0001's gate still runs all seventeen.
<!-- atom:end id=SPEC-0072 -->

<!-- atom:begin id=SPEC-0073 -->
```yaml
id: SPEC-0073
type: specification
scope: story:story-0001
state: proposed
version: 1.0.0
instantiated_at: "2026-08-10T14:00:00Z"
author: consul-draft
authorized_by: null
title: "Conformance runs in CI gated on merge with evidence emitted per AC"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0001
```
The build gate mounts CTRL-0004; a red suite blocks merge (ENF-0001); each
AC emits an EVID- row on acta.evidence.ctrl-0004 against the image digest.
<!-- atom:end id=SPEC-0073 -->

---

<!-- atom:begin id=STORY-0002 -->
```yaml
id: STORY-0002
type: story
scope: platform
state: proposed
version: 1.2.0
instantiated_at: "2026-08-11T14:50:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Spawn contract: supervised CLI-session agent in a citizen container"
tags: [step-5, risky-hop, spawn-contract]
tracker_ref: "gh:tecthulhu/republic#2"
acceptance: [SPEC-0081, SPEC-0082, SPEC-0083, SPEC-0084, SPEC-0085, SPEC-0086]
sprint_ref: SPRINT-0001
relations:
  - { rel: derives, target: DOC-0003 }
  - { rel: derives, target: DOC-0004 }
```
Prove the capability no adjacent capability substitutes for: a CLI agent
in session mode, containerized on the gold base, story-scoped, supervised,
streaming. API-mode fleet evidence does not satisfy any criterion below.
<!-- atom:end id=STORY-0002 -->

<!-- atom:begin id=SPEC-0081 -->
```yaml
id: SPEC-0081
type: specification
scope: story:story-0002
state: proposed
version: 1.1.0
instantiated_at: "2026-08-11T01:20:00Z"
author: agent-worker-story-0004
authorized_by: null
title: "Spawn gate: refusal without story, mint and inject with one, ceiling and mount refusals"
tags: [acceptance-criterion, spawn-ac-1]
binding: checked
check: machine
story_ref: STORY-0002
```
A spawn request lacking a story reference is refused before container
creation (ENF-0002). With one: a leaf is minted whose act token carries
audience = the story id (ES-020) and whose transport grant is the ES-003
projection; the container starts on the gold base with zero host mounts;
core-class context (laws, strategy hash-verified, mandate) is injected
per L0-051 with restrictions armed pre/post, never in-prompt.

v1.1.0 (D5) absorbs the two harness-tested conformance criteria that
STORY-0001 cannot run because the harness is this story's deliverable:
BASE-AC-9 — a spawn spec containing any host bind or volume is refused
by the harness, recorded against the image digest; and BASE-AC-17 — a
derived image requesting caveats outside its role layer's
`l0.caveat_ceiling` is refused at spawn.
<!-- atom:end id=SPEC-0081 -->

<!-- atom:begin id=SPEC-0082 -->
```yaml
id: SPEC-0082
type: specification
scope: story:story-0002
state: proposed
version: 1.0.0
instantiated_at: "2026-08-10T14:00:00Z"
author: consul-draft
authorized_by: null
title: "IO path: session stream to bus, live render, durable persistence"
tags: [acceptance-criterion, spawn-ac-2]
binding: checked
check: machine
story_ref: STORY-0002
```
The CLI session's stream-json output is captured by the harness and
published as ES-010 envelopes on acta.<citizen>.<story>.output; a
subscriber renders it live during the session (stub console sufficient);
the Acta consumer persists the same subjects (ES-031). No output path
exists except the bus: the container exposes no other egress for session
content.
<!-- atom:end id=SPEC-0082 -->

<!-- atom:begin id=SPEC-0083 -->
```yaml
id: SPEC-0083
type: specification
scope: story:story-0002
state: proposed
version: 1.0.0
instantiated_at: "2026-08-10T14:00:00Z"
author: consul-draft
authorized_by: null
title: "Isolation: ephemeral workspace, three sanctioned egress paths only"
tags: [acceptance-criterion, spawn-ac-3]
binding: checked
check: machine
story_ref: STORY-0002
```
Container inspection shows no host binds/volumes (BASE-AC-9 lineage);
kill -9 on the container mid-task leaves zero host residue; after a full
task run, durable effects exist only as git pushes, object-store writes,
and bus messages — verified by diffing host filesystem and enumerating
the three sinks.
<!-- atom:end id=SPEC-0083 -->

<!-- atom:begin id=SPEC-0084 -->
```yaml
id: SPEC-0084
type: specification
scope: story:story-0002
state: proposed
version: 1.0.0
instantiated_at: "2026-08-10T14:00:00Z"
author: consul-draft
authorized_by: null
title: "Attribution: every message and commit chain-verifiable to the leaf"
tags: [acceptance-criterion, spawn-ac-4]
binding: checked
check: machine
story_ref: STORY-0002
```
Every published envelope verifies per ES-013 (sig, chain walk, act token);
every commit produced in the session is signed with a key enrolled under
the leaf and verified at the merge gate; an envelope signed outside the
chain, and a commit signed by an unenrolled key, are both rejected (rogue
fixtures required, must fail).
<!-- atom:end id=SPEC-0084 -->

<!-- atom:begin id=SPEC-0085 -->
```yaml
id: SPEC-0085
type: specification
scope: story:story-0002
state: proposed
version: 1.0.0
instantiated_at: "2026-08-10T14:00:00Z"
author: consul-draft
authorized_by: null
title: "Supervision: interrupt, mid-session injection, clean terminate"
tags: [acceptance-criterion, spawn-ac-5]
binding: checked
check: machine
story_ref: STORY-0002
```
The harness demonstrates, on a live session: (a) interrupt of in-flight
generation with the session surviving; (b) injection of a follow-up
instruction that observably alters subsequent behavior; (c) clean
termination with exit status captured and a final telemetry event
emitted. Session-mode control, not fire-and-forget: an implementation
that only submits prompts and awaits completion fails this criterion by
definition. This is the distinguishing hop over API-mode fleet evidence.
<!-- atom:end id=SPEC-0085 -->

<!-- atom:begin id=SPEC-0086 -->
```yaml
id: SPEC-0086
type: specification
scope: story:story-0002
state: proposed
version: 1.0.0
instantiated_at: "2026-08-10T14:00:00Z"
author: consul-draft
authorized_by: null
title: "Versioned measurement: CLI pinned, instabilities re-verified on bump"
tags: [acceptance-criterion, spawn-ac-pin]
binding: checked
check: machine
story_ref: STORY-0002
```
The CLI binary version and digest are pinned in the agent-layer build and
recorded in every evidence row this story emits. Two watched behaviors are
asserted by explicit probes at pin time and on every bump: the verbose
stream flag remains load-bearing for uninterrupted stream capture, and
bare/default-mode behavior does not silently drop configured hooks. A
version bump invalidates prior evidence for this story: SPEC-0081..0085
re-run in full against the new pin before it is adopted.
<!-- atom:end id=SPEC-0086 -->

---

<!-- atom:begin id=SPRINT-0001 -->
```yaml
id: SPRINT-0001
type: sprint
scope: platform
state: proposed
version: 1.1.0
instantiated_at: "2026-08-11T01:20:00Z"
author: agent-worker-story-0004
authorized_by: null
title: "Foundation sprint: base + spawn contract to convergence"
tags: [c1-path]
arc_ref: STRAT-0001
stories: [STORY-0001, STORY-0002]
gate: CTRL-0005
relations:
  - { rel: advances, target: STRAT-0001 }
```
Exit gate (ONT-042: the sprint gate is a convergence point, run against
real running components): the gate library suite executes STORY-0002's
full acceptance set end-to-end on the gold base image with the pinned
CLI — one horizontal pass through spawn, stream, isolate, attribute,
supervise. Green here is the platform's first walked hop.

The gate runs the full citizenship set, BASE-AC-1 through BASE-AC-17, in
one pass: BASE-AC-1..14 and 15..16 at the image level (SPEC-0071,
SPEC-0072 v1.1.0) and BASE-AC-9 and BASE-AC-17 at the harness (SPEC-0081
v1.1.0). Splitting the seventeen across two stories by where they are
testable does not split them at the convergence point — that is what
makes it one.
<!-- atom:end id=SPRINT-0001 -->

<!-- atom:begin id=STRAT-0001 -->
```yaml
id: STRAT-0001
type: strategy
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-10T14:00:00Z"
author: consul-draft
authorized_by: null
title: "Arc: C1 — one directive walked end to end with provenance"
tags: [c1-path]
horizon: "MVP build (PA-030 steps 4–8)"
outcomes:
  - "The PA-020 chain runs against real components with a clean evidence set"
  - "Standing queries report zero dangling, zero unevidenced, zero coverage gap for in-scope claims"
  - "Every interim posture exists as a governed atom per PA-021"
constraints: [RSTR-0002, RSTR-0003]
```
The integration-level intent for the MVP arc: prove the spawn contract
first (the risky hop opens the arc), then compose Consul, Rostra, and
data-access around the proven primitive rather than ahead of it.
<!-- atom:end id=STRAT-0001 -->
