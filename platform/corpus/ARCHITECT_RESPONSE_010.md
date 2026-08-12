# ARCHITECT RESPONSE 010 — demotion ruled; the tree-gap closed; a mechanism commended

PR #22 accepted in shape: three charters cut D27-correct (refs filled
from real issues, verified resolving), the SPEC-0056 problem laid out
rather than quietly chosen, the untracked work order caught and
committed. Three dispositions and one commendation.

## D42 — COMMENDATION, not a correction: the self-failing posture is the right pattern

SPEC-0120's posture that *cannot outlive its own condition* — CTRL-0002
asserting chainverify exposes no revocation surface, so implementing
revocation forces the posture's supersession — is exactly how every
interim posture in this system should have been built from the start. A
posture that "promises to be revisited" relies on human vigilance; a
posture whose enabling condition is itself a checked claim fails
structurally the moment it becomes false. This is mechanism-over-
discipline applied to the honesty of the corpus's own hedges. Ruling:
this is the **standard pattern for interim postures going forward** —
every posture atom SHOULD name a checkable condition whose falsification
forces its supersession, not a prose promise. Recorded as a principle
(worker cuts PRIN- or folds into the interim-posture guidance). The
revocation-runtime story (STORY-0011) inherits the good outcome: its
first act will *fail* CTRL-0002, which is the signal that the posture
must retire — the story cannot pretend to be done while the posture
still stands.

## D43 — RULING: SPEC-0056 stays active; the missing demotion edge is deliberate

The worker is right that D38's "held at ratified" was unimplementable —
SPEC-0056 is active, bound by an active rule, and active → ratified is a
backwards edge ONT-060 does not define, the mirror of the gap DEC-0004
fixed forward. The worker's recommendation is adopted: **leave SPEC-0056
active; the missing demotion edge is deliberate, not an omission to
amend.**

Reasoning, so it is not re-litigated: activation is caused by
binding-completeness (D34) — SPEC-0056 *is* bound by an active rule, so
it *is* active; that is the truth. What is model-attested is not the
claim's activation but its *evidence quality* — CTRL-0002 tests a
fixture model, not runtime behavior. That distinction belongs in the
evidence, not the lifecycle: the claim is active and correctly so; its
latest evidence carries the model-attested qualifier and SPEC-0120's
self-failing posture records the gap. Demoting an active, rule-bound
claim to express "its evidence is provisional" would overload lifecycle
state with an evidence-quality concern — two facts on one field, the
error D36 just finished separating for the meters. The lifecycle table's
omission of active → ratified is therefore correct: there is no honest
trigger for it. D38 is amended to match reality: *ENT-051's claim
remains active; its model-attested evidence quality is carried by the
evidence row and the self-failing posture, retiring when STORY-0011's
runtime suite supersedes it.*

## D44 — RULING: close the canonical-tree gap now — it has bitten twice

Two occurrences is the pattern speaking (SPEC-0091's canonical-tree
clause has no enforcing control; a governed document outside
platform/corpus is invisible to the gate unless it collides on an id).
The worker correctly diagnosed *why* nothing complained: a prose-only
document changes no atom digest, so the corpus looks identical. This is
a live instance of the doc-truth defect the whole system exists to
prevent — a rule (SPEC-0091) with no binding control is exactly the
"dangling claim" the meters are built to surface, except this one
dangles in the *tree-shape* dimension the current controls don't scan.

Ruling: **CTRL-0001 gains a repository-tree check** (folded into
STORY-0012's provenance-consistency scope, since that story is already
opening atom_lint for the author/timestamp check — one PR, related
gates): every `*.md` file in the repository is classified as either
(a) inside platform/corpus/** (governed — parsed and validated), (b) an
enumerated root allowlist (CLAUDE.md, README.md, LICENSE), or (c) a
violation. A governed-looking document — one carrying atom markers OR
matching the DOC-/DEC-/ARCHITECT_RESPONSE- naming family — found outside
platform/corpus/** fails the gate. Correspondence included: architect
responses are governed content and belong under
platform/corpus/correspondence/ (STORY-0005's shelf), so the check also
ends the "response sat untracked at root" class by making root
placement a failure, not a habit.

Note this subsumes a standing question: architect responses have been
landing at repo root by delivery convention this whole time. Post-D44
they land in the corpus tree like everything else, and the gap that let
one sit untracked-and-invisible closes in the same stroke.

## D45 — The gh-issue-create silent failure: MEM-0004's family, third confirmed sibling

`gh issue create` rejecting `--jq`, the `|| true` swallowing it, empty
issue numbers reported as success — the same failure-path-looks-like-
quiet-success class as the watcher (MEM-0004) and the vacuous lint
(SPEC-0092). Caught by listing the issues rather than trusting the
command, which is the discipline working. Endorsed as an extension of
MEM-0004 rather than a new memory: its generalization is now *a command
whose failure path is indistinguishable from an empty success must be
verified against the world it claims to have changed, not its own exit
status* — watcher, lint, and issue-create are three faces of one rule.
Worker updates MEM-0004 (grooming, per ONT-049a — supersession, new
instance).

## Standing state

Owner: merge #22 (charters plus the demotion resolution recorded). Then
**STORY-0002 is the mainline with nothing in front of it** — the spawn
contract, on active law, three companion stories chartered beside it and
gating nothing. STORY-0012 grows the D44 tree-check and the D41
provenance check together. Parallel as ever: senate licensing + URL
fixes; DEC-0002 on the AGPL counsel pass. The next report worth waiting
for is the first one that describes a container coming up rather than a
ceremony going through.
