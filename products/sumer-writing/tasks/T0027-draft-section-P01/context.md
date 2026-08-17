# Context Packet — T0027-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0027-draft-section-P01/report.md`, `tasks/T0027-draft-section-P01/operator-brief.json`

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

Every script has three clear audience-facing acts, whether it lasts 30 minutes or three hours:

- **Opening:** begin with a concrete object, person, action or situation; establish the central tension and the promise of the journey without resolving it immediately.
- **Body:** follow causal change through formation, expansion, conflict, consequence and adaptation. Each movement changes the state of the story.
- **Ending:** answer the central question, trace the final consequence or legacy, and reconnect it to the opening tension.

These acts belong to the whole script. A production section is only a bounded work unit and must not repeat opening–body–ending as a miniature template.

## Voice

The narrator is calm, clear, weighty and investigative. Start concrete, widen only when a mechanism needs explanation, then return to what that mechanism allows or costs people. Prefer causality to chronology, consequence to trivia and ordinary Vietnamese to abstract terminology. Emotional weight comes from evidenced consequences, not rhetorical intensity.

The identity is stable; its expression remains adaptive. The Agent chooses local structure, pace and phrasing from the material instead of filling a house style formula.
# END INSTRUCTION: system/standards/channel-constitution.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Responsibility

Write one section that produces the approved audience shift and advances its assigned act and movement.

Treat the story plan as intent and evidence selection, not as a route that must be reproduced. Choose the opening form, ordering, paragraph count, rhythm and transitions that work best for the material.

Use core evidence as the anchor. Optional evidence appears only when the listener needs it. Guardrails constrain wording without becoming exposition; excluded claims remain out. Keep the approved entry/exit state and continuity handoff.

The length range is a planning estimate, not a quota. Never repeat an idea, add a fact or stretch a sentence to reach its minimum. The only hard size boundary is the production-unit cap. If the section needs a materially different scope, explain the mismatch in the report so it can be routed to design.

Write natural spoken Vietnamese and a compact handoff. Do not review or approve your own draft.
# END INSTRUCTION: system/operations/draft-section.md

# BEGIN INPUT: 02_outline/story-bible.md
# Story Bible — Sumer Writing C002

Status: approved

## Central causal spine

Phim kiểm nghiệm mệnh đề “chữ viết tạo ra văn minh” thay vì dùng nó làm premise. Câu trả lời được phép là **đồng phát triển rồi phản hồi theo từng giai đoạn**: các thiết chế quy mô lớn tạo áp lực ổn định quantity, category, person và obligation; nhiều thực hành clay, seal, numerical và visual được kết hợp thành proto-cuneiform; khi record được nhúng vào trained communities, authentication, archive, retrieval và authority, nó có thể tăng một số năng lực phối hợp. Năng lực tăng lại tạo thêm nhu cầu record.

Tác nhân xuyên suốt không phải một tablet, một language hay một ethnic population. Nó là thực hành có thể tái tạo: biến một số quan hệ thành dấu bền, chuẩn hóa và có thể truy hồi, rồi duy trì người đủ năng lực để tạo, đọc, sao chép và hành động theo chúng.

Viewer-facing question đơn giản hơn internal causal model: **chữ viết có tự tạo ra sức mạnh của xã hội Sumer, hay chỉ trở thành power khi cả một social system khiến dấu được hiểu và biến thành action?**

## Retention spine

Phim không dùng hook formula cho từng section. Retention phải đến từ một chuỗi câu hỏi được **kiếm ra từ câu trả lời trước**:

1. **P01:** Tablet còn dấu nhưng không trao full speech — vậy tại sao loại record này vẫn hữu ích?
2. **P02:** Nhiều partial solutions giải từng phần của memory/verification problem — chuyện gì xảy ra khi relation được gom lên một surface?
3. **P03:** Nếu language còn uncertain, làm sao ta vẫn biết system đang làm việc? Viewer phải tự suy ra function từ layout/quantity/category trước khi nghe definition.
4. **P04:** Capability mở rộng bằng cách nào, và mỗi bước mở rộng tạo maintenance cost gì?
5. **P05:** Ai trả cost đó? Sau khi thấy training/practice, viewer được dẫn tới assumption rằng competent writing + authority hẳn phải tạo action.
6. **P06:** MMA 86.11.111 phá assumption bằng một written order không được thi hành. Câu hỏi earned duy nhất: **thiếu mắt xích nào?**
7. **P07:** Rebuild answer từng mắt xích qua record/action cases; chỉ sau khi chain hoạt động mới reveal asymmetric visibility.
8. **P08:** Nếu chain sống nhờ competent practice, nó có survive khi language setting đổi không? Akkadian adaptation được kể như mismatch→adaptation→survival.
9. **P09:** Nếu survival phụ thuộc competence, điều gì xảy ra khi competent readers biến mất? Decipherment là competence reconstruction; P005390 khóa final payoff.

Mỗi section chỉ nên giữ **một dominant viewer question**. Không mở ba mystery song song. Không kết bằng “nhưng câu chuyện chưa dừng ở đó”; transition phải sinh từ limitation, failure hoặc consequence vừa được chứng minh.

## Competitive narrative discipline

- **Reward before explanation:** Opening có micro-reveal trong 20–30 giây và full reveal trong 60–90 giây. Ở các section sau, object/action/consequence phải land trước definition hoặc qualifier.
- **Human/material carrier:** một đoạn explanation dài phải được mang bởi object, thao tác, role hoặc consequence có evidence. “Human” không đòi invented character.
- **Event/state-change density:** carrier chỉ tạo concreteness; propulsion cần trước–sau. P03 là puzzle có changed interpretation; P04 có hai problem-solution transformations; P05 có work/correction; P06 có failure; P07 có chain reconstruction; P08 có mismatch/adaptation; P09 có break/recovery.
- **Abstraction ceiling:** không chồng threshold → chronology → language → ethnicity → world-first hoặc classification → archive → authority. Concept mới chỉ mở sau khi viewer đã nhận reward từ vật/action trước.
- **Earned open loops:** câu hỏi kế tiếp phải được tạo bởi limitation của câu trả lời hiện tại, không bằng withholding giả.
- **Emotional accumulation:** emotional weight đến từ consequence được chứng minh—effort để học, người bị biến thành category, command thất bại, clay còn mà readers biến mất—không từ invented scene hay hyperbole.

## Three-act state change

### Opening — Một vật thể chưa chịu kể chuyện

P005390 cho thấy material survival không đồng nghĩa transparent speech. Reward đầu tiên phải đến rất sớm: viewer biết đây không phải một “message chỉ cần dịch”. Full reveal trong 60–90 giây chuyển mystery từ *nó nói gì?* sang *một record chưa phải full speech giải quyết điều gì tốt hơn trí nhớ người?*

P02 chỉ đưa token, seal, bulla và numerical devices vào qua pressure→action→limitation. Act kết khi viewer thấy nhiều partial solutions cùng xử lý một family of problems và muốn biết chúng tạo capability mới ra sao khi relation được ổn định trên tablet.

### Body — Khi dấu hiệu trở thành năng lực tổ chức

P03 không mở bằng definition. Nó là một puzzle: từ layout, quantity và category, viewer phải thấy system hữu ích trước khi narrator giải thích ngưỡng writing, chronology hay language uncertainty.

P04 chỉ dùng hai technical transformations. Mỗi transformation đi **old limitation → sign/material operation → mechanism → new capability → new cost**. Cost đó đẩy thẳng sang P05.

P05 dùng P228744/House F để complexity hiện thành work: copying, calculation, lexical organization và correction. Section không trở thành history of education; payoff là continuity phải được tái tạo qua trained practice. Cuối P05 seed assumption: nếu competent people có record đúng, written authority hẳn phải có force.

**P06** là midpoint/body reversal. MMA 86.11.111 được theo đủ lâu để viewer kỳ vọng order sẽ thành action rồi chứng kiến failure. Không giải chain ngay; chỉ khóa câu hỏi “thiếu mắt xích nào giữa inscription và action?”

**P07** trả lời đúng câu hỏi đó bằng 2–3 bounded Ur III/later record/action cases. Authentication, archive/retrieval/aggregation và authority chỉ xuất hiện khi một case cụ thể chứng minh function. Sau khi chain đã work mới mở consequence kép: capacity tăng, nhưng visibility bị phân phối không đối xứng.

### Ending — Đất sét còn lại sau khi người đọc biến mất

P08 kể **Akkadian adaptation như survival test**. Một tradition hình thành trong một language setting gặp mismatch khi phải làm việc trong setting khác; simple substitution không đủ, nên sign values và conventions phải đổi. Hittite chỉ là contrast; curricula chỉ giải thích infrastructure của competent reuse.

P09 mở trên competence brink với latest-known dated tablet 75 CE, rồi cho reproduction ecosystem co lại. Decipherment không phải scholar-hero arc mà là chuỗi competence reconstruction: copy signs, compare multilingual evidence, test readings. Mỗi bước trả lại một phần capacity đã mất. Return P005390 là ending duy nhất.

## Chronology guardrails

- Uruk IV: khoảng 3350/3300–3200 BCE; Uruk III/Jemdet Nasr: khoảng 3200–3000 BCE. Giữ qualifier và ưu tiên relative sequence.
- Không dùng Ur III capacity evidence làm bằng chứng trực tiếp cho mechanism ở Uruk; luôn đánh dấu chronological gap.
- Formal curriculum có context tốt nhất ở later household/institutional settings, đặc biệt Old Babylonian; không chiếu ngược edubba thống nhất.
- Akkadian adaptation là primary survival case; không biến Hittite hoặc later multilingual use thành civilization tour song song.
- Tablet năm 75 CE là latest currently known dated tablet, không phải final act chắc chắn.
- Modern recovery xảy ra sau competence break; recovery-mediated legacy không phải direct transmission.

## Term discipline

- **Writing:** ngưỡng phân tích có cấp độ; conventional durable marks mang linguistic/lexical values. Devices chỉ truyền quantity/meaning mà chưa chứng minh language encoding được gọi accounting/proto-writing.
- **Proto-cuneiform:** hệ Uruk IV–III phần lớn incised, sparse phonology, language chưa chắc; tránh gọi toàn bộ là mature cuneiform.
- **Cuneiform:** logo-syllabic tradition có semantic và phonological values, không phải một stage tự nhiên hướng đến alphabet.
- Tách **script**, **language**, **population label**, **professional title**, **functional competence**, **literacy**, **institution**.

## Evidence anchors

- P005390/MMA 1988.433.2: opening object và running material reference; grain-related quantities, exact transaction/language uncertain.
- P228744 và House F: bounded evidence cho lexical training/curriculum ở Old Babylonian Nippur; human carrier cho cost của complexity.
- MMA 86.11.111: written royal security order không được thi hành; body reversal trước khi giải thích conditional capacity.
- Ur III Umma và Puzriš-Dagan: bounded tests cho classification, aggregation, audit, archive và asymmetric visibility; không back-project về Uruk.
- Akkadian adaptation: primary case cho việc cuneiform đổi sign values/orthographic conventions để sống trong language setting khác.
- Hittite: contrast cho selective transfer, không phải second tour.
- Behistun/comparative decipherment: recovery là chuỗi tích lũy, không phải một eureka moment.
- ETCSL 3.1.19: later composite textual tradition, không phải contemporary Ur III dispatch; chỉ dùng nếu section design thực sự cần.

## Setup/payoff continuity

- Setup: tablet có dấu nhưng không trao một voice rõ. Early payoff: nó vẫn giữ structured relations; final payoff: clay chỉ nói lại khi social knowledge được phục dựng.
- Setup: partial solutions giải memory/verification pressure. Payoff: tablet recombine relation thành capacity mới nhưng không tự biến thành speech hay power.
- Setup: complexity mở rộng capability. Payoff: complexity trở thành labor của trained people.
- Setup: competent record có vẻ đồng nghĩa authority. Payoff: P06 phá assumption; P07 rebuild conditional power.
- Setup: system chưa encode language trọn vẹn. Payoff: survival đến từ khả năng đổi language và convention, không từ purity.
- Setup: archive làm quá khứ visible. Payoff: visibility luôn bị định hình bởi category, discard, excavation và provenance.
- Setup: clay bền. Payoff: material survival không bảo đảm survival of competence.

## Global exclusions

- Không nói “ethnic Sumerians invented writing in 3200 BCE” hoặc uncontested world-first.
- Không kể token → tablet → civilization như đường thẳng; không dùng writing như autonomous cause của state hay enforcement.
- Không đồng nhất market, tax, tribute, redistribution, labor coordination, obligation và ownership.
- Không suy ra literacy rate, universal male-only access, everyday experience hoặc whole-population compliance.
- Không dùng archive như mẫu trung tính của society.
- Không direct-quote translation chưa rights-cleared; ưu tiên attributed paraphrase và Met objects đã thuận lợi hơn về rights.
- Không thêm invented character, dialogue, interiority hoặc sensory scene chỉ để tăng “human feel”.
- Không nối Sumer trực tiếp đến database, smartphone hay modern writing; resemblance chỉ là analogy nếu được dùng.
# END INPUT: 02_outline/story-bible.md

# BEGIN INPUT: 02_outline/voice-profile.md
# Voice Profile — Sumer Writing C002

Status: approved

## Product voice

Giọng kể bình tĩnh, sáng rõ và có sức nặng của một cuộc điều tra. Narrator không đứng ngoài đọc kết luận; viewer được dẫn qua **question → evidence → changed interpretation**. Một thời điểm chỉ giữ một dominant question. Câu hỏi kế tiếp phải sinh từ limitation, failure hoặc consequence vừa land, không dùng cliffhanger giả.

Mỗi lần mở rộng khái niệm phải bắt đầu hoặc nhanh chóng trở về một **carrier có provenance**: vật thể, thao tác, role hoặc consequence. Carrier tạo concreteness; để tạo propulsion, đoạn kể còn cần state change—một puzzle được giải, capability xuất hiện, expectation bị phá, chain được rebuild hoặc competence biến mất rồi được phục dựng.

Câu tiếng Việt ưu tiên động từ nhân quả cụ thể: “ổn định”, “phân loại”, “xác thực”, “truy hồi”, “đào tạo”, “thi hành”. Thuật ngữ Anh chỉ giữ khi bản dịch dễ làm mất ranh giới; lần đầu phải giải thích bằng lời Việt thông thường.

## Borrowed functions

Từ các benchmark lớn chỉ học causal macro arc, material anchor, primary-text presence, event/action propulsion, circular callback và khả năng chuyển nhịp giữa người–vật–institution. Không học cadence, persona hay chapter sequence. Retention phải đến từ **earned curiosity**: câu trả lời hiện tại tạo ra vấn đề kế tiếp.

## Original expression

Trục riêng của product là khoảng cách giữa **dấu bền** và **năng lực xã hội khiến dấu có nghĩa**. P005390 cho micro-reward rất sớm rồi đổi mystery; P03 cho viewer tự suy ra function trước definition; P05 biến complexity thành work; P06 phá assumption record=compliance; P07 rebuild power từng mắt xích; P08 biến adaptation thành survival problem; P09 quay lại opening sau competence break.

Nhịp câu linh hoạt: câu ngắn khóa reveal/state change, câu dài hơn chỉ khi nối mechanism đã có carrier. Sau một đoạn abstraction, phải trả lại object/action/consequence trước khi mở abstraction mới.

## Prohibited imitation

Không dùng motif ruins-in-the-present, cadence, chapter order, narrator persona, signature transition hay wording của *Fall of Civilizations* hoặc kênh tham chiếu khác. Không thêm dialogue, nội tâm, sensory scene hay certainty không có nguồn. Không dùng “nhưng mọi chuyện chưa dừng ở đó”, “điều họ không biết là…” hoặc withholding fact đã biết để giả tạo suspense. Toàn phim có opening–body–ending; từng P## không tự dựng mini-hook–explanation–payoff công thức.

## Draft tests

- Trong mỗi đoạn, có thể trả lời ngay: viewer đang muốn biết **một câu gì**?
- Câu hỏi kế tiếp có được sinh ra từ answer/limitation trước, hay chỉ là teaser gắn thêm?
- Reward chính của đoạn đã land trước definition/qualifier chưa?
- Mỗi stretch abstraction có carrier; mỗi section dài có ít nhất một state-changing action/event/puzzle.
- P03–P05 không trở thành lecture valley; P06 được giữ đủ space như midpoint reversal; P07 trả đúng câu hỏi “missing link”.
- Script, language, population, competence, literacy và institution không bị trộn.
- Qualifier rõ nhưng không tạo disclaimer pile.
- Human texture không vượt evidence ceiling và không biến thành invented drama.
- Không có câu nào có thể bị nhầm là mô phỏng bề mặt của benchmark.
# END INPUT: 02_outline/voice-profile.md

# BEGIN INPUT: 03_sections/P01/brief.md
# P01 — Một mảnh đất sét không chịu nói

## Whole-script acts

- opening — Một vật thể chưa chịu kể chuyện

## Macro movements

- M01 — Một tablet còn dấu nhưng không còn giọng nói

## Narrative job

Cold-open P005390. Trong 20–30 giây phải có micro-reveal đủ cụ thể để viewer biết mình đang nhìn một paradox thật; full reveal trong 60–90 giây/~140–210 từ trước chronology/definition. Sau đó chuyển ngay sang câu hỏi earned: nếu tablet chưa trao lại full speech, tại sao loại relation này vẫn đáng giữ qua thời gian?

## Entry state

Khán giả coi tablet như thông điệp chỉ cần dịch.

## Exit state

Khán giả biết cái gì còn/mất và giữ một câu hỏi đơn giản: loại memory này giải quyết điều gì mà trí nhớ của người có mặt không giải quyết được?

## Anchor options

Không có.

## Continuity in

Không có.

## Continuity out

Không có.

## Non-goal

Không tuyên bố language/transaction/world-first; không trì hoãn reward đầu tiên tới cuối phút đầu; không rời object sang exposition dài ngay sau reveal; không tạo mystery bằng cách giấu fact đã biết.
# END INPUT: 03_sections/P01/brief.md

# BEGIN INPUT: 03_sections/P01/story-plan.json
{
  "schema_version": 3,
  "section": "P01",
  "status": "approved",
  "audience_shift": "Khán giả bắt đầu với giả định rằng một tablet cổ là một thông điệp chỉ cần được dịch. Cuối P01, họ nhận ra điều lạ hơn: ngay cả khi không thể khôi phục một câu nói hoàn chỉnh, ta vẫn có thể thấy tablet đang giữ những quantity và relation có cấu trúc. Câu hỏi vì thế đổi từ ‘nó nói gì?’ sang ‘tại sao việc làm cho những relation như vậy tồn tại ngoài trí nhớ lại hữu ích?’",
  "story_strategy": "Giữ P005390 làm carrier duy nhất của opening. Trả reward sớm bằng điều có thể quan sát: quantity, repetition, arrangement và grain-related signs cho thấy tablet đang giữ một relation có cấu trúc ngay cả khi ta chưa thể đọc nó như một câu hoàn chỉnh. Sau đó mới mở contradiction: vật thể vẫn giữ được một phần structure nhưng không trao lại chắc chắn underlying language, exact transaction hay một lời nói trọn vẹn. Không biến uncertainty thành disclaimer; mỗi giới hạn chỉ xuất hiện sau một điều viewer vừa hiểu được. Không mở rộng sang world-first, nguồn gốc chữ viết, chronology dài hay tranh luận định nghĩa. Kết section bằng câu hỏi earned: nếu một tablet không cần giữ lại trọn một câu nói mà vẫn giữ được một phần relation, tại sao con người lại cần làm cho những relation đó tồn tại ngoài trí nhớ?",
  "word_budget": {
    "recommended": {
      "min": 500,
      "max": 800
    },
    "rationale": "Đủ để object và reveal land sớm, làm rõ giới hạn diễn giải rồi chuyển câu hỏi sang P02 mà không biến opening thành exposition."
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
    "Biến uncertainty về language và transaction thành disclaimer pile.",
    "Nói quá mức rằng tablet ghi một giao dịch cụ thể hoặc một câu hoàn chỉnh.",
    "Rời P005390 quá sớm để giảng chronology, nguồn gốc chữ viết hoặc world-first.",
    "Giữ mystery quá lâu thay vì trả micro-reveal ngay trong opening.",
    "Mở đầu bằng provenance, tuổi hoặc archaeology quá lâu trước khi viewer nhận được observable clue đầu tiên."
  ],
  "approved_by": "user",
  "approved_at": "2026-08-17T15:30:00+07:00"
}
# END INPUT: 03_sections/P01/story-plan.json

# BEGIN INPUT: 03_sections/P01/narration-pack.json
{
  "schema_version": 2,
  "section": "P01",
  "created_at": "2026-08-17T08:30:00+00:00",
  "story_plan_sha256": "5c284d694c6ba475c6f2070c4324d9c20a486a517d6da8f9eff9252597988b90",
  "evidence_pack_sha256": "8b29ea363f9db3db2f30b9f38095c150cf2a26ee7196a499baf43d9832bd16a3",
  "core_claims": [
    {
      "id": "CLM-0042",
      "statement": "P005390/MMA 1988.433.2 is a physical Uruk III administrative tablet recording grain-related quantities; its language and exact transaction remain uncertain.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "counterevidence": "CDLI and the Met use overlapping but different date labels, and both qualify the Uruk provenience; missing verbs prevent a fully secure reading of deliveries versus distributions.",
      "narrative_implication": "Use as a representative preserved administrative form, not as a quoted individual voice or proof of a specific economic institution.",
      "sources": [
        "SRC-0023",
        "SRC-0024"
      ]
    },
    {
      "id": "CLM-0024",
      "statement": "Proto-cuneiform sign distribution and tablet position can reveal structural regularities even when a sign's spoken value or underlying language remains uncertain.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "counterevidence": "Corpus readability, sign variants and genre classification affect frequency and positional analysis.",
      "narrative_implication": "Separate observable graphic pattern from modern decipherment and language attribution.",
      "sources": [
        "SRC-0005",
        "SRC-0010"
      ]
    }
  ],
  "optional_claims": [],
  "guardrails": [],
  "excluded_claim_ids": [],
  "source_refs": [
    {
      "id": "SRC-0005",
      "title": "Visible Language: Inventions of Writing in the Ancient Middle East and Beyond",
      "author": "Christopher Woods (ed.)",
      "year": 2010,
      "locators": [
        "comparative chronology and essays on earliest Mesopotamian and Egyptian writing; catalogue overview",
        "pp. 33–50; development of accounting systems",
        "Mesopotamian writing essays"
      ]
    },
    {
      "id": "SRC-0010",
      "title": "A Quantitative Analysis of Proto-Cuneiform Sign Use in Archaic Tribute",
      "author": "Logan Born and Kathryn Erin Kelley, 2021",
      "locators": [
        "§§1–3; corpus definition, sign-frequency and genre limits",
        "§§1–3; 6,726-artifact working corpus and sign-use method"
      ]
    },
    {
      "id": "SRC-0023",
      "title": "MSVO 3, 79 artifact entry (P005390)",
      "author": "Cuneiform Digital Library Initiative; transliterations by Robert K. Englund, Jacob L. Dahl and CDLI",
      "locators": [
        "CDLI P005390; MMA 1988.433.2",
        "Text: obverse columns 1–2 and reverse columns 1–2",
        "Edition references: MSVO 3 no. 79; Frühe Schrift no. 4.79; CTMMA IV no. 180"
      ]
    },
    {
      "id": "SRC-0024",
      "title": "Cuneiform tablet: administrative account concerning the distribution of barley and emmer",
      "author": "Metropolitan Museum of Art",
      "locators": [
        "Object no. 1988.433.2",
        "Object overview and artwork details",
        "Open Access/Public Domain image flag"
      ]
    }
  ],
  "writer_contract": "Core claims are anchors, not mandatory paragraphs. Optional claims appear only when needed. Guardrails constrain wording without becoming exposition. Excluded claims stay out."
}
# END INPUT: 03_sections/P01/narration-pack.json

# BEGIN INPUT: 03_sections/P01/continuity-in.md
# Continuity Input — P01

Dependencies: Không có.

## Prior handoff

Chưa có hoặc sẽ được task owner cập nhật trước drafting.

## Canonical terms required here

Tham chiếu story bible.
# END INPUT: 03_sections/P01/continuity-in.md
