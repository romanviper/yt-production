# Phase 1 Evaluation Artifacts

The JSON files in this directory that were created in commit `2929c16bbd615dc512749bd6a9ef4c5941c39c06` are **development annotations from the superseded v1.0 benchmark**.

They are retained only for implementation history. They are NOT:

- owner/human gold labels;
- valid v1.1 Product-review outputs;
- truth authority;
- calibration evidence;
- Phase 1 exit evidence.

Known contamination includes descriptive sample roles, prior expectations, absolute `GOOD/WEAK/FAIL` scoring, and reuse of legacy Truth conclusions. The active v1.1 calibration state is tracked in `benchmarks/p01/owner-calibration.json` and future v1.1 evaluation outputs must conform to `schemas/output-quality.schema.json`.

Do not feed these legacy files to Product reviewers.
