# Context Packet — T0029-research-workstream-WS01

- Product: `sumer-writing`
- Operation: `research_workstream`
- Context profile: `research`
- Section: `-`
- Unit: `WS01`
- Allowed writes: `01_research/workstreams/WS01/sources.json`, `01_research/workstreams/WS01/claims.json`, `01_research/workstreams/WS01/materials.json`, `01_research/workstreams/WS01/synthesis.md`, `tasks/T0029-research-workstream-WS01/report.md`, `tasks/T0029-research-workstream-WS01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Only the material inside this packet is task context. Do not scan the repository.

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

# BEGIN INSTRUCTION: system/operations/research-workstream.md
# Operation — Research Workstream

## Responsibility

Research đúng một workstream. Web notes và quá trình tìm kiếm không phải deliverable; các task sau chỉ nhận structured evidence và synthesis.

## Outputs

- `sources.json`: source records có ID namespaced `{WS##}-SRC-{###}`, type, authority, locators, access status, limitation và notes.
- `claims.json`: claim có ID namespaced `{WS##}-CLM-{###}`, classification, confidence, local source IDs, counterevidence, status và narrative implication.
- `materials.json`: candidate material có ID namespaced `{WS##}-MAT-{###}` để giữ những vật liệu lịch sử cụ thể có thể mang một phần câu chuyện.
- `synthesis.md`: tối đa khoảng 2.500 từ, trả question, nêu mechanism, chronology, strongest evidence, contradictions, unknowns và handoff cho synthesis toàn cục.

ID local được namespace để các workstream có thể chạy độc lập mà không collision. Operation `research_synthesis` sẽ nhận ledger đã được remap và giữ provenance về ID local.

## Story material contract

`materials.json` không phải danh sách anecdote hay ý tưởng viết. Chỉ ghi một material candidate khi evidence đủ để lớp sau dựng lại nó mà không bịa.

Mỗi material gồm:

- `id`, `kind`, `label`;
- `what_audience_follows`: một câu ngắn mô tả vật thể, người, hành động, process, encounter, failure, consequence hoặc sequence mà audience thực sự có thể theo;
- `sequence`: các bước hoặc thay đổi được evidence hỗ trợ, theo thứ tự nếu có;
- `claim_ids`: local claim IDs giới hạn điều có thể khẳng định;
- `source_refs`: local source ID kèm locator hẹp cho chính material này;
- `representativeness`: representative, exceptional, illustrative hoặc unknown;
- `limitations`: điều không được suy rộng hoặc chi tiết chưa chắc.

Locator của material phải đủ hẹp để truy lại chi tiết cần dùng. Page range rộng có thể support synthesis claim nhưng không đủ để coi là material evidence.

Một workstream có thể bàn giao `materials: []` nếu không có candidate đủ chắc. Không ép mọi workstream phải tìm người, scene hay event.

## Preserve usable historical material

Đừng chỉ bàn giao kết luận trừu tượng. Khi evidence cho phép, `synthesis.md` phải gọi đúng material ID và giải thích nó có thể giúp audience theo sự thay đổi nào.

`narrative_implication` của claim không phải prose để copy vào script. Nó chỉ nói claim support phần nào của object/process/consequence và giới hạn nào phải giữ.

Không kể lại mọi nguồn. Không viết narration có thể copy thẳng vào script. Không săn anecdote chỉ vì hấp dẫn nếu provenance hoặc representativeness yếu.
# END INSTRUCTION: system/operations/research-workstream.md

# BEGIN INPUT: 01_research/rework-request.md
# Research Rework Request — C003

Requested by: user

Requested at: 2026-08-18T20:27:00+07:00

## Goal

Rework the research handoff for the entire Sumer-writing product before rebuilding the outline. The current research contains strong analytical claims, but the production pipeline did not preserve enough concrete historical material for the outline to preview the story reliably.

## Required approach

- Review WS01–WS08 under the current material-aware research contract.
- Preserve existing sources, claims, qualifications and synthesis when they remain valid; do not research from zero or rewrite unrelated work for style.
- For each workstream, create or complete `materials.json` using only evidence strong enough to reconstruct a concrete object, person, action, process, documented encounter, failure, consequence or supported sequence.
- Reuse existing sources first. Open additional research only where current locators or evidence are insufficient to support a needed material candidate.
- Give material evidence narrow, retrievable locators and keep observation separate from scholarly or causal inference.
- It is valid for a workstream to return no strong material candidate; record the gap instead of inventing narrative material.
- The goal is not to preserve the current nine-section outline. After all workstreams are reworked, research synthesis and the full outline will be rebuilt from the resulting evidence and story-material map.

## Execution order

Rework one workstream per canonical `research_workstream` task, WS01 through WS08 unless evidence dependencies justify a documented change of order. After all eight are complete, run consolidation and `research_synthesis`, then rebuild the whole outline. Do not draft or redesign individual sections during this research rework.
# END INPUT: 01_research/rework-request.md

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

# BEGIN INPUT: 01_research/workstreams/WS01/brief.md
# WS01 — Definition, chronology and attribution

## Question

Thế nào được tính là writing, các mốc earliest evidence là gì, và attribution cho Sumer/Uruk chắc đến đâu?

## In scope

Definitions, proto-cuneiform threshold, dating, archaeological context, comparative attribution.

## Out of scope

Formation mechanism, full development of later genres or scribal institutions.

## Ownership

Thiết lập vocabulary, chronology ranges và mức chắc chắn của first/invented/attribution claims; không kết luận vì sao writing hình thành.

## Required evidence

- Primary archaeological/corpus evidence
- Recent scholarly synthesis
- Competing definitions and chronologies

## Completion criteria

- Qualify first/invented claim
- Produce chronology ranges
- List unresolved attribution issues

## Required synthesis handoff

- Working definitions and terminology warnings
- Chronology ranges with confidence
- Attribution disputes
- Boundary conditions for WS02 and WS03

## Shared research protocol

### Chronology

- Dùng date range và archaeological period khi chronology còn tranh luận; không biến approximate date thành một năm chính xác.
- Mọi workstream phải phân biệt evidence đương thời, retrospective copy và modern reconstruction.

### Terminology

- Phân biệt Sumerian language, Sumerian population label, proto-cuneiform, cuneiform, script, writing và literacy.
- Thuật ngữ gây tranh luận phải dùng định nghĩa/qualification do WS01 thiết lập; bất đồng được giữ lại cho synthesis thay vì tự chuẩn hóa.

### Case selection

- Ưu tiên case có provenance, chronology, primary evidence và khả năng kiểm tra causal mechanism; narrative value không đủ để chọn case.
- Ghi rõ case là representative, exceptional hay chỉ illustrative; không suy rộng từ một archive, city hoặc elite corpus.
- Ưu tiên một số địa điểm/thời kỳ có thể nối xuyên workstream khi evidence cho phép, nhưng không ép continuity giả.

### Cross-cutting ownership

- **exchange:** WS02 sở hữu vai trò của exchange/accounting trong formation; WS05 lập chronology các use case kinh tế; WS06 chỉ đánh giá effect lên obligation, ownership, standardization hoặc institutional action khi có case evidence.
- **social_memory:** WS05 xác định các form/genre dùng để lưu và tái tạo memory; WS06 đánh giá selection, erasure và political consequences; WS08 chỉ xử lý survival, loss và modern recovery.
- **knowledge_transmission:** WS04 sở hữu training/community of practice; WS05 sở hữu lexical/curricular content và functional expansion; WS07 sở hữu transmission qua language, region và institution. Synthesis nối ba lớp này.

### Common handoff contract

- Mỗi workstream bàn giao chronology ranges, supported claims, disputed claims, unknowns, selected cases, scope limits và dependencies on other workstreams.
- Mỗi claim phân biệt observation, scholarly inference và causal inference; nêu counterevidence hoặc alternative explanation khi có.
- Không workstream nào tự giải quyết contradiction thuộc ownership của workstream khác; contradiction được chuyển rõ cho research synthesis.
# END INPUT: 01_research/workstreams/WS01/brief.md

# BEGIN INPUT: 01_research/workstreams/WS01/sources.json
{
  "schema_version": 1,
  "workstream": "WS01",
  "status": "complete",
  "sources": [
    {
      "id": "WS01-SRC-001",
      "title": "Proto-Cuneiform Account-Books and Journals",
      "author": "Robert K. Englund",
      "year": 2004,
      "type": "scholarly chapter / corpus synthesis",
      "authority": "Leading specialist synthesis grounded in the archaic tablet corpus and CDLI work.",
      "url": "https://cdli.earth/files-up/publications/englund2004a.pdf",
      "locators": ["pp. 24–27 (PDF pp. 2–5), especially chronology figure and discussion of Uruk IV/III corpus"],
      "status": "reviewed",
      "limitations": "Chronological ranges and corpus counts reflect the state of publication in 2004; some causal interpretation belongs to WS02.",
      "notes": "Supports ca. 3300 BCE emergence, relative Uruk IV→III sequence, overwhelmingly administrative earliest corpus, and caution around token continuity."
    },
    {
      "id": "WS01-SRC-002",
      "title": "Uruk and I",
      "author": "Hans J. Nissen",
      "year": 2024,
      "type": "scholarly excavation historiography",
      "authority": "CDLI Journal article by a senior Uruk specialist auditing excavation records and chronology.",
      "url": "https://cdli.earth/articles/cdlj/2024-1",
      "locators": ["§15.8; §16.1–16.4; §17.3; §18.2"],
      "status": "reviewed",
      "limitations": "Author explicitly foregrounds failures in legacy excavation documentation; exact absolute dates remain model-dependent.",
      "notes": "Uruk IVa is the most probable archaeological placement of the oldest script, slightly earlier cannot be excluded; find context is often insufficient and unreliable."
    },
    {
      "id": "WS01-SRC-003",
      "title": "Writing in Early Mesopotamia: Beyond the Meme",
      "author": "Massimo Maiocchi",
      "year": 2019,
      "type": "peer-reviewed scholarly chapter",
      "authority": "Assyriological synthesis focused on early Mesopotamian writing, semiotics and material systems.",
      "url": "https://iris.unive.it/retrieve/e4239dde-83dd-7180-e053-3705fe0a3322/Maiocchi%20M.%202019%2C%20Writing%20in%20Early%20Mesopotamia%20--%20Beyond%20the%20Meme.pdf",
      "locators": ["pp. 410–412 (PDF pp. 15–17), especially discussion of glottographic/semasiographic boundary"],
      "status": "reviewed",
      "limitations": "The chapter advocates a fluid continuum; terminology is analytical rather than a universally accepted threshold definition.",
      "notes": "Useful counterweight to a binary true-writing/proto-writing distinction and to a linear token→tablet story."
    },
    {
      "id": "WS01-SRC-004",
      "title": "The Origins of Writing",
      "author": "Ira Spar",
      "year": 2004,
      "type": "museum scholarly essay",
      "authority": "Metropolitan Museum of Art Heilbrunn Timeline essay by a cuneiform specialist.",
      "url": "https://www.metmuseum.org/essays/the-origins-of-writing",
      "locators": ["paragraphs 62–69"],
      "status": "reviewed",
      "limitations": "Introductory synthesis and now older; statements about possible mid-fourth-millennium Syrian/Turkish systems are provisional.",
      "notes": "States that Sumerian identification of Uruk tablets is popular but not universal; phonetic use is sparse before 3000 and consistently apparent much later."
    },
    {
      "id": "WS01-SRC-005",
      "title": "Visible Language: Inventions of Writing in the Ancient Middle East and Beyond",
      "author": "Christopher Woods (ed.)",
      "year": 2010,
      "type": "academic museum catalogue / comparative synthesis",
      "authority": "University of Chicago Oriental Institute catalogue curated by a Sumerologist.",
      "url": "https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/oimp32.pdf",
      "locators": ["comparative chronology and essays on earliest Mesopotamian and Egyptian writing; catalogue overview"],
      "status": "reviewed",
      "limitations": "Catalogue compresses specialist disagreements for comparative presentation; use for comparison scope, not exact Uruk stratigraphy.",
      "notes": "Treats Mesopotamia and Egypt as roughly contemporary independent inventions; supports avoiding an unqualified unique 'world first' claim."
    },
    {
      "id": "WS01-SRC-006",
      "title": "Visible Language exhibition overview",
      "author": "Institute for the Study of Ancient Cultures, University of Chicago",
      "year": 2010,
      "type": "academic institutional overview",
      "authority": "Official ISAC summary of the Woods-curated exhibition.",
      "url": "https://isac.uchicago.edu/museum-exhibits/visible-language-inventions-writing-ancient-middle-east-fall-2010",
      "locators": ["paragraphs 46–51"],
      "status": "reviewed",
      "limitations": "Public-facing overview rather than full argument; dates are rounded.",
      "notes": "Places Mesopotamian tablets around 3200 BCE and early Egyptian tags around 3320 BCE, illustrating why 'first' depends on definition and dating."
    },
    {
      "id": "WS01-SRC-007",
      "title": "The State of Decipherment of Proto-Elamite",
      "author": "Robert K. Englund",
      "year": 2004,
      "type": "scholarly chapter / comparative script study",
      "authority": "Corpus-based comparison by a leading proto-cuneiform and proto-Elamite specialist.",
      "url": "https://cdli.earth/files-up/publications/englund2004c.pdf",
      "locators": ["pp. 124–127 and 139–140 (PDF pp. 24–27, 39–40)"],
      "status": "reviewed",
      "limitations": "Proto-Elamite comparison is secondary to WS01 and does not establish the spoken language of Uruk scribes.",
      "notes": "Supports relative order Uruk IV before Uruk III and contemporaneity/contact with proto-Elamite; shows attribution is regional and transmissional, not a simple ethnic label."
    },
    {
      "id": "WS01-SRC-008",
      "title": "The Origins of Writing",
      "author": "Metropolitan Museum of Art, object and corpus context",
      "year": 2004,
      "type": "museum corpus overview",
      "authority": "Major museum collection context linked to excavated and collected early tablets.",
      "url": "https://www.metmuseum.org/art/collection/search/327385",
      "locators": ["object description: earliest tablets around 3300 BCE; two early phases"],
      "status": "reviewed",
      "limitations": "Single object is illustrative, not representative; provenance and dating of market-derived tablets can be weaker than excavated material.",
      "notes": "Material anchor for the approximate 3300 BCE date and phase distinction."
    }
  ]
}
# END INPUT: 01_research/workstreams/WS01/sources.json

# BEGIN INPUT: 01_research/workstreams/WS01/claims.json
{
  "schema_version": 1,
  "workstream": "WS01",
  "status": "complete",
  "claims": [
    {"id":"WS01-CLM-001","statement":"For this project, 'writing' should be treated as a graded analytical threshold: durable conventional marks that encode repeatable linguistic or lexical values count as writing, while devices that communicate quantities or meanings without demonstrable language encoding remain accounting/proto-writing; proto-cuneiform lies across this disputed boundary.","type":"contested","confidence":"medium","status":"qualified","sources":["WS01-SRC-003","WS01-SRC-004","WS01-SRC-005"],"counterevidence":"A strict glottographic definition excludes much earliest proto-cuneiform; broader functional definitions include it because it records words/categories and develops directly into cuneiform.","narrative_implication":"Never let one definition silently decide who invented writing or its exact birthday."},
    {"id":"WS01-CLM-002","statement":"The earliest substantial proto-cuneiform horizon is conventionally placed near the end of the Late Uruk period, approximately 3350/3300–3200 BCE (Uruk IV), followed by Uruk III/Jemdet Nasr approximately 3200–3000 BCE.","type":"fact","confidence":"high","status":"qualified","sources":["WS01-SRC-001","WS01-SRC-002","WS01-SRC-008"],"counterevidence":"Absolute ranges vary among chronologies, and poor excavation records prevent a precise first year; a slightly earlier date cannot be excluded.","narrative_implication":"Use ranges and archaeological phases, never a single invention year."},
    {"id":"WS01-CLM-003","statement":"Uruk IVa is the most probable context for the oldest script at Uruk, but the original find documentation is too weak to make the stratigraphic placement definitive.","type":"fact","confidence":"high","status":"supported","sources":["WS01-SRC-002"],"counterevidence":"No corrective reconstruction can fully repair the deficient find-spot and architectural documentation.","narrative_implication":"The uncertainty is archaeological, not merely rhetorical caution."},
    {"id":"WS01-CLM-004","statement":"The earliest Uruk IV corpus known to scholarship is overwhelmingly administrative; lexical texts become materially more visible in Uruk III.","type":"fact","confidence":"high","status":"supported","sources":["WS01-SRC-001"],"counterevidence":"Survival and excavation bias mean the preserved corpus cannot prove that no other uses or media existed.","narrative_implication":"Early evidence supports an administrative center of gravity, not the claim that administration was the only origin or use."},
    {"id":"WS01-CLM-005","statement":"Calling the earliest system 'cuneiform' is potentially anachronistic: proto-cuneiform signs were initially drawn/incised and only later acquired the systematic wedge-impressed form associated with mature cuneiform.","type":"fact","confidence":"high","status":"supported","sources":["WS01-SRC-003","WS01-SRC-004"],"counterevidence":"Scholarly convention uses proto-cuneiform to name the ancestral system, so the term remains useful when explicitly qualified.","narrative_implication":"Distinguish proto-cuneiform from later wedge-shaped cuneiform in terminology and visuals."},
    {"id":"WS01-CLM-006","statement":"The language underlying Uruk IV–III proto-cuneiform cannot be securely identified as Sumerian because the texts encode little phonology and can often be interpreted without recovering continuous speech.","type":"contested","confidence":"high","status":"qualified","sources":["WS01-SRC-003","WS01-SRC-004"],"counterevidence":"Some rare rebus/phonetic readings may fit Sumerian, and the later descendant script unquestionably writes Sumerian; this makes Sumerian plausible but not demonstrated for the earliest horizon.","narrative_implication":"Do not convert 'found in southern Mesopotamia/Uruk' into 'written by ethnic Sumerians in Sumerian'."},
    {"id":"WS01-CLM-007","statement":"The safest attribution is regional and institutional: proto-cuneiform is first securely attested as a large corpus in the Uruk cultural sphere of southern Mesopotamia, especially Uruk, rather than securely attributable to a named ethnic population.","type":"inference","confidence":"high","status":"qualified","sources":["WS01-SRC-001","WS01-SRC-002","WS01-SRC-004","WS01-SRC-007"],"counterevidence":"Uruk's corpus dominance may partly reflect excavation and preservation; related early practices are attested beyond Uruk and transmitted toward Susiana/Iran.","narrative_implication":"Use 'Uruk/southern Mesopotamian tradition' for the earliest phase; reserve 'Sumerian writing' for contexts with linguistic evidence."},
    {"id":"WS01-CLM-008","statement":"An unqualified claim that Sumer or Uruk produced the world's first writing is not defensible, because early Egyptian writing at Abydos overlaps the late-fourth-millennium date range and priority depends on calibration and definition.","type":"contested","confidence":"high","status":"qualified","sources":["WS01-SRC-005","WS01-SRC-006"],"counterevidence":"Uruk provides one of the earliest and by far the largest early corpora and may precede Egyptian material under some chronologies; neither establishes a universally accepted single winner.","narrative_implication":"Claim 'one of the earliest independently developed writing traditions' or 'earliest large writing corpus', not an uncontested world first."},
    {"id":"WS01-CLM-009","statement":"The relative sequence Uruk IV proto-cuneiform → Uruk III proto-cuneiform → later language-explicit cuneiform is much more secure than the absolute dates or a sharp boundary between proto-writing and writing.","type":"inference","confidence":"high","status":"supported","sources":["WS01-SRC-001","WS01-SRC-002","WS01-SRC-003","WS01-SRC-007"],"counterevidence":"Local corpora and cross-regional contacts complicate a single linear sequence, and the exact transition to language-explicit writing is gradual.","narrative_implication":"Organize chronology by states and transitions rather than invention moments."},
    {"id":"WS01-CLM-010","statement":"The claim 'Sumer invented writing' should remain rejected as a premise fact but retained as a researchable shorthand whose components—place, system, language, population and priority—must be tested separately.","type":"inference","confidence":"high","status":"supported","sources":["WS01-SRC-002","WS01-SRC-004","WS01-SRC-005","WS01-SRC-006"],"counterevidence":"Public and some scholarly summaries still use 'Sumerian invention' because the later continuity into Sumerian cuneiform is strong and convenient.","narrative_implication":"The central narrative payoff can emerge from dismantling and rebuilding this familiar sentence with precise qualifiers."}
  ]
}
# END INPUT: 01_research/workstreams/WS01/claims.json

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
