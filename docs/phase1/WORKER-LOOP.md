# Phase 1 Worker Improvement Loop

Status: **ACTIVE ON `codex/p01-phase1-benchmark`**

This loop improves the Phase 1 benchmark itself. It does not authorize a new Writer probe, production task, Phase 2 runtime, or Phase 3 white-box architecture.

## Core rule: record both process and output

Every Worker iteration MUST publish one structured iteration record under:

`benchmarks/p01/iterations/<iteration-id>.json`

The record conforms to `schemas/phase1-worker-iteration.schema.json` and has two first-class surfaces:

- `process`: what the Worker actually implemented — observable decisions, changed files, validation steps, deviations, unresolved limitations, and the external/evidence basis used for consequential design choices.
- `output`: the resulting Phase 1 benchmark state — benchmark version, deliverables, measurement design, calibration/holdout readiness, verifier result, known limitations, and readiness claim.

`process` is diagnostic telemetry, not private chain-of-thought. Do not dump hidden reasoning. Record concise decisions and their inspectable basis.

## Review isolation

Product/benchmark quality review is black-box with respect to Worker process:

1. Review the benchmark `output` and benchmark artifacts first.
2. Do not use the Worker `process` log to excuse weak benchmark behavior or infer that an intended property exists.
3. Only after an observable defect is found may an auditor open `process` to trace where that defect entered the implementation.

This preserves the future architecture principle:

`observable output failure -> inspect process -> bounded root-cause region`

not:

`Worker says it implemented X -> reviewer assumes X works`.

## Iteration lifecycle

1. Freeze the review/work order for the iteration.
2. Worker records the source commit and objective before editing.
3. Worker makes the smallest coherent benchmark changes that address the frozen findings.
4. Worker updates `process` as implementation facts become known; retrospective reconstruction must be labelled as such.
5. Worker runs validations and records exact commands/results.
6. Worker writes the `output` snapshot.
7. Reviewer judges the output independently.
8. If output still fails, auditor traces into `process`; the next work order targets only the bounded failure region.

## Required process content

At minimum record:

- objective and source commit;
- consequential design decisions and why they were selected;
- files changed by each implementation step;
- external framework/paper or repository evidence used as basis when applicable;
- validation commands and their observed results;
- deviations from the work order;
- unresolved questions/coverage gaps;
- no self-certification beyond what validations actually prove.

## Required output content

At minimum record:

- benchmark version and deliverable paths;
- primary evaluation mode and secondary diagnostics;
- DEV / CALIBRATION / HOLDOUT partition state;
- owner-preference calibration state;
- craft-reference corpus coverage;
- verifier result;
- known limitations;
- readiness status chosen from the schema.

## Phase 1 completion boundary

A Worker iteration may make the benchmark technically runnable, but it MUST NOT mark Phase 1 complete merely because files exist or a structural verifier passes. Human relevance/calibration and held-out transfer requirements from the architecture plan remain external exit gates.
