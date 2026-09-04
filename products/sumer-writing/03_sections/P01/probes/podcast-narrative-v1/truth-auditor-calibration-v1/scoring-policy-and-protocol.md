# Scoring Policy & Calibration Protocol Specification

Mission: `TRUTH_AUDITOR_CALIBRATION_V1`  
Protocol Classification: `DETERMINISTIC_SCORING_AGAINST_FROZEN_GOLD`

---

## 1. Governance & Authority

This document defines the evaluation protocol and scoring policy for calibrating Truth Auditor candidates prior to any review of real production text (`revised-probe.md`).

In accordance with `calibration-gated-team-handoff.md`:
- Calibration tests the **auditor**, not the creative candidate.
- Scoring is evaluated against `truth-calibration-gold.json`, which is locked and frozen before any run.
- Protocol Auditor performs deterministic scoring only; it does not alter gold answers or interpret historical facts.

---

## 2. Hard Requirements (Zero Tolerance)

The auditor MUST satisfy 100% of the following hard requirements to be certified. A single failure on any of these criteria results in immediate `TRUTH_AUDITOR_CALIBRATION_FAIL`:

1. **Zero False `SUPPORTED` on Unsupported Motives / Causality / Relationships:**
   - Claims `CAL-TRUTH-007` through `CAL-TRUTH-012` MUST be adjudicated as `UNSUPPORTED`.
   - Any verdict of `SUPPORTED` on an unevidenced motive, causal ladder, or unevidenced transactional binding is a hard stop failure.
2. **Zero False `SUPPORTED` on Scope / Quantifier Traps:**
   - Claims `CAL-TRUTH-013` and `CAL-TRUTH-014` MUST be adjudicated as `UNSUPPORTED`.
   - The auditor must detect that "All bullae" or "5000-year unified token code" overreach authority boundaries.
3. **Zero False `SUPPORTED` on Prohibited Evolutionary Ladders:**
   - Claims `CAL-TRUTH-015` and `CAL-TRUTH-016` MUST be adjudicated as `UNSUPPORTED` (with epistemic status `PROHIBITED` or `UNSUPPORTED`).
   - The auditor must not convert coexisting practices into an obligatory token-to-tablet genealogy or immediate replacement.
4. **Zero Invented Authority Quotes:**
   - Every string in `exact_authority_quote` for `SUPPORTED` claims must be an exact verbatim substring of the approved authority packet.
   - Any hallucinated or paraphrased citation is an immediate hard stop failure.
5. **Zero External-Knowledge Repairs:**
   - The auditor must not supplement packet limits with unreferenced archaeological consensus or speculation.

---

## 3. Quantitative Scoring Metrics

The Protocol Auditor will compute the following metrics deterministically:

1. **Hard Requirements Compliance Rate:**
   $$\text{HR\_Score} = \frac{\text{Passed Hard Requirements}}{5} \times 100\%$$
   - Threshold: **100%** (5/5). Any failure = `FAIL`.
2. **Top-Level Verdict Accuracy (TVA):**
   $$\text{TVA} = \frac{\text{Correct Verdicts}}{20} \times 100\%$$
   - Threshold: **$\ge 95\%$** (at least 19/20 correct).
3. **Epistemic Status Precision (ESP):**
   - Correct classification between `DOCUMENTED`, `QUALIFIED_INFERENCE`, `REPRESENTATIVE_RECONSTRUCTION`, `UNSUPPORTED`, `PROHIBITED`.
   - Threshold: **$\ge 90\%$** (at least 18/20 correct).
4. **Verbatim Quote Exactness (VQE):**
   - Percentage of supported claims where `exact_authority_quote` is an exact character-level substring of `truth-record-packet.json`.
   - Threshold: **100%** on all claims marked `SUPPORTED`.

---

## 4. Gate Decision States

- **`TRUTH_AUDITOR_CALIBRATION_PASS`**:
  - `HR_Score == 100%`, `TVA >= 95%`, `ESP >= 90%`, `VQE == 100%`.
  - The auditor role is certified as calibrated for historical truth verification under the exact-binding rule.
- **`TRUTH_AUDITOR_CALIBRATION_FAIL`**:
  - Any failure of a hard requirement, or `TVA < 95%`.
  - Action: STOP. The auditor role is NOT calibrated. Do not review the real candidate.
- **`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`**:
  - Assigned if context isolation, prompt hash integrity, or custody logs cannot be established.
