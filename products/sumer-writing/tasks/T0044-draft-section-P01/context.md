# Context Packet — T0044-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0044-draft-section-P01/report.md`, `tasks/T0044-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0044-draft-section-P01 <capability>`.
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

Requested at: 2026-08-25T12:36:45.140778+00:00

## Request

Fast v3 harness experiment. Write a completely fresh P01 without reading prior drafts, reviews, scores, task history or benchmark prose. Before committing story_route, open only approved source URLs/locators and record 1-2 short source-level details that are materially observable (object, mark, physical arrangement, action or change), with a hard cap of 3 records; if no such grounded material can be obtained quickly, stop and report the blocker instead of drafting. Commit one material carrier and 3-5 ordered observable transformations in which each physical change creates the next live question or consequence. Do not order topics, claims, caveats or thesis points. After claim resolution, use the ledger only to remove, qualify or locally correct unsupported material; do not rebuild the route around claim order. Let show carry meaning and reserve tell for indispensable connections or evidence limits. Produce one full draft, perform one short read-aloud polish, submit, then stop for immediate human feedback.
# END INPUT: 03_sections/P01/draft-rework-request.md
