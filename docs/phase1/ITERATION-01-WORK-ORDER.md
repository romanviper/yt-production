# Phase 1 Improvement Iteration 01 — Work Order

Status: **READY FOR WORKER**  
Source benchmark commit: `2929c16bbd615dc512749bd6a9ef4c5941c39c06`

## Objective

Revise the Phase 1 benchmark so that it measures product quality with less rubric overfitting, less label leakage, and better evaluator calibration. Preserve useful implementation already present, but replace weak measurement assumptions before claiming Phase 1 readiness.

This iteration MUST emit `benchmarks/p01/iterations/iteration-01.json` following `schemas/phase1-worker-iteration.schema.json`, with separate top-level `process` and `output` sections.

## External benchmark patterns to adapt

Use these as design patterns, not as templates to copy mechanically:

- **HELM** — scenario/metric separation, multi-metric evaluation, explicit coverage gaps, transparent artifacts.
- **MQM** — span-grounded hierarchical error taxonomy and severity; errors are localized before aggregation.
- **Chatbot Arena / Bradley-Terry** — anonymized pairwise human preference as the primary comparison signal; counterbalance A/B position and preserve uncertainty.
- **LitBench** — creative-writing judges require calibration against human preference; LLM agreement is not ground truth.

The benchmark remains personalized to the owner/product: Vietnamese long-form historical podcast prose, FoC as primary craft reference, historical truth as a hard boundary.

## Keep from the current implementation

Retain unless a concrete conflict appears:

- immutable sample/source hashing;
- black-box Product review boundary;
- exact prose-span grounding;
- explicit `UNCERTAIN`;
- separation of hard truth/scope gates from craft evaluation;
- A/B counterbalancing concept;
- relative old/new comparison distinct from reference/target analysis;
- minimal decision-record concept.

## Required changes

### 1. Make pairwise preference the primary craft measurement

Do not make `GOOD/WEAK/FAIL` absolute ratings the primary optimization signal for open-ended prose.

For candidate-vs-baseline trials, primary Product review should return per applicable criterion:

`A | B | TIE | UNCERTAIN`

plus exact supporting spans and observed consequence. Absolute annotations may remain as secondary diagnostics where useful.

### 2. Separate quality dimensions from defect taxonomy

`essay_tendency` must not be a mandatory seventh craft score. Treat essay/lecture behavior as a diagnostic defect pattern that may explain failures in movement, continue, connection, payoff, or spoken comprehension.

Introduce an MQM-inspired hierarchical defect taxonomy with at least these initial families:

- `TRUTH.*`
- `PROGRESSION.*`
- `EXPOSITION.*`
- `CONNECTION.*`
- `SPOKEN.*`

Each defect annotation requires exact span, severity (`MINOR | MAJOR | CRITICAL` where applicable), observation, and listener/product consequence.

Do not double-count one observable weakness as several independent defects without justification.

### 3. Remove benchmark definitions that encode the current P01 solution

Criterion definitions must not define good `movement`, `continue`, or `payoff` using the exact token -> envelope -> paradox -> tablet sequence from round-01.

Use positive and limiting examples, but mark them as examples rather than the definition. A future passage using a different narrative architecture must still be measurable fairly.

### 4. Remove uncalibrated spoken-prose thresholds

Do not assert universal limits such as `15–25 syllables per clause` or `>40 words = weak` unless the benchmark contains validated evidence for them.

Separate medium of evidence:

- `TEXT_PREDICTION`
- `AUDIO_OBSERVATION`
- `LISTENER_REPORT`

Text-only listenability judgments must remain predictions, not claims about actual listener performance.

### 5. Replace scalar target distance with observable target differences

Remove or demote `NEAR | MODERATE | FAR` as the main target-gap representation.

A target-gap record should identify:

- matched reference ID and function;
- exact candidate/reference spans;
- observable similarity/difference;
- specific remaining gap;
- medium limitation;
- retained strengths.

Do not claim a global distance from FoC from one excerpt.

### 6. Add dataset partitions and prevent label leakage

Create explicit `DEV`, `CALIBRATION`, and `HOLDOUT` partitions.

- DEV may include the already-inspected historical samples.
- CALIBRATION is used to compare judge predictions with owner/human preferences.
- HOLDOUT must remain unused while criteria are being tuned.

Reviewer-facing artifacts must not contain labels such as `known_weak_essay`, `candidate`, `baseline`, preferred answer, historical verdict, or descriptive titles that reveal expected ranking.

### 7. Add owner-preference calibration protocol

Prepare, but do not fabricate, a small anonymized pairwise calibration set. Owner labels remain missing until actually supplied.

The protocol should measure at least:

- owner/judge pairwise agreement;
- position consistency under A/B reversal;
- duplicate/same-text consistency;
- uncertainty rate;
- evidence-span validity;
- ability to distinguish clearly different versus subtle pairs.

Agent agreement alone cannot close Phase 1.

### 8. Separate failure signature from root-cause hypothesis

A failure signature is output-side evidence only:

- defect type/subtype;
- exact span;
- severity;
- observation;
- uncertainty.

Do NOT include `suspect_upstream_regions` inside the signature.

If useful, create a separate `diagnostic_hypothesis` artifact/field. That hypothesis is tentative and may only guide later white-box inspection.

### 9. Do not import historical reviewer claims as truth ground truth

The round-01 statement `32/32 sentences verified` is not authoritative. Re-audit factual claims under the new truth contract or mark truth status unvalidated/incomplete.

FoC craft references are `CRAFT_ONLY`; do not truth-certify them as if they were P01 historical authority.

### 10. Expand and characterize the FoC craft corpus

Target the architecture-plan coverage: approximately 6–10 function-matched excerpts across at least two FoC episodes, covering multiple functions such as investigation/opening, mechanism explanation, scale change, uncertainty, transition, and payoff.

If available repository material cannot meet this requirement, record the uncovered functions as an explicit coverage limitation. Do not fabricate excerpts, timestamps, or episode provenance.

### 11. Make the verifier prove properties instead of printing hard-coded exit success

The verifier MUST NOT contain a checklist whose statuses are literal `True` values.

Add mechanical checks where possible, including:

- schema validity or equivalent structural validation;
- sample/hash consistency;
- evidence spans are exact substrings of the correct text;
- reviewer-facing packets do not leak expected labels;
- DEV/CALIBRATION/HOLDOUT IDs are disjoint;
- required craft-reference coverage is reported rather than assumed;
- failure signatures contain no upstream blame;
- `CRAFT_ONLY` references are not used as P01 truth authority;
- missing owner calibration prevents Phase 1 completion;
- missing/uncertain evidence cannot silently become PASS.

The verifier may report `STRUCTURALLY_READY` or `READY_FOR_HUMAN_CALIBRATION`; it must not certify aesthetic validity.

## Required Worker process log

In `benchmarks/p01/iterations/iteration-01.json -> process`, record each consequential implementation decision with:

- changed behavior;
- declared reason;
- framework/repo evidence used as basis;
- files affected;
- expected measurable effect;
- actual validation result;
- unresolved tradeoffs.

Do not write private chain-of-thought.

## Required Worker output snapshot

In `... -> output`, summarize the benchmark that actually exists after implementation:

- primary evaluation method;
- defect taxonomy state;
- dataset partition state;
- owner calibration readiness;
- FoC corpus coverage;
- verifier result;
- known limitations;
- readiness status.

Do not mark `READY_FOR_EXIT_REVIEW` unless the implementation truly has the required human calibration/transfer evidence. For this iteration, `READY_FOR_HUMAN_CALIBRATION` is a valid and likely successful endpoint.

## Stop condition

Stop after producing one coherent revised benchmark plus its `process`/`output` iteration record. Do not start a Writer round or Phase 2 work. Return the branch for independent review.
