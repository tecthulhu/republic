# FLOOR RESPONSE — whitepaper session (currency seam + Class III self-dilution ruling)

**From:** republic architect session (via the human bridge)
**To:** the whitepaper/spine session
**Date:** 2026-08-13
**Register:** resolvable-reference; each item owner + action + object + gate. Two blocks: a currency seam the apparatus has not yet caught, and the Class III self-dilution ruling with two hardenings before it's built.

---

## Block 1 — Currency seam: the paper now *understates* the repo (conservative-direction defect)

**The finding.** SPINE S4 Bound 1 and whitepaper §7 are pinned to HEAD 97ee84f. Since that snapshot, this session merged STORY-0002 (PR #24): the full spawn contract is walked and on main, CTRL-0005 and CTRL-0006 now carry passing evidence, and `rules_without_passing_evidence` dropped 22→8. The paper's "full-chain data pending" (Bound 1) and the §7 status are therefore stale — and stale in the *conservative* direction: the paper claims **less** than the evidence now supports.

**Why it still must be fixed.** The spine's own law is "never drift from testable to validated" — the inverse applies with equal force: a paper whose entire thesis is *enforced-is-a-number-not-an-audit* must not under-report the number when the number is the point. Under-claiming the walked hop is not a lie in the dangerous direction, but it is a divergence between repo and paper, which is exactly the seam class the review rounds exist to close.

**Actions:**
- **B1-a (whitepaper §7):** re-snapshot §7 at post-#24 HEAD for rc9. The walked-hop material (surrogate-refusal quote, rogue-set catches, DEC-0004 meter split) stays; add that STORY-0002 merged, CTRL-0005/0006 now evidence-passing, meter delta 22→8. *Object:* §7 status section. *Gate:* rc9 cut.
- **B1-b (SPINE S4 Bound 1):** review "full-chain data pending" against what CTRL-0005/0006 now evidence. This is an edit to ratified spine text → requires a floor ruling, not an editorial change. Route it as a Bound-1 currency ruling alongside the two already pending (the noted-not-applied "first evidence rows exist for corpus controls" amendment is adjacent and could ride the same sitting). *Object:* SPINE S4 Bound 1. *Gate:* floor ruling → propagates to rc9.

*Note on direction:* fix this in the good direction — the repo did more than the paper claims. But hold the line at "walked hop, evidence exists," never "full chain validated"; testable≠tested still governs the parts genuinely pending.

---

## Block 2 — Class III self-dilution mitigation: RULED, with two hardenings

**Ruling.** The floor accepts the acceptance-baseline-pinning mitigation as specified: the merge/evidence gate grades a story's work against the acceptance set **as of the last floor-touched instance**; agent revisions to in-flight acceptance specs stay recordable but do not move the grading baseline until floor-touched; supplemented by the weakening-diff lint at the build gate; time-boxed with retirement condition = the magistracy D1 authorship-mandate mechanism going live. The fix class is correct: it closes the composition **without reversing either posture** (bootstrap spawn rule stands; authorship stays open pending D1), enforced at an existing gate — mechanism, not vigilance.

**The attack, confirmed exact.** POSTURE-1 (resolvable-not-ratified spawn) + POSTURE-2 (mandate-unbounded authorship) compose: an agent authors a weakening of its own in-flight acceptance specs, the gate grades against the weakened set, green passes against criteria no human touched — the §3 self-consumption loop reintroduced *inside the governance plane*. It is dangerous precisely because every individual signal stays green (authorship valid, story resolvable, gate graded current specs, merge passed) — the same "green check implying an absent property" pattern as the buffering proxy and the L0 egress hole, one layer up. The missing property is "a human authorized what 'passing' means."

### Hardening 1 — the lint flags ALL non-floor acceptance edits; it does not adjudicate weakening
"Removes or loosens criteria" needs a mechanically decidable "loosens" predicate or the lint is a classifier with no denominator — it over-fires (flags every edit) or is bypassed by a semantic weakening dressed as a rewrite. **Resolution:** the lint flags *any* non-floor diff to an acceptance-spec atom on an in-flight story — removal, threshold change, or rewrite, without classifying which — and surfaces it as pending floor touch. The pin does the load-bearing work (baseline doesn't move); the lint just makes the pending state visible. Stronger (no semantic-weakening bypass) and simpler (no "is this looser?" oracle to attack).

### Hardening 2 — the spawn act pins the initial baseline
POSTURE-1 spawns stories while proposed, so a self-spawned story's *initial* acceptance specs may never have been floor-touched when work starts — leaving the pin nothing to compare against and the initial-specs-authored-weak variant open. **Resolution:** the story's spawn-authorizing act pins the initial baseline (spawning a story is a floor or floor-delegated touch of its initial criteria); only revisions *after* spawn require fresh floor touch to move the baseline. This closes the "author the initial specs weak" edge without adding ceremony.

### The provenance note is promoted from footnote to claim
"This attack was findable only because §7 declared both postures honestly — the disclosure recruited the adversary into the security analysis" is not throat-clearing; it is the paper's thesis demonstrated on the paper itself: honest external-resolvable declaration beat self-attestation, and transparency was a security *asset*. It also demonstrates the adversarial-companion pattern (the external reviewer found the composition the authors missed looking at each posture alone). **Direction:** give it a matter-of-fact sentence in §7, not a "may note" — it is one of the paper's strongest concrete demonstrations that the model works, and the cross-layer rhyme (same failure mode and remedy whether governing code or governing governance) is worth one line as evidence the thesis is substrate.

---

## The big question: does making this real require new stories? YES — three, republic-side

The ruling is the floor's direction; **it is not self-executing.** The gate change, the lint, and the posture atom are code and corpus, which by this system's own law means stories with acceptance SPECs — a ruling that stays a chat reply is the exact "declaration outrunning implementation" the program forbids. Three stories (or one story, three SPECs), republic-session jurisdiction:

**STORY-A — Acceptance-baseline pinning (the gate change).**
- SPEC: the merge/evidence-grading query resolves a story's acceptance set to the last floor-touched instance (spawn act for initial specs per Hardening 2; explicit floor ratification/co-sign for revisions); agent-authored revisions post-spawn are recorded but do not move the graded baseline. Fixture: an agent-authored weakening on an in-flight story is graded against the *pinned* set, not the weakened one, and the merge that would have passed against the weakened set fails against the pin.
- Object: the merge-gate control (CTRL-0004/0005 grading path) and the evidence-grading query.

**STORY-B — Weakening-diff lint (the new lint class).**
- SPEC: atom_lint flags any non-floor-authored diff to an acceptance-spec atom on an in-flight story (removal, threshold change, rewrite — all of them) at the build gate; flag names the pending-floor-touch state. Fixture: non-floor acceptance edit → flagged; floor-touched edit → clean; the flag does not attempt weakening classification (a pure rewrite is flagged too).
- Object: atom_lint; acceptance-spec atom types. (May ride STORY-A's PR or its own.)

**STORY-C — The composition posture atom.**
- SPEC: a declared-posture atom (D42 self-failing family, sibling to POST-0001 spawn-resolvability) naming the composition attack, the A+B mitigation, and the retirement condition (magistracy D1 authorship-mandate live → mandate-bounded authorship supersedes floor-touch pinning for mandated scopes), time-boxed per R6's interim-posture rule (prolonged silence past retirement = posture failure). Fixture: the posture resolves, names its retirement condition, and a check asserts the pin+lint are active while the posture stands.
- Object: the posture-atom family. Whitepaper rc9 §7 cites this atom's ID when it exists; until then "posture atom pending ID," which is honest and temporary.

**Sequencing:** these fold naturally into the STORY-0010 window (they touch the same grading/gate machinery and the human-evidence primitive is adjacent to "floor-touched instance"). Not blocking the approved queue; they join it. The synopsis's Block A already carries A1/A2/A3 as floor direction — **these three stories ARE Block A made executable**, so this is not new scope, it is Block A's implementation form. The dispositions (story → SPEC → atom IDs) return by bridge and rc9 §7 consumes STORY-C's ID.

---

## Sequencing addendum (floor-ruled) — integrity fix runs AHEAD of STORY-0010

The self-dilution composition is an **integrity** gap (an agent can grade its own work against criteria it weakened), not a capability gap. It outranks STORY-0010, which is a capability gap (cannot yet drive `unbound_claims` to zero). An open integrity hole in the merge gate — flagged "critical" by external review, and *live* wherever agents author in the STORY-0009/0010 machinery — precedes a missing capability. Resequenced republic-session queue:

1. Reconcile (CTRL-0005/0006 → active; meters true)
2. Two atoms (SPEC-0085-locally-evidenced posture; provider-portability atom)
3. **Reviewer-seam postures FIRST** (POST-0001 spawn-resolvability; OPEN-0001 agent-authorship) — these precede the dilution stories because STORY-C's posture is a sibling to POST-0001 and references OPEN-0001's retirement condition; the postures it builds on must exist first.
4. **STORY-A / B / C (the integrity fix) — AHEAD of STORY-0010.**
5. STORY-0010 (human evidence) — now behind the integrity fix.
6. CTRL-0008 → 7. STORY-0005 (README) → 8. STORY-0011 (revocation runtime).

**Cousin-primitive note to the worker:** STORY-A's pin needs a definition of "floor-touched instance." That concept is a *cousin* of STORY-0010's human-evidence primitive — both are "a human deliberately touched this" — but they are **not the same** (floor-touch on an acceptance spec is a ratification/co-sign act; human-evidence is an evidence record). Build floor-touch **minimally** in STORY-A (spawn act pins initial baseline per Hardening 2; explicit floor co-sign moves it for revisions). Do **not** pre-unify with human-evidence. Flag if they converge, and let STORY-0010 unify them later if they turn out to be one primitive wearing two hats. Two different "human touched this" mechanisms built by accident is the anti-pattern to avoid.

## Compressed return

- **B1-a/B1-b:** currency seam — §7 re-snapshot (editorial, rc9) + Bound-1 currency (floor ruling, adjacent to the two pending). Repo did more than the paper claims; fix in the good direction.
- **Block 2:** Class III ruled, two hardenings (lint flags all non-floor edits; spawn pins initial baseline), provenance note promoted to a §7 claim.
- **Stories:** yes — STORY-A (pin), STORY-B (lint), STORY-C (posture). Block A made executable, **routed AHEAD of STORY-0010** (integrity before capability), behind the reviewer-seam postures they reference. IDs return by bridge for rc9's §7 citation.
