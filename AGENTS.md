# AI Agent Router

## Current architecture-learning phase

The repository is currently in **Observable Learning Architecture — Phase 3 MVP**.
For owner-directed architecture-learning work, start at `docs/phase3/START.md`.
The active learning path remains `learning_runtime/` with the fixed topology:

`Plan -> Write -> Truth -> Product`

Phase 3 adds white-box instrumentation only where it reduces fault uncertainty.
The current MVP instruments `Plan` and `Write` so an observed output failure can
be traced backward to a mapped Writer beat and Plan node. Do not expand this into
a generic observability platform, agent registry, event bus or root-cause engine.

The Phase 1 benchmark under `benchmarks/p01/` remains the output-side measurement
surface. Guided owner review may provide diagnostic failure seeds, but it does not
become blind calibration evidence. Do not resume benchmark-perfection work unless
a concrete learning-loop failure shows that the measurement surface itself blocks
diagnosis.

The experiments under `docs/experiments/`, `experiments/`, and
`scripts/experiments/` are **legacy evidence only**. Their historical artifacts may
be imported as immutable trace fixtures, but historical evaluator verdicts do not
become current ground truth. Do not rerun or extend those experiments unless the
owner explicitly re-authorizes that exact experiment.

This file contains only repo-wide operating boundaries. Creative logic belongs in
the bounded task/intervention packet.

## Canonical branches

- `main` remains the canonical production branch and repository source of truth.
- `codex/p01-phase3-whitebox-mvp` is an owner-authorized architecture-learning branch; it must not mutate production product state.
- Historical architecture branches are evidence, not active production inputs.

## Architecture-learning entrypoint

For Phase 3 MVP work:

1. Read `docs/phase3/START.md`.
2. Read `docs/phase3/decision-telemetry-contract.md` before any fresh agent execution.
3. Use `python -m learning_runtime.phase3 p01-rootcause-01 --out <run-dir>` for the current white-box slice.
4. Treat `plan/trace.jsonl`, `write/trace.jsonl`, `diagnosis.json`, and `phase3-manifest.json` as Phase 3 diagnostic artifacts.
5. Keep observations separate from derived diagnosis. A diagnosis may bound a fault region; it is not final causal proof.
6. The current bounded intervention is `learning_runtime/interventions/p01-rootcause-01-plan-only.json`.
7. Do not fabricate a live rerun. A live Writer execution must use the same evidence ceiling and return to Product/owner measurement.

## Structured process telemetry — mandatory for fresh roles

A fresh Plan, Writer, Truth or Audit execution must not return only a final artifact plus a retrospective explanation.
While it is working, the role must emit ordered structured telemetry through its `RoleWorkspaceBroker` to:

`output/telemetry.jsonl`

Allowed event classes are bounded engineering/editorial observations:

- `DECISION`
- `CHECKPOINT`
- `RISK`
- `DEVIATION`

A `DECISION` records the chosen action, concise declared rationale, evidence refs,
alternatives considered, expected effect, risks and affected output refs. This is
**declared process evidence**, not raw private chain-of-thought and not causal proof.

For Plan, Writer, Truth and Audit, the telemetry is also temporally binding: a
`DECISION` naming the exact `output/<path>` must exist **before** that final output
is materialized. Final artifacts under `output/` are write-once through the broker.
If the role needs to explore, rewrite or compare alternatives, it must do that under
`scratch/` and only materialize the final artifact after its bounded decision has
been declared. The seal independently checks that every primary output is bound to
a decision, so a direct-filesystem bypass fails closed at handoff.

Do not request, store or simulate unrestricted private chain-of-thought, hidden
scratchpads, internal monologues or token-by-token reasoning. Runtime validation
rejects fields such as `chain_of_thought`, `private_reasoning` and
`internal_monologue`.

Before any downstream handoff or feedback, the launcher must validate telemetry,
hash telemetry + declared primary outputs, and create an execution seal under:

`control/seals/<role>-<execution-id>.json`

After seal, broker writes from that execution are denied. A handoff may copy only
an artifact whose identity is present in a valid source execution seal. This freeze
is required so downstream feedback cannot be used to rewrite earlier rationale.

The blind Product reviewer is the exception: do not force analytical decision
rationale before its first-pass vote. Freeze the preference first; post-vote
diagnostic observation may follow afterward.

## Phase 3 boundaries

Allowed in the current MVP:

- exact output-span -> Writer-beat -> Plan-node mapping;
- structured trace events and hashes;
- in-execution structured decision/process telemetry with temporal output binding and pre-feedback seals;
- Plan-vs-realization fault isolation;
- one bounded intervention targeted to the diagnosed region;
- recording process/output and validation evidence.

Not authorized merely by Phase 3:

- production draft mutation;
- broad Planner/Writer harness rewrite;
- adding many specialist agents;
- replacing Truth/Product contracts;
- claiming improvement before a new output is measured;
- unrestricted private chain-of-thought logging.

## Authority

- Product work runs as `product_agent` and may write only the paths declared by its router-generated work order.
- An explicit user instruction to edit an outline or section output may run as a human-directed amendment instead of an AI task. It may touch only the creative output allowlists enforced by `scripts/approval.py`, must record provenance, and may not widen evidence authority.
- `.github/`, `AGENTS.md`, `Makefile`, `README.md`, `docs/`, `scripts/`, `system/`, `templates/` and `tests/` are protected system paths.
- A system defect is reported as a blocker. It does not grant a Product Agent permission to fix the system.
- System architecture changes require an explicit owner-assigned `system_architect` task and may not share a commit with product content.
- Only the user may approve research plans, outlines, story plans or sections.

## Product task entrypoint

1. Resolve the named product. If the repo has only one product and none is named, use it.
2. Read `products/<slug>/tasks/ACTIVE.json`, its work order and the single compiled context packet it references.
3. Do not scan the repository or load files outside that packet.
4. Write only `allowed_write_paths`, run the packet's validations, produce `report.md` and `operator-brief.json`, then submit through `scripts/task.py`.
5. Stop at the current checkpoint. Do not silently start the next operation.

The task entrypoint applies to AI-generated work. For explicit human feedback or a direct human edit, use `human-amend-outline` or `human-amend-section`; do not create a replacement task merely to legitimize the user's authority.

When the user asks to replay a bounded production path across multiple operations, use `scripts/replay.py` instead of manually editing task or section state. `replay.py start` records the requested path and routes only its first canonical task; after each required human approval, `replay.py continue` materializes or routes the next task. Human approval gates remain mandatory. Single-operation reruns still use `scripts/rework.py`.

For a newly requested production operation, create it through `python scripts/task.py create`; never hand-author router artifacts. Operation names and preconditions are machine-readable in `system/operations/registry.json`.

## Hard stops

Stop and report a blocker when the packet is stale, malformed, missing an input, over budget or requires evidence outside its ceiling. Do not solve those failures by browsing extra files, widening scope or padding prose.

For a fresh Phase 3 role, also stop before final output/handoff if a required decision
has not been declared for that exact output path, if telemetry is missing/invalid,
if the execution cannot be sealed, or if the sealed artifact identity no longer
matches. Do not downgrade these to warnings.

## User-facing handoff

For task output, lead with `python scripts/task.py brief products/<slug> <task-id>`. Keep operational detail in `report.md`; expose deeper analysis only when the user asks for it or needs it to make a safe decision.
