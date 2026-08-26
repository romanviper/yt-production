# Context Packet — T0048-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0048-draft-section-P01/report.md`, `tasks/T0048-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0048-draft-section-P01 <capability>`.
Capabilities: `scope`, `resolve_claims`, `claims`, `sources`, `source`, `search`, `record`.
Use it only to increase source-level resolution inside the approved claim/source scope.
Every capability call is audit-logged. If external source reading adds detail, record it through the adapter before relying on it.
New claims, causal conclusions, contradictions or generalizations must be routed back to evidence authority.

Submission requirement: call `resolve_claims` successfully before submitting this task.

# BEGIN INSTRUCTION: system/core/creative-boundaries.md
# Creative Boundaries

These are the only content boundaries the creative Agent must carry:

1. Stay inside the section's approved evidence ceiling and continuity scope.
2. A clearly signaled representative reconstruction may combine supported conditions, practices, objects and consequences into an anonymous situation or composite sequence. It must remain compatible with the evidence and must not pose as a documented event.
3. Reconstruction may supply only connective action or non-claiming sensory texture. It may not create names, quotations, private thoughts, precise motives, decisive events or outcomes, dates, measurements, causal links or certainty. Removing it must not change the section's factual or causal meaning.
4. Do not imitate a reference creator's wording, cadence, motifs, narrator persona or signature structure.
5. If a narrative move needs missing evidence or conflicts with entry/exit state, report the blocker instead of hiding it with prose.

All other narrative choices belong to the writer.
# END INSTRUCTION: system/core/creative-boundaries.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Assignment

Write historical narrative with the imaginative continuity of a novel—not a lecture, textbook chapter or claim summary. Let the listener experience the outline's causal model through events and consequences instead of being told the model.

Answer the approved mission. Entry/exit states set the destination; the writer owns the narrative choices inside it.

## Truth and reconstruction

When no continuous witnessed scene survives, you may clearly signal and build a representative reconstruction from supported practices, conditions, objects and consequences inside the evidence graph. It may join separately attested elements into an anonymous situation the listener can follow, but it may not become a claimed historical occurrence.

Reconstruction embodies supported meaning; it never creates meaning. Do not invent names, quotations, private thoughts, precise motives, decisive events or outcomes, dates, measurements, causal links or certainty. This permission is optional, not a required scene, POV or beat template.

## Evidence

Call `resolve_claims` before submission. It receives no creative plan and returns an unordered truth ceiling—not a coverage list or sequence authority. Retrieve source detail only where the telling needs more resolution. New meaning returns to evidence authority.

## Listener outcome

The listener must answer the mission in their own words and retell the historical path that made it true.

The evidence broker audits access and provenance; it never asks for, records or validates the writer's creative route. Do not scan the repo. Do not self-approve.
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

Requested at: 2026-08-26T04:18:35.282006+00:00

## Request

Reject the current P01 draft and rewrite P01 from a clean context as a historical narrative with the imaginative continuity of a novel. Let the approved causal model emerge through a sequence of events and consequences rather than lecture-style exposition. Use bounded representative reconstruction only within verified truth; do not reuse the rejected draft or imitate any benchmark.
# END INPUT: 03_sections/P01/draft-rework-request.md
