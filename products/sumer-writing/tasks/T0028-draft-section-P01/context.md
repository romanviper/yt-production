# Context Packet — T0028-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0028-draft-section-P01/report.md`, `tasks/T0028-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Only the material inside this packet is task context. Do not scan the repository.

# BEGIN INSTRUCTION: system/core/creative-boundaries.md
# Creative Boundaries

These are the only content boundaries the creative Agent must actively carry:

1. Stay inside the current section's approved evidence ceiling and continuity scope.
2. Do not invent people, scenes, thoughts, dialogue, sensory details or causal certainty.
3. Do not imitate a reference creator's wording, cadence, motifs, narrator persona or signature structure.
4. If the intended narrative move needs missing evidence or conflicts with the section's entry/exit state, report the blocker instead of hiding it with prose.

Everything else about ordering, paragraph count, rhythm, opening form and local structure is a creative decision.
# END INSTRUCTION: system/core/creative-boundaries.md

# BEGIN INSTRUCTION: system/standards/channel-constitution.md
# Channel Constitution

## Core value

A system, institution, technology or idea becomes the protagonist. The story follows how pressure forms it, how it expands what people can do, what conflicts and consequences it creates, and how it transforms, weakens or survives as a legacy.

## Whole-script architecture

Every script has three clear audience-facing acts. These acts belong to the whole script. A production section is only a bounded work unit and must not repeat opening–body–ending as a miniature template.

## Voice

The narrator is calm, clear, weighty and investigative. Their default relationship to the audience is guide and companion, not lecturer. Let the audience encounter concrete evidence, action, consequence or change before supplying interpretation when the material genuinely permits it.

Audience agency must be real rather than staged: do not call specialist classifications or decoded categories “what we can already see” unless a non-specialist can actually perceive the relevant cue without that expertise. When expert interpretation is necessary, provide it plainly and then let the audience follow what changes because of it.

Start concrete, widen only when a mechanism needs explanation, then return to what that mechanism allows or costs people. Prefer causality to chronology, consequence to trivia and ordinary Vietnamese to abstract terminology. Emotional weight comes from evidenced consequences, not rhetorical intensity.

The identity is stable; its expression remains adaptive. The Agent chooses local structure, pace and phrasing from the material instead of filling a house style formula.
# END INSTRUCTION: system/standards/channel-constitution.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Responsibility

Write one section that achieves the approved audience shift and advances its assigned act/movement. Treat the story plan as intent and evidence selection, not a prescribed route. The Agent chooses ordering, opening form, paragraph count, rhythm and transitions.

## Narrative stance

Place the audience beside the evidence rather than beneath a lecture. When material allows, let them encounter an object, action, process, consequence, contrast or change before explanation. Narrator clarification should sharpen an inference already underway, not perform the full `observe → interpret → qualify → conclude` sequence for them.

Do not stage specialist classification as audience observation. If a cue only becomes meaningful after expert identification, give that identification as narrator context instead of implying the listener could already see its meaning for themselves.

A real object, documented action, process, failure, transformation or bounded puzzle can carry story without invented drama. A section does not need a historical event chain if another carrier creates genuine narrative movement. Compress stretches that mainly deliver processed analysis, or return to the concrete carrier.

Core evidence anchors the draft. Optional evidence appears only when useful. Guardrails constrain wording without becoming exposition; excluded claims stay out. Preserve approved entry/exit state and continuity.

Do not turn a narrative implication, intuitive consequence or useful metaphor into a substantive historical function or causal claim unless the narration pack supports it. If the approved shift requires such a claim, or depends on evidence the audience cannot actually perceive as designed, report the mismatch for design/evidence routing instead of concealing it with prose.

Length is an estimate, never a quota. Do not pad.

Write natural spoken Vietnamese and a compact handoff. Do not review or approve your own draft.
# END INSTRUCTION: system/operations/draft-section.md

# BEGIN INPUT: 02_outline/story-bible.md
# Story Bible — P01 relevant scope

P005390 shows material survival does not equal transparent speech. Reward first: viewer learns this is not merely a “message to translate”. Full reveal shifts the mystery from “what does it say?” to “what can a not-full-speech record do better than human memory?”. Keep one dominant question, reward before explanation, no invented human scene, no world-first claim, and no chronology/definition pile.

P005390 is the opening object: grain-related quantities; exact transaction/language uncertain. The retention rule is earned curiosity: the next question must come from the limitation just demonstrated, not a teaser added from outside.
# END INPUT: 02_outline/story-bible.md

# BEGIN INPUT: 02_outline/voice-profile.md
# Voice Profile — P01 relevant scope

Lead through question → evidence → changed interpretation. Calm, clear investigative Vietnamese. Narrator is guide/companion, not lecturer. Product voice prefers ordinary Vietnamese and concrete verbs. A short sentence may lock a reveal; longer sentences may connect a mechanism. Qualifiers should be clear without becoming a disclaimer pile.

P005390 gives the micro-reward early then changes the mystery. After abstraction, return to the object/action/consequence. Do not imitate benchmark cadence, persona, motifs or wording.
# END INPUT: 02_outline/voice-profile.md

# BEGIN INPUT: 03_sections/P01/brief.md
# P01 Brief

Narrative job: cold-open P005390. Micro-reveal in 20–30 seconds; full reveal in 60–90 seconds/~140–210 words before chronology/definition. Then shift to the earned question: if the tablet does not return full speech, why is this kind of relation worth preserving?

Entry: viewer treats tablet as a message that only needs translation.
Exit: viewer knows what remains/what is missing and asks what this kind of memory solves that human memory does not.
Non-goals: no language/transaction/world-first claim; do not delay the first reward; do not hide known facts to fake mystery.
# END INPUT: 03_sections/P01/brief.md

# BEGIN INPUT: 03_sections/P01/story-plan.json
{
  "schema_version": 3,
  "section": "P01",
  "status": "approved",
  "audience_shift": "Khán giả bắt đầu bằng mô hình quen thuộc: tablet cổ là một message có ý nghĩa hoàn chỉnh nhưng hiện chưa được dịch. Cuối P01, họ phải tự đổi category của P005390: thứ chắc chắn nhất còn lại không phải một câu nói bị khóa trong đất sét, mà là một record có tổ chức mà scholarship vẫn nhận ra được quantity/grain classification và structural regularity dù language, exact transaction và full speech không còn chắc chắn. Từ sự đổi category đó mới sinh ra câu hỏi tiếp theo: nếu full speech không phải thứ cần được giữ lại, tại sao việc đưa những relation này ra ngoài trí nhớ lại đáng làm?",
  "story_strategy": "Dùng P005390 như một reclassification puzzle, không như một ví dụ để narrator giảng về early writing. Viewer chỉ được tự nhận ra raw cue thật sự nhìn thấy trên vật thể: dấu được nhóm, lặp và chiếm những vị trí có tổ chức; tuyệt đối chưa gọi đó là quantity hay grain. Narrator nhanh chóng cung cấp classification chuyên môn hẹp nhất mà evidence cho phép: đây là một administrative tablet ghi các quantity liên quan đến grain. Sau đó không mở thêm kiến thức mới mà thử chính mô hình 'message cần dịch': lần lượt bỏ khỏi nó những gì evidence không cho khôi phục chắc chắn — underlying language, exact transaction, full sentence/voice. Local turn phải xảy ra ở đây: mỗi lớp certainty bị lấy đi làm tablet kém đọc được như speech nhưng đồng thời rõ hơn như một structured record. Tension vì thế đến từ việc vật thể đổi nghĩa ngay trước mắt viewer, không từ withholding fact hay mystery giả. Giữ toàn bộ P01 bám vào một object và một dominant question; không mở chronology, world-first, definition debate hay history-of-decipherment. Dừng ngay khi viewer đã đổi cách hiểu P005390 từ 'message bị thiếu bản dịch' thành 'record không cần giữ trọn speech để vẫn giữ được structure', vì chính limitation đó mới kiếm ra câu hỏi về externalized memory cho P02.",
  "word_budget": {
    "recommended": {
      "min": 500,
      "max": 650
    },
    "rationale": "P01 chỉ có một carrier, hai core claims và một state change chính: reclassify P005390 từ unread message thành structured record. 500–650 từ đủ cho raw cue, early expert clarification, controlled subtraction và category shift mà không biến uncertainty thành lecture."
  },
  "evidence_roles": {
    "core": [
      "CLM-0042",
      "CLM-0024"
    ],
    "optional": [],
    "guardrail": [],
    "exclude": []
  },
  "design_risks": [
    "Để viewer tự suy ra quantity, grain hoặc transaction từ hình dạng dấu trước narrator clarification.",
    "Dùng uncertainty như disclaimer pile thay vì làm động cơ cho category shift của object.",
    "Nói thesis về externalized memory quá sớm, trước khi P005390 thực sự đổi từ 'message' thành 'record' trong đầu viewer.",
    "Biến structural regularity thành bằng chứng cho exact syntax, exact transaction hoặc recovered voice mà evidence không cho phép.",
    "Rời object sang chronology, definition, world-first hoặc decipherment ngay sau reveal và làm mất local dramatic problem.",
    "Biến story strategy thành beat sheet/cadence prescription thay vì giữ writer tự chọn route để đạt đúng audience shift."
  ],
  "approved_by": "user",
  "approved_at": "2026-08-18T09:44:00+00:00"
}
# END INPUT: 03_sections/P01/story-plan.json

# BEGIN INPUT: 03_sections/P01/narration-pack.json
# Narration Pack — P01

CORE CLM-0042: P005390/MMA 1988.433.2 is a physical Uruk III administrative tablet recording grain-related quantities; its language and exact transaction remain uncertain. Use it as a representative preserved administrative form, not as quoted individual voice or proof of a specific economic institution.

CORE CLM-0024: Proto-cuneiform sign distribution and tablet position can reveal structural regularities even when a sign's spoken value or underlying language remains uncertain. Separate observable graphic pattern from modern decipherment and language attribution.

No optional, guardrail or excluded claims.
# END INPUT: 03_sections/P01/narration-pack.json

# BEGIN INPUT: 03_sections/P01/continuity-in.md
Dependencies: none. No prior handoff.
# END INPUT: 03_sections/P01/continuity-in.md
