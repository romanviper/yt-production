# Setup handoff — system_architect

## Authority and provenance

Owner request on 2026-09-05 authorized implementation, commit/push and a parallel
branch for the proposed evidence-led model. Implemented only on
`codex/p01-foc-evidence-loop-v1`, based on `82b94ed0a933d0ab5fc1a3680adfbf759de6e856`.
No production prose, historical authority, approvals or task state changed.
The scoped AGENTS exception makes the experimental entrypoint explicit rather
than pretending it is a canonical production task. No new agent was dispatched.

## Delivered

- Three exact repository FoC transcript references with locked source/excerpt hashes.
- Frozen baseline extent, single hypothesis and six evidence-bearing craft dimensions.
- Separate Writer, Truth and two counterbalanced Product packets, no answer labels.
- Fail-closed input/packet/candidate identity checks and exact-quote/sentence coverage checks.
- Conservative provisional-only decision, explicit process limitations and audio/human gates.
- Round-1-only run guard, refusal to overwrite/re-randomize, and no automatic next round.

## Validation

Run `python -m unittest discover -s tests -p test_p01_foc_loop.py -v`:
29 tests passed, including temporary-directory end-to-end synthetic workflows,
input/packet/candidate tampering, missing execution evidence, false quotations,
truth omissions, order sensitivity, ties, regressions and duplicate runs.
Synthetic outputs are test fixtures, not evaluations of the actual probe.
`python scripts/experiments/p01_foc_loop.py check` returned
`READY_FOR_ROUND_1_PREPARATION`. `git diff --check` passed.
Existing production tests were not run: implementation is isolated and does not
change production runtime modules. The new tests are self-authored software tests,
NOT evidence that an AI reviewer can judge podcast quality reliably.

## Remaining limits and next action

The actual Writer and reviewers have not run. Start at `START.md` and generate
the round-01 packet. The launcher is operator-driven; this is not a background
agent scheduler. The harness cannot verify semantic entailment, authenticate
platform exports or enforce another application's context isolation. Commander
must check actual execution evidence, not self-attestations; unsupported runtime
isolation means `INCONCLUSIVE_PROCESS`. No permanent evaluator certification.
FoC audio alignment and target-listener testing remain explicit future gates;
readiness means ready for a bounded script experiment, not podcast release.
