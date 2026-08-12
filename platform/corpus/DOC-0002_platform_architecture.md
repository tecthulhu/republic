---
id: DOC-0002
type: document
title: Platform Architecture — Enforcement Plane, Core Components, MVP
scope: platform
state: draft
version: 0.1.2
instantiated_at: "2026-08-12T20:00:00Z"
author: agent-worker-dec-0004
authorized_by: null
relations:
  - { rel: derives, target: DOC-0000 }
  - { rel: derives, target: DOC-0005 }
  - { rel: contains, target: "PA-*" }
---

# Document 2 — Platform Architecture

The architecture that enforces the ontology (Layer 1), the core components it
governs (Layer 2), and the MVP that proves the whole chain (Layer 3).
Requirement IDs use the `PA-` prefix. This document references the extracted
corpus (REQUIREMENTS_REGISTER, CONTROLS, ENFORCEMENT_RULES) rather than
restating its claims.

---

## 1. The enforcement plane

**PA-001** — The enforcement plane consists of exactly: the atom store, the
atom index, `atom-lint` (CTRL-0001), the gate library, the evidence emitter,
and the chain verifier. No rules engine, policy server, or governance service
exists; governance runs on PR mechanics, embedded libraries, and generated
indexes.

**PA-002** — **The atom store is git.** Platform-scope atoms live in the
governance repo; repo-scope atoms live in each citizen's repo. Ratification
is physically the signed merge that lands a decision atom (ENT-079: the
merge is the signed adopting act). History immutability implements
ONT-012/015; the store is append-only in instance space.

**PA-003** — **The atom index is generated, never authored** (ONT-016). It
is rebuilt from the store by the data-access citizen's consumer and serves
all standing queries (ONT-080/089, ENT-041). Index loss is an inconvenience,
never a truth loss.

**PA-004** — **The gate library** is one implementation mounted at three
chokepoints, consuming only the `checkable` and `enforceable` facets:

| Gate | Mount | Enforces (representative) |
|---|---|---|
| Build gate | CI | CTRL-0001/0002/0003 rules; citizenship conformance (CTRL-0004) |
| Spawn gate | Harness | Story-required spawn, mandate resolution, strategy hash, restriction arming (CTRL-0005 rules) |
| Runtime gate | Bus auth callout + envelope check | Chain walk, lease TTL, caveat evaluation (CTRL-0006 rules) |

**PA-005** — **Evidence emission is structural.** Every control invocation
passes through the evidence emitter; an `EVID-` atom is written to the
provenance stream per run. No control can execute without recording.

**PA-006** — **The chain verifier** is a single implementation of the §9
grammar (ENT-091–094) plus chain-walk and lease-TTL checking (ENT-072),
embedded in both the bus auth callout and the gate library. Its wire-token
format is a constrained deliverable of DEC-0001 R1: NATS-native credentials
for transport identity; grammar-caveated tokens in the envelope for
act-level authority.

**PA-007** — **The persistence pipeline** (data-access citizen) is one
transaction-shaped path: persist instance → compute embedding under the
resolved band instrument → write index row with full measurement provenance
(ONT-085/088). Provenance capture and embedding are side effects of the
transport chokepoint, not disciplines.

## 2. Container and component topology

**PA-010** — **Container-first is absolute for citizens.** The harness and
deploy tooling know only how to start containers; no host-execution path
exists to outgrow. Citizens mount nothing from the host; durable effects
exist only via git push, object store write, and bus publish.

**PA-011** — **The image hierarchy**: L0 gold base (hardening, identity
init, bus citizenship, heartbeat, self-descriptor, telemetry, conformance
suite) → L1 role layers (agent, service, ui, data-access), each FROM the
base by digest, adding only its role delta and declaring its caveat ceiling
in image labels → L2 applications, FROM a role layer by digest. Floating
tags are prohibited anywhere in the chain. The conformance suite ships
inside the base and runs against every derived image in CI (ENT-032).

**PA-012** — **Core citizens** (all L0-derived):

| Citizen | Role layer | Responsibility |
|---|---|---|
| Consul | service | Intake, decomposition, fan-out, merge orchestration; drafts atoms, never ratifies |
| Rostra | ui | Stateless render of bus streams; approval/veto surface; humans connect to the bus as themselves |
| Data-access | data-access | Sole store-speaker: index, object store (Tabularium), Acta durable consumer, embedder pipeline |
| Agent workers | agent | One container per story; supervised CLI session; ephemeral workspace |
| Persona custodians | service | One per human: standing policy, notary, lease holder, veto queue (post-MVP; see PA-021) |

**PA-013** — **Adopted infrastructure**: the bus (NATS + JetStream — also
the runtime identity root and KV presence), the relational store, and the
object store (S3 API; MinIO local). Admitted by digest-pinned allowlist,
reachable only behind their fronting citizens (ENT-023), except the bus,
which is the substrate itself.

**PA-014** — **One IO path.** UI and agent containers never address each
other; both speak only the bus. Agent output streams to
`acta.<agent>.<story>.output`; the Rostra subscribes; the data-access
consumer persists the same subjects. One wire, three consumers; audit is
the transport.

**PA-015** — **External surfaces**: the tracker (GitHub Issues first-class
default, JIRA adapter) holds all story status (ONT-044); repos hold code
and repo-scope atoms; the object store holds artifacts and evidence detail.
The platform adapts to infrastructure and never provides it (scope law).

## 3. MVP — the C1 slice

**PA-020** — The MVP is the following chain running against real
components, each clause an acceptance specification (story-scoped SPEC-
atoms at cut time):

signed human directive at the Rostra → consultum recorded in the Acta →
story + acceptance SPECs drafted by the Consul → story reflected to GitHub
Issues → spawn gate refuses story-less spawn, then mints a story-scoped
leaf and starts a hardened agent container with laws and strategy injected →
supervised session (interrupt, inject, terminate) with output streaming
live → merge gate runs CTRL-0001 and acceptance controls, emitting
evidence → artifact merges only on pass → provenance walk resolves
directive → decision → story → identity → artifact → standing queries
report zero dangling, zero unevidenced, zero coverage gap for the in-scope
set.

**PA-021** — **Interim postures, declared** (each carried as a waiver or
labeled posture atom at cut time, never as silence): custodian-lite (direct
hardware-token CLI signing; no standing presence, no two-party minting);
transport-only caveats (NATS subject scoping; grammar tokens and decay
ladder await the chain-verifier deliverable); agent role layer only under
full citizenship conformance (ui/data-access citizens may run as scaffolds);
liveness suite parked; JIRA, semantic enforcement rungs, and federation out.

**PA-022** — **MVP done-test**, stated as the numbers it reads (ONT-080 as
amended by DEC-0004): the PA-020 chain's evidence set passes; for in-scope
claims `unbound_claims = 0` and `unevidenced_claims = 0`; the embedding
coverage gap is zero; `dangling_claims = 0` as a drift guard; and every
PA-021 item exists as a governed posture atom. Done is a query result
(ONT-081).

The coverage number is `unbound_claims`, not `dangling_claims`. The two are
not interchangeable and this requirement previously named the wrong one:
ONT-060 activates a claim only when a rule binds it, so `dangling_claims` is
structurally zero at activation and cannot measure whether the law is wired
up (ONT-080a). It stays in the list because a nonzero reading means a rule
was removed from under a live claim, which is an incident worth gating on.

## 4. Build order

**PA-030** — Sequence, each step gated by its predecessor's evidence.
**Evidence is environment-scoped** (ONT-014): a step is achieved *in a named
environment against a subject digest*, never in the abstract, and
re-verifies per environment. An untimed, unscoped "achieved" is the decayed
statement ONT-014 describes.

1. Corpus + schemas + atom-lint green (evidenced in the drafting
   environment against corpus@a1084129, and re-verified in the worker
   environment — first evidence emitted).
2. Grammar property suite green (evidenced in the drafting environment,
   re-verified in the worker environment).
3. Embedder pipeline + index + standing queries running (evidenced in the
   drafting environment under the B0 lexical instrument; re-verification
   required per environment, dependencies pinned in tools/requirements.txt;
   semantic instrument is a band re-resolution).
4. Gold base image + conformance suite (CTRL-0004) against a hello-citizen.
5. Agent layer + harness: spawn gate + supervised session (CTRL-0005;
   pinned CLI version — the spawn contract remains the risky hop).
6. Chain verifier v1 (CTRL-0006) in the bus auth callout.
7. Minimal Consul + Rostra + data-access; tracker adapter.
8. C1 run; PA-022 query; ship gate.
