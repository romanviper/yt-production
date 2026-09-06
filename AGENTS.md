# AI Agent Router

## Current architecture-learning phase

The repository is currently in **Observable Learning Architecture — Phase 2 MVP**.
For owner-directed architecture-learning work, start at `docs/phase2/START.md` and
read `docs/architecture/observable-learning-architecture-plan.md` only as historical
design context. The active MVP objective is intentionally narrower than the original
full Phase 2 plan.

For architecture-learning work, `learning_runtime/` is the only active execution
path. Its topology is exactly:

`Plan -> Write -> Truth -> Product`

Phase 2 uses deterministic fixture replay to prove stage boundaries and artifacts.
It does not authorize a new Writer round, live Planner/Writer orchestration,
white-box tracing, root-cause claims, benchmark expansion, or production prose.
Those belong to Phase 3 or explicit owner-directed product work.

The Phase 1 benchmark under `benchmarks/p01/` remains the current measurement
surface. Do not continue benchmark perfection work unless a concrete learning-loop
failure shows that the measurement surface itself is blocking diagnosis.

The experiments under `docs/experiments/`, `experiments/`, and
`scripts/experiments/` are **legacy evidence only**. Their historical `START.md`
files and scripts must not be treated as active entrypoints, rerun, extended, or
used to create a new round unless the owner explicitly re-authorizes that exact
experiment. Existing run artifacts may be imported as immutable Phase 2 smoke
fixtures, but their historical evaluator verdicts do not become ground truth.

This file contains only repo-wide operating boundaries. Creative logic belongs in the task packet.

## Canonical branch

- `main` remains the canonical production branch and repository source of truth.
- `codex/p01-phase2-minimal-runtime` is an owner-authorized architecture-learning branch; it must not mutate production product state.
- Do not create additional feature, task or agent branches for routine production work. Historical remote branches are not valid production inputs.

## Architecture-learning entrypoint

For Phase 2 MVP work:

1. Read `docs/phase2/START.md`.
2. Use `python -m learning_runtime.run p01-mvp --out <run-dir>` for the smoke path.
3. Treat generated `input.json`, `output.*`, and `manifest.json` files as the only Phase 2 runtime artifacts.
4. Do not call production router/rework/replay scripts from the Phase 2 runtime.
5. Stop after the four-stage smoke path. Do not add trace/event infrastructure or live agents in Phase 2.

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

An `outline` work order compiled with `execution_runtime.kind: dsh` is the only POC exception to direct packet consumption. Launch it through `scripts/outline_runtime.py`; the Agent receives a minimal seed and may access repository context only through the packet-declared, audit-logged capability broker. Do not grant that runtime filesystem, shell, web or repo-scan tools.

For a newly requested operation, create it through `python scripts/task.py create`; never hand-author router artifacts. Operation names and preconditions are machine-readable in `system/operations/registry.json`.

## Hard stops

Stop and report a blocker when the packet is stale, malformed, missing an input, over budget or requires evidence outside its ceiling. Do not solve those failures by browsing extra files, widening scope or padding prose.

## User-facing handoff

For task output, lead with `python scripts/task.py brief products/<slug> <task-id>`. Keep operational detail in `report.md`; expose deeper analysis only when the user asks for it or needs it to make a safe decision.
