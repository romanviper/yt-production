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
2. Writer receives one primary objective—to tell a compelling historical story that earns continued voluntary attention—plus the section mission, length forecast, continuity input and a bounded evidence interface. The audience should discover the mission's meaning through what unfolds rather than hear a thesis proved. Writer uses `search`/`source` to discover the story material available inside the truth ceiling, then chooses or refines the route. Material questions never become required beats. The broker never asks for, records or validates a creative route. Writer writes the declared outputs, runs packet validations and submits.
3. Run a clean `draft_cold_read` with the anonymous target viewer. Stop before formal review when continuation is `no` or `uncertain`, the curiosity chain has a material break, spoken naturalness fails, trust weakens, or material resistance remains. Do not auto-loop a writer from this result.
4. Route `review_section` to a fresh reviewer only after the cold read passes. Reviewer calls `resolve_claims`, emits the production-gate block and submits; it receives neither the named source profile nor viewer reasoning.
5. If every hard gate passes and every evidence-adjusted dimension is at least 8, stop at human approval.
6. If the verdict is `changes_requested`, route the smallest approved change through one `revise_section` task, then run one fresh cold read and one fresh review. A second revision is a blocker or a new user-authorized production cycle.

At revision routing, packet schema v5 captures one immutable draft-to-revision receipt anchor. A revision with no new trace inherits valid draft receipts through that anchor; a revision with new receipts contributes a deterministic union with origin IDs preserved. The review never recurses or searches task history. Missing or changed anchors, traces, packets, hashes, section/cycle bindings, UTC timestamps or predecessor input hashes are hard stops. Frozen v4 lineage is not inferred and is surfaced as `legacy_unverifiable`.

## Feedback interpretation boundary

Before routing draft rework, separate four things:

1. **Observation** — what failed in the existing audience experience.
2. **Desired outcome** — what the audience should instead be able to understand, feel or retell.
3. **Repair hypothesis** — a possible method such as adding a character, staging a handoff or moving from micro to macro.
4. **Explicit owner directive** — a method the user deliberately requires for this task.

Only observation and desired outcome enter a normal Writer packet. A repair hypothesis never becomes a requirement through repetition, specificity, evaluator confidence or operator paraphrase. An explicit owner directive may enter only through `--lock-method`; it is labeled `owner_locked_for_single_task`, expires with that task and cannot be promoted into the reusable harness. Keep the raw request in the audit log so no information is lost outside Writer context.

Feedback such as “too abstract,” “lecture-like,” “not visual” or “lacks a point of view” describes a failed listening result until the owner explicitly locks a method. Translate it into the audience state that failed—continued attention, orientation or a graspable historical reality—and keep proposed visual grammar outside the Writer packet.

## Cost and stop policy

The default budget is one draft, one review and at most one revision plus its review. Do not generate parallel drafts by default. Attest the scope once, then retrieve only enough evidence to find and support the story being authored. Stop immediately for stale packets, evidence outside the truth ceiling, outline/boundary defects, unsupported historical claims or changed paths outside the packet allowlist.

For each task, retain task/packet hashes, evidence trace, model family when known, input/output usage when available, validation result and stop reason. Record `unknown` rather than inventing telemetry.

## Promotion labels

A passing P01 is `section_calibrated` only after independent evidence, boundary and blind benchmark checks. P01 alone does not prove a reusable harness. Promote the harness only after fresh holdout runs across multiple section types and products at the same model/budget tier, reporting median quality, lower-tail quality, hard-gate failure rate and tokens per passing script.

## Non-canonical excerpt calibration

Use `scripts/excerpt_packet.py` when the requested sample is only a slice of a section. The operator must provide an excerpt position, a local narrative job, a local completion rule and one to three in-scope claims. The compiler exposes neither the full section exit state nor unselected claims and labels the run `canonical_output: false`. A 300–400 word probe from a 1,400-word section must stop at its local boundary; it must not answer or summarize the whole section. Probe prose never enters product files or the section lifecycle.
