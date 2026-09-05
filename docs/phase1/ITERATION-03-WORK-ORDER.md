# Phase 1 Improvement Iteration 03 — Work Order

Status: **READY / PACKAGING ONLY**

## Triggering output defect

Iteration 02 output has a calibration protocol and unlabeled source pairs, but no reviewer-facing/owner-facing pair packets exist. Phase 1 therefore cannot collect preference without reconstructing inputs ad hoc, which would weaken reproducibility and risk label leakage.

## Objective

Materialize the smallest owner-calibration input set without changing the measurement contract.

## Required outputs

Create three owner-facing pair packets under:

`benchmarks/p01/calibration/owner-packets/`

Each packet must contain only:

- opaque packet/pair ID;
- Product scenario in neutral language;
- Sample A prose;
- Sample B prose;
- allowed result `A | B | TIE | UNCERTAIN`;
- optional prompts for brief product feedback.

Packets MUST NOT contain:

- source paths;
- internal sample IDs (`P01-C...`);
- historical labels or prior verdicts;
- candidate/baseline/new/old wording;
- FoC excerpts or target-gap commentary;
- Worker/Writer/Planner process;
- expected winner.

A separate internal dispatch map may bind packet positions back to calibration sample IDs. It is not reviewer input.

## Owner feedback prompt

Keep owner feedback lightweight. Ask for overall preference first. Optional feedback may capture:

- where attention drops;
- what changed in understanding;
- what remained memorable;
- why the preferred version works better;
- whether the difference is subtle or obvious.

Do not require the owner to score every criterion unless useful.

## Mechanical controls

Prepare judge-order metadata for later A/B reversal, but do not run judges or fabricate owner labels in this iteration.

The same-text control remains a judge reliability control and need not be presented to the owner as a genuine preference question.

## Worker log

Publish `benchmarks/p01/iterations/iteration-03.json` with separate `process` and `output` surfaces.

Stop at `READY_FOR_HUMAN_CALIBRATION` only if the packet packaging is inspectably clean. Structural verifier execution remains a separate reported status; do not claim it ran if it did not.
