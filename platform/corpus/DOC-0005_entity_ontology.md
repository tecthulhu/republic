---
id: DOC-0005
type: document
title: Entity Interface Ontology
scope: platform
state: ratified
version: 1.0.0
instantiated_at: "2026-08-11T19:06:00Z"
author: consul-draft
authorized_by: DEC-0001
relations:
  - { rel: contains, target: "ENT-*" }
  - { rel: derives, target: "DOC-0000" }
---

# Document 0.5 — Entity Interface Ontology

This document governs **runtime actors**: the identity-bearing entities of the
platform, their chain positions, their citizenship classes, and the interfaces
at which they touch one another. It is the peer of Document 0 (Ontology
Specification) at the substrate layer.

The dependency runs one way. This document references Document 0 downward for
every contract binding: interface contracts are `SPEC-` atoms, conformance is
enforced through `RULE-` bindings, runtime attestations are `EVID-` records,
and authority grants are `MAND-` atoms. Document 0 does not depend on this
document, and entity types defined here are not atom types (ONT-005).

Requirement IDs use the `ENT-` prefix.

---

## 1. The single entity type

**ENT-001** — There is exactly one entity type: the **identity-bearing
actor**. A human's core identity, a human persona, a browser session, an
agent's service certificate, and a spawned sub-agent worker are all instances
of this one type at different chain positions. No component may define a
second entity type or branch behavior on human-versus-agent distinctions
outside the descriptive `kind` property (ENT-010).

**ENT-002** — Every entity is a node in exactly one **identity chain**: a
signing chain rooted at the platform root keypair, in which each node's
credential is signed by its parent with attenuating caveats.

```
Root (platform root keypair, cold)
 └─ Persona        (human@platform, or a citizen's service certificate)
     └─ Surface    (browser A, CLI session, spawned worker)
         └─ Leaf   (second browser, sub-agent, tab)
```

The depth labels are illustrative, not fixed: chains may be shorter or deeper.
What is fixed is the direction of authority.

**ENT-003** — **The attenuation law.** A child credential can never carry a
capability absent from its parent's grant. Authority strictly narrows with
depth. "Weaker identity" means strictly narrower scope — never a lower
numeric trust score. No trust scores exist in this system; scoring invites
runtime inference of authority, which is prohibited (ENT-004).

**ENT-004** — Authority is **granted, never inferred**. An entity's
capabilities are the intersection of its credential caveats and its governing
mandate's `imperium` (ONT-040). No runtime component may widen, promote, or
infer an entity's authority from its behavior, history, or kind. Verification
is a chain walk to root; a credential that does not verify, or that claims a
capability outside its chain's grants, is rejected at the surface it presents
to.

**ENT-005** — Human and silicon entities authenticate through the same
machinery. Human leaf enrollment uses device-bound keypairs (WebAuthn-class),
making each browser or device a genuine cryptographic subset of the person.
Agent leaves are minted by their spawner (the harness) at container start.
Both produce the same credential shape; every downstream consumer — gates,
veto, provenance, envelope signing — operates on chain position and caveats,
agnostic to what kind of actor holds the key.

---

## 2. Entity properties

Three orthogonal properties describe every entity. Only one bears authority.

**ENT-010** — **Kind**: `carbon | silicon | infrastructure`. Descriptive
only. Kind MAY inform presentation (a UI showing a human icon) and MUST NOT
inform authorization, gating, veto, or verification logic. Any branch on kind
in an enforcement path is a defect.

**ENT-011** — **Chain position**: `{ parent, depth, caveats }`. This is the
authority-bearing property, per ENT-003/004. The caveat language is defined
in §9.

**ENT-012** — **Citizenship class**:

| Class | Definition | Obligations |
|---|---|---|
| `citizen` | Runs in the mesh; image inherits the gold base (L0). | Full L0 contract: hardening, identity init, bus citizenship, health, telemetry, self-description. |
| `adopted` | Vendor image (bus, database, object store) admitted by digest pin and allowlist. | Sits behind a citizen; never directly addressed by other citizens except its fronting citizen and the L0 substrate itself. |
| `external` | Touches the mesh but does not run in it: humans, the tracker, cloud object stores, model providers. | Interacts only through `adapter` or `human` interfaces (ENT-021). |

**ENT-013** — Citizens are born through the birth process (conception →
scaffold → mandate ratification → conformance → first heartbeat). A citizen's
mandate (`MAND-`) is its standing authority record; its birth is authorized by
a decision (`DEC-`), giving the population itself provenance. Adopted
infrastructure is admitted by decision with a digest-pinned allowlist entry;
external entities are never admitted, only interfaced.

---

## 3. Interfaces

**ENT-020** — An interface is not a freestanding thing. An interface is a
**binding between an entity's surface and a contract**: the contract is a
`SPEC-` atom describing the shape (subjects and schemas, endpoints and
payloads, or interaction flow), and the binding declares which entity exposes
it, in which direction, and what caveat is required to invoke it.

```yaml
interface:
  contract:      # SPEC- reference. REQUIRED.
  direction: exposes | consumes
  archetype: bus | request | adapter | human
  required_caveat:   # Caveat an invoking credential must carry. REQUIRED
                     #   for exposed interfaces; empty means chain-valid-only.
```

**ENT-021** — Four **interface archetypes** cover the platform. No fifth may
be added without a new version of this document.

| Archetype | Definition | Declared by |
|---|---|---|
| `bus` | Subjects spoken and consumed on the message bus, envelope schema ref. | Emitted in the self-descriptor (ENT-030) — never hand-authored. |
| `request` | Synchronous API surface (endpoints, payloads). | Role-layer contract plus per-citizen additions in the descriptor. |
| `adapter` | Outbound contract to an external entity: tracker, object store, model provider. | The consuming citizen's descriptor. The only archetype permitted to cross the citizenship boundary outward. |
| `human` | Interaction surfaces for carbon entities: chat, veto inbox, status views. | UI-role citizens. Human leaves bind here via device-bound credentials. |

**ENT-022** — Interface contracts follow the layered exposure rule: a role
layer may add interfaces to those of the gold base; it may not remove,
weaken, or reopen what a lower layer sealed. The caveat ceiling of a
citizen's role layer bounds the `required_caveat` values it may demand and the
adapter caveats it may request (image ancestry is an input to identity
scoping).

**ENT-023** — Only `adapter` interfaces touch `external` entities, and only
`citizen`-class entities may hold adapter caveats (e.g., store credentials are
grantable solely within the data-access role layer's ceiling). An `adopted`
entity is reachable only through its fronting citizen. This makes the
citizenship boundary checkable: any credential grant or traffic path that
violates it is a conformance failure, not a style concern.

---

## 4. The self-descriptor

**ENT-030** — Every citizen publishes a **self-descriptor** at startup and on
change, signed by its identity leaf, on the standard descriptor subject. The
descriptor is the runtime attestation of this document's claims for that
entity:

```yaml
descriptor:
  entity:           # Identity-chain reference of the publishing leaf.
  citizen:          # repo:<org/name>.
  image_digest:     # The running image, by digest.
  base_version:     # Gold base contract version (e.g. BASE-v1).
  role_layer:       # L1 layer and version.
  mandate_ref:      # MAND- reference.
  interfaces:       # List of interface bindings per ENT-020.
  heartbeat:        # Liveness cadence and subject.
```

**ENT-031** — Descriptors are **emitted, never authored**. They are the
descriptive-class documentation of the entity population (per the two-class
documentation rule): registry views, subject catalogs, and topology renderings
are queries over live descriptors. A hand-maintained registry of entities is
prohibited — it would reintroduce the drift class this architecture removes.

**ENT-032** — Descriptor publication and validity are gold-base obligations,
tested by the citizenship conformance suite: a derived image that cannot emit
a valid, signed, schema-conformant descriptor fails CI.

---

## 5. Conformance

**ENT-040** — Interface conformance uses Document 0 machinery end to end.
For each exposed interface: the contract is a `SPEC-`, a `CTRL-` verifies the
running entity honors it (schema conformance of emitted messages, endpoint
behavior against contract, caveat enforcement on invocation), a `RULE-` binds
them with an enforcement, and each verification run produces an `EVID-`
record. "Does citizen X actually expose what it declares" is therefore an
evidence query, never an integration meeting.

**ENT-041** — Declared-but-unverified interfaces are the entity-side dangling
claim. The standing query *interfaces in active descriptors with no passing
evidence against the current image digest* joins the launch-readiness gate
alongside Document 0's dangling-claims and unevidenced-claims queries
(ONT-080).

**ENT-042** — A citizen whose runtime behavior exceeds its descriptor
(speaking an undeclared subject, exposing an undeclared endpoint, invoking
with a caveat it was not granted) is in violation. The enforcement path is the
standard ladder (ONT-034): deterministic-critical violations gate;
non-critical drift raises a blocker (`BLK-`); nothing kills. Undeclared
surface is treated as a defect of the citizen, not of the observer.

---

## 6. Entity lifecycle

**ENT-050** — Entities have a runtime lifecycle distinct from the atom
lifecycle (atoms: ONT-060; entities are not atoms):

```
minted → active ⇄ suspended → retired
                     ↓
                  revoked
```

| Transition | Trigger |
|---|---|
| minted → active | Credential verifies; for citizens, first valid descriptor + heartbeat observed. |
| active → suspended | Tribune-class veto, or a suspend-escalate enforcement. Reversible. |
| suspended → active | Human release via the veto surface. |
| active/suspended → retired | Orderly end: container exit, session end, credential expiry. |
| any → revoked | Credential revocation. Terminal for that leaf; revocation of a node revokes its entire subtree. |

**ENT-051** — Revocation walks downward only, mirroring attenuation: revoking
a parent invalidates all descendants; revoking a leaf touches nothing above
it. Ephemeral leaves (browser sessions, spawned workers) SHOULD carry short
TTLs so retirement is the default outcome and revocation the exception.

**ENT-052** — Every lifecycle transition is recorded to the provenance stream
with the acting identity. Suspension and revocation additionally require a
reference: the veto record or the enforcement/decision that triggered them.

---

## 8. The persona custodian and human liveness

Carbon entities require a live custodian for their standing authority, exactly
as silicon citizens require a running container. This section defines that
custodian and the proof-of-human structure that bounds it.

**ENT-070** — Each human persona is represented in the mesh by a **persona
custodian**: a citizen-class container, born through the birth process,
inheriting the gold base, emitting a descriptor, addressable on the bus. The
custodian holds the human's standing policy, notarizes routine leaf minting,
queues escalations and veto items for that human, and provides the human's
standing presence for delegation decisions made in their absence.

**ENT-071** — **The persona key never enters the custodian.** The persona key
resides on a hardware token (PIN- and user-presence-protected, capable of
arbitrary payload signing). The custodian holds only a **custodian lease**: a
caveated, TTL-bounded credential minted by the persona key on the token. All
leaves the custodian notarizes chain through the lease:

```
Root (cold, offline)
 └─ Persona key (hardware token)
     └─ Custodian lease (container; TTL = dead-man window)
         └─ Session / surface / delegation leaves (short TTL)
```

**ENT-072** — **Dead-man property.** Every verifier — gates, bus
authentication, merge checks — validates lease TTL at every chain walk
(this obligation is a `SPEC-` bound by rule to the chain-walk control). On
lease expiry, everything downstream of the lease fails verification
mesh-wide without any revocation event or watchdog. Cessation of the human's
periodic proof and cessation of the custodian's authority are the same fact,
by construction.

**ENT-073** — **Lease renewal is a presence ceremony.** Renewal requires the
hardware token: PIN plus physical user-presence confirmation. Each renewal
may carry fresh caveats (narrowed policy for travel, read-only windows,
lowered imperium ceilings). Renewal cadence is human-configurable within
platform bounds.

**ENT-074** — **Decay ladder.** Lease caveats SHOULD encode age thresholds so
custodian authority attenuates as the last proof-of-presence recedes: full
standing policy in the fresh window; auto-grants narrowing to read-class with
all else queued in the stale window; nothing verifying past TTL. A missed
renewal degrades gracefully to queued approvals, never to a cliff lockout.

**ENT-075** — **Notary restriction** (`RSTR-` class). The custodian assembles,
countersigns, applies policy, and records; it never originates authority.
Authority-bearing acts — ratify, veto, waive, enroll, revoke — require a live
per-act device assertion from the human in addition to a valid lease. Routine
attenuation within standing policy may proceed on the lease alone. Any path
by which the custodian performs an authority-bearing act without a per-act
human proof is a violation, checked pre and post per restriction semantics
(ONT-032).

**ENT-076** — **Two-party minting.** Leaf minting requires both the
custodian's lease signature and a fresh assertion from an enrolled device of
the human. Neither the custodian alone nor a stolen device alone is
sufficient.

**ENT-077** — **Break-glass revocation.** At each renewal the token co-signs
a sealed revocation credential for that specific lease, held outside the
custodian. Publishing it revokes the lease and its entire subtree
immediately (ENT-051 downward walk). Custodians are disposable: recovery is
destroy, re-instantiate, re-lease — never repair-in-place.

**ENT-078** — **Enrollment ceremony** (resolves open item 3). Cold root mints
the persona key onto the hardware token (offline ceremony). The token mints
the first custodian lease into a freshly born custodian container. The
custodian then enrolls the human's surface devices (passkeys,
commit-signing keys, CLI device keys) as persona children. All subsequent
device enrollment and revocation routes through the custodian under ENT-075
rules; recovery from total custodian loss routes through the cold root.

**ENT-079** — **Unsigned input is draft.** Input arriving through surfaces
that cannot sign (external chat interfaces, tracker comments, email) enters
the provenance stream as an unattributed candidate. No atom transition,
ratification, or veto proceeds from it until a signed surface adopts it via a
per-act assertion. Provenance records both hops: origin of the words, and the
signed act that gave them force.

**ENT-080** — **Continuous liveness (extension surface).** The renewal and
per-act ceremonies of ENT-073/075 define *what* must be proven. The
mechanisms by which presence is proven continuously and non-intrusively —
pulse applications, proximity attestation, multi-factor liveness collections
— are specified in the companion **Liveness Extension** (DOC-0006). That
document composes with this section solely by producing the assertions and
renewals defined here; it may not weaken any requirement of §8, and its
factors feed the lease/assertion machinery rather than bypassing it.

---

## 9. The caveat grammar

This section defines the limiter grammar: the language in which credential
caveats are expressed and verified. It is the credential-layer half of a
two-layer condition system; the rule-layer half (the exception grammar for
waivers and conditional enforcements) lives in Document 0 §5.5, and the two
MUST NOT be interchanged (ENT-095).

**ENT-091** — **A caveat is a conjunction of guard predicates.** Each
predicate tests one fact from the fixed vocabulary (ENT-092) against a
literal or a chain-supplied value. A caveat set contains no disjunctions
across authorities, no else-branches, no alternative outcomes, and no side
effects. The grammar is restriction-only: a caveat can narrow what a
credential permits and can never widen, substitute, or conditionally swap
authority.

```
caveat      := predicate ( AND predicate )*
predicate   := fact op literal
op          := = | != | < | <= | > | >= | in | prefix-of
```

**ENT-092** — **The fact vocabulary** is fixed by this document and supplied
by the verifier at evaluation time. Predicates over facts outside the
vocabulary fail closed (ENT-094).

| Fact family | Facts | Enables |
|---|---|---|
| Time | `now`, `mint_time`, `lease_age` | TTLs, decay ladder (ENT-074) |
| Operation | `subject`, `action`, `resource` | Scope limits, read-class windows |
| Audience | `audience` | Act-scoped credentials (ENT-075), e.g. `audience = DEC-0114` |
| Use | `use_count` | Single-use semantics, e.g. `use_count < 1` |
| Chain | `depth`, `parent_id`, `lease_id` | Positional and lease-referencing limits |

Extending the vocabulary requires a new version of this document via the
decision process.

**ENT-093** — **Composition is union; attenuation is algebraic.** A child
credential's effective caveat set is the union of every caveat set along its
chain to root. Because every caveat only restricts, union of caveats is
intersection of authority: monotonic attenuation (ENT-003) is a property of
the algebra, not a policed convention. No operation exists that removes,
overrides, or relaxes an inherited caveat.

**ENT-094** — **Verification is fail-closed with no else.** At each chain
walk, the verifier evaluates every predicate of every caveat along the full
chain against current facts. All predicates hold → the authority survives
this check. Any predicate fails, references an unknown fact, or cannot be
evaluated → the action is denied. There is no fallback branch, no
alternative rule, no partial grant. In the caveat grammar, "otherwise" is
always "otherwise: no."

**ENT-095** — **Layer separation** (`RSTR-` class). Exception-grammar
constructs (given/when/then conditional rule modification, Document 0 §5.5)
MUST NOT appear inside credentials, and limiter caveats MUST NOT be used to
express rule exceptions. Rationale: a credential that can conditionally
select which rule applies is escalation-capable, breaking ENT-003 at the
grammar level; conversely, rules legitimately admit governed exceptions
(waivers) that credentials never may. Rules may have exceptions; credentials
may only have limiters.

**ENT-096** — **Dual-audience rendering.** The canonical caveat form is the
predicate structure the verifier evaluates. A human-readable rendering in
given/when phrasing ("applies only when lease_age < 48h and action is
read-class") is generated from the canonical form for display surfaces.
Display forms are descriptive-class: generated, never authored, never
evaluated.

**ENT-097** — **Carrier independence.** This grammar is defined
independently of its wire carrier. The standing recommendation for the
carrier remains the hybrid of open item 1: NATS-native chains for transport
identity, with caveated tokens of this grammar carried in the message
envelope for act-level authority. Ratifying this section does not foreclose
the carrier ruling; the carrier ruling must implement this section without
loss.

---

## 10. Bootstrap and open items

**ENT-090** — This document enters the lifecycle at `draft` and is ratified
alongside Document 0 by the platform's first decisions. Its conformance
machinery activates when the gold base conformance suite (which carries the
descriptor and interface checks) reaches `active`.

Open items requiring rulings:

1. **Credential carrier** — narrowed by §9: the caveat *grammar* is now
   specified (ENT-091–097) and carrier-independent; what remains is the wire
   carrier ruling. Working direction per ENT-097: NATS-native chains for
   transport identity plus §9-grammar caveated tokens in the envelope for
   act-level authority. Ruling formalizes the carrier and its token format.
2. **Descriptor change semantics** — full re-publication versus delta events
   on interface change.
3. **Human persona enrollment ceremony** — resolved by ENT-078; ruling
   ratifies the ceremony as written.
4. **Adopted-entity attestation** — whether adopted infrastructure gets a
   thin descriptor published *by its fronting citizen* on its behalf, so the
   entity population query covers the whole topology.
5. **Lease TTL and decay bounds** — platform minimum/maximum for renewal
   windows and decay thresholds (ENT-073/074).
