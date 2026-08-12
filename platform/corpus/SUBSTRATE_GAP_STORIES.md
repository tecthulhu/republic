# Substrate gap stories — human evidence, revocation runtime, provenance consistency

Three small stories chartered by ARCHITECT_RESPONSE_009 (D38, D39, D41). None
blocks STORY-0002; each closes a gap the C1 gate eventually needs closed. Cut
without `tracker_ref` per D27 — the reference is filled from the issue that
actually exists, in the commit that first needs it.

---

## STORY-0010 — human evidence

The one genuinely missing governance primitive (D39). Every other readiness number
has a mechanism; `check: human` claims have none, so `unbound_claims` cannot reach
zero however much code is written. Eleven claims are waiting on it today.

<!-- atom:begin id=STORY-0010 -->
```yaml
id: STORY-0010
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Human evidence: the signed-determination record for check: human claims"
tags: [governance-primitive, c1-gate]
tracker_ref: "gh:tecthulhu/republic#19"
acceptance: [SPEC-0116, SPEC-0117]
```
A human-evidence record is an `EVID-` atom whose `checker` is a human identity
rather than a tool identity. Evidence is evidence — the atom type does not fork;
what differs is the checker class, that it cannot be auto-emitted, and that its
authority is a signed act. Structurally, a human attesting "RSTR-0002 holds, verified
by inspection at digest X" is the same act as ratifying a decision, so it reuses the
machinery already built rather than adding a parallel one.
<!-- atom:end id=STORY-0010 -->

<!-- atom:begin id=SPEC-0116 -->
```yaml
id: SPEC-0116
type: specification
scope: story:story-0010
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Human-evidence records exist, are signed acts, and cannot be auto-emitted"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0010
```
A tool assembles a human-evidence record for a named claim at a named corpus digest
with `checker` set to a human identity, and refuses to emit one for a `check:
machine` claim. No automated path can produce a human-checker record: a fixture
demonstrates that the emitter requires an explicit human identity argument and that
the standing report counts such records only for claims whose `check` is `human`.
The record's authority is the signing commit that lands it, exactly as a ceremony's
is — no new authority mechanism is invented.
<!-- atom:end id=SPEC-0116 -->

<!-- atom:begin id=SPEC-0117 -->
```yaml
id: SPEC-0117
type: specification
scope: story:story-0010
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Human evidence goes stale on drift, and the eleven claims are evidenced once"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0010
```
A human-evidence record is true-at-T against the digest it names (ONT-014), so when
the claim's subject changes the record goes stale and the claim returns to
unevidenced — the same content-addressed staleness `--since` and the embedder
already implement, rather than a new expiry mechanism. A fixture proves a record
covering digest A stops counting once the corpus moves to digest B.

First real use is the acceptance test: the eleven `check: human` claims standing
today — RSTR-0002, RSTR-0004, RSTR-0009, RSTR-0012, SPEC-0001, SPEC-0003, SPEC-0010,
SPEC-0032, SPEC-0042, SPEC-0064, SPEC-0070 — are evidenced by the owner in one
reviewing pass, and `unbound_claims` reaches zero for the first time.
<!-- atom:end id=SPEC-0117 -->

---

## STORY-0011 — revocation runtime

D38 sequences this *after* the hop: the forward path (mint, attenuate, verify) must
prove out before teardown is worth building. What this story ends is P5 attesting a
design rule against a fixture tree instead of shipped behaviour.

<!-- atom:begin id=STORY-0011 -->
```yaml
id: STORY-0011
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Revocation runtime: downward revocation in the verifier, P5 behaviour-attested"
tags: [chain-verifier, post-hop]
tracker_ref: "gh:tecthulhu/republic#20"
acceptance: [SPEC-0118]
```
Revocation is the teardown path and is not on the C1 critical walk — a directive
produces work; it does not require revoking a leaf mid-hop. Until this lands, the
gap is a governed, visible posture (SPEC-0120) rather than a silent overclaim.
<!-- atom:end id=STORY-0011 -->

<!-- atom:begin id=SPEC-0118 -->
```yaml
id: SPEC-0118
type: specification
scope: story:story-0011
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "chainverify revokes downward; P5 tests the verifier, not a fixture tree"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0011
```
`base/l0/chainverify.py` implements revocation: a revoked node invalidates its
entire subtree and nothing above it (ENT-051), checked during the chain walk and
failing closed like every other predicate. CTRL-0002's P5 then derives its verdict
from the verifier rather than from a tree the suite built itself, which is what makes
it evidence of behaviour. The revocation credential's shape follows ENT-077
(break-glass, co-signed at renewal). On landing, SPEC-0120's posture is superseded —
not edited — and the one-algebra check (SPEC-0108) still passes, because revocation
lives in the same module as the rest of the algebra.
<!-- atom:end id=SPEC-0118 -->

---

## STORY-0012 — provenance consistency

D41: SPEC-0113 catches content changing without a version bump. This catches the
level beneath — a version bumped while the provenance fields stay behind, which
passes lint today while misattributing the authoring act.

<!-- atom:begin id=STORY-0012 -->
```yaml
id: STORY-0012
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Provenance consistency: a new version must carry a new authoring act"
tags: [gate, follow-on]
tracker_ref: "gh:tecthulhu/republic#21"
acceptance: [SPEC-0119]
```
Caught as a near-miss while amending DOC-0000 for DEC-0004: a no-op'd replacement
left the reconciliation's `author` and `instantiated_at` on an amended instance, so
the atom would have claimed authorship by the reconciler at the reconciler's
timestamp. Lint passed. Provenance can currently lie through this gate.
<!-- atom:end id=STORY-0012 -->

<!-- atom:begin id=SPEC-0119 -->
```yaml
id: SPEC-0119
type: specification
scope: story:story-0012
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "A version increment requires a fresh instantiated_at and a consistent author"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0012
```
The `--since` mode fails any atom whose `version` increments while
`instantiated_at` is unchanged from the prior instance: a new instance that claims
the previous instance's moment is not a new instance. It further fails an atom whose
`author` is inconsistent with the change class — an amendment carrying content
changes may not be authored by `ont-060-reconciliation`, whose only legitimate
change is a lifecycle transition. Fixtures demonstrate the stale-timestamp case and
the misattributed-author case caught, and a correctly-authored new instance passing.
<!-- atom:end id=SPEC-0119 -->

---

## The revocation posture

<!-- atom:begin id=SPEC-0120 -->
```yaml
id: SPEC-0120
type: specification
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Interim posture: revocation is model-attested, not behaviour-attested"
tags: [interim-posture, d38, ent-051]
binding: checked
check: machine
```
`chainverify` implements no revocation, so CTRL-0002's P5 derives its verdict from a
credential tree the suite constructed rather than from the verifier. SPEC-0056
(ENT-051's claim, "revocation walks downward only") is therefore attested against a
model of the rule and not against shipped behaviour, and this atom says so where a
reader of the standing report will see it.

The posture is itself checked, which makes it self-retiring: CTRL-0002 asserts that
the verifier exposes no revocation surface. When STORY-0011 implements one, that
assertion fails and forces this posture's supersession rather than letting it linger
as stale prose. Retirement condition: revocation in the chain verifier
(SPEC-0118), at which point P5 becomes behaviour-attested.
<!-- atom:end id=SPEC-0120 -->

<!-- atom:begin id=RULE-0081 -->
```yaml
id: RULE-0081
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Bind SPEC-0120 via CTRL-0002"
tags: [binding, interim-posture]
claim: SPEC-0120
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0120 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0081 -->
