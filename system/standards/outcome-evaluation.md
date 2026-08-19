# Outcome Evaluation Standard

Evaluate the draft that exists, not whether it followed one preferred route.

## What to judge

- **Arc contribution:** does the section advance its assigned role?
- **Narrative movement:** does story/understanding change, or does prose mainly restate?
- **Material carries motion:** do objects, actions, processes, failures or consequences carry most movement, with narration adding only what material cannot safely make clear?
- **Outline realization:** does the draft make the approved `audience_experience`/`material_ids` progression happen rather than verbalize the outline's interpretation?
- **Audience agency/readability:** can a non-specialist encounter the raw clue before specialist classification when the draft asks them to infer from it?
- **Narrator stance:** guide/recount/clarify, or repeatedly tell the audience what to see and think?
- **Causal clarity:** can the listener follow pressure → mechanism → consequence where relevant?
- **Voice/scale:** natural spoken Vietnamese; shifts from object/person to institution/system are earned.
- **Semantic economy:** does each major idea land once rather than being shown, interpreted, paraphrased and summarized again?
- **Guardrail discipline:** are evidence limits mostly silent constraints? Speak them only to prevent a material misconception.
- **Evidence integrity:** no invention, unsupported function/causation, false certainty or disclaimer pile.

## Audio reconstruction test

Do not ask only “would the listener understand with the screen off?” A lecture can pass that test.

After each major stretch ask:

> Can the listener recount what they just pictured **existing, being done, changing, failing or producing a consequence**?

If the listener can mainly say “the narrator explained that X means Y,” flag `expository_reconstruction_failure` even when the prose is accurate and clear.

This is not a demand for scenes or events. A documented object, long process, contrast, failure or reconstruction sequence can pass if audio gives the listener reconstructable reality to follow.

## Failure patterns

Flag document-mode when a stretch is dominated by narrator-run `observe → interpret → qualify → conclude`.

Flag explanatory echo when the draft does `show X → explain X → paraphrase X → summarize X` without a new fact, boundary or consequence. Deletion test: if removing a sentence preserves the same understanding and evidence limit, it is likely redundant. Do not impose a numeric cut target.

Repeated meta-narration such as “điều đáng chú ý” or “chính ở đây chúng ta thấy” is a warning, not an automatic violation. Flag it when narration describes how the audience should process the story instead of letting material/consequence produce the shift.

Flag pseudo-agency when expert classification is supplied first and the resulting inference is staged as audience discovery. Remove the classification: can a casual listener still identify the raw clue?

## Diagnose the layer

- `prose_execution`: outline/material/evidence are sufficient; wording, pacing, redundancy, narrator stance or use of reconstructable detail failed.
- `product_architecture`: movement, material selection or section boundary cannot produce the intended experience.
- `evidence`: required reconstructable detail or claim support is missing, contradicted or insufficient.

With no active story-plan design layer, do not use `local_design` as a default rescue bucket. Route the issue to the layer that actually made the decision: draft, outline or research.

Give an observable acceptance test. Do not create a global writer rule for a one-off failure.
