# Operation — Evidence Resolution

## Responsibility

Recover and preserve high-resolution, source-level material affordances for a bounded section from already approved sources, without widening the section's truth ceiling or pre-authoring narrative routes.

When a section's evidence territory contains only abstract claims and propositions, `evidence_resolution` inspects the approved source records and locators to extract concrete historical particulars that allow a writer to author a nonfiction story:
- actual objects, artefacts, tablets, inscriptions, or physical traces;
- documented actions and actors/systems directly supported by the source;
- explicit source sequences (e.g. administrative steps, excavation strata, or inscription order);
- physical descriptions, measurements, and spatial/topographical relations;
- unresolved questions visible in surviving evidence;
- subsequent discoveries or later evidence that changed historical interpretation;
- source genre and temporal distance (`contemporary_material`, `contemporary_interested_account`, `later_copy`, `retrospective_literature`, `cultural_tradition`, `modern_hypothesis`).

`evidence_resolution` owns evidence preservation resolution, **not** story design:
- It does **not** author a story plan, scene, camera angle, opening, or climax.
- It does **not** assign narrative roles or narratability scores.
- It does **not** introduce new claims, new causal conclusions, or synthetic generalizations outside approved research authority.
- If the approved sources cannot support a nonfiction movement, it must stop and report a blocker for owner decision rather than manufacturing historical incidents or inventing details.

## Required inputs

- `02_outline/outline.json`
- `03_sections/{section}/section.json`
- `03_sections/{section}/brief.md`
- `03_sections/{section}/evidence-pack.json`
- `01_research/source-index.json`
- `01_research/claim-ledger.json`

## Optional inputs

- `01_research/material-ledger.json`
- `03_sections/{section}/evidence-resolution-request.md`

## Required outputs

- `03_sections/{section}/materials.json`

## Contract rules

1. Every material record must specify:
   - `id`: namespaced identifier (e.g. `{section}-MAT-###` or global `MAT-####`);
   - `kind`: `object`, `actor`, `place`, `process`, `record`, or `trace`;
   - `label`: neutral descriptive label;
   - `claim_ids`: subset of approved section claims;
   - `source_refs`: source IDs from the section evidence pack with narrow, specific locators;
   - `limitations`: explicit boundaries on what the evidence does and does not prove;
   - `source_relation`: classification of source proximity to the narrated reality.
   - `epistemic_layers`: five explicit lists named `observed`,
     `functional_inference`, `representative_reconstruction`, and
     `qualified_live_hypothesis`, plus `prohibited_or_rejected_inference`.
     Each entry has a `statement`; every
     non-observed entry also has a source-honest `qualification`.
2. Concrete factual affordances must preserve their epistemic layer. A manufacture
   action visible in an artifact may be `documented_action`; a complete workflow
   assembled from several sources is a representative reconstruction, never a
   documented incident. Unknown actors remain unknown; plausible roles are labeled
   inferred. Representativeness claims require a qualified inference and bounded
   source scope—never unsupported `universal`, `standard`, or `canonical`.
   Rejected inference is a red-line surface, not a positive Writer affordance.
3. Output materials must be consolidated into the section territory and available to the writer via the bounded evidence broker.
