# Context Packet — T0058-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0058-draft-section-P01/report.md`, `tasks/T0058-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0058-draft-section-P01 <capability>`.
Capabilities: `scope`, `attest_scope`, `source`, `search`, `record`.
Use it inside the approved claim/source scope to discover story material as well as verify facts: who or what acts, what happens, where, what object or trace is present, what remains unexplained, and what later evidence changes the current understanding.
These are optional retrieval questions, not required story ingredients or a narrative order; evidence records prescribe no creative route.
Every capability call is audit-logged. If external source reading adds detail, record it through the adapter before relying on it.
New claims, causal conclusions, contradictions or generalizations must be routed back to evidence authority.

Submission requirement: call `attest_scope` successfully before submitting this task.

# BEGIN INSTRUCTION: system/core/creative-boundaries.md
# Creative Boundaries

These are authorship limits, not story instructions.

1. Make no factual historical claim beyond approved evidence. Preserve qualifications, uncertainty, disagreement and counterevidence.
2. Distinguish documented fact, qualified inference and naturally signaled representative reconstruction. Reconstruction may add plausible ordinary action, perception or spatial detail around a composite person or local event embodying approved conditions. It is not evidence and cannot invent named actors, attributed quotes, chronology, measurements, institutions, motives, dialogue, private thoughts or causal conclusions.
3. Stay inside the section mission and established continuity unless explicitly authorized.
4. Keep evidence metadata out of narration.
5. Do not imitate another creator's wording, cadence, motifs, persona or signature structure.
6. Report a blocker when evidence or authority is insufficient.

Within these boundaries, every creative choice belongs to the writer. No creative method or sequence is compulsory unless the user locks it for this task.
# END INSTRUCTION: system/core/creative-boundaries.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Objective

Tell a compelling historical story within truth and continuity. Optimize for the listener wanting to keep following it. Let meaning emerge through what unfolds; do not announce and defend a thesis. Explanation serves the story. The mission is meaning to earn, not a proposition to prove. Hook and retention are outcomes, not a required technique.

## Assignment and authority

Write original long-form historical narration that is natural aloud. Choose its telling, composition, evidence, exposition, reconstruction and language. Use this style compass: calm, clear, weighty, investigative, grounded, causally meaningful and trustworthy rather than spectacular.

The word target is a forecast. Use bounded `search` and `source` to find story material by asking: who or what acts, what happens, where, what object or trace appears, what remains unexplained, and what later evidence changes understanding. This optional retrieval lens is not required ingredients, beats or prose order. Do not survey the ledger; call `attest_scope` before submission.

If bounded sources yield conclusions but no truthful story material, report an evidence-resolution blocker; do not substitute exposition.

## Feedback boundary

In rework, the observed problem and desired audience outcome bind. Repair examples and method hypotheses are non-binding. Only `owner_locked_for_single_task` compels a method.

Keep metadata out. Block when the mission exceeds evidence or section bounds.
# END INSTRUCTION: system/operations/draft-section.md

# BEGIN INPUT: 03_sections/P01/section.json
{
  "section": "P01",
  "title": "Trước chữ viết đã có một bài toán phải giải",
  "mission": "Điều gì khiến việc giữ thông tin bằng những dấu bền trên đất sét trở nên hữu ích?",
  "historical_change": {
    "from": "Kế toán bằng token và ấn tín rời rạc chỉ đủ sức theo dõi các giao dịch điểm-điểm trong một cộng đồng nhỏ.",
    "to": "Sự xuất hiện của các tập hợp ký hiệu số và dấu ấn hình thành hệ thống lưu trữ ngoại thân đầu tiên, cho phép thiết chế duy trì nghĩa vụ qua thời gian và khoảng cách."
  },
  "earned_meaning": "Chữ viết ban đầu không phải là một nỗ lực ghi lại lời nói, mà là một công nghệ vật chất để neo giữ các cam kết thực tế khi trí nhớ con người không còn gánh nổi.",
  "length_forecast_words": {
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
    "mode": "writer_directed_on_demand_v1",
    "access": "search_or_open_only_when_chosen_telling_needs_it"
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

Requested at: 2026-09-03T17:02:05.778953+00:00

## Observed failure and desired outcome

Ground P01 opening in material reality of transfer and counting without preconceptions

## Method authority

writer_owned

The writer owns the repair method. Examples and hypotheses from evaluation or conversation are not instructions and are intentionally absent from this packet.
# END INPUT: 03_sections/P01/draft-rework-request.md
