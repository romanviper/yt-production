# Owner Guided Review — Behavioral Target Comparison

Status: Phase 1 diagnostic UX; not benchmark-valid blind preference evidence.

## Purpose

The owner should not have to review a long probe as a single object. This review mode decomposes a sample into small rhetorical/functional units and shows the observable behavior of each unit against a function-matched FoC craft target.

Use this mode when the owner can say only `BOTH_FAIL` or otherwise cannot efficiently articulate why a long sample misses the product target.

## Relationship to Benchmark V1

Two modes exist and must remain distinct.

### Blind benchmark mode

`anonymous A/B -> holistic vote -> confidence -> freeze`

No FoC/reference, taxonomy, process log, or diagnostic feature card is visible before the vote.

### Guided owner-review mode

`one sample -> micro-units -> feature extraction -> function-matched target comparison -> owner gap labels`

This mode may use FoC craft references because its purpose is preference elicitation and diagnostic vocabulary, not blind benchmark validity.

A guided result MUST NOT be copied into calibration statistics as if it were a blind vote.

## Review unit

A `micro_unit` is one rhetorical or editorial function, usually 1–3 sentences. Do not split mechanically by word count.

A good micro-unit is small enough that the owner can answer: “What is this unit doing to my listening state?”

Examples of unit functions:

- establish_material_object
- open_question
- reveal_constraint
- contrast_two_interpretations
- reframe_previous_fact
- bridge_to_next_artifact
- local_payoff
- uncertainty_boundary

## Guided feature families

These are descriptors, not scores.

### INFORMATION_RELEASE

Question: Does the unit give interpretation before the listener has a reason to need it, or does meaning emerge from what has just been encountered?

### LISTENER_ORIENTATION

Question: At this moment, does the listener know what object/problem/question they are following and why it matters?

### FORWARD_PRESSURE

Question: What concrete unresolved consequence, curiosity, tension, contrast, or pending interpretation creates a reason to continue?

### CONCRETENESS_FUNCTION

Question: Do material details create inference/experience/distinction, or merely decorate exposition?

### NARRATOR_STANCE

Question: Is the narrator discovering, framing, accompanying, lecturing, concluding, or summarizing?

### LOCAL_TRANSFORMATION

Question: What changes in the listener’s state of understanding from the start to the end of the unit?

### SPOKEN_LOAD

Question: From text evidence only, what creates one-pass cognitive or syntactic burden? This remains `TEXT_PREDICTION` until audio/listener evidence exists.

## FoC target comparison

FoC is used only as `CRAFT_ONLY_NOT_TRUTH` and only through a matched editorial function.

For every feature card show:

- `candidate_behavior`
- `target_behavior`
- `overlap`
- `gap`
- `confidence`
- `medium_limitation`

Never show:

- percentage similarity;
- global FoC score;
- sentence-length mimicry;
- wording to copy;
- motif/cadence imitation as a target.

The target should be phrased as a transferable behavior, e.g.:

`TARGET: material observation appears before the narrator explains why it matters`

not:

`TARGET: use FoC's sentence pattern here`.

## Owner controls

For each micro-unit or feature the owner may choose:

- `MATCHES_TARGET`
- `PARTIAL`
- `MISSES_TARGET`
- `WRONG_TARGET`
- `UNCERTAIN`

`WRONG_TARGET` is important: it tells us that the extracted FoC-derived target behavior itself does not represent the product the owner wants.

Optional owner fields:

- decisive note;
- preferred behavior;
- feature to ignore;
- micro-unit boundary correction.

## Review flow

1. Show one micro-unit only.
2. Show its declared editorial function.
3. Show 3–5 most relevant feature comparisons, not every possible feature.
4. Collect owner labels/notes.
5. Continue to next micro-unit.
6. At the end, summarize recurring gaps and owner corrections.
7. Do not aggregate into a scalar quality score.

The summary may say, for example:

- 4 units repeatedly put interpretation before observation;
- 3 target behaviors were marked `WRONG_TARGET` by the owner;
- spoken-load concerns concentrated in transition units.

It may not say:

- candidate quality = 63/100;
- FoC similarity = 71%;
- Writer score = 6.3.

## Trace role

Guided review creates a richer output-side failure surface for later Phase 3 tracing:

`owner-marked micro gap -> exact candidate span -> feature behavior -> failure signature -> white-box trace`

It still does not claim Planner/Writer/root-cause responsibility.
