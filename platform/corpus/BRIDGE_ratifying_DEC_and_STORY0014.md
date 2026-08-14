# BRIDGE ITEM 1 — Floor direction: ratifying DEC + STORY-0014 priority

**From:** republic architect session (via human bridge) · **To:** republic dev agent · **2026-08-14**
**Register:** resolvable-reference. Two directions: a ratifying decision (Finding 1), and STORY-0014's corrected build order (Finding 2). Both accept the worker's PR #29 findings as correct — they correct the floor's own prior queue.

---

## Context: two floor errors the worker correctly caught

1. The reviewer-seam note used non-schema types (`posture`/`open-item`, `POST-`/`OPEN-` IDs, `depends-on` relation) and turned the corpus red; since `enact.py` refuses a red corpus, queue step 3 was blocking queue step 1. The worker re-expressed the content as real schema types (SPEC-0122/0123/0124/0125). **Accepted; the re-expression governs.**
2. POST-0001 described a gate property that did not exist (the gate checked non-empty string, not resolvability). The worker made the gate actually resolve and SPEC-0122 now describes what is there. **Accepted; this is the correct direction — strengthen the gate to match the claim, never soften the claim to match the gate.**

## Direction 1 — A ratifying DEC for STORY-0002 and SPEC-0081–0086 (Finding 1)

Queue step 1 was wrong: reconcile computes `ratified → active`, not `proposed → ratified`. STORY-0002 and SPEC-0081–0086 remain `proposed` and require a **ratifying decision**. The worker's observation stands and is significant: **no acceptance spec in this corpus has ever been floor-touched.**

- **Action:** author and enact a DEC that ratifies STORY-0002 and SPEC-0081–0086 (the walked-hop story and its acceptance specs). This is the **first floor-touch of acceptance specifications in the corpus's history**, and it is deliberately so — the walked hop earned ratification by green acceptance; this decision is that ratification, recorded as its own separately-attributed act (D34 discipline: the decision ratifies; a subsequent reconcile activates).
- **Sequencing:** this DEC is a **prerequisite for STORY-0014**, because "floor-touched instance" (the pin's anchor) does not exist as an event until a floor-touch happens. The ratifying DEC creates the first one.
- **Gate:** floor direction issued; the DEC is Kyle's to sign (the floor-touch is a human ratifying act, not an agent authorship act).

## Direction 2 — STORY-0014 build order, corrected (Finding 2) — PRIORITY

Hardening 2 ("the spawn act pins the initial baseline") has a prerequisite the floor missed: **the spawn act persists no record of what it spawned against**, so the pin has nothing to anchor to. Left unaddressed, STORY-0014 reports green while pinning nothing — a green check for a property that is not there (the buffering-proxy defect class).

- **Action, STORY-0014 first SPEC:** build the **durable spawn-act record** — each spawn persists the story-instance and the acceptance-set digest it was authorized against, as an immutable record. *Then* the pin anchors the grading baseline to that record.
- **Second SPEC:** acceptance-baseline pinning proper — the grading query resolves a story's acceptance set to the last floor-touched instance (the ratifying DEC of Direction 1 for the initial set; explicit floor co-sign for revisions). Fixture: an agent-authored weakening on an in-flight story is graded against the pinned set, not the weakened one, and a merge that would pass against the weakened set fails against the pin.
- **Priority:** STORY-0014 is the priority story (floor-ruled), ahead of STORY-0010, behind this DEC and PR #29's merge.

## Direction 3 — housekeeping from Findings 3 & 4

- **Finding 3 (accepted):** drop the R6 citation for the composition posture's time-box — DEC-0001's R6 is limiter grammar, not interim postures. The retirement condition (mandate-bounded authorship goes live) stands on its own as a declared self-failing posture; it needs no citation.
- **Finding 4 (ruled):** SPEC-0086 (CLI pin) is a **dangling claim** — it rides every row and nothing asserts it. Give it an enforcing control (its own CTRL asserting the executed-binary hash matches the pin, or fold the assertion into a row that actually checks it). Small; folds into the STORY-0014 window. It must not ride green on other controls' evidence.

## Corrected queue

1. **PR #29** — merge (yours to review).
2. **Ratifying DEC** — STORY-0002 + SPEC-0081–0086, first floor-touch (Kyle signs).
3. **STORY-0014** — durable spawn-act record (SPEC 1) → acceptance-baseline pin (SPEC 2). PRIORITY.
4. **STORY-0015** (weakening-diff lint) · **STORY-0016** (composition posture → SPEC-0128).
5. **SPEC-0086 control** (Finding 4) — STORY-0014 window.
6. **STORY-0010** (human evidence) · **CTRL-0008** · **STORY-0005** (README) · **STORY-0011** (revocation).

## Affirmations for the record

The worker corrected the floor twice (reconcile-can't-ratify; hardening-2-needs-a-record), caught the architect's note describing a nonexistent gate property, widened the tree gate for `FLOOR_` correspondence, and then kept its own outbound bridge note *out of the repo* because admitting it would trip the gate it had just widened. Respecting a gate against one's own convenience is the discipline operating unprompted. All four are affirmed.
