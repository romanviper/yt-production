# Operation — Historical Substrate

## Responsibility

Convert approved evidence authority into a bounded **model of the historical world**. This operation owns historical practices, object affordances, relations, changes, roles and states supported by evidence. It does not write narration and does not decide how a story should be told.

```text
Evidence Authority
→ Historical Substrate
→ Outline historical territory / change
→ Writer narration
→ Evidence Review
```

## Native representation

Schema v2 is world-shaped, not a claim deck. Each ordinary record contains a structured `world` object appropriate to its `kind`:

```text
practice
  participants
  operation
  object_or_medium
  information_or_relation_handled
  context

object_affordance
  object
  permits
  carries
  constrains

relation
  left
  relation
  right
  temporal_scope
  qualification

change
  dimension
  earlier_state
  later_state
  coexistence
  qualification
```

Other supported kinds (`state`, `process`, `actor_role`) must still carry structured historical data. Do not create a giant ontology merely to fill fields.

`statement` is an optional human-readable rendering. It is **not** the canonical semantic payload: removing statements must leave the historical relationships intelligible from `world`.

Each record also preserves epistemic status, time/place scope, claim IDs, reviewed source refs/locators and non-narrative boundaries.

## Truth-only constraints

Historiographical/evidence-state limits do not belong in Writer-facing historical primitives. Put them in top-level `constraints`, with:

- `rule`;
- `applies_to` historical record IDs;
- claim/source provenance.

Writer projection exposes applicable constraint rules as boundaries, not as historical events/facts to narrate.

## Forbidden authority

Historical Substrate is not a story plan. Records must reject opening, hook, ending, carrier, protagonist, scene, beat sequence, reveal order, climax, emotional turn, camera language, recommended order, story role or narrative route.

Do not choose an artifact because it would make a good opening. An object belongs here only when its historical affordance is source-backed.

## Epistemic boundary

`unknown` means Writer may not invent an answer; it does not mean narration must announce the unknown. `contested` constrains certainty; it does not require a historiographical aside.

Use `documented`, `qualified_inference`, or `bounded_reconstruction`. Reconstruction may describe ordinary operations only inside approved conditions; never invent names, dialogue, motives, unsupported chronology or causal conclusions.

## Coverage and output

Write `01_research/historical-substrate.json` using `scripts/historical_substrate_contract.py` schema version 2.

A normal new product uses `coverage.mode: product`. A bounded migration may use `section_migration` and list only the migrated sections. Section materialization requires coverage for the requested section; whole-outline creation requires product-complete coverage.

Validate with:

```text
python scripts/historical_substrate.py validate <product>
python scripts/historical_substrate.py validate <product> --require-product-complete
```

## Stop conditions

Block instead of filling gaps when a needed historical primitive has no approved authority; when only a truth/evidence boundary is supportable; when chronology, actor identity, institution, motive or causality would have to be invented; or when a proposed field is actually narrative choreography.
