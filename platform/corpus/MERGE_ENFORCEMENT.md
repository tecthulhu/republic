# Merge enforcement — the claim, and the control that evidences it

**STORY-0017.** Source: `BRIDGE_branch_protection_evidence.md`, from an external
repository-grounded review of the whitepaper (P0 finding).

## The distinction this closes

- **A CI job that detects a violation is a control.**
- **A repository rule that refuses the merge when that control is red is enforcement.**

Everywhere else in this corpus those are kept apart — that separation is what the
binding triple *is*. On the single most load-bearing public sentence this repository
prints, they had collapsed. The whitepaper and the README both say **"a red suite
blocks merge"**, and what a reader could walk was the workflow: the control half. The
rule making it binding was configured and correct, and nothing pointed at it, so
enforcement had to be taken on trust.

That is the one-hop gap the paper spends §3 warning about, sitting on the sentence a
sceptical reader tests first. The gap was never in the configuration. It was that the
enforcement half was not a governed fact.

## What the review's premise got wrong, in the useful direction

The finding assumed a reviewer inspecting public surfaces *cannot* verify enforcement.
They can: `GET /repos/{owner}/{repo}/rules/branches/main` answers **without a
credential**. Seven of the eight facts below are anonymously reproducible against this
repository by anyone, right now.

So this story is not "make enforcement walkable" — it already was. It is *point at the
walkable thing, and check it on every run*, which is a smaller job and a better one:
the evidence is reproducible by the reader rather than being one more artifact to
trust.

One fact is not anonymous. `bypass_actors` is returned only to a credential holding
`administration: read` — and that is a personal-access-token scope, **not** a
`GITHUB_TOKEN` workflow permission. The first attempt at this story named it in the
workflow's `permissions:` block, which fails validation before any job is created: no
run, no jobs, and the two required contexts simply never report. The pull request then
reads *"Expected — waiting for status to be reported"* forever.

That failure is worth recording rather than quietly fixing, because of its shape. An
invalid permission does not present as a red check. It presents as **no check**, and a
required context that never arrives blocks merges without ever saying why — the merge
gate stops existing and looks like it is still thinking about it. A control that fails
loudly is a control; one that fails by not appearing is a hole, and this repository's
whole argument is about the difference.

So the probe never assumes what it cannot see: the CI capture records the bypass scope
as unobserved and falls back to the newest authenticated capture committed to the
Acta (SPEC-0130).

## What the capture found

Recorded here because a claim's qualifications belong next to the claim:

| fact | state |
|---|---|
| ruleset on `main` | active, `~DEFAULT_BRANCH`, repository-scoped |
| required contexts | `corpus-controls`, `citizenship-conformance` |
| those contexts published by a job | both |
| direct push / force-push / deletion | all refused |
| bypass actors | **none — administrators included** |
| branches up to date before merge | **not required** |
| required approving reviews | 0 |

Two of those narrow the claim rather than supporting it, and are stated rather than
omitted. **Branches need not be up to date with the base**, so a green check can
describe a base the merge result never had — the suite passed on what the PR tested,
which is not always what lands. **No review is required**, so the merge is the owner's
act alone; that is consistent with PA-002 treating the merge as the signature, but it
means "blocks merge" means "blocks a merge nobody re-checked", not "blocks a merge
somebody approved".

Neither is a failure and neither is hidden. The first is a live candidate for
tightening; the second is the ratified model working as designed.

---

<!-- atom:begin id=SPEC-0130 -->
```yaml
id: SPEC-0130
type: specification
scope: platform
state: active
version: 1.3.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Merge enforcement is captured from the live setting, not asserted"
tags: [acceptance-criterion, enforcement, meta-control, public-claim]
binding: checked
check: machine
story_ref: STORY-0017
```
The claim "a red suite blocks merge" resolves to a timestamped evidence record derived
from the hosting platform's live branch-protection state, captured on every
conformance run and committed to the Acta like any other control's output.

The record asserts, each as a proposition and none as prose: the default branch is
governed by an active rule set; status checks are required before merging; the
conformance contexts are required **by name**, so dropping one is detected; every
required context is **published by a workflow job**, so a required check that can never
report is detected as well; direct push, force-push and deletion are refused; and no
actor may bypass the rule set. It further records, without failing on them, the
qualifications that narrow the claim — whether branches must be up to date before
merging, and how many approving reviews are required.

Three properties are load-bearing and each closes a way this could have been theater.
**Captured, never constant:** a hardcoded assertion of enforcement is the attestational
governance the whitepaper argues against, so every fact comes from the API each run.
**Bound to the context name:** the actor being graded cannot quietly remove the
required-check binding, because removing it turns this red. **Never assumes what it
cannot see:** an unobserved bypass scope is recorded as unobserved.

**The bypass scope is not observable from CI, and the claim says so.** `bypass_actors`
is returned only to a credential holding `administration: read`, which is a personal
access token scope and *not* a `GITHUB_TOKEN` workflow permission — naming it in a
workflow's `permissions:` block fails validation before any job is created. So the CI
capture records `bypass_observed: false` and falls back to the newest **authenticated
operator capture committed to the Acta**, requiring it to exist, to have been taken
with a credential, and to show no bypass actor. The unobserved run therefore still
asserts something real — *somebody with sight of it recorded none* — instead of
assuming emptiness or staying silent.

That fallback is weaker than a live read and the difference is time: it cannot notice
a bypass actor added since the last authenticated capture. The row records
`bypass_observed: false` and names the capture it relied on, so the weaker basis is
visible in the evidence rather than inferred. Closing the gap needs a stored
administration-scoped token, which is an owner's decision about credential exposure on
a public repository, not a worker's.

Fixtures demonstrate seventeen cases, including: the real configuration passing; a
claimed context absent from the rule set caught; a required context published by no
job caught; a bypass actor caught; the fallback recording `unobserved` rather than
`observed-empty`; a committed capture showing a bypass actor caught; an anonymous row
refused as an attestation of something anonymous runs cannot see; the newest committed
capture governing rather than the cleanest; and no committed capture at all failing.

v1.1.0 — v1.0.0 required the probe to *fail closed* on an unobservable bypass scope.
That was unimplementable in the environment it governs: the Actions token cannot hold
`administration: read` at all, so the criterion would have reddened the required check
on every future run and taken the merge gate down with it. This is not the tool being
softened to fit the claim — the claim asked for a capability the runner cannot have,
and the replacement is stricter about honesty (`bypass_observed: false` recorded, an
authenticated capture required on record) while being satisfiable.
<!-- atom:end id=SPEC-0130 -->

<!-- atom:begin id=RULE-0095 -->
```yaml
id: RULE-0095
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Bind SPEC-0130 via CTRL-0009"
tags: [binding, enforcement, meta-control]
claim: SPEC-0130
control: CTRL-0009
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0130 }
  - { rel: binds, target: CTRL-0009 }
  - { rel: binds, target: ENF-0001 }
```
ENF-0001 (block merge), with the circularity acknowledged rather than glossed: the
control that verifies merge enforcement is itself gated on merge enforcement. If the
required-check binding were removed, this control would go red on the pull request and
nothing would stop that pull request merging.

That is not a defect this story can engineer away — no check inside a gate can
guarantee the gate. What it can do is make the removal *loud*: the run goes red, the
evidence row records the weakened state, and the standing query answers differently
from that moment on. A reviewer reads the record rather than the intention.
<!-- atom:end id=RULE-0095 -->

<!-- atom:begin id=STORY-0017 -->
```yaml
id: STORY-0017
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T17:30:00Z"
author: agent-worker-story-0017
authorized_by: null
title: "Merge enforcement emits walkable evidence for the claim that rests on it"
tags: [enforcement, meta-control, public-claim, reviewer-seam]
tracker_ref: "gh:tecthulhu/republic#32"
acceptance: [SPEC-0130]
relations:
  - { rel: advances, target: SPRINT-0001 }
```
Sequenced ahead of STORY-0014 on the bridge's judgement and this worker's agreement:
it is a public-credibility gap on the claim a reader tests first, it touches evidence
emission rather than the grading path, and it is small. STORY-0014 is unaffected.
<!-- atom:end id=STORY-0017 -->
