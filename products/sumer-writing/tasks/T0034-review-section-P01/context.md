# Context Packet — T0034-review-section-P01

- Product: `sumer-writing`
- Operation: `review_section`
- Context profile: `evaluation`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/review.md`, `tasks/T0034-review-section-P01/report.md`, `tasks/T0034-review-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0034-review-section-P01 <capability>`.
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

# BEGIN INSTRUCTION: system/standards/channel-constitution.md
# Channel Constitution

## Core value

A system, institution, technology or idea is the protagonist. Follow how pressure forms it, what capabilities it creates, what conflicts/consequences follow, and how it changes, weakens or survives.

## Whole-script architecture

Every script has three audience-facing acts:

- **Opening:** establish the central tension, question and promise.
- **Body:** develop formation, expansion, conflict, consequence and adaptation.
- **Ending:** answer the question and close through consequence or legacy.

The three acts belong to the whole script, not each production section. Local storytelling form is adaptive.

## Voice and authorship

Narration should feel deliberate, clear, weighty and investigative, with expression suited to the subject. It need not be conversational.

Prefer causality to chronology dumps and consequence to trivia. Emotional weight must come from evidenced consequences, not rhetoric.

Inside approved truth/continuity boundaries, the writer owns local structure, POV, pace, factual selection, scale, imagery, reveal timing and phrasing. No carrier, concrete-first, before/after or recount-before-interpret route is universal.

## Conditional audience agency

Only when narration stages discovery/inference, the audience must have had access to the relevant cue before specialist classification. This is an integrity rule for that technique, not a requirement that every section use it.
# END INSTRUCTION: system/standards/channel-constitution.md

# BEGIN INSTRUCTION: system/standards/outcome-evaluation.md
# Outcome Evaluation Standard

Judge the draft by **outcome → diagnosis**, never method compliance.

## Primary judgment

First evaluate:

- whether the listener can answer the section mission after hearing the section;
- whether the listener can retell the historical path that led to that answer;
- section exit state and meaningful listener progression;
- authored narration rather than research recital;
- causal clarity;
- continuity;
- evidence integrity: no invention, false certainty, truth-ceiling expansion or hidden qualification/contradiction.

A factually correct draft may still fail if it delivers conclusions as a list or essay without leaving the listener with a retellable progression to the mission answer.

A draft may pass through many routes. Do not fail it for lacking a carrier, scene, object, before/after, raw clue, process sequence, chronology-first order or recount-before-interpret structure.

## Required outcome questions

Every review must answer both questions explicitly:

1. After hearing the section, can the audience answer the section mission in their own words?
2. Can the audience retell the historical path that led to that answer?

A `pass` requires both outcomes to be supported by the draft.

## Diagnose after failure

Only after an outcome problem is observed, diagnose the responsible layer. Any suggested repair method is optional; it is not a pass/fail invariant.

## Common failures

- `document mode`: accurate conclusions without a retellable historical progression;
- causal blur;
- continuity failure;
- evidence overreach.

## Routing

- `prose_execution`: mission/evidence territory are sound; execution failed to produce the required outcome.
- `product_architecture`: mission, boundary, progression or evidence territory is wrong.
- `evidence`: support is missing/contradicted/insufficient or requires truth-ceiling expansion.

No active story-plan/local-design authority exists on the current path. Give the smallest responsible revision scope and an observable acceptance test.
# END INSTRUCTION: system/standards/outcome-evaluation.md

# BEGIN INSTRUCTION: system/standards/section-quality-gate.md
# Section Production Quality Gate

Evaluation-only; never expose to the writer.

Emit one `schema_version: 1` JSON object between `<!-- production-gate:start -->` and `<!-- production-gate:end -->`.

Hard gates (`status: pass|fail|blocked`):

- `evidence_integrity`: supported and qualified
- `mission_and_exit`: answerable mission, achieved exit
- `adjacent_section_boundary`: complete current job, preserve next
- `one_hearing_narration`: intelligible and retellable once heard

Evidence-adjusted dimensions (integer 1–10):

- `hook_and_audience_promise`
- `historical_progression`
- `causal_clarity`
- `concrete_specificity`
- `narrative_momentum_and_stakes`
- `supported_human_work_orientation`
- `explanatory_economy`
- `spoken_rhythm_and_clarity`
- `ending_payoff_and_transition`

Record `score`, `evidence_scope: full|limited` and `basis`. Score supported opportunity, not volume. Limited evidence never licenses invention. Human/work orientation may score highly without a person or scene when evidence lacks one. Fabrication fails evidence integrity.

Derived verdict: `blocked` for any blocked gate; else `changes_requested` for any failed gate or score below 8; else `pass`. Diagnose the smallest issue set. Do not prescribe benchmark surface style.
# END INSTRUCTION: system/standards/section-quality-gate.md

# BEGIN INSTRUCTION: system/operations/review-section.md
# Operation — Review Section

## Responsibility

Evaluate the produced draft independently. Do not rewrite it.

Use the Outcome Evaluation Standard. Judge outcome first. The review must explicitly answer:

1. After hearing the section, can the audience answer the section mission in their own words?
2. Can the audience retell the historical path that led to that answer?

A draft that states correct conclusions but does not produce a retellable progression may be failed. Do not require any particular carrier, scene, object, reveal order, chronology, sequence or storytelling method.

Apply the Section Production Quality Gate. Emit its machine-readable block exactly once. A `pass` is valid only when all four hard gates pass and all nine evidence-adjusted dimensions score at least 8/10.

Also judge exit state, causal clarity, continuity and evidence integrity. Do not penalize a valid result because the writer chose a route different from anything upstream anticipated.

The packet contains a compact, hash-bound current/next-section boundary projection. Use it only to test whether this section completes its own job without consuming the next section's job. When a factual question cannot be resolved from the packet, use the bounded evidence broker; do not scan the repository.

For every material issue, record:

- an observable location and failure;
- its effect on listening, understanding or trust;
- the responsible layer: `prose_execution`, `product_architecture` or `evidence`;
- the smallest valid revision scope;
- an observable acceptance test.

The review must state one verdict: `pass`, `changes_requested` or `blocked`. A pass makes the section eligible for human approval; it never approves the section automatically.
# END INSTRUCTION: system/operations/review-section.md

# BEGIN INPUT: 02_outline/outline.json
{
  "projection_kind": "review_current_next_boundary",
  "outline_sha256": "d707db0c172a9db579593a136791d2b1e629892315e31bedfa0d795b8c92da9d",
  "current": {
    "id": "P01",
    "title": "Trước chữ viết đã có một bài toán phải giải",
    "narrative_job": "Thiết lập các pressure và information practices trước/sát thời điểm proto-cuneiform xuất hiện, đồng thời phá hai shortcut: một invention event duy nhất và token→tablet như đường tiến hóa tất định. Section phải kết thúc khi audience đã hiểu vì sao durable, inspectable records trở nên đáng giá mà chưa cần biết 'ai phát minh chữ viết'.",
    "entry_state": "Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.",
    "exit_state": "Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.",
    "transition": "Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.",
    "non_goal": "Không invention scene; không ethnic attribution; không universal token code; không direct token→tablet genealogy; không biến administrative pressure thành monocause."
  },
  "next": {
    "id": "P02",
    "title": "Hữu ích trước khi thành câu",
    "narrative_job": "Giải thích early record có thể làm công việc có thật trước khi continuous speech hoặc underlying language được recover chắc chắn. Section phải land được usefulness trước khi mở các guardrail về writing threshold, chronology, language và world-first.",
    "entry_state": "Khán giả vẫn có thể nghĩ 'chưa thành câu' đồng nghĩa 'chưa phải công nghệ có sức nặng'.",
    "exit_state": "Khán giả hiểu structured signs/layout có thể giữ repeatable relations đủ để vận hành administration; ranh giới writing/proto-writing và language attribution vẫn phải qualified.",
    "transition": "Một system đã có thể làm việc. Bây giờ câu chuyện cần theo dõi điều gì xảy ra khi writing được dùng cho ngày càng nhiều loại việc khác nhau.",
    "non_goal": "Không definition-first lecture; không chắc hóa Sumerian language; không uncontested world-first; không kể proto-cuneiform như mature cuneiform hay một bước tất định hướng tới alphabet."
  }
}
# END INPUT: 02_outline/outline.json

# BEGIN INPUT: 02_outline/story-bible.md
# Story Bible — Sumer Writing C003

Status: canonical companion to the approved C003 outline

## Trục nhân quả trung tâm

Phim không dùng mệnh đề “chữ viết tạo ra văn minh Sumer” như một sự thật mặc định. Mô hình mạnh nhất là **cùng phát triển rồi tạo phản hồi**: các thiết chế ở miền nam Mesopotamia làm tăng áp lực phải giữ ổn định lượng, loại, người và nghĩa vụ; nhiều thực hành đếm, niêm phong, phân loại và ghi dấu tạo nên môi trường trong đó proto-cuneiform xuất hiện; về sau, khi record được gắn với người có kỹ năng, xác thực, lưu trữ, truy hồi và authority, chúng có thể mở rộng một số năng lực phối hợp của institution. Năng lực tăng lên lại có thể làm tăng nhu cầu ghi chép.

Continuity không nằm ở một loại tablet, một dạng script hay một language bất biến. Thứ có thể sống qua nhiều thế kỷ là một **thực hành xã hội có thể tái tạo**: chọn quan hệ cần giữ, biến chúng thành dấu đủ bền và đủ quy ước, rồi duy trì người và thủ tục có khả năng tạo, đọc, chép, sửa, thích nghi, truy hồi và hành động dựa trên chúng.

Câu hỏi trung tâm dành cho khán giả là: **chữ viết đã thay đổi xã hội Sumer bằng cách nào, nếu bản thân những dấu trên đất sét không thể tự làm gì?**

## Whole-product causal progression

1. **Formation pressure / ecology:** trước một hệ thống writing rõ ràng đã có nhu cầu và nhiều phương thức để giữ quantity, classification và authentication. Administration là pressure lớn nhưng không phải monocause; không có một invention event hay genealogy tuyến tính được phép mặc định.
2. **Early usefulness:** một record có thể giữ những quan hệ lặp lại đủ để làm việc trước khi continuous speech hay underlying language được phục hồi chắc chắn. Writing threshold vì vậy là một boundary phải qualified, không phải opening verdict.
3. **Functional expansion:** writing tích lũy thêm economic, political, religious, legal/normative, correspondence, lexical, scholarly và literary uses theo kiểu additions/recombinations, không phải chiếc thang accounting → literature.
4. **Institutional feedback:** record tăng capacity khi gắn với classification, responsible people, authentication, accumulation và retrieval. Later institutional evidence có thể test mechanism này nhưng không được back-project magnitude về Uruk.
5. **Reproduced competence:** system chỉ sống khi competence được tái tạo qua người. Material durability, professional scribal identity, functional competence và population literacy phải được tách riêng.
6. **Enforcement boundary:** written claim, order, law hay norm có thể tồn tại và được truy hồi nhưng không tự tạo compliance. Agency và enforcement thuộc về people, procedure và authority.
7. **Adaptation:** survival đòi hỏi convention được học lại và sửa đổi trong language/institutional settings mới. Script survival, language survival và institutional survival là ba timeline khác nhau.
8. **Contraction / break / recovery:** cuneiform co lại qua nhiều thế kỷ; material có thể sống sau khi living competence mất. Modern decipherment là một quá trình xây lại competence bằng copying, multilingual comparison và repeated testing, không direct transmission.

Các bước trên là **state progression của toàn bộ phim**, không phải quy định về carrier, scene, reveal order hay paragraph structure. Writer được quyền chọn local route miễn ở trong evidence ceiling và đưa audience từ entry state tới exit state của section.

## Guardrail thời gian và attribution

- Uruk IV thường được đặt khoảng 3350/3300–3200 BCE; Uruk III/Jemdet Nasr khoảng 3200–3000 BCE. Ưu tiên relative sequence và giữ qualifier cho absolute date.
- Không xác định chắc underlying language của Uruk IV–III proto-cuneiform là Sumerian; không suy từ regional script tradition sang ethnic attribution.
- Không dùng “world first” như một fact không tranh cãi; early Egyptian writing chồng lấn chronology và priority phụ thuộc definition/calibration.
- Evidence Ur III về institutional capacity là bounded later test, không phải bằng chứng trực tiếp rằng Uruk đã có cùng magnitude.
- Evidence Old Babylonian về school/curriculum cho thấy later reproduction mechanism; không back-project một formal school system về origin phase.
- Ca. 1632 BCE failed-order case là exceptional bounded evidence; không generalize thành norm.
- 75 CE là latest-known dated anchor theo current research, không absolute last tablet hay last reader.
- Modern decipherment xảy ra sau competence break và phải được hiểu như recovery, không living continuity.

## Kỷ luật thuật ngữ

- **Writing:** dùng như một graded analytical threshold. Durable conventional marks có repeatable linguistic/lexical value có thể được xem là writing; devices truyền quantity/meaning mà chưa chứng minh language encoding đầy đủ có thể thuộc accounting/proto-writing.
- **Proto-cuneiform:** Uruk IV–III system với limited phonological recovery và underlying language chưa chắc chắn; không đồng nhất với mature cuneiform.
- **Cuneiform:** later logo-syllabic tradition có semantic và phonological values; không kể như một stage tất định hướng tới alphabet.
- Luôn tách **script, language, population, scribal role, functional competence, literacy và institution**.
- Tách **tax, tribute, market exchange, redistribution, ownership, labor obligation** khi evidence không cho phép đồng nhất.

## Causal và epistemic guardrails

- Không “ethnic Sumerians invented writing in 3200 BCE”.
- Không universal token → tablet → civilization ladder.
- Không writing-as-autonomous cause của state, law, labor coordination, memory hay enforcement.
- Không coi technical capacity của system là bằng chứng community luôn dùng capacity đó.
- Không coi archive là neutral sample của society; clay durability, discard, excavation và provenance tạo survival bias.
- Không suy population-wide literacy từ school/archive evidence.
- Không biến later copied/composite texts thành transparent original speech.
- Không direct Sumer → modern writing lineage; modern legacy mạnh nhất là recovery-mediated knowledge và ancient transmission chains có evidence.

## Evidence limits

- Không có defensible single invention event.
- Long technical shift từ proto-cuneiform sang mature wedge ductus chưa có tight state-by-state comparative evidence.
- Hittite adaptation hiện được support tốt ở process level, không ở một single documented adoption event.
- 75 CE là qualified endpoint anchor nhưng current research không support claim về một absolute “last tablet” hoặc “last reader”.
- Uruk → Ur III chronological jump phải luôn minh bạch khi later evidence được dùng để test feedback mechanism.

## Continuity và payoff toàn phim

Whole-product progression phải tạo được nhu cầu điều tra sức mạnh của durable records, sau đó lần lượt mở rộng rồi giới hạn claim về sức mạnh đó, và cuối cùng phân biệt material survival với living competence và recovered meaning. Final understanding không phải “clay was powerful” mà là: **durable marks trở thành historical force khi communities khiến chúng repeatable, retrievable và actionable; khi chain ấy đứt, material có thể còn nhưng meaning không tự tồn tại.**

Story Bible không chỉ định exact object, imagery sequence, discovery device, reveal timing, scene order hay paragraph mechanics cho bất kỳ P## nào. Những quyết định đó thuộc writer trong evidence ceiling của outline.
# END INPUT: 02_outline/story-bible.md

# BEGIN INPUT: 02_outline/voice-profile.md
# Voice Profile — Sumer Writing C003

Status: approved

## Product voice

Giọng kể bình tĩnh, sáng rõ, có sức nặng và mang tinh thần điều tra. Bộ phim theo lịch sử của chữ viết như một hệ thống xã hội–kỹ thuật: nó hình thành, mở rộng chức năng, tạo năng lực mới, gặp giới hạn, thích nghi và để lại di sản. Sự chắc chắn trong giọng kể phải đi theo độ chắc của bằng chứng; không dùng cường điệu để bù cho chỗ evidence yếu.

## Borrowed functions

Từ *Fall of Civilizations* và các benchmark lịch sử dài, chỉ học những chức năng tổng quát: giữ được một causal macro arc, chuyển scale khi cần, tôn trọng nguồn và uncertainty, và để vật thể, con người hoặc thực hành lịch sử xuất hiện khi evidence thực sự hỗ trợ chúng. Benchmark là tiêu chuẩn chức năng, không phải template sáng tác.

## Original expression

Bản tiếng Việt phải có nhịp và cách diễn đạt riêng của sản phẩm này. Khi thuật ngữ học thuật cần thiết, dùng nó chính xác nhưng không để vocabulary phân tích thay thế cho lịch sử đang được kể. Qualifier chỉ xuất hiện ở nơi thiếu nó sẽ làm sai nghĩa. Hệ thống là protagonist, nhưng hậu quả đối với con người, trách nhiệm, kỹ năng, access và continuity vẫn phải được nhìn thấy khi nguồn cho phép.

## Prohibited imitation

Không sao chép wording, cadence, motif, narrator persona, signature transition, chapter sequence hay opening formula của benchmark. Không dùng “Sumer invented writing” như settled fact; không kể token → tablet → civilization như một chiếc thang tất định; không gán agency tự trị cho clay hay writing; không biến archive thành toàn bộ society hoặc school evidence thành population literacy.

## Draft tests

Khi review hoặc revise, kiểm tra bốn điều: section có đạt entry→exit state đã duyệt không; causal claim có nằm trong evidence ceiling không; uncertainty quan trọng có được giữ đúng mức không; và prose có đứng được bằng logic, bằng chứng và expression riêng thay vì dựa vào việc mô phỏng benchmark không.
# END INPUT: 02_outline/voice-profile.md

# BEGIN INPUT: 03_sections/P01/section.json
{
  "schema_version": 4,
  "id": "P01",
  "title": "Trước chữ viết đã có một bài toán phải giải",
  "mission": "Điều gì khiến việc giữ thông tin bằng những dấu bền trên đất sét trở nên hữu ích?",
  "order": 1,
  "status": "ready_for_review",
  "human_approved": false,
  "dependencies": [],
  "narrative_job": "Thiết lập các pressure và information practices trước/sát thời điểm proto-cuneiform xuất hiện, đồng thời phá hai shortcut: một invention event duy nhất và token→tablet như đường tiến hóa tất định. Section phải kết thúc khi audience đã hiểu vì sao durable, inspectable records trở nên đáng giá mà chưa cần biết 'ai phát minh chữ viết'.",
  "entry_state": "Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.",
  "exit_state": "Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.",
  "target_words": {
    "min": 1050,
    "max": 1550
  },
  "cycle_id": "C003",
  "outline_sha256": "d707db0c172a9db579593a136791d2b1e629892315e31bedfa0d795b8c92da9d",
  "transition": "Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.",
  "movement_ids": [
    "M01"
  ],
  "macro_movements": [
    {
      "id": "M01",
      "title": "Trước chữ viết đã có một bài toán phải giải",
      "narrative_job": "Xác lập formation pressure và ecology: nhu cầu giữ thông tin hành chính/xác thực tăng trong bối cảnh thiết chế lớn hơn, nhưng evidence không cho phép một nguyên nhân duy nhất hay một genealogy tuyến tính. Movement phải khiến câu hỏi chuyển từ 'ai phát minh?' sang 'những áp lực và thực hành nào khiến durable recording trở nên hữu ích?'.",
      "entry_state": "Nguồn gốc được tưởng như một invention event đơn lẻ.",
      "exit_state": "Nguồn gốc được hiểu như một quá trình nhiều thực hành và nhiều áp lực cùng hội tụ; administration là trọng tâm nhưng không phải monocause."
    }
  ],
  "acts": [
    {
      "id": "A01",
      "role": "opening",
      "title": "Khi một xã hội cần trí nhớ ngoài con người"
    }
  ],
  "prose_provenance": {
    "task_id": "T0033-draft-section-P01",
    "operation": "draft_section",
    "submitted_at": "2026-08-25T03:12:26.242161+00:00",
    "draft_sha256": "a5611ee14f167c193a9faba73ac79711626ef816a333e79a6cb1463e2de6a292",
    "handoff_sha256": "836d755d3315efafdf6b354d36575d65cdba6a05f0164c7e2e276ff156eb7993"
  }
}
# END INPUT: 03_sections/P01/section.json

# BEGIN INPUT: 03_sections/P01/brief.md
# P01 — Trước chữ viết đã có một bài toán phải giải

Cycle: `C003`

## Whole-script acts

- opening — Khi một xã hội cần trí nhớ ngoài con người

## Macro movements

- M01 — Trước chữ viết đã có một bài toán phải giải

## Section objective

Thiết lập các pressure và information practices trước/sát thời điểm proto-cuneiform xuất hiện, đồng thời phá hai shortcut: một invention event duy nhất và token→tablet như đường tiến hóa tất định. Section phải kết thúc khi audience đã hiểu vì sao durable, inspectable records trở nên đáng giá mà chưa cần biết 'ai phát minh chữ viết'.

## Entry state

Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.

## Exit state

Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.

## Evidence territory

- CLM-0011
- CLM-0012
- CLM-0013
- CLM-0014
- CLM-0015
- CLM-0016
- CLM-0017
- CLM-0018

## Transition

Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.

## Continuity in

Không có.

## Continuity out

Không có.

## Non-goal

Không invention scene; không ethnic attribution; không universal token code; không direct token→tablet genealogy; không biến administrative pressure thành monocause.
# END INPUT: 03_sections/P01/brief.md

# BEGIN INPUT: 03_sections/P01/narration-pack.json
{
  "schema_version": 4,
  "section": "P01",
  "cycle_id": "C003",
  "created_at": "2026-08-19T10:21:00+00:00",
  "outline_sha256": "d707db0c172a9db579593a136791d2b1e629892315e31bedfa0d795b8c92da9d",
  "brief_sha256": "95e3739f6707521143b26085330ac1097d0416dba59b0418c3466f9a44e8888b",
  "evidence_pack_sha256": "488fbbd30dffd8f874eb1ad8cb44d153a0384b309d2c7637fa85dcd19b0e10df",
  "permitted_claims": [
    {
      "id": "CLM-0011",
      "statement": "Numerical systems provide the strongest material continuity between pre-writing devices and proto-cuneiform.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "counterevidence": "Continuity of individual non-numerical sign shapes is much less secure.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ]
    },
    {
      "id": "CLM-0012",
      "statement": "Neolithic clay objects called tokens were multifunctional; their existence does not prove a millennia-long standardized accounting code.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "counterevidence": "Some late simple tokens in bullae clearly served numerical/accounting functions.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "sources": [
        "SRC-0005",
        "SRC-0009"
      ]
    },
    {
      "id": "CLM-0013",
      "statement": "The direct token→tablet→writing sequence is too linear; seals, iconography, bullae, numerical tablets and institutional practice formed a parallel ecology.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "counterevidence": "Exact contribution of each component cannot be quantified.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "sources": [
        "SRC-0005",
        "SRC-0009",
        "SRC-0003"
      ]
    },
    {
      "id": "CLM-0014",
      "statement": "Administrative scale is a major formation pressure but not evidence that administration was the sole cause of writing.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "counterevidence": "Preserved earliest texts are overwhelmingly administrative, but corpus survival is selective.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ]
    },
    {
      "id": "CLM-0015",
      "statement": "The evidence supports a feedback model: expanding institutions demanded records, and better records could expand institutional capacity.",
      "type": "inference",
      "confidence": "medium",
      "status": "qualified",
      "counterevidence": "Downstream effects require WS06 case studies; WS02 cannot establish them alone.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ]
    },
    {
      "id": "CLM-0016",
      "statement": "The preserved proto-cuneiform corpus can distinguish accounting contexts more securely than it can distinguish market exchange from tax, tribute or redistribution.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "counterevidence": "Named agents, commodities, metrology and document structure sometimes narrow the transaction, but sign readings and institutional context remain incomplete.",
      "narrative_implication": "Use 'accounting/administrative transfer' unless reciprocity or institutional flow is independently demonstrated.",
      "sources": [
        "SRC-0001",
        "SRC-0010"
      ]
    },
    {
      "id": "CLM-0017",
      "statement": "Redistribution, labor coordination, obligation and ownership are not interchangeable formation mechanisms: each requires different evidence beyond the presence of numbers and commodities.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "counterevidence": "A single tablet may participate in more than one mechanism, and early terminology is partly reconstructed.",
      "narrative_implication": "Label the mechanism only when flows, persons, quotas, duration, seals or transfer conditions support it.",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0010"
      ]
    },
    {
      "id": "CLM-0018",
      "statement": "Co-occurrence between urban institutional growth and record systems establishes pressure and compatibility, not a one-way proof that either caused the other.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "counterevidence": "Later cases may demonstrate capacity effects, but those belong to WS06 and cannot be back-projected.",
      "narrative_implication": "Present the WS02 feedback loop as a hypothesis to be tested, not as a completed causal verdict.",
      "sources": [
        "SRC-0005",
        "SRC-0003",
        "SRC-0011"
      ]
    }
  ],
  "qualifications": [
    {
      "id": "CLM-0011",
      "constraint": "Use only with the stated confidence and boundary.",
      "counterevidence": "Continuity of individual non-numerical sign shapes is much less secure."
    },
    {
      "id": "CLM-0012",
      "constraint": "Use only with the stated confidence and boundary.",
      "counterevidence": "Some late simple tokens in bullae clearly served numerical/accounting functions."
    },
    {
      "id": "CLM-0013",
      "constraint": "Use only with the stated confidence and boundary.",
      "counterevidence": "Exact contribution of each component cannot be quantified."
    },
    {
      "id": "CLM-0014",
      "constraint": "Use only with the stated confidence and boundary.",
      "counterevidence": "Preserved earliest texts are overwhelmingly administrative, but corpus survival is selective."
    },
    {
      "id": "CLM-0015",
      "constraint": "Use only with the stated confidence and boundary.",
      "counterevidence": "Downstream effects require WS06 case studies; WS02 cannot establish them alone."
    },
    {
      "id": "CLM-0016",
      "constraint": "Use 'accounting/administrative transfer' unless reciprocity or institutional flow is independently demonstrated.",
      "counterevidence": "Named agents, commodities, metrology and document structure sometimes narrow the transaction, but sign readings and institutional context remain incomplete."
    },
    {
      "id": "CLM-0017",
      "constraint": "Label the mechanism only when flows, persons, quotas, duration, seals or transfer conditions support it.",
      "counterevidence": "A single tablet may participate in more than one mechanism, and early terminology is partly reconstructed."
    },
    {
      "id": "CLM-0018",
      "constraint": "Present the WS02 feedback loop as a hypothesis to be tested, not as a completed causal verdict.",
      "counterevidence": "Later cases may demonstrate capacity effects, but those belong to WS06 and cannot be back-projected."
    }
  ],
  "guardrails": [
    {
      "source": "outline.non_goal",
      "constraint": "Không invention scene; không ethnic attribution; không universal token code; không direct token→tablet genealogy; không biến administrative pressure thành monocause."
    }
  ],
  "excluded_claim_ids": [],
  "exclusion_rule": "Any substantive historical interpretation/generalization outside permitted_claims requires evidence-authority validation before narration.",
  "source_refs": [
    {
      "id": "SRC-0001",
      "title": "Proto-Cuneiform Account-Books and Journals",
      "author": "Robert K. Englund",
      "year": 2004,
      "type": "scholarly chapter / corpus synthesis",
      "authority": "Leading specialist synthesis grounded in the archaic tablet corpus and CDLI work.",
      "url": "https://cdli.earth/files-up/publications/englund2004a.pdf",
      "locators": [
        "pp. 24–27 (PDF pp. 2–5), especially chronology figure and discussion of Uruk IV/III corpus",
        "pp. 24–31",
        "pp. 28–31"
      ]
    },
    {
      "id": "SRC-0003",
      "title": "Writing in Early Mesopotamia: Beyond the Meme",
      "author": "Massimo Maiocchi",
      "year": 2019,
      "type": "peer-reviewed scholarly chapter",
      "authority": "Assyriological synthesis focused on early Mesopotamian writing, semiotics and material systems.",
      "url": "https://iris.unive.it/retrieve/e4239dde-83dd-7180-e053-3705fe0a3322/Maiocchi%20M.%202019%2C%20Writing%20in%20Early%20Mesopotamia%20--%20Beyond%20the%20Meme.pdf",
      "locators": [
        "pp. 410–412 (PDF pp. 15–17), especially discussion of glottographic/semasiographic boundary",
        "pp. 410–412"
      ]
    },
    {
      "id": "SRC-0005",
      "title": "Visible Language: Inventions of Writing in the Ancient Middle East and Beyond",
      "author": "Christopher Woods (ed.)",
      "year": 2010,
      "type": "academic museum catalogue / comparative synthesis",
      "authority": "University of Chicago Oriental Institute catalogue curated by a Sumerologist.",
      "url": "https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/oimp32.pdf",
      "locators": [
        "comparative chronology and essays on earliest Mesopotamian and Egyptian writing; catalogue overview",
        "pp. 33–50; development of accounting systems",
        "Mesopotamian writing essays"
      ]
    },
    {
      "id": "SRC-0009",
      "title": "Reconsidering ‘Tokens’",
      "author": "Lucy E. Bennison-Chapman, 2019",
      "type": "peer-reviewed article",
      "authority": "Systematic archaeological reassessment",
      "url": "https://www.cambridge.org/core/journals/cambridge-archaeological-journal/article/reconsidering-tokens-the-neolithic-origins-of-accounting-or-multifunctional-utilitarian-tools/7E6C04CB040AD8AA0EA84B94D4D275C4",
      "locators": [
        "abstract and pp. 233–259"
      ]
    },
    {
      "id": "SRC-0010",
      "title": "A Quantitative Analysis of Proto-Cuneiform Sign Use in Archaic Tribute",
      "author": "Logan Born and Kathryn Erin Kelley, 2021",
      "type": "peer-reviewed corpus study",
      "authority": "CDLI corpus-based quantitative analysis",
      "url": "https://cdli.earth/articles/cdlb/2021-6",
      "locators": [
        "§§1–3; corpus definition, sign-frequency and genre limits",
        "§§1–3; 6,726-artifact working corpus and sign-use method"
      ]
    },
    {
      "id": "SRC-0011",
      "title": "Cuneiform Script and the Origin of the Oldest Writing Systems in Comparative Perspective",
      "author": "Massimo Maiocchi, 2015",
      "type": "specialist institutional essay",
      "authority": "Institute for the Study of Ancient Cultures",
      "url": "https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/nn227.pdf",
      "locators": [
        "pp. 6–9; token frequency mismatch and multiple antecedent practices"
      ]
    }
  ],
  "retrieval_scope": {
    "claim_ids": [
      "CLM-0011",
      "CLM-0012",
      "CLM-0013",
      "CLM-0014",
      "CLM-0015",
      "CLM-0016",
      "CLM-0017",
      "CLM-0018"
    ],
    "source_ids": [
      "SRC-0001",
      "SRC-0003",
      "SRC-0005",
      "SRC-0009",
      "SRC-0010",
      "SRC-0011"
    ],
    "adapter": "scripts/draft_evidence.py",
    "rule": "Writer may increase source-level resolution inside these sources but may not silently expand the truth ceiling."
  },
  "writer_contract": "Permitted claims define a truth ceiling, not a required content list or narrative route. The writer may use any evidence-safe subset and any authored structure that reaches the section objective. Bounded evidence retrieval may add factual resolution from approved supporting sources; new claims, causal conclusions, contradictions or generalizations must return to research authority."
}
# END INPUT: 03_sections/P01/narration-pack.json

# BEGIN INPUT: 03_sections/P01/draft.md
# P01 — Trước chữ viết đã có một bài toán phải giải

Đừng bắt đầu lịch sử chữ viết bằng một tấm bảng. Hãy bắt đầu bằng một vật còn lạ hơn: một **bulla**. Đó là lớp vỏ đất sét khép quanh những vật nhỏ cũng bằng đất sét, thường được gọi là **token**. Một số token muộn trong bulla rõ ràng có liên quan đến số lượng và kế toán. Nhưng bulla tạo ra một nghịch lý. Khi lớp vỏ đóng lại, các token được gom vào một chỗ—và đồng thời biến khỏi tầm mắt. Muốn nhìn những gì ở trong, phải mở vật đang giữ chúng. Muốn giữ lớp vỏ nguyên vẹn, phải tìm cách đưa thông tin ra ngoài.

Trước câu chuyện về chữ, đã có bài toán vật chất ấy: làm sao giữ một lượng thông tin cho bền mà vẫn khiến nó có thể được sử dụng?

Bây giờ hãy đặt vật nhỏ này trở lại Uruk. Ở giai đoạn liên quan đến sự xuất hiện của chữ hình nêm sơ khai, khu đô thị ấy được ước tính rộng khoảng hai trăm hecta, với hơn bốn mươi nghìn cư dân. Cả hai con số chỉ là ước tính, nhưng quy mô mà chúng gợi ra thì rất rõ. Một lần đếm không còn đứng một mình. Nó nằm giữa nhiều lần chuyển giao, nhiều đối tượng được tính và nhiều hoạt động của các thiết chế.

Trong công việc kế toán, chuyển một lượng hàng mới chỉ là nửa việc. Lượng ấy còn phải có một hình thức để người ta có thể tiếp tục xử lý nó sau khi thao tác ban đầu đã kết thúc. Token cho lượng một hình thức vật chất: thay vì chỉ nói “bao nhiêu”, có những vật nhỏ hiện diện để mang việc đếm. Không phải mọi token thời đồ đá mới đều là một phần của cùng một mã kế toán kéo dài hàng thiên niên kỷ. Nhưng ở những trường hợp muộn đã được đặt trong bulla, chức năng số của một số token đủ rõ để ta theo tiếp đường đi của thông tin.

Đường đi ấy đổi hướng ngay trên lớp vỏ. Ở một số bulla, token được ấn lên phía ngoài; những vết ấn này tương ứng với các dấu số sớm. Bulla lúc đó mang hai cách giữ cùng một lượng: các vật nằm bên trong và dấu hiện ra trên bề mặt. Đây chưa phải một tấm bảng chữ hoàn chỉnh. Nhưng một thay đổi quan trọng đã xảy ra. Muốn biết lượng, người ta không còn nhất thiết chỉ nhìn vào tập vật được cất kín. Bề mặt đất sét cũng có thể làm lượng hiện diện.

Các bảng ghi số đưa khả năng đó đi xa hơn. Trên bảng, dấu số không chỉ gợi về những token đang nằm sau một lớp vỏ. Chính bề mặt trở thành nơi bản ghi tồn tại. Việc đếm vẫn là sợi dây nối chắc nhất giữa các thiết bị có trước chữ và những bảng proto-cuneiform: lượng đi qua nhiều vật mang tin, nhưng thực hành số vẫn có thể được nhận ra. Với các dấu không phải số, mối nối về hình dạng kém chắc chắn hơn nhiều.

Tuy vậy, đừng nghe chuỗi này như một niên biểu thẳng: token rồi bulla, bulla rồi bảng, bảng rồi chữ. Đó là một logic vật chất, không phải một hàng quân thay thế nhau. Tại Tushan, token còn tồn tại cùng các tài liệu viết. Một hình thức mới có thể xuất hiện mà hình thức cũ vẫn tiếp tục làm việc. Vì thế, token, bulla, con dấu, hình ảnh, bảng số và thực hành của các thiết chế nên được nhìn như một **hệ sinh thái ghi nhận**: nhiều giải pháp chồng lấn quanh cùng một bài toán, chứ không phải một phát minh đơn độc xóa sạch mọi thứ trước nó.

Nhìn theo cách đó, điều đáng nhớ không phải tên của từng vật mà là những động tác chúng cho phép. Token làm lượng có hình dạng. Bulla gom những vật mang lượng vào một đơn vị khép kín. Dấu ngoài vỏ đưa một phần thông tin ra bề mặt. Bảng số cho bề mặt tự mang bản ghi. Giữ, gom, niêm phong, đánh dấu: mỗi động tác sắp xếp lại quan hệ giữa lượng, vật và nơi thông tin có thể được tìm thấy.

Đây là nơi quy mô hành chính trở thành một áp lực lớn. Phần tư liệu proto-cuneiform còn bảo tồn được nghiêng mạnh về kế toán và hành chính. Nó cho ta nhận ra bối cảnh ghi nhận chắc hơn là cho phép gọi mọi bảng là trao đổi thị trường, thuế, cống nạp hay phân phối. Những cơ chế ấy không thể đổi tên cho nhau chỉ vì cùng có số và hàng hóa. Dù vậy, điểm chung vẫn hiện ra: các thiết chế đang vận hành cần những lượng có thể được giữ lại và tiếp tục xử lý.

Hành chính không vì thế trở thành nguyên nhân duy nhất của chữ viết. Corpus còn lại có tính chọn lọc, và việc đô thị, thiết chế cùng hệ thống ghi nhận phát triển bên nhau không chứng minh một mũi tên nhân quả một chiều. Cách hiểu hợp lý hơn là một khả năng phản hồi: thiết chế mở rộng tạo thêm áp lực cho hồ sơ; hồ sơ hữu dụng hơn lại có thể tăng năng lực của thiết chế. Đây là mô hình phù hợp với bằng chứng hiện có, không phải một phán quyết rằng ta đã định lượng xong đóng góp của từng thành phần.

Giờ ta có thể trả lời câu hỏi mở đầu. Những dấu bền trên đất sét trở nên hữu ích vì chúng chuyển lượng từ chỗ chỉ được mang bởi vật rời hoặc giấu trong một lớp vỏ sang một bề mặt có thể làm việc như hồ sơ. Ở quy mô Uruk, sự chuyển chỗ ấy gặp đúng áp lực của những hoạt động tổ chức đang mở rộng. Độ bền giúp thông tin còn hiện diện; bề mặt giúp thông tin có thể được tiếp cận; còn quy mô khiến hai khả năng đó đáng để đầu tư.

Câu trả lời ngắn có thể nhớ là: **quy mô tạo nhu cầu, bề mặt làm lượng nhìn thấy, và độ bền giúp công việc tiếp tục.**

Nhưng nhu cầu cùng các thực hành ghi nhận chưa tự động tạo ra một hệ thống dấu mới. Nếu token, bulla, con dấu và bảng số đã cùng góp mặt, điều gì khiến hệ thống dấu mới thực sự khác trước? Đó là câu hỏi tiếp theo.
# END INPUT: 03_sections/P01/draft.md
