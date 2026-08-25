# Section Production Harness

Use this workflow for a new section draft or a bounded section rework. Product agents still execute only router-generated packets; this file guides the operator and never enters the writer packet.

## Roles and isolation

1. **Operator** starts from current `main`, records the base SHA, routes tasks and runs validations. The operator does not approve a section.
2. **Writer** receives only the active draft packet and bounded evidence broker. It cannot read prior drafts, reviewer scoring, competitor prose or the repository at large.
3. **Reviewer** is a fresh agent. It receives the review packet, the compact current/next-section boundary projection, a bounded receipt projection with an explicit `projected`, `none` or `legacy_unverifiable` state, and bounded evidence access. The projection names the current prose task and every receipt origin. It evaluates but never rewrites. Receipts save duplicate source opening but neither widen the narration truth ceiling nor prove that revised prose used a recorded detail correctly.
4. **Reviser** is a fresh agent used only after a diagnosed `changes_requested` result. It sees the routed change request, current prose, compact mission/boundary control and narration truth ceiling, then performs one bounded pass.
5. **User** is the only section approval authority.

Never let one agent write, score and explain its own improvement. FoC or another benchmark belongs only in a separate blind calibration panel, never in writer, reviewer or reviser context.

## Canonical sequence

1. Route `draft_section` with `scripts/task.py create`, or use `scripts/rework.py` for a requested rerun.
2. Writer privately commits one short structured `story_route` from the mission and state change before opening claim prose: one materially observable carrier, observable entry/exit states, and 3–6 ordered transformations pairing an `observable_change` with its `question_or_consequence`. Transformations are changes in world, material or action—not topics, claims, themes, explanations or caveat order. The writer passes that object to `resolve_claims`; the broker attests its canonical hash and returns the unordered constraint/support ledger in one atomic call. Claim/search access stays closed until that call succeeds. Claims only constrain, support or correct the route. Writer retrieves only useful source detail, writes the declared outputs, runs packet validations and submits. The route is audit-traced private scratch: do not add an artifact, approval gate or extra agent for it.
3. Route `review_section` to a fresh reviewer. Reviewer calls `resolve_claims`, emits the production-gate block and submits.
4. If every hard gate passes and every evidence-adjusted dimension is at least 8, stop at human approval.
5. If the verdict is `changes_requested`, route the smallest approved change through one `revise_section` task, then run one fresh review. A second revision is a blocker or a new user-authorized production cycle.

At revision routing, packet schema v5 captures one immutable draft-to-revision receipt anchor. A revision with no new trace inherits valid draft receipts through that anchor; a revision with new receipts contributes a deterministic union with origin IDs preserved. The review never recurses or searches task history. Missing or changed anchors, traces, packets, hashes, section/cycle bindings, UTC timestamps or predecessor input hashes are hard stops. Frozen v4 lineage is not inferred and is surfaced as `legacy_unverifiable`.

## Cost and stop policy

The default budget is one draft, one review and at most one revision plus its review. Do not generate parallel drafts by default. Retrieve once at whole-claim scope, then open only sources that can materially improve the telling. Stop immediately for stale packets, evidence outside the truth ceiling, outline/boundary defects, unsupported human detail or changed paths outside the packet allowlist.

For each task, retain task/packet hashes, evidence trace, model family when known, input/output usage when available, validation result and stop reason. Record `unknown` rather than inventing telemetry.

## Promotion labels

A passing P01 is `section_calibrated` only after independent evidence, boundary and blind benchmark checks. P01 alone does not prove a reusable harness. Promote the harness only after fresh holdout runs across multiple section types and products at the same model/budget tier, reporting median quality, lower-tail quality, hard-gate failure rate and tokens per passing script.
