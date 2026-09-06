# Writer Fast Path

If the Owner tells you to write P01, write immediately. Do not wait for any assignment, controller state, budget, active task, Planner, Reviewer, or other agent.

## Read only these two inputs

- `products/sumer-writing/02_outline/section-overlays/P01.json`
- `products/sumer-writing/03_sections/P01/historical-substrate.json`

## Write one attempt

Write one Vietnamese historical-podcast excerpt for P01.

Choose the telling freely. Do not force essay structure, hook formulas, beat counts, or self-review. Do not read another Writer's output or Owner feedback before finishing.

Historical boundaries:

- overlapping clay practices are not a mandatory token → envelope → tablet replacement sequence;
- do not invent a specific tax/market/tribute/ownership mechanism without evidence.

Suggested size is roughly 450–650 words, but this is not a hard gate.

## Save output only here

Use your own partition under:

`writer-output/P01/<writer>/`

For the current Writers:

- Gemini → `writer-output/P01/gemini/`
- GPT-5.6 Sol → `writer-output/P01/sol/`
- GPT-6 → `writer-output/P01/gpt6/`

A new model may create one new short model-name partition under `writer-output/P01/`.

Each partition contains only:

- `draft.md`
- `meta.json`

Do not write the draft into `products/`, `runs/`, or controller folders.

## Minimal metadata

```json
{
  "model": "<actual model if known, otherwise UNKNOWN>",
  "inputs": [
    "products/sumer-writing/02_outline/section-overlays/P01.json",
    "products/sumer-writing/03_sections/P01/historical-substrate.json"
  ],
  "attempt": 1,
  "notes": "<brief issue/uncertainty if any>"
}
```

Timing is optional. There is no Writer time budget.

Commit `draft.md` and `meta.json` on your current Writer branch, then stop for Owner reading.

Do not store chain-of-thought or private reasoning.
