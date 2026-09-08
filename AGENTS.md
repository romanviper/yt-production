# AI Agent Router — compression-first Writer MVP

The immediate goal of this branch is simple: **let the Owner inspect the story before anyone spends effort turning it into polished prose**.

Do not redesign, optimize or extend the architecture before the Owner has read the Writer output and given feedback.

## If you are a Writer

If the Owner tells you to write P01 or start Writer round 1, follow [WRITER.md](WRITER.md) immediately.

A direct Owner instruction is sufficient authority.

Do not wait for or require:

- `writer-assignment.json` or `assignment.json`;
- controller/runtime state;
- Writer budget approval;
- `tasks/ACTIVE.json` or a fresh canonical task;
- Planner/Reviewer/Audit/coordinator handoff.

Absence of those artifacts is not a blocker.

Current Writer flow:

```text
Owner starts Writer round 1 for P01
  → read the three canonical inputs in WRITER.md
  → write one narrative compression
  → save compression.md in the Writer partition
  → commit
  → STOP for Owner reading

Owner approves the compression and later gives a separate prose order
  → only then may a Writer expand the approved story into listener-facing prose
```

Round 1 is **a short telling of the whole story, before expansion into a full podcast script**. Do not create a draft, writing report, metadata packet, scorecard or alternative versions unless the Owner explicitly asks for them.

Do not store chain-of-thought, private reasoning, hidden scratchpads, or internal-monologue transcripts.

Do not read another Writer's compression or Owner feedback on another Writer before finishing your own attempt when the Owner wants an independent comparison. Do not modify system architecture while acting as Writer.

## If you are operating the repo

Keep repo work minimal. Only change architecture/harness when:

1. the Owner explicitly asks for that change; or
2. a concrete blocker prevents a Writer from producing an output, and the smallest fix is necessary.

Prefer removing a constraint over adding a new abstraction.

Do not add code enforcement for the compression-first loop unless the Owner explicitly asks for it. The current contract is instructional and intentionally lightweight.

Do not replace Owner judgment with automated quality gates. The Owner decides whether a compression is ready to become prose.

## Output location

All current P01 Writer outputs live under:

`writer-output/P01/`

For a new round-1 attempt, each Writer/model writes:

`writer-output/P01/<writer>/compression.md`

Existing historical `draft.md`, `meta.json` and `writing-report.md` files may remain where they already exist. Do not delete or rewrite them merely to conform to the new loop.

## Historical material

Phase 1/2/3 experiments, coordinator prototypes, old budget/submission machinery and cancelled production tasks are not prerequisites for this compression-first MVP. Do not activate them unless the Owner explicitly asks.

