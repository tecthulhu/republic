# Memory seed — first MEM- instances proving the type

<!-- atom:begin id=MEM-0001 -->
```yaml
id: MEM-0001
type: memory
scope: repo:eldritch-labs/platform
state: superseded
version: 1.1.0
instantiated_at: "2026-08-11T18:20:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Marker recognition is column-0 anchored; indented examples are inert"
tags: [context-control, superseded]
context_class: relevant
keywords: [encoding, markers, column-zero]
source_refs: [DOC-0000]
```
Learned during first lint run: the ONT-070a example inside the spec parsed as
a live atom until column-0 anchoring was ruled.

v1.1.0 records the lifecycle transition only (D26/D30): superseded by MEM-0003,
which carries the same content under the scope this repository actually has.
The content above is unchanged and remains true at its own time — what moved is
the state, and per ONT-015 a transition is itself a change and therefore a new
instance. v1.0.0, with `state: active` and the scope
`repo:eldritch-labs/platform` that was never this repository, stays addressable
in history. Note that the stale scope is preserved deliberately: correcting it
here would edit a memory, which ONT-049a forbids — grooming emits successors.
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

<!-- atom:begin id=MEM-0004 -->
```yaml
id: MEM-0004
type: memory
scope: platform
state: superseded
version: 1.1.0
instantiated_at: "2026-08-12T22:00:00Z"
author: agent-worker-story-0012
authorized_by: null
title: "A monitor must verify its target exists; usage-text-and-exit-0 is not observation"
tags: [tooling, doc-truth, superseded]
context_class: relevant
keywords: [watcher, exit-zero, verify-target]
source_refs: [SPEC-0092]
```
A background CI watcher was launched with a command-substituted run id that
resolved to empty, because the run did not exist yet. The CLI printed its usage
text and exited 0, and the zero was read as "watching" — a completion was reported
on the strength of a monitor that had never attached to anything.

Same defect family as the vacuous lint pass (SPEC-0092): a check whose null case
reports success. The rule generalizes past this tool — a monitor must confirm its
watched resource exists before its exit status means anything, and any wrapper built
for CI watching fails closed on a missing target. Practically: resolve the id first,
assert it is non-empty, then watch.

v1.1.0 records the transition only: superseded by MEM-0005, which generalizes the
rule past watchers after a third sibling appeared. Content unchanged and true at
its own time (D30).
<!-- atom:end id=MEM-0004 -->

<!-- atom:begin id=MEM-0005 -->
```yaml
id: MEM-0005
type: memory
scope: platform
state: active
version: 1.0.0
instantiated_at: "2026-08-12T22:00:00Z"
author: agent-worker-story-0012
authorized_by: null
title: "Verify a command against the world it claims to have changed, not its exit status"
tags: [tooling, doc-truth, groomed]
context_class: relevant
keywords: [exit-zero, verify-target, silent-failure]
source_refs: [SPEC-0092]
groomed_from: MEM-0004
relations:
  - { rel: supersedes, target: MEM-0004 }
```
A command whose failure path is indistinguishable from an empty success must be
verified against the world it claims to have changed. Its exit status is not
evidence. Three siblings of one rule, found separately:

- **The vacuous lint** (SPEC-0092): a check over zero atoms reported pass.
- **The watcher** (MEM-0004): an empty run id made the CLI print usage and exit 0,
  read as "watching"; then a non-empty id pointed at the *previous* commit; then a
  merge mid-flight left a branch whose run could never start.
- **`gh issue create --jq`**: the flag is unsupported, `|| true` swallowed the error,
  and empty issue numbers were reported as created issues. Caught by listing the
  issues.

The practice: after a command that should have changed something, read the thing it
changed — list the issues, match the run's head sha, count the parsed atoms. Bound
every wait so a target that can never exist reports instead of hanging.
<!-- atom:end id=MEM-0005 -->
