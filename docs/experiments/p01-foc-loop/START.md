# P01: evidence-led FoC comparison loop

> **LEGACY / EVIDENCE ONLY.** This experiment is closed. Do not start, extend,
> rerun, or treat the commands below as the current repository workflow. Preserve
> its artifacts as historical evidence for Phase 1 benchmark calibration. Current
> architecture work starts at `docs/phase1/START.md`.

Owner-authorized system experiment, 2026-09-05. Source: `82b94ed`.
Branch: `codex/p01-foc-evidence-loop-v1`. Production and historical probes are read-only.

## Start round 1

From the repository root, using Python 3.10+ (standard library only):

On this Windows host, if `python` is not on PATH, invoke the bundled executable
with PowerShell's `&` operator:
`C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.
The commands below use `python` as shorthand; no package installation is needed.

```text
python scripts/experiments/p01_foc_loop.py check
python scripts/experiments/p01_foc_loop.py writer --run round-01
```

The first command must return `READY_FOR_ROUND_1_PREPARATION`. This means frozen
inputs and runnable packet tooling exist, NOT reviewer certification or a good
podcast. The second writes `experiments/p01-foc-loop/runs/round-01/writer-packet.json`.
Give only that packet to a fresh Writer context. Do not fork this conversation
or the previous reviewing/planning contexts. Writer returns prose only; save it
as `candidate.md` in that run directory. Do not edit the old probe.

Then:

```text
python scripts/experiments/p01_foc_loop.py prepare --run round-01
```

Dispatch `truth-packet.json`, `product-1-packet.json`, `product-2-packet.json`
to three separate fresh input-only contexts with repository, shell, web,
conversation history and sibling outputs unavailable. The two Product packets
present the same texts in reversed order; this is a position-sensitivity check,
not four independent votes. Do not send dispatch.json, writer-packet.json,
baseline identity, old verdicts or this commander's history to reviewers.

Save unedited tool/platform request and response exports with timestamps in the
run directory, then the returned JSON as `truth.json`, `product-1.json`,
`product-2.json`. Complete `execution.json` using its generated template; record
actual model/config and exported execution evidence, never invented IDs/logs.
Use timezone-aware ISO timestamps. Commander must verify that each export
contains the exact dispatched packet, actual returned review and tool/input
restrictions, not just an agent's statement of compliance. Its semantic audit
must enumerate uncovered factual clauses, wrong-record bindings, unwarranted
qualifications, reviewer-added bridges and remaining FoC gaps, with specific
locations. The presence/hash of a file alone cannot verify those assertions.
If input-only contexts are unavailable, exploratory reviews are allowed but
the decision is `INCONCLUSIVE_PROCESS`; no blind/independent claim is permitted.

```text
python scripts/experiments/p01_foc_loop.py decide --run round-01
```

Only `PROVISIONAL_SCRIPT_IMPROVEMENT` permits retaining the candidate for a
listening trial. It does not authorize publication, production submission,
audio-quality certification, or a new round automatically. No score overrides
an unresolved truth defect. A tie or reviewer disagreement is not improvement.

## Commander contract

Read `protocol.md`, `round-01.json`, and the generated packets, not historical
calibration verdicts. The old `DUAL_PASS_CERTIFIED` and leaked calibration tests
are superseded as authority for this route, preserved as historical artifacts.
Do not change frozen files mid-run. A changed hypothesis/criterion requires a
new version, an explicit change reason and renewed preflight; old runs remain.

One round = one candidate + one truth review + two independent product reviews
with reversed order. No best-of-many rerolls or extra tie-breaking votes until
a preferred verdict appears. Repeat after a technical failure only with both
attempts retained and the failure documented. After two consecutive rounds
without demonstrated improvement, stop the tactic and diagnose material,
hypothesis or evaluator failure. Do not escalate merely for internal mechanics.

Commit run evidence after all reviews close; private dispatch maps only after
review closure. Gitignore is convenience, NOT security. If tools cannot enforce
input restriction, report that limitation; do not count agent promises as proof.
Share a short owner brief: sample, old/new difference, remaining FoC gap,
truth limitations and listening status. Ask for broader historical research
only if needed, and ask for product feedback on a meaningful sample.

## Listening checkpoint (not completed by setup)

Script-level assessment has limits: current references are repository
transcripts, not audio-verified transcripts. Before claiming podcast quality,
verify excerpt timestamps/text against original FoC audio and archive locators.
Compare old/new in the same voice, speed, loudness and production treatment;
record actual durations, don't equate English words with Vietnamese syllables.
Use function-matched FoC audio as an external reference while noting production
and language confounds. Collect target-listener reactions without version
labels: where attention drops, what was understood/recalled, why continue.
Save responses including negative/ambiguous ones. Owner feedback remains a
product gate, not a substitute for technical gatekeeping.
