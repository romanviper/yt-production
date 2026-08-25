# Target Viewer Protocol

Operator-only experimental and evaluation protocol. It does not enter product-agent packets and does not create creative authority.

## Identity separation

`system/audiences/foc-public-v1.md` is a named public-source calibration record for the operator only. It must never be passed to a target viewer, writer, reviewer or reviser.

`system/audiences/longform-history-runtime-v1.md` is the exact anonymous projection passed to the target viewer. Do not add channel identity, platform identity, metrics, named examples, comparison prose, production goals or user feedback. Behavior and listening needs may cross this boundary; source identity and style features may not.

## Clean runtime

Start a fresh fork with no inherited conversation. Give it no filesystem, repository, web, shell, evidence-broker or search tools. The viewer receives only:

1. the exact anonymous runtime projection;
2. the mode name;
3. one ordered narration stimulus chunk;
4. an explicit completion signal only after the final chunk.

Send exactly one new chunk per turn. Do not reveal later chunks, operator hypotheses, expected questions, prior draft scores, mission notes, sources, outline, claims, benchmark material or human feedback. Preserve each raw JSON response without editing it.

## Mode: `route_probe`

This is an experimental material-curiosity probe, not a production operation.

1. The operator selects one short, evidence-bounded stimulus containing only observable material that the current truth ceiling permits.
2. The viewer returns the per-chunk contract, especially one `strongest_next_question`.
3. The operator selects the next evidence-bounded stimulus in response to that question.
4. The next stimulus must partially pay the prior question with observable material, or plainly disclose that the evidence cannot answer it, and then open a natural next question through change or consequence.
5. Continue only while the trace yields useful diagnostic information; stop instead of padding a dead chain.

The trace never enters a writer packet, is never copied into a rework request and does not replace or pre-author the writer-private `story_route`. It may tell the operator whether the evidence territory can sustain a listener-led chain; the fresh writer still owns route, order, POV and wording inside the canonical task.

## Mode: `draft_cold_read`

Run this after a submitted draft and before formal `review_section` routing.

1. Start a new clean viewer; do not reuse a `route_probe` viewer.
2. Supply the draft narration in original order, one coherent listening chunk at a time, without headings or metadata that the eventual listener would not hear.
3. Collect one per-chunk result after each stimulus, then send the completion signal and collect the final result.
4. If `continue` is `no` or `uncertain`, the curiosity chain has a material break, spoken naturalness is mixed or mechanical, trust is weakened or broken, or unresolved material resistance remains, stop before formal review.
5. A pass permits the operator to route the canonical formal review; it does not approve the section.

The viewer evaluates and diagnoses only. It never rewrites, prescribes replacement language, performs formal evidence review or grants approval. Do not pass the named source profile, viewer trace or viewer reasoning into writer, reviewer or reviser packets.

## Decision rule

Do not impose a fixed numeric score threshold or optimize for constant intensity. Decide from the whole continuation chain: whether observable developments partially pay live questions, whether a coherent mental world survives, whether immersion and trust persist, and whether the narration sounds natural when heard once. Calm, patient attention may pass; an energetic but broken chain may fail.

## Contamination and holdouts

- Keep all named comparison data and prose outside the runtime and production packets.
- Never transform public-comment wording into writer instructions or a device checklist.
- Do not tune the runtime to make one draft pass. Version any material projection change and retain its reason at the operator layer.
- Treat public comments as nonrandom, self-selected observations; do not infer private demographics, retention or theme frequency.
- After calibrating one section, run the unchanged runtime on a fresh adjacent section and on a materially different section or product type.
- Do not label the harness reusable until holdouts preserve lower-tail quality without audience-profile retuning.
