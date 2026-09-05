# P01 probe-readiness review

Status: `architecture_frozen_probe_gate_only`

Branch: `codex/foc-editorial-historical-substrate-v2`

## Decision

Stop optimizing the architecture for broad unit-test coverage.

The critical architecture problems that previously blocked a clean P01 experiment are now sufficiently resolved:

1. Historical Substrate adoption is explicit rather than inferred from direct-authorship.
2. P01 adopts the new contract through a bounded, approved section overlay.
3. Legacy direct-authorship remains on a compatibility path instead of being forced through Historical Substrate.
4. Canonical P01 Writer context uses Historical Substrate as the primary history model.
5. Evidence access is secondary verification after the Writer chooses a telling from the substrate; it is no longer the primary story-discovery substrate.
6. P01 Historical Substrate is world-shaped rather than a flat proposition list.
7. P01 primary substrate selection is intentionally minimal rather than equal to full claim coverage.
8. Canonical section/substrate freshness is executable and can block stale derived artifacts.

These decisions are now frozen for the purpose of the next experiment. Do not reopen or reshape them merely to make unrelated legacy tests pass.

## Important test policy from this point

Do not treat `all unit tests green` as a prerequisite for the next P01 probe.

Tests may contain three different kinds of authority:

### Tests that may block the probe

A failing test may block the probe only if it demonstrates a violation of the active P01 critical path, especially:

- P01 overlay/adoption cannot be resolved canonically;
- P01 section state cannot be regenerated from canonical inputs;
- P01 section Historical Substrate is stale or edited;
- Writer packet does not contain the intended Historical Substrate;
- evidence is again presented as the place to discover the story/history;
- Writer receives claim/source/material ledgers as primary composition input;
- truth/provenance hard boundaries are bypassed;
- the Writer task can run against stale architecture authority;
- narrative choreography has leaked upstream into Historical Substrate or the section contract.

### Tests that do not automatically block the probe

Do not change the new architecture solely because tests for older generations still expect:

- the old three-file Writer packet shape;
- legacy mission semantics;
- direct-authorship without Historical Substrate;
- old prompt assembly details;
- old exact error wording;
- compatibility-only lifecycle behavior that is not on the adopted P01 path.

If such tests remain useful, keep them scoped to the compatibility path or update their fixtures. Do not make canonical P01 behave like the old architecture to satisfy them.

### Hard-boundary tests remain authoritative

Do not weaken tests that protect:

- source/claim scope;
- unsupported certainty;
- stale task/projection detection;
- provenance/hash integrity;
- task write scope;
- forbidden narrative authority upstream;
- false reconstruction or causal overreach.

## Required final gate before the probe

Do only the following now.

### 1. Rematerialize P01 from current canonical inputs

The current P01 overlay has changed and derived section artifacts may still contain the previous overlay hash.

Regenerate P01 through the normal bounded materialization path. Do not hand-edit `section.json` or `historical-substrate.json` to make hashes match.

Expected result:

```text
approved outline
+ approved P01 overlay
+ product Historical Substrate
→ canonical P01 section state
→ canonical P01 Writer Historical Substrate
```

### 2. Run only the critical P01 preflight

Confirm that:

- P01 explicitly adopts Historical Substrate v1;
- section state matches the resolved outline + overlay;
- section Historical Substrate matches deterministic projection;
- selected substrate IDs remain only the intended minimal set;
- Historical Substrate remains world-shaped;
- no narrative-route fields appear in the substrate;
- truth boundaries remain attached and enforceable.

### 3. Compile the actual fresh Writer packet

Inspect the packet that the new Writer will actually receive, not only source code or tests.

The packet must satisfy these invariants:

```text
Historical Substrate = primary historical input
Evidence broker = secondary verification only
No old probe text
No evaluator diagnosis
No competitor prose
No old feedback
No prescribed scene/carrier/opening/reveal order
No claim/material ledger as primary composition substrate
```

The Writer may receive normal continuity and task-local probe bounds.

### 4. If the packet passes, create the fresh probe immediately

Do not continue harness work after this gate unless the critical P01 path itself fails.

Use a fresh Writer with no rejected probes or architecture diagnosis in context.

The probe should be one contiguous passage from the larger unfinished P01, approximately 450–650 words. It is a slice of the section, not a compressed miniature of the whole section.

Do not prescribe how the Writer should create narrative quality. In particular, do not require a scene, protagonist, artifact carrier, hook, reveal sequence, sensory beat, climax or specific prose method.

The purpose of the experiment is now clean:

> Does Writer produce materially better historical narration when its primary input is a canonical, minimal, world-shaped model of historical reality rather than claims/evidence records?

## Evaluation after the probe

Judge the prose on the historical experience it creates, not on whether it visibly uses substrate records.

Key questions:

1. Are we following history/practice changing, or the narrator explaining evidence?
2. Is there a natural reason to continue listening?
3. Does meaning emerge from progression rather than being announced and defended?
4. Can a listener retell what changed after one hearing?
5. Did the Writer remain inside truth/reconstruction boundaries without turning those boundaries into constant epistemic commentary?

If the result is still essay-like after this clean run, do not automatically expand Historical Substrate or add more anti-essay rules.

At that point move the primary diagnosis downstream to Writer-owned nonfiction composition/model behavior.

## Freeze rule

Until the probe is evaluated:

```text
DO NOT optimize architecture for unrelated unit tests.
DO NOT add new Writer craft rules.
DO NOT widen P01 substrate for completeness.
DO NOT restore evidence-first story discovery.
DO NOT change world-shaped substrate back toward proposition lists.
```

Only fix something before the probe if it prevents the active P01 path from satisfying the critical invariants above.

## Final authorization rule

```text
P01 rematerialized
+ critical substrate/preflight checks pass
+ actual Writer packet matches architecture
= AUTHORIZED TO RUN FRESH P01 PROBE
```

Full repository test cleanup can continue later as compatibility/maintenance work, but it is no longer the experiment gate.
