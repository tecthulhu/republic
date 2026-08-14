# BRIDGE ITEM — Make branch-protection enforcement visible and load-bearing

**From:** architect (via human bridge) · **To:** republic dev agent · **2026-08-14**
**Origin:** OpenAI repository-grounded RC9 review, P0 finding. The whitepaper and README both claim **"a red suite blocks merge."** Branch protection *is* configured — but a reviewer inspecting only public surfaces cannot verify that the required status check is actually enforced on `main`. Detection (the CI job) is publicly walkable; enforcement (the repo rule that refuses merge on a red check) is not. That is the exact one-hop gap the paper warns against, sitting on the most load-bearing public claim.

**The goal is not to change branch protection — it already works. The goal is to make its enforcement state emit walkable evidence, so the claim rests on a resolvable artifact rather than on trust.**

**Priority:** high, but does not preempt STORY-0014 (acceptance-baseline pin) unless you judge otherwise — this is a public-credibility gap on a load-bearing claim, and closing it before wider circulation matters. Sequence at your discretion; it touches evidence emission, not the grading path.

---

## The distinction being closed (state it in the atom's rationale)

- **A CI job that detects a violation is a control.**
- **A repository rule that refuses merge when that control is red is enforcement.**
- Republic's binding-triple logic depends on keeping those separate — so the enforcement half must be evidenced as its own governed fact, not assumed from the presence of the control.

## Step 0 — Discover current state

- Confirm what branch protection / ruleset is actually configured on `main`: which status checks are **required**, whether the protection is a classic branch-protection rule or a repository ruleset, and the exact **CI context name(s)** of the required check(s) (e.g. `corpus-controls`, `citizenship-conformance`). Use `gh api` (e.g. `gh api repos/tecthulhu/republic/branches/main/protection` or the rulesets endpoint) to read the real state.
- Record: is the protection present, are the corpus-controls/citizenship-conformance checks required, is the required context name **stable** (matches what the workflow publishes), and is "require branches up to date"/"require status checks to pass" actually on.
- **If the discovered state does not match the claim** ("red suite blocks merge") — e.g. the check exists but is not marked *required* — **flag it and stop before writing any passing evidence.** An evidence object asserting enforcement that isn't configured is the exact false-green the paper exists to prevent. Report the gap; do not paper over it.

## Step 1 — Make the enforcement state a governed evidence object

Build a control that captures the branch-protection/ruleset state and writes it as a timestamped evidence record, on the same append-only surface as every other control:

- **Source of truth:** the GitHub API ruleset/branch-protection response for `main` — not a hand-written assertion. The evidence must be *derived from the live setting*, so it cannot drift from reality without the next capture catching it.
- **Load-bearing facts to assert** (each a checkable proposition, not prose):
  - `main` is protected / governed by a ruleset.
  - The required status checks include the corpus-controls and citizenship-conformance contexts **by their stable context names** (bind to the name, so a renamed/removed check is detected).
  - "Require status checks to pass before merging" is enabled.
  - (If applicable) the checks are required for everyone including admins, or — if admins can bypass — that bypass is itself recorded as a named fact rather than hidden, so the evidence states the true enforcement scope rather than an idealized one.
- **Write the result** as an evidence record under `platform/acta/` (or wherever the evidence tree lives), timestamped, with provenance (which API endpoint, when queried, against which repo/branch). This makes "is merge-enforcement actually configured" a **standing query with a resolvable answer**, exactly like "is this claim currently evidenced."
- **Bind it to a claim.** The whitepaper/README claim "a red suite blocks merge" should become a governed claim that this control evidences — so the claim is no longer unbound prose. If a SPEC/claim atom for merge-enforcement does not exist, author one and bind this control to it (the binding-triple: claim + control + enforcement). An unbound "red suite blocks merge" is a dangling claim; this closes it.

## Step 2 — Keep it honest (the guardrails that stop this being theater)

- **Capture from the live setting, never from a constant.** If the evidence is a hardcoded "yes, it's enforced," it is exactly the attestational theater the paper attacks. It must query the real API each run and assert against what comes back.
- **Bind to the stable CI context name**, so that if someone renames or removes the required check (weakening enforcement), the evidence goes red — the capture detects the weakening. This is the meta-control protection the reviewer asked for: the actor being graded cannot quietly remove the required-check binding without the evidence catching it.
- **State bypass truthfully.** If repository admins can merge past a red check (a common default), the evidence must say so — "enforced except admin bypass" is the honest claim, and hiding it would be the overclaim. Record the real enforcement scope.
- **Freshness matters.** A one-time capture goes stale the moment the setting changes. Prefer a scheduled re-capture (or capture-on-each-conformance-run) so the evidence reflects current state, with the timestamp making staleness visible.

## Step 3 — Update the public claim to match the evidence

Once the evidence object exists and passes against the real configuration:
- The README / whitepaper "verify rather than trust" surface should **point at this evidence** — so a reviewer can resolve "red suite blocks merge" to a walkable artifact instead of taking it on trust.
- If Step 0 revealed the enforcement is narrower than the claim (e.g. admin bypass), the claim text is tightened to match the evidence, not the reverse.

## What NOT to do

- Do **not** assert enforcement the discovered state doesn't support — flag the gap instead (Step 0).
- Do **not** hardcode the evidence — capture it live (Step 2).
- Do **not** hide admin-bypass or any narrowing of scope — state the true enforcement (Step 2).
- Do **not** leave "red suite blocks merge" as unbound prose — bind it to the control (Step 1).

## Return

Report: the discovered branch-protection state (required checks, context names, bypass scope), the evidence object created and where it writes, the claim atom it binds to, whether the public claim needed tightening to match the true enforcement scope, and — if the discovered state did not match "red suite blocks merge" — the gap, flagged rather than papered over. The extraction test applies: each reported fact resolvable without this note's context.
