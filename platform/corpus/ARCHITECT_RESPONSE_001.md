# ARCHITECT RESPONSE 001 — dispositions for bootstrap report 2026-08-10

Reply to the first worker bootstrap report. Findings acknowledged in full;
the report is the intended behavior of the bootloader's doc-truth rule.
Dispositions D1–D8 below. D7 and D8 are reserved for the platform owner's
signature and are marked as such; everything else is actionable now.

Two atoms are cut at the end of this file: STORY-0003 (corpus integrity —
authorizes the fixes in D2/D3/D4) and its acceptance SPECs. Lint this file
into the corpus before acting on it.

---

## D1 — "Step 3 achieved" claim: amended, environment-scoped

The claim in DOC-0002 PA-030 and CLAUDE.md was true in the drafting
environment and stated without its environment — an untimed truth that
decayed exactly per ONT-014. Disposition:

- Amend both files (under STORY-0003): "steps 1–3 evidenced in the drafting
  environment against corpus@a1084129; re-verification required per
  environment." Evidence claims in prose MUST carry subject digest and
  environment from now on.
- Add `tools/requirements.txt` pinning `jsonschema`, `pyyaml`,
  `scikit-learn`, `numpy` (exact versions from the drafting environment are
  in the zip's tool imports; pin whatever resolves on your box and record
  it — the pin is the measurement, per SPEC-0086's pattern).
- Then run embedder locally; its evidence supersedes nothing, it adds a row
  for your environment.

## D2 — Duplicate documents at root: platform/ is canonical

Ruling (pending owner ratification with D7, but safe to stage): the
canonical tree is `platform/`. Root-level copies of DOC-0000/0002/0003/
0004/0005, DEC-0001, SPAWN_CONTRACT_STORIES, ONTOLOGY/ENTITY_ONTOLOGY/
LIVENESS_EXTENSION are delivery artifacts from the drafting session and
are deleted, not merged — where root copies diverged, the platform/corpus
copy wins unconditionally (the root DOC-0005 that fails lint is stale, not
alternative). Root keeps only: CLAUDE.md, .gitignore, README if desired.
Cause noted for the record: the drafting session presented documents at
two paths and both were committed — the delivery mechanism manufactured a
second source of truth. Standing rule going forward: one canonical tree;
anything presented for reading convenience is a copy that never gets
committed.

Executed under STORY-0003 / SPEC-0091.

## D3 — CTRL-0001 vacuous pass: fail closed on empty input

Confirmed defect, the serious one. A control that can emit passing
evidence having checked nothing inverts its purpose. Fix (STORY-0003 /
SPEC-0092):

- atom_lint accepts files and directories; a file argument parses that
  file, not zero.
- If total atoms parsed == 0, exit non-zero and emit a FAIL evidence row
  with reason `empty-input` — a checker's null case is a failure, the
  ENT-094 fail-closed law applied to controls.
- Evidence subject line includes the parsed-atom count, so a vacuous run
  can never masquerade in the evidence stream even if the exit code is
  swallowed.

## D4 — CLAUDE.md path drift: corrected

Bootloader paths updated (STORY-0003 / SPEC-0091) to `platform/…`, or —
preferable if the owner agrees — CLAUDE.md moves inside `platform/` and
the repo root becomes the platform root on the next clone. Worker's
call which is less disruptive to the working tree; record which in the
commit.

## D5 — Cross-story acceptance dependency: SPEC-0072 amended

Correct catch: BASE-AC-9 and BASE-AC-17 are harness-tested and the
harness is STORY-0002. Amendment (new versions; all affected atoms are
`proposed`, so this is pre-ratification correction, ONT-012 respected):

- SPEC-0072 v1.1.0 narrows to BASE-AC-15 and BASE-AC-16 (image-level
  negatives, runnable in STORY-0001).
- BASE-AC-9 and BASE-AC-17 move to STORY-0002's acceptance via SPEC-0081
  v1.1.0 (they are spawn-gate refusals — that is where they always
  belonged) and are additionally named in SPRINT-0001's gate description,
  so the convergence point still runs the full seventeen.

## D6 — Missing infrastructure: in-scope, not blocking

- No bus: run `nats:2.10-alpine` (digest-pin it) via docker for
  BASE-AC-10..13 — the bus is adopted infrastructure and a local container
  is its legitimate dev form (PA-013).
- No CI: `.github/workflows/conformance.yml` is part of SPEC-0073's
  deliverable — build it in STORY-0001, it was always implied by "runs in
  CI gated on merge."
- resolve/recall: adopt L0 open item (c) as recommended — NOT_AVAILABLE
  stub, BASE-AC-14 recorded as a declared interim posture atom (WVR- or
  tagged posture SPEC) rather than silence. SPEC-0071 already permits
  this.
- cosign/syft absent: not needed for STORY-0001's ACs; digest pinning via
  docker manifest is sufficient at this step.

## D7 — OWNER SIGNATURE REQUIRED: upstream base ruling (L0 open item a)

Architect recommendation: **Wolfi** — glibc compatibility (the CLI
runtime in STORY-0002 will want it), apk available in the build stage
while the final stage stays shell-less and package-manager-less per
L0-001, strong CVE response cadence, trivial non-root. Distroless remains
acceptable; either way the deliverable is a digest pin recorded in the
build file. One-line ruling; blocks the first line of the base build
file.

## D8 — OWNER SIGNATURE REQUIRED: proceed-under-proposed, or enact now

The worker is right that per ONT-090 nothing is enforceable until
DEC-0001 lands. Two legitimate paths:

- (a) Proceed under bootstrap posture: all evidence rows carry
  `posture: pre-ratification` until enactment. Legal, already implied.
- (b) **Recommended: enact now.** Per ENT-079 the signed act is the
  commit: the owner commits DEC-0001 with `process_ref` set to that
  commit's hash and state moved to `ratified`→`active` effects applied
  (DOC-0000/0005 → ratified). One commit, the corpus becomes law, the
  bootstrap asterisk disappears from every subsequent evidence row.
  STORY-0003's corpus fixes should land *before* the enactment commit so
  the ratified corpus is the corrected one.

---

## Cut: STORY-0003 and acceptance

<!-- atom:begin id=STORY-0003 -->
```yaml
id: STORY-0003
type: story
scope: platform
state: proposed
version: 1.3.0
instantiated_at: "2026-08-11T14:50:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Corpus integrity: canonical tree, fail-closed lint, claim scoping"
tags: [corpus-integrity, pre-ratification]
tracker_ref: "gh:tecthulhu/republic#3"
acceptance: [SPEC-0091, SPEC-0092, SPEC-0093]
```
Fixes the three defects surfaced by bootstrap report 001 before the
corpus is ratified: duplicate sources of truth removed, the lint null
case fails closed, environment-scoped claims corrected. Enactment of
DEC-0001 waits on this story by design — the ratified corpus must be the
corrected one. That impediment is carried by BLK-0001; v1.0.0 of this
atom carried `rel: blocks` directly, which is outside ONT-050 (`blocks`
runs blocker → any). v1.0.0 remains addressable in history.
<!-- atom:end id=STORY-0003 -->

<!-- atom:begin id=SPEC-0091 -->
```yaml
id: SPEC-0091
type: specification
scope: story:story-0003
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-architect
authorized_by: DEC-0003
title: "One canonical tree: root duplicates removed, paths corrected"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0003
```
No governed document exists outside platform/corpus (or the relocated
canonical root per D4); linting the whole repository tree yields zero
duplicate-ID findings; CLAUDE.md load-order paths resolve as written.
<!-- atom:end id=SPEC-0091 -->

<!-- atom:begin id=SPEC-0092 -->
```yaml
id: SPEC-0092
type: specification
scope: story:story-0003
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-architect
authorized_by: DEC-0003
title: "atom-lint fails closed on empty input and file arguments parse"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0003
```
atom_lint given a file path parses that file; given input yielding zero
atoms it exits non-zero and emits a FAIL evidence row with reason
empty-input; the evidence subject carries the parsed-atom count. A test
fixture demonstrates the previously-vacuous invocation now failing.
<!-- atom:end id=SPEC-0092 -->

<!-- atom:begin id=SPEC-0093 -->
```yaml
id: SPEC-0093
type: specification
scope: story:story-0003
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-architect
authorized_by: DEC-0003
title: "Evidence claims in prose are environment-scoped; deps pinned"
tags: [acceptance-criterion]
binding: checked
check: human
story_ref: STORY-0003
```
DOC-0002 PA-030 and CLAUDE.md amended per D1; tools/requirements.txt
exists with pinned versions; embedder runs green in the worker
environment and its evidence row is present in index/ for that
environment.
<!-- atom:end id=SPEC-0093 -->
