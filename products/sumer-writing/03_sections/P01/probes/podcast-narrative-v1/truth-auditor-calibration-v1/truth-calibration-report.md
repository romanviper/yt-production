# Truth Auditor Calibration V1 — Failure Record & Supersession Report

Mission: `TRUTH_AUDITOR_CALIBRATION_V1`  
Evaluators: `Historical Truth Auditor A` (`fc8e31a1`) & `Historical Truth Auditor B` (`17e24e82`)  
Protocol Scorer: `Protocol Auditor`  
Status: `TRUTH_AUDITOR_CALIBRATION_V1 — CONTENT_GATE_FAIL — PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE — CALIBRATION_NOT_PROVEN — NO_PRODUCT_CALIBRATION — NO_REAL_CANDIDATE_REVIEW — NO_WRITER`  
Supersession Target: Commit `96e4ba9ca9e50250f1d997276d1b49b2a6cbd846`  
Feedback Directive: Commit `f9677b9ddf803fd53802b4018ca428a7f767ef00` (`review-feedback-after-96e4ba9.md`)

---

## 1. Formal Supersession Notice

The passing status previously reported in commit `96e4ba9` (`TRUTH_AUDITOR_CALIBRATED — ZERO_FALSE_PASSES — READY_FOR_PRODUCT_CALIBRATION`) is hereby **formally superseded and declared invalid**.

Under the frozen zero-tolerance calibration policy established in `scoring-policy-and-protocol.md`:
- Certification requires **100% correctness on every scored dimension** (TVA, ESA, CSMA, BA, VQE, MBA, PROCESS_VALID).
- Sibling agreement ($A == B$) does not override gold failure.
- Both Auditor A and Auditor B failed hard requirements on Epistemic Status Accuracy, Component Support Matrix Accuracy, Binding Accuracy, and deterministic Missing-Binding scoring.

The calibration result cannot be used to certify the Truth Auditor role, to begin Product Reviewer calibration, to review the real candidate `revised-probe.md`, or to authorize Writer execution.

---

## 2. Machine-Readable Scorecard Summary

The full cell-by-cell machine-readable scorecard is committed in [`calibration-scorecard.json`](calibration-scorecard.json).

| Metric Dimension | Required Pass Threshold | Auditor A Result | Auditor B Result | Gate Outcome |
|---|---|---|---|---|
| **Top-Level Verdict Accuracy (TVA)** | 20/20 (100.0%) | 20/20 (100.0%) | 20/20 (100.0%) | PASS |
| **Epistemic Status Accuracy (ESA)** | 20/20 (100.0%) | 17/20 (85.0%) | 18/20 (90.0%) | **FAIL** |
| **Component Matrix Accuracy (CSMA)** | 140/140 (100.0%) | 125/140 (89.3%) | 131/140 (93.6%) | **FAIL** |
| **Binding Accuracy (BA)** | 35/35 (100.0%) | 15/35 (42.9%) | 22/35 (62.9%) | **FAIL** |
| **Verbatim Quote Exactness (VQE)** | 100.0% | 21/21 (100.0%) | 21/21 (100.0%) | PASS |
| **Missing-Binding Accuracy (MBA)** | 100.0% (Deterministic) | Non-auditable free-form | Non-auditable free-form | **FAIL** |
| **Process Gate** | `PROCESS_VALID` | Platform limits | Platform limits | **PROCESS_BLOCKED** |
| **Overall Calibration Outcome** | **ALL 100%** | **FAIL** | **FAIL** | **CALIBRATION_FAIL** |

---

## 3. Specific Failure Diagnoses

### A. Epistemic Status Failures (ESA)
- `CAL-TRUTH-007`: Gold requires `UNSUPPORTED`; both auditors returned `PROHIBITED`.
- `CAL-TRUTH-013`: Gold requires `UNSUPPORTED`; both auditors returned `PROHIBITED`.
- `CAL-TRUTH-010`: Auditor A returned `UNSUPPORTED` against gold `PROHIBITED`.

### B. Component Support Matrix Failures (CSMA)
- Over-assignment of `UNSUPPORTED` on unasserted components:
  - Auditor A marked `causality = UNSUPPORTED` on `CAL-TRUTH-010` (gold `N/A`).
  - Auditor A marked `relationship = UNSUPPORTED`, `sequence = UNSUPPORTED` on `CAL-TRUTH-011` (gold `N/A`).
  - Auditor A marked `relationship = UNSUPPORTED`, `motive = UNSUPPORTED` on `CAL-TRUTH-012` (gold `N/A`).
  - Auditor A marked `function = SUPPORTED` on `CAL-TRUTH-013` (gold `N/A`).
  - Auditor B marked `motive = UNSUPPORTED` on `CAL-TRUTH-008` (gold `N/A`).
  - Auditor B marked `causality = UNSUPPORTED` on `CAL-TRUTH-010` (gold `N/A`).
  - Auditor B marked `relationship = UNSUPPORTED`, `function = N/A` on `CAL-TRUTH-014` (gold `relationship = N/A`, `function = UNSUPPORTED`).

### C. Binding Accuracy Failures (BA)
- Raw answers omitted multiple required gold bindings:
  - `CAL-TRUTH-007`: Omitted support bindings for attested entities OIM A64678 and ChM III-937a.
  - `CAL-TRUTH-008`: Omitted function/relationship `LIMITS` bindings from `P01-MAT-0003`.
  - `CAL-TRUTH-009`: Provided only one motive rejection binding instead of statement and qualification.
  - `CAL-TRUTH-012`: Omitted supported breakability function and coexistence rejection bindings.

### D. Missing-Binding Non-Determinism (MBA)
- Gold expected standardized tokens (`same_transaction_relationship`, `fraud_prevention_motive`, `urban_growth_to_memory_failure`).
- Auditors returned free-form natural language strings.
- Without a pre-frozen normalization mapping, scoring this as 100% was an unverified semantic judgment.

### E. Process Gate Status
- Because OS-level process virtualization is unavailable and runtime prompt hashes/tool lineage were not committed alongside raw outputs:
  $$\text{PROCESS\_BLOCKED — INDEPENDENCE\_UNAVAILABLE}$$

---

## 4. Retraction of Overclaims

The claim in commit `96e4ba9` that the exact-binding rule "completely eliminate[s] the correlated false pass failure mode" is retracted. A 20-claim calibration run tests only bounded performance on that specific fixture; it does not authorize general reliability assertions about model behavior.

---

## 5. Next Internal Corrective Steps

In accordance with Section 8 of `review-feedback-after-96e4ba9.md`:
1. This run is preserved as failure evidence.
2. The team will harmonize the auditor schema and gold definitions internally:
   - Provide standard missing-binding enum tokens or deterministic matching rules.
   - Clarify component assignment boundaries (when an unasserted component must be `N/A` rather than `UNSUPPORTED`).
   - Align epistemic status criteria (`PROHIBITED` vs `UNSUPPORTED`).
3. Maintain hard boundary: `NO_PRODUCT_CALIBRATION`, `NO_REAL_CANDIDATE_REVIEW`, `NO_WRITER`.
4. Work proceeds internally toward a valid, calibrated system without surfacing intermediate process debris to the owner.
