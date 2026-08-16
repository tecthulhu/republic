# ADVERSARIAL_REVIEW_CORPUS_MANIFEST.md

**Status:** MANIFEST v1.2 — 2026-08-15 — inventory and identity record; authorizes nothing.
**Scope:** Every file in the adversarial-review corpus classified in `ADVERSARIAL_REVIEW_CORPUS_CLASSIFICATION.md` (v1.5.1), plus the classification round's own deliverables. This manifest records *what each file is* — identity, instrument, subject, version role, and content digest. Analysis and rationale live in the classification report; this file is the lookup, not the argument.
**Versioning rule:** This manifest follows the canonical-plus-instance model. `ADVERSARIAL_REVIEW_CORPUS_MANIFEST.md` is the canonical rendering; each cut pins an immutable instance `ADVERSARIAL_REVIEW_CORPUS_MANIFEST_v<N>.md` before the canonical advances. The integrity check is: canonical digest equals newest instance digest.
**Digest law:** Every file row carries a SHA-256 digest. The digest identifies; the filename locates. If a filename and digest disagree with this manifest, the digest governs — a matching digest under a different name is the same artifact; a matching name with a different digest is a different (or tampered) artifact. Tables show the first 12 hex characters; §5 is the full-digest register.

---

## 1. Classification-round deliverables

| File | Digest (12) | What it is | Version role |
|---|---|---|---|
| `ADVERSARIAL_REVIEW_CORPUS_CLASSIFICATION.md` | `f51d8af1a1d1` | Classification report: per-artifact subject + instrument attribution, per-set review counts, attribution-method findings, change log v1.0–v1.5.1 | **Canonical.** Advances with future cuts; must always match the newest pinned instance |
| `ADVERSARIAL_REVIEW_CORPUS_CLASSIFICATION_v1.5.1.md` | `f51d8af1a1d1` | Byte-identical pin of the canonical at v1.5.1. First retained instance; cuts v1.0–v1.5 were edited in place and survive only as change-log entries | **Immutable instance.** Never edited |
| `COPILOT_REVIEW_TRANSCRIPT_2026-08-13_14.md` | `88c3a4a59440` | Verbatim Copilot session transcript (2026-08-13/14), recovered via operator paste; provenance header records reliability flags and operator exclusion from absorption | **Corpus artifact #21**, single-cut v1.0; stored with deliverables because it was created (preserved) during this round |
| `DIGEST_ANCHOR_VERIFICATION.md` | `72bf04ccdd05` | Integrity pattern: the digest/anchor law, procedures V-1…V-5, five-failure evidence base, lint hooks, signing successor. Archivist-authored v0.1; a proposal until independently graded per ACP | **Canonical**, pattern atom |
| `DIGEST_ANCHOR_VERIFICATION_v0.1.md` | `72bf04ccdd05` | Byte-identical pin of the pattern at v0.1 | **Immutable instance** |

Integrity check at manifest time: canonical digest `f51d8af1…` = instance digest `f51d8af1…` — **PASS**.

---

## 2. Corpus artifacts — Set A: Republic whitepaper, paper-only

| File | Digest (12) | Instrument | Subject | Disposition / flags |
|---|---|---|---|---|
| `republic_critical_analysis.pdf` | `27737ec52ea5` | Gemini (F3) | Whitepaper v1.0-rc7 | Consumed. Retains `[cite: 1]` markers (F3 vendor tell) |
| `REPUBLIC_v1_0-rc7_critical_review.md` | `83bbcc3da2b3` | OpenAI (F1) | Whitepaper v1.0-rc7 | Consumed |
| `Republic_Whitepaper_Critical_Analysis.docx` | `8eed26239c2e` | Grok (F2) | Whitepaper v1.0-rc7 | Consumed |
| `adversarial_review_republic.pdf` | `85d55e4b84b3` | Gemini (F3) | Whitepaper v1.0-rc8 | Consumed. Includes citation-verification table refs [1]–[16] |
| `REPUBLIC_v1_0-rc8_ADVERSARIAL_REVIEW.md` | `4d1776169642` | OpenAI (F1) | Whitepaper v1.0-rc8 | Consumed. Operator-anchored (v1.5.1); grades rc8 against its own rc7 findings; probes A–G; late enrollment v1.5 |
| `Republic_Whitepaper_rc8_Adversarial_Review.docx` | `c538ecf1d4b6` | Grok (F2) | Whitepaper v1.0-rc8 | Consumed |
| `COPILOT_REVIEW_TRANSCRIPT…` (pass 1) | `88c3a4a59440` | Copilot (F6) | Whitepaper v1.0-rc4 | **Excluded** from absorption; preserved for provenance. rc4 read after two failed rc7 uploads |

## Set B: Republic repository-grounded

| File | Digest (12) | Instrument | Subject | Disposition / flags |
|---|---|---|---|---|
| `repository_audit_republic.pdf` | `302a01c28cef` | Gemini (F3) | `tecthulhu/republic` at HEAD vs whitepaper v1.0-rc9 | Consumed. Operator anchor for F3 |
| `REPUBLIC_RC9_REPOSITORY_GROUNDED_ADVERSARIAL_REVIEW.docx` | `717eb959ea3b` | OpenAI (F4) | Whitepaper v1.0-rc9 + public repo (inspected 2026-08-14) | Consumed. Operator anchor for F4; `[W-n]`/`[R-n]` citation discipline |
| `Republic_Repo_Informed_Feedback.docx` | `4b5cf2c4e328` | Grok (F2) | Whitepaper through v1.0.1 + public repo | Consumed. Operator anchor for F2; updates its own prior rc-line reviews |

## Set C: Companion subset (ACP + VSB)

| File | Digest (12) | Instrument | Subject | Disposition / flags |
|---|---|---|---|---|
| `Review_ADV_COMP_VAL_SCOPE_BINDING.md` | `d847e1729f50` | **DeepSeek** (F5) | ACP v0.2 + VSB v0.1 | Consumed. **False self-label**: frontmatter claims "Grader: Claude … different-session"; all ACP §8 provenance tags wrong as written; true independence class cross-model. Operator-anchored via exact-match re-supply. File retains the false frontmatter internally — this manifest row and the classification report are the corrections of record |
| `VALUATION_ACP_COMPANION_ADVERSARIAL_REVIEW.md` | `fee506c693a8` | OpenAI (F1) | ACP v0.2 + VSB v0.1 | Consumed |
| `Companion_Subset_Adversarial_Review.docx` | `1d0569e1bf04` | Grok (F2) | ACP v0.2 + VSB v0.1 | Consumed |
| `Adversarial_Review_Companion_Subset.pdf` | `53f9a08ba035` | Gemini (F3) | ACP v0.2 + VSB v0.1 | Consumed |
| `VSB_ACP_ABSORPTION_REVIEW_FINDINGS.md` | `013f4aa6b48c` | Claude (CL) | VSB v0.2 + ACP v0.3 (absorption round; F-A1…F-A5) | Consumed. Second-order pass; self-discloses author-adjacent, uncalibrated. Its instrument-class ledger is flagged for re-annotation after the F5 reclassification |
| `COPILOT_REVIEW_TRANSCRIPT…` (pass 2) | `88c3a4a59440` | Copilot (F6) | Mixed: whitepaper excerpt + ACP v0.2 + VSB v0.1 | **Excluded** from absorption; preserved. Fabricated grader roster (lists operator as human grader), false cross-substrate claim, self-declared "binding" verdict |

## Set D: Magistracy / emergence

| File | Digest (12) | Instrument | Subject | Disposition / flags |
|---|---|---|---|---|
| `MAGISTRACY_REVIEW_FINDINGS.md` | `77dcc408c5ce` | Claude (CL) | MAGISTRACY_PATTERN v0.3 + emergence analysis v0.1 (F1–F12) | Consumed |
| `MAGISTRACY_ADVERSARIAL_REVIEW_COMPREHENSIVE.md` | `ad6adb9a649f` | OpenAI (F1) | MAGISTRACY_PATTERN v0.4 + emergence v0.1/v0.2 + ACP + VERSIONS manifest | Consumed. Also a second-pass external input to Set C; counted once here |

## Set E: Resolvable/Resolved-Reference Register (RRR)

| File | Digest (12) | Instrument | Subject | Disposition / flags |
|---|---|---|---|---|
| `RRR_v0_1_INDEPENDENT_GRADE.md` | `2cc0c041d2cd` | Claude (CL, I-C2) | RRR v0.1 (findings RRR-1…10) | Consumed |
| `RRR_COVER_NOTE.md` | `11fc55e922dd` | Claude (CL, I-C2) | Transmittal of the I-C2 grade | Meta-artifact (not a review pass) |
| `RESOLVED_REFERENCE_REGISTER_v0_1_adversarial_review.md` | `3fe96d873f81` | OpenAI (F1 = I-X1) | RRR v0.1 (15 sections) | Consumed. Source of the DV-1 overturn of the fourth-plane claim |
| `Resolved_Reference_Register_Adversarial_Review.docx` | `de03c079a50b` | Grok (F2 = I-X2) | RRR v0.1 (9 sections) | Consumed |
| `RRR_MULTI_INSTRUMENT_SUMMATION.md` | `30a41327eb24` | Claude (CL, I-C3) | Full RRR review stack (ledger + findings RRR-11…17) | Consumed as one pass + ledger meta-function; self-discloses compiler correlation |

---

## 3. Roll-up

**22 corpus artifacts** (21 files in the upload set + the preserved Copilot transcript) · **22 evidenced review passes** — 20 consumed, 2 preserved-but-excluded (both Copilot) · **6 instruments**, every fingerprint family operator-anchored: F1/OpenAI (rc8 review), F2/Grok (repo-informed feedback), F3/Gemini (repo audit), F4/OpenAI (RC9 review), F5/DeepSeek (re-supply match), F6/Copilot (paste), CL/Claude (self-declared + corpus-internal corroboration).

**Standing corrections this manifest carries:** (1) `Review_ADV_COMP_VAL_SCOPE_BINDING.md` is DeepSeek regardless of its internal Claude frontmatter — the digest `d847e1729f50…` binds that correction to the exact bytes; if a wrapped copy with a corrected header is ever cut, it enrolls as a new digest with lineage to this one. (2) The two Copilot passes are excluded from all consumption counts. (3) The absorption round's instrument-class ledger predates the F5 reclassification and awaits re-annotation.

## 3a. Source-session register (operator-supplied 2026-08-15)

The originating chat sessions for each external instrument, recorded at the vendor level. Per the digest/anchor law these URLs **locate** — they are account-gated and resolvable only by the operator, so they strengthen each anchor's *recoverability* (the origin context can be re-opened, re-exported, or re-verified by the accountable party) without changing its attestational class. Per-artifact session mapping is not asserted: each link is the vendor's review session; individual artifacts attribute to vendors via the anchors in §2.

| Instrument | Source session |
|---|---|
| OpenAI (F1, F4) | `https://chatgpt.com/c/6a7dc839-9994-83ea-a212-ed6b6849432f` |
| Gemini (F3) | `https://gemini.google.com/app/e6914d4eda65ddbb` |
| Grok (F2) | `https://grok.com/c/dc513d14-96bc-4ccd-84fd-c88a3ce81f7f?rid=f06889b6-5636-483b-8409-485922c2ed81` |
| Copilot (F6) | `https://copilot.microsoft.com/chats/utLEwUq4vrNh5r2b7k9GY` — origin of the preserved transcript (artifact #21) |
| DeepSeek (F5) | `https://chat.deepseek.com/a/chat/s/0455e437-8e06-4514-8354-6c821b2bd51d` — origin of `Review_ADV_COMP_VAL_SCOPE_BINDING.md`; names the true source behind that artifact's false Claude self-label |

Claude-family sessions are indexed separately in SESSION_INDEX v0.2 (Architect / Author / Archivist / Researcher UUIDs).

## 4. Verification procedure

To verify any file against this manifest: compute `sha256sum <file>` and compare against §5. To verify the classification deliverables' version integrity: the canonical's digest must equal the highest-numbered instance's digest. A canonical that diverges from its newest instance means an unpinned edit occurred — pin or revert before consuming.

## 5. Full-digest register

```
53f9a08ba0351bd4529c218dc8ea4357781b1b6870f0c7e7101c8e440f6acb31  Adversarial_Review_Companion_Subset.pdf
1d0569e1bf04b68c61d728a011c6b17d4933d3da75563b592e45d5fab574a549  Companion_Subset_Adversarial_Review.docx
ad6adb9a649fbe932514327dc81f6f81e348c870997b53691bd39eee76530430  MAGISTRACY_ADVERSARIAL_REVIEW_COMPREHENSIVE.md
77dcc408c5cefd2bb9598d8f05d02a2899a79b6ef57ed8760f9b9e1c1b8cd9e0  MAGISTRACY_REVIEW_FINDINGS.md
717eb959ea3be8e59f262512a13ff2f5a03c07864d0f6c2e5dd97ad362d51907  REPUBLIC_RC9_REPOSITORY_GROUNDED_ADVERSARIAL_REVIEW.docx
83bbcc3da2b375beceb51108a70120c787f79c1d617f8fea445ac1dd01877852  REPUBLIC_v1_0-rc7_critical_review.md
4d177616964217a08d6eff2c1c22b5cf85a12c16ee5a7b5de994e4d854b042cc  REPUBLIC_v1_0-rc8_ADVERSARIAL_REVIEW.md
3fe96d873f81beafed8c85acbd76995c1936bee1da6faf220cac248dda2af99c  RESOLVED_REFERENCE_REGISTER_v0_1_adversarial_review.md
11fc55e922ddd045646cc28d7ecaceed80419ec2ccd5037b67531ed358c9d07c  RRR_COVER_NOTE.md
30a41327eb24b1ffdb25fcad934e0f1d80de7c0445bec5e64d910bc655caa7cd  RRR_MULTI_INSTRUMENT_SUMMATION.md
2cc0c041d2cd40bd1cdbdf604301bcc6498f3fd246bf417da0edbf4b9e514764  RRR_v0_1_INDEPENDENT_GRADE.md
4b5cf2c4e3280875da24e42d90f09f1f1a09e81890d36c1d1b079975ce9a20f2  Republic_Repo_Informed_Feedback.docx
8eed26239c2e851eab937851c7dc7ae5360c8ff66666fb828224f7dca20e43c1  Republic_Whitepaper_Critical_Analysis.docx
c538ecf1d4b6eedb4b74807280394250502a5fcb1ec6bf95fc1c8e60a9c15d22  Republic_Whitepaper_rc8_Adversarial_Review.docx
de03c079a50bbb956137abd37fceea4e745593447a7d84ed37d897d6cfb519c3  Resolved_Reference_Register_Adversarial_Review.docx
d847e1729f509c33f635085412ee5ba0165957ea71e98414866cd143ef47321d  Review_ADV_COMP_VAL_SCOPE_BINDING.md
fee506c693a8fe9faae005db02d8ff7891876681a9371abcad7c5323e8d76a7a  VALUATION_ACP_COMPANION_ADVERSARIAL_REVIEW.md
013f4aa6b48ca12afbc47e662bba40a11af9a6a477aac63c2407dc6cff8ecedf  VSB_ACP_ABSORPTION_REVIEW_FINDINGS.md
85d55e4b84b31738f5eb4edfbe5dd28d5098c3e1ae38b0df0cd61421817543e2  adversarial_review_republic.pdf
302a01c28cefcaf013bf5dc45a627d2485a93ff4971c509600a0e30584565480  repository_audit_republic.pdf
27737ec52ea562b8ffbd6bca484b87d22ae60b8b76b32fd148289ae9ed31f1ad  republic_critical_analysis.pdf
88c3a4a594403ef6d5d0fb111004fbcbf9619e0f2698eb453ffc239f566e118e  COPILOT_REVIEW_TRANSCRIPT_2026-08-13_14.md
f51d8af1a1d1b681888478642a4e6180c9071b8a4c855d6ddb9e95b608d70a54  ADVERSARIAL_REVIEW_CORPUS_CLASSIFICATION.md
f51d8af1a1d1b681888478642a4e6180c9071b8a4c855d6ddb9e95b608d70a54  ADVERSARIAL_REVIEW_CORPUS_CLASSIFICATION_v1.5.1.md
72bf04ccdd051b171cc6915acded18d8ef7434fba21f82debb3a04e9ba80f1df  DIGEST_ANCHOR_VERIFICATION.md
72bf04ccdd051b171cc6915acded18d8ef7434fba21f82debb3a04e9ba80f1df  DIGEST_ANCHOR_VERIFICATION_v0.1.md
```

## Change log
- **2026-08-15 v1.2** — source-session register added (§3a): operator-supplied origin links for all five external instruments, recorded as vendor-level anchor-recoverability data. DeepSeek and Copilot origins now bind their respective correction records to named sessions. Instance `_v1.2` pinned at cut.
- **2026-08-15 v1.1** — `DIGEST_ANCHOR_VERIFICATION.md` v0.1 enrolled (canonical + pinned instance) as the pattern formalizing the integrity law this manifest runs. Instance `_v1.1` pinned at cut.
- **2026-08-15 v1.0** — initial manifest. 22 corpus artifacts + 3 deliverables inventoried with SHA-256 identity; all six instrument families operator-anchored; standing corrections (F5 false self-label, Copilot exclusions, absorption-ledger re-annotation) recorded as manifest-carried facts. Instance `_v1.0` pinned at cut.
