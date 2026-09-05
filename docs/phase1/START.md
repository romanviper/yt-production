# Phase 1 — Output Benchmark & Measurement Contract

Status: **ACTIVE IMPROVEMENT LOOP**  
Canonical production branch: `main`  
Active Phase 1 implementation branch: `codex/p01-phase1-benchmark`

This is the single active entrypoint for the Observable Learning Architecture work.
Read `docs/architecture/observable-learning-architecture-plan.md` before making
Phase 1 changes.

For the current benchmark work, read in this order:

1. `docs/phase1/WORKER-LOOP.md`
2. `benchmarks/p01/iterations/iteration-01.json` — closed first improvement iteration
3. `docs/phase1/ITERATION-02-WORK-ORDER.md` — current narrow measurement-lane fix
4. `schemas/phase1-worker-iteration.schema.json`

Iteration 02 MUST publish `benchmarks/p01/iterations/iteration-02.json` with separate
`process` and `output` sections before returning the branch for review.

## Objective

Build a benchmark that can identify *what is wrong in an output* using observable
prose evidence before attempting to diagnose which upstream agent or module caused
it. The benchmark is the root of the future trace tree.

Phase 1 does **not** improve Writer prompts, create a new production draft, extend
legacy experiments, redesign the production router, or build a generic white-box
runtime.

## Repository readiness after cleanup

- `main` is the only canonical production branch.
- `codex/p01-phase1-benchmark` is a bounded implementation/review branch for Phase 1 only.
- Production router state for `products/sumer-writing` is idle; do not create a production task for benchmark work.
- Legacy experiment scripts/runs and historical product tasks are immutable evidence, not active work.
- No new Writer round is authorized until the Phase 1 benchmark passes the required calibration gates.

## Phase 1 measurement lanes

The active contract separates three independent evaluator lanes:

1. **Truth / scope gate** — one sample + approved P01 historical authority only; output uses `schemas/truth-gate.schema.json`.
2. **Product pairwise preference** — anonymized A/B prose + Product criteria only; output uses `schemas/output-quality.schema.json`.
3. **Target-gap analysis** — starts only after Product preference is frozen and may then use function-matched `CRAFT_ONLY` references; output uses `schemas/target-gap.schema.json`.

Do not mix these inputs or outputs into one reviewer context.

## Phase 1 checkpoint artifacts

The measurement layer includes or evolves:

1. `docs/quality/output-quality-contract.md`
2. `schemas/output-quality.schema.json`
3. `schemas/truth-gate.schema.json`
4. `schemas/target-gap.schema.json`
5. `benchmarks/p01/benchmark-set.json`
6. `benchmarks/p01/source-manifest.json`
7. `benchmarks/p01/craft-corpus.json`
8. `docs/quality/product-trial-protocol.md`
9. `benchmarks/p01/owner-calibration.json`
10. Worker iteration records with `process` and `output`

Do not write new candidate prose for this checkpoint.

## Calibration corpus

Use immutable existing material. Historical reviewer verdicts are hypotheses, not gold labels. Owner/human labels must be recorded only when actually supplied; do not infer them from filenames or historical commentary.

The current corpus is partitioned into DEV, CALIBRATION, and a fresh transfer sample. Because all files live in a shared repository, the current HOLDOUT reliability is explicitly `FRESH_EXPOSED_NOT_BLIND`, not a claim of sequestered blindness.

## Measurement invariants

Every retained Product criterion must:

- ask an observable question about the output;
- identify exact output spans supporting the judgment;
- separate observation from interpretation;
- preserve `UNCERTAIN` when evidence is insufficient;
- avoid scalar quality scores as the primary signal;
- avoid encoding one P01 solution path as the definition of good writing.

Exact quotation proves location, not semantic entailment.

## Black-box boundary

Product pairwise reviewers receive anonymized prose plus the frozen Product criteria only. They do NOT receive FoC references, Truth results, target-gap records, Planner/Writer/Worker process logs, intended winner, old verdicts, or diagnostic hypotheses.

Only after the Product preference is frozen may Target-gap review receive function-matched craft references.

The Worker `process` record exists for downstream audit after an output defect is observed. It is never evidence that an intended feature actually works.

## Exit gate

Do not move to Phase 2 until the Phase 1 exit criteria in `docs/architecture/observable-learning-architecture-plan.md` are satisfied, including owner-preference calibration and a fresh transfer check. Agent agreement or a structural verifier alone is insufficient for Phase 1 closure.

A Worker may legitimately stop at `READY_FOR_HUMAN_CALIBRATION`.

## Legacy warning

Do not execute the legacy FoC or writer-trace-v2 experiment scripts as active workflows. They remain only so their implementation and run artifacts can be audited and used as development evidence.
