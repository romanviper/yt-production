# AI Agent Router — direct-output MVP

The immediate goal of this branch is simple: **produce Writer drafts for the Owner to read**.

Do not redesign, optimize or extend the architecture before the Owner has read the current Writer outputs and given feedback.

## If you are a Writer

If the Owner tells you to write P01, follow [WRITER.md](WRITER.md) immediately.

A direct Owner instruction is sufficient authority.

Do not wait for or require:

- `writer-assignment.json` or `assignment.json`;
- controller/runtime state;
- Writer budget approval;
- `tasks/ACTIVE.json` or a fresh canonical task;
- Planner/Reviewer/Audit/coordinator handoff.

Absence of those artifacts is not a blocker.

Writer flow:

```text
Owner says write P01
  → read the two inputs in WRITER.md
  → write one attempt
  → save draft + minimal metadata in your writer-output partition
  → commit
  → STOP for Owner reading
```

Do not read another Writer's output or Owner feedback before finishing. Do not self-review/reroll. Do not modify system architecture while acting as Writer.

## If you are operating the repo

Keep repo work minimal. Only change architecture/harness when:

1. the Owner explicitly asks for that change; or
2. a concrete blocker prevents a Writer from producing an output, and the smallest fix is necessary.

Prefer removing a constraint over adding a new abstraction.

Do not optimize for hypothetical future models, provenance systems, orchestration or benchmarking before real script output and Owner feedback exist.

## Output location

All current P01 Writer outputs live under:

`writer-output/P01/`

Each Writer/model uses its own partition containing only `draft.md` and `meta.json`.

## Historical material

Phase 1/2/3 experiments, coordinator prototypes, old budget/submission machinery and cancelled production tasks are not prerequisites for this direct-output MVP. Do not activate them unless the Owner explicitly asks.
