# Orchestrator Handoff — P01 Podcast Narrative Probe v1

## Purpose

Run one product-quality experiment whose success criterion is a clearly better historical-podcast passage, not cleaner architecture or broader CI coverage.

Base commit: `d1cd03123e8dd5d59c85b6df027e7ed2916836a6`
Branch: `codex/p01-podcast-narrative-probe-v1`

Canonical architecture is frozen for this experiment. Do not modify harness, runtime, Historical Substrate contracts, material schemas, outline contracts or legacy tests.

## Fresh Writer requirement

Create a fresh Writer with no exposure to rejected probes, A/B/C diagnostics, architecture discussion, evaluator diagnoses, competitor prose or this handoff.

The Writer receives exactly these two task-local files:

- `products/sumer-writing/03_sections/P01/probes/podcast-narrative-v1/writer-task.md`
- `products/sumer-writing/03_sections/P01/probes/podcast-narrative-v1/writer-notebook.md`

Do not additionally inject `materials.json`, `historical-substrate.json`, `section.json`, evidence packs, claim ledgers, reviews or previous drafts.

The current coordinating agent may prepare files and verify scope but must not write the prose on behalf of the fresh Writer.

## Expected Writer outputs

Inside the same experiment directory:

- `composition-decision.json`
- `probe.md`

The composition record must remain high-level only. The probe should be approximately 700–900 Vietnamese words and remain a contiguous unfinished passage from P01.

## Execution policy

Run the Writer once. No evaluator feedback, repair loop, self-critique, rewrite or second Writer pass before human review.

Do not make broad CI success a prerequisite for this prose experiment. Only verify that:

- the Writer used only the two allowed input files;
- no prior probe or feedback text entered the Writer context;
- output paths are scoped to this experiment directory;
- the Writer did not modify canonical product or system files.

If the Writer reports that the notebook is insufficient, preserve that blocker as the experiment result. Do not silently expose additional research context.

## Human gate

After the two Writer outputs are committed, stop. The owner will perform cold-read review.

Do not pre-score the prose for the owner and do not repair it. The key question is whether this input environment produces a different class of product: engaging historical narration with forward movement and retellable change, rather than merely a more polished explanation.

## Non-goals

- no new architecture layer;
- no Historical Substrate v3;
- no unit-test cleanup;
- no compatibility work;
- no canonical P01 draft replacement;
- no competitor imitation;
- no attempt to prove a single-variable causal result.

This is deliberately a maximum-quality product probe. If it succeeds, later work may isolate which parts deserve canonicalization.
