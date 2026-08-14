# Context Packet — T0008-research-workstream-WS08

- Product: `sumer-writing`
- Operation: `research_workstream`
- Unit: `WS08`
- Allowed writes: `01_research/workstreams/WS08/sources.json`, `01_research/workstreams/WS08/claims.json`, `01_research/workstreams/WS08/synthesis.md`, `tasks/T0008-research-workstream-WS08/report.md`, `tasks/T0008-research-workstream-WS08/operator-brief.json`

## Acceptance criteria
- Chỉ trả lời question của workstream hiện tại.
- Source có locator, authority và limitation.
- Claim tách fact/inference/contested/unknown và có counterevidence.
- Synthesis đủ dùng cho task sau mà không cần raw browsing context.

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

# BEGIN INSTRUCTION: system/operations/research-workstream.md
# Operation — Research Workstream

## Responsibility

Research đúng một workstream. Web notes và quá trình tìm kiếm không phải deliverable; các task sau chỉ nhận structured evidence và synthesis.

## Outputs

- `sources.json`: source records có ID namespaced `{WS##}-SRC-{###}`, type, authority, locators, access status, limitation và notes.
- `claims.json`: claim có ID namespaced `{WS##}-CLM-{###}`, classification, confidence, local source IDs, counterevidence, status và narrative implication.
- `synthesis.md`: tối đa khoảng 2.500 từ, trả question, nêu mechanism, chronology, strongest evidence, contradictions, unknowns và handoff cho synthesis toàn cục.

ID local được namespace để các workstream có thể chạy độc lập mà không collision. Operation `research_synthesis` sẽ cấp ID toàn cục và giữ provenance về ID local.

Không kể lại mọi nguồn. Không viết đoạn narration có thể copy thẳng vào script.
# END INSTRUCTION: system/operations/research-workstream.md

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

# BEGIN INPUT: 01_research/workstreams/WS08/brief.md
# WS08 — Decline, rediscovery and bounded legacy

## Question

Khi living cuneiform tradition suy tàn và biến mất, nó được recovered dưới điều kiện nào, và những legacy claim nào có transmission evidence thay vì chỉ analogy?

## In scope

Terminal ecosystem decline after WS07's living-tradition endpoint, final dated use, loss, material survival, excavation/decipherment, modern recovery and bounded legacy.

## Out of scope

Earlier multilingual adaptation owned by WS07, a full history of archaeology/Assyriology, or direct Sumer-to-smartphone lineage without transmission evidence.

## Ownership

Giải thích cessation, material survival and modern recovery; legacy claims phải tách direct transmission, recovery-mediated influence và analogy.

## Required evidence

- Late dated records
- Evidence for institutional/ecosystem decline
- Histories of excavation and decipherment
- Transmission-vs-analogy analysis

## Completion criteria

- Avoid monocausal ending
- Use the endpoint established with WS07
- Find opening/ending anchors without turning into a general archaeology history
- Classify and bound each legacy claim

## Required synthesis handoff

- Decline mechanism set
- Final-use and loss chronology
- Recovery chain
- Legacy claims classified by transmission strength
- Opening/ending anchor candidates

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
# END INPUT: 01_research/workstreams/WS08/brief.md
