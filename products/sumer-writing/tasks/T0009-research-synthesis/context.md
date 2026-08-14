# Context Packet — T0009-research-synthesis

- Product: `sumer-writing`
- Operation: `research_synthesis`
- Section: `-`
- Unit: `-`
- Allowed writes: `01_research/research-synthesis.md`, `tasks/T0009-research-synthesis/report.md`, `tasks/T0009-research-synthesis/operator-brief.json`

## Acceptance criteria

- Không mất contradiction hoặc unknown giữa các workstream.
- Dùng global ledgers do deterministic consolidation tạo; không remap hoặc rewrite chúng trong AI task.
- Synthesis tổ chức theo causal questions, không theo thứ tự nguồn.
- Không viết outline hoặc narration.

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

# BEGIN INSTRUCTION: system/operations/research-synthesis.md
# Operation — Research Synthesis

## Responsibility

Hợp nhất các workstream handoff thành một mental model có thể dùng để dựng outline. Global source/claim ledgers đã được router hợp nhất bằng code trước khi task bắt đầu và không phải output của AI task này.

## Rules

- Không mở hoặc rewrite toàn bộ local/global ledger trong task này; `consolidation.json` xác nhận chúng đã được remap và giữ provenance.
- Dùng workstream synthesis làm bounded handoff. Nếu handoff thiếu evidence cần thiết, trả blocker về đúng workstream thay vì nạp mọi ledger để bù.
- Conflict giữa workstream trở thành contradiction, không bị “giải quyết” bằng trung bình hóa.
- Phân biệt evidence về chronology, mechanism, magnitude và lived experience.
- Xác định claim trụ cột nào đủ support, cần qualify hoặc phải loại.
- `research-synthesis.md` tổ chức theo causal chain và open decisions, không theo WS01, WS02…
# END INSTRUCTION: system/operations/research-synthesis.md

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

# BEGIN INPUT: 01_research/plan.json
{
  "schema_version": 1,
  "status": "approved",
  "central_research_question": "Writing ở miền nam Mesopotamia đã hình thành, trở thành hạ tầng xã hội, biến đổi và để lại afterlife như thế nào?",
  "hypotheses_to_test": [
    "Administrative scale là động lực trung tâm nhưng không nhất thiết là nguyên nhân duy nhất của writing sớm.",
    "Writing không chỉ phản ánh thiết chế mà còn thay đổi capacity và distribution of power.",
    "Script, language và scribal practice có lifecycle khác nhau.",
    "Legacy có thể được chứng minh qua persistence/adaptation/recovery mà không cần tuyên bố lineage trực tiếp tới mọi writing hiện đại."
  ],
  "shared_research_protocol": {
    "chronology": [
      "Dùng date range và archaeological period khi chronology còn tranh luận; không biến approximate date thành một năm chính xác.",
      "Mọi workstream phải phân biệt evidence đương thời, retrospective copy và modern reconstruction."
    ],
    "terminology": [
      "Phân biệt Sumerian language, Sumerian population label, proto-cuneiform, cuneiform, script, writing và literacy.",
      "Thuật ngữ gây tranh luận phải dùng định nghĩa/qualification do WS01 thiết lập; bất đồng được giữ lại cho synthesis thay vì tự chuẩn hóa."
    ],
    "case_selection": [
      "Ưu tiên case có provenance, chronology, primary evidence và khả năng kiểm tra causal mechanism; narrative value không đủ để chọn case.",
      "Ghi rõ case là representative, exceptional hay chỉ illustrative; không suy rộng từ một archive, city hoặc elite corpus.",
      "Ưu tiên một số địa điểm/thời kỳ có thể nối xuyên workstream khi evidence cho phép, nhưng không ép continuity giả."
    ],
    "cross_cutting_ownership": {
      "exchange": "WS02 sở hữu vai trò của exchange/accounting trong formation; WS05 lập chronology các use case kinh tế; WS06 chỉ đánh giá effect lên obligation, ownership, standardization hoặc institutional action khi có case evidence.",
      "social_memory": "WS05 xác định các form/genre dùng để lưu và tái tạo memory; WS06 đánh giá selection, erasure và political consequences; WS08 chỉ xử lý survival, loss và modern recovery.",
      "knowledge_transmission": "WS04 sở hữu training/community of practice; WS05 sở hữu lexical/curricular content và functional expansion; WS07 sở hữu transmission qua language, region và institution. Synthesis nối ba lớp này."
    },
    "handoff_contract": [
      "Mỗi workstream bàn giao chronology ranges, supported claims, disputed claims, unknowns, selected cases, scope limits và dependencies on other workstreams.",
      "Mỗi claim phân biệt observation, scholarly inference và causal inference; nêu counterevidence hoặc alternative explanation khi có.",
      "Không workstream nào tự giải quyết contradiction thuộc ownership của workstream khác; contradiction được chuyển rõ cho research synthesis."
    ]
  },
  "workstreams": [
    {
      "id": "WS01",
      "title": "Definition, chronology and attribution",
      "question": "Thế nào được tính là writing, các mốc earliest evidence là gì, và attribution cho Sumer/Uruk chắc đến đâu?",
      "in_scope": "Definitions, proto-cuneiform threshold, dating, archaeological context, comparative attribution.",
      "out_of_scope": "Formation mechanism, full development of later genres or scribal institutions.",
      "ownership": "Thiết lập vocabulary, chronology ranges và mức chắc chắn của first/invented/attribution claims; không kết luận vì sao writing hình thành.",
      "required_evidence": [
        "Primary archaeological/corpus evidence",
        "Recent scholarly synthesis",
        "Competing definitions and chronologies"
      ],
      "completion_criteria": [
        "Qualify first/invented claim",
        "Produce chronology ranges",
        "List unresolved attribution issues"
      ],
      "synthesis_handoff": [
        "Working definitions and terminology warnings",
        "Chronology ranges with confidence",
        "Attribution disputes",
        "Boundary conditions for WS02 and WS03"
      ]
    },
    {
      "id": "WS02",
      "title": "Prehistory and formation mechanisms",
      "question": "Tokens, seals, counting and urban/institutional pressures relate to writing formation by what mechanisms?",
      "in_scope": "Pre-writing information practices, Uruk scale, accounting hypothesis, exchange/redistribution pressures and alternative functions.",
      "out_of_scope": "Defining the writing threshold already owned by WS01, later functional expansion, demonstrated downstream power effects and final decline.",
      "ownership": "Giải thích và đối chiếu các formation mechanisms, gồm vai trò ban đầu của exchange/accounting; không suy từ formation pressure sang later institutional consequence.",
      "required_evidence": [
        "Material sequence and provenance",
        "Administration and exchange hypotheses",
        "Critiques/non-linear models"
      ],
      "completion_criteria": [
        "Test token continuity",
        "Separate evidence from inference",
        "Identify causal direction limits",
        "Distinguish exchange, redistribution, labor coordination, obligation and ownership where evidence permits"
      ],
      "synthesis_handoff": [
        "Mechanism comparison",
        "Evidence-to-inference map",
        "Alternative explanations",
        "Candidate feedback loop to WS06"
      ]
    },
    {
      "id": "WS03",
      "title": "Sign system and language transformation",
      "question": "Hệ thống dấu hiệu thay đổi về medium, form và relation to language như thế nào?",
      "in_scope": "Sign forms, numerical/metrological systems, phonetic/rebus use, cuneiform technique and the material production/use cycle of tablets where it changes expressive capacity.",
      "out_of_scope": "Definition and attribution owned by WS01, social uptake/genre history, archive survival after use, full political history and modern decipherment.",
      "ownership": "Xác định system có thể biểu đạt và vận hành ra sao ở từng state; không đồng nhất technical possibility với actual social use.",
      "required_evidence": [
        "Tablet/corpus examples",
        "Palaeographic/linguistic scholarship",
        "Uncertainty over language encoding",
        "Material evidence for production and use"
      ],
      "completion_criteria": [
        "Avoid pictograph-to-alphabet teleology",
        "Explain state changes",
        "Separate script from language",
        "Distinguish technical capacity from attested use"
      ],
      "synthesis_handoff": [
        "Technical state changes",
        "Medium/sign/language distinctions",
        "Capability limits",
        "Questions for actual use in WS05"
      ]
    },
    {
      "id": "WS04",
      "title": "Scribes, institutions and access",
      "question": "Ai sản xuất và học writing, trong những thiết chế nào, và access thay đổi theo thời kỳ ra sao?",
      "in_scope": "Training, labor, workplace, identity, gender/class/access, institutional sponsorship and knowledge-transmission communities.",
      "out_of_scope": "Claims about median experience without evidence, genre chronology owned by WS05 and social consequences owned by WS06.",
      "ownership": "Lập bản đồ users, training và access theo từng period; không coi scribe hoặc literacy là category xã hội ổn định xuyên thời gian.",
      "required_evidence": [
        "School/practice texts with caveats",
        "Administrative archives",
        "Social-history scholarship"
      ],
      "completion_criteria": [
        "Map known/unknown users",
        "Avoid modern literacy categories",
        "Identify human-scale anchors",
        "Periodize changes in scribal identity and access"
      ],
      "synthesis_handoff": [
        "Actor/institution map by period",
        "Access and uncertainty map",
        "Training mechanisms",
        "Human anchors with representativeness labels"
      ]
    },
    {
      "id": "WS05",
      "title": "Functional expansion and human voices",
      "question": "Writing mở từ các record sớm sang những domain nào, khi nào, và primary voices nào đại diện được?",
      "in_scope": "Chronology of administrative/economic, lexical, legal/normative, epistolary, literary/religious and memory-related uses; a bounded set of primary voices illustrating verified functional turns.",
      "out_of_scope": "Genre catalogue without causal implication, proof of institutional/power effects owned by WS06, or a general anthology selected only for narrative appeal.",
      "ownership": "Chứng minh what/when of functional expansion and select evidence-backed voices; WS06 alone owns claims that a recorded domain changed action or power.",
      "required_evidence": [
        "Primary texts/translations",
        "Genre and use chronology",
        "Representative-use critique",
        "Provenance and reuse/copy status"
      ],
      "completion_criteria": [
        "Select a bounded set of evidence-backed voices",
        "Explain functional turns rather than catalogue genres",
        "Label representative, exceptional and illustrative cases",
        "Flag translation/rights issues"
      ],
      "synthesis_handoff": [
        "Functional-turn chronology",
        "Economic/memory/knowledge use cases",
        "Primary-voice shortlist with provenance",
        "Claims requiring consequence tests in WS06"
      ]
    },
    {
      "id": "WS06",
      "title": "Power, consequences and archive bias",
      "question": "Recorded information changed institutional capacity and power in what demonstrable ways, and how does archive formation limit what can be claimed?",
      "in_scope": "A bounded set of causal case studies involving labor, obligation, ownership, standardization, law/norm, royal memory or erasure; archive selection, preservation and absence as limits on those cases.",
      "out_of_scope": "Re-cataloguing functions owned by WS05, formation pressures owned by WS02, full material afterlife/rediscovery owned by WS08, or technology-determinist claims without causal evidence.",
      "ownership": "Kiểm tra whether/how recorded information changed action, capacity and distribution; archive bias là constraint applied to each selected case, không phải một lịch sử archive độc lập.",
      "required_evidence": [
        "Case studies linking record to action",
        "Archive formation/preservation scholarship",
        "Counterexamples and limits",
        "Evidence of non-written or parallel practices where available"
      ],
      "completion_criteria": [
        "Distinguish tool/user/institution agency",
        "Identify distributional effects",
        "Apply archive-bias assessment to every causal case",
        "Identify limits and domains remaining outside writing"
      ],
      "synthesis_handoff": [
        "Tested causal cases",
        "Feedback loop with WS02",
        "Distributional effects and counterexamples",
        "Archive-bias limits attached to claims"
      ]
    },
    {
      "id": "WS07",
      "title": "Spread, adaptation and multilingual afterlife",
      "question": "Writing practice moved across languages, regions and political systems through what channels and transformations while it remained a living learned tradition?",
      "in_scope": "Adaptation cases, training/diplomacy/prestige/administration, Sumerian as learned language, and transmission while institutions still taught or used the tradition.",
      "out_of_scope": "Unbounded global history of writing, terminal ecosystem decline, post-loss rediscovery and modern legacy owned by WS08.",
      "ownership": "Giải thích transmission/adaptation within a living tradition; endpoint là khi reproduction through active communities and institutions ceases.",
      "required_evidence": [
        "Comparative script/language cases",
        "Transmission institutions",
        "Chronology",
        "Evidence of active teaching/use"
      ],
      "completion_criteria": [
        "Show mechanisms of spread",
        "Separate script/language survival",
        "Identify transformation costs",
        "Define and justify the living-tradition endpoint handed to WS08"
      ],
      "synthesis_handoff": [
        "Transmission channels",
        "Adaptation cases",
        "Script/language/institution survival distinctions",
        "Evidence-based endpoint for WS08"
      ]
    },
    {
      "id": "WS08",
      "title": "Decline, rediscovery and bounded legacy",
      "question": "Khi living cuneiform tradition suy tàn và biến mất, nó được recovered dưới điều kiện nào, và những legacy claim nào có transmission evidence thay vì chỉ analogy?",
      "in_scope": "Terminal ecosystem decline after WS07's living-tradition endpoint, final dated use, loss, material survival, excavation/decipherment, modern recovery and bounded legacy.",
      "out_of_scope": "Earlier multilingual adaptation owned by WS07, a full history of archaeology/Assyriology, or direct Sumer-to-smartphone lineage without transmission evidence.",
      "ownership": "Giải thích cessation, material survival and modern recovery; legacy claims phải tách direct transmission, recovery-mediated influence và analogy.",
      "required_evidence": [
        "Late dated records",
        "Evidence for institutional/ecosystem decline",
        "Histories of excavation and decipherment",
        "Transmission-vs-analogy analysis"
      ],
      "completion_criteria": [
        "Avoid monocausal ending",
        "Use the endpoint established with WS07",
        "Find opening/ending anchors without turning into a general archaeology history",
        "Classify and bound each legacy claim"
      ],
      "synthesis_handoff": [
        "Decline mechanism set",
        "Final-use and loss chronology",
        "Recovery chain",
        "Legacy claims classified by transmission strength",
        "Opening/ending anchor candidates"
      ]
    }
  ],
  "coverage_matrix": {
    "definition_chronology_attribution": [
      "WS01"
    ],
    "pressure_and_formation": [
      "WS01",
      "WS02"
    ],
    "technical_transformation": [
      "WS03"
    ],
    "adoption_people_and_training": [
      "WS04"
    ],
    "functional_expansion": [
      "WS05"
    ],
    "exchange": [
      "WS02",
      "WS05",
      "WS06"
    ],
    "social_memory": [
      "WS05",
      "WS06",
      "WS08"
    ],
    "knowledge_transmission": [
      "WS04",
      "WS05",
      "WS07"
    ],
    "consequence_and_conflict": [
      "WS06"
    ],
    "material_and_archive_ecology": [
      "WS03",
      "WS06",
      "WS08"
    ],
    "adaptation_within_living_tradition": [
      "WS07"
    ],
    "terminal_decline_recovery_and_legacy": [
      "WS08"
    ]
  },
  "synthesis_questions": [
    "Writing là cause, capacity, co-development hay record của social complexity ở từng phase?",
    "Object nào giữ continuity xuyên các lần đổi medium, language, user và institution?",
    "Vòng phản hồi nào tồn tại giữa institutional pressure, writing capacity và institutional expansion?",
    "Exchange, social memory và knowledge transmission thay đổi ở đâu, và evidence chỉ cho thấy record hay cho thấy action/consequence?",
    "Archive formation và survival bias giới hạn từng causal claim như thế nào?",
    "Human voices nào đủ representative và có translation/provenance tốt?",
    "Ranh giới giữa living transmission, terminal decline, recovery-mediated legacy và analogy nằm ở đâu?",
    "Opening và ending nào tạo payoff mà không lặp FoC?"
  ],
  "approved_by": "user",
  "approved_at": "2026-08-12T16:26:25.828Z"
}
# END INPUT: 01_research/plan.json

# BEGIN INPUT: 01_research/consolidation.json
{
  "schema_version": 1,
  "generator": "scripts/consolidate_research.py",
  "mode": "adopted",
  "created_at": "2026-08-13T06:18:26.425Z",
  "inputs": [
    {
      "path": "01_research/workstreams/WS01/sources.json",
      "sha256": "a08f9ac66023d911a9635143a11b4a2b64e2f0ea6204deafc73c23b31f3057e1",
      "bytes": 6784
    },
    {
      "path": "01_research/workstreams/WS01/claims.json",
      "sha256": "1cdbdc78f163716e5f6a8d95a81a6b94afe057d9540e946a2e7bca0ba34e6493",
      "bytes": 7759
    },
    {
      "path": "01_research/workstreams/WS02/sources.json",
      "sha256": "5f52e389c74ec50584b7f3a6556030e726ae846eea023af14bd5beebdc8b39cf",
      "bytes": 3969
    },
    {
      "path": "01_research/workstreams/WS02/claims.json",
      "sha256": "3a26489a7de6cd97208c6d980aab30c2a2eb94a29870c8c19c8fa23ba58b9355",
      "bytes": 4984
    },
    {
      "path": "01_research/workstreams/WS03/sources.json",
      "sha256": "d06ffa08fa923a8150c9550e8af387af737c41e0d8c1551f2e2ed6799af6512d",
      "bytes": 3001
    },
    {
      "path": "01_research/workstreams/WS03/claims.json",
      "sha256": "c7eecccb6d4742f0d5e488367a63280a5c42e93be33c17c4fc09b807aec89669",
      "bytes": 3960
    },
    {
      "path": "01_research/workstreams/WS04/sources.json",
      "sha256": "d629bd5d01011728153c838799a3e34e18229e9540cfff560995ed13afa03196",
      "bytes": 4282
    },
    {
      "path": "01_research/workstreams/WS04/claims.json",
      "sha256": "e4bb91a67fa625f0cd7969a35032c225d9b6ed8a98400b6fd0dd79e91088f96f",
      "bytes": 4606
    },
    {
      "path": "01_research/workstreams/WS05/sources.json",
      "sha256": "a98f8fcdffa19f8b40b2c30a9e5764078ed2230a8562bd319282445778b59fff",
      "bytes": 9122
    },
    {
      "path": "01_research/workstreams/WS05/claims.json",
      "sha256": "17954ea2049d05d48a18665e8bd892d5306bb9d8dcbf6ab787bf80fec701e33f",
      "bytes": 7867
    },
    {
      "path": "01_research/workstreams/WS06/sources.json",
      "sha256": "91f8503d55cdc33081ccd7fcb78637ec0765b0806b53199c93883a09318fd5fe",
      "bytes": 2947
    },
    {
      "path": "01_research/workstreams/WS06/claims.json",
      "sha256": "c76df5fd16d6649a84a5d94bdd72dfba454acdec68d8370dc6520f2e7901a45e",
      "bytes": 5283
    },
    {
      "path": "01_research/workstreams/WS07/sources.json",
      "sha256": "8c3278a13db0d4e06d10b5af0327814026a28ce26ecb7dee7636020637117c2f",
      "bytes": 3609
    },
    {
      "path": "01_research/workstreams/WS07/claims.json",
      "sha256": "56fe05265a6e005091649f2e777a7e0b3885036a9d822fcc652215da1cdc2c3b",
      "bytes": 4592
    },
    {
      "path": "01_research/workstreams/WS08/sources.json",
      "sha256": "a941dbcd5ad32bf9a42d2bc8732b3d9f5e2b2d5db69b1b98a753d5a0f8d33d31",
      "bytes": 3765
    },
    {
      "path": "01_research/workstreams/WS08/claims.json",
      "sha256": "1301c42e3c61d5b67c53529db6291d920bfcf9a6e5b46279062e86d93047cc1d",
      "bytes": 5361
    }
  ],
  "outputs": [
    {
      "path": "01_research/source-index.json",
      "sha256": "902e4ea8cb6bc91c166cff67ac5222fbb739310063ac3b06c72c5bd1c2d66581",
      "bytes": 39770
    },
    {
      "path": "01_research/claim-ledger.json",
      "sha256": "5b316543e9d25b449066ba6986edea2f88631dfcf440cfcb26b1062fed8e088a",
      "bytes": 53758
    }
  ]
}
# END INPUT: 01_research/consolidation.json

# BEGIN INPUT: 01_research/workstreams/WS01/synthesis.md
# Synthesis — WS01

Status: complete

## Answer

Không có một ngưỡng hoàn toàn trung tính để trả lời “chữ viết bắt đầu khi nào”. Nếu writing được định nghĩa nghiêm ngặt là một hệ thống có thể biểu đạt lời nói bằng các giá trị ngôn ngữ ổn định, phần lớn proto-cuneiform sớm đứng gần ranh giới hơn là chắc chắn ở phía “true writing”: nó truyền đạt số lượng, vật phẩm, chức danh và các quan hệ trong bố cục tablet, nhưng rất ít phonology và không tái tạo lời nói liên tục. Nếu dùng định nghĩa rộng hơn—một hệ dấu quy ước ghi lại các đơn vị lexical có thể lặp lại—Uruk IV đã là writing. Vì vậy, dự án cần công khai một mô hình phân tầng thay vì để định nghĩa âm thầm quyết định kết luận.

Niên đại làm việc đáng tin nhất là:

- các thiết bị/accounting notations tiền thân tồn tại trước ngưỡng proto-cuneiform;
- **Uruk IV, khoảng 3350/3300–3200 BCE:** horizon proto-cuneiform sớm nhất có corpus đáng kể;
- **Uruk III/Jemdet Nasr, khoảng 3200–3000 BCE:** corpus lớn hơn, format và repertory phát triển hơn, lexical materials rõ hơn;
- sau đó là quá trình dần tiến đến cuneiform có biểu đạt ngôn ngữ rõ ràng hơn trong thiên niên kỷ III BCE.

Relative sequence này đáng tin hơn absolute date. Nghiên cứu mới về hồ sơ khai quật Uruk cho rằng IVa là context có khả năng cao nhất cho script sớm nhất, nhưng find-spot và stratigraphy được ghi chép quá kém để ấn định một “năm phát minh” hay loại trừ tuyệt đối một date sớm hơn.

Attribution cũng phải chia thành bốn câu hỏi:

1. **Địa điểm/corpus:** Uruk và southern Mesopotamia—mức chắc chắn cao.
2. **Truyền thống script:** proto-cuneiform ancestral to later cuneiform—cao.
3. **Ngôn ngữ của tablet sớm:** Sumerian là khả năng hợp lý nhưng chưa chứng minh chắc—trung bình/thấp cho attribution trực tiếp.
4. **Population/ethnicity của người tạo:** không thể suy ra chỉ từ địa điểm và later language—thấp.

Do đó, phát biểu an toàn là: **một trong những truyền thống writing độc lập sớm nhất, với corpus lớn sớm nhất được biết đến, xuất hiện trong Uruk cultural sphere ở southern Mesopotamia khoảng cuối thiên niên kỷ IV BCE và phát triển thành cuneiform**. “Người Sumer phát minh chữ viết vào năm 3200 BCE” là quá chính xác ở cả population, language, date và priority.

## Mechanism and chronology

WS01 không quyết định vì sao hệ thống hình thành; đó là WS02. Điều WS01 có thể bàn giao là boundary condition: không được dùng sự nối tiếp vật chất giữa token/bulla/numerical tablet/proto-cuneiform như bằng chứng tự động cho một đường phát minh tuyến tính. Một số continuity về clay, numerical notation và administrative practice rất mạnh, nhưng ranh giới giữa semasiography và glottography vẫn không rõ và các hệ thống có thể cùng tồn tại.

Cũng cần tách proto-cuneiform khỏi “cuneiform” theo hình dạng. Các dấu sớm phần lớn được vạch/incise; wedge-impressed ductus đặc trưng phát triển sau. Tên proto-cuneiform hữu ích để chỉ ancestry, nhưng không được dùng để khiến hình thức muộn hơn xuất hiện quá sớm.

## Strongest evidence

- Corpus synthesis của Englund đặt emergence gần 3300 BCE và phân biệt rõ Uruk IV với Uruk III; Uruk IV gần như toàn administrative trong material đã biết, trong khi lexical texts tăng ở Uruk III.
- Audit khai quật Uruk của Nissen xác định IVa là placement có khả năng nhất, đồng thời chứng minh tại sao exact context vẫn không thể được coi là chắc chắn.
- Phân tích semiotic của Maiocchi cho thấy không có đường ranh sạch giữa nonwriting và writing trong evidence sớm; glottographic/semasiographic là công cụ phân tích, không phải hai hộp khảo cổ tuyệt đối.
- So sánh với Abydos cho thấy Mesopotamia và Egypt xuất hiện gần như đồng thời trong độ phân giải chronology hiện có; “world first” phụ thuộc definition và dating.
- Việc proto-cuneiform ít phonetic information khiến Sumerian-language attribution ở giai đoạn Uruk IV–III chưa thể khẳng định, dù continuity với later Sumerian cuneiform là mạnh.

## Contradictions and unknowns

- **Definition dispute:** strict language encoding hay conventional lexical record đủ để gọi là writing?
- **Absolute priority:** Uruk hay Abydos sớm hơn không thể giải quyết chắc bằng date ranges hiện tại.
- **Earliest Uruk context:** IVa có khả năng nhất; slightly earlier vẫn chưa bị loại trừ.
- **Underlying language:** rare rebus evidence có đủ để gọi proto-cuneiform là Sumerian hay không?
- **Corpus bias:** clay và Uruk excavation khiến một tradition/city có thể trông độc tôn hơn thực tế.
- **Perishable media:** khả năng dùng wood hoặc medium dễ mất tồn tại nhưng không thể dùng như fact nếu thiếu artefact.
- **Attribution vocabulary:** “Sumerian” có thể chỉ language, later textual tradition, region hoặc population; mọi lần dùng phải ghi rõ nghĩa.

## Handoff to global synthesis

### Working definitions

- **Accounting device:** vật/thao tác lưu quantity hoặc identity nhưng không có hệ dấu hai chiều đủ ổn định.
- **Proto-writing/semasiography:** hệ dấu truyền meaning hoặc quantity mà không chứng minh được language-specific values.
- **Writing/glottography:** hệ dấu quy ước có khả năng mã hóa đơn vị ngôn ngữ; không nhất thiết phải ghi đầy đủ câu nói.
- **Proto-cuneiform:** tên lịch sử cho các hệ tablet Uruk IV–III ancestral to cuneiform; vị trí của nó trên ngưỡng proto-writing/writing tùy definition.
- **Cuneiform:** script family wedge-impressed và logo-syllabic ở các phase sau; không đồng nhất với mọi dấu sớm trên clay.

### Confidence handoff

- Relative Uruk IV → Uruk III sequence: **high**.
- Approximate ranges 3350/3300–3200 và 3200–3000 BCE: **medium-high**, luôn dùng range.
- IVa as earliest secure/probable context: **medium-high**, không definitive.
- Uruk/southern Mesopotamian regional attribution: **high**.
- Direct Sumerian-language attribution for earliest proto-cuneiform: **low-medium/contested**.
- Ethnic Sumerian inventor claim: **low/unsupported**.
- Unique “first writing in the world” claim: **contested; không dùng như fact**.

### Boundaries for later workstreams

- WS02 có thể nghiên cứu formation mechanisms nhưng không được coi token continuity hoặc administrative predominance là proof of a single cause.
- WS03 phải tách technical capability khỏi attested language encoding và không đặt wedge-shaped cuneiform vào earliest phase.
- Global synthesis nên dùng “Uruk/southern Mesopotamian proto-cuneiform tradition” cho horizon sớm; chỉ dùng “Sumerian writing” khi claim có linguistic/contextual support.
# END INPUT: 01_research/workstreams/WS01/synthesis.md

# BEGIN INPUT: 01_research/workstreams/WS02/synthesis.md
# Synthesis — WS02

Status: complete

## Answer

Proto-cuneiform did not emerge from one invention event. The strongest continuity runs from late-fourth-millennium numerical practices—tokens inside bullae, sealings, numerical tablets and metrological signs—into proto-cuneiform. Yet the evidence does not support a universal, linear token-to-sign genealogy. Urban scale and institutional accounting created a strong selection pressure, while seals, visual repertoires and multiple clay information devices supplied parallel components.

## Mechanism and chronology

- Numerical systems provide the strongest material continuity between pre-writing devices and proto-cuneiform.
- Neolithic clay objects called tokens were multifunctional; their existence does not prove a millennia-long standardized accounting code.
- The direct token→tablet→writing sequence is too linear; seals, iconography, bullae, numerical tablets and institutional practice formed a parallel ecology.
- Administrative scale is a major formation pressure but not evidence that administration was the sole cause of writing.
- The evidence supports a feedback model: expanding institutions demanded records, and better records could expand institutional capacity.

## Strongest evidence

- **Woods (ed.), Visible Language:** pp. 33–50; development of accounting systems; limitation: Comparative overview; some pathways remain hypothetical.
- **Proto-Cuneiform Account-Books and Journals:** pp. 24–31; limitation: Older chronology; causal interpretation remains debated.
- **Reconsidering ‘Tokens’:** abstract and pp. 233–259; limitation: Full text access limited; abstract supports multifunctionality critique.
- **Writing in Early Mesopotamia: Beyond the Meme:** pp. 410–412; limitation: Framework-oriented rather than a new excavation report.

## Contradictions and unknowns

- Some late simple tokens in bullae clearly served numerical/accounting functions.
- Exact contribution of each component cannot be quantified.
- Preserved earliest texts are overwhelmingly administrative, but corpus survival is selective.
- Downstream effects require WS06 case studies; WS02 cannot establish them alone.

## Completion handoff

### Mechanism comparison

| Mechanism | Minimum evidence | What the present corpus supports | Limit |
|---|---|---|---|
| Accounting/administrative transfer | quantities, commodities, document structure | Strong for much Uruk IV–III material | Does not identify reciprocity or ownership by itself |
| Redistribution | centralized inflow/outflow, offices or recipient classes | Plausible in bounded institutional records | Institution and flow direction are often reconstructed |
| Labor coordination | persons/teams, rations, time or output measures | Possible where personnel and metrology co-occur | Later labor regimes cannot be projected backward |
| Obligation | quota, due delivery, named responsible party or repeated cycle | Supported in selected administrative subgenres | Recording does not prove enforcement |
| Ownership/transfer | durable claimant, seal/witness, transfer conditions | Weak for the earliest corpus | Stronger evidence belongs to later WS05/WS06 cases |
| Exchange | reciprocal parties and transfer terms | Not established by commodity-plus-number alone | “Trade” is too specific without transaction structure |

### Evidence-to-inference map

Observation: numerical signs, metrological systems, sealings, bullae, tablets and administrative layouts coexist in a late-fourth-millennium information ecology. Scholarly inference: numerical practice is the strongest continuity, while iconography and sealing supplied other resources. Causal inference, held at medium confidence: growing institutions selected for records and records may later have increased capacity. The last step is not closed here.

### Alternatives and unknowns

The linear token genealogy is rejected as a universal explanation. Remaining alternatives are parallel development among counting, sealing and image traditions; selective incorporation of some token practices; and independent institutional standardization. Exact weights cannot be recovered from frequency alone.

### Handoff to WS06

Test the candidate loop only through cases where a record can be connected to procedure and action: **institutional scale → demand for stable classifications → records/seals/archives → greater coordination or claim enforcement → capacity for larger operations**. WS06 must identify users, enforcement and distributional effects before accepting the return arrow.

### Scope limits and dependencies

WS01 owns the writing threshold; WS03 owns technical expressive capacity; WS05 owns later economic-use chronology; WS06 owns demonstrated consequences. No formation claim here proves later power effects.
# END INPUT: 01_research/workstreams/WS02/synthesis.md

# BEGIN INPUT: 01_research/workstreams/WS03/synthesis.md
# Synthesis — WS03

Status: complete

## Answer

The system changed along several axes that must not be collapsed: marks shifted from drawn/curvilinear forms toward impressed wedges; tablet layout carried syntactic work; sign repertoires and metrological systems became more standardized; and phonetic/rebus use gradually made language more explicit. This was not a pictograph-to-alphabet ladder. Technical possibility preceded consistent linguistic use, and cuneiform remained logo-syllabic rather than becoming alphabetic.

## Mechanism and chronology

- Proto-cuneiform and mature cuneiform differ in ductus: early signs were largely drawn, while wedge impressions became systematic later.
- Tablet cases, subcases and spatial organization carried relations that later writing could encode more linguistically.
- Rare rebus/phonetic uses appear early, but consistent phonetic writing becomes evident mainly in the third millennium BCE.
- Cuneiform developed as a logo-syllabic system with semantic and phonological values, not as a stage naturally progressing toward alphabetic writing.
- Changes in metrology and sign standardization were pragmatic adaptations, not uniform replacement of old systems.

## Strongest evidence

- **The Origins of Writing:** paragraphs 62–69; limitation: Introductory; dates rounded.
- **Visible Language:** Mesopotamian writing essays; limitation: Catalogue compresses disagreements.
- **Numerical and Metrological Graphemes:** §3.5 and conclusions; limitation: Focuses on specific numerical systems.
- **Classifying and Comparing Early Writing Systems:** chapter summary; limitation: Accessible summary rather than full chapter.

## Contradictions and unknowns

- Layout conventions varied and do not map cleanly to spoken syntax.
- Dating and identification of individual early phonetic examples remain debated.
- Corpus gaps prevent a complete state-by-state reconstruction.

## Completion handoff

### Technical state changes

| Approximate state | Medium and sign practice | Relation to language | Demonstrated capacity and limit |
|---|---|---|---|
| Uruk IV, c. 3350/3300–3200 BCE | drawn signs, numerical/metrological systems, compartmented tablets | underlying language often uncertain | classification, quantity and structured relations; limited continuous linguistic expression |
| Uruk III, c. 3200–3000 BCE | larger sign ecology and more regular layouts | rare phonetic/rebus readings remain debated | broader referential combinations; capability exceeds what can be securely read |
| Early Dynastic, third millennium BCE | increasingly impressed wedge ductus and changing sign conventions | Sumerian readings become more demonstrable | names, clauses and more explicit linguistic sequencing; use remains genre- and place-specific |
| Later third/second millennia BCE | mature logo-syllabic cuneiform | adapted for Akkadian and other languages | semantic plus syllabic expression; never an inevitable move toward alphabetic writing |

### Medium, sign and language distinctions

Clay and stylus constrain mark form; ductus is not language. A sign inventory and tablet layout are script organization; they do not identify the speaker population. Phonetic values link signs to language, but isolated rebus possibilities are weaker than repeated language-specific spellings.

### Capability limits

Observed sign frequency and position can reveal patterned structure without resolving readings. Conversely, a value available in the repertoire does not prove routine use. Numerical and metrological subsystems remain domain-dependent; standardization was incomplete and locally variable.

### Questions handed to WS05

Which functions are actually attested at each state? Which objects show repeated phonetic use rather than isolated possibility? When do legal, epistolary, literary and scholarly uses become corpus-visible, and are examples contemporary originals or later copies?

### Scope limits and dependencies

WS01 terminology and chronology remain locked. WS05 must establish uptake; WS07 owns later cross-language transmission. This workstream does not infer social consequence from technical possibility.
# END INPUT: 01_research/workstreams/WS03/synthesis.md

# BEGIN INPUT: 01_research/workstreams/WS04/synthesis.md
# Synthesis — WS04

Status: complete

## Answer

Writing was produced by small communities of trained specialists whose social location changed over time. The earliest scribes are visible mainly through their products, not biographies. By the later third and especially Old Babylonian periods, practice tablets and lexical/literary curricula reveal household- and institution-based training. ‘Edubba’ should not be projected backward as a uniform temple-school system, nor should modern mass-literacy categories be applied.

## Mechanism and chronology

- The earliest writing implies trained specialists, but their identities, recruitment and institutional status are poorly recoverable.
- The best archaeological evidence for formal curricula comes from later household and institutional contexts, especially the Old Babylonian period.
- Edubba was not necessarily a single standardized temple-run school system across Mesopotamian history.
- Scribal competence included copying, calculation, lexical knowledge and genre conventions, not merely decoding signs.
- Access was restricted and socially consequential, but no reliable percentage for literacy or a universal male-only rule can be derived.

## Strongest evidence

- **Masters’ Writings and Students’ Writings:** school material analysis; limitation: Focused mainly on later school corpora.
- **The Scribal Tablet-House in Ancient Mesopotamia:** pp. 305–332; limitation: Older and sometimes institutionally schematic.
- **DCCLT lexical introduction:** introductory sections; limitation: Public overview; not a demographic study.
- **Excursus: Scribes and Scribal Education:** chapter overview; limitation: Specific focus on composition and legal tradition.

## Contradictions and unknowns

- Lists and handwriting variation provide indirect evidence, not biographies.
- Literary school texts use institutional language, but excavated teaching often occurs in houses.
- Named female scribes and elite women exist in some periods; corpus is not population-representative.

## Completion handoff

### Actor and institution map by period

| Period | Actors visible | Institutional setting | Access/uncertainty |
|---|---|---|---|
| Uruk IV–III | anonymous trained producers inferred from tablets | administrative workshops/organizations reconstructed from products | identities, recruitment, gender and career paths unknown |
| Third millennium BCE | named scribes and officials appear unevenly; lexical traditions continue | temple, palace and administrative households vary by city | titles do not reveal all competent users |
| Old Babylonian | teachers, students, household heads and professional scribes become archaeologically clearer | household training such as House F plus institutional employment | best curricular evidence, but not a universal edubba model |
| Later second/first millennia | professional, scholarly, cultic and administrative specialists; some non-professional use | palaces, temples, families and provincial centers | highly regional; skill levels and access cannot be reduced to one literacy rate |

### Training mechanisms

Training combined copying from a master's model, sign and lexical lists, calculation/metrology, legal or administrative exercises, and later advanced literary/scholarly work. Household apprenticeship, institutional service and on-the-job learning coexist; they are not one standardized school pipeline.

### Human anchors

- **House F, Nippur — illustrative/high-resolution, not universal:** over 1,400 contextualized tablets show a household curriculum and expose the gap between literary school images and archaeology.
- **Tell Khaiber — illustrative regional counterexample:** titled scribes, apprentices and non-professional competence complicate a professional/non-literate binary.
- **Named women/female voices — exceptional or locally representative only when provenance permits:** demonstrate possible access, not a female literacy rate or automatic authorship.

### Access and unknowns

Access was unequal, but “literacy” must be decomposed into functional, technical and scholarly competences. Unknowns include population proportions, early recruitment and how much reading/writing occurred on perishable media.

### Scope limits and dependencies

WS05 owns genre/use chronology and final voice selection; WS06 owns consequences of restricted access; WS07 owns transmission across regions. No median social experience is claimed.
# END INPUT: 01_research/workstreams/WS04/synthesis.md

# BEGIN INPUT: 01_research/workstreams/WS05/synthesis.md
# Synthesis — WS05

Status: complete

## Answer

The preserved corpus expands from predominantly administrative records and lexical lists in Uruk IV–III to increasingly explicit royal, legal, epistolary, literary, religious and scholarly uses during the third and second millennia. Expansion was uneven: new genres did not replace accounting, and a text's existence does not prove it governed practice. Human voices are strongest where object identity, chronology, provenance, copy status and edition can be stated; even then, a document is mediated by genre and scribal practice.

## Mechanism and chronology

- Uruk IV evidence is overwhelmingly administrative, while lexical texts become substantially more visible in Uruk III.
- By the middle third millennium BCE cuneiform served economic, religious, political, literary and scholarly domains.
- Lexical lists form a continuous but repeatedly reorganized knowledge tradition.
- Letters and contracts provide human-scale cases but remain formulaic and institutionally situated.
- Functional expansion is successive addition and recombination, not a ladder from accounting to literature.

## Strongest evidence

- **P005390 / MMA 1988.433.2:** an Uruk III grain account with an object-level transliteration and qualified provenance.
- **MMA 86.11.111 / CTMMA I no. 69:** a dated Old Babylonian private letter with a specific sender, institutional problem and edition.
- **P228744 / Q000001:** a Nippur lexical school tablet tied to a defined curricular composite.
- **ETCSL 3.1.19:** a specific literary royal letter with a complete manuscript list, composite edition and translation, explicitly separated from its narrated Ur III setting.

## Contradictions and unknowns

- CDLI dates P005390 to Uruk III, ca. 3200–3000 BCE; the Met catalog uses Jemdet Nasr, ca. 3100–2900 BCE. Use the range/period labels, not a single exact year.
- First-person grammar is not transparent access to private interiority.
- Provenience for the two Met acquisition objects is qualified; P228744 lacks detailed findspot/stratigraphic metadata.
- The exact original composition date of ETCSL 3.1.19 is not established by its later surviving copies.

## Completion handoff

### Functional-turn chronology

| Horizon | Added or expanded function | Selected evidence | Boundary |
|---|---|---|---|
| Uruk III, ca. 3200–3000 BCE | administrative classification of grain and quantities | P005390 / MMA 1988.433.2 | transaction and language remain partly unreadable |
| Third millennium into Old Babylonian | royal, legal and epistolary forms become explicit | MMA 86.11.111, ca. 1632 BCE, as a later documentary anchor | one unusual letter cannot stand for all correspondence |
| Old Babylonian, ca. 1900–1600 BCE | formal lexical copying and curricular organization | P228744 / Q000001 from Nippur | evidence represents trained contexts, not mass literacy |
| Old Babylonian manuscript tradition | retrospective royal correspondence as literary/political memory | ETCSL 3.1.19 | composite of later copies, not an eyewitness Ur III dispatch |

### Bounded primary-text/object shortlist

| Selection and function | Date | Provenance and copy status | Edition / translation locator | Representativeness | Rights flag |
|---|---|---|---|---|---|
| **P005390 / MMA 1988.433.2 / MSVO 3 no. 79** — administrative grain account | CDLI: Uruk III, ca. 3200–3000 BCE; Met: ca. 3100–2900 BCE | Probably Uruk; CDLI marks provenience uncertain. Contemporary ancient tablet, not a later copy; language undetermined. | CDLI P005390, obv. cols. 1–2 and rev. cols. 1–2; MSVO 3 no. 79; CTMMA IV no. 180. | **Representative only of preserved early administrative recording**, not society or a securely reconstructed transaction. | Met images are **Public Domain**. Credit Met and object number. Cite CDLI transliteration; do not assume line-art rights. |
| **MMA 86.11.111 / CTMMA I no. 69** — Marduk-mushallim's private report letter | Old Babylonian, ca. 1632 BCE | Probably Sippar-Yahrurum; purchased 1886, no excavated context. Ancient documentary letter, not identified as a school copy. | CTMMA I no. 69, p. 87, pls. 63–64, 135–136; Met object overview summarizes sender, order and non-implementation. | **Exceptional/illustrative:** unusually exposes failure to carry out a royal security order; not ordinary correspondence. | Met images are **Public Domain**. Modern CTMMA/Met translation wording is not cleared for quotation; use attributed paraphrase pending rights check. |
| **P228744 / N 6052 (+) UM 29-16-393 / Q000001** — lexical school exercise | Old Babylonian, ca. 1900–1600 BCE | Excavated at Nippur; fragmented, obverse lost. A school copy/witness to OB Nippur Ura 03, not an authoritative “original.” | CDLI P228744, rev. cols. 1–2, preserved lines 4–30; composite score Q000001; DCCLT object link. | **Representative of formal Nippur lexical training only**, not all scribes or general access. | Cite CDLI/DCCLT text data. Photo is marked **© Penn Museum**; obtain permission/licence before image use. |
| **ETCSL 3.1.19, Letter from Puzur-Shulgi to Ibbi-Suen** — literary royal correspondence and social memory | Narrated setting: end of Ur III; surviving witnesses: Old Babylonian copies | Modern composite from multiple manuscripts. Principal/full witnesses include 3N-T311 = IM 58418 and IM 13347; not one contemporary dispatch. | ETCSL composite and translation, lines 1–53; bibliography lists every witness and print edition. | **Illustrative of retrospective scribal/political memory**, not eyewitness reporting or an unmediated authorial voice. | ETCSL translation is **copyrighted** and requires attribution; paraphrase unless quotation permission is cleared. Images depend on each holding institution. |

### Why these four and no more

The set is deliberately bounded. P005390 shows the early administrative baseline; MMA 86.11.111 shows a later documentary voice tied to command and reporting; P228744 shows knowledge organization through training; ETCSL 3.1.19 shows memory transformed by copying and modern reconstruction. Together they establish functional turns without becoming a genre catalogue.

### Economic, memory and knowledge cases

- **Economic:** P005390 stabilizes commodity/quantity relations, but whether that changed institutional action remains a WS06 question.
- **Knowledge:** P228744 links a physical student witness to a lexical series; WS04 owns the training community and WS07 later transmission.
- **Memory:** ETCSL 3.1.19 demonstrates that preservation is active copying and recomposition, not passive survival.
- **Epistolary action:** MMA 86.11.111 records reporting and an order's failed implementation; it therefore prevents equating a written command with compliance.

### Claims requiring WS06 tests

Whether accounts enlarged coordination, whether letters altered decisions, whose memories were selected, and who gained leverage from written claims remain consequence questions. WS05 establishes object, date, function and mediation; it does not prove power effects.

### Scope limits and dependencies

Composition date, manuscript date and modern reconstruction remain separate. Direct quotation and image reuse must follow the rights flags above. WS04 owns access/training communities, WS06 causal consequences and WS07 transmission. No other workstream is revised, and global synthesis has not been run.
# END INPUT: 01_research/workstreams/WS05/synthesis.md

# BEGIN INPUT: 01_research/workstreams/WS06/synthesis.md
# Synthesis — WS06

Status: complete

## Answer

Writing demonstrably enlarged institutional capacity when records were embedded in procedures: labor obligations could be quantified, accounts reconciled, property claims authenticated and distant transactions coordinated. But tablets did not act alone; scribes, seals, witnesses, archives and coercive institutions made records effective. Surviving archives are operational residues of organizations, not neutral samples of society, and they disproportionately expose those being counted through the categories of those doing the counting.

## Mechanism and chronology

- Administrative writing increased capacity to classify, aggregate and audit labor, goods and obligations when tied to institutional procedure.
- Ur III labor records reveal ordinary people mainly through top-down categories and required work.
- Writing’s power distribution changed over time: uses once concentrated in royal/institutional systems were later appropriated by urban private actors.
- A written law, norm or transaction is evidence of recording and claim-making, not automatic evidence of enforcement.
- Archive survival is structurally biased by clay durability, institutional discard, excavation history and antiquities-market provenance.

## Strongest evidence

- **An Interdisciplinary Overview of a Mesopotamian City and its Hinterlands:** §2.3 and archive discussion; limitation: Umma/Ur III case is not universal.
- **Equivalency Values and the Command Economy of the Ur III Period:** labor norms and equivalencies; limitation: Ur III is much later than writing’s origin.
- **Old Babylonian Networks of Urban Notables:** §1.2 and §2.4; limitation: Broad model debated; Old Babylonian focus.
- **Cuneiform Tablets in Collections at the University of Kansas:** §1.7 provenance warning; limitation: Collection-focused rather than archive theory.

## Contradictions and unknowns

- The scale and timing of ‘privatization’ vary by region.

## Completion handoff

### Tested causal cases with archive bias attached

| Case | Record-to-action chain | Distributional effect | Archive-bias limit |
|---|---|---|---|
| Ur III Umma labor/administration | categories and equivalencies → scribal accounts → institutional review/assignment | officials gain aggregate visibility; workers appear through imposed units | c. 27,500 known texts cover only about 45 years and a partial provincial archive |
| Puzriš-Dagan livestock agency | entries + seals + responsible officials → retrievable obligations/gifts → royal fiscal/diplomatic action | central court and officeholders gain coordination and claim capacity | 13,500+ texts reconstruct a repository; not a neutral census or literal stockyard |
| Old Babylonian private documents | contract/letter + witnesses/seals → claim presentation within urban networks | some private actors gain documentary leverage beyond royal institutions | urban notables and preserved transactions overrepresent successful/documented claims |

These are mechanisms, not claims that tablets acted independently. Tool affordance, human users and institutional enforcement remain separate links.

### Feedback loop to WS02

Supported direction: established institutions create demand for stable classifications and records. Qualified return direction: where records are embedded in authentication, retrieval and enforcement, they enlarge coordination and claim capacity. The loop is case-bound and cannot be projected wholesale onto the Uruk formation horizon.

### Counterexamples and limits

Written law or contract is not proof of enforcement. Oral bargaining, household practice, embodied expertise and unrecorded exchange continued. Private documentary use can widen leverage rather than only centralize it. Absence from an archive is not absence from society.

### Archive-bias rule

Every causal claim must state: what entered the archive, who selected it, why clay survived, how excavation/market provenance affects context, and which people or practices remain invisible.

### Scope limits and dependencies

WS02 supplies only the formation hypothesis; WS05 supplies use chronology. WS08 owns material afterlife and rediscovery. No population-wide claim is licensed by a single archive.
# END INPUT: 01_research/workstreams/WS06/synthesis.md

# BEGIN INPUT: 01_research/workstreams/WS07/synthesis.md
# Synthesis — WS07

Status: complete

## Answer

Cuneiform spread not as a fixed Sumerian package but through trained communities that adapted signs, values and curricula to new languages and institutions. Its decisive early adaptation was to Akkadian; later users included Elamite, Hittite, Hurrian and others. Sumerian continued after vernacular decline as a learned, copied and prestigious language. The living tradition persisted wherever institutions still trained readers and reproduced tablets.

## Mechanism and chronology

- Cuneiform was adapted from Sumerian-associated use to Akkadian and then to multiple unrelated languages.
- Adaptation required modification of sign values and orthographic conventions rather than simple substitution of words.
- Lexical lists and bilingual curricula were key transmission infrastructure across regions and centuries.
- Sumerian outlived probable vernacular use as a learned literary, cultic and scholarly language.
- The living-tradition endpoint is institutional reproduction: active teaching, copying and competent reuse, not the survival of old tablets alone.

## Strongest evidence

- **The Sumerian language:** full overview; limitation: Public overview.
- **DCCLT lexical introduction:** introduction; limitation: Lexical tradition focus.
- **Ancient Mesopotamia:** summary; limitation: Full chapter access limited.
- **A History of Hittite Literacy — Introduction:** introduction; limitation: Hittite-specific.

## Contradictions and unknowns

- The date and social extent of spoken-language decline remain debated.

## Completion handoff

### Transmission channels

Cuneiform moved through court and temple employment, imported or traveling specialists, diplomatic contact, copying, lexical/bilingual curricula and family or institutional apprenticeship. An artifact's presence shows contact; a sustained local corpus and training sequence are needed to show institutional reproduction.

### Adaptation cases and costs

| Case | What traveled | What changed or did not travel | Cost/limit |
|---|---|---|---|
| Akkadian adoption | sign repertoire and scribal practices | syllabic/phonological values expanded for a Semitic language | ambiguity and learned polyvalence |
| Hittite Anatolia | cuneiform, Akkadian/Sumerian curricular material and selected compositions | local Hittite conventions developed; Mesopotamian bookkeeping/metrology did not necessarily transfer | trained specialists, multilingual lists and court support |
| Sumerian after vernacular decline | learned language, lexical/literary/cultic repertoire | survival as scholarly content, not proof of everyday speech | continuous schooling and copying |

### Script, language and institution

Script survival means competent sign use; language survival may be vernacular or learned; institutional survival means communities can teach, copy, interpret and reuse. These timelines are related but not identical.

### Endpoint passed to WS08

The living tradition ends regionally when institutional reproduction—competent teaching, copying and reuse—can no longer be demonstrated. Surviving old tablets alone do not extend it. Late Babylonian temple/scholarly practice supplies the final positive evidence; WS08 must date contraction and the latest-known use without turning a discovery-sensitive tablet into an exact extinction date.

### Scope limits and unknowns

Elite archives overrepresent formal channels. Oral domains could remain broad even where cuneiform was active. WS08 owns cessation and recovery; this workstream does not claim a single endpoint year.
# END INPUT: 01_research/workstreams/WS07/synthesis.md

# BEGIN INPUT: 01_research/workstreams/WS08/synthesis.md
# Synthesis — WS08

Status: complete

## Answer

Cuneiform did not end in a single collapse. Its ecosystem contracted as Aramaic and alphabetic practices expanded, political and temple institutions changed, and specialist communities narrowed. Learned cuneiform survived in Babylonian scholarly/temple settings into the first centuries CE. After living competence disappeared, clay tablets persisted materially but became unreadable until nineteenth-century decipherment reconstructed the tradition. Its modern legacy is therefore recovery-mediated; direct lineage to modern writing is not established.

## Mechanism and chronology

- Cuneiform use contracted over centuries rather than ending through one event.
- Lexical and scholarly traditions persisted into the first centuries CE in narrowed institutional settings.
- Material tablets survived after living reading competence disappeared, creating a break between ancient transmission and modern knowledge.
- Nineteenth-century decipherment was cumulative and comparative, not a single eureka moment.
- Cuneiform’s defensible modern legacy is recovery-mediated knowledge of ancient societies and influence through ancient Near Eastern textual transmission; resemblance to digital record systems is analogy, not lineage.

## Strongest evidence

- **Ancient Mesopotamia:** summary; limitation: Full chapter access limited.
- **The Sumerian language:** overview; limitation: Public overview.
- **Art of the Ancient Near East: A Resource for Educators:** Cuneiform Messages, pp. 27–29; limitation: Educational compression.
- **Discoveries and Excavations — The City of Babylon:** chapter overview; limitation: Babylon-focused.

## Contradictions and unknowns

- Regional and genre-specific endpoints differ.
- Specific transmitted texts or concepts require separate chains of evidence.

## Completion handoff

### Decline mechanism set

Cuneiform's terminal contraction combined competition from Aramaic and Greek/alphabetic practices, changing political and economic institutions, narrowing temple/scholarly patronage, and the high cost of maintaining specialist multilingual training. Their relative importance varies; no single factor is sufficient everywhere.

### Final-use and loss chronology

- First millennium BCE: cuneiform remains active but increasingly concentrated in specialist administrative, temple and scholarly settings.
- First centuries BCE/CE: the final preserved corpora are especially astronomical/scholarly.
- **75 CE:** latest currently known dated tablet, not a guaranteed final act.
- After institutional reproduction ceases: tablets survive materially while reading competence is no longer demonstrable.

This uses WS07's endpoint—active teaching/copying/competent reuse—not mere object survival.

### Recovery chain

Early modern copies and observations made signs available; Old Persian was partially deciphered; the trilingual Behistun inscription enabled comparative testing; Akkadian readings were validated by multiple scholars and texts; Sumerian recognition and reconstruction followed through further corpus comparison. The chain is cumulative and error-correcting, not a single eureka.

### Legacy classification

| Class | Decision rule | Status |
|---|---|---|
| Direct ancient transmission | documented chain through intervening communities/texts | allow only case by case |
| Recovery-mediated influence | modern decipherment restores knowledge that then affects scholarship/culture | strongly supported |
| Analogy | formal resemblance without transmission chain, e.g. clay records vs databases | illustrative only; not historical lineage |

### Opening and ending anchors

Opening candidate: the 75 CE astronomical tablet as the latest-known trace of a shrinking competent community, explicitly discovery-sensitive. Ending candidate: a nineteenth-century comparative decipherment test that makes a previously mute clay archive readable again. Neither requires a general history of archaeology.

### Scope limits and unknowns

Local competence may have outlasted preserved dates; new finds can move the terminus. Specific legacy claims still require their own transmission evidence. Global synthesis has not been run.
# END INPUT: 01_research/workstreams/WS08/synthesis.md
