# Story bindings and declared postures

Rule bindings and interim-posture atoms for STORY-0001 and STORY-0008. Postures
are written as checked claims rather than comments so a deviation is something the
suites test and the standing queries can see, never silence (PA-021).

## STORY-0001

STORY-0001's acceptance specifications become *enforceable* only when an active
rule binds them (ONT-036: an unbound claim is a proposal). The three rules below
are that binding, mounting CTRL-0004 at the build gate with ENF-0001 —
the governed form of SPEC-0073's sentence "a red suite blocks merge".

SPEC-0074 records the one deviation SPEC-0071 permits: `resolve`/`recall` are
stubbed until the data-access citizen exists. It is written as a checked claim
rather than a comment, so the interim posture is a thing the suite tests and the
standing queries can see — the L0 open item (c) recommendation carried out
(PA-021: every interim posture exists as a governed atom, never as silence).

<!-- atom:begin id=SPEC-0074 -->
```yaml
id: SPEC-0074
type: specification
scope: story:story-0001
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Interim posture: resolve/recall answer NOT_AVAILABLE until data-access exists"
tags: [interim-posture, l0-open-item-c]
binding: checked
check: machine
story_ref: STORY-0001
```
`agentd` serves the L0-020 surface in full except `resolve` and `recall`, which
return the error `NOT_AVAILABLE` together with the posture reason. Both are
served by the data-access citizen over the bus (PA-030 step 7), which does not
exist at step 4; a stub that answers honestly is preferable to an op that
appears to work. BASE-AC-14 is therefore satisfied as a declared posture, and
the conformance suite asserts the stub's exact response so the deviation cannot
quietly become permanent. This atom is superseded — not edited — when
`resolve`/`recall` begin answering.
<!-- atom:end id=SPEC-0074 -->

<!-- atom:begin id=RULE-0076 -->
```yaml
id: RULE-0076
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Bind SPEC-0071 via CTRL-0004"
tags: [binding, step-4]
claim: SPEC-0071
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0071 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0076 -->

<!-- atom:begin id=RULE-0077 -->
```yaml
id: RULE-0077
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Bind SPEC-0072 via CTRL-0004"
tags: [binding, step-4]
claim: SPEC-0072
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0072 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
The falsifiability half: this rule is satisfied only when the violating fixture
*fails* the suite, which is why the control is invoked twice with opposite
expectations at the build gate.
<!-- atom:end id=RULE-0077 -->

<!-- atom:begin id=RULE-0078 -->
```yaml
id: RULE-0078
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Bind SPEC-0073 via CTRL-0004"
tags: [binding, step-4]
claim: SPEC-0073
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0073 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0078 -->

<!-- atom:begin id=RULE-0079 -->
```yaml
id: RULE-0079
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Bind SPEC-0074 via CTRL-0004"
tags: [binding, step-4, interim-posture]
claim: SPEC-0074
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0074 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0079 -->

## STORY-0008

<!-- atom:begin id=SPEC-0115 -->
```yaml
id: SPEC-0115
type: specification
scope: story:story-0008
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T17:00:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Interim posture: evidence embeds in batch, with coverage-zero as the gate"
tags: [interim-posture, d25, ont-085]
binding: checked
check: machine
story_ref: STORY-0008
```
ONT-085 requires embedding to be a non-optional side effect of persistence. In
bootstrap there is no streaming persistence pipeline: controls write their own
evidence rows into `acta/` directly, so a synchronous embed-at-persistence is not
available to honor. The posture, stated rather than left implicit: embedding runs
in batch, and **a non-empty coverage gap is a red condition** — the standing-query
report is the meter, satisfied by running the embedder before the report. ONT-085's
non-optionality is carried by the gate instead of by the write path.

The consequence is honest and bounded: between a control run and the next embedder
run, the newest evidence rows have no vector, so coverage is momentarily nonzero by
construction rather than by neglect. This atom is superseded — not edited — when the
data-access citizen's durable consumer (PA-007) makes persistence synchronous, at
which point embed-at-persistence holds literally and the gate becomes redundant.
<!-- atom:end id=SPEC-0115 -->

<!-- atom:begin id=RULE-0080 -->
```yaml
id: RULE-0080
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T17:00:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Bind SPEC-0115 via CTRL-0007"
tags: [binding, interim-posture]
claim: SPEC-0115
control: CTRL-0007
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0115 }
  - { rel: binds, target: CTRL-0007 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0080 -->
