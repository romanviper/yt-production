# Context Packet — T0043-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0043-draft-section-P01/report.md`, `tasks/T0043-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0043-draft-section-P01 <capability>`.
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

Answer the approved mission with a self-authored section. Mission and entry/exit states define the destination; the writer owns route, order, factual subset, POV and wording.

## Route-first composition

Do not build the section by arranging claim records. Before reading claim prose, privately form an authored historical movement from changing conditions, live questions and consequences. Pass that provisional 200–2,000-character route with `resolve_claims --route-intent "..."`, without claim/source IDs or copied claim prose. It is private scratch recorded in the audit trace, not a deliverable, approval gate or beat sheet.

Treat the returned `claim_records` map as an unordered ledger that constrains, supports and corrects the route. Select only what the telling needs; change the route when support fails. Storage order, claim IDs and one-paragraph-per-claim coverage have no narrative authority.

Let supported action, object, place and process carry meaning. Explain only connections or needed caveats they cannot. Never bolt imagery onto an argument.

## Listener outcome

Write for one attentive hearing. When the section ends, a listener must be able to:

1. answer the section mission in their own words; and
2. retell the historical path that made that answer true.

## Boundaries and evidence

Stay inside the truth ceiling and continuity scope. Do not invent unsupported people, scenes, thoughts, dialogue, details or causal certainty. Draft submission requires whole-scope `resolve_claims`; claim/search access remains closed until its route commitment succeeds.

Before `route_intent`, use `scope`, `sources`, `source` or `record` only to gather observable material when the mission packet is too thin; none orders or authorizes the story.

Increase source-level resolution only inside the approved graph. New claims, causal conclusions, contradictions, theses or generalizations return to evidence authority.

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

Requested at: 2026-08-25T11:59:42.699734+00:00

## Request

Clean validation run of the route-first harness. Write a completely fresh P01 from the approved mission, state change and evidence ceiling without reading or preserving prior prose, scores or benchmark prose. Let supported transformations, live questions and consequences carry the telling; use direct explanation only where the meaning or evidence boundary cannot otherwise be completed. Produce one full draft, perform one short read-aloud polish, then stop for human feedback.
# END INPUT: 03_sections/P01/draft-rework-request.md
