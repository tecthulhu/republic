# Controls

<!-- atom:begin id=CTRL-0001 -->
```yaml
id: CTRL-0001
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "atom-lint"
tags: [enforcement-plane]
target: codebase
implementation: tools/atom_lint.py
```
Parses ONT-070a boundaries and frontmatter, validates schemas, ids, references, fixed fields, model literals, embedding fields, exception placement
<!-- atom:end id=CTRL-0001 -->

<!-- atom:begin id=CTRL-0002 -->
```yaml
id: CTRL-0002
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "grammar property suite"
tags: [enforcement-plane]
target: artifact
implementation: tools/test_grammar.py
```
Property tests over the caveat algebra: attenuation monotonicity, fail-closed verification, layer separation, downward revocation
<!-- atom:end id=CTRL-0002 -->

<!-- atom:begin id=CTRL-0003 -->
```yaml
id: CTRL-0003
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "lifecycle transition checker"
tags: [enforcement-plane]
target: codebase
implementation: tools/atom_lint.py#transitions
```
Validates lifecycle transitions in change history against the state machine and decision authorization
<!-- atom:end id=CTRL-0003 -->

<!-- atom:begin id=CTRL-0004 -->
```yaml
id: CTRL-0004
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "citizenship conformance suite"
tags: [enforcement-plane]
target: runtime
implementation: suite/citizenship
```
Runs against every derived image: hardening, identity init, descriptor, heartbeat, interface conformance, layer sealing
<!-- atom:end id=CTRL-0004 -->

<!-- atom:begin id=CTRL-0005 -->
```yaml
id: CTRL-0005
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "gate library suite"
tags: [enforcement-plane]
target: runtime
implementation: suite/gates
```
Tests spawn, merge, and runtime gates: story-required spawn, injection order, restriction pre/post, unsigned-input draft rule
<!-- atom:end id=CTRL-0005 -->

<!-- atom:begin id=CTRL-0006 -->
```yaml
id: CTRL-0006
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "chain verifier suite"
tags: [enforcement-plane]
target: runtime
implementation: suite/chain
```
Tests the identity walk: chain-to-root, lease TTL at every hop, imperium ceilings, two-party minting, break-glass
<!-- atom:end id=CTRL-0006 -->

<!-- atom:begin id=CTRL-0007 -->
```yaml
id: CTRL-0007
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "embedder pipeline suite"
tags: [enforcement-plane]
target: artifact
implementation: tools/test_embedder.py
```
Tests per-atom chunking, measurement provenance completeness, instrument digest pinning, generated-rendering rule
<!-- atom:end id=CTRL-0007 -->

<!-- atom:begin id=CTRL-0008 -->
```yaml
id: CTRL-0008
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "index and query suite"
tags: [enforcement-plane]
target: artifact
implementation: suite/index
```
Tests standing queries: dangling claims, unevidenced claims, coverage, provenance walk, append-only store
<!-- atom:end id=CTRL-0008 -->
