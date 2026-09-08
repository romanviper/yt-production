# Writer Harness — compression-first MVP

The immediate goal is to make the **story itself easy for the Owner to inspect before prose is written**.

If the Owner tells you to write P01 or start Writer round 1, begin immediately. Do not wait for an assignment, controller state, budget, Planner, Reviewer, or other agent.

Round 1 produces a **narrative compression**, not listener-facing prose.

The Owner will decide whether the compression is ready. Only a later, separate Owner order may ask a Writer to expand an approved compression into prose.

Do not store chain-of-thought, private reasoning, hidden scratchpad or internal-monologue transcripts.

## Read these three Writer inputs

1. `products/sumer-writing/02_outline/P01-creative-brief.md` — what product/experience you are making and P01's role in it.
2. `products/sumer-writing/02_outline/section-overlays/P01.json` — bounded section territory/change/discovery.
3. `products/sumer-writing/03_sections/P01/historical-substrate.json` — historical reality model and claim boundaries.

The creative brief already distills the product/story direction needed for this attempt. Do not reload the old workflow or legacy task contexts merely to reconstruct those goals.

Do not read another Writer's output or Owner feedback on another Writer before finishing when the Owner wants independent attempts.

## Output

Write exactly one new round-1 artifact in your Writer partition:

`writer-output/P01/<writer>/compression.md`

Do not create `draft.md`, `writing-report.md`, `meta.json`, a plan, scorecard, evaluator output or alternative complete versions for this round unless the Owner explicitly asks.

Existing historical files in the partition may remain untouched.

## What a narrative compression is

A narrative compression is the **smallest readable version of the intended story that still preserves its movement and meaning**.

It is not:

- an outline;
- a bullet list of facts;
- a list of beats or scene instructions;
- a summary of what you intend to write;
- polished podcast prose;
- a methodological explanation of the evidence.

Write it as a condensed retelling in natural Vietnamese. It may use short headings when useful, but the body should read as a story rather than a production document.

The Owner should be able to read the compression and quickly see:

- where the historical world begins;
- what becomes interesting or problematic;
- what question the listener has enough context to naturally care about;
- where explanation is needed and what it resolves;
- what actually changes historically rather than merely being rephrased;
- what consequence or new meaning follows;
- what creates the pull into the next movement.

A useful compression often has a movement such as:

```text
world / situation
→ pressure, change or puzzle becomes visible
→ listener has enough context to want an explanation
→ explanation resolves part of the puzzle
→ a historical consequence or new capability becomes visible
→ the story moves forward
```

This is a diagnostic shape, not a mandatory formula. Do not force every section into identical beats.

## What to optimize for in round 1

### 1. Story before sentences

Do not spend effort making individual lines beautiful. Make the **sequence of meaning** clear first.

If the compression reveals that several steps are only restating the same idea, fix the story structure here rather than hiding repetition inside longer prose.

### 2. Earn explanation

Historical explanation and essay-like exposition are valid and often necessary, especially when explaining how writing functions.

The question is not whether a passage is explanatory. The question is whether the preceding story has given the listener enough context to want that explanation.

Before an explanatory movement, make it possible for the Owner to see why that question has become relevant. Do not manufacture curiosity with a rhetorical question when the story has not earned it.

### 3. Preserve the product promise

This podcast uses the history of writing/cuneiform as the path through which the listener discovers the Sumerian world. Do not reduce the compression to a technical history of sign systems.

When selecting and connecting material, keep both questions alive:

- What changes in how people create, use, learn or transmit writing here?
- What does this use of writing reveal about the Sumerian world?

### 4. Historical movement over conceptual repetition

A compression should make it obvious when the section moves through history, capability, social use, consequence or meaning.

Do not mistake several reformulations of one property — for example durability, inspectability or information storage — for several story developments.

### 5. Evidence boundaries stay backstage

The overlay and historical substrate constrain what may be presented as history. They do not need to dominate the compression.

Do not invent unsupported commodities, transactions, named actors, motives, taxes, ownership claims or deterministic causal links. Keep chronological distinctions clear.

If uncertainty itself changes the story, include it naturally. Otherwise let it constrain the telling silently.

## Scope

Unless the Owner explicitly asks for a smaller test, compress the **whole assigned P01 story movement**, not a 450–650-word prose excerpt.

There is no required word count. Use enough space for the Owner to see the complete movement without prose-level expansion.

## Finish

Read the compression once as a whole.

Fix obvious problems that are easier to see at this level: missing setup, premature explanation, repeated meaning, weak causal links, historical jumps, a payoff with no setup, or a next question that has not been earned.

Then freeze `compression.md`, commit it, and STOP for Owner reading.

Do not begin prose on your own, even if the compression seems good to you. Approval and the prose order belong to the Owner.
