# Handoff — three clean Writer diagnostic experiment

Status: `READY_TO_EXECUTE_THREE_CLEAN_WRITERS`

Architecture freeze reference: `149420b97aa73b7e63ea6267462e4005495fe7cb`

## Goal

Run three fresh, isolated Writer executions to determine whether the P01 quality failure comes primarily from:

1. overly compressed/abstract Writer input;
2. missing Writer-owned composition before drafting; or
3. the Writer objective/model behavior itself.

This is a diagnostic experiment, not a production draft and not another architecture iteration.

## Global rules for all three Writers

All three Writers must be genuinely clean.

They must **not** see:

- `probe.md` from `hsub-clean-01`;
- Probe 1/2/3/4 outputs;
- any evaluator review or diagnosis;
- `three-writer-diagnosis-feedback.md`;
- this handoff file;
- competitor prose/scripts;
- another Writer's context, plan, or output.

The coordinating agent may read this handoff. The three Writer agents may receive only their variant-specific task packets.

Keep constant across all three variants:

- section: P01;
- language: Vietnamese;
- target: 450–650 words;
- output is one contiguous passage from a larger unfinished P01;
- do not summarize or complete the whole section;
- same truth ceiling / approved sources;
- same broad P01 historical territory;
- no required scene, protagonist, hook, beat structure, reveal order, climax, sensory quota, or stylistic imitation;
- no prior failed prose as reference;
- use the same Writer model/configuration if the execution system allows it.

Save outputs separately. Do not revise one Writer using another Writer's result.

Suggested experiment root:

`products/sumer-writing/03_sections/P01/probes/three-writer-diagnostic/`

Suggested outputs:

- `writer-a-rich-material.md`
- `writer-b-substrate.md`
- `writer-c-composition.md`
- variant-specific frozen contexts/packets as needed for audit.

Do not write any of these into canonical `draft.md`.

---

## Writer A — rich historical material, direct draft

### Question tested

Is the Historical Substrate projection simply too compressed to support strong prose?

### Input principle

Give Writer A the P01 angle/territory and a **richer source-grounded historical material set** from the already approved evidence universe.

The material should preserve useful factual resolution such as concrete objects, practices, relationships, documented examples, relevant temporal/spatial context, and source-grounded details that a Writer could choose among.

Do not convert that material into an ordered story plan. Do not label items as opening, beat, carrier, reveal, climax, ending, or preferred sequence.

Do not require Writer A to cover all supplied material.

The truth ceiling must remain the same as the canonical P01 authority. This variant changes **resolution available to the Writer**, not factual permission.

### Important

Writer A should draft directly after reading its packet. Do not give it an explicit composition procedure.

Expected diagnostic interpretation:

- A much better than B → strong evidence that the substrate projection is too information-poor/abstract for authorship.
- A similar to B → rich material alone is insufficient.

---

## Writer B — current Historical Substrate control

### Question tested

Provide a clean control for the architecture that produced the latest probe.

### Input principle

Use the current canonical Historical Substrate Writer context:

- P01 territory/change;
- selected substrate IDs `HS-P01-0001`, `HS-P01-0003`, `HS-P01-0004`, `HS-P01-0007`;
- Historical Substrate as primary history model;
- evidence only as secondary verification;
- no old probe text or feedback.

Do not change the Historical Substrate schema or add additional primitives for this variant.

Run a **new** Writer rather than reusing the Writer that produced `hsub-clean-01`.

This is the baseline/control output.

---

## Writer C — rich historical material + Writer-owned composition

### Question tested

Does the Writer need an explicit authorship phase between understanding material and producing prose?

### Input principle

Give Writer C the **same rich historical material and truth ceiling as Writer A**.

Before drafting prose, instruct the Writer to perform a private/task-local composition pass in which it decides for itself what local thread to inhabit and how the passage should progress.

This composition phase belongs to the Writer. Upstream must not prescribe its answer.

The instruction should be functional rather than stylistic. For example, its purpose is to choose a bounded telling from the available history before prose generation, not to satisfy a fixed story template.

Do not require named beats, three-act structure, hook formulas, scene quotas, tension curves, protagonist choice, or any particular narrative method.

If the execution environment requires an auditable artifact, save a **brief composition decision record**, not hidden chain-of-thought. It may contain only high-level choices such as:

- what local historical thread the Writer chose;
- where this passage begins and deliberately stops;
- which supplied material it expects to use or leave unused.

Do not request or preserve detailed reasoning traces.

Then have the same Writer draft the 450–650 word passage from its own composition decision.

Expected diagnostic interpretation:

- C much better than A and B → missing Writer-owned composition is the leading cause.
- A and C both much better than B → material resolution is the leading cause; composition may help but is not necessary.
- C better than B but A weak → composition is more important than simply increasing material volume.
- all three weak → stop iterating evidence/substrate architecture and investigate Writer objective/model behavior.

---

## Material preparation rules for A and C

The coordinating agent may build an experiment-local rich-material packet from existing approved P01 research/evidence sources.

It must not use rejected prose as material.

It must not sneak conclusions from prior evaluator feedback into the Writer packet.

It must not preselect material because it fits a desired scene or story route. Selection should be based on relevance to P01 and usefulness as historical material, while leaving composition ownership to the Writer.

Prefer enough material to offer genuine choice rather than a four-item sequence, but avoid dumping the entire repository or forcing exhaustive coverage.

A and C must receive the same substantive rich-material payload so that their difference isolates the composition phase.

---

## Execution discipline

Run the Writers independently. Recommended order is irrelevant, but do not let later Writers see earlier outputs.

For each variant, record:

- exact context hash or immutable packet;
- model/config identity if available;
- output word count;
- whether evidence lookup was actually used;
- output path.

Do not evaluate or repair an output before all three have completed.

Do not regenerate a variant because it looks bad unless there was a mechanical execution failure. A weak output is experimental evidence.

---

## Human review gate

After all three outputs exist, stop.

Do not let an automated evaluator rewrite them or turn the result into another harness patch.

Present the three raw passages to the owner side by side, anonymized as A/B/C if practical, together with only minimal execution metadata.

The owner should first judge prose cold. Architectural interpretation happens only after that judgment.

No subsequent architecture change is authorized by this handoff.