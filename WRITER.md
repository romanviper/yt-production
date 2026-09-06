# Direct Writer Fast Path

This is the active path when the Owner directly tells you to write P01.

## Do this immediately

1. Read only:
   - `products/sumer-writing/02_outline/section-overlays/P01.json`
   - `products/sumer-writing/03_sections/P01/historical-substrate.json`
2. Write **one** Vietnamese historical-podcast draft for P01.
3. Save it to:
   - `products/sumer-writing/03_sections/P01/draft.md`
4. Save minimal metadata to:
   - `products/sumer-writing/03_sections/P01/writer-meta.json`
5. Commit both files on your current Writer branch and stop.

## Owner authority

A direct Owner instruction such as "write P01" is sufficient authority to start writing.

Do **not** wait for `writer-assignment.json`, `assignment.json`, a controller run, a budget, an active production task, a Planner, or another role.

Do **not** revive cancelled tasks or scan for a different assignment.

## Writing constraints

- One content attempt only.
- Use the P01 overlay for the intended audience discovery / angle.
- Use the P01 historical substrate as the factual boundary.
- Do not turn overlapping clay practices into a simple token → envelope → tablet replacement genealogy.
- Do not invent a specific tax/market/tribute/ownership mechanism without evidence.
- Choose the telling freely. Do not force essay structure, hook formulas, beat counts, or self-review.
- Do not read another Writer's draft or Owner feedback before finishing.

The suggested size is roughly 450–650 words, but this is **not** a hard gate. Write the amount needed for a strong readable excerpt.

## Minimal metadata

`writer-meta.json` only needs:

```json
{
  "model": "<actual model if known, otherwise UNKNOWN>",
  "inputs": [
    "products/sumer-writing/02_outline/section-overlays/P01.json",
    "products/sumer-writing/03_sections/P01/historical-substrate.json"
  ],
  "attempt": 1,
  "notes": "<brief issues/uncertainty if any>"
}
```

Timing is optional. No Writer time budget applies.

Do not store chain-of-thought or private reasoning.
