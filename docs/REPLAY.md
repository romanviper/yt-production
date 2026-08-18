# Semantic Production Replay

Use replay when the human request names a bounded **path**, not just one operation. Example: “apply the current harness and replay from outline through P01 draft.”

```bash
python scripts/replay.py start products/<slug> \
  --from outline \
  --through draft_section \
  --section P01 \
  --request "Replay current harness from outline through P01 draft"
```

The command routes only the first canonical task and records the durable intent in `replay-state.json`. It does not bypass human approval.

After the current task is submitted, call:

```bash
python scripts/replay.py continue products/<slug>
```

`continue` behaves semantically:

- while the current task is still `ready` or `in_progress`, it waits for task completion;
- after outline submission, it waits for human outline approval;
- after outline approval, it archives prior-cycle section workspaces when necessary, materializes the approved sections, and routes `design_section`;
- after story-plan submission, it waits for human story-plan approval;
- after story-plan approval, it routes `draft_section` using the narration pack produced by the existing approval path;
- after the terminal replay task is submitted, the replay is marked complete.

The replay layer delegates state transitions to existing primitives (`rework.py`, `lifecycle.py`, `materialize_sections.py`, `task.py`). It must not become a second lifecycle authority.

For a one-operation rerun, keep using `rework.py`. For recovery/debugging, low-level state commands remain available, but an Agent should not use them to satisfy an ordinary human replay request.
