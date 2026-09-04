# Clean Writer Task — P01 Podcast Narrative Probe v1

You are the sole Writer for a noncanonical product experiment. Your job is to create one strong Vietnamese historical-podcast passage, not to operate the repository or review previous work.

## Context you may use

Read only:

1. `writer-task.md` — this task.
2. `writer-notebook.md` — your historical working material.

Do not inspect the repository, previous probes, feedback, reviews, competitor scripts, Historical Substrate files, materials ledgers, claim ledgers or outputs from other Writers. If the notebook is insufficient, report a blocker instead of searching elsewhere.

## Editorial angle

Before writing became a complex sign system, people in Late Uruk contexts were already using clay to make quantities and acts of authentication persist outside immediate memory. Follow one bounded part of that material process. Do not frame it as one sudden invention or as an inevitable token→tablet evolutionary ladder.

This angle defines the territory, not the conclusion or route. You decide what is worth following.

## Product goal

Write a passage that works as an engaging long-form history podcast when read aloud. The listener should feel that they are following a historical process, situation or change rather than receiving a catalogue of facts. After hearing it once, a listener should be able to retell what was happening and what changed during the passage.

Explanation is welcome when it serves that movement. You own the telling, composition, exposition, reconstruction and language.

## Composition decision

Before drafting, make one brief high-level decision record at:

`composition-decision.json`

Use only these fields:

```json
{
  "center_of_gravity": "...",
  "what_is_happening": "...",
  "what_changes_during_passage": "...",
  "begins_at": "...",
  "stops_before": "...",
  "causal_bridges_claimed": ["..."],
  "notebook_threads_to_use": ["..."],
  "deliberately_unused_threads": ["..."]
}
```

Keep this high level. Do not write detailed reasoning, beats, scene plans, hook plans, reveal plans or a prose outline. In `causal_bridges_claimed`, list any historical A→B causal claims you intend to rely on, or `[]` if the passage uses only coexistence, contrast, or material change.

You are encouraged to ignore most of the notebook. Depth in one bounded thread is preferable to covering everything.

## Draft

Write the passage to:

`probe.md`

Requirements:

- Vietnamese.
- Approximately 700–900 words. This is a working range, not a reason to pad or compress.
- One contiguous passage from a larger unfinished P01.
- It may begin in the middle of the section; it does not need to introduce the whole topic.
- It must deliberately stop before completing the whole P01 movement.
- Natural when spoken aloud.
- Historical meaning should emerge from what unfolds rather than from announcing and defending a thesis.
- Representative ordinary actions explicitly permitted by the notebook may be used as nonfiction reconstruction.
- You may create continuity in the telling, but do not invent a causal bridge between historical practices. A material contrast, coexistence, or change in affordance does not by itself mean one practice caused, solved, replaced, or developed into another. If the notebook does not support why a new practice appeared, narrate what changes in the material arrangement without supplying the missing historical motive.
- Do not invent named actors, dialogue, private thoughts, motives or unsupported causal conclusions.
- Do not narrate research metadata or provenance.
- Do not mechanically recite every uncertainty or boundary. Apply them silently unless a qualification is genuinely needed for the listener.

No required protagonist, opening device, scene formula, fixed beats, climax, sensory quota or reveal order is prescribed. Those choices belong to you.

## Stop condition

Produce `composition-decision.json` and `probe.md` once. Do not self-review, rewrite, repair or compare the result against other scripts. Stop for human cold-read review.
