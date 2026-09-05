# Black-Box Product Evaluation Trial Protocol v1.1

Status: **PHASE 1 / CALIBRATION PROTOCOL**

## 1. Purpose

This protocol evaluates product-quality preference without exposing upstream intent. It is designed for Vietnamese long-form historical podcast prose where open-ended quality is difficult to represent with a single absolute score.

The primary comparative signal is anonymized pairwise preference. Defect annotation and target-gap analysis are secondary diagnostics.

## 2. Black-box boundary

A Product Reviewer may receive only:

- anonymized Sample A and Sample B;
- the frozen Output Quality Contract version;
- function-matched `CRAFT_ONLY` reference excerpts when relevant;
- output schema and evidence-grounding rules.

The reviewer MUST NOT receive:

- candidate/baseline/new/old labels;
- filenames or titles that reveal expected quality;
- historical verdicts;
- Planner/Writer/Worker process logs;
- intended winner;
- diagnostic hypotheses;
- upstream agent identity.

## 3. Pairwise review

For each applicable criterion, return:

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

Do not select a winner because one sample follows the benchmark examples more literally.

## 4. Position control

Every meaningful pair used for judge calibration is evaluated twice with reversed order:

- battle 1: X=A, Y=B;
- battle 2: X=B, Y=A.

A preference that flips merely with position is `POSITION_UNSTABLE` and cannot count as demonstrated separation.

Do not add more voters merely to break a disagreement.

## 5. Duplicate / same-text control

Calibration includes at least one pair where A and B contain identical text under different opaque IDs.

Expected behavior is `TIE` or defensible `UNCERTAIN` across applicable dimensions. A claimed substantive A/B difference is a reliability defect that must be investigated.

## 6. DEV / CALIBRATION / HOLDOUT

### DEV

May be inspected while criteria are designed. Historical P01 samples already discussed by the team belong here.

### CALIBRATION

Used to measure judge predictions against real owner/human preference. Owner labels are absent until explicitly supplied.

### HOLDOUT

Reserved for a fresh transfer check after definitions stabilize. The contract must not be tuned against holdout outcomes.

Partition membership is frozen in `benchmarks/p01/benchmark-set.json` before owner/judge scoring.

## 7. Owner-preference calibration

Owner preference is the primary personalized relevance signal for this product. The benchmark prepares anonymized comparisons; it MUST NOT infer owner labels from historical filenames, comments, or previous agent summaries.

For each owner-labelled pair, compare judge result against owner result and record:

- overall pairwise agreement;
- criterion-level agreement where the owner supplied criterion feedback;
- position consistency;
- duplicate consistency;
- uncertainty rate;
- evidence-span validity;
- whether the pair was clearly different or subtle/contested.

Small-sample results are descriptive. Do not claim population-level accuracy.

## 8. Defect annotation after preference

After forming the pairwise judgment, the reviewer may annotate concrete defects using the contract taxonomy.

Defects require:

- family/subtype;
- exact span;
- severity;
- observation;
- listener/product consequence;
- uncertainty.

`essay-like` is not a standalone score. It must be expressed through concrete defect types such as `EXPOSITION.CONCLUSION_BEFORE_EXPERIENCE` or `EXPOSITION.ABSTRACT_THESIS_TRANSITION`.

## 9. Target-gap comparison

Target-gap analysis uses a function-matched craft reference frozen before scoring.

Record exact candidate/reference spans and specific differences. Do not use a global `NEAR/MODERATE/FAR` judgment from one excerpt.

FoC references are `CRAFT_ONLY`; they never expand P01 historical authority.

## 10. Truth boundary

Historical truth evaluation is a hard gate separate from Product preference.

Do not reuse historical `32/32 verified` or similar legacy claims as gold truth. A current truth result must be supported under the current contract or remain `UNCERTAIN`/unvalidated.

## 11. Readiness semantics

A structural verifier may return:

- `NOT_READY`
- `STRUCTURALLY_READY`
- `READY_FOR_HUMAN_CALIBRATION`

Only actual owner/human calibration plus a fresh transfer check can support `READY_FOR_EXIT_REVIEW`.

A structural pass never certifies aesthetic quality.
