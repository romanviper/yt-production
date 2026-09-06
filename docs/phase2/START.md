# Phase 2 — Minimal Learning Runtime

Status: **ACTIVE MVP**

## Goal

Phase 2 does one thing: create the smallest unambiguous execution path that Phase 3 can instrument.

Active topology:

```text
Plan -> Write -> Truth -> Product
```

This is not a production rewrite and not an agent framework.

## MVP command

```bash
python -m learning_runtime.run p01-mvp --out /tmp/p01-phase2-mvp
```

The smoke scenario replays immutable historical artifacts through the new stage boundaries. It does **not** invoke a Writer, rerun a legacy experiment, certify an old Truth verdict, or create production prose.

Expected output:

```text
/tmp/p01-phase2-mvp/
  manifest.json
  plan/
    input.json
    output.json
    manifest.json
  write/
    input.json
    output.md
    manifest.json
  truth/
    input.json
    output.json
    manifest.json
  product/
    input.json
    output.json
    manifest.json
```

Every node records parent linkage plus input/output/source hashes. `trace_available=false` is intentional. White-box trace belongs to Phase 3.

## Active architecture boundary

For architecture-learning work, `learning_runtime/` is now the only active execution path.

The existing production router, approval/rework/replay framework, legacy experiments and task machinery remain in the repository for production compatibility and historical evidence. Phase 2 does not delete or refactor them. They are not dependencies of the MVP runtime.

## What is deliberately absent

Do not add these during Phase 2:

- agent registry;
- event bus;
- generic plugin/module framework;
- trace/event telemetry;
- root-cause engine;
- live Planner/Writer orchestration;
- benchmark expansion;
- new P01 prose.

Those are Phase 3 or later concerns.

## Validation

```bash
python -m unittest tests.test_learning_runtime -v
python -m learning_runtime.run p01-mvp --out /tmp/p01-phase2-mvp
```

## Exit criterion

Phase 2 MVP is ready when:

1. the four stages run in exactly `Plan -> Write -> Truth -> Product` order;
2. each stage has explicit input/output/manifest artifacts and hashes;
3. stage parentage is mechanically inspectable;
4. the runtime does not call legacy scripts or production router code;
5. historical evaluator artifacts retain explicit trust limitations;
6. the generated surface is sufficient for Phase 3 to add trace to Plan and Write without another repo-wide refactor.

Passing Phase 2 does not mean the writing system improved. It means there is finally one small path on which improvement can be measured and traced.
