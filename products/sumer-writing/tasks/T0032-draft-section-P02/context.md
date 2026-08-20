# Context Packet — T0032-draft-section-P02

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P02`
- Unit: `-`
- Allowed writes: `03_sections/P02/draft.md`, `03_sections/P02/handoff.md`, `tasks/T0032-draft-section-P02/report.md`, `tasks/T0032-draft-section-P02/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0032-draft-section-P02 <capability>`.
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

# BEGIN INPUT: 03_sections/P02/section.json
{
  "section": "P02",
  "title": "Hữu ích trước khi thành câu",
  "mission": "Vì sao một hệ thống ghi dấu có thể hữu ích ngay cả trước khi nó ghi được một câu nói liên tục?",
  "entry_state": "Khán giả vẫn có thể nghĩ 'chưa thành câu' đồng nghĩa 'chưa phải công nghệ có sức nặng'.",
  "exit_state": "Khán giả hiểu structured signs/layout có thể giữ repeatable relations đủ để vận hành administration; ranh giới writing/proto-writing và language attribution vẫn phải qualified.",
  "transition": "Một system đã có thể làm việc. Bây giờ câu chuyện cần theo dõi điều gì xảy ra khi writing được dùng cho ngày càng nhiều loại việc khác nhau.",
  "target_words": {
    "min": 1150,
    "max": 1750
  }
}
# END INPUT: 03_sections/P02/section.json

# BEGIN INPUT: 03_sections/P02/narration-pack.json
{
  "section": "P02",
  "cycle_id": "C003",
  "truth_ceiling": {
    "claim_ids": [
      "CLM-0001",
      "CLM-0002",
      "CLM-0003",
      "CLM-0004",
      "CLM-0005",
      "CLM-0006",
      "CLM-0007",
      "CLM-0008",
      "CLM-0009",
      "CLM-0019",
      "CLM-0020",
      "CLM-0021",
      "CLM-0022",
      "CLM-0023",
      "CLM-0024",
      "CLM-0025",
      "CLM-0034",
      "CLM-0042"
    ]
  }
}
# END INPUT: 03_sections/P02/narration-pack.json

# BEGIN INPUT: 03_sections/P02/continuity-in.md
# Continuity Input — P02

Cycle: `C003`

Dependencies: P01

## Prior handoff

P01 đã khóa payoff rằng dấu bền trở nên hữu ích khi các thực hành đếm, niêm phong, xác thực và ghi số gặp nhu cầu theo dõi hàng hóa, lao động và nghĩa vụ ở quy mô lớn hơn. Numerical systems là continuity chắc hơn token genealogy; administration là pressure lớn nhưng không phải monocause.

## Canonical terms required here

Giữ phân biệt proto-cuneiform với mature cuneiform; không chắc hóa underlying language là Sumerian.
# END INPUT: 03_sections/P02/continuity-in.md

# BEGIN INPUT: 03_sections/P01/handoff.md
# Handoff — P01

Cycle: `C003`
Task: `T0031-draft-section-P01`

## Mission answer

Dấu bền trên đất sét trở nên hữu ích khi những thực hành đếm, niêm phong, xác thực và ghi số gặp một môi trường đô thị có nhu cầu theo dõi ngày càng nhiều hàng hóa, lao động và nghĩa vụ. Giá trị nằm ở khả năng giữ một phần thông tin ở dạng ổn định để có thể kiểm tra lại, không ở một invention event duy nhất.

## Historical progression

1. Uruk cho thấy quy mô đô thị và thiết chế đủ lớn để làm việc kiểm soát thông tin trở thành một pressure đáng kể.
2. Trước proto-cuneiform đã tồn tại nhiều thực hành song song: token, clay balls/bullae, seals và numerical tablets.
3. Token không tạo thành một universal code hay một genealogy tuyến tính; numerical systems là continuity vật chất chắc hơn.
4. Vật liệu sát proto-cuneiform cho thấy seal impressions, numerical notation và commodity signs có thể cùng xuất hiện mà không cần một câu hoàn chỉnh.
5. Earliest corpus còn lại chủ yếu hành chính, nhưng evidence không cho phép biến administration thành monocause hay gán tax/tribute/redistribution khi thiếu dấu hiệu phân biệt.

## Evidence retrieval used

- Resolved `CLM-0011`–`CLM-0018` qua bounded evidence scope.
- Opened approved source `SRC-0001`, reviewed locator `pp. 24–31`.
- Recorded source-level resolution về quy mô Uruk, clay tokens trong sealed clay balls, exterior numerical impressions, linearity caveat và early Uruk numerical/commodity signs.

## Boundary kept

Không invention scene; không direct token→tablet genealogy; không universal token code; không ethnic attribution; không biến administrative pressure thành nguyên nhân duy nhất; không gán loại giao dịch cụ thể khi evidence chỉ cho phép accounting/administrative context.

## Transition

P02 có thể bắt đầu từ câu hỏi: khi numerical recording đã hữu ích, điều gì khiến hệ thống dấu bắt đầu mang nhiều loại thông tin hơn?
# END INPUT: 03_sections/P01/handoff.md
