# Product Reviewer Calibration Scoring Policy & Protocol Specification

Mission: `PRODUCT_REVIEWER_CALIBRATION_V1`  
Protocol classification: `DETERMINISTIC_AND_RUBRIC_SCORING_UNDER_DELEGATED_AUTHORITY`  
Status: `ACTIVE_CALIBRATION_PROTOCOL_V1 — DELEGATED_INTERNAL_GATE`

---

## 1. Purpose & Standards

This calibration certifies whether a Product Quality Reviewer can evaluate the text actually present without laundering explanatory essays into stories, confusing physical catalogues with narrative movement, or rewarding invented melodrama.

Certification requires **100% agreement on core diagnostic dimensions**:

1. **Passage Verdict Accuracy (PVA):** 4/4 (100.0%) matching expected top-level verdicts.
2. **Mode Classification Accuracy (MCA):** 4/4 (100.0%) matching mode enum (`EXPLANATORY_ESSAY`, `INVENTED_CAUSAL_DRAMA`, `STATIC_CATALOGUE`, `GENUINE_NARRATIVE_MOVEMENT`).
3. **Carrier Detection Accuracy (CDA):** 4/4 (100.0%) matching carrier status.
4. **Question Progression Accuracy (QPA):** 4/4 (100.0%) matching question status.
5. **Reviewer-Added Interpretation Tagging:** Zero unacknowledged reviewer-added narrative bridges.
6. **Zero Truth Authority Violations:** Reviewer does not issue factual truth certifications.

A single diagnostic failure on these hard categories returns:
`PRODUCT_REVIEWER_CALIBRATION_FAIL`
and stops downstream execution.
