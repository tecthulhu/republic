---
id: DOC-0004
type: document
title: Envelope & Subject Specification
scope: platform
state: draft
version: 0.1.0
instantiated_at: "2026-08-10T13:30:00Z"
author: consul-draft
authorized_by: null
relations:
  - { rel: derives, target: DOC-0000 }
  - { rel: derives, target: DOC-0005 }
  - { rel: derives, target: DOC-0003 }
  - { rel: contains, target: "ES-*" }
tags: [substrate, wire]
---

# Document 4 — Envelope & Subject Specification

The one wire everything shares: the subject taxonomy, the envelope byte
contract, the act-token wire format (closing the DEC-0001 R1 carrier
deliverable), and the stream/retention bindings. L0-040 pinned the envelope
frame; this document is its full elaboration and the single naming
authority for subjects — L0-030/031/032's subject placeholders resolve
here (L0 open item b).

Requirement IDs use the `ES-` prefix. This document is written to the
legate test.

---

## 1. Subject taxonomy

**ES-001** — All platform subjects live under exactly four roots. No
citizen may publish outside these roots; new roots require a new version of
this document.

| Root | Purpose | Producers |
|---|---|---|
| `mesh.*` | Citizenship signals: presence, description, entity lifecycle | L0 base (init/agentd) only |
| `acta.*` | Provenance and telemetry: everything that happened | L0 base capture + gate evidence emitters |
| `work.*` | Coordination: directives, decomposition, packets, results | Consul, agents, Rostra, custodians |
| `data.*` | Request/reply services: resolution, recall, index queries | Data-access citizen (responder); any citizen (requester) |

**ES-002** — **Grammar.** Subjects are dot-delimited tokens matching
`[a-z0-9-]+`. Dynamic segments are constrained:

```
mesh.descriptor.<citizen>
mesh.heartbeat.<citizen>
mesh.entity.<citizen>.<transition>        # minted|active|suspended|retired|revoked
acta.<citizen>.<context>.output           # context = story id (kebab) | service
acta.<citizen>.<context>.event            # structured emit_event telemetry
acta.evidence.<control>                   # EVID- emission per control run
acta.retrieval.<citizen>                  # ONT-049b measurement rows
work.directive.<persona>                  # signed human directives (Rostra origin)
work.story.<story>.assign                 # Consul → agent fan-out
work.story.<story>.result                 # agent → Consul completion
work.veto.<persona>                       # tribune queue items and releases
data.resolve                              # request/reply (ES-030)
data.recall                               # request/reply (ES-030)
data.query.<name>                         # standing queries by name
```

`<citizen>` is the repo short-name (kebab); `<story>` is the tracker id
(kebab); `<persona>` is the persona short-name. The taxonomy is closed:
subjects not matching a pattern above are refused by agentd locally
(BASE-AC-5 lineage) and denied by transport permissions.

**ES-003** — **Transport permission derivation.** NATS subject permissions
in a leaf's transport credential are *derived from* its act-token caveats
at mint time by the minting parent — the transport grant is always a
superset-free projection of the act grant (an agent leaf for story S gets
publish on `acta.<self>.<S>.*` and `work.story.<S>.result`, subscribe on
`work.story.<S>.assign` and its inbox; nothing else). Transport never
grants what the act token would deny; where projection cannot express a
caveat (time, use-count), transport permits and the envelope check denies
(DEC-0001 R1: transport concerns transport).

## 2. Envelope

**ES-010** — The envelope is JSON, UTF-8, one envelope per NATS message.
Field order is not significant; unknown fields MUST be ignored on read
(tolerant reader) and MUST NOT be emitted by conforming writers (closed
writer, ONT-051 lineage).

```json
{
  "env_version": 1,
  "subject": "acta.east-agent.story-0042.output",
  "sender": { "leaf": "<leaf public key>", "chain": "<chain head id>" },
  "sent_at": "2026-08-10T13:30:00Z",
  "seq": 118,
  "act_token": "<base64url, ES-020>",
  "payload_type": "text|json|ref",
  "payload": "<utf-8 text | JSON object | object-store ref>",
  "sig": "<base64url Ed25519 over the signing form>"
}
```

**ES-011** — **Signing form.** `sig` is Ed25519 by the sender leaf over
the canonical serialization (JCS / RFC 8785) of the envelope with `sig`
removed. Verifiers MUST canonicalize identically; any canonicalization
failure is a verification failure (fail closed).

**ES-012** — **Size discipline.** Envelopes above 128 KiB MUST carry
`payload_type: ref` with the payload in the object store
(content-addressed digest ref). The Tabularium write happens first; the
envelope references it; large payloads never ride the bus.

**ES-013** — **Verification order** (every consumer, and the bus auth
callout for gated subjects): (1) `sig` verifies against `sender.leaf`;
(2) chain walks to root with lease TTL checked at every hop (ENT-072);
(3) act token evaluates against operation facts (ES-022). Failure at any
step: drop, count in telemetry, never deliver (BASE-AC-13). Steps run in
that order so the cheapest check fails first.

## 3. Act token — the carrier wire format (DEC-0001 R1 closed)

**ES-020** — The act token is a compact JSON object, base64url in the
envelope, detached-signed by the minting parent (not by the leaf — the
token is the parent's grant *to* the leaf):

```json
{
  "tok_version": 1,
  "leaf": "<leaf public key this token empowers>",
  "parent": "<minting parent public key>",
  "chain_ref": "<parent's own token | lease id | root>",
  "minted_at": "2026-08-10T13:00:00Z",
  "caveats": [
    [ ["audience","=","story-0042"], ["lease_age","<",48] ],
    [ ["action","in",["publish","request"]] ]
  ],
  "parent_sig": "<base64url Ed25519 over JCS of the above>"
}
```

`caveats` is a list of caveat blocks; each block is a conjunction of
`[fact, op, literal]` predicate triples in the §9 grammar (ENT-091/092) —
lists of lists, no objects, so no field can smuggle an exception construct
(ENT-095 made unrepresentable, the ONT-032 pattern applied to the wire).

**ES-021** — **Chaining.** A leaf's effective caveat set is the union of
`caveats` in its token and every token/lease reachable through
`chain_ref` to root (ENT-093). Tokens are attenuation-only by
construction: a child token adds blocks and can remove nothing; verifiers
evaluate the full union.

**ES-022** — **Operation facts** supplied by the verifier at evaluation:
`now`, `mint_time` (token's), `lease_age` (from the chain's lease, where
present), `subject`, `action` (publish|request|subscribe-deliver),
`resource` (subject's dynamic segments), `audience` (context binding:
story id for agent work, DEC- id for ratification acts), `use_count`
(from the verifier's replay ledger for single-use tokens), `depth`,
`parent_id`, `lease_id`. Exactly the ENT-092 vocabulary; a predicate over
anything else fails closed.

**ES-023** — **Single-use and replay.** Tokens carrying a `use_count`
predicate are tracked by verifier-side ledger keyed on
`hash(parent_sig)`; the ledger is a data-access responsibility with a
short retention window bounded by the token's own TTL caveat. Tokens
without time or use caveats are refused at mint by policy for
authority-bearing acts (ENT-075 lineage: ratification tokens are always
audience-bound, TTL-bounded, single-use).

## 4. Streams and retention

**ES-030** — JetStream bindings (adopted-infrastructure configuration,
digest-pinned with the bus):

| Stream | Subjects | Retention |
|---|---|---|
| `ACTA` | `acta.>` | Permanent; the provenance record. Persisted by the data-access consumer to durable store + object store detail |
| `MESH` | `mesh.>` | Interest-based, 7 d; descriptors/heartbeats are re-emitted state, not history of record — entity lifecycle transitions are additionally mirrored to `acta.` by the emitting init |
| `WORK` | `work.>` | Work-queue semantics; acked on consumption; 30 d safety window |

`data.*` is plain request/reply — no stream; results that matter are
whatever the responder persisted already (ONT-016: the index is
regenerable, the store is truth).

**ES-031** — The Acta consumer writes: raw envelope (verbatim, for
signature re-verification forever), extracted `EVID-`/`PROV-`/retrieval
rows where the payload declares them, and the embedding row per ONT-085 —
one pipeline, per PA-007.

## 5. Conformance

**ES-040** — This document's machine-checkable claims bind to CTRL-0005
(gate library suite: envelope verification order, size discipline,
subject refusal) and CTRL-0006 (chain verifier suite: token chaining,
union evaluation, replay ledger, projection consistency ES-003). Two
fixtures are required alongside the suites: a golden set of valid
envelopes/tokens (must verify) and a rogue set — bad canonicalization,
smuggled object in `caveats`, widened child token, replayed single-use,
subject outside taxonomy — every one of which must fail.

Open items for ruling: (a) JCS canonicalization library pin per
implementation language (a versioned measurement); (b) `MESH` retention
window (7 d proposed); (c) whether `work.directive.*` payloads embed the
full signed directive or a `ref` (recommendation: full embed under 128 KiB
so the provenance chain's first hop never depends on store availability).
