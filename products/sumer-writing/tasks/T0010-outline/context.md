# Context Packet — T0010-outline

- Product: `sumer-writing`
- Operation: `outline`
- Section: `-`
- Unit: `-`
- Allowed writes: `02_outline/outline.json`, `02_outline/story-bible.md`, `tasks/T0010-outline/report.md`, `tasks/T0010-outline/operator-brief.json`

## Acceptance criteria

- Outline có đúng số section đã chọn và ID ổn định.
- Mỗi section có một narrative job, state change, claim set và word budget.
- Tổng arc trả North Star và khác biệt rõ với benchmark.
- Story bible đủ continuity nhưng nằm trong giới hạn compact.

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Only the material inside this packet is task context. Do not scan the repository.

# BEGIN INSTRUCTION: system/core/invariants.md
# Core Invariants

Các luật này có hiệu lực với mọi operation.

1. Một task chỉ thực hiện một operation và một target chính.
2. Chỉ đọc input trong context packet; không “đọc thêm cho chắc” bằng cách quét repo.
3. Chỉ sửa `allowed_write_paths`.
4. Không tự đặt artifact thành `approved`.
5. Không đưa claim chưa support vào narration như fact.
6. Không bịa scene, suy nghĩ, hội thoại hoặc chi tiết giác quan.
7. Không sao chép cách diễn đạt/cadence/structure đặc trưng của creator tham chiếu.
8. Nếu input mâu thuẫn, stale, thiếu hoặc vượt context budget: dừng và báo blocker.
9. Output phải hoàn thành contract hiện tại; không chủ động chạy operation kế tiếp.
10. Delivery là build artifact; source of truth nằm ở artifact module.
11. Product operation có authority `product_agent`: không được sửa control plane hoặc protected system paths.
12. Khi product task phát hiện lỗi hệ thống, chỉ báo cáo blocker và escalation; không tự sửa.
13. Architecture task và product-content task không được trộn trong cùng commit.

## Artifact boundary

- Research tạo evidence, không tạo narration.
- Outline tạo section contracts, không tạo prose.
- Draft tạo prose một section, không review/approve.
- Review tạo diagnosis, không rewrite.
- Revision sửa đúng issue đã duyệt, không “polish toàn bộ”.
- Integration tìm dependency conflict qua handoff trước, không tái sinh script.
# END INSTRUCTION: system/core/invariants.md

# BEGIN INSTRUCTION: system/standards/channel.md
# Channel Standard

## North Star đã khóa

> Trong những hệ thống, thiết chế, công nghệ và ý niệm đã tạo nên nền một nền văn minh, thành phần nào có quá trình hình thành, phát triển, mở rộng, tạo ra hệ quả và xung đột, rồi biến đổi, suy yếu hoặc để lại di sản đủ rõ ràng để tự nó trở thành trục chính của một câu chuyện lịch sử có tính điện ảnh?

Subject phải cho phép kiểm tra phần lớn chuỗi:

`pressure → formation → adoption → expansion → consequence/conflict → transformation/decline → legacy`

Đây là diagnostic, không phải chapter formula.

Promise ưu tiên:

`recognizable object + specific causal tension → broad mental-map delivery`

Không dùng “entire history/explained” hoặc universal stakes để che một product thiếu causal question.
# END INSTRUCTION: system/standards/channel.md

# BEGIN INSTRUCTION: system/standards/evidence.md
# Evidence Standard

## Claim protocol

`claim → falsification criterion → evidence hierarchy → contradiction → classification → narrative use`

Claim được phân loại `fact`, `inference`, `contested`, `unknown`; trạng thái `open`, `supported`, `qualified`, `rejected`, `blocked`.

## Hierarchy

1. Primary evidence/corpus/artefact có provenance.
2. Scholarly monograph, chapter, paper, handbook, catalogue.
3. Expert interpretation xác định được chuyên môn.
4. University/museum/academic encyclopedia.
5. Documentary, podcast, báo, blog và video: discovery, không tự gánh claim trụ cột.

Source `reviewed` phải có locator và note về giới hạn. Link không đồng nghĩa đã đọc.

## Historical restraint

- Bất đồng học thuật phải được lưu dưới `counterevidence`/`alternatives`.
- Không chọn giả thuyết vì cinematic hơn.
- Không biến absence of evidence thành evidence of absence.
- “First”, “oldest”, “invented”, “caused” luôn cần definition và comparison scope.
- Direct quote cần source, locator, translation attribution và rights flag.
# END INSTRUCTION: system/standards/evidence.md

# BEGIN INSTRUCTION: system/standards/story.md
# Story Standard

## Causal spine

Story phải giải thích pressure nào tạo mechanism mới; mechanism đổi capacity/incentive của ai; hệ quả và adaptation nào biến state A thành B.

Mỗi section contract có:

- một narrative job;
- entry/exit state;
- central question/payoff;
- claim IDs;
- material/human anchor có provenance;
- dependencies và bridge;
- word budget;
- boundary: điều cố ý chưa giải thích.

## Long-form rhythm

Luân phiên có chủ đích:

`human/object → institution → system → human consequence`

Entity được giới thiệu theo `FUNCTION → NAME → thuộc tính cần cho hành động kế tiếp`.

Opening thiết lập object, causal tension, stakes và boundary. Ending trả causal question và legacy có mắt xích; không chỉ recap hay “bài học lịch sử” chung chung.
# END INSTRUCTION: system/standards/story.md

# BEGIN INSTRUCTION: system/operations/outline.md
# Operation — Outline

## Responsibility

Biến research synthesis thành outline nhiều phần và story bible compact. Không viết narration.

## `outline.json`

Mỗi section gồm:

- `id` dạng `P##`, title làm việc và order;
- narrative job duy nhất;
- entry/exit state;
- `question` và `payoff` là hai field riêng;
- claim IDs và dependencies;
- anchor requirements;
- bridge in/out;
- target word range;
- boundary và risk.

Outline phải có status `draft` cho tới khi người dùng approve.
`section_count` phải bằng đúng số section thực tế. Contract này được dùng chung bởi validator, approval và materializer.

## `story-bible.md`

Chỉ giữ premise, causal spine, global chronology, canonical terminology, central entities, thematic rule, setup/payoff map và global exclusions. Không nhét research notes vào story bible.
# END INSTRUCTION: system/operations/outline.md

# BEGIN INSTRUCTION: system/standards/operator-interface.md
# Operator Interface Standard

Cuộc trò chuyện là bảng điều khiển cho người ra quyết định. Mục tiêu không phải luôn nói ngắn, mà dùng đúng độ sâu với đúng mục đích.

## Hai lớp thông tin

- **Operator brief:** kết luận ngắn giúp người dùng hiểu trạng thái và quyết định.
- **Task report trong repo:** phân tích đầy đủ, provenance, issue list, validation, file scope và chi tiết kỹ thuật.

Repo giữ chiều sâu. Chat mở lượng thông tin cần cho ý định hiện tại; không mặc định sao chép task report vào chat.

## Chọn response mode theo ý định

Agent tự chọn mode; người dùng không cần nhớ câu lệnh kỹ thuật.

### 1. Brief mode

Dùng cho status, task handoff, blocker, checkpoint và approval decision.

- Tối đa 140 từ, không tính nội dung người dùng yêu cầu trích nguyên văn.
- Kết luận nằm ở câu đầu tiên.
- Tối đa ba `material_points`, xếp theo mức ảnh hưởng.
- Chỉ nêu điều làm thay đổi approval, scope, evidence readiness, chất lượng, rủi ro lớn hoặc bước kế tiếp.
- Không kể đã đọc file nào, chạy lệnh gì, suy luận qua bước nào hoặc đã tuân thủ những điều hiển nhiên nào.
- Không liệt kê file path, hash, test và command khi chúng đều bình thường. Lưu chúng trong `report.md`.
- Không lặp lại cùng một nhận xét dưới nhiều heading.
- Dùng tiếng Việt tự nhiên; chỉ giữ ID như `WS02`, `P04`, `ISSUE-01` khi chúng giúp người dùng chỉ định đối tượng.

Mọi blocker thật phải xuất hiện. Nếu có quá ba vấn đề quan trọng, nhóm chúng thành tối đa ba quyết định hoặc nhóm rủi ro; không giấu blocker để đạt giới hạn từ.

### 2. Guided explanation mode

Dùng khi người dùng hỏi `tại sao`, `như thế nào`, muốn hiểu concept, so sánh phương án hoặc cần được dẫn qua một quyết định phức tạp.

- Mở đầu bằng kết luận hoặc mental model ngắn.
- Sau đó giải thích vừa đủ để người dùng hiểu quan hệ nhân quả và trade-off.
- Không có trần 140 từ, nhưng dừng khi câu hỏi đã được giải quyết; không biến thành audit nếu người dùng không yêu cầu.

### 3. Deep review mode

Dùng khi người dùng yêu cầu `mở chi tiết`, `evidence`, `audit đầy đủ`, phản biện sâu hoặc kiểm tra toàn diện.

- Bắt đầu bằng executive summary để người dùng vẫn có bức tranh tổng quát.
- Chi tiết được nhóm theo câu hỏi/decision, không theo nhật ký Agent đã làm gì.
- Nêu evidence, uncertainty và issue đầy đủ đến mức cần thiết; độ dài do nhiệm vụ quyết định.

### 4. Deliverable mode

Dùng khi người dùng yêu cầu xem chính sản phẩm như outline, draft, bảng claim hoặc bản sửa.

- Operator brief là lớp đầu.
- Sau đó hiển thị hoặc liên kết đúng artifact được yêu cầu; độ dài artifact không bị tính vào giới hạn brief.
- Không thay artifact bằng một bản tóm tắt nếu người dùng cần kiểm duyệt nội dung thật.

Nếu ý định chưa rõ, bắt đầu bằng brief. Chỉ hỏi lại khi lựa chọn mode hoặc độ sâu sẽ làm thay đổi đáng kể công việc.

## Phân loại đúng mức

- **Blocker:** ngăn operation hiện tại hoặc operation kế tiếp chạy hợp lệ.
- **Material risk:** chưa chặn nhưng có thể làm người dùng đổi quyết định.
- **Detail:** hữu ích cho người thực thi nhưng không thay đổi quyết định; chỉ nằm trong report.

Không gọi một cải tiến nhỏ là blocker. Không đưa detail vào chat chỉ để chứng minh Agent đã làm nhiều việc.

## Khi cần người dùng quyết định

Brief phải có:

1. khuyến nghị rõ ràng;
2. đúng một câu hỏi quyết định hiện tại;
3. tối đa ba lựa chọn, mỗi lựa chọn nói ngắn gọn hiệu lực nếu được chọn.

Không gộp các quyết định thuộc giai đoạn sau. Không tự approve và không trình bày command nội bộ như một lựa chọn cho người dùng.

## Progressive disclosure

Mặc định đưa bức tranh tổng quát trước. Mở reasoning, evidence hoặc artifact khi người dùng yêu cầu hoặc khi thiếu chúng sẽ khiến một quyết định trở nên không an toàn. Brevity không được dùng để che uncertainty, trade-off hoặc blocker.

## Task completion

Mỗi task ghi cả:

- `report.md`: hồ sơ kỹ thuật đầy đủ;
- `operator-brief.json`: dữ liệu ngắn dùng để render câu trả lời cuối.

Sau khi submit, dùng output của `python scripts/task.py brief products/<slug> <task-id>` làm lớp đầu của câu trả lời. Chỉ nối thêm explanation, deep review hoặc deliverable khi ý định người dùng yêu cầu; không nối thêm process diary.
# END INSTRUCTION: system/standards/operator-interface.md

# BEGIN INPUT: 00_brief/product-brief.md
# Product Brief — Chữ viết Sumer

Status: direction approved by user on 2026-08-12.

## Locked direction

- Đây là sản phẩm đầu tiên theo North Star mới của kênh.
- Subject là câu chuyện về chữ viết trong nền văn minh Sumer.
- *Fall of Civilizations* là benchmark/đối thủ tham chiếu, không phải template để sao chép.
- Kịch bản dự kiến dài 1–2 giờ và được tạo, review, sửa theo module.
- Research xác định historical mechanism và boundary; không quyết định lại subject.

## Product question

> Một hệ thống ghi dấu xuất hiện trong những cộng đồng ngày càng phức tạp ở miền nam Mesopotamia đã hình thành, mở rộng chức năng, tái phân phối năng lực xã hội, biến đổi qua các ngôn ngữ và thiết chế, rồi để lại di sản lâu hơn thế giới tạo ra nó như thế nào?

Đây là research frame, không phải verdict. Mọi causal verb phải được evidence kiểm tra.

## In scope

- Điều kiện và information practices trước/sát thời điểm writing hình thành.
- Medium, sign system, language, function và community of practice.
- Hệ quả đối với quản trị, trao đổi, quyền lực, ký ức và tri thức khi có bằng chứng.
- Adaptation, persistence, decline và legacy của các truyền thống liên quan.

## Out of scope

- Tổng sử chính trị Sumer nếu không phục vụ causal chain của writing.
- Catalogue vua, thành bang, thần thoại hoặc thành tựu.
- Đường tiến bộ tất định từ pictograph tới alphabet hiện đại.
- “Sumer invented writing” hoặc “writing created civilization” như premise fact chưa kiểm chứng.

## Known risks

- Nhầm Sumerian language, population label, proto-cuneiform và cuneiform.
- Monocausal administration story.
- Token → tablet → phonetic writing như đường thẳng tất định.
- Survival bias của clay archives.
- Presentism về literacy, bureaucracy, author và ownership.
- Legacy bằng analogy thay vì transmission chain.

## Target

- Ngôn ngữ: tiếng Việt.
- Thời lượng: 60–120 phút.
- Section count dự kiến cho pilot: 10, được outline quyết định và người dùng duyệt.
# END INPUT: 00_brief/product-brief.md

# BEGIN INPUT: 00_brief/benchmark.md
# Benchmark — Sumer Writing

Status: orientation, audited 2026-08-12.

## Direct adjacent competitor

**Fall of Civilizations, Episode 8: “The Sumerians — Fall of the First Cities”**

- Duration được công bố: 2 giờ 29 phút.
- Promise: đi từ nguồn gốc bí ẩn và những thành phố đầu tiên tới sự sụp đổ của nền văn minh Sumer.
- Experience signals: ruins/rediscovery opening, myths, proverbs, voice actors và recreated music.
- Episode này đã bao phủ writing như một thành tựu nằm trong tổng sử Sumer.

Sources:

- [YouTube episode](https://www.youtube.com/watch?v=d2lJUOv0hLA)
- [Apple Podcasts listing and duration](https://podcasts.apple.com/ee/podcast/8-the-sumerians-fall-of-the-first-cities/id1449884495?i=1000454904678)
- [Official recommended reading page](https://fallofcivilizationspodcast.com/recommended-reading/)

## Không gian khác biệt cần bảo vệ

Sản phẩm này không cạnh tranh bằng việc kể lại nhiều thông tin hơn về Sumer. Nó đổi historical object:

| FoC episode | Pilot này |
|---|---|
| một civilization | một công nghệ–thiết chế |
| rise and fall của Sumer | formation → adoption → expansion → consequence/conflict → transformation → legacy của writing |
| writing là một thành tựu trong arc lớn | writing là causal object được điều tra |
| payoff là sự sụp đổ/impermanence | payoff dự kiến là thứ có thể sống lâu hơn xã hội tạo ra nó |

## Benchmark attributes được phép học

- Causal macro arc dễ hiểu trong thời lượng dài.
- Material/sensory anchor có provenance.
- Primary voices và văn bản cổ như evidence lẫn human presence.
- Chuyển nhịp giữa đời sống thường ngày, thiết chế và biến đổi hệ thống.
- Thừa nhận uncertainty và giới hạn source.
- Emotional weight đến từ evidence, không từ hyperbole.

## Những thứ không được sao chép

- Wording, cadence và motif “ruins in the present” như công thức bắt buộc.
- Chapter order hoặc sequence của episode Sumer.
- Giọng narrator, câu chuyển và cách dàn dựng đặc trưng.
- Claim “invented writing” chỉ vì benchmark đã dùng trong description năm 2019.
# END INPUT: 00_brief/benchmark.md

# BEGIN INPUT: 01_research/research-synthesis.md
# Global Research Synthesis — Sumer Writing

Status: ready_for_review

## Central answer

Writing did not create Sumerian civilization in a single causal act. A more defensible model is **co-development followed by feedback**: late-fourth-millennium institutions in southern Mesopotamia generated pressure to stabilize quantities, categories, persons and obligations; several clay, sealing, numerical and visual practices were combined into proto-cuneiform; once records became embedded in trained communities, authentication, retrieval and enforcement, they increased what institutions could coordinate across time, space and personnel. That increased capacity generated further demand for records.

The object that supplies continuity is therefore not one fixed script, language or tablet form. It is a **reproducible practice of turning selected relations into durable, standardized and retrievable marks**, maintained by communities that knew how to create, interpret, copy and act on them.

This model rejects three shortcuts: “ethnic Sumerians invented writing in 3200 BCE”; token → tablet → civilization as a linear ladder; and writing as an autonomous force that commanded labor or created the state.

## Proposed causal spine

### 1. A problem of scale selects for durable records

Before proto-cuneiform, numerical objects, bullae, seals, metrological conventions and images already handled parts of accounting and authentication. The strongest continuity is numerical, but the devices formed a parallel ecology rather than one universal token code.

As urban and institutional operations expanded, memory held in persons, gestures and local encounters became less sufficient for some tasks. The preserved Uruk IV–III corpus is overwhelmingly administrative, supporting administration as a major selection pressure. It does not by itself distinguish market exchange from redistribution, labor coordination, tax, tribute, obligation or ownership; each mechanism requires different evidence.

### 2. The first system is powerful precisely because it is incomplete

Uruk IV proto-cuneiform, approximately 3350/3300–3200 BCE, can stabilize quantities, commodities, offices and structured relations, often through tablet layout as much as language. Whether it already counts as “writing” depends on the declared threshold. Phonology is sparse, the underlying language is uncertain and the earliest marks are largely incised rather than mature wedges.

Uruk/southern Mesopotamian attribution is strong. Direct attribution to Sumerian language is low-to-medium and ethnic attribution is unsupported. Egypt overlaps chronologically, so “one of the earliest independently developed traditions” is safer than “the world’s first.”

### 3. Technical capacity and social use diverge

Across the third millennium, impressed wedge ductus, logo-syllabic values and more explicit language encoding expanded what cuneiform could express. This was not a march toward the alphabet. Nor did every technically possible use immediately become routine.

Functions accumulated and recombined: administration remained; lexical organization, letters, legal and normative documents, literature, cult and political memory expanded in different places and periods. Four bounded anchors can make this visible without becoming a genre catalogue: P005390 for early administrative classification; MMA 86.11.111 for a documentary report whose written order was not implemented; P228744 for lexical schooling; and ETCSL 3.1.19 for later copies transforming royal correspondence into political/literary memory.

### 4. Specialists turn marks into infrastructure

Earliest scribes are visible mainly through their products. Later contexts, especially Old Babylonian households and institutions, reveal training through copying, calculation, lexical lists and genre conventions. “Edubba” cannot be projected backward as a uniform temple-school, and modern mass-literacy categories do not fit.

The infrastructure is a chain: tablet affordance → trained writer/reader → seal, witness or convention → archive and retrieval → institution capable of acting. Break a link and a record may document a command without producing compliance.

### 5. Embedded records enlarge capacity and redistribute visibility

Ur III Umma and Puzriš-Dagan provide later, bounded evidence for the return arrow in the feedback loop. Classifications, equivalencies, responsible officials, seals and archives allowed institutions to aggregate labor, reconcile accounts and make obligations retrievable. Some later private actors also gained documentary leverage.

The distribution was asymmetric. Officials gained an aggregate view; workers and dependents became legible through imposed categories. Yet oral negotiation, household practice, embodied expertise and much exchange remained outside surviving archives. Archives are organizational residues shaped by clay durability, discard, excavation and the antiquities market—not neutral samples of society.

### 6. Survival comes from adaptation, not purity

Cuneiform spread through courts, specialists, diplomacy, apprenticeship, copying and lexical/bilingual curricula. It survived by changing sign values and orthographic conventions for Akkadian, Hittite and other languages. Script, language and institution followed different timelines: Sumerian could persist as learned content after probable vernacular decline while cuneiform encoded other languages.

The true unit of survival was the trained community capable of competent reuse. Old tablets alone do not constitute a living tradition.

### 7. The tradition contracts, breaks and is recovered

Cuneiform declined over centuries as language competition, political economy, temple contraction and the cost of specialist training narrowed its ecosystem. The tablet dated 75 CE is the latest currently known, not a proven final act. When institutional reproduction ceased, clay survived but competence did not.

Nineteenth-century recovery proceeded cumulatively through copied signs, Old Persian, Behistun, comparative testing of Akkadian and later reconstruction of Sumerian. This break defines the defensible legacy: modern access to ancient societies is recovery-mediated. Direct transmission must be proven case by case; parallels with databases are analogy, not lineage.

## Claim decisions for outline use

- **Supported spine:** administrative/institutional pressure was central; writing and institutions co-developed; procedural records later enlarged bounded capacities; trained communities enabled expansion and transmission; decline was multicausal; modern recovery followed a competence break.
- **Must remain qualified:** the writing threshold; absolute dates; earliest underlying language; strength and direction of the early feedback loop; literacy/access scale; regional timing of spoken Sumerian decline; the final date of competence.
- **Reject as premise facts:** ethnic Sumerians invented writing in a single year; an uncontested Mesopotamian world-first; a universal token genealogy; writing alone created the state or enforced law; archives represent the whole population; direct Sumer-to-modern-writing lineage.

## Contradictions retained

1. **Definition:** strict language encoding versus broader conventional lexical recording.
2. **Formation:** strong numerical continuity versus rejection of a universal token ladder.
3. **Causation:** writing as record of complexity versus writing as capacity multiplier; evidence supports a phase-bound feedback loop, not one timeless answer.
4. **Access:** restricted specialist practice versus later non-professional/private appropriation; no population rate follows.
5. **Continuity:** script, language and institution survive differently.
6. **Legacy:** living transmission ends before modern decipherment; recovery is not direct lineage.

## Open decisions before outline

1. **Framing of the title question.** Recommended: treat “created civilization” as the proposition to test and replace it with co-development/feedback in the payoff, not as a fact announced at the start.
2. **Chronological architecture.** Recommended: use a lifecycle with recurring causal returns—pressure → encoding → institutional embedding → expansion → adaptation → contraction/recovery—rather than eight workstream chapters.
3. **Human anchors.** The four WS05 cases are evidence-ready, but the outline must decide which two or three carry narrative weight. Rights currently favor the two Met objects; Penn imagery and direct ETCSL/CTMMA quotation remain uncleared.
4. **Opening/ending pair.** Strong candidate: open on an early tablet whose meaning is constrained and end with a once-readable tradition becoming mute, then recovered. The 75 CE tablet is a compelling late anchor but its latest-known status must stay explicit.

## Gaps that may block or constrain outline

- **No blocker to constructing a causal outline.**
- A precise claim about the proportion of administrative versus other early tablets would require a current corpus-count audit; use qualitative “overwhelmingly administrative” meanwhile.
- Claims about everyday experience, literacy rates, gender distribution or population-wide compliance remain unavailable and must not become section premises.
- Direct quotation and visual use for Penn/CDLI/ETCSL/CTMMA materials require production-stage rights checks; attributed paraphrase and cleared Met images are currently safer.
- If the outline wants a direct bridge from the Uruk origin horizon to Ur III capacity effects, it must mark the chronological gap and present later archives as tests of a possible return mechanism, not proof of what happened at Uruk.
# END INPUT: 01_research/research-synthesis.md

# BEGIN INPUT: 01_research/claim-ledger.json
{
  "schema_version": 1,
  "product": "sumer-writing",
  "status": "complete",
  "claims": [
    {
      "id": "CLM-0001",
      "statement": "For this project, 'writing' should be treated as a graded analytical threshold: durable conventional marks that encode repeatable linguistic or lexical values count as writing, while devices that communicate quantities or meanings without demonstrable language encoding remain accounting/proto-writing; proto-cuneiform lies across this disputed boundary.",
      "type": "contested",
      "confidence": "medium",
      "status": "qualified",
      "sources": [
        "SRC-0003",
        "SRC-0004",
        "SRC-0005"
      ],
      "counterevidence": "A strict glottographic definition excludes much earliest proto-cuneiform; broader functional definitions include it because it records words/categories and develops directly into cuneiform.",
      "narrative_implication": "Never let one definition silently decide who invented writing or its exact birthday.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0002",
      "statement": "The earliest substantial proto-cuneiform horizon is conventionally placed near the end of the Late Uruk period, approximately 3350/3300–3200 BCE (Uruk IV), followed by Uruk III/Jemdet Nasr approximately 3200–3000 BCE.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0001",
        "SRC-0002",
        "SRC-0008"
      ],
      "counterevidence": "Absolute ranges vary among chronologies, and poor excavation records prevent a precise first year; a slightly earlier date cannot be excluded.",
      "narrative_implication": "Use ranges and archaeological phases, never a single invention year.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0003",
      "statement": "Uruk IVa is the most probable context for the oldest script at Uruk, but the original find documentation is too weak to make the stratigraphic placement definitive.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0002"
      ],
      "counterevidence": "No corrective reconstruction can fully repair the deficient find-spot and architectural documentation.",
      "narrative_implication": "The uncertainty is archaeological, not merely rhetorical caution.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0004",
      "statement": "The earliest Uruk IV corpus known to scholarship is overwhelmingly administrative; lexical texts become materially more visible in Uruk III.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0001"
      ],
      "counterevidence": "Survival and excavation bias mean the preserved corpus cannot prove that no other uses or media existed.",
      "narrative_implication": "Early evidence supports an administrative center of gravity, not the claim that administration was the only origin or use.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0005",
      "statement": "Calling the earliest system 'cuneiform' is potentially anachronistic: proto-cuneiform signs were initially drawn/incised and only later acquired the systematic wedge-impressed form associated with mature cuneiform.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0003",
        "SRC-0004"
      ],
      "counterevidence": "Scholarly convention uses proto-cuneiform to name the ancestral system, so the term remains useful when explicitly qualified.",
      "narrative_implication": "Distinguish proto-cuneiform from later wedge-shaped cuneiform in terminology and visuals.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-005"
        }
      ]
    },
    {
      "id": "CLM-0006",
      "statement": "The language underlying Uruk IV–III proto-cuneiform cannot be securely identified as Sumerian because the texts encode little phonology and can often be interpreted without recovering continuous speech.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0003",
        "SRC-0004"
      ],
      "counterevidence": "Some rare rebus/phonetic readings may fit Sumerian, and the later descendant script unquestionably writes Sumerian; this makes Sumerian plausible but not demonstrated for the earliest horizon.",
      "narrative_implication": "Do not convert 'found in southern Mesopotamia/Uruk' into 'written by ethnic Sumerians in Sumerian'.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0007",
      "statement": "The safest attribution is regional and institutional: proto-cuneiform is first securely attested as a large corpus in the Uruk cultural sphere of southern Mesopotamia, especially Uruk, rather than securely attributable to a named ethnic population.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0001",
        "SRC-0002",
        "SRC-0004",
        "SRC-0007"
      ],
      "counterevidence": "Uruk's corpus dominance may partly reflect excavation and preservation; related early practices are attested beyond Uruk and transmitted toward Susiana/Iran.",
      "narrative_implication": "Use 'Uruk/southern Mesopotamian tradition' for the earliest phase; reserve 'Sumerian writing' for contexts with linguistic evidence.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0008",
      "statement": "An unqualified claim that Sumer or Uruk produced the world's first writing is not defensible, because early Egyptian writing at Abydos overlaps the late-fourth-millennium date range and priority depends on calibration and definition.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0006"
      ],
      "counterevidence": "Uruk provides one of the earliest and by far the largest early corpora and may precede Egyptian material under some chronologies; neither establishes a universally accepted single winner.",
      "narrative_implication": "Claim 'one of the earliest independently developed writing traditions' or 'earliest large writing corpus', not an uncontested world first.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-008"
        }
      ]
    },
    {
      "id": "CLM-0009",
      "statement": "The relative sequence Uruk IV proto-cuneiform → Uruk III proto-cuneiform → later language-explicit cuneiform is much more secure than the absolute dates or a sharp boundary between proto-writing and writing.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0001",
        "SRC-0002",
        "SRC-0003",
        "SRC-0007"
      ],
      "counterevidence": "Local corpora and cross-regional contacts complicate a single linear sequence, and the exact transition to language-explicit writing is gradual.",
      "narrative_implication": "Organize chronology by states and transitions rather than invention moments.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-009"
        }
      ]
    },
    {
      "id": "CLM-0010",
      "statement": "The claim 'Sumer invented writing' should remain rejected as a premise fact but retained as a researchable shorthand whose components—place, system, language, population and priority—must be tested separately.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0002",
        "SRC-0004",
        "SRC-0005",
        "SRC-0006"
      ],
      "counterevidence": "Public and some scholarly summaries still use 'Sumerian invention' because the later continuity into Sumerian cuneiform is strong and convenient.",
      "narrative_implication": "The central narrative payoff can emerge from dismantling and rebuilding this familiar sentence with precise qualifiers.",
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-CLM-010"
        }
      ]
    },
    {
      "id": "CLM-0011",
      "statement": "Numerical systems provide the strongest material continuity between pre-writing devices and proto-cuneiform.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ],
      "counterevidence": "Continuity of individual non-numerical sign shapes is much less secure.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0012",
      "statement": "Neolithic clay objects called tokens were multifunctional; their existence does not prove a millennia-long standardized accounting code.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0009"
      ],
      "counterevidence": "Some late simple tokens in bullae clearly served numerical/accounting functions.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0013",
      "statement": "The direct token→tablet→writing sequence is too linear; seals, iconography, bullae, numerical tablets and institutional practice formed a parallel ecology.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0009",
        "SRC-0003"
      ],
      "counterevidence": "Exact contribution of each component cannot be quantified.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0014",
      "statement": "Administrative scale is a major formation pressure but not evidence that administration was the sole cause of writing.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ],
      "counterevidence": "Preserved earliest texts are overwhelmingly administrative, but corpus survival is selective.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0015",
      "statement": "The evidence supports a feedback model: expanding institutions demanded records, and better records could expand institutional capacity.",
      "type": "inference",
      "confidence": "medium",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ],
      "counterevidence": "Downstream effects require WS06 case studies; WS02 cannot establish them alone.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-005"
        }
      ]
    },
    {
      "id": "CLM-0016",
      "statement": "The preserved proto-cuneiform corpus can distinguish accounting contexts more securely than it can distinguish market exchange from tax, tribute or redistribution.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0001",
        "SRC-0010"
      ],
      "counterevidence": "Named agents, commodities, metrology and document structure sometimes narrow the transaction, but sign readings and institutional context remain incomplete.",
      "narrative_implication": "Use 'accounting/administrative transfer' unless reciprocity or institutional flow is independently demonstrated.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0017",
      "statement": "Redistribution, labor coordination, obligation and ownership are not interchangeable formation mechanisms: each requires different evidence beyond the presence of numbers and commodities.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0010"
      ],
      "counterevidence": "A single tablet may participate in more than one mechanism, and early terminology is partly reconstructed.",
      "narrative_implication": "Label the mechanism only when flows, persons, quotas, duration, seals or transfer conditions support it.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0018",
      "statement": "Co-occurrence between urban institutional growth and record systems establishes pressure and compatibility, not a one-way proof that either caused the other.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0003",
        "SRC-0011"
      ],
      "counterevidence": "Later cases may demonstrate capacity effects, but those belong to WS06 and cannot be back-projected.",
      "narrative_implication": "Present the WS02 feedback loop as a hypothesis to be tested, not as a completed causal verdict.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-008"
        }
      ]
    },
    {
      "id": "CLM-0019",
      "statement": "Proto-cuneiform and mature cuneiform differ in ductus: early signs were largely drawn, while wedge impressions became systematic later.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0004",
        "SRC-0005"
      ],
      "counterevidence": "The ancestral system is conventionally still called proto-cuneiform.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS03",
          "local_id": "WS03-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0020",
      "statement": "Tablet cases, subcases and spatial organization carried relations that later writing could encode more linguistically.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005"
      ],
      "counterevidence": "Layout conventions varied and do not map cleanly to spoken syntax.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS03",
          "local_id": "WS03-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0021",
      "statement": "Rare rebus/phonetic uses appear early, but consistent phonetic writing becomes evident mainly in the third millennium BCE.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0004",
        "SRC-0005"
      ],
      "counterevidence": "Dating and identification of individual early phonetic examples remain debated.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS03",
          "local_id": "WS03-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0022",
      "statement": "Cuneiform developed as a logo-syllabic system with semantic and phonological values, not as a stage naturally progressing toward alphabetic writing.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0004",
        "SRC-0013"
      ],
      "counterevidence": "Later alphabetic cuneiform at Ugarit is a separate adaptation, not the endpoint of Sumerian evolution.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS03",
          "local_id": "WS03-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0023",
      "statement": "Changes in metrology and sign standardization were pragmatic adaptations, not uniform replacement of old systems.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0012"
      ],
      "counterevidence": "Corpus gaps prevent a complete state-by-state reconstruction.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS03",
          "local_id": "WS03-CLM-005"
        }
      ]
    },
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
      "id": "CLM-0025",
      "statement": "A system's technical capacity to encode a relation is not evidence that communities used it consistently for that purpose.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0004",
        "SRC-0005",
        "SRC-0012",
        "SRC-0010"
      ],
      "counterevidence": "Repeated attested examples can establish use for a bounded corpus and period.",
      "narrative_implication": "Route claims about actual economic, legal, literary or pedagogical uptake to WS05.",
      "provenance": [
        {
          "workstream": "WS03",
          "local_id": "WS03-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0026",
      "statement": "The earliest writing implies trained specialists, but their identities, recruitment and institutional status are poorly recoverable.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0016"
      ],
      "counterevidence": "Lists and handwriting variation provide indirect evidence, not biographies.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS04",
          "local_id": "WS04-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0027",
      "statement": "The best archaeological evidence for formal curricula comes from later household and institutional contexts, especially the Old Babylonian period.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0014",
        "SRC-0015",
        "SRC-0016"
      ],
      "counterevidence": "Later evidence cannot be projected unchanged onto Uruk.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS04",
          "local_id": "WS04-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0028",
      "statement": "Edubba was not necessarily a single standardized temple-run school system across Mesopotamian history.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0014",
        "SRC-0015"
      ],
      "counterevidence": "Literary school texts use institutional language, but excavated teaching often occurs in houses.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS04",
          "local_id": "WS04-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0029",
      "statement": "Scribal competence included copying, calculation, lexical knowledge and genre conventions, not merely decoding signs.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0014",
        "SRC-0016",
        "SRC-0017"
      ],
      "counterevidence": "Curriculum differed by period, place and career path.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS04",
          "local_id": "WS04-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0030",
      "statement": "Access was restricted and socially consequential, but no reliable percentage for literacy or a universal male-only rule can be derived.",
      "type": "unknown",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0014",
        "SRC-0015"
      ],
      "counterevidence": "Named female scribes and elite women exist in some periods; corpus is not population-representative.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS04",
          "local_id": "WS04-CLM-005"
        }
      ]
    },
    {
      "id": "CLM-0031",
      "statement": "House F at Old Babylonian Nippur provides an unusually contextualized household training sequence, not proof of a universal Mesopotamian school system.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0018"
      ],
      "counterevidence": "Its more than 1,400 tablets make the sequence unusually rich but also locally exceptional.",
      "narrative_implication": "Use House F as an illustrative, high-resolution anchor explicitly labeled non-representative of all periods.",
      "provenance": [
        {
          "workstream": "WS04",
          "local_id": "WS04-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0032",
      "statement": "Professional title, functional competence and broad literacy must be mapped separately; some later archives show on-the-job or non-professional use outside a single formal school track.",
      "type": "inference",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0017",
        "SRC-0019"
      ],
      "counterevidence": "Survival still favors administrative settings and trained writers.",
      "narrative_implication": "Describe capabilities and work roles instead of assigning a modern literate/illiterate binary.",
      "provenance": [
        {
          "workstream": "WS04",
          "local_id": "WS04-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0033",
      "statement": "Named women and female-authored or female-voiced texts demonstrate access in some settings but cannot establish population rates or unmediated authorship.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0020"
      ],
      "counterevidence": "Scribal mediation, elite selection and uneven survival complicate attribution.",
      "narrative_implication": "Use specific women only with period, role, mediation and representativeness labels.",
      "provenance": [
        {
          "workstream": "WS04",
          "local_id": "WS04-CLM-008"
        }
      ]
    },
    {
      "id": "CLM-0034",
      "statement": "Uruk IV evidence is overwhelmingly administrative, while lexical texts become substantially more visible in Uruk III.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0001"
      ],
      "counterevidence": "Preservation and excavation bias prevent exclusivity claims.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0035",
      "statement": "By the middle third millennium BCE cuneiform served economic, religious, political, literary and scholarly domains.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0004"
      ],
      "counterevidence": "Chronologies differ by genre and city; ‘by’ does not mean simultaneous everywhere.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0036",
      "statement": "Lexical lists form a continuous knowledge-organizing tradition from the earliest writing through later cuneiform cultures.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0001",
        "SRC-0016"
      ],
      "counterevidence": "Continuity involved copying, reordering and transformation, not static preservation.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0037",
      "statement": "Legal documents, letters and contracts provide human-scale cases but are mediated by scribal formula and institutional context.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0021"
      ],
      "counterevidence": "First-person grammar is not transparent access to private interiority.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0038",
      "statement": "Functional expansion should be narrated as successive additions and recombinations, not a ladder from accounting to literature.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0001",
        "SRC-0004",
        "SRC-0016",
        "SRC-0021"
      ],
      "counterevidence": "Local discontinuities and corpus gaps remain.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-005"
        }
      ]
    },
    {
      "id": "CLM-0039",
      "statement": "ETCSL's 394 literary compositions are modern composites based on late-third- and early-second-millennium manuscripts, so they are evidence for textual tradition rather than transparent transcripts of an original speaker.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0022"
      ],
      "counterevidence": "Individual manuscripts can preserve locally and chronologically specific variants when cited at tablet level.",
      "narrative_implication": "Attribute translation and edition; identify composite status and avoid invented authorial interiority.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0040",
      "statement": "The bounded primary-text shortlist is fixed to four cases: administrative tablet P005390/MMA 1988.433.2, private letter MMA 86.11.111, lexical school tablet P228744, and literary composition ETCSL 3.1.19.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0023",
        "SRC-0024",
        "SRC-0025",
        "SRC-0026",
        "SRC-0027"
      ],
      "counterevidence": "The four cases cover distinct functional turns but cannot represent every city, period, social group or genre.",
      "narrative_implication": "Use only these four handoff candidates unless a later production task documents why a substitution is needed.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0041",
      "statement": "Published English translations are editorial products and require attribution and rights review before direct quotation.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0021",
        "SRC-0022",
        "SRC-0024",
        "SRC-0025",
        "SRC-0026",
        "SRC-0027",
        "SRC-0028"
      ],
      "counterevidence": "Met object images selected here are explicitly Public Domain, but that status does not extend to modern catalogue prose, CDLI/Penn photographs or ETCSL/CTMMA translations.",
      "narrative_implication": "Met images may be used with object credit; paraphrase modern translations unless a production-stage rights check clears quotation.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-008"
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
    },
    {
      "id": "CLM-0043",
      "statement": "MMA 86.11.111 is a ca. 1632 BCE Old Babylonian letter in which Marduk-mushallim reports failure to implement a royal security order.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0021",
        "SRC-0025"
      ],
      "counterevidence": "Its probable Sippar-Yahrurum origin lacks excavated context, and the museum itself presents the letter as unusual.",
      "narrative_implication": "Use as an exceptional human-scale epistolary case illustrating reporting and command, not as representative everyday correspondence or proof that writing caused compliance.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-010"
        }
      ]
    },
    {
      "id": "CLM-0044",
      "statement": "P228744 is a fragmented Old Babylonian lexical school tablet excavated at Nippur and a witness to the OB Nippur Ura 03 composite Q000001.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0016",
        "SRC-0026"
      ],
      "counterevidence": "The obverse is missing and the record does not preserve detailed stratigraphy; formal school material cannot establish population-wide literacy.",
      "narrative_implication": "Use as a representative case of formal lexical classification and copying within the Nippur training tradition only.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-011"
        }
      ]
    },
    {
      "id": "CLM-0045",
      "statement": "ETCSL 3.1.19 is a modern composite of the Puzur-Shulgi royal letter tradition assembled from multiple Old Babylonian manuscripts, not a contemporary Ur III dispatch.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0022",
        "SRC-0027",
        "SRC-0028"
      ],
      "counterevidence": "Individual witnesses such as 3N-T311/IM 58418 preserve substantial portions and can be cited separately, but no one witness equals the complete ETCSL text.",
      "narrative_implication": "Use to show retrospective political/literary memory and scribal copying; always distinguish narrated event, manuscript date and modern reconstruction.",
      "provenance": [
        {
          "workstream": "WS05",
          "local_id": "WS05-CLM-012"
        }
      ]
    },
    {
      "id": "CLM-0046",
      "statement": "Administrative writing increased capacity to classify, aggregate and audit labor, goods and obligations when tied to institutional procedure.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0029",
        "SRC-0030"
      ],
      "counterevidence": "Records alone do not prove compliance or causal primacy.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0047",
      "statement": "Ur III labor records reveal ordinary people mainly through top-down categories and required work.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0029",
        "SRC-0030"
      ],
      "counterevidence": "They do not recover the full lives or viewpoints of recorded workers.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0048",
      "statement": "Writing’s power distribution changed over time: uses once concentrated in royal/institutional systems were later appropriated by urban private actors.",
      "type": "inference",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0031"
      ],
      "counterevidence": "The scale and timing of ‘privatization’ vary by region.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0049",
      "statement": "A written law, norm or transaction is evidence of recording and claim-making, not automatic evidence of enforcement.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0031"
      ],
      "counterevidence": "Case-specific links among tablet, witnesses, seal and action are required.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0050",
      "statement": "Archive survival is structurally biased by clay durability, institutional discard, excavation history and antiquities-market provenance.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0029",
        "SRC-0032"
      ],
      "counterevidence": "Bias does not invalidate the corpus, but limits population-wide inference.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-005"
        }
      ]
    },
    {
      "id": "CLM-0051",
      "statement": "At Puzriš-Dagan, more than 13,500 tablets reconstruct an archival agency tied to livestock, taxation, royal gifts and diplomacy; the archive should not be read as a literal inventory of one stockyard.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0033"
      ],
      "counterevidence": "The surviving repository is selective and its reconstructed units remain scholarly models.",
      "narrative_implication": "Use as a bounded causal case in which records, seals, officials and retrieval practices jointly made obligations actionable.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0052",
      "statement": "Agency belongs to people and institutions using records: tablets stabilize classifications, scribes and sealers authenticate them, archives make them retrievable, and authorities supply enforcement.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0029",
        "SRC-0030",
        "SRC-0033"
      ],
      "counterevidence": "The strength of each link differs by archive; a preserved record alone cannot demonstrate enforcement.",
      "narrative_implication": "Never say writing itself commanded, owned or coerced.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0053",
      "statement": "Distributional effects were asymmetric: record systems improved institutional visibility and elite/private claims while exposing workers and dependents through imposed categories.",
      "type": "inference",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0029",
        "SRC-0030",
        "SRC-0031",
        "SRC-0033"
      ],
      "counterevidence": "People could also use documents strategically, and private uptake widened access in some later settings.",
      "narrative_implication": "Pair every capacity gain with who gained legibility, leverage, burden or exclusion.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-008"
        }
      ]
    },
    {
      "id": "CLM-0054",
      "statement": "Oral negotiation, embodied skill, household practice and much routine exchange remained partly or wholly outside surviving writing.",
      "type": "unknown",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0029",
        "SRC-0032"
      ],
      "counterevidence": "Absence from archives cannot quantify the size of unwritten domains.",
      "narrative_implication": "State the limit; do not turn archival silence into proof of absence.",
      "provenance": [
        {
          "workstream": "WS06",
          "local_id": "WS06-CLM-009"
        }
      ]
    },
    {
      "id": "CLM-0055",
      "statement": "Cuneiform was adapted from Sumerian-associated use to Akkadian and then to multiple unrelated languages.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0034",
        "SRC-0016",
        "SRC-0036"
      ],
      "counterevidence": "Adaptation was not uniform and sometimes imported Mesopotamian languages alongside the script.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS07",
          "local_id": "WS07-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0056",
      "statement": "Adaptation required modification of sign values and orthographic conventions rather than simple substitution of words.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0034",
        "SRC-0036"
      ],
      "counterevidence": "Degree of modification differed by language and scribal center.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS07",
          "local_id": "WS07-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0057",
      "statement": "Lexical lists and bilingual curricula were key transmission infrastructure across regions and centuries.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0016",
        "SRC-0035",
        "SRC-0036"
      ],
      "counterevidence": "Surviving lists privilege formal training contexts.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS07",
          "local_id": "WS07-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0058",
      "statement": "Sumerian outlived probable vernacular use as a learned literary, cultic and scholarly language.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0034",
        "SRC-0035"
      ],
      "counterevidence": "The date and social extent of spoken-language decline remain debated.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS07",
          "local_id": "WS07-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0059",
      "statement": "The living-tradition endpoint is institutional reproduction: active teaching, copying and competent reuse, not the survival of old tablets alone.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0016",
        "SRC-0035"
      ],
      "counterevidence": "Sparse late evidence makes the exact endpoint regional rather than singular.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS07",
          "local_id": "WS07-CLM-005"
        }
      ]
    },
    {
      "id": "CLM-0060",
      "statement": "Transmission moved through courts, traveling or imported specialists, diplomatic contact, copying and formal curricula rather than by script diffusion alone.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0036",
        "SRC-0037",
        "SRC-0038"
      ],
      "counterevidence": "The balance among channels varies by region and is often reconstructed from elite archives.",
      "narrative_implication": "Name the human and institutional carrier for every spread claim.",
      "provenance": [
        {
          "workstream": "WS07",
          "local_id": "WS07-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0061",
      "statement": "The Hittite case shows selective transfer: scholarly and literary cuneiform practices traveled, while Mesopotamian bookkeeping and metrology did not necessarily travel with them.",
      "type": "fact",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0037"
      ],
      "counterevidence": "Other Anatolian sites and periods may preserve different practical uses.",
      "narrative_implication": "Use as a transformation-cost case, not a universal rule of adaptation.",
      "provenance": [
        {
          "workstream": "WS07",
          "local_id": "WS07-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0062",
      "statement": "Script survival, language survival and institutional survival are separable: cuneiform could encode new languages, Sumerian could persist as learned content, and both depended on training communities.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0034",
        "SRC-0016",
        "SRC-0035",
        "SRC-0037"
      ],
      "counterevidence": "Sparse regional evidence prevents one synchronized timeline.",
      "narrative_implication": "Track the three layers independently through the endpoint passed to WS08.",
      "provenance": [
        {
          "workstream": "WS07",
          "local_id": "WS07-CLM-008"
        }
      ]
    },
    {
      "id": "CLM-0063",
      "statement": "Cuneiform use contracted over centuries rather than ending through one event.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0035",
        "SRC-0034"
      ],
      "counterevidence": "Regional and genre-specific endpoints differ.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0064",
      "statement": "Lexical and scholarly traditions persisted into the first centuries CE in narrowed institutional settings.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0035"
      ],
      "counterevidence": "Exact last-tablet dates depend on genre and dating; ‘last’ remains a discovery-sensitive claim.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0065",
      "statement": "Material tablets survived after living reading competence disappeared, creating a break between ancient transmission and modern knowledge.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0035",
        "SRC-0039",
        "SRC-0040"
      ],
      "counterevidence": "Some local knowledge of ruins or objects may have persisted without script competence.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0066",
      "statement": "Nineteenth-century decipherment was cumulative and comparative, not a single eureka moment.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0039",
        "SRC-0040"
      ],
      "counterevidence": "Public narratives often center Behistun and a few individuals, underrepresenting collaboration and error.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0067",
      "statement": "Cuneiform’s defensible modern legacy is recovery-mediated knowledge of ancient societies and influence through ancient Near Eastern textual transmission; resemblance to digital record systems is analogy, not lineage.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0035",
        "SRC-0039",
        "SRC-0040"
      ],
      "counterevidence": "Specific transmitted texts or concepts require separate chains of evidence.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-005"
        }
      ]
    },
    {
      "id": "CLM-0068",
      "statement": "The latest currently known dated cuneiform tablet is an astronomical text from 75 CE, but this is a latest-discovered datum, not a proven final act of writing.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0041"
      ],
      "counterevidence": "New finds may move the endpoint, and competence could outlast the latest preserved tablet.",
      "narrative_implication": "Use 'latest currently known' and keep WS07's institutional-reproduction definition.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0069",
      "statement": "Cuneiform decline combined language competition, institutional contraction, changing political economies and the cost of specialist training; no surviving evidence isolates one sufficient cause.",
      "type": "inference",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0035",
        "SRC-0034",
        "SRC-0041"
      ],
      "counterevidence": "The relative weight of Aramaic, Greek, temple change and regional politics differs by place and century.",
      "narrative_implication": "End with a mechanism set, not a single-collapse explanation.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0070",
      "statement": "Modern recovery proceeded through copied inscriptions, the partial decipherment of Old Persian, multilingual comparison at Behistun, and subsequent testing of Akkadian and Sumerian readings.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0039",
        "SRC-0040",
        "SRC-0042"
      ],
      "counterevidence": "Individual milestones are important but none alone recovered the full cuneiform tradition.",
      "narrative_implication": "Use a short cumulative chain rather than a hero-only eureka story.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-008"
        }
      ]
    },
    {
      "id": "CLM-0071",
      "statement": "Legacy claims fall into three classes: direct ancient transmission, recovery-mediated modern knowledge, and analogy without lineage.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0035",
        "SRC-0039",
        "SRC-0040",
        "SRC-0042"
      ],
      "counterevidence": "Each proposed direct transmission still requires its own documented chain.",
      "narrative_implication": "Permit only the first two as historical legacy; label digital-record parallels as analogy.",
      "provenance": [
        {
          "workstream": "WS08",
          "local_id": "WS08-CLM-009"
        }
      ]
    }
  ],
  "contradiction_register": [
    {
      "id": "CTR-0001",
      "question": "Earliest proto-cuneiform đã là writing hay vẫn là proto-writing?",
      "positions": [
        "Strict glottography excludes much of Uruk IV material.",
        "Broader lexical/conventional definition includes it."
      ],
      "provenance": [
        "WS01-CLM-001"
      ],
      "outline_rule": "State the definition before making invention/first claims."
    },
    {
      "id": "CTR-0002",
      "question": "Token có phát triển tuyến tính thành tablet và writing không?",
      "positions": [
        "Numerical continuity is strong for selected late devices.",
        "A universal millennia-long token code and direct genealogy are unsupported."
      ],
      "provenance": [
        "WS02-CLM-001",
        "WS02-CLM-002",
        "WS02-CLM-003"
      ],
      "outline_rule": "Use an information ecology, not a single ancestor story."
    },
    {
      "id": "CTR-0003",
      "question": "Writing caused institutional power or merely recorded it?",
      "positions": [
        "Later procedural archives show capacity effects.",
        "Co-development and enforcement by people/institutions prevent technological determinism or back-projection to Uruk."
      ],
      "provenance": [
        "WS02-CLM-005",
        "WS06-CLM-001",
        "WS06-CLM-007"
      ],
      "outline_rule": "Present a phase-bound feedback loop."
    },
    {
      "id": "CTR-0004",
      "question": "Sumerian continuity is language, script or institution?",
      "positions": [
        "Sumerian persisted as learned content after probable vernacular decline.",
        "Cuneiform also survived by adapting to other languages; timelines are not identical."
      ],
      "provenance": [
        "WS07-CLM-004",
        "WS07-CLM-008"
      ],
      "outline_rule": "Track script, language and training community separately."
    },
    {
      "id": "CTR-0005",
      "question": "Modern legacy is direct transmission or rediscovery?",
      "positions": [
        "Recovery-mediated knowledge is strongly supported.",
        "Direct lineage to modern writing or databases is unproven; resemblance alone is analogy."
      ],
      "provenance": [
        "WS08-CLM-003",
        "WS08-CLM-005",
        "WS08-CLM-009"
      ],
      "outline_rule": "End at the break and recovery, not a smartphone lineage."
    }
  ]
}
# END INPUT: 01_research/claim-ledger.json
