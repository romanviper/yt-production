# AI Agent Router

## Current owner-first MVP path

The current architecture task is **Owner-first MVP v3**. For the next bounded P01 reading comparison, start at [docs/MVP.md](docs/MVP.md) and use `python scripts/learning.py`.

The active MVP path is deliberately small:

```text
Owner request
  → frozen P01 authority + Sol repo brief
  → Owner-approved time budget for Sol repo only
  → Sol repo prepares one frozen Plan
  → one frozen common Writer assignment
  → Owner launches any number/models of Writers
  → each Writer returns one draft + self-declared provenance
  → Owner closes the submission pool
  → Owner reads and records verbatim comparison feedback
  → stop
```

There is **no separate Planner agent** in this MVP. Sol repo prepares the Plan as an operator/repo step but may not write Writer prose or choose a winner. Do not insert Product Review, Audit, a time-auditor, coordinator, FoC diagnosis, root-cause attribution, automatic reroll or self-improvement before the Owner gate.

### Budget rule

Only **Sol repo** is time-budget governed. It can modify/investigate the repo and therefore may expand scope. No Sol repo work may start until the Owner explicitly approves that exact budget request. Sol repo extensions require an exact Owner decision.

Writers have **no time-budget gate**. Writer timing is observability metadata only. Do not create Writer allocations, overrun extension requests, transfer unused Writer seconds, or block a valid Writer submission because it took longer than an arbitrary threshold.

### Dynamic Writer rule

Writers are not pre-registered actors. Do not hard-code Gemini/Sol/GPT-6/Claude into the controller merely to allow them to submit prose. Freeze the work, not the worker.

The common artifact is `control/writer-assignment.json`. Owner may launch any model/session externally. A Writer returns `draft.md` plus `execution-report.json` with its own model/provider/session/input/timing metadata.

A Writer that actually received the frozen assignment declares:

```text
assignment_binding = PREBOUND
```

and its assignment hash must match.

A Writer launched directly by Owner without the frozen assignment may still be preserved as readable evidence with:

```text
assignment_binding = NOT_PREBOUND
```

but the controller must mark it ineligible for controlled same-assignment claims. Never retroactively convert NOT_PREBOUND to PREBOUND.

Each `submission_id` is write-once. Writers get one content attempt: no self-review/reroll for a prettier result. Do not show an unfinished Writer another Writer's draft or Owner feedback.

Writer timing may be self-reported or `UNKNOWN`; either is acceptable provenance. Never infer model identity or timing that the Writer/host did not actually observe. Raw/private chain-of-thought must not be stored in execution metadata.

After Owner has enough submissions, `close-submissions` freezes the comparison set. No new Writer may enter that run after closure. Owner may select a completed `submission_id`, `TIE`, or `UNSELECTED`, and may separately name one submission as primary. A single preference must not silently become model-level evidence or a default model configuration.

The experiments under `docs/experiments/`, `experiments/`, historical Phase 1–3 material, and coordinator prototypes are **legacy/reference evidence only** for this MVP. They are not prerequisites for producing the reading set and must not be silently reactivated. The canonical production router described below remains a separate production flow.

This file contains repo-wide operating boundaries. Creative logic belongs in the frozen assignment or canonical production packet, not in this router.

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

- **Owner:** supplies the goal; approves Sol repo budget/extensions; launches any Writer models; decides when to close submissions; reads the frozen set; records selection/feedback; may explicitly choose a primary submission.
- **Sol repo:** snapshots authority, prepares one Plan and common Writer assignment, operates/tests/transfers repo artifacts, records repo-work budget/timing evidence; may not write Writer prose, self-approve budget, or choose a winner.
- **Dynamic Writer:** may be any model/session chosen by Owner. It writes one content attempt and self-declares provenance. It may not modify Plan/authority/control state, inspect another Writer/Owner feedback, self-review/reroll, or claim PREBOUND when it did not receive the frozen assignment.
- **Operator/controller:** may snapshot, hash, freeze and transfer artifacts and parse a real Owner decision into an immutable record; may not invent Owner approval, model identity, timing, production prose or feedback.
- **Review/Audit/time-auditor/coordinator:** inactive in this MVP unless Owner separately assigns a later work item.
- **System architect:** may change system/docs/tests in the assigned PR; may not create or approve production prose. Architecture repair cost is separate from Writer execution telemetry.

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

Stop and report a blocker when a canonical production packet is stale, malformed, missing an input, over budget or requires evidence outside its ceiling. Do not solve those failures by browsing extra files, widening scope or padding prose.

For the Owner-first MVP specifically:

- stop at `AWAITING_OWNER_BUDGET_APPROVAL` only for Sol repo budget/extension decisions;
- Writer timing never creates that state;
- reject duplicate/rerolled `submission_id` and PREBOUND hash mismatch;
- stop accepting Writers after `close-submissions`;
- stop at `AWAITING_OWNER_FEEDBACK` for Owner comparison;
- stop at `OWNER_FEEDBACK_RECORDED` after Owner feedback.

Literary weakness is not permission to open an architecture project or reroll a Writer. Any architecture repair requires explicit Owner scope/budget.

## User-facing handoff

For the Owner-first MVP, `python scripts/learning.py status --run <id>` is the single status surface. It must identify the waiting person/role, next action and artifact(s) to open, plus Sol repo budget state and the dynamic Writer submission list.

For canonical production task output, lead with `python scripts/task.py brief products/<slug> <task-id>`. Keep operational detail in `report.md`; expose deeper analysis only when the user asks for it or needs it to make a safe decision.
