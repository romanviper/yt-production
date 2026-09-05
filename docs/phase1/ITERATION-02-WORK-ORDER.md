# Phase 1 Improvement Iteration 02 — Work Order

Status: **READY / NARROW FIX**

## Triggering output defects

Independent review of Iteration 01 output found two coupled measurement defects:

1. Product pairwise review still permits function-matched FoC references before preference is frozen. This can bias the reviewer toward FoC similarity instead of judging whether A or B works better as the product.
2. `schemas/output-quality.schema.json` mixes absolute truth gates, pairwise craft preference, defects and target-gap comparison in one record. A pair-level gate cannot cleanly identify whether A or B failed, and a single reviewer object encourages measurement leakage between independent questions.

## Root-cause region from Iteration 01 process

Inspecting Iteration 01 process after the output defect was found points to a packaging mistake across decisions D01/D04/D09: the design separated concepts semantically but still represented them as one evaluator-facing record.

## Required change

Split Phase 1 measurement into three independent lanes:

### Lane A — Truth / scope gate

Input:
- one sample;
- approved P01 historical authority only.

Output:
- per-sample gate/claim audit.

Must not receive FoC craft references or Product preference.

### Lane B — Product pairwise preference

Input:
- anonymized Sample A and Sample B;
- frozen Product Quality Contract criteria only.

Output:
- A/B/TIE/UNCERTAIN per criterion;
- exact spans;
- observation vs interpretation;
- optional span-grounded craft defects;
- output-only failure signature.

Must NOT receive FoC reference excerpts, Truth reviewer results, process logs, new/old labels, or target-gap hypotheses before preference is frozen.

### Lane C — Target-gap analysis

Input only after Lane B result is frozen:
- selected sample/passage;
- function-matched `CRAFT_ONLY` reference excerpt(s);
- target-gap contract.

Output:
- exact candidate/reference span differences;
- specific remaining gaps and retained strengths;
- medium limitation.

It must not change or retroactively justify Lane B preference.

## Schema requirements

Keep `schemas/output-quality.schema.json` as the Product pairwise output schema only.

Add:
- `schemas/truth-gate.schema.json`
- `schemas/target-gap.schema.json`

Remove from Product pairwise schema:
- `absolute_gates`
- required `target_gap`
- `SINGLE_DIAGNOSTIC` mode if it cannot satisfy pairwise invariants cleanly.

Product pairwise schema must require both opaque sample IDs A/B.

## Holdout reliability wording

The repository cannot enforce true secrecy for a file present in the shared repo. Keep the HOLDOUT partition, but explicitly label its current reliability as `FRESH_EXPOSED_NOT_BLIND` (or equivalent) until access is actually sequestered. Do not claim a blind holdout merely because the rubric author did not open the file.

## Verifier changes

The verifier must check:
- three measurement schemas exist;
- Product protocol explicitly forbids craft references before pairwise preference is frozen;
- Product pairwise schema contains no truth-gate or target-gap fields;
- Truth schema cannot accept craft reference authority;
- target-gap schema identifies `CRAFT_ONLY` references and function match;
- holdout reliability limitation is explicit;
- missing owner calibration still prevents Phase 1 closure.

## Required iteration record

Publish `benchmarks/p01/iterations/iteration-02.json` using the Worker iteration schema with separate `process` and `output`.

Stop after this narrow separation. Do not start owner scoring or a Writer round in this iteration.
