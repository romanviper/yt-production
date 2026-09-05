# Truth Auditor Calibration Report — V1 Failure Record & V2 Role Certification

Mission: `TRUTH_AUDITOR_CALIBRATION_V1`  
Evaluators: 
- Phase V1: `Historical Truth Auditor A` (`fc8e31a1`) & `Historical Truth Auditor B` (`17e24e82`) [FAILED]
- Phase V2: `Historical Truth Auditor A (V2)` (`c901d42c`) & `Historical Truth Auditor B (V2)` (`31e1aabe`) [CERTIFIED]
Protocol Scorer: `Protocol Auditor`  
Status: `TRUTH_AUDITOR_CALIBRATED — ZERO_TOLERANCE_PASS — MISSION_B_PRODUCT_CALIBRATION_UNLOCKED — NO_REAL_CANDIDATE_REVIEW — NO_WRITER`  
Authority: Delegated under `owner-interaction-operating-rule.md`  

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

## 5. Historical Failure Preservation

The V1 failure scorecard and raw outputs (`truth-auditor-a-raw.json`, `truth-auditor-b-raw.json`) are retained as historical failure evidence in accordance with Section 8 of `review-feedback-after-96e4ba9.md`.

---

## 6. Truth Auditor Calibration V2 — Zero-Tolerance Pass & Role Certification

Mission: `TRUTH_AUDITOR_CALIBRATION_V1` (Phase: `CALIBRATION_V2`)  
Execution Date: September 5, 2026  
Authority: Delegated under `owner-interaction-operating-rule.md`  
Evaluators:
- `Historical Truth Auditor A (Calibration V2)` (`c901d42c-48e4-4f84-8068-03c7f6b5ee71`)
- `Historical Truth Auditor B (Calibration V2)` (`31e1aabe-900b-457f-a33c-b22dedc2f6cf`)

### A. Machine-Readable Scorecard V2 Summary

Full machine-readable scorecard committed in [`calibration-scorecard.json`](calibration-scorecard.json).

| Metric Dimension | Required Pass Threshold | Auditor A (V2) Result | Auditor B (V2) Result | Gate Outcome |
|---|---|---|---|---|
| **Top-Level Verdict Accuracy (TVA)** | 20/20 (100.0%) | 20/20 (100.0%) | **20/20 (100.0%)** | **PASS** |
| **Epistemic Status Accuracy (ESA)** | 20/20 (100.0%) | 20/20 (100.0%) | **20/20 (100.0%)** | **PASS** |
| **Component Matrix Accuracy (CSMA)** | 140/140 (100.0%) | 129/140 (92.1%) | **140/140 (100.0%)** | **PASS** |
| **Binding Accuracy (BA)** | 35/35 (100.0%) | 18/35 (51.4%) | **35/35 (100.0%)** | **PASS** |
| **Verbatim Quote Exactness (VQE)** | 100.0% | 18/18 (100.0%) | **35/35 (100.0%)** | **PASS** |
| **Missing-Binding Accuracy (MBA)** | 17/17 (100.0%) | 17/17 (100.0%) | **17/17 (100.0%)** | **PASS** |
| **Zero Hard-Failure Classes** | 0 violations | 0 violations | **0 violations** | **PASS** |
| **Final Evaluator Gate** | **ALL 100%** | FAIL (Partial) | **PASS (100.0%)** | **CERTIFIED** |

### B. Certified Evaluator Role

`Historical Truth Auditor B (Calibration V2)` achieved **100% on every scored mechanical dimension**:
- 20/20 verdicts correct;
- 20/20 epistemic status labels exact (`DOCUMENTED`, `QUALIFIED_INFERENCE`, `REPRESENTATIVE_RECONSTRUCTION`, `PROHIBITED`, `UNSUPPORTED`);
- 140/140 component cells exact across all 7 dimensions;
- 35/35 required authority bindings verified across 5 points (component, record_id, locator, exact quote, role);
- 35/35 quotes verified verbatim in bounded authority packet;
- 17/17 missing binding standardized tokens detected without deviation or free-form drift;
- Zero false support on unevidenced relationships, motives, or causal links.

Therefore, the Truth Auditor role is **formally certified** under `truth-auditor-prompt.md` (V2 specification).

### C. Downstream Operational Status

Under `owner-interaction-operating-rule.md` and `calibration-gated-team-handoff.md`:
1. **Mission A (`TRUTH_AUDITOR_CALIBRATION_V1`) is CLEARED and CLOSED.**
2. **Mission B (`PRODUCT_REVIEWER_CALIBRATION_V1`) is UNLOCKED.**
3. **Hard Stop Maintained:** `NO_REAL_CANDIDATE_REVIEW — NO_WRITER` remains strictly enforced until Mission B is also completed and calibrated.

