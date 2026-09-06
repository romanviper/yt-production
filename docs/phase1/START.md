# Phase 1 — Output Benchmark & Measurement Contract

Status: **ITERATION 04 / ARCHITECTURE FREEZE**  
Canonical production branch: `main`  
Phase 1 parent branch: `codex/p01-phase1-benchmark`  
Current implementation branch: `codex/p01-phase1-benchmark-v1-freeze`

This is the active entrypoint for Phase 1 benchmark architecture.

Read in this order:

1. `docs/architecture/observable-learning-architecture-plan.md`
2. `docs/phase1/WORKER-LOOP.md`
3. `docs/phase1/ITERATION-04-WORK-ORDER.md`
4. `docs/quality/output-quality-contract.md`
5. `docs/quality/product-trial-protocol.md`
6. `schemas/phase1-worker-iteration.schema.json`

Iteration 04 MUST publish `benchmarks/p01/iterations/iteration-04.json` with separate `process` and `output` sections.

## Frozen construct

Benchmark V1 measures:

> blind preference of the product owner between two Vietnamese historical-podcast outputs performing the same editorial function, while historical truth is audited independently.

The construct is `OWNER_PRODUCT_FIT`.

It is not general-audience preference, objective literary quality, FoC similarity, or AI-judge preference.

## Objective

Build the smallest benchmark that can tell us whether output is moving toward the product the owner wants, localize observable failure when it is not, preserve uncertainty, and create a clean root node for future white-box tracing.

Phase 1 does **not** improve Writer prompts, create a new production draft, redesign the production router, or build the Phase 3 white-box runtime.

## Active measurement primitives

### Evaluation unit

`schemas/eval-unit.schema.json`

Every comparison declares:

`historical_topic × editorial_function × granularity × modality × evidence_condition`

Granularity:

- `FUNCTION_CLIP`
- `SECTION_SENTINEL`
- `EPISODE_SENTINEL`

### Product preference

`schemas/pairwise-preference.schema.json`

First-pass holistic result:

`A | B | TIE | BOTH_FAIL | UNCERTAIN`

plus confidence. Preference freezes before diagnostics/reference material.

### Failure signature

`schemas/failure-signature.schema.json`

Post-vote only. One primary defect family. Scope may be `SPAN`, `MULTI_SPAN`, or `UNIT_GLOBAL`. `root_cause` is always null in Phase 1.

### Truth

`schemas/truth-gate.schema.json`

Independent claim-level lane. Product evaluation still runs when Truth blocks release, and Truth still runs when Product loses.

### Spoken evidence

`schemas/spoken-observation.schema.json`

Evidence modes stay separate:

- `TEXT_PREDICTION`
- `AUDIO_OBSERVATION`
- `LISTENER_REPORT`

### Target gap

`schemas/target-gap.schema.json`

Runs only after Product preference freezes. FoC/reference is function-matched `CRAFT_ONLY_NOT_TRUTH` and style similarity is not a score.

### LLM judge reliability

`schemas/judge-reliability.schema.json`

LLM judge is `SHADOW_ONLY` until out-of-sample owner validation and transfer gates pass under pre-registered tolerances.

## Dataset roles

### DEV

All historical P01 material already visible in this repository. This includes the former calibration candidates and former shared-repo holdout.

### PILOT

The three current owner A/B packets are DEV-derived protocol/interface pilots only. They may test `BOTH_FAIL`, confidence, freeze order, optional reason/span capture, and unresolved diagnostics. They cannot establish benchmark validity.

### CALIBRATION

Fresh owner-labelled pairs collected after pilot protocol is stable.

### SEQUESTERED

Private/restricted fresh-topic evidence. Payload and labels MUST NOT be committed to this public repository.

Public metadata shell: `benchmarks/p01/sequestered-manifest.json`.

After a sequestered set is opened for tuning it becomes calibration history and a new `REFRESHED_SEQUESTERED` set is required.

## Product taxonomy

Canonical taxonomy: `benchmarks/p01/taxonomy.json`.

Families:

- `NARRATIVE_FUNCTION`
- `EXPOSITION_LOAD`
- `SPOKEN_COMPREHENSION`
- `GROUNDING_SPECIFICITY`
- `VOICE_STANCE`
- `REDUNDANCY`

The legacy six-dimension Product score surface is no longer the primary decision contract.

## Black-box boundary

The primary Product vote sees anonymized A/B output and neutral evaluation-unit context only.

It does NOT see:

- FoC/reference material;
- Truth results;
- taxonomy before the vote;
- process logs;
- model/system identity;
- historical verdicts;
- intended winner;
- shadow-judge prediction.

Only after the preference is frozen may diagnostics and target-gap analysis open their additional inputs.

## Aggregation

V1 keeps raw pair outcomes and uncertainty. No global quality score, Elo, Bradley-Terry requirement, or agent-majority gold.

## Readiness

Iteration 04 may reach only:

`ARCHITECTURE_FROZEN_READY_FOR_PILOT`

Phase 1 still requires:

1. pilot usability;
2. fresh owner calibration;
3. shadow-judge reliability measurement;
4. private/restricted sequestered validation;
5. transfer to new historical topics/editorial functions/granularities.

Structural verification alone cannot close Phase 1.

## Legacy warning

`schemas/output-quality.schema.json` is deprecated for new outputs. Legacy FoC/writer-trace experiment scripts and historical evaluator artifacts remain evidence only and must not be executed as the active Phase 1 workflow.
