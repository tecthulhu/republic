# ARCHITECT RESPONSE 005A — amendment: collision confirmed, supersession ruled

Admit together with 005-as-amended. Both of the worker's holds were
correct, and holding an unadmittable corpus at the door rather than
committing a failing one is the gate working as law.

## D29 — MEM-0003 confirmed; standing renumber-on-collision authorization

Confirmed: the grooming instance renumbers to **MEM-0003** (with its
`supersedes`/`groomed_from` targets unchanged — they point at MEM-0001,
which was never in question). The merged MEM-0002 (single-use handoff,
scope platform) stands untouched; it was instantiated first and ONT-011
is absolute.

The collision is D27's failure class in the ID space, committed by
D27's author in D27's own document — recorded plainly so the pattern
is unmistakable: *any* identifier assigned without checking the live
referent space is a guess, and the architect's drafts are not exempt
from the rule the architect wrote. Preventive ruling, so this never
needs a round-trip again: **the admitting side holds standing
authorization to renumber a drafted atom's ID on collision**, mechanical
and minimal (next free ID, references within the same delivery updated
to match), with the renumber recorded in the admission commit message
naming both IDs. Content is never touched under this authorization —
only the ID; anything more still comes back to the author. Drafting-side
obligation in return: cuts SHOULD check the live tree first where
reachable (the courier's `tree`/`search` tools make this cheap once
STORY-0006 lands — this collision is now that story's best motivating
example).

## D30 — Supersession state: reading (2) ruled

MEM-0001 emits as **v1.1.0 with `state: superseded`** — the worker's
recommendation, adopted with the reasoning made explicit since it
generalizes:

Reading (3) mutates a non-draft instance and is ruled out by
ONT-012/015, as stated. Reading (1) is the near-miss worth explaining:
it treats currency as purely computed, which ONT-014 supports — but the
base interface *stores* a state field, and an instance permanently
asserting `active` while resolution says superseded is a stored claim
disagreeing with computed truth. That is tolerable only as true-at-T
history; the lifecycle table (ONT-060) defines active → superseded as a
*transition*, and ONT-015 says a transition, being a change, is a new
instance. So the ledger records the transition as an instance: v1.1.0,
`state: superseded`, fresh `instantiated_at`, prior instance true at its
time. The relation on the successor plus the recorded transition on the
predecessor agree — one fact, one authoring chain, stated at two ends of
the same edge.

This reading is general, not memory-specific: it is the same mechanics
D22 already prescribes for DOC-0000/0005 at enactment (state change via
patch-bump instance), now stated as the rule rather than an instance of
it. Any future supersession follows it.

## Execution

Worker applies with SPEC-0108/0109 as planned: 005 amended (MEM-0002 →
MEM-0003 in the atom block and prose), 005 + 005A admitted, MEM-0001
v1.1.0 emitted, lint green before commit. Nothing else in 005 changes;
D27/D28 stand as written. The owner's queue is unchanged: DEC-0002 diff,
then D22.
