# ARCHITECT RESPONSE 007 — activation attribution ruled; road to DEC-0003

PR #16 acknowledged as green with all three suites and the first live
`--since` gate. The four fixture-caught defects are noted with
appreciation — every one of them (the version clobber, the demotion
edge, the wrong-repo ref resolution, the fixture inheriting the
assumption it tests) is the class that only surfaces when something
adversarial runs, which is why the fixtures were required. The CI
watcher self-correction is separately acknowledged below (D35).

Owner's note: the authorship declaration and ABG manager consent are
executed and filed; DEC-0002's ownership precondition is satisfied.

## D34 — RULING: ceremonies are scoped; reconciliation is its own act

The question posed two readings of ONT-060 — eligibility as a corpus
property (global sweep) versus ceremonies scoped to their effects. Both
are half right, and the tension dissolves once *cause* and *recording
act* are separated:

**Activation is never caused by a decision.** ONT-060's ratified →
active trigger is binding-completeness — a computed property of the
corpus. No decision's effects list contains "activate"; no signature
confers it. Therefore activation transitions must never ride a
decision's signing commit — not because ceremonies are narrowly scoped
as a style preference, but because activation is not part of *any*
ceremony. A signature attests exactly its decision's effects; lifecycle
movements caused by the law operating are attributable to the law, and
recording them under someone's signature misattributes them. The
worker's licence-signature concern is the correct instinct: DEC-0002's
merge should never read as "the licence signature moved the ontology's
lifecycle."

**Reconciliation is the missing named operation.** Ruled mechanics:

1. `enact.py <decision> --apply` applies **only the decision's
   enumerated effects**. Scoped, always.
2. `enact.py --reconcile` is a distinct mode: computes ONT-060
   eligibility corpus-wide and stages ratified → active transitions for
   every eligible atom, attributed in the staged instances and the
   commit to the lifecycle law itself (author: the tool identity;
   authorization: ONT-060, citing the corpus digest at computation).
   Forward-only, per the defect-2 fix — demotion has no trigger in the
   table and reconciliation must never invent one. It requires no
   fresh decision, because DEC-0001's ratification of ONT-060 *is* its
   standing authorization; each run is the ratified law operating, on
   the record.
3. Reconciliation may run whenever — post-ceremony, scheduled, or
   on demand. An unreconciled corpus is legal but visible: the standing
   report's ratified-but-eligible line is the meter for it, target
   zero.

**DEC-0003 under this ruling** becomes one PR, two commits, two
attributions:

- Commit 1 — the owner's signature: DEC-0003 generated against the
  named digest, its enumerated effects applied (proposed → ratified
  across the D31 scope). This is the act the merge signs.
- Commit 2 — the machine's reconciliation: `--reconcile` output, moving
  the newly-ratified (and the three already-ratified substrate atoms)
  to active where binding-completeness holds, attributed to ONT-060.

The merge still wakes the meters in one review, and the ledger forever
shows who caused what: the human ratified; the law activated. SPEC-0112
is amended in intent accordingly (the worker re-versions it with the
two-commit shape; the acceptance meaning — meters live post-merge — is
unchanged).

This also future-proofs the licence act: DEC-0002's eventual ceremony
touches DEC-0002 alone, and if any atom happens to become eligible that
week, a reconciliation pass — separately attributed — picks it up.

## D35 — Watcher lesson endorsed for memory

The empty-run-ID watcher that exited 0 on usage text and was read as
"watching" is the same defect family as the vacuous lint pass
(SPEC-0092): a monitor whose null case reports success. The
self-correction was proper doc-truth practice — the claim was retracted
the moment it was found resting on nothing. Endorsed as a MEM- atom
(context_class: relevant; keywords: watcher, exit-zero, verify-target):
*a background watcher must verify its watched resource exists before
trusting exit status; usage-text-and-exit-0 is not observation.* If a
gh-CLI wrapper for CI watching gets built later, its null case fails
closed by the same rule.

## Standing state

Owner's queue: review/merge PR #16; then the DEC-0003 PR arrives as the
two-commit ceremony and its merge is the second signature. Parallel,
non-blocking: licence the senate pair and fix senate's stale
kescott027 URLs when convenient; DEC-0002 waits on the AGPL counsel
pass only. After DEC-0003: meters live, STORY-0008's SPEC-0108/0109
close if not already, and STORY-0002 — the spawn contract — opens on
active law.
