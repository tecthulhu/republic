---
id: DOC-0006
type: document
title: Liveness Extension — Continuous Human Presence Verification
scope: platform
state: draft
version: 0.1.0
instantiated_at: "2026-08-10T12:00:00Z"
author: consul-draft
authorized_by: null
relations:
  - { rel: contains, target: "LIV-*" }
  - { rel: derives, target: "DOC-0005" }
---

# Liveness Extension — Continuous Human Presence Verification

This document specifies the application suite and factor collection that
proves continuous human presence to the persona custodian machinery of
Document 0.5 §8. It defines *how* presence is demonstrated; Document 0.5
defines *what* presence unlocks. Requirement IDs use the `LIV-` prefix.

**Design intent.** Conventional MFA proves presence once and trusts a long
TTL. This suite inverts that: short TTLs, re-confirmed continuously, through
factors chosen to be nearly frictionless — so that "a live person is at the
wheel" is a standing, decaying, cryptographically consumable fact rather than
a login event. Modeled on the watch-unlocks-phone interaction class: proof so
cheap you stop noticing it.

---

## 1. Composition rules — how this document binds to Document 0.5

**LIV-001** — **Non-bypass.** Every mechanism here terminates in one of
exactly two Document 0.5 outputs: a **lease renewal** (ENT-073) or a
**per-act assertion** (ENT-075/076). No liveness factor creates a third
authority path, extends a TTL without producing a renewal, or substitutes for
the hardware-token ceremony where Document 0.5 requires it.

**LIV-002** — **Factors weaken nothing.** Adding factors may shorten
intervals, raise convenience, or gate higher decay tiers; a factor collection
may never lower the requirements of ENT-071–077. In particular, no soft
factor (biometric, behavioral, proximity) ever substitutes for the hardware
token in lease renewal, and no factor collection removes the per-act device
assertion from authority-bearing acts.

**LIV-003** — **Signals are local; the mesh sees signatures.** Raw biometric
data, camera frames, audio, keystroke timings, and proximity measurements
never leave the device that captures them and are never published to the bus
or stored by the platform. A factor's only mesh-visible output is a signed
attestation from an enrolled device key: *factor class X verified at time T on
device D*. Verification happens at the sensor; the mesh consumes proofs.

**LIV-004** — **Configurable per persona, bounded by platform floor.** Each
human composes their own factor stack and cadences in the custodian's
standing policy (ratified like any policy change, per ENT-075). Platform-scope
law sets floors: minimum factor strength per decay tier, maximum interval per
tier, and the mandatory hardware ceremonies that no configuration removes.

---

## 2. The liveness tier model

**LIV-010** — Liveness is a decaying score consumed by the lease decay ladder
(ENT-074). Factors refresh tiers; tiers gate what the custodian may do:

| Tier | Meaning | Refreshed by | Custodian behavior |
|---|---|---|---|
| T3 — Ceremonial | Human present, deliberate, hardware-proven | Token PIN + touch (lease renewal); per-act assertion | Authority-bearing acts permitted (with per-act proof) |
| T2 — Active | Human demonstrably at the wheel now | Pulse confirmation, device biometric, watch-class proximity + activity | Full standing policy; auto-grants per policy |
| T1 — Ambient | Human plausibly nearby, not actively confirmed | Passive proximity, behavioral continuity | Read-class auto-grants; writes queue |
| T0 — Absent | No current proof | Timeout of all above | Everything queues; lease continues toward expiry |

**LIV-011** — Tiers decay downward on their own clocks; only a factor event
moves a tier up, and only to the ceiling that factor class permits (§4). T3 is
event-scoped, never standing: it exists for the duration of a ceremony or a
single authorized act, then falls to T2.

---

## 3. The application suite

**LIV-020** — **Desktop pulse app.** Resident application on the machine
where the hardware token is inserted. At the configured interval it prompts a
minimal confirmation — configurable among: token touch (strongest), platform
biometric (Touch ID / Windows Hello class), or hotkey + PIN (weakest
permitted). Each confirmation emits a signed T2 attestation; token-touch
confirmations MAY additionally execute a lease renewal when the renewal
window is open, so the dead-man tap rides an existing habit instead of being
a separate chore. Snooze is honest: it suppresses the prompt, not the decay.

**LIV-021** — **Phone app.** Enrolled as a persona child device with its key
in the phone's secure enclave, biometric-gated. Provides: (a) pulse
confirmations equivalent to LIV-020 via Face ID/fingerprint; (b) per-act
assertion approvals — each authority-bearing act arrives as its own
approval card showing the specific act (`DEC-0114: ratify`), confirmed
biometrically, single-use, minutes-TTL, per ENT-075 — deliberately *not*
one-push-and-in-for-the-session; (c) proximity attestation to a bound
machine (§4, proximity class).

**LIV-022** — **Watch extension.** The continuous-wear factor. Composes
wrist-detection (the watch knows it has been on a body continuously since its
last biometric unlock — the watch-unlocks-phone primitive) with proximity to
the bound phone or desktop. While worn-and-near, it emits periodic signed T1
attestations and can one-tap-confirm T2 pulses. Removal from the wrist drops
its attestation class immediately.

**LIV-023** — All suite components are enrolled device leaves under the
persona (ENT-078), individually revocable, and their attestations carry the
device identity — so the custodian's policy can weight factors per device and
a lost device's factor history is cleanly excisable.

---

## 4. The factor collection

**LIV-030** — Factor classes, their ceilings, and their standing. The
collection is deliberately plural: the design goal is that any given moment's
re-confirmation is satisfied by whichever factor is cheapest *right then*.

| Class | Mechanism | Ceiling | Standing |
|---|---|---|---|
| Hardware ceremony | Token PIN + physical touch | T3 | Mandatory; not configurable away |
| Per-act assertion | Enrolled-device biometric on a single named act | T3 (act-scoped) | Mandatory for authority acts |
| Device biometric | Face ID / Touch ID / Windows Hello confirming a pulse | T2 | Recommended default pulse factor |
| Pulse acknowledgment | Hotkey/tap + PIN on pulse prompt | T2 | Permitted; platform floor may restrict |
| Watch continuity | Wrist-detection since last unlock + proximity | T1 sustain, T2 on tap | Recommended |
| Proximity | Phone/watch near bound machine | T1 | Permitted with LIV-031 constraints |
| Behavioral continuity | On-device typing/interaction dynamics | T1 sustain only | Optional; LIV-032 constraints |
| Ambient co-presence | Devices proving same-room via shared local signal observation | T1, corroborating only | Optional |

**LIV-031** — **Proximity honesty.** Bluetooth RSSI alone is relayable and
spoofable; it may sustain T1 only. Where hardware supports it, ranging-grade
proximity (UWB or secure-channel time-of-flight) is REQUIRED for proximity to
contribute to T2, and then only in combination with a continuity factor
(watch-worn). Proximity never contributes to T3.

**LIV-032** — **Behavioral factors are sustainers, not authenticators.**
On-device behavioral continuity (typing cadence, interaction rhythm) may
extend an existing T1 between active confirmations. It may never raise a
tier, never confirm a pulse, and never contribute to any assertion. Rationale:
behavioral biometrics have material false-accept characteristics and drift;
they are evidence of *continuity of the same operator*, not proof of identity.

**LIV-033** — **Excluded factors.** The following are prohibited from the
collection, with rationale recorded to prevent re-litigation:

- **Voice verification prompts** — modern speech synthesis defeats speaker
  verification at commodity cost; a factor whose forgery is cheap and
  improving is negative security. Excluded at any tier.
- **Phone-call PIN confirmation** — inherits SIM-swap and call-interception
  exposure and carries the highest interruption cost of any candidate; worst
  on both axes this document optimizes.
- **Continuous camera-based face recognition** — periodic *on-device*
  platform biometric (Face ID class, with the platform's own liveness
  anti-spoofing) is admitted under the device-biometric class; a
  platform-operated continuous camera watch is excluded as
  disproportionately invasive relative to T-tier value, and as a standing
  sensor it violates the spirit of LIV-003 even when processed locally.
- **Server-side biometric matching of any kind** — violates LIV-003
  categorically.

**LIV-034** — **Anti-fatigue rule.** Prompt-based factors MUST be scheduled
against an interruption budget (per-hour ceiling in standing policy), and the
suite MUST prefer passive sustainment (watch, proximity) between deliberate
confirmations. A liveness system that trains its human to confirm reflexively
is security-negative; cadence tuning is a first-class configuration surface,
not an afterthought.

---

## 5. Failure and degradation

**LIV-040** — Factor unavailability (dead watch battery, phone left home)
degrades tiers per the decay ladder — it never hard-locks. The floor
experience with zero suite components functioning is exactly Document 0.5
without this extension: queued approvals until the next hardware ceremony.

**LIV-041** — Repeated failed confirmations (wrong PIN, failed biometric
beyond threshold) drop the persona to T0 immediately and flag the custodian
to require the hardware token for the next elevation. Suspicion degrades;
it does not auto-revoke — revocation remains a deliberate act (ENT-077).

---

## 6. Open items

1. **Interval floors/ceilings per tier** — platform-scope numbers for
   LIV-004; interacts with lease TTL bounds (Document 0.5 open item 5).
2. **UWB availability strategy** — whether T2-grade proximity ships in v1 or
   proximity is T1-only until ranging-capable hardware is assumed.
3. **Ambient co-presence inclusion** — ship in v1 or defer; corroboration
   value versus implementation surface.
4. **Attestation subject schema** — the bus subject and envelope shape for
   signed factor attestations (belongs with the Envelope & Subject Spec).
