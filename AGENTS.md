# AI Agent Router — direct-output MVP

The immediate goal of this branch is simple: **produce Writer drafts the Owner can read and diagnose**.

Do not redesign, optimize or extend the architecture before the Owner has read Writer outputs and given feedback.

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
  → read the canonical inputs in WRITER.md
  → record the small PRE-WRITE SNAPSHOT
  → write one prose attempt
  → freeze draft
  → complete the POST-WRITE TRACE
  → save draft + metadata + writing report in your partition
  → commit
  → STOP for Owner reading
```

The observability artifacts exist for the **Owner**, not for an automated evaluator. Do not score, rank, PASS/FAIL, or decide whether the Writer succeeded. Record observable facts, final decisions, source mappings, material changes, uncertainty, and self-observed risk locations so the Owner can inspect them directly.

Do not store chain-of-thought, private reasoning, hidden scratchpads, or internal-monologue transcripts.

Do not read another Writer's output or Owner feedback before finishing. Do not reroll the prose. Do not modify system architecture while acting as Writer.

## If you are operating the repo

Keep repo work minimal. Only change architecture/harness when:

1. the Owner explicitly asks for that change; or
2. a concrete blocker prevents a Writer from producing an output, and the smallest fix is necessary.

Prefer removing a constraint over adding a new abstraction.

Do not optimize for hypothetical future models, provenance systems, orchestration or benchmarking before real script output and Owner feedback exist.

Do not replace Owner judgment with automated quality gates. Writer observability should expose behavior and evidence, not decide quality on the Owner's behalf.

## Output location

All current P01 Writer outputs live under:

`writer-output/P01/`

Each Writer/model uses its own partition containing exactly:

- `draft.md`
- `meta.json`
- `writing-report.md`

`meta.json` is compact factual execution metadata. `writing-report.md` is the human-readable behavioral/evidence trace defined in `WRITER.md`.

## Historical material

Phase 1/2/3 experiments, coordinator prototypes, old budget/submission machinery and cancelled production tasks are not prerequisites for this direct-output MVP. Do not activate them unless the Owner explicitly asks.
