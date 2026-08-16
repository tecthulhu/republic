# D1 Confirmation Markup — rc6 Assembled Sections

**Version 0.1 — 2026-08-12 — scope: sections new since the closed claim markup (Abstract, Introduction, §§1–2, §3 head, §4 lead, §5, §7, §8, §9-transplant, Close). Transplanted §4.1–4.6 bodies and §6 were adjudicated in the closed markup and are not re-opened. Promise-ledger audit: previously automated, all-pass.**

---

## Findings requiring fix (3)

**M1 — Universal negative meets real prior art (Introduction; §4.6 opportunity).** The Introduction claims the provenance chain "answers a question no current development system can." Supply-chain attestation frameworks (in-toto, SLSA, sigstore) *do* answer part of it — how an artifact was built, by what, attested how. Our claim is the *full* four-part question including decision and authority, which those frameworks do not carry — but the absolute phrasing hands a T1 reader an easy "what about SLSA?" objection. Fix: Introduction → "a question that goes unanswered in full by current systems"; and strengthen §4.6 with the distinguishing clause, which converts the vulnerability into positioning: supply-chain attestation records *how* an artifact was built; this chain joins the *why* — who decided, under what authority — to the how. **Class: BROAD-absolute → scoped + prior-art acknowledged.**

**M2 — Uniqueness claim on the RCT (§1).** "In the one randomized trial on experienced developers in their own repositories" — other RCTs on AI-assisted development exist (including enterprise Copilot trials our own evidence brief cites for positive task-level effects). The qualifier chain arguably scopes it to METR uniquely, but the uniqueness is doing no work and invites the check. Fix: "in a randomized trial of experienced developers working in their own repositories." **Class: precision; tighten-default applies.**

**M3 — "Only" overclaims against our own ledger (§9).** "The only governance interventions with measured effects are enforcement-shaped" — the governance doc's own source ledger carries one measured non-enforcement datum (the securities-firm difference-in-differences study, logged as genuine-but-isolated). The transplant lost the original's scoping. Fix: "the governance interventions with measured effects are overwhelmingly enforcement-shaped." **Class: absolute → evidence-matched; tighten-default applies.**

## Confirmed clean (with voice flags, retained)

- **Abstract** — spine-conformant by construction; states, dangles nothing; all citations verified this conversation. CLEAN.
- **Introduction** — "two-thirds of developers… top frustration [21]": matches the survey (66%, top-ranked). Journey-map promises each verified against their pay sections. M1 aside, CLEAN.
- **§1** — all nine anchor deployments match the spine's caveat-attached forms; DORA conditionality, Veracode trend, strata distinction, abandonment figures all as-verified. "The strictest instrument in circulation" (official statistics) — defensible superlative, retained. "How most public discourse goes wrong" — voice, retained. P3 marker present.
- **§2** — EU AI Act dating (high-risk Aug 2026–2027) correct; ISO 42001 "first certifiable" correct; gap trio (75/36, 87/<25, 79/48) as sourced; *governance theatre* attributed; SR 11-7/SR 26-2 sequence as the supervisory record shows. P4 close present. CLEAN.
- **§3 head** — Amazon doctrine attribution precise per [22]; "good intentions, industrialized" is ours, presented as ours. CLEAN.
- **§4 lead** — "composed of five things" vs. §4.5's "enforcement plane consists of exactly six": nested scopes, no conflict; loop→mechanism map complete (P5 paid). CLEAN.
- **§5** — intervention numbers as peer-review sourced; detect/fix asymmetry as sourced; fold sentences carry the C-55-safe wording ("assumes a software artifact"). CLEAN.
- **§7** — verified against HEAD (2ab3c3f) this week: DEC-0001 enactment, lifecycle counts, live CI with public evidence upload, branch-protection interim flag, DEC-0002 posture. Strongest section in the paper evidentially. CLEAN.
- **§8** — H1–H3 with measurement bases as ruled; "aspiration" line consistent with corpus law. CLEAN.
- **§9** — faithful transplant of the adjudicated four-link chain; both bounds present; M3 aside, CLEAN.
- **Close** — four tools match spine S8 exactly; supersession + record-wins present. CLEAN.

## Disposition

M2 and M3 applied under the standing tighten-default. M1 applied as scoped reword + §4.6 distinguishing clause (small addition; strengthens rather than defends — flagged for the author's veto on the rc7 read). All three cut as rc7. **With rc7, this pass closes; pending item 1 completes.**

## Change log
- **2026-08-12** — v0.1: pass executed; 3 fixes, 11 sections confirmed clean; dispositions applied in whitepaper v1.0-rc7.
