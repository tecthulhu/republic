# Memory seed — first MEM- instances proving the type

<!-- atom:begin id=MEM-0001 -->
```yaml
id: MEM-0001
type: memory
scope: repo:eldritch-labs/platform
state: active
version: 1.0.0
instantiated_at: "2026-08-10T12:30:00Z"
author: agent-worker-demo
authorized_by: null
title: "Marker recognition is column-0 anchored; indented examples are inert"
tags: [context-control]
context_class: relevant
keywords: [encoding, markers, column-zero]
source_refs: [DOC-0000]
```
Learned during first lint run: the ONT-070a example inside the spec parsed as
a live atom until column-0 anchoring was ruled.
<!-- atom:end id=MEM-0001 -->

<!-- atom:begin id=MEM-0002 -->
```yaml
id: MEM-0002
type: memory
scope: platform
state: active
version: 1.0.0
instantiated_at: "2026-08-11T14:55:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "The L0 handoff is single-use: init unlinks it, so every start needs a fresh mint"
tags: [spawn-contract, l0]
context_class: relevant
keywords: [handoff, single-use, respawn]
source_refs: [DOC-0003, SPEC-0081]
```
`/l0/init` reads the three handoff files and unlinks them before the payload
starts, which is how BASE-AC-3 holds inside a capability-dropped container
(namespace manipulation is unavailable). The consequence is not stated in
DOC-0003: a handoff cannot be reused, so restarting a citizen against the same
mount fails at L0-011 with a missing-handoff exit, not a chain error. The
harness must mint per start, and anything that retries a spawn must re-mint
rather than re-run. Learned in STORY-0001 when the conformance suite's second
citizen start failed and the failure turned out to be the shredding working.
<!-- atom:end id=MEM-0002 -->
