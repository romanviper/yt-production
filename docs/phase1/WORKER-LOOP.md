# Phase 1 Worker Improvement Loop

Status: **ACTIVE FOR BENCHMARK V1 FREEZE / PILOT PREPARATION**

This loop improves the Phase 1 benchmark itself. It does not authorize a new Writer probe, production task, Phase 2 runtime, or Phase 3 white-box architecture.

## Core rule: record both process and output

Every Worker iteration MUST publish one structured iteration record under:

`benchmarks/p01/iterations/<iteration-id>.json`

The record conforms to `schemas/phase1-worker-iteration.schema.json` and has two first-class surfaces:

- `process`: what the Worker actually implemented — observable decisions, changed files, validation steps, deviations, unresolved limitations, and external/evidence basis used for consequential design choices.
- `output`: the resulting benchmark state — version, deliverables, measurement design, dataset lifecycle, owner state, judge state, verifier result, limitations, and readiness claim.

`process` is diagnostic telemetry, not private chain-of-thought. Record concise inspectable decisions, not hidden reasoning.

## Review isolation

Benchmark/Product quality review is black-box with respect to Worker process:

1. Review benchmark `output` and artifacts first.
2. Do not use Worker `process` to excuse weak benchmark behavior or infer that an intended property exists.
3. Only after an observable defect is found may an auditor open `process` to trace where that defect entered implementation.

Future diagnostic direction:

`observable output failure -> inspect process -> bounded root-cause region`

not:

`Worker says it implemented X -> reviewer assumes X works`.

## Iteration lifecycle

1. Freeze the work order.
2. Record source commit and objective.
3. Make the smallest coherent benchmark change.
4. Record implementation facts as they become known; label retrospective reconstruction when applicable.
5. Run validations where the environment allows and record exact commands/results.
6. Write the `output` snapshot.
7. Review output independently.
8. If output fails, open process only to bound the next work order.

## Required process content

At minimum:

- objective and source commit;
- consequential design decisions and declared basis;
- files changed;
- external framework/research basis when applicable;
- validation commands and observed results;
- deviations;
- unresolved questions/coverage gaps;
- no self-certification beyond what validation proves.

## Required output content

At minimum:

- benchmark version and deliverables;
- primary evaluation and post-vote diagnostic design;
- dataset state for `DEV`, `PILOT`, `CALIBRATION`, `SEQUESTERED`, and `REFRESHED_SEQUESTERED` where applicable;
- owner calibration/pilot state;
- shadow-judge state;
- craft-reference coverage;
- verifier result;
- known limitations;
- readiness status.

## Public/private data boundary

Historical P01 material already committed to the shared/public repo is DEV.

A real `SEQUESTERED` payload and labels must not be committed here. The public repo may contain only a metadata/hash shell. Once a sequestered set is opened for tuning it becomes calibration history and the next blind claim requires `REFRESHED_SEQUESTERED` evidence.

## Phase 1 completion boundary

A Worker iteration may make the architecture structurally coherent or ready for pilot/calibration, but it MUST NOT mark Phase 1 complete merely because files exist or a verifier passes.

Phase 1 closure requires real owner calibration, judge reliability evidence if an LLM judge is to be used, private/restricted sequestered validation, and transfer to new historical topics/functions/granularities.
