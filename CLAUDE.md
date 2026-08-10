# CLAUDE.md — worker bootstrap

You are a build worker on this platform. This file is a bootloader, not the
law: the law is the governed corpus in `corpus/`. Read this, then load the
core set, then work the loop. If anything here conflicts with a resolved
corpus atom, the resolved atom wins (ONT-049c: resolution wins).

## Load order (core context — re-assert after any context compaction)

1. `corpus/DOC-0000_ontology.md` — the atom system. Skim §2 (base fields,
   truth model), §4 (types), §6 (lifecycle), §7 (encoding standard).
2. `corpus/DOC-0002_platform_architecture.md` — what you are building.
3. The document for your current story: STORY-0001 → `corpus/DOC-0003_l0_base_contract.md`;
   STORY-0002 → DOC-0003 + `corpus/DOC-0004_envelope_subject_spec.md`.
4. `corpus/SPAWN_CONTRACT_STORIES.md` — your acceptance criteria, verbatim.

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
   before any commit that touches `corpus/` — a red lint is a stop.
4. When an acceptance check can run, run it and capture output. Evidence
   rows land in `index/` (generated — never hand-edit, never commit).
5. Commit with the story ID in the message trailer: `Story: STORY-000X`.
6. If blocked, record the blocker plainly and stop; do not route around a
   gate, do not weaken a check to pass it, do not mark anything done that
   has not run green.

## Repository facts

- `corpus/` — governed atoms and documents. Source of truth. Lintable.
- `schemas/atoms-1.0.0.json` — atom schemas (DEC-0001 rulings encoded).
- `tools/` — atom_lint.py (CTRL-0001), test_grammar.py (CTRL-0002),
  embedder.py (ONT-085–089), extract.py (corpus generator — regenerating
  overwrites REQUIREMENTS_REGISTER/CONTROLS/ENFORCEMENT_RULES; do not run
  it casually).
- `index/` — generated: evidence rows, embeddings, standing queries.
  Regenerable, git-ignored, never truth.
- Current build order: PA-030 in DOC-0002. Steps 1–3 done with evidence.
  You are on step 4 (STORY-0001) unless told otherwise.

## Interim honesty

This bootstrap file is hand-authored during the bootstrap phase and will be
superseded by a corpus-rendered version once the render pipeline exists.
Until then it is intentionally minimal: durable rules belong in the corpus,
and anything you are tempted to add here probably belongs there as an atom.
