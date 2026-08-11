# STORY-0001 bindings and declared postures

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
