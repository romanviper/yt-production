# Phase 3 Feedback Repair Report

Status: **IMPLEMENTATION COMPLETE — OWNER MEASUREMENT PENDING**

## Scope

This repair followed the owner work order on `codex/p01-phase3-whitebox-mvp`.

- source commit recorded before repair: `0751c9f9ad9ec39c299a5f23761e463c2e5754e3`
- implementation/test result commit used for the final focused acceptance evidence: `a4cd0e6dd1b643ef131ec3469c3503e18bf8e5cc`
- platform for recorded CI evidence: Ubuntu 24.04.4
- Python: 3.12.14
- no product files, historical run artifacts, benchmark prose or owner labels were modified
- no new Writer/live LLM was called
- no legacy experiment was rerun

The topology remains:

```text
Plan -> Write -> Truth -> Product
```

## What was wrong before repair

### Output identity and mapping

The previous white-box implementation could diagnose without receiving the actual candidate text. Writer mapping used loose two-way string containment, so empty quotes or shorter strings could match. Duplicate quotes could resolve by first match. Diagnosis could therefore combine one materialized candidate with mutable Plan/Writer/failure artifacts read later from the repository.

### Attribution semantics

The previous rule could turn a legacy `symptom_present` boolean plus Writer `REALIZED` / no-deviation declarations into `PLAN_FAILURE / HIGH`, or route responsibility to Writer from an unqualified deviation. Exact hashes and quote matches established location, but the result overclaimed semantic/causal certainty.

### Verification

The guided-review verifier did not validate the active BEFORE/AFTER Phase 3 card against its actual sources. The benchmark verifier trusted more legacy identity metadata than it verified from current source content.

### Measurement loop

The existing P3-I01 revised micro-output was not connected through one frozen case that bound baseline/candidate hashes, Plan scope, trace result, measurement scope, open Truth/regression invariants and owner measurement status.

## Red-before evidence

Before implementing the repair, regression tests were committed intentionally against the old implementation.

Recorded workflow:

- run: `34017352593`
- focused job: `101443374960`
- Python 3.12.14 / Ubuntu 24.04
- result: **FAIL**, as expected before repair

The red suite reproduced seven core failures:

1. diagnosis had no `candidate_text` input;
2. empty Writer quote could map;
3. duplicate Writer quote was not rejected as ambiguous;
4. changing only `symptom_present` could change attribution;
5. an unrelated punctuation deviation could route fault to Writer;
6. a missing cited Plan field could still produce `PLAN_FAILURE/HIGH`;
7. the runtime had no explicit raw-byte / normalized-text artifact identity API.

This was a known B03 drill, not blind discovery.

## Repair 1 — exact run evidence and provenance

The runtime now:

- snapshots candidate, Plan, Writer report, failure observation and intervention before diagnosis;
- diagnoses from those snapshots;
- keeps raw SHA-256 separate from newline-normalized text SHA-256;
- normalizes only CRLF/CR -> LF for the text view;
- requires non-empty exact quotes;
- rejects missing and ambiguous spans;
- requires the mapped Writer span to cover the exact failure span;
- emits typed evidence errors with artifact/field/expected/observed;
- marks trace availability on Plan/Write manifests and refreshes parent manifest hashes;
- writes a non-self-referential bundle that can be reverified;
- detects post-freeze content changes;
- accepts a newline-only raw-byte change through the declared text normalization policy while still detecting a one-word content change.

A run can be checked with:

```bash
python -m learning_runtime.phase3 --verify-run <run-dir>
```

## Repair 2 — honest bounded attribution

The runtime now separates these authority classes:

```text
RUNTIME_OBSERVED
AGENT_DECLARED
REVIEWER_INTERPRETATION
INTERVENTION_SUPPORTED_HYPOTHESIS
```

`REALIZED`, no declared deviation and legacy `symptom_present` flags no longer decide attribution.

Plan interpretation must bind to exact Plan beat fields that still exist. A missing referenced field becomes stale evidence. A Writer deviation affects attribution only when it is explicitly symptom-relevant and carries evidence. An irrelevant punctuation deviation does not move the suspect region.

For the known B03 case, the repaired result is:

```text
mapping_status: VALIDATED_EXACT
mapping_confidence: HIGH
suspected_regions: [PLAN]
attribution_confidence: MEDIUM
root_cause_status: BOUNDED_HYPOTHESIS_NOT_CAUSAL_PROOF
```

This deliberately replaces the former `PLAN_FAILURE / HIGH` claim. Exact mapping is reliable; causal attribution remains bounded and uncertain.

## Repair 3 — verifier checks the artifacts in use

`verify_phase1_guided_review.py` now accepts an explicit session and distinguishes:

- `SINGLE_SAMPLE` guided review;
- `COMPARISON` BEFORE/AFTER guided review.

It validates the actual schema instance, file/JSON/paragraph locator, exact excerpt grounding and target references. Empty `micro_units`, fake locators and fake excerpts are regression-tested failures. Null owner labels remain a valid pending-measurement state.

`verify_phase1_benchmark.py` now validates active schema instances and resolves actual product/craft source identities. Legacy Phase-1 `SHA256_TEXT` records created with stripped-text semantics are handled through an explicit compatibility adapter; their manifest hashes were not rewritten to make the verifier pass. New runtime identities remain exact raw + newline-normalized identities.

## Repair 4 — bounded B03 measurement case

The new `learning_runtime.feedback` path uses only existing artifacts.

Prepare:

```bash
python -m learning_runtime.feedback prepare p01-rootcause-01 --out /tmp/p01-feedback-case
```

Verify:

```bash
python -m learning_runtime.feedback verify --case-dir /tmp/p01-feedback-case
```

Ingest a real measurement later:

```bash
python -m learning_runtime.feedback ingest \
  --case-dir /tmp/p01-feedback-case \
  --measurement <measurement.json>
```

The case freezes:

- baseline candidate identity;
- revised candidate identity;
- failure/symptom ID;
- exact mapping status;
- bounded suspect region;
- P3-I01 intervention identity;
- B03-only Plan change;
- unchanged evidence ceiling;
- `B03_MICRO_UNIT_ONLY` measurement scope;
- unmeasured Truth/clarity/continuity state;
- comparison card;
- measurement status.

A Plan patch whose beat identity is outside B03 is rejected. A measurement for a stale candidate hash, wrong case or wrong scope is rejected.

Synthetic `TEST_ONLY` positive/negative measurements prove the frozen feedback rule changes directionally, but they never enter owner state. Even a positive diagnostic result stays:

```text
symptom_delta: DIRECTIONALLY_REDUCED_NOT_RESOLVED
improvement: NOT_ESTABLISHED
```

If Truth is missing or a regression is present, that gap remains visible and there is still no overall-gain claim. Lexical disappearance of the old sentence is explicitly not treated as symptom resolution.

## Green acceptance evidence

Recorded focused workflow after the repair:

- run: `34018140611`
- focused job: `101445572009`
- checkout: `a4cd0e6dd1b643ef131ec3469c3503e18bf8e5cc`
- platform: Ubuntu 24.04.4
- Python: 3.12.14
- focused result: **SUCCESS**

Focused unit command:

```bash
python -m unittest \
  tests.test_learning_runtime \
  tests.test_phase3_whitebox \
  tests.test_feedback_integrity \
  tests.test_feedback_loop -v
```

Result:

```text
Ran 33 tests in 0.195s
OK
exit 0
```

The same focused CI check also ran, with exit 0:

```bash
python scripts/experiments/verify_phase1_benchmark.py
python scripts/experiments/verify_phase1_guided_review.py --session benchmarks/p01/review-sessions/owner-pilot-01-guided.json
python scripts/experiments/verify_phase1_guided_review.py --session benchmarks/p01/review-sessions/phase3-p3-f01-rerun-guided.json
python -m learning_runtime.feedback prepare p01-rootcause-01 --out /tmp/p01-feedback-case
python -m learning_runtime.feedback verify --case-dir /tmp/p01-feedback-case
```

Observed verifier/case states:

```text
benchmark: ARCHITECTURE_FROZEN_READY_FOR_PILOT
single guided review: STRUCTURALLY_READY / AWAITING_OWNER
Phase3 comparison: STRUCTURALLY_READY / AWAITING_OWNER
B03 case prepare: AWAITING_MEASUREMENT
B03 case verify: VALID
```

Machine B03 identities printed by CI:

```text
baseline_text_sha256:
  aa0de7b1a42bb2233c84e12ba7ea0aa0c6ad40868516023d22a9a3566f258665

candidate_text_sha256:
  abe8fe2bab89bcfbd7670c25e178c4da8fe4c2897fe82a9b6501ae7b3fd9a053

intervention_raw_sha256:
  e4192555f5024511fd52f3b6e43d5d8508caf9de9258678a9c94a033e0c2a7e2
```

The whole focused check block completed in well under the proposed 5-second post-environment budget. The unit subset itself was 0.195s. The prepare drill occupied roughly 0.084s between CI log timestamps and bundle verification roughly 0.068s; these are log-derived observations, not a dedicated performance benchmark.

## Trace drill cost

B03 was predeclared as a known case. The question was fixed in advance: can the same failure span be bound to the actual candidate, one Writer beat and one Plan beat without overstating the semantic attribution?

Core diagnosis inputs opened/snapshotted by the repaired bundle:

1. candidate;
2. Plan;
3. Writer report;
4. failure observation;
5. intervention for provenance/bounded next step.

No repository-wide scan is needed once the case bundle exists. The machine trace maps the failure to B03 exactly and leaves one unresolved semantic edge: Plan is supported as a suspect, but Writer contribution is not independently excluded. Human inspection time was not separately instrumented, so no fabricated before/after human-time claim is made.

## Full production validation

The original full `validate` job is intentionally unchanged and still exits non-zero because of the same three production-baseline failures already present before this repair:

1. `HistoricalSubstrateRuntimeIntegrationTest.test_section_migration_materializes_only_declared_section`;
2. `WriterBaselineTests.test_current_sumer_c003_p01_smoke_compiles_to_minimal_writer_packet`;
3. `WriterBaselineTests.test_current_sumer_p01_review_packet_with_handoff_and_receipts_stays_under_budget`.

These paths are outside the owner feedback-repair scope. They were not weakened, deleted or fixed opportunistically.

## What is more trustworthy now

The system is now materially stronger at:

- rejecting stale/ambiguous/malformed evidence before diagnosis;
- proving which exact candidate/Writer/Plan artifacts were mapped;
- detecting post-freeze tampering;
- separating mapping certainty from semantic attribution uncertainty;
- refusing boolean/deviation shortcuts to root-cause claims;
- validating the review artifact the owner is actually being shown;
- binding a bounded intervention to the exact revised output being measured;
- changing feedback when a valid measurement changes while never manufacturing an overall gain.

## What is still not known

This repair does **not** establish:

- that Plan is the true literary root cause of P01's essay-like quality;
- that the manual B03 revised micro-output is better;
- that the symptom is resolved because the old sentence disappeared;
- that Truth, section continuity or whole-section quality improved;
- benchmark validity, transfer validity or judge promotion;
- completion of all three phases.

## Next owner action

Owner measurement is still missing. The correct current state is:

```text
AWAITING_MEASUREMENT
improvement: NOT_ESTABLISHED
```

The next action is to read the frozen B03 BEFORE/AFTER guided comparison and provide a real owner-guided diagnostic result bound to the candidate hash. That result may support, reject or leave uncertain P3-I01; it will not by itself prove broader quality gain or causality.
