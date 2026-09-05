# Historical Substrate v2 architecture feedback

Status: `changes_requested_before_fresh_writer_probe`

Reviewed branch: `codex/foc-editorial-historical-substrate-v2`

Reviewed head: `bebec13a0a7a5122b04b4d2aaccd7610453e720b`

Architecture decision baseline: `8e4142ebf3d3caa4faff698805a342811b824430`

## Decision

The architecture direction is approved, but the current implementation is not yet coherent enough to run a fresh Writer probe.

Do not respond to this review by adding more narrative, scene, character, pacing, hook, carrier, sensory-detail or anti-essay instructions to Writer.

The main remaining problems are architectural/runtime mismatches:

```text
operation docs say Historical Substrate is canonical
        ↓
executable contracts and packet runtime still partly behave as before
        ↓
manual P01 migration compensates for those mismatches
        ↓
Writer could receive a context that is valid-looking but not reproducible from canonical state
```

The purpose of this correction round is to make the new architecture executable end-to-end before evaluating prose again.

## What is already correct and should be preserved

Do not reopen these decisions unless a correctness failure requires it.

1. Historical Substrate is a first-class layer between evidence and authorship.
2. Product-level substrate records retain claim/source authority while Writer-facing projection hides claim IDs and source refs.
3. Historical uncertainty is represented as authority/boundary rather than mandatory narration.
4. Outline is conceptually responsible for historical territory/change, not local storytelling choreography.
5. Writer evidence access is intended to be secondary verification rather than the native story substrate.
6. Reviewer carries the burden of mapping prose back to evidence authority.
7. `audience_discovery` / `earned_meaning` must not prime Writer with a thesis.
8. Historical Substrate must reject hook/carrier/scene/beat/reveal/climax/ending/story-route authority.
9. Do not prescribe a specific artifact, scene, protagonist, opening or reveal order for the next probe.

## P1 — Canonical P01 state is split between approved outline and manual section migration

`03_sections/P01/section.json` now contains the new architecture:

- declarative `historical_territory`;
- historical-world `historical_change`;
- `historical_substrate_ids`;
- declarative compatibility `mission`.

But canonical `02_outline/outline.json` still contains the old P01 contract:

- question-shaped `mission`;
- evidence-shaped `historical_change.from` beginning with surviving evidence;
- no `historical_territory`;
- no `historical_substrate_ids`.

At the same time, the new materializer treats outline sections as the source from which section state is generated and validates section binding against Historical Substrate.

This creates two competing sources of truth:

```text
approved outline → old P01 architecture
manual section migration → new P01 architecture
```

The current section state is therefore not canonically reproducible.

### Required correction

Choose one explicit architecture for bounded migrations and enforce it in code.

Two acceptable directions:

**A. Canonical section overlay**

Introduce a first-class, hash-bound section migration/overlay artifact whose authority is explicitly resolved after the approved outline and before section materialization. The materializer and validator must understand this overlay; manual `section.json` replacement is not sufficient.

or

**B. Canonical outline amendment**

Amend P01 in the outline under an explicit bounded re-approval/migration mechanism that does not silently rewrite unrelated P02–P08 authority.

The exact mechanism is open. The invariant is not:

```text
outline says A, section.json silently says B
```

A fresh Writer task must be reproducible from canonical architecture inputs without hand-editing section state.

## P1 — `section_migration` exists in schema/docs but current materializer requires product-complete substrate

The product Historical Substrate currently uses:

```text
coverage.mode = section_migration
covered_sections = [P01]
```

But direct-authorship materialization calls Historical Substrate validation with product-complete coverage required before processing sections.

Therefore the documented bounded migration mode cannot pass the normal materialization path.

### Required correction

Make lifecycle semantics match the contract.

A bounded P01 migration should be able to materialize P01 while refusing operations that genuinely require product-complete substrate, such as rebuilding the entire new outline.

Conceptually:

```text
materialize one migrated section
→ require substrate coverage for that section

create/rebuild whole outline
→ require product-complete substrate
```

Do not bypass the materializer by maintaining a manually generated P01 state.

Add an integration test proving that `coverage.mode=section_migration` can materialize its declared section and cannot masquerade as product-complete coverage.

## P1 — Runtime still tells Writer to discover story material from evidence

`system/operations/draft-section.md` now correctly says:

```text
Historical Substrate is primary.
Choose a telling from history.
Use evidence broker afterward for verification/specificity/qualification.
```

However the shared runtime header produced by `context_packet.py` still tells tasks with evidence access to use the broker to:

```text
discover story material as well as verify facts
who or what acts
what happens
where
what object or trace is present
...
```

That restores the exact evidence→story coupling Historical Substrate was introduced to remove.

### Required correction

Change runtime routing, not Writer prose rules.

For canonical Historical Substrate draft/revise tasks, evidence access should be described only as secondary verification/sharpening for a telling already chosen from substrate.

Do not tell Writer to survey evidence to discover what history exists to tell.

If legacy workflows still require the old discovery behavior, branch the runtime semantics by architecture version rather than keeping contradictory instructions in one packet.

Add a packet-level test that a canonical Historical Substrate Writer context contains no instruction that evidence is the primary story-discovery substrate.

## P1 — Section Historical Substrate freshness is not a task precondition

The new contract already provides deterministic section projection and `verify_writer_section_substrate()`.

But draft/review/revise task creation currently does not require this verifier to pass.

This is already visible in P01: the checked-in section substrate has authority-binding fields that differ from the current generator's deterministic output shape, yet task preflight can still proceed.

### Required correction

Before creating canonical:

```text
draft_section
review_section
revise_section
```

require:

```text
validate product Historical Substrate authority
validate section binding
verify Writer-facing section Historical Substrate is current and deterministically reproducible
```

If any binding/hash/input changes, refuse task creation until the projection is regenerated.

Historical Substrate must have lifecycle treatment at least as strict as material snapshots and narration-pack provenance.

## P1 — Review runtime drops the Historical Substrate that Reviewer is supposed to evaluate

Registry declares section Historical Substrate as a required `review_section` input.

But canonical review context uses a hard-coded required-input override that does not include `03_sections/{section}/historical-substrate.json`.

Meanwhile `review-section.md` asks Reviewer to diagnose whether exposition was demanded by the substrate or introduced by Writer.

Reviewer cannot perform that architectural diagnosis without seeing the substrate.

### Required correction

Make runtime inputs match the operation contract.

Canonical Reviewer must receive the compact Historical Substrate projection plus the relevant section/outline boundary and evidence authority capability.

Add a context-packet test asserting that Historical Substrate is present in canonical review context.

## P1 — Executable validation has not adopted the new architecture

`validate.py` does not yet enforce the new Historical Substrate lifecycle.

It should validate at least:

- product Historical Substrate against approved claims/sources;
- required coverage mode for the attempted lifecycle stage;
- direct-authorship outline/section binding to substrate;
- section Historical Substrate presence and freshness;
- `historical_substrate_contract_version` where required;
- historical territory/change contract for migrated/current sections.

Similarly, `system/operations/outline.md` documents a new section contract, but `scripts/outline_contract.py` still primarily validates the old schema semantics and does not require the new substrate fields for current migrated output.

### Required correction

Make executable contracts the authority.

Do not rely on operation Markdown to enforce architecture invariants that scripts permit violating.

Add end-to-end validation coverage so the current inconsistent P01 state would fail validation rather than appear ready.

## P2 — Historical Substrate is still too proposition-shaped

This is not a request to remove Historical Substrate. It is the next architectural refinement after runtime coherence.

Current records are structurally close to:

```text
kind
statement
status
time
place
limitations
```

The Writer-facing result is therefore still a flat set of historical propositions.

Examples include propositions conceptually like:

```text
administrative scale coincided with demand for records
feedback between institutions and records is plausible
early records support some classifications more securely than others
```

This is cleaner than an evidence ledger, but its cognitive shape remains close to a claim deck:

```text
statement A
statement B
statement C
→ Writer synthesizes propositions into prose
```

That can still naturally produce explanation-first writing.

### Required architectural direction

Move Historical Substrate toward a world-shaped representation rather than increasingly elaborate prose statements.

Do not build a giant ontology. A small structured schema is enough if the native representation distinguishes historical primitives.

Conceptually:

```text
practice:
  roles / participants when supported
  operation
  object_or_medium
  information_or_relation_handled
  context

object_affordance:
  object
  permits / carries / constrains

relation:
  left
  relation
  right
  temporal_scope

change:
  dimension
  earlier_state
  later_state
  coexistence / qualification

constraint:
  prohibited historical inference
```

`statement` may remain as a human-readable rendering, but it should not be the only semantic representation Writer/Outline tooling can consume.

Acceptance test:

> Removing the rendered `statement` strings should not destroy the native historical relationships represented by the substrate.

If all meaning disappears when `statement` is removed, the layer is still primarily a proposition list.

## P2 — Evidence-state propositions must also be rejected inside substrate records

The architecture correctly rejects evidence-shaped `historical_change`, but substrate records themselves can still contain historiographical/evidence-state language.

For example, a record equivalent to:

```text
Early records support identification of accounting contexts more securely than...
```

is a statement about what the corpus permits us to classify, not directly a historical-world primitive.

### Required correction

Apply the evidence-world vs historical-world distinction at substrate-record level too.

When a proposition is purely a truth boundary, represent it as a boundary/constraint associated with historical primitives rather than a Writer-facing historical primitive.

Do not solve this with a larger lexical blacklist alone. Schema placement should carry most of the semantic distinction.

## P2 — P01 substrate selection still looks like claim coverage rather than minimal historical territory

P01 currently selects all nine migrated substrate records, spanning:

- basic recording practices;
- object affordances;
- coexistence/genealogy boundary;
- administrative scale;
- classification limits;
- institutional feedback model;
- the central historical change.

This appears close to:

```text
P01 owns CLM-0011..0018
→ include substrate equivalents of every claim
```

That recreates evidence-coverage pressure one layer later.

### Required correction

Outline should select the minimum historical primitives necessary to make the assigned historical territory/change authorable.

A substrate record is not automatically Writer-facing merely because its supporting claim is in the section's truth ceiling.

Keep the distinction:

```text
claim_ids = what evidence authority permits
historical_substrate_ids = what historical reality this section needs as primary context
```

Secondary facts can remain available through substrate/evidence lookup without becoming default prose pressure.

Add an acceptance test or design review question:

> If this primitive were removed from the default Writer projection, would the historical change cease to be understandable/authorable, or would we merely reduce informational coverage?

If the answer is only coverage, it probably should not be default Writer context.

## P2 — Remove architecture compensation from Writer instructions after runtime is correct

`draft-section.md` currently contains several negative reminders added to defend the new routing, such as not turning substrate into a checklist and not structuring source A → implication → source B.

These are reasonable temporary guardrails while architecture is under construction, but they must not become the mechanism that makes the architecture work.

After runtime and schema boundaries are enforced, re-evaluate whether these local anti-failure instructions are still needed.

The target is:

```text
correct native input + correct authority routing
→ natural Writer behavior
```

not:

```text
same dangerous affordances
+ increasingly specific instructions telling Writer not to use them
```

Do not expand the negative-rule list in this round.

## Required implementation order

Keep the correction sequence diagnostic and separable.

### COMMIT A — Canonical migration/lifecycle authority

- choose and implement a first-class bounded section migration mechanism;
- eliminate silent outline-vs-section authority split;
- support `section_migration` in the materialization lifecycle;
- preserve the approved rest of the product without pretending P01 was generated from the old outline contract.

### COMMIT B — Runtime routing coherence

- canonical draft/revise evidence broker = secondary verification only;
- canonical review packet includes Historical Substrate;
- no contradictory story-discovery language in canonical packets.

### COMMIT C — Substrate provenance gates

- preflight section substrate freshness for draft/review/revise;
- bind deterministic substrate projection into task provenance;
- stale or manually edited projections block task creation.

### COMMIT D — Executable validation integration

- integrate Historical Substrate into `validate.py`;
- align `outline_contract.py` / materializer / registry / operation docs;
- add end-to-end integration tests covering canonical migration → section materialization → Writer packet → Reviewer packet.

At this point run the full repository validation/test suite.

Do **not** create a Writer probe yet if any canonical/runtime mismatch remains.

### COMMIT E — World-shaped substrate schema

After A–D are stable:

- evolve native substrate primitives beyond a flat statement list;
- separate historical-world data from truth-boundary metadata;
- retain provenance and epistemic status;
- preserve route neutrality;
- migrate P01 substrate.

### COMMIT F — Minimal P01 substrate selection

- select only primitives necessary for P01 territory/change;
- keep evidence ceiling broader than Writer primary context when appropriate;
- regenerate P01 Writer projection from canonical inputs.

## Tests required before a fresh Writer probe

At minimum add tests proving:

1. section migration can materialize P01 without product-complete substrate;
2. whole-outline creation still requires product-complete substrate;
3. canonical section state is reproducible from canonical architecture inputs;
4. stale/edited section Historical Substrate blocks task creation;
5. canonical Writer packet contains Historical Substrate as primary historical input;
6. canonical Writer packet does not tell Writer to discover its story by surveying evidence;
7. canonical Reviewer packet contains Historical Substrate;
8. outline/section evidence-shaped historical change is rejected;
9. evidence-only constraint language does not become an ordinary Writer-facing historical primitive;
10. substrate narrative-authority fields remain rejected;
11. section substrate selection does not automatically equal all section claim coverage.

## Fresh Writer probe gate

A new Writer probe is authorized only when all of the following are true:

- one canonical source of P01 architecture exists;
- bounded P01 migration is reproducible through normal lifecycle tooling;
- product and section Historical Substrate validate;
- section substrate projection verifies current;
- Writer packet runtime semantics match Historical Substrate architecture;
- Reviewer can see the same historical model Writer authored from;
- executable validation catches stale/inconsistent substrate state;
- P01 substrate is world-shaped enough that it is not merely a claim list with citations removed;
- P01 default substrate selection is intentionally minimal;
- no new local narrative technique rules were added to compensate for architecture gaps.

## Next experiment after architecture is coherent

Only then create a fresh Writer task with no previous probe prose or feedback in context.

The experiment should test one thing:

> Does Writer behave differently when its actual runtime context is a canonical, world-shaped historical model rather than evidence/claim propositions?

If the next output still collapses into essay-like explanation after these conditions are met, do not expand the evidence/substrate architecture again by default. At that point the primary suspect should move to nonfiction composition planning / Writer objective / model behavior.

## Architectural invariant

```text
Evidence owns what can be supported.
Historical Substrate owns a bounded model of historical reality.
Outline owns which historical movement the section covers.
Writer owns how that history becomes narration.
Reviewer owns evidence integrity and audience outcome diagnosis.
Lifecycle tooling owns which revision of those authorities is actually allowed to run.
```

The last line is now essential. A good conceptual architecture is insufficient if runtime can still execute an older or contradictory authority path.
