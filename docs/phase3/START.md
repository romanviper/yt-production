# Phase 3 — White-box Learning MVP

Status: **ACTIVE — FEEDBACK LOOP REPAIRED, OWNER MEASUREMENT PENDING**

## Goal

Turn a bounded output failure into trustworthy engineering feedback without pretending that exact mapping proves literary causality.

Keep the active topology:

```text
Plan -> Write -> Truth -> Product
```

The feedback loop must answer, in order:

1. Are the candidate, failure span, Writer report and Plan the exact artifacts intended for this run?
2. Does the output span map exactly and unambiguously to a Writer beat and Plan beat?
3. Which bounded region is supported by semantic evidence, and how uncertain is that attribution?
4. Was the allowed intervention actually limited to the registered beat?
5. Is there owner/Product measurement for the revised output, and what authority does that measurement have?

## White-box trace command

```bash
python -m learning_runtime.phase3 p01-rootcause-01 --out /tmp/p01-phase3-rootcause-01
python -m learning_runtime.phase3 --verify-run /tmp/p01-phase3-rootcause-01
```

The run snapshots candidate, Plan, Writer report, failure observation and intervention before diagnosis. `diagnosis.json` reads those snapshots, not mutable repository sources.

Plan and Write traces contain typed engineering observations, not raw private chain-of-thought.

## Repaired evidence semantics

Exact identity and mapping are separate from semantic attribution.

A valid B03 trace currently yields:

```text
mapping: VALIDATED_EXACT / HIGH
suspected region: PLAN
attribution confidence: MEDIUM
root-cause status: BOUNDED_HYPOTHESIS_NOT_CAUSAL_PROOF
```

This replaces the earlier overclaim `PLAN_FAILURE / HIGH`.

`REALIZED`, absence of a declared deviation, and legacy `symptom_present` booleans are provenance observations only. They do not independently prove semantic adherence or causality. Only symptom-relevant, grounded Writer deviations may nominate Write as a suspect. Plan interpretation must bind to the exact Plan hash/beat/fields that are still present.

## Evidence integrity

Each run keeps two identities where text is involved:

- raw bytes SHA-256;
- newline-normalized text SHA-256 (`CRLF` / `CR` -> `LF` only).

This allows a legitimate newline-only change to preserve content identity while a real word change fails verification. Newline normalization never trims or collapses substantive content.

The run bundle can be reverified after storage. Post-freeze edits to candidate/failure/report/trace/diagnosis are detected instead of silently accepted.

## Bounded B03 feedback case

No new Writer is called by this MVP repair. It reuses the already-existing B03 intervention and manual micro-output.

Prepare and verify the case:

```bash
rm -rf /tmp/p01-feedback-case
python -m learning_runtime.feedback prepare p01-rootcause-01 --out /tmp/p01-feedback-case
python -m learning_runtime.feedback verify --case-dir /tmp/p01-feedback-case
python -m learning_runtime.feedback show --case-dir /tmp/p01-feedback-case
```

The prepared bundle freezes:

```text
baseline candidate + hash
failure/symptom identity
validated output -> Writer -> Plan mapping
bounded attribution hypothesis
P3-I01 intervention
full materialized Plan with only B03 changed
existing revised micro-output + hash
measurement scope and open invariants
comparison card
feedback status
```

The Plan patch is rejected if its beat identity is outside B03. The manual revised output retains `independence: NONE`.

## Measurement

If no owner label exists, the correct state is:

```text
AWAITING_MEASUREMENT
improvement: NOT_ESTABLISHED
```

A real guided owner measurement must bind to the current case ID, candidate text hash and `B03_MICRO_UNIT_ONLY` scope before ingestion:

```bash
python -m learning_runtime.feedback ingest \
  --case-dir /tmp/p01-feedback-case \
  --measurement <measurement.json>
```

Guided owner measurement is diagnostic/directional evidence only. It does not establish blind benchmark gain, whole-section quality or causal proof. A preferred candidate with missing Truth/regression checks still reports those gaps and still cannot become an overall gain.

`TEST_ONLY` synthetic measurements exist only for regression tests and never become owner state.

## Guided review verification

Single-sample and BEFORE/AFTER comparison formats are separate contracts:

```bash
python scripts/experiments/verify_phase1_guided_review.py \
  --session benchmarks/p01/review-sessions/owner-pilot-01-guided.json

python scripts/experiments/verify_phase1_guided_review.py \
  --session benchmarks/p01/review-sessions/phase3-p3-f01-rerun-guided.json
```

The verifier checks the actual schema instance, source/JSON locator, exact excerpt grounding and target references. Null owner labels are a valid pending-measurement state, never a format failure and never a gain claim.

## Focused feedback checks

CI has a dedicated `feedback-focused` job. It runs the Phase 2/3 regression suite, both current verifiers, and a real temporary B03 prepare/verify drill. The original full production validation job is unchanged; unrelated production baseline failures therefore cannot hide the feedback signal and are not waived.

## Boundaries

Do not use this repair to:

- call a new Writer or live LLM;
- create new production prose;
- rerun a legacy experiment;
- alter historical evidence, taxonomy or owner labels;
- claim the Plan is the proven root cause;
- claim the manual micro-output improved before owner measurement;
- add a registry, event bus, voting layer or generic root-cause framework.

The next owner-facing action is to measure the frozen B03 BEFORE/AFTER card. That measurement may support, reject or leave uncertain the bounded intervention; it does not complete a broader quality claim.
