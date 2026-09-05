# Black-Box Product Evaluation Trial Protocol v1.2

Status: **PHASE 1 / CALIBRATION PROTOCOL**

## 1. Purpose

This protocol separates three measurement questions that must not contaminate one another:

1. Is each sample historically admissible?
2. Which anonymized sample works better as the intended podcast product?
3. After preference is frozen, what observable craft gap remains to the function-matched target reference?

These are independent lanes. No single reviewer is asked to infer all three at once.

## 2. Lane A — Truth / scope gate

The Truth reviewer receives:

- one sample only;
- approved P01 historical authority;
- truth/scope gate schema.

The Truth reviewer MUST NOT receive:

- FoC craft references;
- Product pairwise verdicts;
- Worker/Writer/Planner process logs;
- target-gap analysis;
- historical evaluator verdicts treated as gold labels.

Truth output is per-sample. Sample A and Sample B are audited independently.

Exact quotation establishes location, not semantic entailment.

## 3. Lane B — Product pairwise preference

A Product Reviewer receives only:

- anonymized Sample A and Sample B;
- frozen Output Quality Contract criteria;
- Product pairwise output schema and grounding rules.

The Product Reviewer MUST NOT receive:

- FoC or other craft-reference excerpts;
- Truth reviewer results;
- target-gap records;
- candidate/baseline/new/old labels;
- filenames or titles that reveal expected quality;
- historical verdicts;
- Planner/Writer/Worker process logs;
- intended winner;
- diagnostic hypotheses;
- upstream agent identity.

The purpose is to judge whether A or B works better as the product, not which sample resembles FoC more closely.

### Pairwise criteria

For each applicable criterion return:

`A | B | TIE | UNCERTAIN`

Criteria:

- `continue`
- `movement`
- `specificity`
- `connections`
- `spoken_comprehension`
- `payoff`

Each criterion requires:

- exact quote(s) from A and/or B;
- observation: what is present/absent in the supplied prose;
- interpretation: likely consequence for the intended listener;
- uncertainty/counterevidence;
- evidence medium.

Do not select a winner because one sample follows benchmark examples more literally.

## 4. Pairwise reliability controls

### Position reversal

Every meaningful calibration pair is evaluated twice:

- battle 1: X=A, Y=B;
- battle 2: X=B, Y=A.

A preference that flips merely with position is `POSITION_UNSTABLE` and cannot count as demonstrated separation.

Do not add extra voters simply to break a disagreement.

### Duplicate / same-text control

Calibration includes at least one pair where A and B contain identical text under opaque IDs.

Expected behavior is `TIE` or defensible `UNCERTAIN` across applicable criteria. A claimed substantive difference is a reliability defect.

## 5. Lane C — Target-gap analysis

Target-gap analysis begins only AFTER Lane B pairwise preference has been frozen and recorded.

The Target-gap reviewer receives:

- one selected sample/passage;
- one or more pre-frozen function-matched `CRAFT_ONLY` references;
- target-gap schema.

It returns:

- exact candidate/reference spans;
- matched editorial function;
- observable similarities;
- observable differences;
- specific remaining gaps;
- retained strengths;
- medium limitations.

Target-gap analysis MUST NOT modify, reinterpret, or retroactively justify the already-frozen Product pairwise preference.

FoC remains `CRAFT_ONLY_NOT_TRUTH`; it never expands P01 historical authority.

## 6. DEV / CALIBRATION / HOLDOUT

### DEV

May be inspected while criteria are designed. Historical P01 samples already discussed by the team belong here.

### CALIBRATION

Used to measure judge predictions against real owner/human preference. Owner labels are absent until explicitly supplied.

### HOLDOUT

Reserved for a fresh transfer check after definitions stabilize. The contract must not be tuned against holdout outcomes.

A file present in the shared repository is not a cryptographically blind holdout. Until access is actually sequestered, label its reliability `FRESH_EXPOSED_NOT_BLIND` and preserve that limitation.

Partition membership is frozen in `benchmarks/p01/benchmark-set.json` before owner/judge scoring.

## 7. Owner-preference calibration

Owner preference is the primary personalized relevance signal for this product. The benchmark prepares anonymized comparisons; it MUST NOT infer owner labels from historical filenames, comments, or previous agent summaries.

For each owner-labelled pair, compare judge result against owner result and record:

- overall pairwise agreement;
- criterion-level agreement where owner criterion feedback exists;
- position consistency;
- duplicate consistency;
- uncertainty rate;
- evidence-span validity;
- whether the pair was clearly different or subtle/contested.

Small-sample results are descriptive. Do not claim population-level accuracy.

## 8. Defect annotation after preference

After forming Lane B preference, the Product reviewer may annotate concrete output defects using the contract taxonomy.

Defects require:

- family/subtype;
- exact span;
- severity;
- observation;
- listener/product consequence;
- uncertainty.

`essay-like` is not a standalone score. It must resolve to concrete defects such as `EXPOSITION.CONCLUSION_BEFORE_EXPERIENCE` or `EXPOSITION.ABSTRACT_THESIS_TRANSITION`.

## 9. Readiness semantics

A structural verifier may return:

- `NOT_READY`
- `STRUCTURALLY_READY`
- `READY_FOR_HUMAN_CALIBRATION`

Only actual owner/human calibration plus a fresh transfer check can support `READY_FOR_EXIT_REVIEW`.

A structural pass never certifies aesthetic quality.
