# Context Packet — T0039-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0039-draft-section-P01/report.md`, `tasks/T0039-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0039-draft-section-P01 <capability>`.
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

## Responsibility

Answer the approved section mission with a self-authored section.

The outline defines the destination. `section.json` defines the section objective and entry/exit state. The writer decides the route, structure, order, factual subset, POV, exposition and wording.

Claims and approved sources limit what the section may assert; they are not a content checklist and do not prescribe a narrative route.

## Listener outcome

Write for one attentive hearing. When the section ends, a listener must be able to:

1. answer the section mission in their own words; and
2. retell the historical path that made that answer true.

This is an outcome, not a prescribed structure. Choose the route yourself. Do not write to an evaluator, mention a scoring system or imitate a benchmark.

## Boundaries and evidence

Stay inside the current truth ceiling and continuity scope. Do not invent unsupported people, scenes, thoughts, dialogue, details or causal certainty.

Before relying on any claim prose, call the packet's `resolve_claims` capability. Direct draft submission is blocked until every scoped claim has been resolved through the broker. Use the other bounded evidence capabilities only when additional factual resolution is needed. Retrieved source-supported detail may sharpen the draft, but it must remain inside the approved claim/source graph and keep provenance/auditability.

**Increase evidence resolution; do not silently expand the truth ceiling.** New claims, causal conclusions, contradictions, theses or generalizations must return to research authority.

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

Requested at: 2026-08-25T09:12:30.812576+00:00

## Request

Viết lại toàn bộ P01 trong một vòng ngắn như một đoạn phim tài liệu có chuyển động, không phải phân tích khảo cổ hay thuyết trình hiện vật. Chọn lọc ít fact hơn và nối chúng thành một quá trình liên tục: mỗi fact phải làm cảnh trong đầu khán giả thay đổi, dịch chuyển thời gian/không gian/quy mô hoặc làm lộ ra một áp lực mới dẫn tự nhiên sang fact kế tiếp. Ưu tiên động từ, biến đổi vật chất, quan hệ không gian và hậu quả có thể quan sát; chỉ giới thiệu thuật ngữ sau khi khán giả đã hình dung vật/chức năng. Không dừng camera quá lâu trên chi tiết hiện vật, taxonomy, định nghĩa, phép đo hoặc caveat; gom qualification cần thiết thật ngắn. Giọng Việt nói tự nhiên, giàu điện ảnh nhưng không bịa người, scene, sensory detail hay causal certainty ngoài evidence. Không xem draft/score cũ hoặc benchmark prose. Giữ mission, truth ceiling, P01-P02 boundary và word cap. Một draft, một read-aloud polish, rồi dừng để human feedback.
# END INPUT: 03_sections/P01/draft-rework-request.md
