# P01 Narrative Rework — Execution Handoff

Status: `planned_not_started`

Plan recorded from canonical `main` at `7bba4c4` on 2026-08-25.

Owner authority: the user reviewed P01, rejected its narrative naturalness, and requested this committed plan so a later session can execute it directly. This document authorizes planning continuity; it does not replace the normal system/product write scopes or human approval gates in `AGENTS.md`.

## Start here in the next session

1. Start from current `main`; do not create or merge an auxiliary branch.
2. Read `AGENTS.md`, this file and `products/sumer-writing/03_sections/P01/human-feedback.md`.
3. Confirm the observed state below still matches HEAD. If it has changed, reconcile the difference before executing.
4. Implement the system calibration first and commit it separately. Only then route the fresh P01 draft.

Do not repeat the broad diagnosis unless the repository state has materially changed. The failure and execution decision are already settled below.

## Observed state at planning time

- `products/sumer-writing/tasks/ACTIVE.json`: idle; no active task.
- `products/sumer-writing/03_sections/P01/section.json`: `status = review_complete`, `human_approved = false`.
- `products/sumer-writing/03_sections/P01/review.md`: machine verdict `pass`; `hook_and_audience_promise = 9`.
- `products/sumer-writing/03_sections/P01/human-feedback.md`: `human_rejected_for_rework` because the prose feels mechanical, unnatural and visibly designed.
- The state therefore contains a deliberate human-over-machine override that has not yet been routed into a fresh task.

The evidence ceiling, P01 mission and P01→P02 boundary were not rejected. The failed layer is audience experience, plus an evaluator false positive that rewarded visible hook mechanics instead of actual desire to continue.

## Locked decisions

- Rewrite P01 as a fresh `draft_section` pass; do not locally patch the current opening and do not begin with `revise_section`.
- Preserve the approved mission, evidence ceiling, section boundary and historical qualifications.
- Do not expose the fresh writer to the old draft, old review, numeric scores, human quotes about `bulla`, competitor prose or FoC.
- Do not create lexical bans, mandatory opening devices, beat quotas or a replacement hook formula.
- Treat naturalness, visible technique and desire to continue as evaluator-side audience outcomes, not writer-side checklist items.
- A machine pass only means eligible for human review. It never overrides a human rejection and never approves a section.
- Keep FoC in a separate, blind calibration panel. It must never enter writer or reviser context.
- Do not run five recursive self-revision rounds. Use one fresh draft, an early cold-read stop, one formal review and at most one bounded revision for a localized issue.

## Execution phases

| Phase | Owner | Output | Mandatory stop |
|---|---|---|---|
| 1. System calibration | `system_architect` | Quality-gate contract, harness guidance and tests | Stop if the change relies on surface wording rules or mixes product content into the commit |
| 2. Independent QA/calibration | fresh calibration agent | Contract audit plus blind negative/control results | Stop if current failed P01 can still receive an audience-experience pass |
| 3. Fresh P01 authorship | fresh `product_agent` writer | One complete P01 draft and normal task handoff | Stop for stale packet, prior-draft leakage, evidence expansion or boundary conflict |
| 4. Audience and formal review | cold reader, then fresh formal reviewer | Audience diagnosis followed by evidence/mission/boundary verdict | Stop before formal review if cold reader does not want to continue |
| 5. Human gate and holdout | user, then later P02 team | Human-approved P01; P02 holdout evidence | Do not promote the harness from P01 alone |

### Phase 1 — repair the evaluator before generating prose

Run this as an explicit `system_architect` task. It may touch protected system paths but must not edit P01 prose or product state in the same commit.

Required behavior:

1. Version the section quality-gate contract if its machine-readable shape changes.
2. Add one evaluation-only `audience_experience` gate, preferably as a small sidecar or blind-reader result rather than a new production operation unless the existing architecture cannot express it safely.
3. The blind reader receives narration only. It must not receive mission compliance notes, evidence receipts, prior scores, human feedback wording or benchmark identity.
4. Record qualitative outcomes sufficient to answer:
   - Does the listener want to continue after the opening?
   - Where is the first point of resistance or disengagement?
   - Does attention move from the history to the writer's visible technique?
   - Does the prose sound natural when read aloud?
5. A material failure in audience experience must derive `changes_requested` even when evidence, progression and retellability pass.
6. A negative continuation judgment must not coexist with a passing audience gate or an unqualified high hook score.
7. Re-anchor `hook_and_audience_promise` to experienced pull, not the presence of object, contrast, paradox, question or thesis components.
8. Preserve the existing evidence, mission, boundary and one-hearing checks. Do not weaken truth controls to improve style.
9. Operator-facing output must display human approval status separately and above machine scores.

Regression and calibration requirements:

- Contract tests: a missing or internally contradictory audience result is invalid.
- Routing tests: audience failure yields `changes_requested`; machine pass cannot set human approval.
- Packet-isolation tests: a fresh draft packet excludes prior draft, review, production-gate scores, human feedback and competitor prose.
- Negative calibration: the P01 at commit `7bba4c4` must be diagnosed as a material audience-experience failure. Reference the historical artifact or use the smallest justified fixture; do not duplicate the full draft casually.
- Control calibration: include contrasting samples so an object opening, paradox or technical noun is not rejected merely for existing.
- Blind FoC comparison may measure preference, naturalness and continuation pressure, but all samples must be de-identified and remain outside production packets.

Likely canonical files to inspect, not an automatic write allowlist:

- `system/standards/section-quality-gate.md`
- `system/workflows/section-production-harness.md`
- the existing review contract/compiler under `scripts/`
- the corresponding contract, packet-isolation and lifecycle tests under `tests/`

Commit the complete system change alone after full validation. Suggested message: `calibrate section review for audience experience`.

### Phase 2 — verify the system change independently

Use a fresh agent that did not author the patch.

It should verify:

- no lexical or device blacklist was introduced;
- the failed P01 no longer false-passes;
- positive/control prose is not rejected just for using an object or paradox;
- audience failure deterministically blocks the overall pass;
- writer packets remain isolated;
- human authority and existing evidence lineage remain intact;
- the full test suite and `scripts/validate.py products/sumer-writing` pass.

Do not proceed to product generation with an unresolved P1/P2 system defect.

### Phase 3 — route one fresh P01 draft

After the system commit is clean, use the canonical semantic rework entrypoint:

```text
python scripts/rework.py products/sumer-writing draft_section --section P01 --request "Write P01 again as a fresh narration from the approved mission and evidence ceiling. Let curiosity and stakes emerge from the historical situation, with a natural spoken voice and no obligation to preserve any prior narrative device or wording."
```

This route should move P01 to the canonical fresh-draft state, clear any approval, record the user rework request and create the new task. Do not call `approval.py request-changes` as the primary route because that prepares a bounded revision of the old draft.

Before launching the writer, inspect only the router-generated packet and assert that it contains:

- the unchanged P01 mission and exit state;
- the unchanged evidence ceiling and narration pack;
- the P01→P02 boundary;
- the outcome-level rework request.

It must not contain:

- current or historical `draft.md` prose;
- `review.md`, machine scores or reviewer reasoning;
- `human-feedback.md` quotes or surface symptoms;
- FoC or other competitor prose;
- a prescribed opening object, hook sequence or beat template.

Launch one fresh writer. The writer retrieves at whole-claim scope once, opens only material sources and produces one complete P01 within the existing length cap. The writer must not score its own output or run recursive self-revision.

Commit product task output separately from the system commit, after packet validations and task submission succeed.

### Phase 4 — run the cheap audience stop before formal review

1. Give a fresh cold reader only the narration, with no mission/evidence/score context.
2. Ask for the structured audience-experience result defined in Phase 1.
3. If continuation is negative, technique is materially visible or spoken naturalness fails, stop. Do not spend a formal review and do not auto-loop another writer.
4. If the cold read passes, route the canonical `review_section` task to a fresh formal reviewer.
5. The formal reviewer checks evidence integrity, mission/exit, historical progression, adjacent boundary and the combined audience result. It evaluates only and never rewrites.
6. A localized evidence, clarity or transition issue may receive one bounded `revise_section` pass followed by one fresh review.
7. A second broad naturalness/voice failure is a blocker requiring a new user decision, not a sentence-level patch cycle.

### Phase 5 — human approval and reusable-harness proof

P01 is complete only when all of the following hold:

- the user wants to continue after the opening;
- the prose sounds natural when read aloud;
- narrative technique is not the foregrounded experience;
- curiosity and stakes arise from the historical material;
- evidence integrity, mission, exit state and P02 boundary pass;
- no benchmark language or structure has leaked into the draft;
- the user explicitly approves the section.

After P01 approval, run P02 as a holdout without tuning the rubric to P01. Record model tier when known, input/output usage when available, retrieval count, revisions, hard-gate failures and tokens per human-approved section. Do not label the harness reusable until it passes P02 and at least one materially different section or product type with acceptable lower-tail quality.

## Agent team for the execution session

Use agents sequentially where isolation matters; do not spend tokens on parallel draft generation.

1. **Root/operator:** routes tasks, enforces scopes, runs validation and commits directly to `main`; never grants creative approval.
2. **System architect:** owns Phase 1 system changes only.
3. **Calibration/QA agent:** independently audits Phase 1 and runs blind negative/control checks.
4. **Writer:** fresh context; receives only the canonical P01 draft packet.
5. **Cold reader:** fresh context; narration only; exits after the audience result.
6. **Formal reviewer:** fresh context; receives the canonical review packet and permitted audience result; never rewrites.
7. **User:** sole final approval authority.

With four concurrency slots, finish and release the architect/QA slots before spawning writer/review roles. Parallelism is useful for independent tests, not for multiple creative candidates.

## Cost and stop budget

Default production budget after the system fix:

- one system implementation plus one independent QA pass;
- one fresh P01 draft;
- one short cold read;
- one formal review only after the cold read passes;
- at most one localized revision and one re-review;
- zero parallel drafts and zero five-round self-improvement loops.

Stop immediately for packet leakage, stale provenance, evidence outside the ceiling, changed mission/boundary, audience failure, a second broad creative failure or any missing human authority.

## Validation and commit discipline

At each implementation commit:

```text
python -m unittest discover -s tests
python scripts/validate.py products/sumer-writing
git diff --check
git status --short --branch
```

- Keep system architecture and product content in separate commits.
- Work directly on canonical `main` under the repo rules.
- Push only after the relevant test suite, product validation and worktree review pass.
- Preserve human feedback and provenance; never rewrite history to conceal the rejected draft.

## Completion report expected from the execution session

Report:

- system commit and product commits;
- exact tests and validation results;
- audience-experience result, formal verdict and human verdict;
- token/retrieval/revision telemetry, using `unknown` when unavailable;
- whether P01 is approved;
- whether the harness is merely P01-calibrated or has also passed the P02/cross-type holdout.

