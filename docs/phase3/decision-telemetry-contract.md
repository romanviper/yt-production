# Phase 3 — Structured Decision / Process Telemetry Contract

Status: **REQUIRED BEFORE THE NEXT REAL LEARNING ROUND**

## Purpose

The learning runtime must not reduce an agent execution to only `input -> final output` plus a retrospective explanation. For Plan, Writer, Truth and Audit roles, the runtime requires structured engineering/editorial telemetry to be emitted while the role is executing and frozen before downstream handoff or feedback.

This telemetry exists to answer questions such as:

- which evidence or Plan fields a decision bound to;
- which bounded action the role chose;
- what concise declared rationale supported that choice;
- what alternative was explicitly rejected or deferred;
- what effect the role expected on the downstream artifact;
- which risks or uncertainties were noticed at the time;
- whether the role knowingly deviated from its declared upstream input;
- which output span/artifact the decision affected.

It is **not** a request for raw private chain-of-thought, hidden scratchpad reasoning, internal monologue or token-by-token reasoning.

## Artifact

Each role execution writes:

```text
agents/<role>/<execution-id>/
  input/
  output/
    <role artifact(s)>
    telemetry.jsonl
  scratch/
```

Schema: `schemas/decision-telemetry-event.schema.json`

Runtime version: `PHASE3-DECISION-TELEMETRY-1`

Events are append-ordered. The broker assigns `role`, `execution_id` and monotonic `sequence`; the agent cannot use another role identity.

## Temporal rule: decision before final artifact

A seal alone is not sufficient because an agent could otherwise finish an artifact and then write a plausible rationale immediately before sealing it.

For **Plan, Writer, Truth and Audit** the broker therefore requires:

```text
work / exploration
      ↓
scratch/  (may be rewritten)
      ↓
DECISION event naming exact output/<path>
      ↓
first and only final write to output/<path>
      ↓
optional later CHECKPOINT / RISK / DEVIATION events
      ↓
seal
      ↓
downstream handoff
```

Rules:

1. A `DECISION` that names the exact final `output/<path>` must already exist before that final artifact can be materialized.
2. Final artifacts in `output/` are write-once through the broker. If the agent still needs to explore, rewrite or compare alternatives, it must use `scratch/`.
3. The execution seal independently checks that every declared primary output is bound to at least one decision; this catches direct-filesystem/broker-bypass cases at the handoff boundary.
4. After seal, no broker write is allowed, including telemetry or scratch writes.

This establishes an observable ordering relation between declared decisions and final output. It does **not** prove that the declared rationale was the hidden psychological cause of the choice; telemetry remains self-report process evidence.

## Event types

### DECISION

A bounded declared choice that can affect downstream output. Required fields include:

```text
decision_type
chosen_action
rationale_summary
evidence_refs
alternatives_considered
expected_effect
risks
output_refs
```

`rationale_summary` is a short engineering/editorial explanation, not a reasoning transcript. `output_refs` must use bounded `output/<path>` references.

Examples of useful decisions:

- Planner: `INFORMATION_ORDER`, `EVIDENCE_SELECTION`, `DEFER_OR_REVEAL`.
- Writer: `REALIZATION_STRATEGY`, `EXPLICITNESS`, `PLAN_DEVIATION`.
- Truth: `CLAIM_CLASSIFICATION`, `EVIDENCE_JUDGMENT`, `QUALIFICATION`.
- Audit: `ATTRIBUTION`, `EVIDENCE_LIMITATION`, `HYPOTHESIS_UPDATE`.

Plan, Writer, Truth and Audit executions must contain at least one `DECISION` before they can be sealed, and each primary output must be named by a decision.

### CHECKPOINT

Records a bounded execution milestone and artifact refs, for example `B03_REALIZATION_COMPLETE` or `FIRST_PASS_VOTE_FROZEN`.

### RISK

Records a risk noticed during execution plus its mitigation or explicit acceptance.

### DEVIATION

Records a conscious departure from an upstream Plan/contract, the chosen action, concise reason, evidence and affected output refs.

## Product review exception

The blind Product reviewer must not be forced to generate analytical rationale before its first-pass preference is frozen. A Review role may therefore materialize and seal a first-pass preference with checkpoint telemetry and zero `DECISION` events.

Only after the vote is frozen may post-vote diagnostic observation be collected. Diagnostic target, attribution and intervention prediction remain hidden before the first-pass vote.

## Freeze rule

An execution is not eligible for handoff merely because its output file exists.

The runtime must:

1. validate `telemetry.jsonl`;
2. require bounded decision evidence for Plan / Writer / Truth / Audit;
3. verify every primary output is bound to a prior decision;
4. hash telemetry and declared primary outputs;
5. create `control/seals/<role>-<execution-id>.json`;
6. reject all broker writes from that execution after seal;
7. allow handoff only from an artifact identity present in the valid execution seal.

The seal status is:

```text
SEALED_BEFORE_DOWNSTREAM_FEEDBACK
```

This prevents downstream Product/Truth/Audit feedback from being used to silently rewrite the agent's earlier declared rationale or output.

## Evidence authority

Decision telemetry is **declared process evidence**. It has more diagnostic value than an unstructured retrospective essay because it is ordered, bound before final materialization and frozen before downstream feedback, but it is still self-report.

Therefore:

```text
telemetry declaration != causal proof
telemetry declaration != semantic adherence proof
telemetry declaration != product-quality evidence
```

A downstream auditor may contradict an agent's declared rationale using actual artifact evidence.

## Prohibited fields

Runtime validation rejects fields named:

```text
chain_of_thought
raw_chain_of_thought
private_reasoning
internal_monologue
hidden_reasoning
scratchpad_reasoning
```

If a role needs to justify a choice, it must express the externally useful decision record: action, evidence, concise rationale, alternatives, expected effect, risks and output mapping.

## Round-01 gate

Do not restart Phase 3 Learning Round 01 until the execution path used for the fresh Planner/Writer/Truth/Audit roles can demonstrate:

```text
role packet includes telemetry contract
-> role explores only in scratch/
-> role emits bounded DECISION for exact final output path
-> final output is materialized once
-> output overwrite is denied
-> primary output + telemetry validate
-> execution seal is created
-> post-seal mutation is denied
-> handoff verifies seal + artifact hash
-> downstream role receives only the sealed artifact
```

The next round must preserve these records alongside the final artifacts so an output failure can be traced through both artifact structure and the decisions that produced it.
