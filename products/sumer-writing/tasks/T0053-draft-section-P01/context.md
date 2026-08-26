# Context Packet — T0053-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0053-draft-section-P01/report.md`, `tasks/T0053-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0053-draft-section-P01 <capability>`.
Capabilities: `scope`, `resolve_claims`, `source`, `search`, `record`.
Use it only to increase source-level resolution inside the approved claim/source scope.
Every capability call is audit-logged. If external source reading adds detail, record it through the adapter before relying on it.
New claims, causal conclusions, contradictions or generalizations must be routed back to evidence authority.

Submission requirement: call `resolve_claims` successfully before submitting this task.

# BEGIN INSTRUCTION: system/core/creative-boundaries.md
# Creative Boundaries

1. Stay inside the approved evidence and continuity scope.
2. Build cinematic nonfiction around a focal subject changing in time, space or scale.
3. Facts alter that experience; they are not claims waiting for illustrations. Explain only what action or juxtaposition cannot carry.
4. In `evidence_bound`, use documented scenes or signaled anonymous reconstruction. Specific invented people, actions, thoughts, dialogue or outcomes require `representative_fiction`; they may never invent historical systems, chronology, measurements or conclusions.
5. Keep uncertainty natural. Hide claim IDs and evidence machinery.
6. Do not imitate another creator's wording, cadence, motifs, persona or signature structure.
7. Report a blocker when a useful move needs missing evidence or crosses the section boundary.

All other choices belong to the writer.
# END INSTRUCTION: system/core/creative-boundaries.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Assignment

Write cinematic narrative nonfiction: a verbal film in which the audience follows historical change through time, space and scale. Let meaning emerge before explanation. Do not decorate sequential claims with imagery or turn nonfiction into fiction.

Silently choose the focal subject, pressure and experienced change. Scale shifts, recurring images and ring returns are optional tools, not a checklist. Do not output this plan.

This is the full canonical section. Make its mission answerable across the full target range. Entry and exit states are section-wide boundaries, not sentences or requirements for every passage.

## Truth and reconstruction

Use documented scenes when supported; otherwise signal bounded anonymous reconstruction once. Never let vividness masquerade as witnessed fact.

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

Requested at: 2026-08-26T12:41:21.148297+00:00

## Request

Human-directed micro-loop. Produce only one 300-400 word P01 probe for review, not a full section. Rewrite the same memory-to-durable-trace beat as a coherent lived scene: concrete action, clear local objective and material consequence, continuous focal orientation, one authorized factual anchor if the packet supports it, and one or two non-symbolic world details. The scene must remain intelligible if abstract explanation is removed. Avoid balanced aphorisms, thesis-signalling metaphors, civilizational zoom-out, and any transition into token, bulla, tablet, writing, or ecology. Stop after the probe and wait for human feedback.
# END INPUT: 03_sections/P01/draft-rework-request.md
