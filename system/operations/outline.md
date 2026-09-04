# Operation — Outline

## Responsibility

Design **which historical movement the product and each section cover**, not how Writer must tell it. Author from Historical Substrate, not directly from the research ledger. Do not write narration or pre-author local storytelling mechanics.

Outline owns:

- central question and audience promise at whole-product level;
- whole-product progression and exactly three acts;
- section historical territory;
- historical-world state change;
- entry and exit state;
- section boundaries;
- selected Historical Substrate records;
- evidence authority metadata through `claim_ids`;
- dependencies, continuity, transition and word allocation.

It does not own exact carrier, artifact sequence, imagery sequence, scene, protagonist, narrative route, reveal strategy, paragraph order or local mechanics.

## Historical Substrate boundary

The principal historical input is `01_research/historical-substrate.json`.

For a new whole-product outline, substrate coverage must be product-complete and valid against approved claim/source authority. Evidence records remain the authority behind the substrate, not the native representation from which the outline should discover history.

A section selects history using `historical_substrate_ids`. `claim_ids` remain an evidence ceiling / audit field and must not be treated as facts that all need to appear.

## Section contract

For new or revised direct-authorship sections, separate these concerns explicitly:

- `historical_territory`: a declarative, non-question description of the bounded historical reality this section owns;
- `historical_change`: `from` / `to` states in the historical world or historical practice, never a change in what surviving evidence appears to show;
- `historical_substrate_ids`: the route-neutral historical primitives available to Writer;
- `audience_discovery`: what may become understandable by following the change. This is an owner/reviewer evaluation target and must not be required in Writer context when it would prime a conclusion.

`mission` may remain only as a compatibility alias for `historical_territory`; it must not be an interrogative proposition that naturally asks Writer to produce an explanatory answer.

Do not encode `earned_meaning` as a Writer-facing thesis. Existing legacy fields may remain readable but have no authority over Writer telling.

## Design order

1. Define the whole-product question, promise and final understanding.
2. Use Historical Substrate to identify actual historical movements rather than evidence-comparison opportunities.
3. Design opening, body and ending at macro level.
4. Give each movement an entry/exit state in the historical world.
5. Give each section a declarative historical territory and historical change.
6. Bind each section to enough substrate records to make that change followable without expanding truth.
7. Retain `claim_ids` only as evidence-authority metadata for audit/retrieval.
8. Cut `P##` work units at meaningful state/context/review limits.

Movement count, section count, length and local form remain adaptive.

## Freedom test

A competent Writer should be able to reach the section's historical change through more than one evidence-safe telling. If a section only works with one artifact, carrier, reveal order or scene, the outline has taken narrative authority that belongs downstream.

A second failure mode is evidence-shaped architecture: if the movement reads like “inspect source A → compare source B → state implication,” return to Historical Substrate and define the historical-world movement instead.

## Output compatibility

New/revised direct-authorship output continues to use `script_architecture.writer_authorship_contract_version: 1` for runtime compatibility, but each migrated section must set:

```text
historical_substrate_contract_version: 1
historical_territory
historical_change
historical_substrate_ids
```

Schema v4 keeps whole-script acts/movements, section architecture and word envelope. `story-bible.md` keeps global causal/chronology/term/continuity constraints; `voice-profile.md` keeps product voice. All remain draft until human approval.
