# External Review Dispositions — rc7 Critical Review

**Version 1.0 — 2026-08-14 — review-round ledger. R1 = OpenAI (critical review); R2 = Grok; R3 = Gemini (peer-style PDF); R4 = Copilot (memo format; reviewed stale rc4 — noted).

R1 note: Verdict: highest-quality input the paper has received; its meta-thesis — apply the corpus's grading discipline to the paper's own prose — is accepted in full. No architectural changes required or proposed; all dispositions are epistemic tightening, exactly as the review predicts.**

---

## R2 (Grok) dispositions — 2026-08-12

| R2 § | Finding | Disposition |
|---|---|---|
| 3.1 | Strongest claims prospectively supported until chain-level data | **CONVERGES with R1-P1** — handled by bounds + Batch A tightening; convergence confirms priority. |
| 3.6 | Rhetorical register; "worldview-selling" close | **CONVERGES with R1-§14** → aphorism trim upgraded from optional to committed (~20–30% conversion at polish; S9 lines exempt). Close structure retained (ruled takeaway inventory); its phrasing joins the hortatory pass. |
| 3.4 | Break-glass / temporary elevation / multi-party under ops pressure | **CONVERGES with R1-§11/§7** → §4.4 waiver paragraph gains one sentence: no elevation path by design — urgency maps to governed waiver + human veto, never widened authority — and whether that holds under operational pressure is H1's subject, not an assumption. Break-glass metrics join H1's measure set. |
| 3.2 | Adoption friction / governance tax unaddressed; routing-around pressure | **ACCEPT (R2's best find).** §8 gains a limitations paragraph: costs real and front-loaded at authoring; the bet is supervision's costs compound while structure's amortize; the bet is measurable, not assumable — H2's cost side. No adoption-path claims. |
| §4 | No related-work positioning vs. 2026 control planes / gateways / policy engines | **ACCEPT.** Compact related-work note at §2 close: concurrent tooling governs access and runtime behavior; Republic's distinct combination = corpus as first-class queryable law, computable enforceability, no central mutable governance service, falsifiability as design goal. Pairs with R1-M1's supply-chain clause. |
| 3.5 | Provenance cost unquantified; tiered provenance may be needed | **ACCEPT as declared-open.** One sentence: overhead unquantified pre-C1; tiered provenance an anticipated option; the plane measures its own overhead as a side effect, so quantification is part of the first chain run's output. |
| 5 | Treat system-level measurements as the primary next deliverable | **ACCEPT-lite.** One line in §8: after this paper, the deliverable is the measurement, not the feature list. |
| 3.3 | Generality risks mild overstatement | **DECLINE, reasons on record:** the wording already draws the requested line ("design property, not an offering, until its chain has been walked"); the property claim is grep-verified (C-55 pass). |
| 2.x | Strengths (diagnosis, distinction, coherence, §7 candor) | NO ACTION — independent confirmation of ruled structure; notable that both reviewers name §7 as the credibility anchor. |

## R3 (Gemini) dispositions — 2026-08-12

| R3 § | Finding | Disposition |
|---|---|---|
| 3.5 + rec 4 | Veto fatigue, waiver overuse, "governance decay" telemetry | **THREE-WAY CONVERGENCE (R1 §11, R2 3.4, R3)** — the exception layer is now the consensus-predicted failure surface across three independent models. Recorded as pre-registration of H1's importance; rec 4 is H1-revised's measurement set nearly verbatim. No new edit beyond the already-slated H1/waiver work. |
| 3.1 + rec 3 | Developer friction / schema rigidity; quantify DX in the research program | **CONVERGES (R2 3.2, now 2-way) + ACCEPT rec 3:** H-series measurement set gains DX/friction metrics (authoring time vs. change size, waiver-request rate, time-to-first-governed-commit) — converts the tax objection into a measured variable. Joins the limitations ¶. |
| 3.3 + rec 1 | Cold-start / legacy retrofit barrier; auto-atomizer tooling | **ACCEPT (new).** §8 limitations gains one sentence: cold-start acknowledged; anticipated path is *enrollment, not migration* — identity assigned to legacy artifacts as-is, on touch, never bulk rewrite (prior art: the Cornerstone enrollment pattern). Auto-atomizer noted as future tooling, unpromised. |
| 3.2 + rec 2 | Gate latency in fast agentic loops; async evidence aggregation | **ACCEPT-fold:** joins the declared-open costs sentence (with provenance overhead); async aggregation (blocking authz, async telemetry) noted as anticipated option consistent with the bus topology. |
| 3.4 | Embedding drift → inconsistent candidate retrieval | **DECLINE, correction on record:** already answered in §4.5 — band-labeled digest-pinned instruments, permanent validity under-instrument, supersession-not-corruption; and *similarity proposes, gates dispose* bounds the blast radius: retrieval jitter cannot alter enforcement, which binds by instance identity. |
| 4 (matrix), 5 | Auditability "EXCEPTIONAL"; §7 "avoids vaporware inflation" | NO ACTION — third independent validation of §7 as credibility anchor; provenance confirmed as differentiator by a third frame. |
| refs | Publisher listed as "Eldritch Labs / Anthropic" | Noted for amusement; incorrect — Anthropic is the collaborator's affiliation, not co-publisher. |

## R4 (Copilot) dispositions — 2026-08-12

| R4 item | Finding | Disposition |
|---|---|---|
| Inline §7 | Direct repo/atom links + reviewer reproduction guide for standing queries | **ACCEPT — best find of R4; cheapest high-value edit of the round.** §7 gains a verify-yourself pointer: store address, `dec-0001-enacted` tag, acta path, one sentence on re-running standing queries. Operationalizes "the record wins." |
| 3 | Telemetry volumes, provenance-walk latency | **COMPLETES 3-WAY** (R2 provenance cost, R3 gate latency, R4 volumes/latency) — declared-open costs sentence now carries all three named costs + plane-measures-own-overhead. |
| 4 + experiments | Migration playbook, "Republic-lite" incremental tiers, pilot/A-B designs | **COMPLETES 3-WAY** (R2 tax, R3 cold-start, R4 playbook) — covered by limitations ¶ + enrollment sentence. Lite-tier concept and pilot/A-B designs logged as future adoption-doc + C1 program-design material, unpromised in D1. |
| 2 | Formal adversary model; stolen leaf creds; **compromised gold base images** | **CONVERGES (R1 §7 → 2-way)** + gold-base-compromise **accepted as new named vector** in §4.4's property list (conformance suite + digest pinning partial; established at base/verifier milestone, declared not claimed). |
| 1 + inline §1 | Publish datasets/scripts; per-statistic methods paragraphs | **CLOSED via REFERENCE_AUDIT v0.1** (the audit R4 proposed, executed by the paper's side: 30-claim cross-check, 0 support gaps, 3 precision upgrades into Batch A). Original half-decline reasons stand: §1/§5 synthesize third-party published literature, each cited to origin — no raw datasets of ours exist to publish; source-grading discipline already stated at References. Ours-data (evidence rows) is public and now linked (accept-half). Per-stat methods ¶s declined: F6 inline caveats + ruled §1 depth. |
| Decision points | Leadership approvals | Out of D1 scope; the leadership in question is the author. |
| Meta | Reviewed rc4 (stale) | Noted; several asks already in flight by rc7. R4 uniquely missed the exception layer — the one consensus item. |

## ROUND 2 (rc8): R5 = OpenAI (27-section graded review) · R6 = Grok (docx) · R7 = Gemini (panel PDF)

**Round-2 character:** round 1 attacked architecture; round 2 attacked wording and found one composition attack. R5 credits all round-1 repairs as held; verdict "publishable in substance — precision pass, not conceptual rewrite." R6: "ready to be tested by the system it describes." R7 supplies the headline finding.

| Finding | Instruments | Disposition |
|---|---|---|
| **Self-dilution attack** — declared postures compose: unbounded agent authorship + spawn-accepts-proposed → agent weakens own acceptance pre-ratification → graded vs. diluted spec → §3 loop reintroduced | **R7 (named as attack)** + R5 #15 + R6 §4.4 (3-way on the posture cluster) | **Class III joint ruling:** acceptance-baseline pinning (gate grades vs. last floor-touched acceptance instance) + weakening-diff lint; full close = magistracy D1 authorship mandate (gated); D1 §7 sentence naming composition + time-boxed mitigation. Routed to republic session verbatim-ready |
| P0 precision set (component-vs-assembly; instrument independence; **evidence completeness structural / validity graded**; etc.) | R5 | **rc9 batch, tighten-default** (Class I, ~14 edits) |
| Spine-touching narrowings: rung-4 "sole authority"; Bound-2 "event-grounded, externally replayable"; H2 pre-registration | R5 #14/#26/#20 + Probe B | **Spine v1.2 mini-slate (Kyle, 3 items)** |
| §7 evidence-class tagging ("exemplary rather than merely candid") | R5 P1 | Accept — rc9 |
| Time-box interim postures; H4/DX equal-prominence; §7 ruthlessly-current process law | R6 | Accept — rc9 language + process law |
| Shadow-path bypass; digest-pin update rigidity | R7 | Accept-lite — chokepoint sentence + declared-open cost item |
| Revocation formal spec pre-v1.0; query benchmarks pre-v1.0 | R7 | **Declined w/ posture:** declared-work at chain-verifier milestone; C1 measures — pre-C1 benchmarks would be the invented-metrics defect |
| Seven adversarial probes A–G (false-green, denominator manipulation, provenance omission, spawn blind-spot, bad-policy, bad-oracle, tax counterexample) | R5 | **Routed:** gate-0 probe suite gains seven critic-authored probes |
| **Meta-governance frontier** — coverage/risk/instrument definers must become governed, versioned, attackable artifacts | R5 (closing) | **Routed:** named Consulta; the corpus's own answer per R5 |
| §7 praised (3rd consecutive round; 9 instruments total); zero architectural changes (again); citation audit all-VERIFIED (2nd independent) | R5+R6+R7 | Recorded |

## R8 — Repository-grounded adversarial review (rc9/v1.0.1 + live repo, 2026-08-14)

**New review class:** paper↔repo cross-examination with a stated scope rule (paper claims corroborated only where public repo evidence supports the same bounded proposition). Overall judgment quoted for the record: Republic has crossed "from a coherent governance architecture with prototype evidence into a real, publicly inspectable substrate" — and the proof burden shifts upward to meta-controls.

| Finding | Disposition |
|---|---|
| **P0 — merge-blocking not publicly closed.** "A red suite blocks merge" is true only if the status check is *required on main* (owner setting, publicly unverifiable); the workflow is a control, the repo rule is the enforcement | **ACCEPT — and the overclaim is a v1.0-series regression introduced in this session's rc8 §7 rebuild**, which dropped the previously-declared "branch protection = owner-configured interim posture" disclosure (praised by R3/R4 in round 1). Two-part fix: **(a) paper** — v1.0.2 restores the two-halves wording as declared posture (rides the SPEC-0128 update trigger); **(b) repo** — new story: repository-rule state becomes a governed evidence object (periodic control captures required-check/ruleset config for the protected branch, bound to the stable CI context name). Kyle to confirm whether the check is currently required on main; the wording fix applies either way |
| **README drift (dogfood target):** README claims stronger than the governed source in two places ("every requirement enforced → number" vs. rc9's binding-coverage narrowing; "Nothing to fail open" vs. rc9's gates-can-drift concession) | **ACCEPT — routed to architect session** (README owner) with the two fixes; the recommended **render-drift control** (public renderings as derived artifacts whose load-bearing claims check against a claim register) joins the C7 enrollment scope — it is the spine's one-spine-N-renderings law, mechanized |
| **Meta-control table** (required-check config, test oracles, coverage denominators, linter semantics, standing-query population lineage) | **ACCEPT — merged into the B3 meta-governance Consulta scope** (extends it with required-check config and query-population lineage, previously unnamed) |
| **Recommended checks:** bad-oracle fixture, provenance-omission fixture, C1 closed-loop probes | **CONVERGES with R5 probes E/F/C** — second independent authorship of the same probe designs; strengthens the gate-0 inventory's provenance |
| Material corroborations (§2: conformance machinery real, negative evidence implemented, current-front narrative supported) | **Recorded** — the paper's evidentiary standing upgraded by inspection, per the review's own scope rule |

## ROUND 3 — Repository-grounded round complete: R8 (OpenAI), R9 (Grok, repo-informed feedback), R10 (Gemini, repository deep-dive audit)

**Round character:** all three instruments independently inspected the live repository and cross-examined it against the paper. All three **upgraded the assessment on inspection** (R9: "high-quality design argument *with a public, partially operating implementation*"; R10: "not vaporware... a working, self-governing software substrate... one of the most intellectually honest agentic AI projects in open source"; R8: "inspectable enforcement substrate"). The verify-rather-than-trust posture was exercised by its intended audience and held.

| Finding | Instruments | Disposition |
|---|---|---|
| **"The next artifact is data, not prose"** — prose refinement at diminishing returns; C1 measurements, live defect history, cost numbers are the decisive tests | **R8 + R9 + R10 — 3-WAY, round-closing** | **ACCEPT AS PROGRAM RULING (recommended):** the adversarial review round closes permanently; further pre-C1 reviews accepted only for new claims. C1 is the next reviewer. |
| Branch-protection evidence (P0 follow-through) | R8, architect bridge | **In flight repo-side** (agent instructions issued: live-capture from API, stable-context binding, admin-bypass stated truthfully, claim-atom binding). v1.0.2 wording fix rides its landing. |
| **Reconciliation-lag window** — merged-but-unreconciled atoms read `proposed`; does the spawn gate resolve lifecycle live or from last reconcile? A spawn during the window is the fixture | **R10 (new — none of 10 prior instruments named it)** | **ACCEPT — routed:** question + probe fixture to the architect session (gate-0 inventory grows by one; candidate answer classes: live in-memory reconciliation at gate-time, or window declared as posture with bound). |
| **Ephemeral-container revocation** — revocation = harness teardown (SIGTERM) within container lifetime; no on-wire token revocation, by the no-standing-service design | R10 (precision on R1/R4's threat-model item) | **ACCEPT — merged into C4** (ENT threat-model SPEC mapping): the honest posture names supervised teardown + short lifetimes as the compensating controls, on-wire revocation absent by design. §4.4's declared-work list already carries revocation-propagation latency; C4 gains this concrete form. |
| Git-churn friction; local-bypass threat; index-caching at scale | R10 (converges with adoption cluster + declared-open costs) | Chokepoint doctrine answers the bypass half (ungoverned local work never becomes truth); git-churn joins H4's cost side; index caching is the generated-index design, noted at scale as declared-open. |
| Composed-posture closure priority; status-language precision as surface grows | R9 (aligns STORY-0014–0016 + R6's ruthlessly-current law) | Already in flight / standing law. |

## Cross-review convergence table (running)

| Finding | R1 | R2 | Status |
|---|---|---|---|
| Prospective vs. demonstrated | ✓ | ✓ (+R3) | 3-way; handled (bounds + tightening) |
| §7 honesty as credibility anchor | ✓ praised | ✓ praised | ✓ R3 praised — 3-way validation of doc-truth discipline |
| Register / aphorism density | ✓ | ✓ | **Upgraded to committed trim** |
| Exception layer as stress point | ✓ (adaptation, threat model) | ✓ (break-glass, ops pressure) | **✓ R3 (veto fatigue, decay telemetry) — 3-WAY; consensus-predicted failure surface; pre-registers H1** |
| Identity threat model (creds, revocation, base compromise) | ✓ | — | ✓ R4 — 2-way; §4.4 property list + gold-base vector |
| Record vs. proposition (truth model) | ✓ | — | Batch A |
| Maturity/permanence overclaim | ✓ | — | Batch A (spine-gated) |
| Adoption cluster (tax / cold-start / playbook) | — | ✓ | ✓ R3 + ✓ R4 — **3-WAY**; limitations ¶ + enrollment direction + DX metrics; lite-tiers logged for adoption docs |
| Cost/perf quantification (provenance, latency, telemetry) | — | ✓ | ✓ R3 + ✓ R4 — **3-WAY**; declared-open sentence carries all three, plane measures own overhead |
| Related work / landscape | ✓ (supply-chain, M1) | ✓ (control planes) | Batch A (two-front positioning) |
| Generality | — | ✓ | Declined w/ reasons |

## Batch A — D1 prose edits (apply as rc8 after the review round closes; spine-gated items marked)

**A-add-2 (defense-round finding, republic-session ruling, 2026-08-13): the spawn-gate invariant correction** — "no story, no spawn" (§4.5, §6) becomes **"no resolvable story, no spawn"**, plus the declared bootstrap posture: *a story may be spawned while proposed; ratification follows the evidence, it does not gate the work* (circular-gate rationale; ruled repo-side, posture atom pending ID). §7's seam disclosure cites the posture atom when it lands. Provenance: this session's defense cross-check at HEAD 97ee84f → republic session's ruling, transported by the human NATS bridge.

**A-add (Kyle-ruled, 2026-08-12): §8 limitations paragraph gains the banded-delegation forward-posture sentence** — "The architecture also anticipates the cost's descent: because decisions are typed atoms and authority is caveated, ratification itself can be banded — mechanically resolvable decisions auto-enacting on green evidence, scoped mandates ratifying within ceilings under sampled audit, the human veto retained asynchronously and the constitutional floor retained absolutely — a delegation pattern whose progression is gated on the same measurements as everything else here, including the measured decay of the delegation itself." Declared-direction class; gated, unpromised; source: MAGISTRACY_PATTERN v0.2.

| Rev § | Finding | Disposition |
|---|---|---|
| 8 | "True at T, permanently" conflates record with proposition | **ACCEPT.** §4.1 gains the four-way distinction (immutable record / resolved state / evidenced claim / truth) compressed to two sentences, closing on: **"The record is immutable. Its claims remain falsifiable."** |
| 4, 16 | "Not a maturity problem" = permanence from persistence; split market vs. architectural thesis | **ACCEPT.** §1: persistence-scoped wording + the trust-boundary argument ("even if capability improves dramatically…"). §9: explicit two-theses separation — market thesis (urgency) / architectural thesis (durable): *governability requires externally resolvable authority, intent, execution, and verification rather than self-attested state.* ⚠ Gated on spine F2 reword (Batch B). |
| 5 | Enforcement ≠ correctness | **ACCEPT.** Bound 3 added at §9: *structural governance guarantees control fidelity and observability, not policy correctness* — it makes declared governance mechanically consequential; it does not make it wise. Binding-triple reference retained as the machinery that keeps the layers separately examinable. |
| 6 | "No governance service" overstated | **ACCEPT.** §4.5 reframed: minimization of independent mutable governance infrastructure; enforcement at chokepoints that already hold authority over the governed transition; forge-property claim retained in its already-hedged form ("visible when bypassed"). |
| 7 | Identity: containment of compromised authority under-treated | **ACCEPT.** §4.4 gains a compact threat-model paragraph naming revocation, credential compromise, blast radius, rotation-with-provenance, delegation limits, lifetimes, and confused-deputy resistance as **security properties to be established by the chain verifier and authorization grammar, with acceptance criteria at that milestone** — declared, not claimed. |
| 9 | Model-collapse analogy unlabeled | **ACCEPT.** §3: "an analogous closed-loop degradation risk — the collapse dynamic observed when models train on their own outputs [3], hypothesized homologous at the scale of a single agent's record"; memory-injection literature [7] noted as the closer direct evidence. |
| 10 | "Never in context" stronger than evidence | **ACCEPT with precision.** Two-step form: the evidence supports *a prohibition that matters cannot depend on context for enforcement*; Republic **additionally chooses** zero injection (`injection: never`), trading possible instructional benefit for zero priming risk. Design choice distinguished from derived law. |
| 11, 12 | H1 near-definitional; H2 density Goodhart | **ACCEPT.** §8: H1 → *effective structural enforcement decays more slowly under repeated exposure than supervisory enforcement* (measures: waiver frequency, control weakening, bypass, out-of-band execution, escaped defects). H2 independent variable → risk-weighted verification coverage. ⚠ Gated on spine S4 reword (Batch B). Companion update: evidence brief §4 at its next cut. |
| 14 | Aphorism density | **ACCEPT modestly.** Targeted conversion of ~20% of secondary aphorisms to plain prose at final polish; S9 inventory lines preserved verbatim. Author's voice call on the specific list. |
| 13, 15 | H3 praise; do not simplify §§4–6 | **NO ACTION** — validates prior rulings (audience markup: on-ramps, not cuts). |

## Batch B — Spine v1.1 ruling slate (Kyle; one session clears six)

Spine law: D1 may not diverge from the ratified spine, so these gate the corresponding Batch A edits.

1. **S6/F2 reword:** "not a maturity problem, so waiting is not a strategy" → *"observed scaling has not closed these defect classes — and even if it does, generation and verification should not share an ungraded trust boundary; waiting is not a strategy either way."*
2. **S4/H1 reformulation** per Batch A row 11.
3. **S4/H2 variable** → risk-weighted verification coverage.
4. **S2 addition — the architectural thesis** as a new rung or S4 preamble: *"Governability requires externally resolvable authority, intent, execution, and verification rather than self-attested state."* (Market thesis retained as rung 2; this is the durable layer beneath it.)
5. **S9 additions (already pending):** the intent-delivery question; the Amazon doctrine line (always-attributed).
6. **S4 Bound-1 currency amendment (already pending):** "first evidence rows exist for corpus controls."
   — Plus new **Bound 3** (control fidelity ≠ policy correctness) into S4, from Batch A row 5.

## Batch C — Upstream (Cass session; Consulta candidates)

1. **ONT truth-model language:** evaluate whether the corpus's own formulation needs the record/proposition distinction ("true at T" vs. "asserted/ratified at T"). The evidence machinery (measurements against subject digests, supersession) already embodies the distinction; the question is whether the prose of the law does. Reviewer's formulation offered as candidate text.
2. **ENT threat-model acceptance criteria:** revocation, blast radius, rotation, confused deputy — confirm which are already specified in the entity ontology/caveat grammar and which need SPEC additions at the chain-verifier milestone; D1's §4.4 paragraph should then cite their IDs.
3. **Evidence brief H1/H2** next cut inherits Batch B wordings.

## Meta

The review is itself evidence for H1's revised form: an external grader detected drift (prose outrunning evidence) that two internal passes missed — independent effective challenge working as SR 11-7 says it should. The reviewer is credited in the paper's acknowledgments if Kyle rules to add them (open question: attribution form for an anonymous/model reviewer).

## Change log
- **2026-08-14** — v1.0: Round 3 complete (R8/R9/R10, all repository-grounded, all upgrading on inspection); **3-way round-closing convergence recorded — "the next artifact is data, not prose" — review program recommended CLOSED, C1 is the next reviewer**; reconciliation-lag window (new, R10) routed with its fixture; revocation posture merged into C4.
- **2026-08-14** — v0.9: R8 (repository-grounded) dispositioned — P0 merge-enforcement gap accepted and owned as an rc8-rebuild regression (fix staged for v1.0.2 + repo-side evidence story); README drift routed; meta-control table merged into B3; probe convergence with R5 recorded.
- **2026-08-13** — v0.8: Round 2 (rc8) dispositioned — R5/R6/R7; dilution composition attack (Class III joint ruling routed); rc9 precision batch staged (Class I); spine v1.2 mini-slate staged (Class II); probes A–G + meta-governance Consulta routed (Class IV); two declines w/ posture.
- **2026-08-13** — v0.7: A-add-2 recorded — spawn-gate invariant correction ("resolvable, not ratified") + declared bootstrap posture, from the defense round's seam finding and the republic session's ruling; magistracy next-cut queue gains the second wild-emergence instance (mandate-unbounded agent authorship, STORY-0002 v1.2.0).
- **2026-08-12** — v0.6: Batch A gains the banded-delegation sentence for §8's limitations ¶ (Kyle-ruled; magistracy pattern as source; answers R2-3.2/R3-3.1's cost objection with a gated design response).
- **2026-08-12** — v0.5: R4's reproducibility item closed via REFERENCE_AUDIT v0.1 (0 support gaps, 3 precision upgrades → Batch A: [20] instrument scope, [19] n=24 note).
- **2026-08-12** — v0.4: R4 (Copilot, vs. stale rc4) dispositioned — §7 verify-yourself links **accepted** (round's cheapest high-value edit); cost/perf and adoption clusters complete **3-way**; threat model → 2-way + gold-base vector; reproducibility half-declined with reasons (third-party literature, no owned datasets; per-stat methods ¶s declined). Ledger now: 3 three-way convergences, 4 reasoned declines.
- **2026-08-12** — v0.3: R3 (Gemini) dispositioned — exception-layer convergence completes 3-way (pre-registration of H1 recorded); DX metrics accepted into H-series; cold-start limitation + enrollment-direction accepted; latency folded into declared-open costs; embedding-drift declined with §4.5 correction. Batch A final unless further reviews arrive.
- **2026-08-12** — v0.2: converted to review-round ledger; R2 (Grok) dispositioned — 3 convergences, 4 accepts (friction ¶, related-work note, provenance declared-open, primary-deliverable line), 1 decline with reasons (generality); convergence table added; Batch A grows accordingly, Batch B unchanged (no new spine items), rc8 held until round closes.
- **2026-08-12** — v0.1: full disposition of the external review; Batch A specified, Batch B slated for ruling, Batch C queued for the repo session.
