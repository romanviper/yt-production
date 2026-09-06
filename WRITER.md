# Writer Harness — observable direct-output MVP

The Owner needs to see not only **what you wrote**, but also **what you actually did to turn the inputs into that draft**.

If the Owner tells you to write P01, write immediately. Do not wait for an assignment, controller state, budget, Planner, Reviewer, or other agent.

This harness does **not** decide whether your writing is good or bad. Do not emit PASS/FAIL, scores, or a verdict. Your job is to leave enough factual, human-readable evidence for the Owner to make that judgment.

Do not store chain-of-thought, private reasoning, hidden scratchpad, or an internal-monologue transcript. Record only observable facts, final decisions, brief stated rationales tied to inputs/constraints, material changes, uncertainties, and the resulting artifact.

## Inputs

For P01, read these two canonical inputs:

- `products/sumer-writing/02_outline/section-overlays/P01.json`
- `products/sumer-writing/03_sections/P01/historical-substrate.json`

If you access any other repo file or external source before finishing the draft, disclose it in `meta.json` and `writing-report.md`. Do not read another Writer's output or Owner feedback before finishing.

## Output partition

Use your own partition:

`writer-output/P01/<writer>/`

Current partitions:

- Gemini → `writer-output/P01/gemini/`
- GPT-5.6 Sol → `writer-output/P01/sol/`
- GPT-6 → `writer-output/P01/gpt6/`

A new model may create one short model-name partition.

Each completed Writer attempt must contain exactly these three artifacts:

- `draft.md` — the prose the Owner will read
- `meta.json` — compact factual execution metadata
- `writing-report.md` — human-readable trace of the writing behavior

Do not write the draft into `products/`, `runs/`, or controller folders.

## Execution sequence

Follow this sequence so the Owner can distinguish intention from outcome.

### 1. Start `writing-report.md` before drafting prose

Write only the **PRE-WRITE SNAPSHOT** sections shown below. Keep them concise. This is not a formal Planner artifact and must not become an essay outline.

### 2. Write one draft attempt

Write one Vietnamese historical-podcast excerpt for P01.

Choose the telling freely. Do not force essay structure, hook formulas, beat counts, or a generic explanatory template.

Historical boundaries:

- overlapping clay practices are not a mandatory token → envelope → tablet replacement sequence;
- do not invent a specific tax/market/tribute/ownership mechanism without evidence.

Suggested size is roughly 450–650 words, but this is not a hard gate.

### 3. Freeze the draft

Once `draft.md` is complete, do not rewrite or reroll it based on the reporting step. The report must describe the draft that actually existed at completion, not an improved second attempt.

### 4. Finish `writing-report.md`

Append the **POST-WRITE TRACE** sections below. You may inspect your own finished draft for reporting purposes, but do not change it afterward.

### 5. Write `meta.json`, commit the three files, then stop

There is no Writer time budget. Timing is telemetry only. Never fabricate unknown timing/model/session information; use `UNKNOWN` or `null`.

---

# `meta.json` contract

Keep metadata factual and compact. The Owner should be able to understand it without knowing the controller architecture.

```json
{
  "schema": "writer-observability-v1",
  "writer": "<partition name, e.g. sol>",
  "model": "<actual model if known, otherwise UNKNOWN>",
  "task": "P01",
  "attempt": 1,
  "owner_instruction": "<short literal/faithful summary of the instruction that started this attempt>",
  "branch": "<current branch if known, otherwise UNKNOWN>",
  "starting_commit": "<HEAD before this attempt if known, otherwise UNKNOWN>",
  "inputs_read": [
    "products/sumer-writing/02_outline/section-overlays/P01.json",
    "products/sumer-writing/03_sections/P01/historical-substrate.json"
  ],
  "extra_context_accessed": [],
  "other_writer_outputs_read": false,
  "owner_feedback_read_before_draft": false,
  "rerolled": false,
  "draft_word_count": 0,
  "timing": {
    "seconds": null,
    "source": "UNKNOWN"
  },
  "outputs": [
    "draft.md",
    "writing-report.md"
  ]
}
```

If a boolean cannot be truthfully known, use `null` rather than guessing.

---

# `writing-report.md` contract

Use these headings in this order. Prefer tables/bullets over long prose. The purpose is traceability, not self-justification.

## PRE-WRITE SNAPSHOT

### 1. Task I am executing

In 1–3 sentences, state what you believe the Owner asked you to produce.

### 2. Audience discovery I intend to create

State the main thing you want the listener to realize or discover by the end. Do not describe whether this is a “good” choice.

### 3. Intended narrative approach

Record the final pre-draft choices only:

- intended opening;
- central narrative spine/question;
- intended ending or destination;
- point of view / narrator stance if relevant.

For each choice, name the input field, substrate ID, or Owner instruction that materially informed it when possible.

### 4. Evidence I expect to rely on

List the specific overlay fields / historical-substrate IDs you expect to use, with a one-line description of what each is for.

### 5. Constraints I am actively carrying

List only constraints that you expect to materially affect the prose. Include any conflict or ambiguity you already see. Do not invent hidden requirements.

---

## POST-WRITE TRACE

### 6. Actual draft map

Map the finished draft by paragraph or short passage.

| Draft location | What this passage is doing | Source / substrate IDs used | Content type |
| --- | --- | --- | --- |
| ¶1 | ... | HS-P01-... | sourced fact / inference / narrative framing / creative reconstruction |

The Owner should be able to follow the draft from top to bottom using this table.

### 7. Source → prose trace

For every **material historical claim, concrete scene/detail, or causal bridge**, show where it came from.

| Draft location or short phrase | Source/basis | What the source supports | What I added or transformed |
| --- | --- | --- | --- |
| ... | HS-P01-0004 | ... | compressed wording / inference / framing / none |

Do not claim a source supports more than it actually does.

### 8. Creative additions and inference

Explicitly list material content in the draft that is not directly stated by the two inputs. Classify each item as one of:

- `CONSERVATIVE_INFERENCE`
- `NARRATIVE_FRAMING`
- `CREATIVE_RECONSTRUCTION`
- `UNSUPPORTED_OR_UNCERTAIN`

If there are none, say `None`.

### 9. Constraints actually applied

For each material constraint, state its observable effect on the draft and point to the affected paragraph/passage.

Also list any instruction you knowingly did **not** apply, with a brief factual explanation.

### 10. Material changes from the pre-write snapshot

If the actual draft differs from the intended opening, spine, evidence use, or ending, record the difference:

| Planned | Actually written | Observable reason/input that caused the change |
| --- | --- | --- |
| ... | ... | ... |

This is a summary of the change, not a transcript of internal reasoning.

If nothing materially changed, say `No material change`.

### 11. Uncertainty and evidence gaps

List places where:

- the source did not permit a stronger claim;
- you were unsure how far an inference could go;
- you deliberately omitted a detail because evidence was insufficient;
- two instructions appeared to pull in different directions.

Point to the relevant draft location and source/constraint.

### 12. Self-observed output risks

Do **not** score the draft or declare it successful/failed. Simply point out passages that, from your own inspection, may exhibit observable risks such as:

- exposition/essay-like explanation;
- weak narrative movement;
- abstraction instead of concrete action/object/process;
- over-compression;
- repetitive explanation;
- historical overreach;
- excessive caution that flattened the narrative;
- an instruction that visibly distorted the prose.

Use paragraph numbers or short phrases so the Owner can inspect the same place.

### 13. Execution disclosure

State:

- any repo files beyond the two canonical inputs that you read;
- any external source/search used;
- whether another Writer output was visible/read;
- whether Owner feedback on another draft was visible/read;
- whether you produced more than one prose attempt;
- timing if actually observable, otherwise `UNKNOWN`.

Then stop. Do not review another Writer, rank models, rewrite the draft, or modify the harness.
