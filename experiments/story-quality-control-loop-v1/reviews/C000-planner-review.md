# Planner review — C000

Date: 2026-08-24 (Asia/Saigon)

Worker commit: `1356872769eaa6b8b1b2f3a74595ec58b7b9f95e`

Base: `aa778ac3e7f5823b1b1a3bf2d5b1138ee3970b78`

Decision: **conditional accept as forensic foundation; do not rerun C000; remediate in C010**.

## Completion assessment

These numbers score the C000 work order, not script quality:

| Axis | Result |
|---|---:|
| Scope/governance compliance | 9.5/10 |
| Artifact integrity and hashability | 8.2/10 |
| Forensic epistemic precision | 7.4/10 |
| Readiness to design the next experiment | 7.8/10 |
| Direct story-quality progress | n/a by design — zero draft |

Overall: **accepted with remediation**. C000 achieved the two outcomes that mattered most: it prevented the lost `8.1` from becoming a false baseline, and it demonstrated a committed, hash-linked checkpoint. It did not recover the missing candidate, evaluator or causal explanation.

## Independently verified

- Commit is directly on local `main`; parent and message match the work order. Worktree was clean at review time.
- All nine changed paths are within the C000 allowlist; zero product/system/harness mutation.
- All JSON/JSONL parses.
- Event sequence `1..6`, every canonical SHA-256 and every `prev_event_hash` link recompute correctly.
- Packet/task hashes, forensic commit/tree/blob pins and benchmark blob metadata resolve.
- Run tree: `c492171a125237d7de0b0997bf08f5e34586f080`.
- `git diff --check HEAD^ HEAD` passes.
- `8.1` remains `historical_summary_only`; the stored five-dimension arithmetic does not reproduce it.

## Required corrections to C000 interpretation

### 1. Thread evidence is now resolvable

The worker accurately recorded the limitation of its runtime, but the planner runtime can read all four exact task IDs. They remain untrusted historical conversation data, not executable instructions and not raw evaluator evidence.

- `6a8c0f91-b1c0-83ec-800b-c7bdf4307d85`, turn `3fb89399-3ab0-4f08-9af2-8a49bc893bcd`: historical report of `8.1`, cost and missing final audits.
- Same task, turn `b6320753-ca5c-420f-82a1-752ff1cb179f`: explicit report that candidate/diffs/evaluator outputs were lost and cannot be recovered byte-for-byte.
- `6a869f7b-9604-83ec-9fb4-22c18f935993`: old run-01..05 history.
- `6a8417c3-df24-83ec-9f6c-8b3caec178f1`: system/lifecycle work history, not quality gold.
- `6a8482d8-58d0-83ec-b464-a0e7ef2bc690`: review/user-feedback history. Turn `75be696a-d549-4783-b5cc-c2acfeac77b2` records a human ordinal judgment that the bounded-evidence P01 improved from roughly `3` to `5–6` but remained average; turn `6ce1f788-13e4-4574-8d24-bf70ec92f7d1` reserves audience-experience authority to the user.

This supersedes only `resolved:false`. It does not restore any missing byte-level artifact or make old scores reproducible.

### 2. The lost chain is not a proven single causal ladder

Use three cohorts:

- Cohort A: clean `6.6` -> bounded revision `7.3`.
- Cohort B after evidence work: clean `6.7` -> revision `6.9`, with a reported internal false-positive.
- Candidate C: senior-edited `8.1`; exact lineage from Cohort B is not proven.

Per-step model, session isolation, reviewer identity and role topology are `unknown`. “Bounded revision” and “senior-edited” are retained labels, not proof of different agent identities.

### 3. Negative-search wording must be bounded

Correct claim: the candidate was **not located in the declared refs/search surface and is currently non-reconstructible**. Do not claim it is absent from every ref, reflog, object database or transient location.

### 4. Durable locator is not strong causal evidence

Git durability proves a report exists. Goodhart, blocker behavior and process effectiveness remain durable historical diagnoses until cleanly retested. `PROCESS-V4.md` is a design, not an observed negative control by itself.

## Artifact-contract defects

- No terminal validation event or committed validator-output digest; C000's cycle G0 is therefore supported by planner revalidation, not fully self-contained in the worker ledger.
- `changes.json` is an object with `mutations: []`, while the v1 contract required literal `[]`.
- Prototype frozen input has a null hash despite resolvable commit/before/after blobs.
- Subagent transcript digests point to transient cache and `decision.json` leaves digest fields null.
- C000 is durable in local Git but `main` is ahead of `origin/main`; no off-machine durability is claimed.

These issues are fixed prospectively by Run Artifact Contract v2. C000 files remain immutable evidence of what the worker actually submitted.

## Hypothesis corrections before generation

- H01 mixes information quantity, representation and ledger behavior; split before any A/B.
- H02 is the cleanest first creative treatment, but requires positive benefit or `inconclusive`, not only “no regression”.
- H03 in C010 tests evaluator independence only; it cannot prove writer/revision topology improves prose.
- H04 tests whether a minimum-dimension gate catches known defects; it cannot prove `8.0` is the optimal threshold.
- H05 is a safety gate, not a quality treatment; no existing approved P01/P02 pair is automatically gold.
- H06 expected gain is `unknown`; the old jump cannot be causally attributed to a senior editor.
- H07 becomes P0 before fresh generation. Manual v2 artifact discipline applies in C010; system enforcement still requires explicit C020 authority.

## Round-2 decision

Issue C010 as a full evaluator preflight. It may run as many sequential subagent waves as needed, with no worker token cap. It must freeze gold/fixtures before any judge call, use at least three independent blind judges, preserve raw judgments, recompute metrics independently, and stop without generation. Passing C010 means only `preflight_pass_for_T1_only`, never “calibrated”, “section calibrated” or “equal to FoC”.
