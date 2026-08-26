# Section Production Harness

Use this workflow for a new section draft or a bounded section rework. Product agents still execute only router-generated packets; this file guides the operator and never enters the writer packet.

## Roles and isolation

1. **Operator** starts from current `main`, records the base SHA, routes tasks and runs validations. The operator does not approve a section.
2. **Writer** receives only the active draft packet and bounded evidence broker. It cannot read prior drafts, reviewer scoring, competitor prose or the repository at large.
3. **Anonymous target viewer** is a fresh, tool-free evaluation agent run under `system/workflows/target-viewer-protocol.md`. It receives only the anonymous runtime projection and sequential narration chunks. It evaluates but never rewrites, formally reviews evidence or approves a section.
4. **Reviewer** is a fresh agent. It receives the review packet, the compact current/next-section boundary projection, a bounded receipt projection with an explicit `projected`, `none` or `legacy_unverifiable` state, and bounded evidence access. The projection names the current prose task and every receipt origin. It evaluates but never rewrites. Receipts save duplicate source opening but neither widen the narration truth ceiling nor prove that revised prose used a recorded detail correctly.
5. **Reviser** is a fresh agent used only after a diagnosed `changes_requested` result. It sees the routed change request, current prose, compact mission/boundary control and narration truth ceiling, then performs one bounded pass.
6. **User** is the only section approval authority.

Never let one agent write, score and explain its own improvement. FoC or another benchmark belongs only in a separate blind calibration panel, never in writer, reviewer or reviser context.
Never pass the named audience source profile, target-viewer trace or target-viewer reasoning into writer, reviewer or reviser packets.

## Canonical sequence

1. Route `draft_section` with `scripts/task.py create`, or use `scripts/rework.py` for a requested rerun.
2. Writer resolves the bounded truth scope once through `resolve_claims` and receives a compact writer brief. The full ledger remains behind the evidence broker for audit and optional lookup. Before prose, the writer privately chooses a carrier, pressure and change; that choice is neither returned nor audited. The writer develops one situation across the section and distributes evidence only where it changes that situation, rather than compressing the brief into an explanatory inventory. The evidence broker never asks for, records or validates a creative route. Writer retrieves only details that materially improve the telling, writes the declared outputs, runs packet validations and submits.
3. Run a clean `draft_cold_read` with the anonymous target viewer. Stop before formal review when continuation is `no` or `uncertain`, the curiosity chain has a material break, spoken naturalness fails, trust weakens, or material resistance remains. Do not auto-loop a writer from this result.
4. Route `review_section` to a fresh reviewer only after the cold read passes. Reviewer calls `resolve_claims`, emits the production-gate block and submits; it receives neither the named source profile nor viewer reasoning.
5. If every hard gate passes and every evidence-adjusted dimension is at least 8, stop at human approval.
6. If the verdict is `changes_requested`, route the smallest approved change through one `revise_section` task, then run one fresh cold read and one fresh review. A second revision is a blocker or a new user-authorized production cycle.

At revision routing, packet schema v5 captures one immutable draft-to-revision receipt anchor. A revision with no new trace inherits valid draft receipts through that anchor; a revision with new receipts contributes a deterministic union with origin IDs preserved. The review never recurses or searches task history. Missing or changed anchors, traces, packets, hashes, section/cycle bindings, UTC timestamps or predecessor input hashes are hard stops. Frozen v4 lineage is not inferred and is surfaced as `legacy_unverifiable`.

## Cost and stop policy

The default budget is one draft, one review and at most one revision plus its review. Do not generate parallel drafts by default. Resolve once for the compact brief, then open only evidence that can materially improve the telling. Stop immediately for stale packets, evidence outside the truth ceiling, outline/boundary defects, unsupported human detail or changed paths outside the packet allowlist.

For each task, retain task/packet hashes, evidence trace, model family when known, input/output usage when available, validation result and stop reason. Record `unknown` rather than inventing telemetry.

## Promotion labels

A passing P01 is `section_calibrated` only after independent evidence, boundary and blind benchmark checks. P01 alone does not prove a reusable harness. Promote the harness only after fresh holdout runs across multiple section types and products at the same model/budget tier, reporting median quality, lower-tail quality, hard-gate failure rate and tokens per passing script.

## Non-canonical excerpt calibration

Use `scripts/excerpt_packet.py` when the requested sample is only a slice of a section. The operator must provide an excerpt position, a local narrative job, a local completion rule and one to three in-scope claims. The compiler exposes neither the full section exit state nor unselected claims and labels the run `canonical_output: false`. A 300–400 word probe from a 1,400-word section must stop at its local boundary; it must not answer or summarize the whole section. Probe prose never enters product files or the section lifecycle.
