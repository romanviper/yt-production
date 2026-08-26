# Context Packet — T0057-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0057-draft-section-P01/report.md`, `tasks/T0057-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0057-draft-section-P01 <capability>`.
Capabilities: `scope`, `resolve_claims`, `source`, `search`, `record`.
Use it only to increase source-level resolution inside the approved claim/source scope.
Every capability call is audit-logged. If external source reading adds detail, record it through the adapter before relying on it.
New claims, causal conclusions, contradictions or generalizations must be routed back to evidence authority.

Submission requirement: call `resolve_claims` successfully before submitting this task.

# BEGIN INSTRUCTION: system/core/creative-boundaries.md
# Creative Boundaries

1. Stay within approved evidence and continuity.
2. Follow a focal carrier—person, object, place, process or question—through change; never force a person.
3. Across scale/viewpoint, keep a physical or causal anchor; widen narrator knowledge only at a real boundary. Make the cut, never explain it.
4. Facts change the experience, not decorate claims. Explain only what action or juxtaposition cannot.
5. Evidence-bound scenes are documented or anonymous reconstructions entered through natural uncertainty, not a technique label. Invented people, actions, thoughts, dialogue or outcomes require `representative_fiction` and may not invent systems, chronology, measurements or conclusions.
6. Keep uncertainty natural; hide claim IDs and evidence machinery.
7. Do not imitate another creator's wording, cadence, motifs, persona or signature structure.
8. Report a blocker when a useful move needs missing evidence or crosses the section boundary.

All other choices belong to the writer.
# END INSTRUCTION: system/core/creative-boundaries.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Assignment

Write cinematic narrative nonfiction: a verbal film in which the audience follows historical change through time, space and scale. Let meaning emerge before explanation. Do not decorate sequential claims with imagery or turn nonfiction into fiction.

Silently choose the focal carrier, pressure and experienced change. Scale shifts, recurring images and ring returns are optional tools, not a checklist. Do not output this plan.

This is the full canonical section. Make its mission answerable across the full target range. Entry and exit states are section-wide boundaries, not sentences or requirements for every passage.

## Truth and reconstruction

Use documented scenes when supported; otherwise enter bounded anonymous reconstruction through brief natural uncertainty. Never pause to label the device or let vividness masquerade as witnessed fact.

## Evidence

Call `resolve_claims` before submission. Its compact brief is material and red lines, not a plan or checklist. Give each passage only the evidence it needs; do not compress the entire brief into an opening or one explanatory block. Retrieve deeper detail only when it improves the telling. New meaning returns to evidence authority.

Keep packet metadata, claim IDs and evidence commentary out of narration. The broker audits provenance, not creative choices. Do not scan the repo or self-approve.
# END INSTRUCTION: system/operations/draft-section.md

# BEGIN INPUT: 03_sections/P01/section.json
{
  "section": "P01",
  "title": "Trước chữ viết đã có một bài toán phải giải",
  "mission": "Điều gì khiến việc giữ thông tin bằng những dấu bền trên đất sét trở nên hữu ích?",
  "entry_state": "Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.",
  "exit_state": "Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.",
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
  "evidence": {
    "mode": "compact_writer_brief_v1",
    "access": "bounded_on_demand"
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

Requested at: 2026-08-26T15:02:57.535213+00:00

## Request

Checkpoint the exact latest P01 opening-unit probe that received the strongest third-party review. This is preservation, not a new rewrite: keep the reviewed 710-word focal-carrier version unchanged, including its current caveats and imperfections, so the next session starts from the demonstrated narrative benchmark. Scope remains only the opening idea-unit and ends at the need for a durable checkable mark. Submit as ready_for_review; do not mark the section human-approved.
# END INPUT: 03_sections/P01/draft-rework-request.md
