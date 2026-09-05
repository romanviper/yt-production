# Legacy experiments

The experiment directories in this section are preserved as historical evidence.
They are **not active workflow entrypoints** after the Observable Learning
Architecture plan was merged into `main`.

## Preserved experiments

- `p01-foc-loop/` — evidence-led FoC comparison experiment (v1).
- `p01-writer-trace-v2/` — writer observability diagnostic experiment; round 1
  completed and preserved under `experiments/p01-writer-trace-v2/runs/round-01/`.

Their packet generators, tests, run reports, reviewer exports, and decision files
remain useful for benchmark calibration and for understanding prior failure modes.
Do not rewrite them to match current architecture semantics.

## Current entrypoint

Use `docs/phase1/START.md` for all current architecture-learning work.

Running, extending, or creating a new round from a legacy experiment requires an
explicit owner instruction naming that experiment. Otherwise treat all legacy
`START.md` commands as documentation of what happened, not instructions for what
to do next.
