# Writer Harness — observable direct-output MVP

The immediate goal is to produce a Writer draft quickly **and make the Writer's observable decisions understandable to the Owner**.

If the Owner tells you to write P01, write immediately. Do not wait for an assignment, controller state, budget, Planner, Reviewer, or other agent.

This harness does not decide whether your writing is good or bad. Do not emit PASS/FAIL, scores, rankings or a verdict. The Owner evaluates the prose.

Do not store chain-of-thought, private reasoning, hidden scratchpad or internal-monologue transcripts. Record only observable facts, final decisions, brief stated rationales tied to the supplied inputs, material changes, uncertainties and the resulting artifact.

## Read these three Writer inputs

1. `products/sumer-writing/02_outline/P01-creative-brief.md` — what product/experience you are making and P01's role in it.
2. `products/sumer-writing/02_outline/section-overlays/P01.json` — bounded section territory/change/discovery.
3. `products/sumer-writing/03_sections/P01/historical-substrate.json` — historical reality model and claim boundaries.

The creative brief already distills the approved product brief, benchmark, channel/story/voice direction needed for this attempt. Do not load the old workflow or legacy task contexts just to reconstruct those goals.

If you access any other repo file or external source before finishing the draft, disclose it in `meta.json` and `writing-report.md`. Do not read another Writer's output or Owner feedback on another Writer before finishing.

## Output partition

Use your own partition:

`writer-output/P01/<writer>/`

Current partitions:

- Gemini → `writer-output/P01/gemini/`
- GPT-5.6 Sol → `writer-output/P01/sol/`
- GPT-6 → `writer-output/P01/gpt6/`

A new model may create one short model-name partition.

Each completed attempt contains exactly:

- `draft.md` — listener-facing prose;
- `meta.json` — compact factual execution metadata;
- `writing-report.md` — Owner-readable trace of the writing behavior.

Do not write the draft into `products/`, `runs/` or controller folders.

## Execution sequence

### 1. Write the PRE-WRITE SNAPSHOT first

Create `writing-report.md` and fill only the PRE-WRITE sections below **before drafting prose**. Keep this concise. It is not a Planner artifact.

### 2. Write one draft attempt

Write one Vietnamese historical-podcast excerpt for P01.

The goal is not merely to explain the substrate correctly. Use the creative brief to create the intended listener experience and section state change while remaining inside the evidence boundaries.

Choose the telling freely. Do not force essay structure, hook formulas, beat counts or a generic explanatory template.

Suggested size is roughly 450–650 words for this learning excerpt, but this is not a hard gate.

### 3. Freeze the draft

Once `draft.md` is complete, do not rewrite or reroll it because of observations made while filling the report. The report must describe the draft that actually existed at completion.

### 4. Finish the POST-WRITE TRACE

Inspect your frozen draft and append the POST-WRITE sections. Do not change the draft afterward.

### 5. Write `meta.json`, commit the three files, stop

There is no Writer time budget. Timing is telemetry only. Never fabricate unknown model/session/timing information; use `UNKNOWN` or `null`.

---

# `meta.json` contract

Keep metadata factual and compact.

```json
{
  "schema": "writer-observability-v2",
  "writer": "<partition name>",
  "model": "<actual model if known, otherwise UNKNOWN>",
  "task": "P01",
  "attempt": 1,
  "owner_instruction": "<short faithful summary of the instruction that started this attempt>",
  "branch": "<current branch if known, otherwise UNKNOWN>",
  "starting_commit": "<HEAD before this attempt if known, otherwise UNKNOWN>",
  "inputs_read": [
    "products/sumer-writing/02_outline/P01-creative-brief.md",
    "products/sumer-writing/02_outline/section-overlays/P01.json",
    "products/sumer-writing/03_sections/P01/historical-substrate.json"
  ],
  "extra_context_accessed": [],
  "other_writer_outputs_read": false,
  "owner_feedback_on_other_writer_read_before_draft": false,
  "rerolled": false,
  "draft_word_count": 0,
  "timing": {
    "seconds": null,
    "source": "UNKNOWN"
  },
  "outputs": ["draft.md", "writing-report.md"]
}
```

If a fact cannot be known truthfully, use `UNKNOWN`/`null` rather than guessing.

---

# `writing-report.md` contract

Use these headings in order. Prefer bullets/tables over long prose. The purpose is traceability, not self-justification.

## PRE-WRITE SNAPSHOT

### 1. Task I am executing

In 1–3 sentences, state what the Owner asked you to produce.

### 2. Product story and P01 role as I understand them

State, in your own words:

- what larger story this podcast is telling;
- what P01 contributes to that story;
- what would be lost if P01 became only an explanation of archaeological caution.

Tie this to `P01-creative-brief.md` rather than inventing a new product goal.

### 3. Listener state change I intend to create

Record:

- listener entry state;
- listener exit state;
- what you want the listener to become curious about next;
- any feeling/stake you intend to create **only if the supplied material can support it**.

This is more than a factual conclusion. It describes the intended audience experience.

### 4. Storytelling functions and narrative approach I intend to use

Record the final pre-draft choices:

- intended opening;
- central narrative spine/question;
- intended ending/destination;
- point of view/narrator stance if relevant;
- which useful long-form narrative functions from the creative brief you actually intend to use (for example causal movement, material anchor, human presence, scale change, evidence-earned consequence).

For each major choice, name the creative-brief clause, overlay field, substrate ID or Owner instruction that materially informed it when possible.

### 5. Evidence I expect to rely on

List the overlay fields / historical-substrate IDs you expect to use and what each is for.

### 6. Boundaries I am carrying — and how I intend to keep them backstage

List only material evidence/claim boundaries.

For each one, state how it will affect the telling:

- `OMIT_UNSUPPORTED_DETAIL`
- `BRIEF_QUALIFIER_IN_PROSE`
- `REPORT_ONLY`
- `NARRATIVELY_RELEVANT_UNCERTAINTY`

Do not assume a boundary deserves listener-facing explanation merely because it exists.

---

## POST-WRITE TRACE

### 7. Actual draft map

Map the frozen draft from top to bottom.

| Draft location | What this passage is doing for the listener | Source / substrate IDs used | Content type |
| --- | --- | --- | --- |
| ¶1 | ... | HS-P01-... | sourced fact / inference / narrative framing / creative reconstruction |

### 8. Product goal → prose trace

Show where the larger product goal and P01 role actually became visible in the draft.

| Intended product/section function | Draft location | What the listener actually receives |
| --- | --- | --- |
| establish the historical problem before “writing” | ¶... | ... |
| create forward pull into the next question | ¶... | ... |

If a goal from the PRE-WRITE snapshot never became visible, say so. Do not mark it PASS/FAIL.

### 9. Source → prose trace

For every material historical claim, concrete scene/detail or causal bridge, show its basis.

| Draft location or short phrase | Source/basis | What the source supports | What I added or transformed |
| --- | --- | --- | --- |
| ... | HS-P01-0004 | ... | compression / inference / framing / none |

Do not claim a source supports more than it does.

### 10. Creative additions and inference

List material content not directly stated by the historical inputs and classify it:

- `CONSERVATIVE_INFERENCE`
- `NARRATIVE_FRAMING`
- `CREATIVE_RECONSTRUCTION`
- `UNSUPPORTED_OR_UNCERTAIN`

If none, say `None`.

### 11. Evidence boundaries as they appeared in the draft

For each material boundary, record what actually happened:

| Boundary | Handling | Draft location if listener-facing | Did the boundary become methodological exposition? |
| --- | --- | --- | --- |
| ... | omitted / qualified / narrated | ¶... / N/A | yes / no |

This section exists so the Owner can see whether evidence discipline silently protected accuracy or leaked into the listener-facing script.

### 12. Material changes from the PRE-WRITE snapshot

| Planned | Actually written | Observable reason/input that caused the change |
| --- | --- | --- |
| ... | ... | ... |

If nothing materially changed, say `No material change`.

### 13. Input limitations versus Writer choices

Keep these separate.

**Input limitations:** identify missing historical material that constrained possible human action, pressure, consequence, scene detail or causal movement.

**Writer choices:** identify places where richer telling was possible within the supplied material but you chose a more explanatory, abstract or cautious route.

Do not use input limitations as a blanket defense of the draft.

### 14. Self-observed output risks

Do not score or declare success/failure. Point to inspectable passages that may show risks such as:

- exposition/essay-like explanation;
- weak narrative movement;
- product goal disappearing behind a narrower factual point;
- abstraction instead of concrete action/object/process;
- missing human presence where evidence allowed it;
- scale that never moves;
- over-compression or repetition;
- historical overreach;
- excessive caution flattening the narrative;
- evidence boundaries leaking into methodological narration;
- an instruction visibly distorting the prose.

Use paragraph numbers or short phrases.

### 15. Execution disclosure

State:

- repo files beyond the three Writer inputs that you read;
- external source/search used;
- whether another Writer output was visible/read;
- whether Owner feedback on another Writer was visible/read;
- whether you produced more than one prose attempt;
- timing if actually observable, otherwise `UNKNOWN`.

Then stop. Do not review another Writer, rank models, rewrite the frozen draft or modify the harness.