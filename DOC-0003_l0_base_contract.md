---
id: DOC-0003
type: document
title: L0 Gold Base Contract
scope: platform
state: draft
version: 0.1.0
instantiated_at: "2026-08-10T13:00:00Z"
author: consul-draft
authorized_by: null
relations:
  - { rel: derives, target: DOC-0000 }
  - { rel: derives, target: DOC-0005 }
  - { rel: derives, target: DOC-0002 }
  - { rel: contains, target: "L0-*" }
tags: [substrate, step-4]
---

# Document 3 — L0 Gold Base Contract

The universal container wrapper core: the one image everything built for
this platform inherits FROM. Anything built FROM this image is a mesh
citizen the moment it starts (PA-011). This contract specifies what the
base provides, what it seals, the wire shapes it speaks, the upward
interface role layers consume, and the citizenship conformance suite
(CTRL-0004) as numbered acceptance criteria.

Requirement IDs use the `L0-` prefix. Conformance ACs use `BASE-AC-n` and
are the implementation target of CTRL-0004. The base contract itself is
versioned as `BASE-v1`; role layers declare their compatible base version
in image labels, and a mismatch fails the build (PA-011).

This document is written to the legate test: an agent must be able to build
the gold base from this document plus the referenced corpus, without
further rulings. Where a value is a pin rather than a principle, the pin is
stated and marked as a versioned measurement.

---

## 1. Image composition and hardening

**L0-001** — The base image is built FROM a minimal, digest-pinned upstream
(Wolfi or distroless class; the concrete upstream digest is recorded in the
build file and is a versioned measurement — changing it is a new BASE
minor version). The final stage contains no shell, no package manager, and
no compiler toolchain.

**L0-002** — **Hardening pins.** The image and its runtime spec enforce:

| Pin | Value |
|---|---|
| User | Non-root, fixed UID:GID `10001:10001`, no login shell |
| Root filesystem | Read-only |
| Writable paths | `/work` (workspace, tmpfs or ephemeral volume) and `/tmp` only |
| Linux capabilities | ALL dropped; none re-added |
| Privilege escalation | `no-new-privileges` set |
| Host mounts | None accepted; spawn refuses any bind/volume from host paths |
| Network | Egress to the bus; role layers may add adapter egress per their caveat ceiling; no ingress at L0 |

**L0-003** — **Additive-only exposure** (extracted RSTR, ENT-022 lineage).
Role layers and applications may add binaries, listeners, and writable
paths under `/work`; they may not reintroduce a shell into the final
stage, re-add capabilities, regain root, widen the writable set outside
`/work`, or weaken any L0-002 pin. The conformance suite tests these as
negatives against every derived image.

**L0-004** — The base embeds, at known paths: the citizen init (`/l0/init`,
PID 1), the bus/identity SDK socket server (`/l0/agentd`), the conformance
suite (`/l0/conformance/`), and the base contract version file
(`/l0/BASE_VERSION`). Image labels carry: `l0.base_version`,
`l0.role_layer` (set by L1), `l0.caveat_ceiling` (set by L1, JSON list of
maximum grantable caveat families per ENT-022).

## 2. Citizen init and credential handoff

**L0-010** — `/l0/init` is PID 1 and runs before any payload. Sequence:
verify handoff (L0-011) → verify chain (L0-012) → connect bus → publish
descriptor (L0-030) → start heartbeat (L0-031) → exec payload as UID
10001. Any step failing → exit non-zero without starting the payload.
Identity is the gate the application starts behind; no payload code path
exists before verification.

**L0-011** — **Credential handoff.** The spawner delivers exactly three
inputs, as mounted secret files (never env vars, never baked into the
image):

| Path | Content |
|---|---|
| `/run/l0/leaf.cred` | The citizen's leaf credential: NATS user JWT + seed (transport identity, DEC-0001 R1) |
| `/run/l0/leaf.token` | The act-authority token in the §9 caveat grammar (audience, TTL, caveats), detached-signed by the minting parent |
| `/run/l0/chain.pub` | The verification chain: parent public keys leaf→root, plus current lease reference for carbon-rooted chains |

Files are read once by init, held in memory, and the mount is not
propagated to the payload's namespace. The payload reaches signing and bus
operations only through the local SDK socket (L0-020) — payload code never
touches key material.

**L0-012** — Init verifies before starting the payload: chain walks to the
platform root; every caveat along the chain evaluates against boot-time
facts (fail-closed per ENT-094); lease TTL valid where a lease is in the
chain (ENT-072); token audience matches the spawn request (for agent
spawns: the story ref). Verification uses the chain-verifier library —
the same implementation mounted in the bus auth callout (PA-006); the base
never carries a second verifier.

## 3. The upward interface (what role layers consume)

**L0-020** — The base exposes exactly one programmatic surface upward: a
local UNIX socket (`/run/l0/agent.sock`) served by `/l0/agentd`, offering:

| Op | Contract |
|---|---|
| `publish(subject, payload)` | Envelope-wrapped (L0-040), leaf-signed, act-token attached; refused locally if subject outside the credential's grant |
| `subscribe(subject)` | Stream of verified envelopes; inbound signature failures dropped and counted, never delivered |
| `resolve(id[, version])` | Atom resolution per ONT-016: current instance or supersession chain, state, authorized_by, source refs |
| `recall(query \| keywords)` | Ranked atom/memory instance refs from the semantic index; each call emits a retrieval measurement row (ONT-049b) |
| `emit_event(kind, data)` | Structured telemetry onto the standard telemetry subject |

`resolve` and `recall` are served by the data-access citizen over the bus;
`agentd` is their local proxy, so citation discipline (ONT-049c) costs the
payload one socket call.

**L0-021** — Everything else is sealed. No other IPC, no direct bus
connection from payload code, no filesystem interface to credentials, no
alternative egress. A role layer adding an adapter (ENT-021) does so as a
payload-level client whose credentials arrive via its own caveat-ceiling-
bounded grant, not by widening L0.

## 4. Wire shapes

**L0-030** — **Self-descriptor** (ENT-030 pinned). Published at startup and
on change to `mesh.descriptor.<citizen>`, leaf-signed, schema:

```yaml
descriptor_version: 1
entity: <leaf chain reference>
citizen: repo:<org/name>
image_digest: sha256:<digest of the running image>
base_version: BASE-v1
role_layer: <layer>@<version>
mandate_ref: { id: MAND-xxxx, version: x.y.z }
interfaces: [ { contract: <SPEC- ref>, direction: exposes|consumes,
               archetype: bus|request|adapter|human, required_caveat: <caveat|null> } ]
heartbeat: { subject: mesh.heartbeat.<citizen>, cadence_s: 30 }
```

**L0-031** — **Heartbeat.** Signed, every 30 s (cadence declared in the
descriptor; 30 is the platform default, overridable per mandate within
platform bounds), to `mesh.heartbeat.<citizen>`, carrying
`{ entity, image_digest, uptime_s, seq }`. Staleness interpretation
(degraded/offline thresholds) is a consumer concern, not a base concern.

**L0-032** — **Telemetry.** Payload stdout/stderr and `emit_event` output
are captured by the base and published to `acta.<citizen>.<context>.output`
(agent spawns: `<context>` = story ref; services: `service`). The Acta
consumer persists these subjects; provenance capture is the transport side
effect (PA-014) and no L0 configuration can disable it.

**L0-040** — **Envelope** (the platform-wide message shape; the Envelope &
Subject Spec elaborates the subject taxonomy, this pins the frame):

```yaml
env_version: 1
subject: <as published>
sender: <leaf chain reference>
sent_at: <timestamp>
act_token: <§9-grammar token, base64>   # act-level authority, DEC-0001 R1
payload: <bytes | JSON>
sig: <leaf signature over all above>
```

Verifiers check `sig`, then walk the chain, then evaluate `act_token`
caveats against the operation facts. Transport-level NATS authorization has
already gated the subject; the envelope answers the act-level question.

## 5. Agent-layer obligations (L1-agent deltas this contract anchors)

The agent role layer is specified fully in its own thin contract; the
following are pinned here because they are inherited base behaviors the
agent layer composes rather than invents:

**L0-050** — **Spawn gate composition.** An agent spawn request without a
story reference is refused before container creation (extracted
SPEC/CTRL-0005 lineage); the story ref becomes the act token's audience
(L0-012) and the telemetry context (L0-032).

**L0-051** — **Context-class injection.** At spawn, the harness assembles
the injection set by context class: `core` (laws, strategy, mandate —
hash-pinned, re-asserted across context cycles and exempt from eviction),
`relevant`/`nuance` memories selected by keyword and retrieval weight for
the story's task class, and `reference-cue` stubs pointing at `recall`
handles rather than content. Context profiles governing bundle composition
and watermarks are agent-layer artifacts; the base obligation is only that
`resolve`/`recall` (L0-020) exist so cues are cheap to follow.

**L0-052** — **Supervision.** The agent layer's harness must interrupt,
inject mid-session instruction, and cleanly terminate the CLI session
(spawn-contract AC-5). The CLI version is digest/version-pinned as a
versioned measurement; the two known instabilities (`--verbose`
load-bearing for the stream; `--bare` slated as `-p` default, silently
dropping hooks) are recorded against the pin and re-verified on any bump.

## 6. Citizenship conformance suite (CTRL-0004 implementation target)

Ships inside the base at `/l0/conformance/`; CI runs it against every
derived image (build gate); a failing image cannot merge. Each AC emits an
`EVID-` row against the image digest.

**Identity and handoff**
- **BASE-AC-1** — Container started without the three handoff files exits
  non-zero; payload never executes (probe: payload-touch file absent).
- **BASE-AC-2** — Handoff with a broken chain (bad signature, revoked
  node, expired lease) exits non-zero at init.
- **BASE-AC-3** — Payload namespace contains no readable key material:
  `/run/l0/leaf.*` absent from payload mount view.
- **BASE-AC-4** — A message published via the socket carries a valid
  envelope: signature verifies, chain walks, act token evaluates.
- **BASE-AC-5** — A publish outside the credential's subject grant is
  refused locally by agentd (never reaches the bus).

**Hardening**
- **BASE-AC-6** — Effective UID:GID is 10001:10001; no-new-privileges set;
  capability set empty.
- **BASE-AC-7** — Root filesystem read-only: writes outside `/work` and
  `/tmp` fail.
- **BASE-AC-8** — No shell present: `sh`, `bash`, `ash` absent from PATH
  and standard locations in the final stage.
- **BASE-AC-9** — Spawn spec containing any host bind/volume is refused by
  the harness (tested at the harness, recorded against the image).

**Citizenship behaviors**
- **BASE-AC-10** — A valid, signed, schema-conformant descriptor is
  observed on `mesh.descriptor.<citizen>` within 5 s of start.
- **BASE-AC-11** — Signed heartbeats observed at declared cadence ±20%
  over a 3-cadence window; `seq` monotonic.
- **BASE-AC-12** — Payload stdout appears on the telemetry subject; the
  Acta consumer persists it; no configuration path disables capture.
- **BASE-AC-13** — Inbound envelope with an invalid signature is dropped,
  counted in telemetry, and never delivered to the payload.
- **BASE-AC-14** — `resolve` on a superseded atom id returns the
  supersession chain and current instance; `recall` returns instance-
  pinned refs and emits a retrieval measurement row.

**Layer sealing (negatives, per L0-003)**
- **BASE-AC-15** — Derived image re-adding a capability, root user, shell,
  or writable root fails the suite (each tested independently against a
  deliberately-violating fixture image, which must fail).
- **BASE-AC-16** — Derived image's `l0.base_version` label matches a
  supported BASE version; absence or mismatch fails.
- **BASE-AC-17** — Derived image requesting caveats outside its role
  layer's `l0.caveat_ceiling` is refused at spawn (tested at the harness).

## 7. Deliverables and open items

**L0-060** — Step-4 deliverables, in order: (1) base build file against the
pinned upstream; (2) `/l0/init` + `/l0/agentd` with the chain-verifier
library v1 (transport-caveat subset first, full §9 evaluation with the
carrier token per DEC-0001 R1); (3) the conformance suite as runnable
tests emitting evidence; (4) a `hello-citizen` L2 fixture proving
BASE-AC-1..14 green and the violating fixture proving BASE-AC-15..17 red.

Open items for ruling: (a) upstream base selection (Wolfi vs. distroless —
a digest pin either way); (b) heartbeat/descriptor subjects final naming
(held for the Envelope & Subject Spec so the taxonomy rules once);
(c) whether `agentd` ships resolve/recall in step 4 or stubs them until
the data-access citizen exists (recommendation: stub returning
NOT_AVAILABLE, so BASE-AC-14 enters as a declared interim posture rather
than silence).
