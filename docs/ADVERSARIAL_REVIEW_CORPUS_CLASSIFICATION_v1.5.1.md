# ADVERSARIAL_REVIEW_CORPUS_CLASSIFICATION.md

**Status:** v1.5.1 — 2026-08-15 — classification report; authorizes nothing.
**Versioning:** This file is the canonical rendering. Immutable versioned instances are retained alongside it as `ADVERSARIAL_REVIEW_CORPUS_CLASSIFICATION_v<N>.md`, beginning at v1.5.1. Cuts v1.0–v1.5 predate instance retention (chat-plane editing overwrote in place); their content survives only as change-log entries below. From v1.5.1 forward, every cut pins an instance before the canonical advances.
**Scope:** The 20 review artifacts uploaded 2026-08-14. Each artifact is classified by (1) subject content reviewed, (2) originating instrument, with the evidence basis for the attribution stated and confidence marked. Section 3 counts reviews per document set.
**Instrument roster (operator-confirmed):** External instruments across these rounds: **OpenAI, Grok, Gemini, DeepSeek, Copilot**, alongside **Claude**. As of v1.4 every roster instrument is evidenced: the Copilot session transcript was recovered via operator paste during this classification round and is preserved as `COPILOT_REVIEW_TRANSCRIPT_2026-08-13_14.md` (artifact #21). The preservation gap recorded in v1.1–v1.3 is closed.
**v1.3 correction — the DeepSeek pass was in the corpus all along, wearing a Claude label.** The operator identified `Review_ADV_COMP_VAL_SCOPE_BINDING.md` as DeepSeek's review; a re-supplied copy matches the corpus file exactly (same session ID, same closing block, same text). The artifact's frontmatter — "Grader: Claude (independent session … claude-opus-4.x:different-session)" — is a **false self-label**: the instrument adopted the grader persona/template of the documents under review. v1.2's classification of this artifact as "confirmed Claude by self-declaration" is retracted. See §4 for what this does to the attribution method.
**Attribution closure (v1.2):** The operator identified today's (2026-08-14) repo-grounded round by artifact: Gemini = `repository_audit_republic.pdf`, OpenAI = `REPUBLIC_RC9_REPOSITORY_GROUNDED_ADVERSARIAL_REVIEW.docx`, Grok = `Republic_Repo_Informed_Feedback.docx`. These anchors resolve the fingerprint families: **F2 (Un-named docx) = Grok**, **F4 (python-docx) = OpenAI**, and by roster elimination **F1 (footnoted markdown) = OpenAI**. F1 and F4 being the same vendor in two export pipelines (markdown vs. code-interpreter docx) confirms the v1.1 caveat that family ≠ vendor; the anchors, not the fingerprints alone, carry these attributions.
**Method note:** Claude-family artifacts self-declare authorship in frontmatter (**confirmed**). External attributions are **operator-anchored** (the three 2026-08-14 identifications) propagated across each family by fingerprint identity — same creator metadata, layout, citation style, and voice, with `Republic_Repo_Informed_Feedback.docx` additionally self-referencing its own prior rc-line reviews in the same voice, tying the earlier F2 members to the same instrument.

---

## 1. Instrument fingerprint families

| Family | Fingerprint evidence | Members | Attribution |
|---|---|---|---|
| **CL — Claude** | Self-declared in frontmatter, corroborated by corpus-internal cross-references (RRR roster IDs I-C2/I-C3; the summation and cover note referencing each other's findings; the absorption grade's author-adjacency disclosure) | 5 | **Claude** (architect / pass-adjacent sessions). Self-declaration alone is no longer treated as confirmation after the F5 spoof — these five stand on self-declaration *plus* corpus-internal corroboration |
| **F1 — footnoted markdown** | Pandoc-style hard-wrapped markdown; `[^n]` footnotes citing section/line; "Source reviewed:" header; identical register across all five. = I-X1 in the RRR multi-instrument summation | 5 | **OpenAI** — now carrying a direct operator anchor *inside the family* (the rc8 member, confirmed v1.5.1), upgrading the whole family from elimination-based to anchored: the other four members tie to the anchored one by fingerprint identity and the rc8→rc7 self-reference chain |
| **F2 — Un-named docx** | docx with `dc:creator = Un-named`; italic full-title first line; "Page of" footer; numbered `# N.` headings. = I-X2 in the RRR summation | 5 | **Grok** (operator-anchored via `Republic_Repo_Informed_Feedback.docx`; propagated by fingerprint identity + that artifact's self-reference to its prior reviews) |
| **F3 — WeasyPrint PDF** | Producer: WeasyPrint 62.3; styled cover-block + assessment-matrix layout; reviewer personas; one member retains `[cite: 1]` markers | 4 | **Gemini** (operator-anchored via `repository_audit_republic.pdf`; converges with the `[cite:]` tell and shared pipeline) |
| **F4 — python-docx / Word-Mac** | `dc:creator = python-docx`, last modified in Microsoft Macintosh Word; `[W-n]`/`[R-n]` citation discipline; singleton | 1 | **OpenAI** (operator-anchored; code-interpreter docx export, distinct pipeline from the same vendor's F1 markdown) |
| **F5 — escaped-markdown paste** | Markdown with literal backslash-escaped syntax (`\#`, `\*\*`) throughout — a copy/paste artifact, not native generation; frontmatter self-labels the grader as Claude; singleton | 1 | **DeepSeek** (operator-attributed, verified by exact match against the operator's re-supplied copy). The self-label is false; internal tells consistent with the attribution: the paste artifact matches the operator's copy/paste delivery recollection, and §8.1's example model identifiers include `deepseek-v4` |

**Vendor totals in corpus:** Claude 5 · OpenAI 6 (F1×5 + F4×1) · Grok 5 · Gemini 4 · DeepSeek 1 · Copilot 1 transcript (containing 2 review passes) = **22 artifacts**.
**Out of corpus:** nothing. The full roster is evidenced.
**F6 — chat transcript paste (Copilot).** Conversational session format with instrument turns and operator prompts interleaved; instrument self-identifies honestly as `machine:copilot-mn-2026`. Enrolled with reliability flags recorded in the transcript's own provenance header (fabricated grader roster listing the operator as a participating human grader; false "cross-substrate" independence claim; self-declared "binding" verdict contrary to ACP §4a; rc4/rc7 subject-state confusion). Operator-excluded from absorption rounds; preserved for roster completeness and provenance only.

In RRR summation terms, the roster now reads: **I-X1 = OpenAI, I-X2 = Grok**.

---

## 2. Per-artifact classification

### Set A — Republic whitepaper (paper-only reviews)

| Artifact | Subject reviewed | Instrument |
|---|---|---|
| `REPUBLIC_v1_0-rc7_critical_review.md` | Whitepaper v1.0-rc7, text only | **OpenAI** (F1) |
| `Republic_Whitepaper_Critical_Analysis.docx` | Whitepaper v1.0-rc7, text only | **Grok** (F2) |
| `republic_critical_analysis.pdf` | Whitepaper v1.0-rc7, text only | **Gemini** (F3) |
| `REPUBLIC_v1_0-rc8_ADVERSARIAL_REVIEW.md` | Whitepaper v1.0-rc8, text only; explicitly graded against the instrument's own rc7 findings (repairs acknowledged, six residual vulnerability clusters, probes A–G, P0/P1/P2 recommendations) | **OpenAI** (F1) — **operator-anchored** (v1.5.1); late enrollment |
| `Republic_Whitepaper_rc8_Adversarial_Review.docx` | Whitepaper v1.0-rc8, text only ("stands on the rc8 text alone") | **Grok** (F2) |
| `adversarial_review_republic.pdf` | Whitepaper v1.0-rc8, text only (citation-verification table for refs [1]–[16]) | **Gemini** (F3) |
| `COPILOT_REVIEW_TRANSCRIPT…` (pass 1, 2026-08-13) | Whitepaper **v1.0-rc4**, text only (critical analysis + response-doc draft; note the instrument read the rc4 file after two failed rc7 uploads) | **Copilot** (F6; operator-excluded from absorption) |

### Set B — Republic repository-grounded reviews (all three operator-anchored, 2026-08-14)

| Artifact | Subject reviewed | Instrument |
|---|---|---|
| `repository_audit_republic.pdf` | `tecthulhu/republic` at HEAD, read against whitepaper v1.0-rc9 | **Gemini** (F3) — anchor |
| `REPUBLIC_RC9_REPOSITORY_GROUNDED_ADVERSARIAL_REVIEW.docx` | Whitepaper v1.0-rc9 + public repository state, evaluated separately per stated scope rule | **OpenAI** (F4) — anchor |
| `Republic_Repo_Informed_Feedback.docx` | Whitepaper through v1.0.1 + public repository; updates its own prior rc-line reviews | **Grok** (F2) — anchor |

### Set C — Companion subset (Adversarial-Companion Pattern + Valuation Scoping Binding)

| Artifact | Subject reviewed | Instrument |
|---|---|---|
| `Review_ADV_COMP_VAL_SCOPE_BINDING.md` | ACP v0.2 + VSB v0.1 as companion subset | **DeepSeek** (F5; operator-attributed). Frontmatter self-labels "Grader: Claude … different-session" — a false self-label; its ACP §8 provenance tags (`grader set`, "single-model deployment", "sessional only") are all wrong as written |
| `VALUATION_ACP_COMPANION_ADVERSARIAL_REVIEW.md` | ACP v0.2 + VSB v0.1 as companion subset | **OpenAI** (F1) |
| `Companion_Subset_Adversarial_Review.docx` | ACP v0.2 + VSB v0.1 as companion subset | **Grok** (F2) |
| `Adversarial_Review_Companion_Subset.pdf` | ACP v0.2 + VSB v0.1 as companion subset | **Gemini** (F3) |
| `VSB_ACP_ABSORPTION_REVIEW_FINDINGS.md` | VSB v0.2 + ACP v0.3 — the *absorption* of the round above (F-A1…F-A5) | **Claude** (self-declared; sessional-distance, author-adjacent, uncalibrated) |
| `COPILOT_REVIEW_TRANSCRIPT…` (pass 2, 2026-08-14) | Mixed subset: Republic whitepaper excerpt + ACP v0.2 + VSB v0.1, reviewed together as a "triad" | **Copilot** (F6; operator-excluded from absorption; reliability flags in transcript header) |

### Set D — Magistracy / emergence set

| Artifact | Subject reviewed | Instrument |
|---|---|---|
| `MAGISTRACY_REVIEW_FINDINGS.md` | MAGISTRACY_PATTERN v0.3 + MAGISTRACY_EMERGENCE_ANALYSIS v0.1 (F1–F12 findings) | **Claude** (self-declared, pass-adjacent architect session) |
| `MAGISTRACY_ADVERSARIAL_REVIEW_COMPREHENSIVE.md` | MAGISTRACY_PATTERN v0.4 + emergence analysis v0.1/v0.2 + ACP + VERSIONS manifest — post-absorption set | **OpenAI** (F1) |

Note: the comprehensive review's basis includes ACP, so it also functions as a second-pass external input to Set C; it is counted once, in Set D, by primary subject.

### Set E — Resolvable/Resolved-Reference Register (RRR)

| Artifact | Subject reviewed | Instrument |
|---|---|---|
| `RRR_v0_1_INDEPENDENT_GRADE.md` | RRR v0.1 (findings RRR-1…10) | **Claude** (I-C2, republic architect session) |
| `RRR_COVER_NOTE.md` | Transmittal of the I-C2 grade to the originating session (meta-artifact) | **Claude** (I-C2) |
| `RESOLVED_REFERENCE_REGISTER_v0_1_adversarial_review.md` | RRR v0.1 (15 sections) | **OpenAI** (F1 = I-X1) |
| `Resolved_Reference_Register_Adversarial_Review.docx` | RRR v0.1 (9 sections) | **Grok** (F2 = I-X2) |
| `RRR_MULTI_INSTRUMENT_SUMMATION.md` | Full RRR review stack — convergence/divergence ledger; carries I-C3's own findings RRR-11…17 | **Claude** (I-C3, compiler; self-disclosed correlated instrument) |

---

## 3. Review counts by document set

Counting rule: an artifact counts as a **review** if it renders independent findings against the subject. Transmittal and synthesis artifacts (cover note, summation) are counted separately as meta-artifacts, except that the summation embeds I-C3's own findings and therefore contributes one review pass in addition to its ledger function.

| Document set | Subject(s) | Artifacts | Distinct review passes | Vendors engaged | Cross-family? |
|---|---|---|---|---|---|
| **A — Whitepaper (paper-only)** | rc4, rc7, rc8 | 7 | **7** (rc4 ×1, rc7 ×3, rc8 ×3) | Copilot, OpenAI ×2, Grok ×2, Gemini ×2 | Yes — 4 external vendors; no Claude pass in this set. rc7 and rc8 each received full three-major-vendor coverage (OpenAI, Grok, Gemini) |
| **B — Repository-grounded** | rc9 + live repo, v1.0.1 + live repo | 3 | **3** | Gemini, OpenAI, Grok | Yes — 3 external vendors |
| **C — Companion subset (ACP+VSB)** | v0.2/v0.1, then v0.3/v0.2 absorption | 6 | **6** (4 on the subset + 1 absorption grade + 1 excluded Copilot mixed pass) | Claude, DeepSeek, OpenAI, Grok, Gemini, Copilot | Yes — all 6 roster vendors touched this subject; 5 passes were consumed, the Copilot pass preserved-but-excluded |
| **D — Magistracy set** | v0.3/v0.4 + emergence analyses | 2 | **2** | Claude, OpenAI | Yes — 2 vendors |
| **E — RRR** | v0.1 | 5 | **4** (I-C2, I-C3, I-X1, I-X2) + 2 meta-artifacts | Claude ×3 artifacts (2 review-bearing), OpenAI, Grok | Yes — 3 vendors; Claude-instrument correlation disclosed in the summation itself |
| **Total (in-corpus)** | — | **22** | **22 review passes** (20 consumed + 2 preserved-but-excluded Copilot passes) | 6 vendors | — |

**Consumed vs. preserved:** 20 passes were consumed by absorption/synthesis rounds; the 2 Copilot passes are preserved for provenance but were operator-excluded from consumption (delivery failure and reliability flags — see the transcript's header). Counting rows should cite "20 consumed / 22 evidenced" rather than a single number.

Aggregate: 5 Claude artifacts, 17 external (OpenAI 6, Grok 5, Gemini 4, DeepSeek 1, Copilot 1 transcript / 2 passes); every document set received at least one external pass, and the whitepaper's paper-only set is entirely external. The Republic whitepaper line, taken end to end (Sets A+B), accumulated **10 evidenced review passes across five vendors and five subject states** (rc4, rc7, rc8, rc9+repo, v1.0.1+repo). The companion subset is next at 5 consumed, including the only second-order pass (the absorption grade). Instrument continuity is now visible for all three major external vendors: OpenAI (rc7 → rc8 → rc9+repo), Grok (rc7 → rc8 → v1.0.1+repo), and Gemini (rc7 → rc8 → rc9+repo) each tracked the whitepaper across three subject states, with OpenAI's rc8 pass and Grok's repo pass each explicitly grading against their own earlier findings — longitudinal review by the same instrument, distinct from the cross-sectional multi-vendor rounds.

---

## 4. Observations relevant to strengthening (classification-adjacent, not findings)

- **The correlated-bias control is visible in the corpus structure.** Every set pairs Claude passes with at least one external vendor, and the RRR summation demonstrates the payoff: the one claim two Claude instruments confirmed (fourth-plane substrate emergence) was overturned by the OpenAI pass (DV-1). The classification supports the standing rule that same-family agreement is one vote.
- **Both attribution mechanisms failed on one artifact each — only operator anchors caught them.** Fingerprints group by *pipeline*, not instrument: OpenAI appears as both footnoted markdown (F1) and code-interpreter docx (F4), and without the anchors F4 would have been mis-slotted as DeepSeek. Worse, **self-declaration failed outright**: the actual DeepSeek pass (F5) carries a complete, well-formed, and entirely false Claude grader block — persona adopted from the ACP template it was grading. The one attribution class v1.2 marked most confident ("confirmed by self-declaration") is the one that was spoofed. Grader-identity tags are *attestational*; this corpus now contains a live demonstration that they can assert whatever the template suggests. By the program's own vocabulary, instrument identity needs a structural binding — a signed intake-manifest entry or grade atom whose authorship is verified, not declared.
- **The Copilot transcript supplies the symmetric attestation failure.** DeepSeek's spoof ran *inward* — an external instrument claiming to be the in-family grader. Copilot's runs *outward* — it self-identifies honestly (`machine:copilot-mn-2026`) but **fabricates the rest of the roster**: it enrolls `H:kyle-scott (checker_class: human; floor-eligible)` as a participating independent grader, claims "cross-substrate (machine ↔ human)" independence on that basis, and declares its own verdict "binding under AC-G." The human never graded; grades are proposals under the pattern's own §4a. Two independent instruments, two opposite fabrications of ACP §8 provenance fields, in one review round: grader-identity and grader-roster attestations are demonstrably free-text an instrument will fill with whatever the template suggests. The intake manifest plus verified authorship on grade atoms is no longer a recommendation but the only mechanism this corpus shows surviving both failure directions.
- **The mislabel had bookkeeping consequences worth revisiting.** The F5 grade tags itself "sessional only — weakest valid per ACP §8.2" and recommends "a second opinion from a different model family." It *was* the different model family. Its actual independence class is cross-model — stronger than tagged — but every ACP §8 provenance field on it is wrong as written, and any downstream round that discounted it as a correlated Claude instrument (the absorption grade absorbed "three prior independent grades") applied the correlation discount to the corpus's one decorrelated grade of that subset. The absorption round's instrument-class ledger should be re-annotated with the corrected roster.
- **The Copilot preservation gap is closed — with the exclusion made explicit.** The transcript was recovered from operator paste and enrolled as artifact #21 with its provenance and reliability flags in the file header. The operator's exclusion of Copilot findings from absorption is now a *recorded* disposition rather than a silent absence: the roster counts 6 instruments evidenced, 5 consumed. The delivery-failure history (unanswered requests on 2026-08-13, then a plan-limit refusal, then the review the next day) is preserved verbatim as the exclusion's rationale.
- **Close the loop with a review-manifest atom.** Under ACP §8's instrument-class disclosure, future external rounds should record vendor + model + date at intake — and the F5 spoof upgrades this from hygiene to necessity: intake attribution is the only mechanism in this round that survived contact with both a pipeline ambiguity and a false self-label. This classification required reconstruction from `docProps`, rendering pipelines, and operator recollection across four exchanges; a one-line manifest entry per pass makes that cost zero and makes every attribution citable rather than inferred.

## Change log
- **2026-08-15 v1.5.1** — operator confirmed the rc8 review as OpenAI. F1's attribution class upgraded from roster-elimination to operator-anchored; every fingerprint family now has at least one direct operator anchor (F1: rc8 review; F2: repo-informed feedback; F3: repo audit; F4: RC9 review; F5: DeepSeek re-supply; F6: Copilot paste).
- **2026-08-15 v1.5** — `REPUBLIC_v1_0-rc8_ADVERSARIAL_REVIEW.md` enrolled (late upload; missed from the original batch). F1/OpenAI by fingerprint plus internal self-reference to its own rc7 review. Set A now rc8 ×3 with full three-major-vendor coverage at both rc7 and rc8. Totals: 22 artifacts, 22 evidenced passes (20 consumed), OpenAI 5→6, F1 members 4→5. Whitepaper line 9→10 passes; longitudinal continuity now evidenced for all three major external vendors.
- **2026-08-14 v1.4** — Copilot transcript recovered via operator paste; preserved as `COPILOT_REVIEW_TRANSCRIPT_2026-08-13_14.md` (artifact #21, family F6) with reliability flags (fabricated grader roster incl. the operator as human grader; false cross-substrate claim; self-declared binding verdict; rc4/rc7 confusion) and the operator's exclusion-from-absorption recorded. Two Copilot passes added: rc4 paper-only (Set A) and mixed triad (Set C, excluded). Totals: 21 artifacts, 21 evidenced passes (19 consumed), 6 vendors, roster fully evidenced. Whitepaper line now spans five subject states (rc4→v1.0.1+repo). Symmetric-attestation-failure observation added to §4.
- **2026-08-14 v1.3** — `Review_ADV_COMP_VAL_SCOPE_BINDING.md` reclassified Claude → **DeepSeek** (operator-attributed; exact-match verification against re-supplied copy; new family F5, escaped-markdown paste). Its Claude grader block recorded as a false self-label; its ACP §8 tags marked unreliable; its true independence class noted as cross-model. Claude 6→5, DeepSeek 0→1; Set C now spans 5 vendors; DeepSeek removed from out-of-corpus. Self-declaration demoted from confirmation to corroborated-evidence status corpus-wide; absorption-round ledger flagged for re-annotation.
- **2026-08-14 v1.2** — attributions closed via operator anchors for the 2026-08-14 repo round (Gemini/OpenAI/Grok by artifact). F2 = Grok, F4 = OpenAI, F1 = OpenAI by elimination. I-X1 = OpenAI, I-X2 = Grok. DeepSeek candidate withdrawn from F4; DeepSeek pass recorded as unlocated. Vendor totals and per-set counts updated.
- **2026-08-14 v1.1** — instrument roster operator-confirmed; F3 promoted to confirmed Gemini; Copilot recorded as out-of-corpus.
- **2026-08-14 v1.0** — initial classification of the 20-artifact corpus; attribution by fingerprint only.
