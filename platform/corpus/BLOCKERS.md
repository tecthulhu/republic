# Blockers — raised impediments and their resolution

Blocker atoms (`BLK-`) are record-class: born `active` without ratification
(ONT-061), resolved by reference to the decision or evidence that lifted
them. `blocks` is the blocker's relation (ONT-050); no other atom type
carries it.

<!-- atom:begin id=BLK-0001 -->
```yaml
id: BLK-0001
type: blocker
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-11T06:10:00Z"
author: agent-worker-story-0004
authorized_by: null
title: "DEC-0001 enactment held until the corpus-integrity fixes land"
tags: [pre-ratification, corpus-integrity]
raised_by: consul-architect
blocks_refs: [DEC-0001]
escalation: platform-owner
resolved_by: EVID-lint-2026-08-11T060442
relations:
  - { rel: blocks, target: DEC-0001 }
  - { rel: derives, target: STORY-0003 }
```
The corpus that DEC-0001 ratifies must be the corrected one (D8 of
ARCHITECT_RESPONSE_001): duplicate sources of truth removed, the lint null
case failing closed, evidence claims environment-scoped. Enactment is held
until STORY-0003's acceptance set is green, at which point this blocker is
resolved by that evidence and the owner's enactment commit proceeds.

Cut under the owner's ruling on bootstrap report 002: STORY-0003 v1.0.0
carried `rel: blocks` directly, which is outside ONT-050 (`blocks` runs
blocker → any, and a story is not a blocker). The impediment moves here;
STORY-0003 v1.1.0 drops the relation.

v1.2.0 (D18) sets `resolved_by`. This became expressible only once evidence
rows were committed under the interim Acta (D17 / SPEC-0106): while records
lived in the ignored index, an EVID- reference could not resolve and the
blocker had no way to record its own lifting. The schema was right and the
storage was wrong.

The referenced row is a re-run, not the original STORY-0003 run: it is a
whole-tree atom-lint pass over the corpus *as corrected*, true at its own
timestamp, which is the sanctioned form under D20 — re-runs produce new
true-at-T rows and nothing is backdated. The original run's row existed only
in an ignored directory and is therefore gone, which is the precise defect
D17 rules against.
<!-- atom:end id=BLK-0001 -->
