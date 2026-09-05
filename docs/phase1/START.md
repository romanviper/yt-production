# Phase 1 — Output Benchmark & Measurement Contract

Status: **ACTIVE IMPROVEMENT LOOP**  
Canonical production branch: `main`  
Active Phase 1 implementation branch: `codex/p01-phase1-benchmark`

This is the single active entrypoint for the Observable Learning Architecture work.
Read `docs/architecture/observable-learning-architecture-plan.md` before making
Phase 1 changes.

For the current benchmark-improvement iteration, also read in this order:

1. `docs/phase1/WORKER-LOOP.md`
2. `docs/phase1/ITERATION-01-WORK-ORDER.md`
3. `schemas/phase1-worker-iteration.schema.json`

The Worker MUST publish `benchmarks/p01/iterations/iteration-01.json` with separate
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
- Production router state for `products/sumer-writing` is currently idle; do not
  create a production task for benchmark work.
- `docs/experiments/p01-foc-loop/`, `docs/experiments/p01-writer-trace-v2/`, their
  scripts, and their run artifacts are legacy evidence only.
- Historical product tasks, rework records, rejected probes, and experiment runs
  remain immutable source material. A stale status string inside a historical
  artifact does not make it active work.
- No new Writer round is authorized until the Phase 1 benchmark can produce
  useful evidence-grounded failure signatures and pass the required calibration gates.

## Phase 1 checkpoint

The measurement layer includes or evolves these artifacts:

1. `docs/quality/output-quality-contract.md`
2. `schemas/output-quality.schema.json`
3. `benchmarks/p01/benchmark-set.json`
4. a frozen reference/source manifest with stable hashes and locators
5. a trial protocol for black-box Product evaluation
6. a minimal decision-record schema for consequential choices
7. DEV / CALIBRATION / HOLDOUT partition metadata
8. owner-preference calibration protocol/artifacts
9. Worker iteration records with `process` and `output`

Do not write new candidate prose for this checkpoint.

## Calibration corpus

Use immutable existing material. At minimum include:

- one earlier P01 sample historically regarded as essay-like, with that old label
  hidden from reviewers;
- the current P01 baseline;
- the writer-trace-v2 round-01 candidate;
- function-matched Fall of Civilizations craft excerpts specified by the
  architecture plan.

Historical reviewer verdicts are hypotheses, not gold labels. Re-evaluate the
text through the new contract. Owner/human labels must be recorded only when
actually supplied; do not infer them from filenames or historical commentary.

## Measurement invariants

Every retained product-quality criterion must:

- ask an observable question about the output;
- identify exact output spans supporting the judgment;
- separate observation from interpretation;
- preserve `UNCERTAIN` when evidence is insufficient;
- separate relative old/new result from remaining target gap;
- avoid scalar quality scores as the primary signal;
- avoid encoding one P01 solution path as the definition of good writing.

Truth/scope/coherence gates stay separate from craft dimensions. Exact quotation
proves location, not semantic entailment.

Open-ended prose comparison should prefer anonymized pairwise preference as the
primary comparative signal. Span-grounded defect annotation is diagnostic and
must remain distinct from root-cause attribution.

## Black-box boundary

Product-quality reviewers receive prose plus the frozen measurement/reference
packet only. They must not receive Planner traces, Writer reports, Worker process
logs, intended winner, old verdicts, or diagnostic hypotheses.

The Worker `process` record exists for downstream audit after an output defect is
observed. It is never evidence that the benchmark feature it intended to build
actually works.

White-box/root-cause work is downstream of an observed benchmark failure and is
not the Phase 1 product-quality measurement mechanism.

## Exit gate

Do not move to Phase 2 until the Phase 1 exit criteria in
`docs/architecture/observable-learning-architecture-plan.md` are satisfied,
including a brief human relevance/owner-preference calibration check and a fresh
transfer/holdout check. Agent agreement or a structural verifier alone is
insufficient for Phase 1 closure.

A Worker may legitimately stop at `READY_FOR_HUMAN_CALIBRATION`.

## Legacy warning

Do not execute these as active workflows:

```text
python scripts/experiments/p01_foc_loop.py ...
python scripts/experiments/p01_writer_trace_v2.py ...
```

They remain in the repository so their implementation and run artifacts can be
audited and used as benchmark evidence.
