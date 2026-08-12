# ARCHITECT RESPONSE 008 — meters ruled; DEC-0004 chartered; merge #17 as-is

The ceremony is accepted as run: two commits, two attributions, 194
ratified by the signature, 167 activated by the law, nothing in the
signature claiming activation. The version convention fired correctly on
first real use (0.1.0 generation → 1.0.0 at ratification). The third
MEM-0004 occurrence (a merge mid-flight leaving no PR trigger to wait
on) is acknowledged with its fix — bounded waits that report rather
than hang; the memory's generalization is now: *verify the target
exists, is the right target, and can ever exist.*

**Owner guidance first: PR #17 merges as-is.** Nothing below changes a
byte of it. The meter finding concerns the *interpretation layer* —
PA-022 (a draft document) and ONT-080's readiness definition — not the
ceremony's content. Sign it.

## D36 — RULING: two meters, two jobs; the done-test re-aimed

The worker's analysis is confirmed: ONT-031 (dangling = *active* claim
with no active rule) and ONT-060 (a claim only activates *when* a rule
binds it) jointly guarantee `dangling_claims` reads zero at every
activation. That is not a defect in either law — it is an emergent
property that reassigns the query's job:

- **`dangling_claims` is the drift detector.** It fires in exactly one
  scenario: a rule later deprecated or deactivated out from under a
  still-active claim. Target zero always; any nonzero reading is an
  incident, not a backlog. It stays in the readiness gate as a guard.
- **`unbound_claims` is the coverage meter** — the held-at-ratified
  line, formalized: claims in state ratified held on ONT-031 grounds
  (no active rule binds them). This is the number D22 and D31 expected
  dangling to be, and it is the number PA-022's done-test must cite.
  Today it reads 27.

The 27 decomposes tellingly, and the decomposition drives the rest of
the ruling: **11** are the human-check claims — honest, known homework
awaiting a human-evidence process; **16** are the acceptance specs of
*closed* stories. Those 16 are not coverage gaps at all — they are
completed lives. ONT-045 says a story-scoped spec's lifetime tracks its
story; their stories closed with evidence; holding them forever in
`ratified` misreports finished work as missing coverage.

## D37 — DEC-0004 chartered: the amendment decision

A small decision, generated and applied through the ceremony tooling —
its second exercise, this time on the document-amendment path:

1. **Amend ONT-080** (DOC-0000, new version via decision): add
   `unbound_claims` to the standing-query table with the definition
   above; redefine launch readiness as *unbound_claims (in-scope) = 0
   AND rules_without_passing_evidence (in-scope) = 0 AND coverage gap =
   0 AND C1 evidence passing AND dangling_claims = 0 (drift guard)*.
2. **Amend ONT-060's table**: permit `ratified → deprecated` by
   decision. The current table omits it, and completed story-scoped
   specs need exactly that exit; the transition is decision-driven like
   every other, so the amendment is one row.
3. **Effects**: deprecate the 16 closed-story acceptance specs,
   enumerated by the generator against the tracker (closed-ness read
   from the tracker, per the DEC-0003 precedent — never a list kept
   beside it).
4. **PA-022** is edited directly in DOC-0002 — it is draft; the fix is
   free — to cite `unbound_claims` and the revised readiness
   definition.

Post-DEC-0004 the coverage meter reads an honest **11** (human-check
claims), the three ONT-033-held controls remain visible until their
suites exist (CTRL-0005/0006 arrive with STORY-0002's build; CTRL-0008
with the index suite), and every number on the standing report means
exactly one thing.

Sequencing: DEC-0004 follows the #17 merge and does not block
STORY-0002 — the spawn contract may open in parallel, since nothing in
it consumes the readiness definition until its sprint gate.

## Standing state

Owner: merge #17 (the second signature — meters live on merge), then
DEC-0004 arrives as a small ceremony PR (third signature, trivially
reviewable: one document amendment, one table row, 16 deprecations).
Parallel: senate licensing + URL fixes; DEC-0002 on the AGPL counsel
pass. Then: **STORY-0002 opens on active law** — CTRL-0005 and
CTRL-0006's suites are its deliverables, so the risky hop is also what
shrinks the held-controls line from three toward zero.
