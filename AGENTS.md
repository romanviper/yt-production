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
2. Use `python -m learning_runtime.phase3 p01-rootcause-01 --out <run-dir>` for the current white-box slice.
3. Treat `plan/trace.jsonl`, `write/trace.jsonl`, `diagnosis.json`, and `phase3-manifest.json` as Phase 3 diagnostic artifacts.
4. Keep observations separate from derived diagnosis. A diagnosis may bound a fault region; it is not final causal proof.
5. The current bounded intervention is `learning_runtime/interventions/p01-rootcause-01-plan-only.json`.
6. Do not fabricate a live rerun. A live Writer execution must use the same evidence ceiling and return to Product/owner measurement.

## Phase 3 boundaries

Allowed in the current MVP:

- exact output-span -> Writer-beat -> Plan-node mapping;
- structured trace events and hashes;
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

## User-facing handoff

For task output, lead with `python scripts/task.py brief products/<slug> <task-id>`. Keep operational detail in `report.md`; expose deeper analysis only when the user asks for it or needs it to make a safe decision.
