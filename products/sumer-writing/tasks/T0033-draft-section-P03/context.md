# Context Packet — T0033-draft-section-P03

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P03`
- Unit: `-`
- Allowed writes: `03_sections/P03/draft.md`, `03_sections/P03/handoff.md`, `tasks/T0033-draft-section-P03/report.md`, `tasks/T0033-draft-section-P03/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0033-draft-section-P03 <capability>`.
Capabilities: `scope`, `claims`, `sources`, `source`, `search`, `record`.
Use it only to increase source-level resolution inside the approved claim/source scope.
Every capability call is audit-logged. If external source reading adds detail, record it through the adapter before relying on it.
New claims, causal conclusions, contradictions or generalizations must be routed back to evidence authority.

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

## Responsibility

Answer the approved section mission with a self-authored section.

The outline defines the destination. `section.json` defines the section objective and entry/exit state. The writer decides the route, structure, order, factual subset, POV, exposition and wording.

Claims and approved sources limit what the section may assert; they are not a content checklist and do not prescribe a narrative route.

For canonical direct-authorship drafting, claim IDs in the packet are a truth boundary, not ready-made writing material. Resolve the relevant claims through the bounded evidence adapter before drafting. Do not bypass that adapter by opening `narration-pack.json`, `evidence-pack.json` or research ledgers directly.

## Boundaries and evidence

Stay inside the current truth ceiling and continuity scope. Do not invent unsupported people, scenes, thoughts, dialogue, details or causal certainty.

Use bounded evidence access to inspect the approved claims and increase factual resolution when the section needs it. Retrieved source-supported detail may sharpen the draft, but it must remain inside the approved claim/source graph and keep provenance/auditability.

**Increase evidence resolution; do not silently expand the truth ceiling.** New claims, causal conclusions, contradictions, theses or generalizations must return to research authority.

Do not scan the repo. Do not self-approve.
# END INSTRUCTION: system/operations/draft-section.md

# BEGIN INPUT: 03_sections/P03/section.json
{
  "section": "P03",
  "title": "Khi chữ viết bắt đầu làm nhiều việc hơn",
  "mission": "Điều gì xảy ra khi chữ viết từ một công cụ ghi chép bắt đầu được dùng cho ngày càng nhiều việc khác nhau?",
  "entry_state": "Writing vẫn chủ yếu được nhìn như công cụ bookkeeping.",
  "exit_state": "Khán giả hiểu writing đã trở thành một môi trường nhiều chức năng; càng nhiều domain dựa vào nó, càng quan trọng việc duy trì convention, access và competence.",
  "transition": "Expansion cho biết writing được dùng ở đâu; phần tiếp theo phải trả lời nó thực sự thay đổi năng lực của một institution bằng cơ chế nào.",
  "target_words": {
    "min": 1000,
    "max": 1450
  }
}
# END INPUT: 03_sections/P03/section.json

# BEGIN INPUT: 03_sections/P03/narration-pack.json
{
  "section": "P03",
  "cycle_id": "C003",
  "truth_ceiling": {
    "claim_ids": [
      "CLM-0035",
      "CLM-0036",
      "CLM-0037",
      "CLM-0038",
      "CLM-0039",
      "CLM-0040",
      "CLM-0041",
      "CLM-0043",
      "CLM-0044",
      "CLM-0045"
    ]
  }
}
# END INPUT: 03_sections/P03/narration-pack.json

# BEGIN INPUT: 03_sections/P03/continuity-in.md
# Continuity Input — P03

Cycle: `C003`

Dependencies: P02

## Prior handoff

Chưa có hoặc sẽ được task owner cập nhật trước drafting.

## Canonical terms required here

Tham chiếu story bible.
# END INPUT: 03_sections/P03/continuity-in.md
