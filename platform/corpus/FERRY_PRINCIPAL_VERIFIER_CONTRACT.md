<!-- ingest: instruction -->
<!-- ingest-ref: FERRY_SYSTEM_CHARTER_v0.4 §5(3b) §6, DOCUMENT_CONVENTIONS_v1.0 -->
---
title: FERRY_PRINCIPAL_VERIFIER_CONTRACT
version: "0.1"  # canonical; pinned instance FERRY_PRINCIPAL_VERIFIER_CONTRACT_v0.1.md
type: instruction
state: proposed
floor: kyle-scott
date: 2026-08-20
owner_session: architect (ee6adc89-…)
truth_level: intent
layer: substrate  # mechanics/contract; FERRY_SYSTEM_CHARTER_v0.4 is the integrator above it
authorizes: nothing until RATIFIED with the charter it serves
---

# Ferry Principal-Verifier Contract v0.1

**Purpose:** define the ONE extendable port through which the ferry obtains human (principal) authorization-in-presence for a shipment. The contract is the stable law; providers are swappable implementations. This spec defines conformance, maps **Duo Auth API** as the first conforming provider (proving applicability), and deliberately catalogs nothing else — a future provider is a conformance exercise, not a spec change.

## 1. The contract

### 1.1 Types

```
Challenge:
  shipment_id      str      # stable shipment ID (charter §3)
  manifest_digest  str      # sha256 of the manifest being authorized
  summary          str      # one human-readable line (e.g. "consolidation ceremony → proposed/")

Verdict:
  result           enum     # APPROVED | DENIED | TIMEOUT | PROVIDER_ERROR
  evidence         Evidence # present for ALL results (refusals are logged too)

Evidence:
  provider         str      # provider's registered name
  ref              str|null # provider's transaction/reference id (e.g. Duo txid)
  timestamp        str      # ISO8601, provider-side where available, else local
  binding          str      # what the human actually saw/confirmed — see 1.3
  truth_level      str      # provider's honest self-description — see 1.3
  detail           dict     # provider-specific extras (never load-bearing for the verdict)
```

### 1.2 The one method

```
verify(principal: str, challenge: Challenge, timeout_s: int) -> Verdict
```

Semantics, non-negotiable for conformance:
- **Fail-closed:** only `APPROVED` authorizes. `DENIED`, `TIMEOUT`, `PROVIDER_ERROR` — and any exception — leave the shipment `CREATED` with the Verdict logged (charter §5 step 3b). A provider MUST NOT retry into an approval after a deny.
- **Challenge-bound:** the provider MUST present as much of the Challenge to the human as its channel allows, and MUST declare in `binding` what was actually presented. Approving a blind prompt and approving a digest-on-screen are different facts; the contract forces the difference onto the record.
- **Evidence always:** every call returns Evidence, including refusals — the refusal log is part of the custody record.
- **No secrets in Evidence:** credentials never appear in Verdicts, logs, or registers (charter B-4).

### 1.3 Honest self-description (the conformance clause that matters most)

Every provider declares, statically:
- `truth_level` ∈ `evidence` (offline-cryptographically-verifiable artifact) | `attested-witnessed` (independent third-party transaction record) | `attested-local` (local-only assertion, e.g. passphrase prompt).
- `binding` ∈ `digest-in-challenge` (human saw the manifest digest) | `summary-only` (human saw a description, not the digest) | `session-only` (human approved presence, saw nothing shipment-specific).

These two strings are copied verbatim into the shipment's AUTHORIZED event and the `enrolled_principals` register row. **The register never claims more than the provider declares; a provider that overstates its truth_level is non-conformant by definition.** (DOCUMENT_CONVENTIONS truth-level discipline, applied to identity factors.)

### 1.4 Selection & registry

`~/.ferry/config.yaml` (gitignored, ship-side local state) selects the provider by name and holds its credentials. `ferry.py` maps name → class in a small registry. Adding a provider = one conforming class + one config stanza. Removing Duo someday = a config edit. Nothing else moves.

### 1.5 Enrollment half

`enroll-principal` delegates a provider-specific `enrollment_ref()` → a string identifying the principal within the provider (Duo: the Duo username). The reception-side `enrolled_principals` row records: principal, provider, enrollment_ref, `truth_level`, `binding`, date, genesis/floor note. Changing providers later = a new register row (append-only), old row superseded in the open.

## 2. Duo Auth API — first conforming provider (applicability proof)

| Contract element | Duo mapping |
|---|---|
| Availability check | `GET /auth/v2/check` (validates ikey/skey/host) |
| Principal exists / can auth | `POST /auth/v2/preauth` (username) → `auth` result required |
| `verify()` | `POST /auth/v2/auth` — `factor=push`, `username=<principal>`, `device=auto`, **`pushinfo=shipment=<id>&digest=<sha256[:16]>…&summary=<text>`** (URL-encoded k/v pairs rendered in the push), synchronous mode; Duo blocks until approve/deny/timeout |
| `result` mapping | Duo `allow` → `APPROVED`; `deny` → `DENIED`; timeout → `TIMEOUT`; HTTP/signature errors → `PROVIDER_ERROR` |
| `evidence.ref` | Duo `txid` |
| `evidence.timestamp` | response time (Duo Admin API auth log holds the witnessed record; txid joins them) |
| `truth_level` | `attested-witnessed` |
| `binding` | `digest-in-challenge` (digest rendered in pushinfo; truncated display is recorded as such in `detail`) |
| Auth | HMAC-SHA1-signed requests per Duo Auth API spec — **stdlib-only** (`hmac`, `hashlib`, `email.utils`, `urllib`); no SDK; ferry.py stays one file |
| Credentials | ikey/skey/api-host in `~/.ferry/config.yaml`; never logged, never in Evidence |
| Free-plan status | **Confirmed by the floor 2026-08-20: Auth API application created under Duo Free.** |

Conformance verdict: Duo satisfies every clause including 1.3's honesty requirements. The contract is proven applicable. (Known limit, recorded: pushinfo display truncates long values on some devices — the full digest is in the signed request and the log; the human may see a prefix. `detail.displayed_digest_prefix` records what was sent for display.)

## 3. Deliberately not defined

No catalog of future providers. `login_duo` (fallback, `binding: summary-only`), FIDO2/passkey local signatures (`truth_level: evidence`), TOTP, or anything else: each is a conformance exercise against §1 when and if wanted — a class and a config stanza, never a spec change. Defining them now would be speculation; the contract's job is to make them cheap later, and it does.

## 4. Conformance checklist (for any future provider)

1. Implements `verify()` with the exact fail-closed semantics (1.2).
2. Declares `truth_level` and `binding` honestly (1.3); declarations survive adversarial reading.
3. Returns Evidence on every path including refusals; no secrets in Evidence.
4. Enrollment half provides `enrollment_ref()`; register row written append-only.
5. Zero changes required outside its own class + config stanza.

## Change log
- **2026-08-20 v0.1** — initial contract: types, single verify() method, fail-closed semantics, honest self-description clause (truth_level/binding as mandatory conformance), registry/config selection, enrollment half; Duo Auth API mapped end-to-end as the first conforming provider (floor-confirmed available on Duo Free); future providers deliberately uncataloged.
