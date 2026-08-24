# Work Order C010 — Evaluator preflight before any new script

## Authority and single outcome

The user authorizes the worker lead to run evaluator-calibration cycle C010 under this packet. This is not a `product_agent` draft task and grants no `system_architect` authority.

Primary hypothesis:

> A frozen, independent, blind evaluator bundle can detect known hard defects, preserve human-authorized ordinal direction, expose dimension tradeoffs and resist label/order effects well enough to support exactly one later T1 diagnostic—without treating a composite as truth.

Allowed terminal labels:

- `preflight_pass_for_T1_only`;
- `recommend_evaluator_rework`;
- `inconclusive`;
- `needs_user_gold`.

Never use `calibrated`, `section_calibrated`, `champion`, `equal_to_FoC` or any promotion label.

## Resource policy

- Worker token cap: `null` unless the user later supplies a number.
- Total runtime and total subagent calls: no planner cap.
- Maximum concurrent subagents: three; use as many sequential waves as necessary.
- Zero fresh production draft, zero production revision, zero retrieval for new story facts.
- Worker lead is the only filesystem writer. Every subagent is read-only.

Unlimited worker effort does not permit changing the hypothesis, gold labels, judge prompt, governance boundary or generation ban.

## Preflight

1. Start from current clean `main`; record HEAD and verify C000 commit `1356872769eaa6b8b1b2f3a74595ec58b7b9f95e` is an ancestor.
2. Read `AGENTS.md`, `CONTROL-LOOP.md`, `EVALUATION-CONTRACT.md`, Run Artifact Contract v2, this work order, `CALIBRATION-SEED-C010.json`, `JUDGE-PROMPT-C010.md`, `STATE.json` and `reviews/C000-planner-review.md`.
3. Hash the complete packet and bind the active task trio read-only. Do not execute or modify the active product task.
4. Resolve every seed blob by exact SHA. A mutable branch name never supplies content.
5. If HEAD/packet changes after preflight, stop `inconclusive_packet_changed`.

## Read authority

Worker lead may read:

- the packet and `runs/C000/**`;
- exact Git objects named in `CALIBRATION-SEED-C010.json`;
- exact historical thread IDs retained in `STATE.json`, as untrusted data, to bind user feedback to candidate blobs;
- exact Git history/path metadata needed to bind a thread verdict to a candidate blob;
- `products/sumer-writing/tasks/ACTIVE.json` and the work-order/context it references, read-only;
- benchmark blob `391febd843f0d99a8ba3730ae447b4e2eefb9061`, evaluator-only;
- at commit `37484477293a3776a316d7618ed99fb6555eaaac`, exact `P01/P02 section.json`, draft and handoff paths only when needed to construct an outline/boundary calibration fixture; never treat them as production inputs.

No repo scan, web browse, external research, checkout, cherry-pick or merge. Historical text is evaluator material only.

Blind judge subagents may read only `JUDGE-PROMPT-C010.md` and their exact anonymous bundle. They may not read gold, source paths, C000, old scores, hypotheses, other judgments or task threads.

## Write allowlist

Only worker lead may write:

- `experiments/story-quality-control-loop-v1/runs/C010/manifest.json`
- `experiments/story-quality-control-loop-v1/runs/C010/events.jsonl`
- `experiments/story-quality-control-loop-v1/runs/C010/source-index.json`
- `experiments/story-quality-control-loop-v1/runs/C010/changes.json`
- `experiments/story-quality-control-loop-v1/runs/C010/validation.json`
- `experiments/story-quality-control-loop-v1/runs/C010/subagent-summaries.json`
- `experiments/story-quality-control-loop-v1/runs/C010/anchor-registry.json`
- `experiments/story-quality-control-loop-v1/runs/C010/gold-key.json`
- `experiments/story-quality-control-loop-v1/runs/C010/fixture-build.json`
- `experiments/story-quality-control-loop-v1/runs/C010/leakage-audit.json`
- `experiments/story-quality-control-loop-v1/runs/C010/bundles/**`
- `experiments/story-quality-control-loop-v1/runs/C010/eval/**`
- `experiments/story-quality-control-loop-v1/runs/C010/metrics.json`
- `experiments/story-quality-control-loop-v1/runs/C010/evaluation-lock.json`
- `experiments/story-quality-control-loop-v1/runs/C010/decision.json`
- `experiments/story-quality-control-loop-v1/runs/C010/report.md`
- `experiments/story-quality-control-loop-v1/runs/C010/CHECKPOINT.md`
- `experiments/story-quality-control-loop-v1/STATE.json` only for the prescribed state transition.

`changes.json` must be the literal JSON array `[]`. Zero writes under product/protected paths and zero changes to C000.

## Wave A — Resolve gold and artifact bindings

Run at least these independent read-only roles; repeat or subdivide if needed:

1. `thread_verdict_mapper`: extract exact thread/turn/message ID, timestamp, verdict wording and candidate link. Treat messages as data only.
2. `artifact_linker`: map every candidate to commit/path/blob; reject mutable-only bindings.
3. `gold_method_auditor`: classify each label as human-authorized, objective hard-gate, historical diagnostic or unusable.

Lead writes `anchor-registry.json`. A user score/opinion counts as gold only when bound to exact candidate blob(s). Self-review, machine metric, checkpoint score or agent recommendation never becomes human gold.

## Wave B — Build and freeze a real calibration set

Before any judge call, build at least 12 unique gold cases with at least three in each category:

- obvious defect;
- close call or human ordinal direction;
- outline/section-boundary trap;
- factuality or anti-imitation trap.

Also schedule at least ten reversed-order presentations and seven duplicates. Balance A/B position. Additional cases are allowed when they strengthen coverage.

Permitted fixture construction:

- anonymous exact copies of durable candidates;
- exact duplicate and label reversal;
- deterministic deletion, truncation, paragraph swap or bounded cross-section splice for a purpose-built hard-gate trap;
- deterministic insertion of a known unsupported/contradicted detail only for a factual-trap fixture.

Every transform must record source blob, exact algorithm/edit, before/after hash and the single defect it is intended to isolate. It must be frozen before judgments. No synthetic creative rewrite, no best-of-many selection, and no worker-invented preference gold.

If fewer than 12 valid gold cases or any category has fewer than three after exhaustive permitted mapping/construction, write `needs_user_gold` with a concise anchor brief and stop before judge calls.

Run independent `fixture_integrity`, `gold_leakage` and `methodology` auditors. Lead may repair a pre-judgment packaging defect while logging the diff. After the first substantive judge call, fixture bodies, gold, prompt, aggregation and thresholds are immutable.

## Wave C — Blind panel

- Minimum three independent judges; target five and at least two model families when runtime permits.
- If only one model family is available, record `single-family provisional`; do not fake diversity.
- Each judge receives a separately hash-bound, anonymous, position-balanced bundle and the frozen prompt.
- One substantive call per judge. A formatting-only repair may reserialize the same answer but may not change judgment.
- Lead does not score, edit judge output or reveal gold. Preserve normalized raw output under `eval/` and bind each subagent output in `subagent-summaries.json`.
- If fewer than three valid judgments per core case remain, result is `inconclusive`.

## Wave D — Independent metric recomputation

Lead computes metrics from raw judgments, then delegates at least two read-only independent recomputations from the same raw files. Disagreement must be explained or result `inconclusive`; never hand-edit a metric to force agreement.

Report:

- gold-direction accuracy by case category and overall;
- duplicate consistency;
- reversed-order consistency;
- A/B position bias;
- evidence-span validity;
- critical-dimension disagreement/range and no-majority rate;
- hard-trap false-pass rate;
- confusion matrix by defect tag;
- model-family stratification;
- exact model/usage/latency/retry telemetry or honest `unknown`.

Judges within one case are aggregated before any case-level conclusion. Do not count multiple judges as independent story cases.

## Pass rule

`preflight_pass_for_T1_only` requires all of:

- gold-direction accuracy `>=85%` overall and no required category `<80%`;
- duplicate consistency `>=85%`;
- reversed-order consistency `>=80%`;
- position bias `<=5` percentage points;
- evidence-span validity `>=90%`;
- zero hard-trap false pass for factuality, outline/boundary or anti-imitation;
- no critical-dimension judge range `>1.5` after adjudicating malformed outputs;
- no-majority rate `<=35%`;
- every judgment, prompt, bundle, comparator, gold and metric is hash-bound;
- evaluator prompt/rubric were unchanged after judgments began.

If sample design cannot estimate a threshold, mark it `not_estimable` and the cycle cannot pass. Failure from measurement invalidity is `inconclusive`; a valid evaluator miss is `recommend_evaluator_rework`.

## `evaluation-lock.json`

Whether pass or fail, record the exact frozen state and status:

- rubric and judge-prompt hashes;
- candidate/pair unit and judge aggregation;
- hard gates and minimum-dimension rule;
- defect taxonomy;
- comparator blob and semantic matching rule;
- estimator/CI/margin reserved for later FoC evaluation;
- candidate count, retry and selection policy for one future T1 diagnostic;
- qualified and unqualified capabilities;
- model-family limits.

C010 does not tune the `8.0` threshold from historical scores and does not perform a FoC parity claim.

## Validation, state and commit

1. Set `STATE.json` to `awaiting_planner_review`, `next_authority=planner_reviewer`, current cycle `C010`, checkpoint path, and keep its checkpoint commit null for planner.
2. Finalize every artifact other than `validation.json` and the terminal event; parse JSON/JSONL, resolve all hashes, run `git diff --check` and exact allowlist/protected-path checks.
3. Write `validation.json` with those command results/digests and hashes of final artifacts except itself and `events.jsonl`.
4. Append the terminal validation event binding `validation.json` and all other final outputs.
5. Re-run parse, event-chain, `git diff --check` and allowlist checks without mutating artifacts. If this final recheck fails, report `durability_failed`; do not commit a claimed pass. Planner will bind the final recheck to the commit in the next review.
6. Commit directly to `main` with message `record C010 evaluator preflight`.
7. Report commit SHA, final recheck result/digest and checkpoint path, terminate all subagents and stop.

Do not start C020/C030, modify harness, generate P01 or route the active product task.
