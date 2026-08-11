# CLAUDE.md — worker bootstrap

You are a build worker on this platform. This file is a bootloader, not the
law: the law is the governed corpus in `platform/corpus/`. Read this, then
load the core set, then work the loop. If anything here conflicts with a
resolved corpus atom, the resolved atom wins (ONT-049c: resolution wins).

**The canonical tree is `platform/`.** It holds the only copy of every
governed document; the repo root carries this bootloader and nothing
governed. A document presented at a second path for reading convenience is
a copy, and a copy is never committed (D2 of ARCHITECT_RESPONSE_001: two
independent sources of truth for one fact are a source of falsehood,
ONT-016). Tool commands below run from `platform/`.

## Load order (core context — re-assert after any context compaction)

1. `platform/corpus/DOC-0000_ontology.md` — the atom system. Skim §2 (base
   fields, truth model), §4 (types), §6 (lifecycle), §7 (encoding standard).
2. `platform/corpus/DOC-0002_platform_architecture.md` — what you are building.
3. The document for your current story: STORY-0001 →
   `platform/corpus/DOC-0003_l0_base_contract.md`; STORY-0002 → DOC-0003 +
   `platform/corpus/DOC-0004_envelope_subject_spec.md`.
4. `platform/corpus/SPAWN_CONTRACT_STORIES.md` — your acceptance criteria,
   verbatim. Architect dispositions and later story cuts land as further
   files in `platform/corpus/`.

## Non-negotiables (these survive every context cycle)

- **No work without a story.** Every change traces to a STORY- atom. If no
  story covers what you're about to do, stop and say so; do not invent scope.
- **Doc-truth.** Never claim a capability, metric, or behavior you have not
  verified in this session. Reported behavior becomes an acceptance check,
  not an assumed fact. If a document and the code disagree, surface it —
  do not silently reconcile either direction.
- **Acceptance criteria are the definition of done.** SPEC- atoms scoped to
  your story, checked by running their checks. Green output pasted, not
  described.
- **Instances are immutable.** Never edit a non-draft atom in place; changes
  are new versions (ONT-012/015). Never renumber or reuse IDs.
- **No model literals** anywhere — band labels only (ONT-039). No location
  references in atom content — IDs only (ONT-016).
- **Restrictions are gates, not prompts.** Do not paste RSTR- content into
  generated prompts or configs; they are checked pre/post (ONT-032).
- **Cite by ID.** When you rely on a corpus fact, cite the atom ID. When
  unsure whether an atom is current, check for `supersedes` relations before
  relying on it.

## The loop

1. Confirm the active story and read its acceptance SPECs.
2. Plan against the referenced documents; list which L0-/ES-/BASE-AC-
   requirements the plan satisfies.
3. Build in small verified steps. Run `python3 tools/atom_lint.py corpus`
   from `platform/` before any commit that touches `platform/corpus/` — a
   red lint is a stop. Zero atoms parsed is a red lint, not a green one
   (SPEC-0092).
4. When an acceptance check can run, run it and capture output. Evidence
   rows land in `index/` (generated — never hand-edit, never commit).
5. Commit with the story ID in the message trailer: `Story: STORY-000X`.
6. If blocked, record the blocker plainly and stop; do not route around a
   gate, do not weaken a check to pass it, do not mark anything done that
   has not run green.

## Repository facts

All paths below are under `platform/`.

- `corpus/` — governed atoms and documents. Source of truth. Lintable.
- `schemas/atoms-1.0.0.json` — atom schemas (DEC-0001 rulings encoded).
- `tools/` — atom_lint.py (CTRL-0001), test_grammar.py (CTRL-0002),
  test_atom_lint.py (CTRL-0001's own fixture suite), embedder.py
  (ONT-085–089), extract.py (corpus generator — regenerating overwrites
  REQUIREMENTS_REGISTER/CONTROLS/ENFORCEMENT_RULES; do not run it casually).
- `tools/requirements.txt` — the dependency pin. Deps are a versioned
  measurement (SPEC-0086's pattern): a bump re-runs what it touches.
- `index/` — generated: evidence rows, embeddings, standing queries.
  Regenerable, git-ignored, never truth.
- Current build order: PA-030 in DOC-0002. **Evidence is environment-scoped**
  (ONT-014): a step is "done" only against a named environment and a subject
  digest, never in the abstract. Steps 1–2 (atom-lint, grammar suite) are
  re-verified in the worker environment; step 3 (embedder/index/standing
  queries) carries drafting-environment evidence and re-verifies per
  environment. Cite the digest when you claim a step.
- Active story: STORY-0003 (corpus integrity) precedes STORY-0001; STORY-0001
  (step 4, gold base) follows it unless told otherwise.

## Interim honesty

This bootstrap file is hand-authored during the bootstrap phase and will be
superseded by a corpus-rendered version once the render pipeline exists.
Until then it is intentionally minimal: durable rules belong in the corpus,
and anything you are tempted to add here probably belongs there as an atom.
