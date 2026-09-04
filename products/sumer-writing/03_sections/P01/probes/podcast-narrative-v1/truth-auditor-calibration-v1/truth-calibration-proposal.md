# Planning Commander Proposal: Truth Auditor Calibration V1

To: **Product & System Owner**  
From: **Planning Commander**  
Date: 2026-09-04  
Mission: `TRUTH_AUDITOR_CALIBRATION_V1`  
Status: `PREPARE_TRUTH_CALIBRATION_FOR_OWNER_APPROVAL — NO_EXECUTION — NO_WRITER`

---

## 1. Executive Summary

In accordance with Section 4 and Section 11 of `calibration-gated-team-handoff.md`, this proposal submits the complete, frozen calibration packet for **Mission A: `TRUTH_AUDITOR_CALIBRATION_V1`** for explicit Owner review and approval.

The purpose of this mission is to calibrate the Truth Auditor role on an **owner-locked ground-truth test set of 20 atomic claims** before any real candidate review of `revised-probe.md` is permitted.

No auditor runs have been launched. Execution is strictly halted at this gate awaiting your sign-off.

---

## 2. Calibration Packet Structure

The calibration materials have been organized in products/sumer-writing/03_sections/P01/probes/podcast-narrative-v1/truth-auditor-calibration-v1/:

| File | Git Blob Hash | Size (Bytes) | Role / Purpose |
|---|---|---|---|
| [`truth-calibration-claims.json`](truth-calibration-claims.json) | `7d6838f5c512f27889fed3decd4cc2fa66c95135` | 4,796 | 20 test claims fixture (auditor input) |
| [`truth-calibration-gold.json`](truth-calibration-gold.json) | `e30414f1302a206c91d7a20ac08826169f33da30` | 21,225 | Frozen ground truth answers & quotes |
| [`truth-auditor-prompt.md`](truth-auditor-prompt.md) | `73627a9b281bf149c5423ea71fc59e52d546665a` | 4,379 | Auditor prompt & 15-field schema spec |
| [`scoring-policy-and-protocol.md`](scoring-policy-and-protocol.md) | `b5ba611e15ca5b46739a4b62423066869db32b69` | 3,833 | Scoring thresholds & hard stop rules |
| [`../product-reviewer-calibration-v1/README.md`](../product-reviewer-calibration-v1/README.md) | `d7de8f5d770ad99a4edfcb1d09a28336d8dca882` | 459 | Reserved directory placeholder |

## 3. Test Set Composition (20 Claims Across 10 Categories)

The 20 atomic claims are balanced 50/50 (10 `SUPPORTED`, 10 `UNSUPPORTED`) across the 10 deliberate trap categories specified in the handoff:

| Category ID | Category Name | Claim IDs | Target Failure Mode Tested | Expected Verdict |
|---|---|---|---|---|
| **Cat 1** | Direct Documented Fact | `CAL-TRUTH-001`, `CAL-TRUTH-002` | Tests baseline ability to recognize physical artifact features | `SUPPORTED` |
| **Cat 2** | Qualified Functional Inference | `CAL-TRUTH-003`, `CAL-TRUTH-004` | Tests recognition of licensed functional deductions | `SUPPORTED` |
| **Cat 3** | Allowed Representative Reconstruction | `CAL-TRUTH-005`, `CAL-TRUTH-006` | Tests recognition of permissible manufacturing workflows | `SUPPORTED` |
| **Cat 4** | Entity Correct, Relationship Unsupported | `CAL-TRUTH-007`, `CAL-TRUTH-008` | Prevents linking real artifacts/practices to unevidenced institutions/transactions | `UNSUPPORTED` |
| **Cat 5** | Entity Correct, Motive Unsupported | `CAL-TRUTH-009`, `CAL-TRUTH-010` | Prevents attributing fraud prevention or psychological motives | `UNSUPPORTED` |
| **Cat 6** | Plausible Causality, No Binding | `CAL-TRUTH-011`, `CAL-TRUTH-012` | Prevents inventing causal ladders (memory overload, breakability causing tablets) | `UNSUPPORTED` |
| **Cat 7** | Scope / Quantifier Overreach | `CAL-TRUTH-013`, `CAL-TRUTH-014` | Prevents generalizing "some" to "all", or universal codes | `UNSUPPORTED` |
| **Cat 8** | Coexistence Converted to Genealogy | `CAL-TRUTH-015`, `CAL-TRUTH-016` | Prevents mandatory 4-stage evolutionary ladders or immediate replacement | `UNSUPPORTED` |
| **Cat 9** | Exact Supported Negative Statement | `CAL-TRUTH-017`, `CAL-TRUTH-018` | Tests recognition that tokens/proto-cuneiform do NOT record spoken syntax | `SUPPORTED` |
| **Cat 10** | Inference with Visible Epistemic Status | `CAL-TRUTH-019`, `CAL-TRUTH-020` | Tests tagging reed-tool inferences and macro shifts as qualified inferences | `SUPPORTED` |

---

## 4. Exact-Binding Verification

Every single quote in `truth-calibration-gold.json` has been programmatically verified as a **100% exact substring** of `products/sumer-writing/03_sections/P01/probes/podcast-narrative-v1/planning-agents-team-v1/truth-record-packet.json`.

There are zero paraphrased quotes, zero external archaeological assumptions, and zero ambiguous locators.

---

## 5. Proposed Execution Plan (Post-Owner Approval)

Once Owner approval is granted:
1. **Launch Sibling Auditors (A & B):**
   - Launch Truth Auditor A and Truth Auditor B as independent, fresh subagents.
   - Supply only: `truth-calibration-claims.json`, `truth-auditor-prompt.md`, `truth-record-packet.json`, `notebook-authority.md`, and `writer-notebook.md`.
   - Withhold `truth-calibration-gold.json` and any prior evaluation logs.
2. **Protocol Auditor Scoring:**
   - Protocol Auditor deterministically evaluates raw outputs against `truth-calibration-gold.json` and computes scores against `scoring-policy-and-protocol.md`.
3. **Commander Gate Matrix:**
   - Commander records outcomes and returns the calibration matrix to Owner.

---

## 6. Action Requested from Owner

Please review the proposed materials and indicate your decision:
1. **Approve:** Authorize `TRUTH_AUDITOR_CALIBRATION_V1` execution with the proposed packet, gold answers, prompt, and scoring policy.
2. **Modify:** Request specific edits to claims, gold rationales, or thresholds.
3. **Reject:** Return with blocking feedback.

Status remains: `PREPARE_TRUTH_CALIBRATION_FOR_OWNER_APPROVAL — NO_EXECUTION — NO_WRITER`.
