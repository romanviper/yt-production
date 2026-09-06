# Phase 1 Improvement Iteration 04 — Deep Research Architecture Freeze

Status: **READY FOR IMPLEMENTATION**  
Source branch: `codex/p01-phase1-benchmark`  
Basis: Deep Research report supplied by the product owner on 2026-09-06.

## Objective

Freeze Benchmark V1 around the smallest evidence-backed architecture that can serve as the product-side root of future white-box tracing.

This iteration is architecture-only. It does not authorize a new Writer probe, production task, Phase 2 cleanup, or Phase 3 runtime.

## Frozen construct

Benchmark V1 measures:

> blind preference of the product owner between two Vietnamese historical-podcast outputs performing the same editorial function, while historical truth is audited independently.

This construct is `OWNER_PRODUCT_FIT`. It is not general-audience preference, objective literary quality, FoC similarity, or AI-judge preference.

## Required changes

### 1. Holistic preference before diagnostics

Primary Product output MUST contain a first-pass holistic result:

`A | B | TIE | BOTH_FAIL | UNCERTAIN`

plus confidence. The first-pass preference is frozen before any taxonomy, craft reference, truth result, or dimension-by-dimension diagnostic is shown.

The six historical dimensions (`continue`, `movement`, `specificity`, `connections`, `spoken_comprehension`, `payoff`) are removed from the primary decision contract. They may survive only as legacy vocabulary or be represented through post-vote diagnostics.

### 2. Separate preference from failure diagnostics

Use separate schemas/artifacts for:

- `pairwise-preference` — first-pass holistic owner or shadow-judge vote;
- `failure-signature` — post-vote localization/explanation;
- `truth-record` — independent claim-level truth lane;
- `spoken-observation` — text/audio/listener evidence lane;
- `target-gap` — post-preference function-matched craft-reference analysis;
- `judge-reliability` — shadow-judge calibration state.

No failure artifact may contain upstream root cause.

### 3. Minimal six-family Product defect taxonomy

Freeze the initial Product taxonomy to:

- `NARRATIVE_FUNCTION`
- `EXPOSITION_LOAD`
- `SPOKEN_COMPREHENSION`
- `GROUNDING_SPECIFICITY`
- `VOICE_STANCE`
- `REDUNDANCY`

Each failure has one `primary_family`. Secondary effects belong in `contributes_to` rather than being counted as independent failures.

Failure scope MUST support:

`SPAN | MULTI_SPAN | UNIT_GLOBAL`

Diagnostics may remain `UNRESOLVED` when the owner preference is clear but the taxonomy cannot explain it.

### 4. Evaluation Unit as the benchmark primitive

Introduce `eval-unit.schema.json` with at least:

- `historical_topic`
- `editorial_function`
- `granularity`
- `modality`
- `evidence_condition`

Granularity enum:

- `FUNCTION_CLIP`
- `SECTION_SENTINEL`
- `EPISODE_SENTINEL`

Do not define clips by arbitrary fixed word counts.

### 5. Truth lane semantic structure

Truth records distinguish claim type and verifiability. Required concepts include:

- `EXPLICIT`
- `IMPLIED_PREMISE`
- `CAUSAL`
- `DATE_QUANTITY`
- `QUOTATION_PARAPHRASE`
- `RECONSTRUCTION`

and:

- `VERIFIABLE`
- `PARTLY_VERIFIABLE`
- `NONFACTUAL`

Source relation:

`SUPPORTS | QUALIFIES | CONFLICTS | ABSENT`

A rhetorical question does not become `NONFACTUAL` if it carries an implied factual premise. Temporal or associative support does not automatically support causality.

Truth is a non-compensatory release lane but does not suppress Product evaluation.

### 6. Spoken evidence as an independent lane

Preserve the evidence distinction:

- `TEXT_PREDICTION`
- `AUDIO_OBSERVATION`
- `LISTENER_REPORT`

Text-only evidence cannot certify audio prosody or actual listener comprehension.

### 7. Demote all historical P01 holdout material to DEV

Every P01 artifact already stored in this shared/public repository and used during benchmark/harness work is contaminated for blind validity and therefore belongs to `DEV`.

The repository MUST NOT contain the payload or labels of a true sequestered set.

Create only a metadata manifest for private/restricted `SEQUESTERED` evidence. After a sequestered set is opened for tuning, it becomes calibration history and a `REFRESHED_SEQUESTERED` set is required for a new blind claim.

### 8. LLM judge is SHADOW_ONLY

Before out-of-sample owner validation, an LLM judge predicts owner preference but has no authority to drive optimization or overturn owner labels.

Judge reliability must record at least:

- owner agreement;
- position-reversal consistency;
- duplicate consistency;
- evidence-span validity;
- confidence-conditioned behavior;
- abstention rate;
- Vietnamese slice;
- long-context slice;
- topic transfer;
- eligibility for the optimization loop.

No universal agreement threshold is invented. Acceptance tolerances must be pre-registered before opening the sequestered set.

### 9. Owner calibration packets become pilot packets

The three existing P01 owner packets remain useful for interface/protocol testing but are not the final calibration corpus.

Update them to support:

- `BOTH_FAIL`;
- confidence;
- explicit first-pass freeze;
- optional reason/spans only after the vote.

They are designated `PILOT`, not evidence of benchmark validity.

### 10. FoC remains post-vote only

FoC/reference material is not visible during primary Product preference. `target-gap` runs after preference freeze, is function-matched, and must not use style similarity as a score.

### 11. No Bradley–Terry requirement in V1

Do not aggregate Benchmark V1 into a global scalar, Elo, or Bradley–Terry ranking. Preserve raw pair outcomes and uncertainty by topic/editorial function/granularity.

## Required output artifacts

At minimum this iteration must create/update:

- `schemas/eval-unit.schema.json`
- `schemas/pairwise-preference.schema.json`
- `schemas/failure-signature.schema.json`
- `schemas/truth-gate.schema.json`
- `schemas/spoken-observation.schema.json`
- `schemas/target-gap.schema.json`
- `schemas/judge-reliability.schema.json`
- `benchmarks/p01/taxonomy.json`
- `benchmarks/p01/benchmark-set.json`
- `benchmarks/p01/sequestered-manifest.json`
- `benchmarks/p01/owner-calibration.json`
- the three owner pilot packets
- `docs/quality/output-quality-contract.md`
- `docs/quality/product-trial-protocol.md`
- `scripts/experiments/verify_phase1_benchmark.py`
- `benchmarks/p01/iterations/iteration-04.json`

The iteration record MUST keep `process` and `output` separate.

## Stop condition

Stop after Benchmark V1 architecture is internally consistent and the pilot owner packets are ready for protocol testing. Do not collect owner labels in this implementation iteration. Do not claim Phase 1 complete. The strongest valid state is `ARCHITECTURE_FROZEN_READY_FOR_PILOT` until human pilot/calibration and real sequestered transfer evidence exist.
