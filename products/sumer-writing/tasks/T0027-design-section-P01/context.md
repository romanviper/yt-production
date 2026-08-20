# Context Packet — T0027-design-section-P01

- Product: `sumer-writing`
- Operation: `design_section`
- Context profile: `creative_design`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/story-plan.json`, `tasks/T0027-design-section-P01/report.md`, `tasks/T0027-design-section-P01/operator-brief.json`

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

The narrator is calm, clear, weighty and investigative. Their default relationship to the audience is guide and companion, not lecturer. Let the audience encounter concrete evidence, action, consequence or change before supplying interpretation when the material genuinely permits it.

Audience agency must be real rather than staged: do not call specialist classifications or decoded categories "what we can already see" unless a non-specialist can actually perceive the relevant cue without that expertise. When expert interpretation is necessary, provide it plainly and then let the audience follow what changes because of it.

Start concrete, widen only when a mechanism needs explanation, then return to what that mechanism allows or costs people. Prefer causality to chronology, consequence to trivia and ordinary Vietnamese to abstract terminology. Emotional weight comes from evidenced consequences, not rhetorical intensity.

The identity is stable; its expression remains adaptive. The Agent chooses local structure, pace and phrasing from the material instead of filling a house style formula.
# END INSTRUCTION: system/standards/channel-constitution.md

# BEGIN INSTRUCTION: system/operations/design-section.md
# Operation — Design Section

## Responsibility

Turn the section brief and evidence pool into a compact design decision. Do not write narration or pre-script the writer's route.

`story-plan.json` records the audience shift, concise strategy, evidence roles (`core`, `optional`, `guardrail`, `exclude`), recommended length with rationale, and optional risks. Partition every claim exactly once; selection defines the evidence ceiling, not a demand that every selected claim be spoken.

Use an evidenced carrier when useful; an event chain is not mandatory.

## Audience-readable evidence

For audience inference, distinguish:

`evidence present → evidence perceivable → evidence interpretable`

Ask viewers to discover only raw cues a non-specialist can notice without first receiving the specialist classification that makes them meaningful. If “quantity”, “grain” or another expert category must be supplied first, present it as narrator clarification, not independent audience observation.

Do not manufacture agency from processed scholarship.

Describe strategy or tension without prescribing numbered beats, paragraph count, cadence, compulsory opening device or miniature payoff formula. If the required shift needs pseudo-agency, lecture or unsupported claims, report the blocker and its layer.

Status remains `draft`. Only the user approves the plan.
# END INSTRUCTION: system/operations/design-section.md

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

# BEGIN INPUT: 03_sections/P01/section.json
{
  "schema_version": 2,
  "id": "P01",
  "title": "Một mảnh đất sét không chịu nói",
  "order": 1,
  "status": "story_plan_changes_requested",
  "human_approved": false,
  "dependencies": [],
  "narrative_job": "Cold-open P005390. Trong 20–30 giây phải có micro-reveal đủ cụ thể để viewer biết mình đang nhìn một paradox thật; full reveal trong 60–90 giây/~140–210 từ trước chronology/definition. Sau đó chuyển ngay sang câu hỏi earned: nếu tablet chưa trao lại full speech, tại sao loại relation này vẫn đáng giữ qua thời gian?",
  "entry_state": "Khán giả coi tablet như thông điệp chỉ cần dịch.",
  "exit_state": "Khán giả biết cái gì còn/mất và giữ một câu hỏi đơn giản: loại memory này giải quyết điều gì mà trí nhớ của người có mặt không giải quyết được?",
  "target_words": {
    "min": 500,
    "max": 800
  },
  "cycle_id": "C002",
  "movement_ids": [
    "M01"
  ],
  "macro_movements": [
    {
      "id": "M01",
      "title": "Một tablet còn dấu nhưng không còn giọng nói",
      "narrative_job": "P005390 phải trả micro-reveal trong 20–30 giây và full reveal trong 60–90 giây/~140–210 từ: quantity/layout/relation còn, nhưng full sentence/language/transaction chắc chắn thì không. Viewer được giải một phần mystery ngay, rồi mystery đổi dạng: nếu đây chưa phải speech đầy đủ, tại sao nó vẫn đáng tạo ra và giữ lại?",
      "entry_state": "Mọi dấu trên clay có thể bị mặc định là câu chữ trực tiếp từ Sumer.",
      "exit_state": "Mystery đổi từ 'nó nói gì?' sang 'một record chưa nói trọn câu có thể giải quyết vấn đề gì tốt hơn trí nhớ người?'."
    }
  ],
  "acts": [
    {
      "id": "A01",
      "role": "opening",
      "title": "Một vật thể chưa chịu kể chuyện"
    }
  ]
}
# END INPUT: 03_sections/P01/section.json

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

# BEGIN INPUT: 03_sections/P01/evidence-pack.json
{
  "schema_version": 1,
  "section": "P01",
  "claims": [
    {
      "id": "CLM-0024",
      "statement": "Proto-cuneiform sign distribution and tablet position can reveal structural regularities even when a sign's spoken value or underlying language remains uncertain.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0010"
      ],
      "counterevidence": "Corpus readability, sign variants and genre classification affect frequency and positional analysis.",
      "narrative_implication": "Separate observable graphic pattern from modern decipherment and language attribution.",
      "provenance": [
        {
          "workstream": "WS03",
          "local_id": "WS03-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0042",
      "statement": "P005390/MMA 1988.433.2 is a physical Uruk III administrative tablet recording grain-related quantities; its language and exact transaction remain uncertain.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0023",
        "SRC-0024"
      ],
      "counterevidence": "CDLI and the Met use overlapping but different date labels, and both qualify the Uruk provenience; missing verbs prevent a fully secure reading of deliveries versus distributions.",
      "narrative_implication": "Use as a representative preserved administrative form, not as a quoted individual voice or proof of a specific economic institution.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-009"
        }
      ]
    }
  ],
  "sources": [
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
      ],
      "status": "reviewed",
      "limitations": [
        "Catalogue compresses specialist disagreements for comparative presentation; use for comparison scope, not exact Uruk stratigraphy.",
        "Comparative overview; some pathways remain hypothetical.",
        "Catalogue compresses disagreements."
      ],
      "notes": [
        "Treats Mesopotamia and Egypt as roughly contemporary independent inventions; supports avoiding an unqualified unique 'world first' claim.",
        "Selected for this workstream's bounded question."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-005"
        },
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-001"
        },
        {
          "workstream": "WS03",
          "local_id": "WS03-SRC-002"
        }
      ]
    },
    {
      "id": "SRC-0010",
      "title": "A Quantitative Analysis of Proto-Cuneiform Sign Use in Archaic Tribute",
      "author": "Logan Born and Kathryn Erin Kelley, 2021",
      "year": null,
      "type": "peer-reviewed corpus study",
      "authority": "CDLI corpus-based quantitative analysis",
      "url": "https://cdli.earth/articles/cdlb/2021-6",
      "locators": [
        "§§1–3; corpus definition, sign-frequency and genre limits",
        "§§1–3; 6,726-artifact working corpus and sign-use method"
      ],
      "status": "reviewed",
      "limitations": [
        "Sign-frequency patterns do not by themselves establish sign meanings or causal direction.",
        "Readability, sign variants, genre assignment and corpus growth constrain quantitative conclusions."
      ],
      "notes": [
        "Used to test how far administrative subgenres can be distinguished from the preserved corpus.",
        "Used to separate observed sign distribution from reconstructed linguistic value."
      ],
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-005"
        },
        {
          "workstream": "WS03",
          "local_id": "WS03-SRC-005"
        }
      ]
    },
    {
      "id": "SRC-0023",
      "title": "MSVO 3, 79 artifact entry (P005390)",
      "author": "Cuneiform Digital Library Initiative; transliterations by Robert K. Englund, Jacob L. Dahl and CDLI",
      "year": null,
      "type": "primary artifact record and corpus transliteration",
      "authority": "CDLI object-level record linked to the Metropolitan Museum of Art",
      "url": "https://cdli.earth/P005390",
      "locators": [
        "CDLI P005390; MMA 1988.433.2",
        "Text: obverse columns 1–2 and reverse columns 1–2",
        "Edition references: MSVO 3 no. 79; Frühe Schrift no. 4.79; CTMMA IV no. 180"
      ],
      "status": "reviewed",
      "limitations": [
        "CDLI labels Uruk provenience uncertain and dates the tablet to Uruk III ca. 3200–3000 BCE; the Met uses Jemdet Nasr ca. 3100–2900 BCE. Language is undetermined and the document lacks verbs, limiting transaction-level interpretation."
      ],
      "notes": [
        "Selected administrative object. Contemporary ancient tablet, not a later copy; use as an early economic-classification case, not a transparent voice."
      ],
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-SRC-006"
        }
      ]
    },
    {
      "id": "SRC-0024",
      "title": "Cuneiform tablet: administrative account concerning the distribution of barley and emmer",
      "author": "Metropolitan Museum of Art",
      "year": null,
      "type": "museum object record",
      "authority": "Holding-institution record for MMA 1988.433.2",
      "url": "https://www.metmuseum.org/art/collection/search/327384",
      "locators": [
        "Object no. 1988.433.2",
        "Object overview and artwork details",
        "Open Access/Public Domain image flag"
      ],
      "status": "reviewed",
      "limitations": [
        "The museum gives 'probably from Uruk' and a broad interpretive description; acquisition rather than excavation context means exact provenience is uncertain."
      ],
      "notes": [
        "Rights anchor for the selected administrative object: Met object images are marked Public Domain; credit the museum and object number."
      ],
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-SRC-007"
        }
      ]
    }
  ],
  "rule": "Only claims in this pack may appear as substantive historical claims in the draft."
}
# END INPUT: 03_sections/P01/evidence-pack.json

# BEGIN INPUT: 03_sections/P01/continuity-in.md
# Continuity Input — P01

Dependencies: Không có.

## Prior handoff

Chưa có hoặc sẽ được task owner cập nhật trước drafting.

## Canonical terms required here

Tham chiếu story bible.
# END INPUT: 03_sections/P01/continuity-in.md

# BEGIN INPUT: 03_sections/P01/story-plan-change-request.md
# Story Plan Rework — P01

Requested by: user

Requested at: 2026-08-18T09:19:42.541135+00:00

## Request

Rework thiết kế P01 đứng trước T0026 để audience agency là evidence-readable: phân biệt raw cue mà non-specialist thực sự có thể nhận thấy với expert classification; không trình bày quantity hoặc grain như điều khán giả tự quan sát trước narrator clarification. Giữ P005390 làm carrier, giữ evidence ceiling hiện tại, entry/exit state và câu hỏi earned.
# END INPUT: 03_sections/P01/story-plan-change-request.md
