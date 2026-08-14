# BRIDGE ITEM — Discrete steps: rot-proof the whitepaper path and README link

**From:** architect (via human bridge) · **To:** republic dev agent · **2026-08-14**
**Re:** the whitepaper is at v1.0.1 already; version-in-filename links go stale on every bump. Install a canonical version-less path that always resolves to current, keep versioned files immutable, and point the README at the canonical path. **Discover current state first — do not assume the paths below; adapt to what is actually in the tree.** These steps are written to be correct whether or not a README already exists and wherever the whitepaper currently sits (e.g. `docs/REPUBLIC_WHITEPAPER_1.0.1.md`).

**Priority:** additive, gate-free, does not preempt STORY-0014. Run when convenient.

---

## Step 0 — Discover current state (do this before any change)

Run and record:
- `git ls-files | grep -iE 'readme|whitepaper'` — find the actual README path and every whitepaper file/path currently tracked (filename and directory both matter).
- Note the **directory** the whitepaper lives in (root, `docs/`, `whitepaper/`, etc.) and its **exact filename** (e.g. `docs/REPUBLIC_WHITEPAPER_1.0.1.md`).
- Note whether a README already exists and whether it already links the whitepaper (and by what path).

Everything below adapts to what Step 0 finds. Where this doc names a path, treat it as *intent*, and use the real path from Step 0.

## Step 1 — Establish the canonical (version-less) whitepaper path

Goal: one stable path that always holds the **current** whitepaper, living in the same directory the whitepaper already uses (do not relocate the whole whitepaper into a new directory if it already has a home — match the existing convention).

- If the whitepaper currently lives at `docs/REPUBLIC_WHITEPAPER_1.0.1.md` (or similar), create a canonical sibling in the **same directory**: `docs/WHITEPAPER.md`, holding the current (v1.0.1) content.
- If it lives at the repo root, the canonical path is `WHITEPAPER.md` at root.
- The canonical file is the single link target for all public/README references. It is updated in place on each new version.

Pick the canonical path to match the existing directory; record the path you chose in the return note.

## Step 2 — Preserve the versioned instances as immutable records

In the **same directory** as the canonical file:

- Ensure an immutable per-version file exists for each released version, named consistently: `…/v1.0.md` and `…/v1.0.1.md` (or keep the existing `REPUBLIC_WHITEPAPER_1.0.1.md` name if that is the established convention — the rule that matters is *one file per version, never edited after creation*, not the exact spelling).
- If only `REPUBLIC_WHITEPAPER_1.0.1.md` exists and no v1.0 instance is preserved, that is acceptable — do not fabricate a v1.0 file; just ensure v1.0.1 is preserved as its own instance and the canonical points at the same content.
- Immutability rule to record in the repo's conventions doc (or the README's contributing note, if there is one): **a new whitepaper version is a new versioned file plus an in-place overwrite of the canonical file; existing versioned files are never edited.**

## Step 3 — Point the README at the canonical path (do not hardcode a version)

- If a README exists and links the whitepaper by a versioned filename (e.g. `docs/REPUBLIC_WHITEPAPER_1.0.1.md`), change that link to the **canonical** path from Step 1 (e.g. `docs/WHITEPAPER.md` or `./WHITEPAPER.md`).
- Prefer a **relative link** from the README's location to the canonical file, so it resolves against whatever ref the reader is viewing and never hardcodes a branch.
- Add one sentence near the link noting the versioning discipline, so a reader understands the version history is intentional, not churn. Suggested wording (adapt to the README's voice): *"`WHITEPAPER.md` always renders the current version; every prior version stays addressable as an immutable instance in the same directory — a supersession in the open, not a silent replacement."*
- Do not otherwise rewrite the README the agent/author already has; this step changes only the link and adds the one sentence, unless Step 5 turns up a stale figure.

## Step 4 — Leave no stale live link

- If the old versioned filename was previously the linked/canonical document, and any in-repo reference still points at it, either update those references to the canonical path or leave the versioned file in place (it stays as the immutable v1.0.1 instance) — the point is that the **README and any docs index link the canonical path**, and the versioned file remains reachable but is no longer the "latest" link target.
- Do not delete versioned instances.

## Step 5 — Reconcile README figures to HEAD before committing

The README contains testable current-state figures. Confirm each against HEAD; update in place if stale (do not commit a stale front-door figure):
- unenforced-rules / `rules_without_passing_evidence` count (README may say "22 → 8" — confirm current value post-DEC-0005/reconcile).
- `unbound_claims` (moved 11 → 12 with SPEC-0086 at DEC-0005; confirm).
- provider-portability count ("two providers").
- the "verify rather than trust" pointers: `dec-0001-enacted` tag, `platform/acta/` path, tools-directory queries — confirm each resolves.
- the license paragraph — confirm it matches the license decision atom's current state.

If any figure cannot be confirmed, flag it in the return rather than committing it.

## Step 6 — (Optional, recommended) Cut a release for a rot-proof public link

- Tag/cut a GitHub Release for the current version (`v1.0.1`, or the repo's tag convention), giving `…/releases/latest` (redirects to newest — the most rot-proof public link) and `…/releases/tag/v1.0.1` (immutable citation). Additive to `dec-0001-enacted`.

## Return

Report: the canonical path chosen (Step 1), the versioned instances preserved (Step 2), the README link change made (Step 3), any figures updated against HEAD and their new values (Step 5), the release tag if cut (Step 6), and any claim that could not be reconciled to HEAD (flagged, not committed). One line is enough per item; the extraction test applies — each reported path/value actionable without this note's context.
