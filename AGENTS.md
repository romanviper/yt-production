# AI Agent Router

## Current owner-first MVP path

The current architecture task is **Owner-first MVP**. For the first new P01 reading sample, start at [docs/MVP.md](docs/MVP.md) and use `python scripts/learning.py`.

The active MVP path is deliberately small:

```text
Owner request
  → frozen Planner packet
  → frozen Plan
  → frozen Writer packet
  → one Writer draft
  → Owner reads
  → verbatim Owner feedback
  → stop
```

Do not insert Product Review, Audit, A/B comparison, FoC diagnosis, root-cause attribution, automatic reroll or self-improvement before this Owner gate unless the Owner explicitly assigns it after reading the draft.

Planner and Writer sessions are separate roles. For manual packet transfer, give a role only its frozen packet and do not describe the transfer as host-enforced isolation. If a real host gives tools, grant only the role workspace broker; do not also grant shell, network or general repo/filesystem access and then call the CWD a sandbox.

After a draft is frozen, the only MVP state is `AWAITING_OWNER_FEEDBACK`. After feedback is recorded, the state is `OWNER_FEEDBACK_RECORDED` and the system waits for the Owner to choose the next change. Agent proposals are not implementation authority.

The experiments under `docs/experiments/`, `experiments/`, historical Phase 1–3 material, and coordinator prototypes are **legacy/reference evidence only** for this MVP. They are not prerequisites for producing the first reading sample and must not be silently reactivated. The canonical production router described below remains a separate production flow.

This file contains repo-wide operating boundaries. Creative logic belongs in the packet given to the active role.

## Canonical branch

- `main` is the repository source of truth. Start from current `main` unless the Owner explicitly assigns an isolated branch/PR, as with the current MVP implementation branch.
- Do not choose historical experiment branches as production inputs.
- Do not mix system architecture changes and product content in one commit.

## Authority

- Product work runs as `product_agent` and may write only the paths declared by its router-generated work order.
- An explicit user instruction to edit an outline or section output may run as a human-directed amendment instead of an AI task. It may touch only the creative output allowlists enforced by `scripts/approval.py`, must record provenance, and may not widen evidence authority.
- `.github/`, `AGENTS.md`, `Makefile`, `README.md`, `docs/`, `scripts/`, `system/`, `templates/` and `tests/` are protected system paths.
- A system defect is reported as a blocker. It does not grant a Product Agent permission to fix the system.
- System architecture changes require an explicit owner-assigned `system_architect` task and may not share a commit with product content.
- Only the user may approve research plans, outlines, story plans or sections.

## Owner-first MVP role boundaries

- **Planner:** reads only its frozen packet; writes its Plan/notes/scratch; may not expand evidence, call Writer or approve story content.
- **Writer:** reads only the frozen Plan + brief/authority in its packet; writes one draft/notes/scratch; may not modify Plan/standards, self-review or reroll.
- **Operator/controller:** may snapshot, hash, freeze and transfer artifacts; may not write Planner/Writer content or Owner feedback.
- **Review/Audit:** inactive in the first-reading path unless Owner separately assigns them a frozen bundle.
- **System architect:** may change system/docs/tests in the assigned PR; may not create or approve production prose.

Manual handoff telemetry must say it is manual. Do not fabricate spawn receipts, host execution timestamps, independence attestations, hidden chain-of-thought or causal proof. If a host log really exists, preserve it unchanged and distinguish its execution time from the operator receive time.

## Product task entrypoint

The following is the separate canonical production flow, not a prerequisite for the Owner-first reading MVP.

1. Resolve the named product. If the repo has only one product and none is named, use it.
2. Read `products/<slug>/tasks/ACTIVE.json`, its work order and the single compiled context packet it references.
3. Do not scan the repository or load files outside that packet.
4. Write only `allowed_write_paths`, run the packet's validations, produce `report.md` and `operator-brief.json`, then submit through `scripts/task.py`.
5. Stop at the current checkpoint. Do not silently start the next operation.

The task entrypoint applies to AI-generated work. For explicit human feedback or a direct human edit, use `human-amend-outline` or `human-amend-section`; do not create a replacement task merely to legitimize the user's authority.

When the user asks to replay a bounded production path across multiple operations, use `scripts/replay.py` instead of manually editing task or section state. `replay.py start` records the requested path and routes only its first canonical task; after each required human approval, `replay.py continue` materializes or routes the next task. Human approval gates remain mandatory. Single-operation reruns still use `scripts/rework.py`.

An `outline` work order compiled with `execution_runtime.kind: dsh` is the only POC exception to direct packet consumption. Launch it through `scripts/outline_runtime.py`; the Agent receives a minimal seed and may access repository context only through the packet-declared, audit-logged capability broker. Do not grant that runtime filesystem, shell, web or repo-scan tools.

For a newly requested production operation, create it through `python scripts/task.py create`; never hand-author router artifacts. Operation names and preconditions are machine-readable in `system/operations/registry.json`.

## Hard stops

Stop and report a blocker when a packet is stale, malformed, missing an input, over budget or requires evidence outside its ceiling. Do not solve those failures by browsing extra files, widening scope or padding prose.

For the Owner-first MVP specifically, also stop after `AWAITING_OWNER_FEEDBACK` and after `OWNER_FEEDBACK_RECORDED`. Literary weakness is not permission to open an architecture project or generate another candidate.

## User-facing handoff

For the Owner-first MVP, `python scripts/learning.py status --run <id>` is the single status surface. It must identify the waiting role/person, next action and artifact to open.

For canonical production task output, lead with `python scripts/task.py brief products/<slug> <task-id>`. Keep operational detail in `report.md`; expose deeper analysis only when the user asks for it or needs it to make a safe decision.
