# Phase 3 — White-box Learning MVP

Status: **READY FOR ROUND 01 RETRY WITH MANDATORY DECISION TELEMETRY**

The prototype feedback corrections and the owner-requested process-observability blocker are implemented. Machine-readable evidence lives in:

- `docs/phase3/prototype-learning-implementation.json`
- `docs/phase3/decision-telemetry-implementation.json`

Read `docs/phase3/decision-telemetry-contract.md` before any fresh agent execution.
Do not continue architecture polishing unless the next bounded real round exposes a concrete execution/evidence-loss defect.

## Goal

Turn a bounded output failure into trustworthy engineering feedback without pretending that exact mapping, agent self-report, or one intervention proves literary causality.

Active topology:

```text
Plan -> Write -> Truth -> Product
                    ↓
                   Audit
```

The loop must answer:

1. What exact inputs and standards did each role receive?
2. What bounded decisions did Plan / Writer / Truth / Audit declare **during execution**?
3. Which evidence, alternatives, expected effects and risks were attached to those decisions?
4. Did each declared decision precede the final artifact it claims to produce?
5. Is the final artifact write-once, hash-bound and sealed before downstream feedback?
6. What did blind Product review prefer?
7. Separately, did the named symptom reduce, remain or stay unknown?
8. Which invariants were measured, missing or regressed?
9. Which bounded region remains supported after artifact evidence and process telemetry are compared?

Preference is not symptom evidence. Exact mapping is not causal proof. Declared process telemetry is not private chain-of-thought and is not causal proof.

## Mandatory process telemetry

For fresh `plan`, `writer`, `truth` and `audit` executions, `input -> final output` is no longer sufficient.

Each role must emit ordered telemetry to:

```text
agents/<role>/<execution-id>/output/telemetry.jsonl
```

Telemetry version:

```text
PHASE3-DECISION-TELEMETRY-1
```

Supported events:

```text
DECISION
CHECKPOINT
RISK
DEVIATION
```

A `DECISION` carries at least:

```text
chosen_action
rationale_summary
evidence_refs
alternatives_considered
expected_effect
risks
output_refs
```

### Temporal anti-rationalization rule

For Plan / Writer / Truth / Audit:

```text
explore / rewrite in scratch/
          ↓
DECISION binds exact output/<path>
          ↓
first and only final write to output/<path>
          ↓
seal telemetry + final outputs
          ↓
downstream handoff
```

The broker rejects a final output write if its decision does not already exist. Final `output/` artifacts are write-once. The seal independently rechecks decision/output binding to catch broker bypass, hashes telemetry + primary outputs, and blocks handoff if the seal is absent or stale.

After seal, all broker writes from that execution are denied, including telemetry and scratch.

The blind Product reviewer is intentionally different: first-pass preference is frozen without requiring analytical decision rationale. Post-vote diagnostic observation may follow only after that freeze.

Runtime validation rejects raw/private-reasoning fields such as:

```text
chain_of_thought
raw_chain_of_thought
private_reasoning
internal_monologue
hidden_reasoning
scratchpad_reasoning
```

## Frozen learning standard

The current B03 case binds exact identities for:

- `learning_runtime/briefs/p01-rootcause-01.json`
- `docs/quality/output-quality-contract.md`
- `benchmarks/p01/review-profiles/foc-functional-targets.json`

Before first-pass Product vote, the reviewer does **not** receive diagnostic defect labels, suspected Plan/Writer attribution, intervention prediction, or FoC target behaviors used for post-vote diagnosis.

## White-box trace

Current fixture command:

```bash
python -m learning_runtime.phase3 p01-rootcause-01 --out /tmp/p01-phase3-rootcause-01
python -m learning_runtime.phase3 --verify-run /tmp/p01-phase3-rootcause-01
```

The existing B03 fixture supports only:

```text
mapping: VALIDATED_EXACT / HIGH
suspected region: PLAN
attribution confidence: MEDIUM
root-cause status: BOUNDED_HYPOTHESIS_NOT_CAUSAL_PROOF
```

Its attribution authority is:

```text
REVIEWER_SUPPORTED_DIAGNOSTIC_HYPOTHESIS
```

Do not promote legacy `REALIZED`, no-deviation declarations, boolean symptom flags, or structured telemetry into causal proof by themselves.

## Immutable measurement history

Measurements remain append-only:

```text
case.json
measurements/M001.json
feedback/M001.json
measurements/M002.json
feedback/M002.json
current.json
```

`preference_result`, `symptom_observation` and `invariant_state` are separate evidence. Guided owner evidence remains diagnostic/directional only and cannot establish blind benchmark gain, whole-section quality or causal proof.

## Role workspaces

Implementation: `learning_runtime/workspace.py`

Policy:

```text
PHASE3-WORKSPACE-PROTOTYPE-2
FILE_BROKER_PLUS_TEMPORAL_DECISION_GATE_PLUS_EXECUTION_SEAL_NO_SHELL_OR_NETWORK_SURFACE
```

Layout:

```text
<root>/<run-id>/
  control/
    role-policy.json
    frozen-standard.json
    handoffs.jsonl
    access-events.jsonl
    seals/
    measurements/
  agents/
    <role>/<execution-id>/
      input/
      output/
        telemetry.jsonl
      scratch/
```

The broker enforces role-local reads/writes, input immutability, path traversal/symlink boundaries, decision-before-final-output, write-once final outputs, execution seals, and hash-bound handoffs.

### Isolation limitation

This is **not** a host/OS sandbox:

```text
host_process_isolation: NOT_PROVEN
```

Enforcement is valid only when `RoleWorkspaceBroker` is the role's sole filesystem surface and the role is not separately granted a shell/network/general filesystem tool that bypasses it.

## Verified telemetry evidence

Temporal telemetry validation at build commit `d91843396aa742ab145bc2d710219d7fe2d0d02a`:

- 56 focused tests: **PASS** in 0.279s;
- Phase 1 benchmark verifier: PASS;
- both guided review verifiers: PASS;
- B03 case prepare/verify: PASS;
- workspace smoke: PASS;
- final output without prior decision: DENIED;
- second final-output write before seal: DENIED;
- direct-filesystem unbound primary output: seal rejects it;
- post-seal write: DENIED;
- Writer -> Truth sealed handoff: hash match.

The full production suite still has the same three pre-existing Sumer/historical-substrate failures. They are outside this Phase 3 scope and are not waived.

## Round 01 hard gate

Do **not** accept a fresh Plan / Writer / Truth / Audit artifact into the learning chain unless:

```text
role-safe packet received
→ ordered telemetry emitted during work
→ bounded DECISION names exact final output path
→ final output materialized once
→ telemetry + output validate
→ execution sealed before downstream feedback
→ handoff verifies sealed hash
→ downstream role receives only sealed artifact
```

A fresh round must preserve these telemetry files and seals alongside final artifacts. This is required so a failed prose span can be traced not only to a Plan node or Writer beat, but also to the declared decisions that produced those artifacts.

## Boundaries

Do not:

- log or request raw private chain-of-thought;
- infer symptom change from preference alone;
- overwrite previous measurements;
- expose diagnostic prediction to blind Product review;
- call telemetry declarations or exact mapping causal proof;
- call the workspace broker an OS sandbox;
- grant agents bypass tools and still claim broker isolation;
- generalize B03 into a global writing rule;
- add a registry, event bus, generic permission platform or new scoring layer.

## Next legitimate step

After this branch is validated, retry **one bounded real Plan -> Writer -> Truth/Product -> Audit learning round** with fresh role contexts and mandatory sealed decision telemetry.

A success, failure or inconclusive result is useful if the artifacts and decision history remain trustworthy. Do not modify architecture during that round before the evidence chain is complete.
