# P01 Historical Substrate migration

Status: `architecture_ready_for_fresh_writer_probe`

Source feedback: `probe-4-feedback.md` on `codex/foc-editorial-probe3`.

## Why the approved outline file is not rewritten in this migration

The current C003 outline is already human-approved and its hash is part of every materialized section lineage. Rewriting the whole approved outline merely to replace P01's legacy question-shaped `mission` and evidence-shaped `historical_change` would invalidate unrelated P02–P08 artifacts and silently turn a P01 architecture experiment into a whole-product re-approval.

Therefore this migration uses an explicit bounded bridge:

- system `outline` contract is changed for future/newly revised sections;
- P01 `section.json` carries `historical_substrate_contract_version: 1`;
- P01 `mission` is retained only as a declarative compatibility alias;
- P01 `historical_territory` and `historical_change` are historical-world contracts;
- P01 binds to the approved-evidence Historical Substrate records;
- Writer receives `03_sections/P01/historical-substrate.json` as the principal historical input;
- the existing `narration-pack.json` remains an evidence-authority/broker artifact and is no longer the native representation Writer authors from.

A future whole-outline rebuild must compile product-complete Historical Substrate first and then write the new contract directly into the outline.

## Feedback-v4 stop conditions

1. First-class Historical Substrate contract exists: **yes** — `scripts/historical_substrate_contract.py`.
2. P01 compiled from already approved evidence: **yes** — `01_research/historical-substrate.json`.
3. Claim/source authority preserved: **yes** — every canonical record carries claim IDs, reviewed source refs and limitations; validator rejects authority widening.
4. No narrative choreography in substrate: **yes** — executable forbidden-field contract rejects hook/carrier/scene/beat/reveal/climax/ending/story order fields.
5. Writer uses substrate as primary historical input: **yes** — `draft_section` registry requires section Historical Substrate; the evidence broker remains separate.
6. Raw evidence retrieval is verification, not discovery: **yes** — Writer operation contract changed accordingly.
7. P01 historical change is historical-practice/world change: **yes** — section state no longer begins from “Bằng chứng Late Uruk…”.
8. Mission no longer structurally asks Writer to answer a question: **yes** — P01 compatibility mission is declarative; future outline contract separates historical territory/change/discovery.
9. No compensating narrative-style rules added: **yes** — no scene, character, sensory, pacing, carrier or FoC-imitation prescription was added.

## What remains intentionally frozen

- approved P01 claim/source truth ceiling;
- research corpus;
- creative-boundaries policy;
- no prescribed artifact, scene, carrier, opening or reveal order;
- no Probe 1/2/3 prose is promoted into Writer input.

## Next experiment

Only now is a fresh Probe 4 Writer task architecturally valid. Its purpose is not to make prose “more narrative.” It is to test whether Writer behaves differently when the principal historical input is a bounded model of historical reality rather than an evidence representation.
