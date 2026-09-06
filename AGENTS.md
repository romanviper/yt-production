# AI Agent Router

## Current owner-first MVP path

The current architecture task is **Owner-first MVP**. For the next bounded P01 reading comparison, start at [docs/MVP.md](docs/MVP.md) and use `python scripts/learning.py`.

The active MVP path is deliberately small:

```text
Owner request
  → frozen P01 authority + Sol repo brief
  → Owner-approved time budget
  → Sol repo prepares one frozen Plan
  → two frozen Writer packets with the same common-content hash
      ├─ Writer Gemini 3.8 Flash → sample A
      └─ Writer GPT-5.6 Sol     → sample B
  → timing/budget report
  → Owner reads and records verbatim comparison feedback
  → stop
```

There is **no separate Planner agent** in this amended MVP. Sol repo prepares the Plan as an operator/repo step but may not write either production draft or choose the winning Writer. Do not insert Product Review, Audit, a time-auditor, coordinator, FoC diagnosis, root-cause attribution, automatic reroll or self-improvement before the Owner gate.

No Sol repo or Writer work may be dispatched until a budget proposal exists and the Owner has explicitly approved that exact initial request. Budget proposals are not approvals. Extension silence/rejection is not approval. Manual approval records preserve verbatim Owner text/source but are not an authentication system.

Writer Gemini and Writer Sol are separate sessions. Writer Sol must not reuse the Sol repo context. Give each Writer only its own frozen packet/workspace; do not show the first draft, Owner feedback, architecture context, baseline predictions, or the other Writer's packet/output to the unfinished Writer. Both Writer packets must bind the same common content hash while keeping session/model metadata separate.

Each Writer has one content attempt. A technical failure/retry must preserve the failed attempt, reason and timing; do not reroll for a prettier result. One failed/timed-out Writer leaves the pair incomplete; do not substitute historical prose, a third Writer, or Sol repo-authored prose.

For manual packet transfer, timing may be recorded as `OPERATOR_OBSERVED_SESSION_WINDOW`; that window may include waiting and is not active inference time. Never infer runtime from `agent_created_at`, operator receive timestamps, or file timestamps. Missing timing is `UNKNOWN`, not zero. Work time, round elapsed time and wait time are separate quantities.

When a Writer output arrives after exceeding the approved allocation, preserve the output as pending evidence but do not silently publish it to the Owner sample or start new work. Move to `AWAITING_OWNER_BUDGET_APPROVAL`. Resume only after an approval that matches the exact request/actor/scope/seconds; extensions add history and never reset usage or grant another content attempt.

If a real host gives tools, grant only the role workspace broker; do not also grant shell, network or general repo/filesystem access and then call the CWD a sandbox. The controller currently does not own an external host process, so do not claim hard timeout/cancel enforcement where only next-step blocking and observed overrun recording are available.

After both samples are frozen, the state is `AWAITING_OWNER_FEEDBACK`. Owner may select `A/B/TIE/UNSELECTED` and may separately name a primary Writer. A single sample preference is not model-level evidence and must not silently become a default model configuration. After feedback is recorded, state is `OWNER_FEEDBACK_RECORDED` and the system waits for the Owner to choose the next change/budget.

The experiments under `docs/experiments/`, `experiments/`, historical Phase 1–3 material, and coordinator prototypes are **legacy/reference evidence only** for this MVP. They are not prerequisites for producing the reading pair and must not be silently reactivated. The canonical production router described below remains a separate production flow.

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

- **Owner:** supplies the goal; approves initial budget/extensions; reads both samples; records selection/feedback; may explicitly choose a primary Writer.
- **Sol repo:** snapshots authority, prepares one Plan, operates/tests/transfers repo artifacts, records budget/timing evidence; may not write Writer prose, self-approve budget, or choose a winner.
- **Writer Gemini / Writer Sol:** each reads only its own packet and workspace; writes one content attempt plus notes/scratch; may not modify Plan/authority/budget/control state, inspect the other Writer, self-review/reroll, or call another role.
- **Operator/controller:** may snapshot, hash, freeze and transfer artifacts and parse a real Owner decision into an immutable record; may not invent Owner approval, timing, Writer identity, production prose or feedback.
- **Review/Audit/time-auditor/coordinator:** inactive in this MVP unless Owner separately assigns a later work item/budget.
- **System architect:** may change system/docs/tests in the assigned PR; may not create or approve production prose. Architecture repair cost must be reported separately from per-round execution cost when the Owner requests runtime accounting.

Manual handoff telemetry must say it is manual. Do not fabricate spawn receipts, host execution timestamps, independence attestations, hidden chain-of-thought or causal proof. If a host log really exists, preserve it unchanged and distinguish observed invocation/session duration from operator receive time.

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

For the Owner-first MVP specifically:

- stop at `AWAITING_OWNER_BUDGET_APPROVAL`; no agent dispatch without matching Owner approval;
- stop new work when timing is `UNKNOWN` or approved budget is exhausted/overrun;
- stop at `AWAITING_OWNER_FEEDBACK` after both valid samples;
- stop at `OWNER_FEEDBACK_RECORDED` after Owner feedback.

Literary weakness is not permission to open an architecture project, reroll a Writer, generate a third candidate, or transfer unused allocation between actors. Any architecture repair or reallocation requires explicit Owner scope/budget.

## User-facing handoff

For the Owner-first MVP, `python scripts/learning.py status --run <id>` is the single status surface. It must identify the waiting person/role, next action and artifact(s) to open, plus budget/timing state including total work, elapsed, wait, overrun and UNKNOWN where applicable.

For canonical production task output, lead with `python scripts/task.py brief products/<slug> <task-id>`. Keep operational detail in `report.md`; expose deeper analysis only when the user asks for it or needs it to make a safe decision.
