# Historical Substrate v2 — CI integration stabilization feedback

Status: `changes_requested_before_fresh_writer_probe`

Reviewed branch: `codex/foc-editorial-historical-substrate-v2`

Reviewed head: `18b143b5e7251bf3abb2948ac3a69027577daa06`

Previous architecture feedback: `historical-substrate-v2-feedback.md`

CI evidence: workflow run `33848282571` — Unit tests stopped the workflow before architecture-boundary and product validation stages.

## Decision

Keep the new Historical Substrate architecture. Do not roll back the world-shaped schema, canonical P01 overlay, minimal P01 substrate selection, secondary-evidence routing intent, or stale-substrate preflight.

The current failure is an integration/adoption-boundary failure, not evidence that the Historical Substrate concept is wrong.

However the implementation is not finished. The full unit suite currently reports:

```text
138 tests
5 failures
57 errors
```

Do not create a fresh Writer probe until the repository-wide compatibility and validation path is green.

The dominant failure pattern is:

```text
new Historical Substrate behavior
is inferred from broad existing concepts such as
"direct authorship" or operation == outline
        ↓
legacy/direct-authorship fixtures are forced into the new contract
        ↓
materialization/task creation fails before the behavior under test is reached
```

The correction is to introduce one explicit adoption boundary and route every lifecycle component through it.

## Preserve these completed improvements

The following changes are approved and should not be reopened merely to make tests pass:

1. P01 uses a canonical, hash-bound section overlay instead of silently hand-editing `section.json` against the approved outline.
2. P01 primary Historical Substrate is intentionally minimal rather than mirroring its whole claim ceiling.
3. Historical Substrate v2 uses structured `world` primitives; `statement` is no longer native semantic authority.
4. Evidence-state language is rejected from historical-world primitives.
5. Truth-only constraints are separated from ordinary historical primitives.
6. Section Historical Substrate has deterministic projection and freshness verification.
7. Writer-facing substrate hides claim/source provenance.
8. Evidence lookup is intended to be secondary verification after Writer chooses a telling from substrate.
9. Reviewer is intended to see the same Historical Substrate Writer authored from.

Do not solve CI by reverting these decisions.

# P1 — Historical Substrate adoption boundary is too broad

`materialize_sections.py` currently uses direct-authorship status as the practical switch into Historical Substrate materialization.

This incorrectly collapses two distinct generations:

```text
direct-authorship legacy-compatible

vs

direct-authorship + Historical Substrate contract
```

Many existing tests correctly construct direct-authorship products that predate Historical Substrate. They now fail immediately because `01_research/historical-substrate.json` is absent.

Typical failure:

```text
Direct-authorship materialization requires 01_research/historical-substrate.json.
```

### Required correction

Create one executable helper/contract that answers:

```text
Does this product/cycle/section explicitly adopt Historical Substrate contract v1?
```

Do not infer adoption merely from:

- `is_direct_authorship_outline(outline)`;
- operation name;
- presence of a new module;
- current branch/version.

The adoption marker should be explicit and authoritative at the correct scope. Acceptable implementations include a product/cycle architecture version or `script_architecture.historical_substrate_contract_version`, with bounded section overlay support where needed.

Every relevant component must use the same helper:

```text
materialize_sections.py
context_packet.py
validate.py
outline creation/rebuild routing
section substrate preflight
tests/fixtures
```

Invariant:

```text
not adopted
→ existing direct-authorship compatibility path remains valid

adopted
→ Historical Substrate invariants are mandatory
```

Do not maintain separate ad-hoc interpretations of adoption in each script.

# P1 — Whole-outline task preflight is also over-applied

`context_packet.py` currently performs product-complete Historical Substrate preflight for every `operation == "outline"`.

This breaks legacy/new-cycle/DSH outline tests before their actual behavior can run.

The long-term canonical pipeline may be:

```text
Research
→ Historical Substrate
→ Outline
```

but repository compatibility still requires an explicit adoption boundary.

### Required correction

Only require product-complete Historical Substrate for an outline operation when the current product/cycle explicitly adopts the Historical Substrate outline contract.

Legacy-compatible outline work must remain routable until that architecture version is explicitly upgraded.

Add tests covering both cases:

```text
legacy-compatible outline task
→ no substrate requirement

Historical-Substrate-v1 outline task
→ product-complete substrate required
```

# P1 — Canonical packet routing is patched after legacy compiler validation

The current wrapper calls the legacy compiler first and then replaces legacy evidence-discovery text with canonical secondary-verification text.

This is semantically better than before, but the timing is wrong:

```text
legacy compiler assembles prompt
→ legacy compiler checks instruction budget
→ may fail
→ canonical replacement never happens
```

CI exposes this through prompt-budget failures such as:

```text
creative_draft: 1526 > 1500 instruction tokens
evaluation: 3041 > 2600 instruction tokens
```

### Required correction

Canonical Historical Substrate routing must participate before final prompt assembly and token-budget validation.

Do not fix this by simply raising prompt budgets.

Preferred architecture:

```text
resolve architecture mode
→ resolve canonical instruction/input/routing layers
→ assemble packet once
→ validate prompt budget once
```

A transitional compatibility module is acceptable, but canonical behavior must not depend on exact post-hoc string replacement after legacy compilation.

Also avoid an architecture whose correctness depends permanently on `_LEGACY_DISCOVERY_TEXT` matching an exact paragraph in another file.

Acceptance tests:

- canonical Writer packet stays inside existing creative budget;
- canonical Reviewer packet stays inside existing evaluation budget;
- canonical packet contains no evidence-as-story-discovery instruction;
- legacy packets retain their prior behavior where explicitly supported.

# P1 — Update fixtures selectively; do not make every old fixture Historical-Substrate-aware

A large portion of the 57 errors are fixtures reaching new Historical Substrate preconditions before the behavior under test.

Do not mechanically add `historical-substrate.json` to every fixture.

That would erase backward-compatibility coverage and make the test suite lie about supported generations.

Classify tests into two sets:

## A. Historical Substrate canonical tests

Fixtures must explicitly adopt the new contract and create the complete minimal canonical authority chain required by the test:

```text
approved outline / bounded overlay
product substrate
section materialization
section substrate projection
narration/evidence authority as needed
```

## B. Legacy/direct-authorship compatibility tests

Fixtures must remain unadopted and continue through the compatibility path without Historical Substrate.

The test name/fixture should make this distinction visible.

Do not weaken new contract checks merely because a legacy fixture accidentally entered the wrong architecture mode.

# P1 — Old P01 draft/task lineage should be superseded, not made valid again

Product validation is already detecting old P01 artifacts that no longer match the new canonical architecture, including old draft provenance and stale material snapshots.

This is expected after changing P01 authority.

### Required correction

Represent the architecture migration explicitly in lifecycle state:

```text
old P01 probe/draft/task lineage
→ historical/superseded

new P01 architecture authority
→ fresh materialization
→ future fresh Writer task
```

Do not relax provenance or freshness validators so T0058/T0059 or other pre-substrate tasks become current again.

Do not delete historical artifacts merely to hide the conflict unless repository lifecycle convention already requires deletion. Prefer explicit archival/supersession semantics consistent with existing task history.

Validation must distinguish:

```text
historical superseded task
≠ active canonical task
```

# P2 — Some current failures are test expectation drift, not implementation defects

Examples include:

- section-migration test expecting a specific error substring while implementation rejects the correct unauthorized section with different wording;
- Writer baseline tests still expecting the pre-substrate input list and therefore treating `historical-substrate.json` as unexpected.

Update these assertions to the new contract where the test is intended to exercise Historical Substrate behavior.

Do not change correct runtime behavior merely to preserve stale exact strings or stale packet input lists.

Prefer semantic assertions over unnecessary exact-message coupling.

# P2 — Keep prompt-budget pressure as a useful architecture signal

The prompt budget failures should not be treated as arbitrary CI noise.

Historical Substrate is supposed to improve native representation and reduce compensating instructions. If adopting it makes creative/evaluation instruction layers larger, investigate duplication.

Before increasing any budget, check whether:

- canonical instructions duplicate legacy anti-failure rules;
- operation docs contain evaluation logic that belongs in Reviewer only;
- compatibility wrappers load both canonical and legacy instructions;
- routing semantics can be encoded in executable packet logic instead of natural-language warnings.

Desired outcome:

```text
new architecture
→ less contradictory prompt authority
→ not a larger rule stack
```

# Required implementation sequence

Keep the next correction round focused on integration. Do not add narrative rules or change the historical content model again unless a failing invariant requires it.

## COMMIT G — Explicit architecture adoption contract

- introduce one shared Historical Substrate adoption resolver;
- route materializer, outline preflight, packet compiler and validator through it;
- preserve legacy/direct-authorship compatibility for unadopted products;
- support bounded P01 overlay adoption without pretending P02–P08 were migrated.

Run targeted tests for materialization + outline task creation before proceeding.

## COMMIT H — Canonical packet assembly before budget validation

- stop relying on post-validation exact-string replacement for canonical routing;
- select canonical/legacy instruction and evidence semantics before packet assembly;
- keep existing prompt budgets unless a separately justified architecture decision changes them;
- verify canonical Writer and Reviewer packets are under budget.

## COMMIT I — Test-suite migration by architecture generation

- update canonical Historical Substrate fixtures to explicitly adopt the new contract;
- keep true compatibility fixtures unadopted;
- update stale input-list/error-string assertions where behavior intentionally changed;
- do not mass-add substrate artifacts to all fixtures.

Run the full unit suite.

Expected gate:

```text
python -m unittest discover -s tests -v
→ PASS
```

## COMMIT J — P01 lifecycle supersession and product validation

After unit tests pass:

- explicitly supersede/archive pre-substrate P01 task/draft lineage as appropriate;
- regenerate P01 derived canonical state through normal tooling;
- run architecture-boundary governance checks;
- run product validation;
- fix actual validation defects without weakening provenance.

Only after all CI stages pass may a fresh Writer probe be created.

# CI acceptance gate

A fresh Writer probe is blocked until the workflow reaches and passes all stages, not merely Unit tests:

```text
Unit tests                         PASS
Architecture/governance boundary  PASS
Product validation                PASS
```

Also manually confirm one compiled P01 Writer packet satisfies:

```text
Historical Substrate is primary history input
P01 default substrate contains only intended minimal primitives
Evidence broker is secondary verification only
No old Probe 1/2/3 prose or evaluator feedback is present
No method/carrier/scene/reveal route is prescribed
Canonical hashes/preflight verify current
```

# Interpretation of the current CI result

Do not report the current failure as “Historical Substrate architecture failed.”

The more precise diagnosis is:

> The core Historical Substrate v2 representation and P01 migration are substantially implemented, but the new contract is currently activated too broadly and too late in shared runtime paths, causing widespread compatibility and prompt-assembly regressions.

That is the problem to fix in this round.

# Do not do in this round

- do not add more anti-essay or narrative instructions;
- do not add scene/character/tension/sensory requirements;
- do not widen P01 substrate again merely because old tests expect more context;
- do not revert world-shaped primitives to flat statements;
- do not remove overlay authority and return to manual section overrides;
- do not weaken stale/provenance validation to preserve old probes;
- do not raise prompt budgets as the first response;
- do not create Probe 4/5 until the complete CI workflow passes.

## Architectural invariant for stabilization

```text
Architecture adoption is explicit.
Compatibility is intentional.
Canonical runtime is selected before prompt assembly.
Historical Substrate remains the primary history model only where adopted.
Evidence remains secondary verification for adopted Writer tasks.
Old authority lineages become superseded rather than silently revalidated.
Tests must prove both the new architecture and the compatibility boundary.
```
