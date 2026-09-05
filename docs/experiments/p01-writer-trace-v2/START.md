# P01 writer-observability loop v2

> **LEGACY / EVIDENCE ONLY.** Round 1 is complete and this experiment is closed.
> Do not run `plan`, `lock-plan`, `prepare`, or `decide` as the current workflow.
> Preserve the run artifacts as calibration/provenance evidence. Current
> architecture work starts at `docs/phase1/START.md`.

Owner-authorized diagnostic experiment on `codex/p01-writer-trace-loop-v2`, based on `2bf59edd0a5e83a9d186146bff4bd6e0c18c671b`. The frozen v1 experiment and production paths are read-only.

## 1. Preflight and Planner packet

```text
python scripts/experiments/p01_writer_trace_v2.py check
python scripts/experiments/p01_writer_trace_v2.py plan --run round-01
```

`check` must return `READY_FOR_PLANNING`. `plan` creates `planner-packet.json`. Dispatch only that packet to a fresh Planner context. Save the unedited platform request/response export in the run directory and save the Planner's JSON response as `writing-plan.json`.

The Planner writes structure only. No candidate prose is allowed in the plan.

## 2. Freeze plan and dispatch Writer

```text
python scripts/experiments/p01_writer_trace_v2.py lock-plan --run round-01
```

This validates evidence bindings and listener-state transitions, freezes `writing-plan.json`, and generates `writer-packet.json`.

Dispatch only `writer-packet.json` to a fresh Writer context with repository, shell, web, old baseline, FoC transcripts, previous verdicts and planner conversation unavailable. The Writer returns `candidate.md` plus `writer-report.json`. The report is a decision/deviation log, not chain-of-thought.

## 3. Prepare independent audits

```text
python scripts/experiments/p01_writer_trace_v2.py prepare --run round-01
```

This creates Truth, two counterbalanced blind Product packets, and a Trace Auditor packet. Truth/Product contexts must not receive the plan or Writer report. Trace Auditor receives plan + candidate + Writer report but no Product verdicts.

Complete `execution.json` from the generated template for all six roles: Planner, Writer, Trace Auditor, Truth, Product 1 and Product 2.

## 4. Decide and diagnose

```text
python scripts/experiments/p01_writer_trace_v2.py decide --run round-01
```

Interpretation: coherent plan + failed prose => Writer realization failure; weak plan + weak prose => planning representation failure; mixed => isolate one failure next; blind improvement + no trace failure => listening trial only, still provisional.
