# Phase 3 — White-box Learning MVP

Status: **READY FOR ONE BOUNDED REAL LEARNING ROUND**

The owner-accepted feedback in `docs/phase3/prototype-learning-feedback.md` has now been implemented. Machine-readable closure and CI evidence live in `docs/phase3/prototype-learning-implementation.json`.

Do not continue polishing the architecture before a real bounded round exposes a concrete execution or evidence-loss defect.

## Goal

Turn a bounded output failure into trustworthy engineering feedback without pretending that exact mapping proves literary causality.

Keep the active topology:

```text
Plan -> Write -> Truth -> Product
                    ↓
                   Audit
```

The loop must answer, in order:

1. Are the candidate, failure span, Writer report and Plan the exact artifacts intended for this run?
2. Does the output span map exactly and unambiguously to a Writer beat and Plan beat?
3. Which bounded region is supported by semantic evidence, and how uncertain is that attribution?
4. Was the allowed intervention actually limited to the registered region?
5. What did the owner/Product reviewer prefer?
6. Separately, was the named symptom observed to reduce, remain, or stay unknown?
7. Which invariants were measured, missing or regressed?

Preference is not symptom evidence. Exact mapping is not causal proof.

## Frozen learning standard

The active B03 case binds exact identities for:

- `learning_runtime/briefs/p01-rootcause-01.json`
- `docs/quality/output-quality-contract.md`
- `benchmarks/p01/review-profiles/foc-functional-targets.json`

The common brief contains one product goal and decision rules, but role visibility is bounded.

Before the first-pass Product vote, the reviewer does **not** receive:

- the diagnostic defect hypothesis;
- suspected Plan/Writer attribution;
- intervention prediction;
- FoC target behavior used for post-vote guided diagnosis.

Therefore “one standard” does not mean “every role sees every diagnostic fact.”

## White-box trace

```bash
python -m learning_runtime.phase3 p01-rootcause-01 --out /tmp/p01-phase3-rootcause-01
python -m learning_runtime.phase3 --verify-run /tmp/p01-phase3-rootcause-01
```

The run snapshots candidate, Plan, Writer report, failure observation and intervention before diagnosis. `diagnosis.json` reads those snapshots rather than mutable repository sources.

A valid current B03 trace yields:

```text
mapping: VALIDATED_EXACT / HIGH
suspected region: PLAN
attribution confidence: MEDIUM
root-cause status: BOUNDED_HYPOTHESIS_NOT_CAUSAL_PROOF
```

The attribution observation authority is only:

```text
REVIEWER_SUPPORTED_DIAGNOSTIC_HYPOTHESIS
```

It is not `INTERVENTION_SUPPORTED_HYPOTHESIS`. Intervention support requires a separately measured intervention result.

`REALIZED`, absence of a declared deviation and legacy `symptom_present` booleans are provenance observations only. They never decide causality by themselves.

## Immutable measurement history

Prepare the bounded B03 case:

```bash
rm -rf /tmp/p01-feedback-case
python -m learning_runtime.feedback prepare p01-rootcause-01 --out /tmp/p01-feedback-case
python -m learning_runtime.feedback verify --case-dir /tmp/p01-feedback-case
python -m learning_runtime.feedback show --case-dir /tmp/p01-feedback-case
```

Measurements now use `schemas/feedback-measurement.schema.json` and must have an immutable `measurement_id`.

Case state is stored as:

```text
case.json                         # frozen case
measurements/M001.json            # immutable observation
feedback/M001.json                # derived result for M001
measurements/M002.json            # later observation/correction
feedback/M002.json
current.json                      # derived current pointer/resolution
```

A duplicate measurement ID is rejected. A correction uses a new ID plus `supersedes`. Independent parallel measurements are both preserved; without explicit supersession the state becomes `MULTIPLE_MEASUREMENTS_UNRESOLVED` rather than silently choosing the latest record.

Ingestion:

```bash
python -m learning_runtime.feedback ingest \
  --case-dir /tmp/p01-feedback-case \
  --measurement <measurement.json>
```

### Measurement semantics

The following are independent:

```text
preference_result
symptom_observation
invariant_state
```

A preference `YES` without a symptom observation produces:

```text
preference_result: YES
symptom_observation: NOT_MEASURED
improvement: NOT_ESTABLISHED
```

`UNCERTAIN` asks for clarification or more observation while keeping the intervention frozen. `WRONG_TARGET` returns to target definition without automatically rewriting Plan or Writer. Partial invariant reports inherit the case's explicit `NOT_MEASURED` states instead of erasing them.

Guided owner evidence remains directional/diagnostic only. It cannot establish blind benchmark gain, whole-section quality or causal proof.

## Role workspaces

The prototype workspace implementation is `learning_runtime/workspace.py`.

Smoke command:

```bash
rm -rf /tmp/p01-workspace-smoke
python -m learning_runtime.workspace smoke --out /tmp/p01-workspace-smoke
```

Layout:

```text
<root>/<run-id>/
  control/
    role-policy.json
    frozen-standard.json
    handoffs.jsonl
    access-events.jsonl
    measurements/
  agents/
    <role>/<execution-id>/
      input/
      output/
      scratch/
```

Policy version:

```text
PHASE3-WORKSPACE-PROTOTYPE-1
```

Enforcement level:

```text
FILE_BROKER_ONLY_NO_SHELL_OR_NETWORK_SURFACE
```

The broker allows a role to read its own input/output/scratch and write only its own output/scratch. Resolved `..`, absolute cross-role access and symlink escapes are denied. Handoff is a launcher-owned byte copy from one role's output to the next role's input, verified by SHA-256; the destination role cannot rewrite the handed-off input through the broker.

The Product review packet is role-safe and excludes diagnostic hypothesis data before vote.

### Important isolation limitation

This is **not** claimed as a host/OS sandbox.

```text
host_process_isolation: NOT_PROVEN
```

Read isolation is enforceable only when the agent receives `RoleWorkspaceBroker` as its sole filesystem surface and is not separately granted a shell/network/general filesystem tool that bypasses it. Any future real round using broader tools must state that isolation is not enforced rather than pretending otherwise.

## Verified prototype evidence

Focused CI at validation commit `d7115f9f1d08f8f521471c837c4115c0820a8ff6` ran:

- 44 focused tests: PASS in 0.379s;
- Phase 1 benchmark verifier: PASS;
- guided single-sample verifier: PASS;
- guided Phase 3 comparison verifier: PASS;
- B03 case prepare/verify: PASS;
- workspace broker smoke: PASS.

Workspace smoke observed real broker denials for:

- Writer cross-role review read via traversal;
- Writer input mutation;
- Truth mutation of handed-off candidate input.

Writer -> Truth handoff result:

```text
COPIED_READ_ONLY_HASH_MATCH
sha256: 3864ef4ec0073ccd3a009c781b7e0b1767750c0b6766e4f3fb0ae72e0ccccb59
```

The full production suite still has the same three pre-existing Sumer/historical-substrate baseline failures. They remain outside this Phase 3 feedback-repair scope and are not waived.

## Guided review verification

```bash
python scripts/experiments/verify_phase1_guided_review.py \
  --session benchmarks/p01/review-sessions/owner-pilot-01-guided.json

python scripts/experiments/verify_phase1_guided_review.py \
  --session benchmarks/p01/review-sessions/phase3-p3-f01-rerun-guided.json
```

Both formats verify actual schema/source/locator/excerpt/target grounding. Null owner labels are a valid pending state, never a quality claim.

## Boundaries

Do not use this prototype to:

- infer symptom change from preference alone;
- overwrite previous measurements;
- expose diagnostic prediction to the blind Product reviewer;
- call exact mapping causal proof;
- call the workspace broker an OS sandbox;
- grant a role repo-wide shell/filesystem access and still claim broker isolation;
- generalize B03 into a global writing rule;
- add a registry, event bus, generic permission platform or new scoring layer;
- continue architecture polishing without evidence from a real bounded round.

## Next legitimate step

When the owner requests execution, run **one bounded real Plan -> Writer -> Truth/Product -> Audit round** through role-safe packets/workspaces.

That round may succeed, fail or remain inconclusive. Any of those outcomes counts as useful learning if evidence is preserved and the system does not respond by inventing broad new rules without support.
