# Phase 3 Feedback Repair — Owner Work Order

Status: **IMPLEMENTATION SCOPE RECORD**

This file canonicalizes the owner-supplied work order used for the bounded feedback repair. It is not evidence that the work had already been performed when the order was written.

## Source and authority

- execution role: `system_architect`
- actual source commit recorded before repair: `0751c9f9ad9ec39c299a5f23761e463c2e5754e3`
- authorized branch: `codex/p01-phase3-whitebox-mvp`
- no branch creation, PR creation, merge or production-state mutation authorized by this work order
- keep topology: `Plan -> Write -> Truth -> Product`

## Objective

Repair the smallest feedback loop so that each bounded change receives trustworthy feedback about:

1. evidence integrity;
2. exact output-span / Writer-beat / Plan-beat mapping;
3. the bounded region actually supported by evidence, with uncertainty preserved;
4. whether the registered intervention is constrained to the allowed region;
5. whether an existing revised output has actually been measured, with the measurement authority explicit.

Priority order:

```text
valid evidence
  -> correct mapping
  -> honest diagnosis
  -> bounded intervention test
  -> feedback cost
```

## Hard boundaries

Do not:

- create new prose or production tasks;
- call a new Writer/live LLM;
- expand historical evidence;
- invent owner labels;
- rerun legacy experiments;
- alter the aesthetic target, taxonomy or Truth authority to make checks pass;
- promote guided diagnostic review to blind calibration evidence;
- add agent registry, event bus, generic root-cause engine or voting layer;
- mutate historical run artifacts to satisfy new validators.

## Required repair sequence

### 0. Reproduce before repair

Record source commit/platform/Python, then make the known failure cases executable as regressions. A known B03 case is a trace drill, not blind discovery.

### 1. Bind trace to exact artifacts

- diagnosis reads the actual candidate for the run;
- freeze candidate/Plan/Writer report/failure/intervention before diagnosis;
- exact, non-empty, disambiguated spans only;
- Writer span must cover the failure span;
- typed errors for missing/ambiguous/stale/malformed evidence;
- raw-byte and normalized-text identities stay distinct;
- manifests and trace availability must remain internally consistent;
- frozen bundle must be re-verifiable and detect tampering.

### 2. Preserve attribution uncertainty

- separate runtime-observed mapping, agent declarations, reviewer interpretation and intervention-supported hypothesis;
- boolean flags, `REALIZED` and absence of deviations never establish root cause alone;
- Plan interpretation binds to exact beat/fields;
- only symptom-relevant grounded deviations affect Writer suspicion;
- allow multiple suspect regions or inconclusive attribution;
- keep mapping confidence separate from attribution confidence.

### 3. Verify artifacts actually in use

- validate active schema instances rather than schema keywords only;
- resolve real file/JSON/paragraph locators;
- verify excerpts and source identities;
- distinguish single-sample guided review from BEFORE/AFTER comparison;
- null owner labels mean pending measurement, not malformed and not completed.

### 4. Connect B03 to measurement

Use only existing B03/P3-I01 artifacts. The feedback case must freeze:

```text
baseline + failure
  -> validated mapping
  -> bounded hypothesis
  -> registered B03-only intervention
  -> revised Plan + existing manual output
  -> guided measurement
  -> feedback
```

No measurement means `AWAITING_MEASUREMENT` and `improvement: NOT_ESTABLISHED`. A stale candidate/case/scope measurement must be rejected. Preference plus a missing/failing Truth/regression invariant must retain the gap and cannot become overall gain.

### 5. Make feedback checks fast and visible

Keep a focused CI signal separate from the full production suite. It must be offline, deterministic, use no live model and verify the active B03 bundle as well as both current verifiers. The proposed local machine budget is <=5 seconds after environment setup; it is not a global CI timeout.

## Completion evidence required

Handoff must include:

- regression cases demonstrating red-before/green-after behavior;
- verifier evidence on the active review artifacts;
- re-verifiable B03 bundle with hashes;
- bounded case waiting honestly for real owner measurement;
- focused-machine timing and platform;
- explicit unresolved edges and unrelated production baseline debt;
- `feedback-repair-report.md` and `feedback-repair-record.json` with separate process/output.

Structural success must not be reported as proof that prose improved, that all three phases are complete, or that the Plan is the proven literary root cause.
