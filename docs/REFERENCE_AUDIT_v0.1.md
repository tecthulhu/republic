# Reference Audit — Claims / Evidence / Gaps

**Version 0.1 — 2026-08-12 — audits REPUBLIC_WHITEPAPER v1.0-rc7 (carries forward to rc8 unchanged unless noted)**
**Origin:** proposed by external reviewer R4 (Copilot) as a reproducibility audit; executed by the paper's own side. Closes R4's half-declined methods request with the correct mechanism: not raw datasets (the load-bearing sources are third-party published literature, cited to origin), but a claim-by-claim cross-check showing which sentence rests on which source and how hard each can be leaned on.

**Method.** Every load-bearing claim in the paper was mapped to its citation; each citation's provenance is a live search-and-verification performed during drafting, recorded in the project's disposition ledgers. Four entries with single-search provenance were re-verified fresh for this audit (results in §1). Gap classes: **DIRECT** (source states the claim) · **DIRECT-SCOPED** (direct, with an instrument/population/date caveat that the paper carries or this audit adds) · **CONSISTENT-WITH** (T3 preprint, deployed only paired with an anchor, labeled as such) · **SYNTHESIS** (our inference across sources, marked as ours in the text) · **DESIGN** (grounded in the public corpus/repo, checkable at HEAD) · **HYPOTHESIS / DECLARED-OPEN** (no evidence claimed; stated as prediction or open cost).

---

## 1. Fresh verifications performed for this audit

| Entry | Result |
|---|---|
| Multi-IF ([1]) | **Verified.** He et al., arXiv:2410.15553 (Meta AI; open-source benchmark, facebookresearch/Multi-IF). Monotonic multi-turn degradation as cited. |
| FDSP ([20]) | **Verified, with instrument scope gained.** Alrashedy et al., arXiv:2312.00024; subsequently journal-published (J. Cybersecurity & Privacy, 2025). The 40.2%→7.4% figure is the **Bandit-detected** vulnerable fraction on PythonSecurityEval for GPT-4; the paper's own summary phrasing is "up to 33% (Bandit) / 12% (CodeQL)" reduction and "+17.6pp over self-feedback." Audit action: instrument-scope clause available for §5 (precision, not correction — see §3). |
| AutoSafeCoder ([20]) | **Verified.** Nunez et al., arXiv:2409.10737; ~13% vulnerability reduction with minimal correctness loss, as cited. |
| 480-incident study ([19]) | **Verified, with population caveat gained.** arXiv:2605.16281 (v1/v2). 87.5% vs 5.3% exact (EU AI Act Art. 72 coding); internal-detection subsample **n=24 of 480 (5%)**; authors explicitly discuss selection bias (mature orgs may both monitor internally and comply better) and frame the corpus as "publicly visible failures, not a census." Audit action: reference-entry precision (see §3). |
| Castricato ([6]) | Previously verified this round (arXiv:2402.07896); finding as cited. |
| GRASP ([20]) | **Secondary-verified only** (synthesis-source figures ~0.6→≥0.8); primary venue not independently confirmed. Audit action: marked **non-load-bearing** — [20]'s weight rests on FDSP, the iterative-loop line, AutoSafeCoder, and the 63-system taxonomy, all primary-verified. |

## 2. Claims / evidence / gaps table

| # | Claim (compressed) | Cite | What the source establishes | Gap class |
|---|---|---|---|---|
| 1 | Instruction-following degrades as context grows | [1] | 39% multi-turn performance drop / reliability collapse (Laban); monotonic per-turn degradation, "instruction forgetting" (Multi-IF); convergent benchmarks | DIRECT (convergence-cited) |
| 2 | Human oversight decays toward acceptance | [2] | Automation-bias corpus, decades replicated; systematic-review confirmation | DIRECT |
| 3 | Review degrades under generation volume | [2] | Anchored by (2); reviewer-habituation longitudinal findings are 2026 preprints | DIRECT + CONSISTENT-WITH (labeled in [2]) |
| 4 | Self-authored memory drifts, entrenches, rewrites | [3][7] | Recursive-training collapse (Nature + MAD + accumulation boundary); memory injection persists as precedent (MINJA >95%, AgentPoison) | DIRECT for mechanisms; agent-scale summarization framed as labeled analogy (rc8 per R1-§9) |
| 5 | Intent-delivery question, not capability, governs ROI | [14][21] | Gartner causes verbatim (costs, unclear value, inadequate risk controls — capability absent); SO trust/almost-right data | SYNTHESIS over DIRECT parts (sentence marked as framing; sources carry each clause) |
| 6 | Individual adoption 84–93% vs firm 17–20% (32% wtd) | [12][21] | Census BTOS (official statistics); Fed reconciliation; SO survey | DIRECT |
| 7 | Abandonment 17%→42% (2025) | [13] | S&P Global measurement | DIRECT |
| 8 | Agentic deployed ~17% vs 60%+ intent; >40% cancel forecast | [14] | Gartner; forecast **cited as forecast, dated** | DIRECT-SCOPED |
| 9 | −7.2% stability per +25% adoption; 2025 throughput recovery, stability negative; control-systems conditioning | [9] | DORA 2024/2025, program's own causal framing | DIRECT-SCOPED (self-report; recovery cited per F6) |
| 10 | Refactoring 25%→<10%; duplication rise | [10] | GitClear 211M-line mining | DIRECT-SCOPED (non-peer-reviewed, stated) |
| 11 | ~45% vuln rate; syntax >95% vs security ~55% flat across generations | [11] | Veracode 100+ models | DIRECT-SCOPED (vendor; no-security-guidance condition stated) |
| 12 | Substantial share of PRs merge unreviewed; review time ballooning | [21] | Single-vendor telemetry | DIRECT-SCOPED (color, never foundation — stated) |
| 13 | Believed +20%, measured −19% | [15] | METR RCT, experienced devs, own repos | DIRECT |
| 14 | Code-scale and market-scale failure = ungraded self-assessment | — | The paper's argument across 1–13 | SYNTHESIS (presented as the paper's claim) |
| 15 | Three governance regimes; none designed for agentic; EU dates | [17] | Primary instruments + practitioner analyses | DIRECT |
| 16 | Attestation-implementation gap (75/36; 87/<25; 79/48) | [18] | Three independent surveys | DIRECT (T2, convergent) |
| 17 | Governance-effectiveness evidence lacking; 220+ tools unvalidated | [18] | SLRs state it explicitly; tool review | DIRECT |
| 18 | Internal-detection compliance effect; "governance theatre"; enforcement > framework density | [19] | 87.5% vs 5.3% exact; theatre is the authors' term | DIRECT-SCOPED (**n=24 internal subsample; authors discuss selection bias** — precision added this audit) |
| 19 | SR 11-7 outcomes-analysis pillar; SR 26-2 excludes gen/agentic AI | [16] | Supervisory record, primary | DIRECT |
| 20 | Prompt constraints fail under pressure | [4][5] | Injection literature; instruction-hierarchy training | DIRECT + marked INFERENCE (the "field concedes" reading is ours, phrased as ours) |
| 21 | Negative instructions prime prohibited behavior | [6] | Wegner (human); Castricato (LLM: unchanged or **more** likely when told to avoid) | DIRECT |
| 22 | Model evaluators favor own outputs; closed loops entrench | [8] | Panickssery NeurIPS 2024 + mechanism follow-ons | DIRECT |
| 23 | Analyzer-feedback loops: 40.2%→7.4%; >40%→13% etc. | [20] | FDSP (Bandit instrument, PythonSecurityEval, GPT-4 — scope available); iterative-loop studies | DIRECT-SCOPED |
| 24 | Single-pass insufficient; best systems embed external verifiers | [20] | 63-system APR taxonomy (survey, cited for consensus per genre rule) | DIRECT |
| 25 | Detect-own-flaws poorly / fix-with-feedback well | [20] | Same experimental line | DIRECT |
| 26 | Amazon mechanism doctrine, attribution | [22] | Working Backwards p.17; doctrine-not-quote precision carried in the entry | DIRECT |
| 27 | §7 status: enactment, counts, live gate, public evidence, interim postures | repo | Verified at HEAD 2ab3c3f this week; **rc8 adds verify-yourself links (R4-accepted)** | DESIGN (repo-checkable) |
| 28 | H1–H3 | — | Stated as falsifiable predictions with measurement bases | HYPOTHESIS (by design) |
| 29 | Costs: provenance overhead, gate latency, telemetry volume | — | Stated as unquantified; plane measures own overhead | DECLARED-OPEN (by design) |
| 30 | Falsifiability position | — | Bounded twice (testable≠tested; reality-graded≠self-graded) | SELF-LIMITING (by design) |

## 3. Gaps found and actions

**Support-class gaps (claim lacking adequate source): ZERO.**

**Precision-class gaps: three, all upgrades not corrections —**
1. **[20]/§5 instrument scope:** add "(as measured by static analysis)" or equivalent to the 40.2→7.4 deployment — the caveat is armor (F6). → rc8 Batch A.
2. **[19] population note:** reference entry gains "internal-detection subsample n=24; selection-bias discussed by the authors" — strengthens the citation against exactly the check a reviewer would run. → rc8 Batch A.
3. **GRASP marking:** retained in [20]'s study family, flagged non-load-bearing pending primary verification; the section's numbers rest on the primary-verified trio. → this audit is the record; no D1 text change required (the 0.6→0.8 figure does not appear in D1).

**Already-slated by the review round (not new):** analogy labeling (R1-§9), maturity/permanence scoping (R1-§4, spine-gated).

## 4. Standing verdict

Every load-bearing claim in the whitepaper resolves to a verified source, a marked inference, a repo-checkable state, or an explicitly declared hypothesis/open item. The paper's weakest evidentiary joints are precision-class and now carry their caveats. This table is the methods appendix requested by R4, produced by the mechanism its memo lacked.

## Change log
- **2026-08-12** — v0.1: audit executed; 4 fresh verifications (Multi-IF, FDSP+scope, AutoSafeCoder, 480-incident+caveat); 30-claim table; 0 support gaps, 3 precision upgrades; GRASP marked non-load-bearing.
