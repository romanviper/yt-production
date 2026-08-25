# Context Packet — T0046-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0046-draft-section-P01/report.md`, `tasks/T0046-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0046-draft-section-P01 <capability>`.
Capabilities: `scope`, `resolve_claims`, `claims`, `sources`, `source`, `search`, `record`.
Use it only to increase source-level resolution inside the approved claim/source scope.
Every capability call is audit-logged. If external source reading adds detail, record it through the adapter before relying on it.
New claims, causal conclusions, contradictions or generalizations must be routed back to evidence authority.

Submission requirement: call `resolve_claims` successfully before submitting this task.

# BEGIN INSTRUCTION: system/core/creative-boundaries.md
# Creative Boundaries

These are the only content boundaries the creative Agent must actively carry:

1. Stay inside the current section's approved evidence ceiling and continuity scope.
2. Do not invent people, scenes, thoughts, dialogue, sensory details or causal certainty.
3. Do not imitate a reference creator's wording, cadence, motifs, narrator persona or signature structure.
4. If the intended narrative move needs missing evidence or conflicts with the section's entry/exit state, report the blocker instead of hiding it with prose.

Everything else about ordering, paragraph count, rhythm, opening form and local structure is a creative decision.
# END INSTRUCTION: system/core/creative-boundaries.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Assignment

Answer the approved mission. Entry/exit states set the destination; the writer owns route, order, factual subset, POV and wording.

## Story-route-first composition

Before claim prose, make one `resolve_claims --story-route-json '...'` call. Its object has exactly `carrier`, `entry_observable_state`, 3–6 ordered `transformations`, and `exit_observable_state`; each transformation has exactly `observable_change` and `question_or_consequence`.

The carrier is one materially observable thing or process. Transformations change world, material or action—not topics, claims, themes, explanations or caveat order. No claim/source IDs or copied 10-word claim windows. The route is traced private scratch, not an artifact, gate or agent.

Claim records are an unordered ledger that only constrains, supports or corrects this route. Ledger order, IDs and claim-by-claim coverage have no narrative authority.

Let supported action, object, place and process carry meaning. Explain only connections or caveats they cannot.

## Listener outcome

The listener must answer the section mission in their own words and retell the historical path that made it true.

## Boundaries and evidence

Stay inside truth and continuity scope; invent no people, scenes, thoughts, dialogue, details or certainty. Claim/search stays closed until the route succeeds. Before it, `scope`, `sources`, `source` and `record` may gather observable material; none orders the story. Submission requires whole-scope resolution. New meaning returns to evidence authority.

Do not scan the repo. Do not self-approve.
# END INSTRUCTION: system/operations/draft-section.md

# BEGIN INPUT: 03_sections/P01/section.json
{
  "section": "P01",
  "title": "Trước chữ viết đã có một bài toán phải giải",
  "mission": "Điều gì khiến việc giữ thông tin bằng những dấu bền trên đất sét trở nên hữu ích?",
  "entry_state": "Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.",
  "exit_state": "Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.",
  "transition": "Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.",
  "target_words": {
    "min": 1050,
    "max": 1550
  }
}
# END INPUT: 03_sections/P01/section.json

# BEGIN INPUT: 03_sections/P01/narration-pack.json
{
  "section": "P01",
  "cycle_id": "C003",
  "truth_ceiling": {
    "claim_ids": [
      "CLM-0011",
      "CLM-0012",
      "CLM-0013",
      "CLM-0014",
      "CLM-0015",
      "CLM-0016",
      "CLM-0017",
      "CLM-0018"
    ]
  }
}
# END INPUT: 03_sections/P01/narration-pack.json

# BEGIN INPUT: 03_sections/P01/continuity-in.md
# Continuity Input — P01

Cycle: `C003`

Dependencies: Không có.

## Prior handoff

Chưa có hoặc sẽ được task owner cập nhật trước drafting.

## Canonical terms required here

Tham chiếu story bible.
# END INPUT: 03_sections/P01/continuity-in.md

# BEGIN INPUT: 03_sections/P01/draft-rework-request.md
# Draft Rework — P01

Requested by: user

Requested at: 2026-08-25T14:00:32.518067+00:00

## Request

Fast viewer-led MVP. Write a completely fresh P01 without reading prior drafts, reviews, scores, task history or benchmark prose. Narrative authority is this empirical cold-viewer trace, obtained with no outline/claims/background: sealed bulla creates 'how can it be checked without breaking?' (curiosity 7); exterior impressions answer that and create 'if marks suffice, why keep counters inside?' (8); a flat tablet with no contents answers that and creates 'without contents, why trust the tablet?' (8); number plus commodity/category plus seal/validation answers that and creates 'show me one concrete record' (7); technical tablet IDs/N46 dropped curiosity to 6, while the plain reveal 'number marks beside a wheat sign preserve an amount of wheat but not who or why' restored it to 7 and naturally opened P02: 'how could a system record who and why?'. Commit 4 story-route transformations in exactly this revelation order; do not reorder into chronology, taxonomy, formation thesis or caveat sequence. Each reveal may answer only the prior viewer question and must leave the next one genuinely open. Retrieve and record at most one bounded approved SRC-0001 detail from pp. 24-31 supporting the number-before-commodity wheat example; omit tablet codes and numerical-system jargon from narration. Use claims only to remove or locally qualify unsupported detail, not to demand complete coverage. No institutional/preservation/feedback lecture tail: any indispensable qualifications must be compressed into at most two sentences attached to the visible object. End on the viewer's who/why question. One draft, one short read-aloud polish, submit, then stop for immediate human feedback.
# END INPUT: 03_sections/P01/draft-rework-request.md
