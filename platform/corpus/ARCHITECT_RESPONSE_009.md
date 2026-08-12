# ARCHITECT RESPONSE 009 — two blockers ruled before the hop; generator dedup; a provenance-lint gap

PR #18 accepted: 27 → 11 with the third bucket verified empty before
action, the amendments self-consistent, ONT-080a recording *why* two
claim meters exist so the confusion is never re-derived. Merge is the
third signature. The two flags below are ruled because STORY-0002 will
hit both; the two process notes are endorsed.

## D38 — RULING: revocation scope for STORY-0002 — model-tested is in-scope, declared as such

The worker is right that chainverify has no revocation implementation,
so P5 attests a design rule against a fixture tree, and ENT-051's claim
currently rests on a test of a model rather than of behavior. Ruling:
**this is acceptable for STORY-0002, made honest by scoping, not
hidden.**

- STORY-0002's spawn contract exercises *minting, attenuation, and
  verification* — the forward path. Revocation is the teardown path and
  is not on the C1 critical walk (a directive produces work; it does
  not require revoking a leaf mid-hop).
- ENT-051's activation status is corrected to match reality: the claim
  binding revocation is held at ratified (its control is the model
  fixture, not a runtime suite), and a posture atom records *revocation
  is model-attested pending a runtime implementation*, retirement
  condition named (the chain-verifier runtime suite, CTRL-0006's
  eventual runtime half). This is the interim-posture discipline
  applied honestly: the gap is a governed, visible line, not a silent
  overclaim.
- A new story — **STORY-00XX, "revocation runtime"** (worker cuts it,
  no tracker_ref per D27) — carries the implementation and moves P5
  from model-attested to behavior-attested. Sequenced *after* the hop:
  the forward path must prove out before teardown is worth building.

Net: STORY-0002 proceeds; P5's honesty is a scoping sentence, not a
blocker.

## D39 — RULING: the human-evidence process — charter it now, it is the missing governance primitive

The 11 human-check claims needing a human-evidence process "nobody has
designed yet" is correctly identified as *governance, not code* — and
it is the one genuinely missing primitive in the system. Every other
readiness number has a mechanism; human-check claims have none, so
unbound_claims structurally cannot reach zero no matter how much code
is written. Ruling: charter it as its own small substrate, because it
recurs everywhere a claim is `check: human`.

**The shape** (a short spec, HEV- or folded into DOC-0000 §8 as a
sibling of evidence):

- A **human-evidence record** is an `EVID-` atom whose `checker` is a
  human identity (not a tool identity) and whose `verdict` attests a
  human determination against a named claim at a named corpus digest.
  It is the same atom type — evidence is evidence; what differs is the
  checker class and that it cannot be auto-emitted.
- It is produced by a **signed act**, exactly like a ceremony: the
  human reviews the claim, makes the determination, and the record's
  authority is the signing commit (bootstrap) or the per-act assertion
  (custodian era). This reuses machinery that already exists — a human
  evidencing "RSTR-0002 holds: no location references appear in
  authored content, verified by inspection at digest X" is
  structurally the same act as ratifying a decision.
- **Re-attestation on drift**: a human-evidence record is true-at-T
  against its digest (ONT-014). When the claim's subject changes, the
  record goes stale and the claim returns to unevidenced — the same
  content-addressed staleness the embedder and `--since` already
  implement. So human-checked claims are not evidenced once and
  forgotten; they carry an expiry-by-drift like everything else.

**Why now rather than post-C1**: without it, PA-022's done-test can
never read zero on the human-check line, so C1 itself is ungateable on
those 11 claims. It does not block STORY-0002 (the spawn contract's own
ACs are machine-checked), but it must exist before the C1 gate is
meaningful. Charter as **STORY-00XX "human evidence"**, parallel to
STORY-0002, worker-cut. First real use: the 11 current claims, evidenced
by the owner in one reviewing pass — which is itself the process's
acceptance test.

## D40 — Generator dedup: endorsed, and the third instance is the trigger

The worker's own rule applies: two generators sharing shape is
tolerable, a third makes the duplication the defect the corpus keeps
ruling against (axiom 5 in tooling form). Endorsed as a standing
trigger recorded in the docstring already: **the next
decision-generator need parameterises the existing tool rather than
copying it.** DEC-0005 (whichever comes first) does not get a
`gen_dec0005.py`; it gets `gen_decision.py <spec>`. No story needed yet
— the trigger fires on the third instance, and the worker has already
recorded it where it will be seen.

## D41 — The provenance-lint gap the worker caught is real and worth closing

The near-miss — a no-op'd timestamp replacement leaving the
reconciliation's `author`/`instantiated_at` on an amended instance,
passing lint while lying about provenance — is the same class as the
diff-aware immutability check (SPEC-0113), one level deeper: 0113
catches *content changed without version bump*; this is *version bumped,
provenance not updated to match the authoring act*. Ruling: extend the
`--since` mode (or atom_lint proper) with a provenance-consistency
check — when an atom's version increments, its `instantiated_at` must
differ from the prior instance's and its `author` must be consistent
with the change class (a decision-effect amendment authored by the
consul/owner, not by ont-060-reconciliation). Folded into STORY-0009's
lineage as a follow-on SPEC (worker cuts it), not blocking — but it
closes a gate through which provenance can currently lie.

## Standing state

Owner: merge #18 (third signature; meters honest). Then **STORY-0002
opens** — and it now opens alongside two small chartered stories
(revocation runtime, human evidence) that it does not depend on but that
the C1 gate eventually needs. The spawn contract remains the mainline
and the one that matters: the supervised, story-scoped, chain-attributed
session in a citizen container. Parallel and non-blocking as ever:
senate licensing + URL fixes; DEC-0002 on the AGPL counsel pass.
