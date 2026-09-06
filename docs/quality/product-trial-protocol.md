# Black-Box Product Evaluation Trial Protocol v1.3

Status: **ARCHITECTURE FROZEN FOR PILOT**

## 1. Purpose

Benchmark V1 measures `OWNER_PRODUCT_FIT` through blind holistic pairwise preference, then explains failures after the vote. Historical truth, spoken evidence, and craft-reference target gap remain independent lanes.

No lane may retroactively rewrite another lane's observation.

## 2. Evaluation unit

Every trial references a frozen evaluation unit conforming to `schemas/eval-unit.schema.json`:

`historical_topic × editorial_function × granularity × modality × evidence_condition`

Granularity:

- `FUNCTION_CLIP`
- `SECTION_SENTINEL`
- `EPISODE_SENTINEL`

## 3. Product Lane — first-pass holistic preference

The Product/owner packet contains only:

- neutral scenario/evaluation-unit context;
- anonymized Sample A and Sample B;
- first-pass result options;
- confidence options.

It MUST NOT contain:

- FoC or other craft references;
- Truth results;
- defect taxonomy before the vote;
- previous preference or reviewer verdicts;
- candidate/baseline/new/old labels;
- source paths that reveal identity;
- Planner/Writer/Worker process logs;
- intended winner;
- upstream diagnostic hypotheses;
- shadow-judge predictions.

First pass:

`A | B | TIE | BOTH_FAIL | UNCERTAIN`

Confidence:

`LOW | MEDIUM | HIGH`

`BOTH_FAIL` means neither output is acceptable as a positive product target. It is not equivalent to `TIE`.

The first-pass preference is recorded and frozen before any diagnostic questions are shown.

Canonical schema: `schemas/pairwise-preference.schema.json`.

## 4. Post-vote diagnostics

Only after the preference is frozen may the owner/reviewer provide:

- optional free reason;
- optional decisive spans;
- output-side failure annotation.

Do not require the owner to score dimensions before choosing the preferred product.

Failure annotations conform to `schemas/failure-signature.schema.json` and `benchmarks/p01/taxonomy.json`.

A diagnostic may be `UNRESOLVED`. A clear preference does not become invalid merely because the current taxonomy cannot explain it.

One observable failure has one `primary_family`. Secondary consequences belong in `contributes_to`.

Failure scope:

- `SPAN`
- `MULTI_SPAN`
- `UNIT_GLOBAL`

`root_cause` remains `null` during Phase 1.

## 5. Product defect taxonomy

The six initial families are:

- `NARRATIVE_FUNCTION`
- `EXPOSITION_LOAD`
- `SPOKEN_COMPREHENSION`
- `GROUNDING_SPECIFICITY`
- `VOICE_STANCE`
- `REDUNDANCY`

The historical six-dimension score surface is not the primary decision mechanism and is not averaged into a quality score.

## 6. Truth Lane

Truth receives one candidate plus approved historical authority and `schemas/truth-gate.schema.json`.

It receives no FoC, Product preference, target-gap result, or process log.

Truth identifies claim type and verifiability before judging support. In particular it must distinguish implied premises and causal claims from genuinely nonfactual material.

Truth continues even when the candidate loses Product preference; Product evaluation also continues when Truth blocks release. The lanes capture different constructs.

A material Truth blocker prevents release but does not erase the Product observation.

## 7. Spoken Lane

Spoken evidence conforms to `schemas/spoken-observation.schema.json`.

Evidence modes:

- `TEXT_PREDICTION`
- `AUDIO_OBSERVATION`
- `LISTENER_REPORT`

Claims must not exceed the evidence mode. Text-only review cannot certify prosody or actual listener comprehension.

## 8. Target-gap Lane

Target-gap starts only after first-pass Product preference is frozen.

It receives:

- one selected candidate/passage;
- the frozen Product preference reference;
- pre-frozen function-matched `CRAFT_ONLY` references;
- `schemas/target-gap.schema.json`.

FoC is hidden from the primary vote. Target gap compares editorial function, not stylistic similarity, and cannot alter the frozen vote.

## 9. Owner pilot

The three current historical P01 packets are protocol/interface pilots only.

They test:

- blinding of source/system identity;
- `BOTH_FAIL` availability;
- confidence capture;
- first-pass freeze;
- optional post-vote reason/spans;
- ability to leave diagnostics unresolved.

Because their prose has already been visible during P01 development, these packets are DEV and cannot establish benchmark validity.

## 10. Fresh calibration

After pilot usability is confirmed, build a fresh calibration corpus across multiple editorial functions, including clear, subtle, challenge, and both-fail pairs.

Calibration is used to understand owner self-consistency and to train/tune a shadow judge. It is not final out-of-sample proof.

Useful owner metrics include:

- test-retest consistency;
- position consistency;
- clear-vs-subtle consistency;
- tie rate;
- both-fail rate;
- uncertainty rate;
- reason localizability;
- taxonomy coverage/unresolved rate.

Do not invent a universal owner-consistency threshold.

## 11. LLM shadow judge

LLM judges operate as `SHADOW_ONLY` until validated on unseen owner-labelled evidence.

Shadow judges:

- predict owner preference;
- may run A/B reversal and duplicate controls;
- may supply post-vote spans/diagnostics;
- cannot drive optimization;
- cannot overturn owner labels;
- cannot become gold through agent majority.

Reliability record: `schemas/judge-reliability.schema.json`.

Acceptance tolerances must be pre-registered before opening sequestered evidence. Do not choose a threshold after seeing the result.

## 12. Dataset lifecycle

### DEV

All historical P01 artifacts and anything used to design/tune benchmark rules.

### CALIBRATION

Fresh owner-labelled pairs collected after pilot protocol freeze.

### SEQUESTERED

Private/restricted fresh-topic evidence withheld until benchmark/judge rules and tolerances are frozen.

The public repo contains only `benchmarks/p01/sequestered-manifest.json`, never sequestered prose or labels.

After a sequestered set is opened and used for tuning, it becomes calibration history and a new `REFRESHED_SEQUESTERED` set is required.

## 13. Aggregation

V1 preserves raw outcomes and slices by topic/editorial function/granularity.

Do not require:

- one quality score;
- Elo;
- Bradley–Terry;
- AI majority voting.

## 14. Readiness semantics

Valid states include:

- `NOT_READY`
- `STRUCTURALLY_READY`
- `ARCHITECTURE_FROZEN_READY_FOR_PILOT`
- `READY_FOR_FRESH_CALIBRATION`
- `READY_FOR_SEQUESTERED_VALIDATION`
- `READY_FOR_EXIT_REVIEW`

Iteration 04 may reach only `ARCHITECTURE_FROZEN_READY_FOR_PILOT`.

Phase 1 cannot close without real sequestered validation and transfer evidence on new historical topics.
