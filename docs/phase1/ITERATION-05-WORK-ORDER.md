# Phase 1 Improvement Iteration 05 — Owner Review UX Layer

Status: READY FOR IMPLEMENTATION

## Objective

Make owner review substantially easier without weakening Benchmark V1 validity.

The owner should not be forced to read two long probes and return only `BOTH_FAIL`. Add a guided review layer that decomposes prose into micro-units, extracts observable craft features, and compares those features against function-matched FoC target behavior.

## Non-negotiable boundary

This layer is **not** the blind primary benchmark vote and must never be represented as calibration-valid preference evidence.

Blind benchmark path remains:

`A/B prose -> holistic preference -> freeze`

Guided owner-review path is:

`sample -> micro-units -> observable features -> function-matched target behavior -> owner gap labels -> preference vocabulary`

FoC/reference material is allowed only in this guided diagnostic mode. It remains forbidden before a benchmark-valid blind vote.

## Required UX

Each review card should be small enough to inspect without reading the full probe again. Prefer one rhetorical/functional unit (usually 1–3 sentences), not arbitrary fixed word counts.

For each micro-unit show:

1. candidate excerpt;
2. unit function;
3. extracted observable features;
4. matched FoC target behavior expressed as craft behavior, not a style-copy instruction;
5. direct similarities;
6. direct gaps;
7. owner response controls.

Owner response should support:

- `MATCHES_TARGET`
- `PARTIAL`
- `MISSES_TARGET`
- `WRONG_TARGET`
- `UNCERTAIN`

plus optional decisive note and optional preferred behavior.

## Feature families for guided review

Keep the set small and behavior-level:

- `INFORMATION_RELEASE` — how information is staged/revealed;
- `LISTENER_ORIENTATION` — what the listener knows they are looking for and why;
- `FORWARD_PRESSURE` — what creates a reason to continue without requiring cliffhangers;
- `CONCRETENESS_FUNCTION` — whether material detail creates inference/experience instead of merely decorating explanation;
- `NARRATOR_STANCE` — whether narrator discovers/frames/lectures/concludes;
- `LOCAL_TRANSFORMATION` — what meaning/state changes across the unit;
- `SPOKEN_LOAD` — one-pass cognitive/syntactic burden from text evidence only.

These are review descriptors, not benchmark scores. Do not aggregate them into a scalar.

## Target comparison rule

Do not say `FoC score = X` or `similarity = 80%`.

For each feature compare behaviorally:

- candidate behavior;
- FoC/reference behavior for the same editorial function;
- observable overlap;
- observable gap;
- confidence/medium limitation.

Do not reward surface wording, sentence length, motif, or cadence imitation.

## Required artifacts

- `docs/quality/owner-guided-review.md`
- `schemas/owner-guided-review.schema.json`
- `benchmarks/p01/review-profiles/foc-functional-targets.json`
- `benchmarks/p01/review-sessions/owner-pilot-01-guided.json`
- `benchmarks/p01/iterations/iteration-05.json`

Update `docs/phase1/START.md` to distinguish blind benchmark review from guided owner review.

## Exit condition

Iteration 05 is complete when:

- the UX layer exists as a separate non-benchmark-valid diagnostic path;
- owner can review one probe through multiple micro-cards instead of one monolithic passage;
- target comparisons are behavioral/function-matched;
- no scalar score is introduced;
- no FoC material leaks into the blind preference packet;
- process/output are logged in the iteration record.
