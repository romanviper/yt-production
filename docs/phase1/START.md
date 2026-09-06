# Phase 1 — Output Benchmark & Measurement Contract

Status: **ACTIVE / BENCHMARK V1 ARCHITECTURE FROZEN, OWNER PILOT ACTIVE**  
Canonical production branch: `main`  
Active Phase 1 implementation branch: `codex/p01-phase1-benchmark`

This is the active entrypoint for Phase 1 of the Observable Learning Architecture.

Read in this order:

1. `docs/architecture/observable-learning-architecture-plan.md`
2. `docs/quality/output-quality-contract.md`
3. `docs/quality/product-trial-protocol.md`
4. `docs/quality/owner-guided-review.md`
5. `docs/phase1/WORKER-LOOP.md`
6. latest iteration record under `benchmarks/p01/iterations/`

## Benchmark V1 primary construct

The benchmark-valid primary construct remains:

`blind holistic owner preference -> confidence -> freeze`

Allowed results:

`A | B | TIE | BOTH_FAIL | UNCERTAIN`

FoC/reference material, taxonomy, process logs, historical labels and diagnostics remain hidden before a benchmark-valid blind vote.

## Owner-friendly guided review mode

A separate diagnostic UX now exists because long-probe review can collapse into uninformative `BOTH_FAIL` feedback.

Guided path:

`one sample -> rhetorical micro-units -> observable feature extraction -> function-matched FoC target behavior -> owner gap labels`

This mode is defined by:

- `docs/quality/owner-guided-review.md`
- `schemas/owner-guided-review.schema.json`
- `benchmarks/p01/review-profiles/foc-functional-targets.json`
- `benchmarks/p01/review-sessions/owner-pilot-01-guided.json`

Important: guided review is `benchmark_evidence_eligible=false`. It is preference-elicitation/diagnostic evidence and MUST NOT be counted as blind calibration evidence.

Owner guided labels:

`MATCHES_TARGET | PARTIAL | MISSES_TARGET | WRONG_TARGET | UNCERTAIN`

`WRONG_TARGET` means the FoC-derived behavior abstraction itself does not represent the desired product and must be corrected rather than imposed on the owner.

## Guided feature vocabulary

The current owner-review UX uses a small behavior-level vocabulary:

- `INFORMATION_RELEASE`
- `LISTENER_ORIENTATION`
- `FORWARD_PRESSURE`
- `CONCRETENESS_FUNCTION`
- `NARRATOR_STANCE`
- `LOCAL_TRANSFORMATION`
- `SPOKEN_LOAD`

These are descriptors, not scores. Do not aggregate them into a scalar quality metric.

## Measurement architecture

Benchmark V1 keeps separate responsibilities:

1. **Product preference** — blind holistic owner A/B preference.
2. **Truth** — independent claim-level historical audit.
3. **Failure signature** — post-vote output-side diagnosis with `root_cause=null`.
4. **Spoken evidence** — `TEXT_PREDICTION | AUDIO_OBSERVATION | LISTENER_REPORT`.
5. **Target gap** — post-vote, function-matched `CRAFT_ONLY_NOT_TRUTH` comparison.
6. **Judge reliability** — LLM judge remains `SHADOW_ONLY` until externally validated.
7. **Guided owner review** — optional micro-unit target comparison for richer human feedback; never blind benchmark evidence.

The legacy monolithic `schemas/output-quality.schema.json` is deprecated and must not be reintroduced as the active combined evaluation object.

## Dataset state

All historical P01 material already exposed in the public/shared repository is DEV.

The three existing owner A/B pairs are PILOT UX inputs only, not fresh calibration evidence.

A true `SEQUESTERED` payload/label set must remain outside the public repository. The public repo may contain only its metadata/hash manifest shell.

## Current pilot

Iteration 05 introduces a guided Sample A pilot with five micro-units. The purpose is to validate owner-review ergonomics before expanding the mechanism across the full probe, Sample B, Section sentinels, or Episode sentinels.

Do not generate dozens of cards before the owner confirms that this review format is useful.

## Worker observability

Every Phase 1 improvement iteration must publish separate `process` and `output` surfaces under:

`benchmarks/p01/iterations/<iteration-id>.json`

Worker process is diagnostic telemetry only. Product/output review happens first; process is opened after an observable defect appears.

## Phase 1 scope boundary

Phase 1 does not authorize:

- a new production Writer probe;
- a Phase 2 runtime rewrite;
- Phase 3 white-box orchestration;
- LLM judge authority over optimization;
- public-repo fake holdouts;
- scalar FoC similarity scores.

## Exit boundary

Phase 1 is not complete until structural readiness, owner calibration, evaluator validity, private/restricted sequestered validation and transfer validity have all been demonstrated.

A structural verifier or agent agreement alone cannot close Phase 1.
