---
id: DOC-0000
type: document
title: Ontology Specification
scope: platform
state: active
version: 1.1.0
instantiated_at: "2026-08-12T20:00:00Z"
author: agent-worker-dec-0004
authorized_by: DEC-0004
relations:
  - { rel: contains, target: "ONT-*" }
---

# Document 0 — Ontology Specification

This document defines the governed artifact type system for the platform: the
base interface every governed atom implements, the atom types and their deltas,
the relation vocabulary, and the single lifecycle state machine. Every other
normative document in the launch set is written *in* this ontology; its claims
are atoms, its enforceability is a property of rule bindings defined here.

This document is self-hosting: the type definitions below are themselves
governed atoms, expressed in the format they define. The frontmatter block at
the head of this file is an instance of the base interface in §2.

Requirement IDs in this document use the `ONT-` prefix. Atom type IDs use the
prefixes assigned in §4.

---

## 1. Definitions and scope model

**ONT-001** — A **governed atom** is the smallest unit of normative or intent
content that carries identity, lifecycle state, authorship, and authorization
independently of any file it is serialized in.

**ONT-002** — Documents, charters, standards, and directives are **not atom
types**. They are serialization containers: files that carry one or more atoms.
A file's genre carries no governance semantics. Governance attaches to atom
IDs, never to filenames or genres.

**ONT-003** — The **scope hierarchy** is `platform → project → repo`:

| Scope | Definition |
|---|---|
| `platform` | Zero or more related projects governed as one system. |
| `project` | An individually identifiable service composed of zero or more containers. |
| `repo` | An individual code repository. |

Scopes are addresses, not types. Every atom carries exactly one `scope` value.
An atom at a broader scope applies to all narrower scopes beneath it unless a
narrower-scope atom of the same type explicitly supersedes it, which requires a
ratifying decision (§6).

**ONT-004** — In the default citizen topology, `repo`, agent, and `project` are
one-to-one-to-one. The hierarchy exists for the exceptions (multi-repo
projects, platform-wide law) and for federation later; it must not be used to
create intermediate governance layers that have no owning artifact.

**ONT-005** — This document governs **artifacts**: governed atoms and their
lifecycle. Runtime actors — identity-bearing entities, their chain positions,
their citizenship classes, and the interfaces at which they touch one another —
are governed by the companion **Entity Interface Ontology** (Document 0.5,
`ENT-` requirement prefix). The two documents are peers at the substrate
layer: Document 0.5 references this document downward for every contract
binding (its interface contracts are `SPEC-` atoms, its conformance is `RULE-`
bindings, its attestations are `EVID-` records); this document does not depend
on Document 0.5. Entity types are not atom types and MUST NOT be added to §4.

---

## 2. The base atom interface

**ONT-010** — Every atom, without exception, implements the following fields.
Serialization is YAML frontmatter in a markdown file (dual-audience: prose body
for humans, frontmatter for machines).

```yaml
id:            # REQUIRED. Stable ID: <TYPE-PREFIX>-<NNNN>. Never reused, never renumbered.
type:          # REQUIRED. One of the atom types in §4.
scope:         # REQUIRED. platform | project:<name> | repo:<org/name>
state:         # REQUIRED. Lifecycle state per §6.
version:       # REQUIRED. Semver (MAJOR.MINOR.PATCH). Prior versions immutable.
               #   Ruled by DEC-0001: semver from the start for rule/control
               #   inheritance and traceability at higher scales.
instantiated_at: # REQUIRED. Timestamp of this instance's creation. An atom
               #   instance is identified by (id, version, instantiated_at);
               #   see the truth model, ONT-014–016.
author:        # REQUIRED. Identity-chain reference of the authoring leaf
               #   (human or agent — same identity type, per the Identity Spec).
authorized_by: # Decision atom ID that ratified this atom.
               #   MUST be null only in state draft or proposed.
relations:     # List of typed links per §5. May be empty.
tags:          # Optional. Extensible human/machine reference labels
               #   (e.g. acceptance-criterion, interim-posture). Tags carry
               #   no governance semantics; gates never branch on tags.
title:         # REQUIRED. Human-readable one-line name.
```

**ONT-011** — ID prefixes are assigned per type in §4. The registry of assigned
prefixes is itself governed content in this document; adding a type requires a
new version of this document via the decision process.

**ONT-012** — Atom versions are immutable once the atom leaves `draft`. A
change to a non-draft atom produces a new version; the prior version remains
addressable. Supersession is expressed via the `supersedes` relation, never by
mutation.

**ONT-013** — `author` and `authorized_by` are the provenance anchors. Both
reference the same identity/decision machinery for human and agent actors.
No atom type may add an alternative authorship or approval field.

### 2.1 The truth model

**ONT-014** — **Truth is temporal.** A statement written without a time
reference transitions from "truth" to merely "true or false" the moment it
is written, because the world it described may have changed. A
time-specified statement is durable: it is *true at timestamp T*
permanently. Every atom instance is therefore a time-specified statement:
its `instantiated_at` fixes when it was true, and the instance never
mutates. The current state of anything is a resolution query over
instances, never a mutable record.

**ONT-015** — **Mutation is a new instance.** Changing an atom produces a
new instance at a new (version, instantiated_at); the prior instance
remains addressable and true-at-its-time forever. The atom store is
append-only in instance space. Nothing edits in place past `draft`.

**ONT-016** — **Reference semantics.** References identify, never locate:

- A reference is `{ id }` (resolve to latest valid instance at retrieval
  time) or `{ id, version }` / `{ id, version, instantiated_at }` (pin an
  instance). A reference by file path, URL, line number, or any storage
  location is a fragile coupling and is prohibited in atom content.
- A **source of truth is an unbroken reference chain** from the querying
  context to authoritative instances. Durability of the chain, not
  prominence of a copy, is what makes truth authoritative.
- **Two independent sources of truth for the same fact constitute a source
  of falsehood.** Every fact has exactly one authoring chain; every other
  appearance is a resolved reference or a generated (descriptive-class)
  rendering. This is why reverse relation links are **computed, never
  materialized** (ruled by DEC-0001): a stored inverse is a second,
  independently-mutable statement of the same fact. Forward links are
  written once at the owning atom; all inverse lookups are index queries.

**ONT-017** — **Documents are assemblies.** A source file carries atom
instances (§7). A *document*, as read, is an assembly of resolved atoms at
a given time: retrieval resolves each reference per ONT-016 and therefore
always presents the latest valid instances — or, when pinned, a faithful
historical assembly. Rendered documents are descriptive-class: generated
from resolution, never a second authored copy.

---

## 3. Facet interfaces

**ONT-020** — Consumers of atoms bind to **facets**, never to the full
ontology. A facet is a narrow interface a subset of atom types implements.
No platform component may require knowledge of atom types outside the facets
it consumes.

| Facet | Implemented by | Consumed by |
|---|---|---|
| `injectable` | principle, strategy, mandate, story (context payload), memory (via context profiles) | Spawner / harness |
| `checkable` | specification (incl. story-scoped), restriction, control | Gates (spawn, merge, CI) |
| `enforceable` | rule (via its enforcement) | Gates |
| `schedulable` | story, sprint | Tracker adapter (Quaestor role) |
| `recordable` | evidence, decision, provenance-link, memory | Provenance stream (Acta role) |
| `grantable` | mandate, waiver | Identity minting, gates |

**ONT-021** — Facet membership is fixed per type in §4. A component that finds
itself needing a type outside its facets is evidence of a layering violation,
not grounds for widening the facet.

---

## 4. Atom types

Types are grouped as **normative** (cause behavior), **intent** (direct work),
and **record** (produced by the system). Each entry defines: prefix, delta
fields beyond the base interface, facets, and binding semantics.

### 4.1 Normative atoms

#### Principle — `PRIN-`

Advisory, prompt-shaping guidance. Honest about being untestable.

```yaml
binding: injected        # FIXED. Principles are never gated.
```

- Facets: `injectable`.
- **ONT-030** — A principle MUST NOT be referenced by a rule. If a principle
  becomes testable, it is superseded by a specification; it does not mutate.

#### Specification — `SPEC-`

A positive, testable claim about the system.

```yaml
binding: checked         # FIXED.
check: machine | human   # How the claim is verified.
```

- Facets: `checkable`.
- **ONT-031** — A specification in state `active` that is not referenced by at
  least one active rule is a **dangling claim**. Dangling claims are reportable
  by query (§8) and block launch-readiness.

#### Restriction — `RSTR-`

A negative claim: something that must not occur.

```yaml
binding: checked         # FIXED.
phase: pre+post          # FIXED. Checked before and after execution, in a tight loop.
injection: never         # FIXED. Restrictions are never placed in prompts.
check: machine | human
```

- Facets: `checkable`.
- **ONT-032** — The `injection: never` and `phase: pre+post` values are fixed
  by the type schema and cannot be overridden per-instance. Rationale: negative
  instructions in prompts prime the prohibited behavior (the "don't think of an
  elephant" failure). Prohibition lives in gates, not context. The schema makes
  the misconfiguration inexpressible rather than discouraged.

#### Control — `CTRL-`

An executable predicate over a codebase, artifact, or running system.

```yaml
target: codebase | artifact | runtime
implementation:          # Reference to the checker (script path, suite name, gate ID).
inputs:                  # What the control examines (paths, subjects, digests).
```

- Facets: `checkable`.
- **ONT-033** — A control's `implementation` reference MUST resolve to an
  invocable checker in CI or a gate. A control whose implementation does not
  resolve cannot enter state `active`.

#### Enforcement — `ENF-`

The consequence binding: what a pass or fail triggers.

```yaml
on_fail: block-merge | refuse-spawn | suspend-escalate | advisory
on_pass:                 # Optional. Usually proceed; may emit evidence only.
escalation_target:       # REQUIRED when on_fail is suspend-escalate.
conditions:              # Optional. Exception-grammar clauses (§5.5) selecting
                         #   among the above by rule-evaluation context.
```

- Facets: none directly (consumed via rule).
- **ONT-034** — Permitted `on_fail` values form the enforcement ladder.
  `suspend-escalate` suspends and routes to the human veto gate; no enforcement
  value terminates an actor. There is no `kill` value in the schema.

#### Rule — `RULE-`

**ONT-035** — A rule is not a fifth kind of claim. A rule is the **binding
triple**: one claim (specification or restriction), one control, one
enforcement.

```yaml
claim:        # SPEC- or RSTR- reference. REQUIRED.
control:      # CTRL- reference. REQUIRED.
enforcement:  # ENF- reference. REQUIRED.
```

- Facets: `enforceable`.
- **ONT-036** — An unbound claim is a proposal. A claim becomes enforceable at
  the moment an active rule binds it. Enforceability is therefore a computable
  property: *does an active rule reference this claim*. This is the
  traceability requirement of the launch set made queryable.
- **ONT-037** — Changing a consequence changes the enforcement atom, not the
  claim. Changing a checker changes the control, not the claim. Single
  responsibility applies per atom.

#### Decision — `DEC-`

A ratified choice. The only atom type whose effect is to change the lifecycle
state of other atoms.

```yaml
question:                # What was decided.
outcome:                 # The ruling.
effects:                 # List of { target: <atom-id>, transition: <state> }.
process_ref:             # Reference to the proposal/vote/ratification record
                         #   (Senate bill, or repo-scope decision record).
```

- Facets: `recordable`.
- **ONT-038** — No atom transitions past `proposed` without a decision
  referencing it in `effects`. Decisions themselves are ratified through the
  governance process appropriate to their scope (platform: Senate lifecycle;
  repo: repo-scope decision process using the same record shape).

#### Mandate — `MAND-`

The per-citizen authority grant: identity ceiling, model band, repo binding.

```yaml
citizen:                 # repo:<org/name> reference.
imperium:                # Caveat ceiling — maximum capabilities grantable to
                         #   this citizen's identity leaves.
model_band:              # Band label (e.g. B0–B3). Never a model literal.
role_layer:              # Which L1 layer this citizen builds FROM.
```

- Facets: `injectable`, `grantable`.
- **ONT-039** — `model_band` MUST be a band label resolved at spawn/render
  time. A model literal in a mandate fails schema validation.
- **ONT-040** — A citizen's identity leaves may never carry a capability
  absent from its mandate's `imperium`. Authority is granted and attenuated,
  never inferred or escalated.

### 4.2 Intent atoms

#### Strategy — `STRAT-`

The intent arc: what the outcome should be over a horizon, at the integration
level. Semi-permanent, one per scope.

```yaml
horizon:                 # The arc's span (e.g. a quarter, a release).
outcomes:                # What true-at-end-of-arc looks like. Prose, testable
                         #   where possible via referenced SPEC- atoms.
constraints:             # Standing constraints; may reference PRIN-/RSTR- atoms.
```

- Facets: `injectable`.
- **ONT-041** — Each citizen's strategy is hash-pinned in its mandate context
  and injected at spawn. Strategy changes only through the decision process;
  drive-by edits fail the atom-lint control because version and
  `authorized_by` will not reconcile.

#### Sprint — `SPRINT-`

A grouping of stories composing a section of an arc, terminated by a gate.

```yaml
arc_ref:                 # STRAT- reference this sprint advances.
stories:                 # STORY- references composing the sprint.
gate:                    # CTRL- reference: the exit check. REQUIRED.
```

- Facets: `schedulable`.
- **ONT-042** — A sprint's exit gate is a **convergence point**: a horizontal
  integration check across the sprint's outputs, run against real running
  components, not mocks. A sprint without a gate is schema-invalid. This
  imports horizontal-convergence-before-vertical-decomposition into ordinary
  sprint mechanics: the gate is the mandatory horizontal slice.

#### Story — `STORY-`

The unit of work.

```yaml
acceptance:              # List of SPEC- references at this story's scope.
                         #   MUST contain at least one.
sprint_ref:              # Optional SPRINT- reference.
tracker_ref:             # External tracker ID (source of truth for status).
```

- Facets: `injectable` (as work context), `schedulable`.
- **ONT-043** — A story with an empty `acceptance` list is schema-invalid and
  therefore unschedulable. This is enforced by validation, not review.
- **ONT-044** — Story *status* lives in the external tracker (`tracker_ref`).
  The platform reflects tracker state and never owns backlog state. There is
  no backlog atom: a backlog is the query *stories at scope X in open states*.

#### Acceptance criteria — story-scoped specifications

**ONT-045** — Ruled by DEC-0001: acceptance criteria are **not a distinct
atom type**. An acceptance criterion is a `SPEC-` atom whose scope is a
story, carrying the tag `acceptance-criterion` and a `story_ref` delta
field. It receives identical gate treatment to any specification through the
`checkable` facet, and its lifetime tracks its story. At-a-glance human
reference is served by the tag and by generated renderings, not by a
separate type: a field specification suffices where a type is not
structurally distinct. Tags carry no governance semantics (ONT-010); gates
key on scope and facet, never on the tag.

### 4.3 Record atoms

#### Evidence — `EVID-`

The record produced when a control is executed.

```yaml
control_ref:             # CTRL- that ran.
subject:                 # What was checked: artifact digest, repo ref @ commit,
                         #   or runtime target.
verdict: pass | fail
checked_at:              # Timestamp.
checker:                 # Identity-chain reference of the executing leaf.
detail_ref:              # Optional pointer to full output in the object store.
```

- Facets: `recordable`.
- **ONT-046** — Evidence atoms are append-only and never versioned; each run
  produces a new atom. "Is claim X currently true" is the query *latest
  evidence for the rule binding X, verdict pass, against the current subject
  digest*. A claim without current evidence is an aspiration, reportable by
  query (§8).

#### Waiver — `WVR-`

A governed exception to a rule.

```yaml
rule_ref:                # RULE- being waived.
waived_scope:            # Scope the waiver applies to (narrower than the rule's).
expires:                 # REQUIRED. Timestamp. No indefinite waivers.
condition:               # Exception-grammar clause (§5.5); canonical form:
                         #   given rule_ref, when scope matches waived_scope
                         #   and now < expires, then suspend, for waived_scope.
```

- Facets: `grantable`.
- **ONT-047** — A waiver without an expiry is schema-invalid. On expiry the
  gate re-arms automatically; renewing a waiver is a new atom requiring a new
  decision. Ungoverned bypass is thereby replaced with governed, provenanced,
  self-expiring deviation.

#### Blocker — `BLK-`

A raised impediment with escalation binding.

```yaml
raised_by:               # Identity-chain reference.
blocks_refs:             # Atom or citizen references impeded. Named _refs, not
                         #   `blocks`, because the bare token names the relation
                         #   in §5: the relation states that something is
                         #   impeded, this field lists what. One token, one
                         #   meaning.
escalation:              # ENF- reference or escalation target.
resolved_by:             # DEC- or EVID- reference once resolved.
```

- Facets: `recordable`.

#### Memory — `MEM-`

An agent-authored recall unit: the durable form of working knowledge that
outlives a context window. Born `active` without ratification (like
evidence); groomable (unlike evidence) — see ONT-049a.

```yaml
context_class: core | relevant | nuance | reference-cue
keywords:                # 1–5 short recall codes for keyed retrieval.
source_refs:             # Atom/instance references grounding the memory.
                         #   A memory contradicting its resolved sources is
                         #   defective by definition (ONT-049c).
groomed_from:            # Optional. Prior MEM- instance this supersedes.
```

- Facets: `injectable` (via context profiles), `recordable`.
- **ONT-049a** — **Grooming is supersession, never edit.** The grooming
  engine (semantic maintenance over the memory population) emits new
  instances that supersede prior ones via `groomed_from` and the
  `supersedes` relation. Memory history is walkable; a bad grooming pass is
  revertible. Instances remain immutable per ONT-015.
- **ONT-049b** — **Retrieval weight is a measurement stream, never a stored
  field.** A retrieval count or weight on a memory atom would be a mutable
  counter on an immutable instance (ONT-014/015) — prohibited. Each
  retrieval writes an index measurement row
  `(memory_id, version, retriever, task_ref, turn, value_mark,
  retrieved_at)`, and weight is a standing query over the stream
  (frequency, retriever-valued marks, recency decay, per-retriever
  discounting). The event stream is the same descriptive-class machinery as
  embeddings (§8.5): generated, append-only, provenanced.
- **ONT-049c** — **Resolution wins.** When an agent's in-context memory of
  a fact conflicts with the resolved current instance of a cited atom, the
  resolved instance is ground truth. Citations are by instance identity
  `(id, version, instantiated_at)` per ONT-016, so cited facts are durably
  true-at-T and supersession is always visible to the citing agent.

#### Provenance Link — `PROV-`

The relation record binding a directive chain end to end. This is the row type
of the provenance stream.

```yaml
directive:               # Verbatim human input reference (stream offset or hash).
decision_ref:            # DEC- if the directive produced a ruling.
story_ref:               # STORY- executed under the directive.
actor:                   # Identity-chain leaf that executed.
artifacts:               # Output references: commits, object-store digests, PRs.
```

- Facets: `recordable`.
- **ONT-048** — Every provenance field is a reference, never a copy, except
  `directive`, which anchors the verbatim human input. The chain
  human directive → decision → story → identity → artifact must be walkable
  from any element to all others.

---

## 5. Relation vocabulary

**ONT-050** — Relations are typed, directed links in the `relations` list.
The permitted vocabulary:

| Relation | From → To | Meaning |
|---|---|---|
| `binds` | rule → claim/control/enforcement | Composition of the binding triple. |
| `satisfies` | evidence → claim | This run verified that claim (incl. story-scoped SPEC-s). |
| `supersedes` | any → same type | Replacement; target moves to `superseded`. |
| `blocks` | blocker → any | Impediment. |
| `advances` | story/sprint → strategy | Work serves this arc. |
| `grants` | decision → mandate/waiver | Authority conferral. |
| `contains` | document → atom | Serialization only; no governance semantics. |
| `derives` | any → any | Traceability without stronger semantics. |

**ONT-051** — New relation types require a new version of this document via
the decision process. Components MUST ignore relation types they do not
consume (open/closed: tolerant reader, closed writer).

---

## 5.5 The exception grammar

**ONT-055** — Rule-layer conditions — governed exceptions to rules and
conditional enforcement selection — are expressed in the **exception
grammar**:

```
exception := GIVEN <source: RULE- | ENF- ref>
             WHEN  <trigger: fact expression>
             MEETS <condition: predicate over trigger>
             THEN  <result: suspend | select <ENF- ref> | modify <field: value>>
             FOR   <scope: scope ref, narrower than or equal to source scope>
```

Fact expressions in `WHEN`/`MEETS` draw on rule-evaluation context (scope,
branch, time, subject artifact properties), not on credential chain facts.

**ONT-056** — The exception grammar is used by exactly two atom types:
**waivers** (`WVR-`), where the canonical form is *given RULE-X, when scope
matches the waived scope and now < expires, then suspend, for scope Z*; and
**conditional enforcements** (`ENF-`), where an enforcement's `on_fail` may
be selected by condition (e.g., *given this rule, when branch meets
protected, then block-merge; for feature scope, advisory*). No other atom
type may carry exception-grammar constructs.

**ONT-057** — **Layer separation** (mirror of ENT-095, Document 0.5 §9).
Exception-grammar constructs MUST NOT appear inside credentials, and
credential limiter caveats MUST NOT be used to express rule exceptions.
Rules may have exceptions; credentials may only have limiters. A `then`
result may suspend or select among pre-ratified enforcements; it may never
grant, widen, or mint authority — authority lives exclusively in the
credential layer.

**ONT-058** — Every exception instance is itself governed content: it exists
only inside a ratified `WVR-` or `ENF-` atom, carries that atom's provenance,
and is validated by atom-lint against the grammar (scope-narrowing checked,
referenced enforcements must be ratified, `suspend` results require an
expiry per ONT-047).

---

## 6. The lifecycle state machine

**ONT-060** — One state machine governs every atom type:

```
draft → proposed → ratified → active → deprecated
                 ↘ rejected              ↘ superseded
```

| Transition | Trigger |
|---|---|
| draft → proposed | Author submits. No decision required. |
| proposed → ratified | Decision atom with matching `effects` entry. |
| proposed → rejected | Decision atom. Terminal. |
| ratified → active | Binding complete: for claims, an active rule references it; for controls, `implementation` resolves; for others, ratification implies activation. |
| ratified → deprecated | Decision atom. The exit for an atom that was ratified but never activated and no longer needs to be — a story-scoped specification whose story has closed with evidence, for instance (ONT-045: its lifetime tracks its story). Without this edge such atoms sit in `ratified` forever, misreporting finished work as missing coverage. |
| active → deprecated | Decision atom. Gate consumers stop enforcing. |
| active → superseded | A `supersedes` relation from a ratified successor, authorized by decision. |

**ONT-061** — Only decision atoms move other atoms past `proposed`. Evidence
atoms and record atoms — including memories — are born `active` (they record
what happened or what was learned; there is nothing to ratify) and are
immutable as instances. Memory supersession via grooming (ONT-049a) requires
no decision; it is record-keeping, not governance change.

**ONT-062** — The ratification path is scope-dependent but shape-identical:
platform-scope decisions run the Senate lifecycle (bill → review → vote →
executive window → enact); repo-scope decisions use the same record shape with
the repo's decision process. One state machine, two ratifying authorities.

---

## 7. Serialization and validation

**ONT-070** — Atoms serialize as structured blocks within host files. Two
forms are legal:

- **Single-atom file**: YAML frontmatter at file head (the base fields),
  prose body following. Preferred for high-churn gate-consumed atoms purely
  to minimize ratification merge collisions.
- **Multi-atom file**: atoms delimited by the **atom encoding standard**
  (ONT-070a). Ruled by DEC-0001: multi-atom files are first-class and fully
  lintable; the boundary standard, not file cardinality, is what gates
  depend on.

**ONT-070a** — **The atom encoding standard.** Atom boundaries are explicit
markers that are functionally invisible in host document formats — legal
comments in the host syntax — so a governed file renders cleanly as an
ordinary document while remaining machine-parseable. Canonical marker pair,
with the atom's machine record as fenced YAML after the open marker and the
atom's prose body following it:

    <!-- atom:begin id=SPEC-0042 -->
    ```yaml
    { base fields and type delta }
    ```
    (prose body of the atom)
    <!-- atom:end id=SPEC-0042 -->

The HTML-comment form is canonical (invisible in rendered Markdown and HTML
alike); per-host equivalents (block comments in source files, etc.) may be
admitted by new versions of this document. Rules: markers are recognized only at column 0 — indented or quoted
markers are inert, which keeps examples and citations un-governed; markers
MUST pair and MUST NOT nest; `id` in begin and end MUST match; content outside any marker pair
is un-governed prose carrying no atom semantics; atom-lint parses by markers
and validates each block independently. A governed file is thereby literally
what ONT-017 defines: an assembly of atoms plus connective prose, in one
renderable document.

**ONT-071** — Each atom type has a JSON Schema. The schemas are governed
artifacts referenced by this document; schema changes are new versions of this
document via the decision process. The basis is self-hosting. Schema versions
follow semver per ONT-010.

**ONT-072** — A single control, `CTRL-0001 atom-lint`, validates every
governed file in CI: frontmatter parses, schema per type validates, fixed
fields carry their fixed values, IDs are unique and correctly prefixed,
references resolve, lifecycle transitions in history are legal, and
`authorized_by` is present for any state past `proposed`.

**ONT-073** — `RULE-0001` binds `SPEC-0001` ("every governed file validates
against its type schema") to `CTRL-0001` with `ENF-0001` (`on_fail:
block-merge`). This rule is the ontology enforcing itself and is the first
entry in the platform rule set.

---

## 8. Standing queries

**ONT-080** — The following are queries over the atom store, not documents.
They MUST be computable from atom frontmatter plus evidence records alone:

| Query | Definition | Use |
|---|---|---|
| Backlog | Stories at scope X in open tracker states | Planning surface. |
| Dangling claims | Active SPEC-/RSTR- with no active rule binding | **Drift guard.** Structurally zero at activation (see below); any nonzero reading is an incident, not a backlog. |
| Unbound claims | Ratified SPEC-/RSTR- that no active rule binds | **Coverage meter.** The claims awaiting a binding rule; the launch-readiness number. |
| Unevidenced claims | Active rules with no passing evidence against current subject digests | Doc-truth report. |
| Expired waivers | Waivers past `expires` | Gate re-arm audit. |
| Launch readiness | Unbound claims (in-scope) = 0 AND unevidenced claims (in-scope) = 0 AND embedding coverage gap = 0 AND C1 evidence passing AND dangling claims = 0 | Ship gate. |

**ONT-080a** — **Why two claim meters, not one.** Dangling claims and unbound
claims answer different questions, and conflating them makes one of them lie.
ONT-031 defines dangling over *active* claims, while ONT-060 activates a claim
only *when* a rule binds it: jointly, dangling claims reads zero at every
activation, by construction rather than by achievement. It therefore cannot
measure coverage, and it was never measuring it. What it does measure is drift —
a rule deprecated or deactivated out from under a still-active claim — which is a
real failure mode with no other detector, so it stays in the readiness gate as a
guard whose target is permanently zero.

Coverage is the *ratified but unbound* population: claims that have been ratified
and are waiting for a rule to make them enforceable (ONT-036). That is the number
the ship gate needs, and the one a reader means by "how much of the law is
actually wired up".

**ONT-081** — Launch readiness is therefore a countable property of the atom
store, not a review outcome.

---

## 8.5 Embedding-native instantiation

**ONT-085** — **Every persisted atom instance is embedded at persistence.**
Embedding generation is a non-optional side effect of the instance
persistence pipeline (the durable consumer of the data-access role), in the
same manner that evidence emission is a non-optional side effect of control
execution. No authoring step, no per-type opt-in, no separate indexing
process exists for an author to skip.

**ONT-086** — **Embeddings are descriptive-class derivations, never
authored content.** An embedding vector MUST NOT appear in atom frontmatter,
atom bodies, or any authored file. Rationale (ONT-016): an embedding is a
deterministic derivation of the instance text; storing it beside the text
creates a second, independently-mutable statement of the same fact — a
source of falsehood. Vectors live exclusively in the generated index, keyed
by instance identity.

**ONT-087** — **The atom is the chunk.** Embedding is computed per atom
instance, bounded by the encoding standard's markers (ONT-070a) — never per
file, never by arbitrary windowing. Semantic retrieval therefore returns
atom instances, and presenting results is ordinary document assembly under
ONT-017: retrieval-augmented assembly is the document model, not an added
integration.

**ONT-088** — **Embeddings are versioned measurements.** Each index row
carries full measurement provenance:

```
(atom_id, version, instantiated_at,
 embedding_model_band, embedding_model_digest, vector, embedded_at)
```

The embedding model is referenced by band label resolved at render/deploy
time and pinned by digest — model literals are prohibited in configuration,
extending ONT-039's law to embedding instruments. Because instances are
immutable (ONT-015), a vector is permanently valid *for its instance under
its model digest*: there is no staleness and no re-index-on-edit. A model
generation change supersedes rather than corrupts — prior rows remain
true-at-T under their digest; re-embedding produces new rows under the new
digest; queries evaluate within one model generation.

**ONT-089** — **Coverage is a standing query.** *Instances lacking a vector
under the current model generation* joins the §8 query family with target
zero, alongside dangling claims and unevidenced claims. Semantic coverage
is thereby countable, not promised. Semantic retrieval results are
proposals to structural machinery — injection candidates, decomposition
context, near-duplicate warnings at proposal time — and never directly
trigger enforcement: similarity proposes, gates dispose.

---

## 9. Bootstrap and open items

**ONT-090** — This document enters the lifecycle at `draft`. Its ratification
is the platform's first decision (`DEC-0001`), which simultaneously ratifies
the type schemas and `RULE-0001`. Until `DEC-0001`, nothing in this document
is enforceable; after it, everything in it is.

The slate formerly open here has been ruled and is recorded in DEC-0001,
whose ratification of this document activates the rulings: semver versioning
(ONT-010), acceptance criteria as story-scoped SPEC- atoms with tags
(ONT-045), the atom encoding standard for multi-atom files (ONT-070a), and
computed relation inverses under the truth model (ONT-016). The credential
carrier ruling (hybrid transport/act-authority split) is recorded in
DEC-0001 against Document 0.5 §9 / ENT-097.
