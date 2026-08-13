# Context Packet — T0021-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0021-draft-section-P01/report.md`, `tasks/T0021-draft-section-P01/operator-brief.json`

## Acceptance criteria

- Chỉ viết section được chỉ định.
- Chỉ dùng claim được story plan chọn; narration pack là trần, không phải checklist.
- Entry/exit state và bridge đúng brief.
- Văn nói phổ thông truyền đạt được governing idea; handoff không thay thế draft.

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
14. Evidence completeness thuộc research artifact; narration không có nghĩa vụ kể mọi claim trong packet.
15. Draft chỉ được bắt đầu sau khi story plan được con người duyệt và narration pack được sinh tự động.

## Artifact boundary

- Research tạo evidence, không tạo narration.
- Outline tạo section contracts, không tạo prose.
- Story design chọn fact và beats, không viết prose.
- Draft tạo prose một section, không review/approve.
- Review tạo diagnosis, không rewrite.
- Revision sửa đúng issue đã duyệt, không “polish toàn bộ”.
- Integration tìm dependency conflict qua handoff trước, không tái sinh script.
# END INSTRUCTION: system/core/invariants.md

# BEGIN INSTRUCTION: system/standards/story.md
# Story Standard

## Causal spine

Story phải giải thích pressure nào tạo mechanism mới; mechanism đổi capacity/incentive của ai; hệ quả và adaptation nào biến state A thành B.

Toàn kịch bản được thiết kế theo hai tầng:

- **narrative movement:** nhịp lớn mà khán giả cảm nhận;
- **production section (`P##`):** work unit giới hạn context, review và revision.

Hai tầng không bắt buộc một-một. Section count không phải mục tiêu thẩm mỹ và không được chọn trước để chia đều thời lượng. Mỗi section contract có:

- một narrative job;
- entry/exit state;
- central question/payoff;
- claim IDs;
- material/human anchor có provenance;
- dependencies và bridge;
- word budget;
- lý do budget và phác họa shape riêng;
- boundary: điều cố ý chưa giải thích.

## Long-form rhythm

Luân phiên có chủ đích:

`human/object → institution → system → human consequence`

Entity được giới thiệu theo `FUNCTION → NAME → thuộc tính cần cho hành động kế tiếp`.

Opening thiết lập object, causal tension, stakes và boundary. Ending trả causal question và legacy có mắt xích; không chỉ recap hay “bài học lịch sử” chung chung.

## Story trước, fact sau

Evidence pack xác định những gì có thể nói đúng. Nó không xác định những gì khán giả cần nghe.

Trước khi viết prose, section phải có story plan được con người duyệt. Story plan phải:

- diễn đạt một governing idea bằng ngôn ngữ phổ thông;
- xác định câu hỏi khán giả mang theo và điều họ hiểu ra ở cuối section;
- phân mọi claim thành `narrated`, `support`, `guardrail` hoặc `omit`;
- chỉ chọn 1–5 claim làm xương sống narration;
- giải thích narrative job của từng claim được giữ;
- sắp beat theo tension và consequence, không theo thứ tự claim hoặc source.
- tự chọn số beat và shape phù hợp; chỉ payoff là bắt buộc, tension/bridge không phải ô phải điền.

Word budget là giả thuyết ở outline, không phải quota. Story design phải đề xuất lại range khi material không đủ hoặc narrative hinge cần thêm không gian. Draft không được lặp ý, thêm fact hay kéo dài câu chỉ để chạm min words.

Một fact chỉ đáng xuất hiện trong narration nếu nó làm ít nhất một việc: tạo câu hỏi, tăng tension, giải thích mechanism, thay đổi cách hiểu, cho thấy consequence hoặc mở bridge cần thiết. Fact chỉ dùng để bảo vệ độ chính xác thường nên ở dạng guardrail và không cần được đọc thành lời.

## Narrative movement

Toàn arc thường cần các chức năng dưới đây, nhưng một section riêng không phải lặp nguyên chuỗi:

`vật/người cụ thể → vấn đề chưa giải được → evidence đổi mô hình → hệ quả đối với người hoặc hệ thống`

Không dùng một object làm cái cớ để lần lượt trình bày toàn bộ niên đại, thuật ngữ, tranh luận và disclaimer có trong packet. Mỗi đoạn phải khiến câu chuyện tiến lên, không chỉ làm hồ sơ dày thêm.
# END INSTRUCTION: system/standards/story.md

# BEGIN INSTRUCTION: system/standards/voice.md
# Channel Voice Standard

## Voice identity

Giọng kênh là **điềm tĩnh, sáng rõ, giàu sức nặng và có tính điều tra**. Người kể không biểu diễn mình thông thái; họ dẫn khán giả nhìn một vật thể hoặc hành động cụ thể, nhận ra một vấn đề, rồi theo hệ quả của nó lên quy mô thiết chế và văn minh.

Mỗi movement ưu tiên:

`điều cụ thể có thể thấy → điều chưa giải thích được → phát hiện làm đổi cách hiểu → hệ quả đối với con người/hệ thống`

Storytelling không đòi hỏi bịa scene hay nhân vật. Tension có thể đến từ giới hạn của hiện vật, xung đột giữa hai cách giải thích, một cơ chế thất bại, hoặc khoảng cách giữa điều con người muốn làm và điều hệ thống cho phép.

## Voice fingerprint

- **Vai người kể:** một người điều tra kiên nhẫn đang cùng khán giả giải một vấn đề, không phải giảng viên đang chứng minh vốn hiểu biết.
- **Thứ tự ưu tiên:** clarity trước sophistication; causality trước chronology; consequence trước trivia; con người được nhìn bên trong hệ thống.
- **Đơn vị nhịp:** một chi tiết cụ thể, một complication, một explanatory turn, rồi một consequence. Không bắt buộc bốn câu, nhưng phải cảm nhận được chuyển động này.
- **Scale:** bắt đầu đủ gần để hình dung, lùi ra khi mechanism cần giải thích, rồi trở lại điều mechanism làm được hoặc gây ra cho con người.
- **Sức nặng:** đến từ điều đã xảy ra và cái giá của nó; người kể không dùng mỹ từ để ra lệnh cho khán giả xúc động.
- **Thái độ với uncertainty:** nói ngắn gọn điều chưa biết, sau đó cho thấy nó thay đổi kết luận nào. Không xếp disclaimer thành một đoạn phòng thủ.

## Spoken Vietnamese

- Dùng từ thông thường trước; thuật ngữ chỉ xuất hiện khi không thể thay và phải được giải thích ngay bằng lời phổ thông.
- Tránh chuỗi danh từ trừu tượng, calque học thuật và code-switching như `corpus`, `horizon`, `relations`, `capacity` trong narration.
- Một đoạn chỉ gánh một bước thay đổi trong cách hiểu. Nếu khán giả không thể kể lại ý đoạn bằng một câu đơn giản, đoạn đó chưa đạt.
- Dùng động từ và chủ thể cụ thể. Không để qualification nối tiếp qualification thành giọng phòng thủ.
- Nhịp câu có tương phản: câu giải thích có thể dài hơn, nhưng phát hiện hoặc consequence cần câu gọn và rõ.

## Fact selection

Research completeness nằm trong repo, không nằm trong narration. Một fact không được đọc lên chỉ vì nó đúng hoặc có trong context.

Fact chỉ được giữ khi nó làm ít nhất một việc:

1. làm câu hỏi trở nên cấp thiết hơn;
2. tạo hoặc giải quyết tension;
3. chứng minh mechanism;
4. làm thay đổi state hiểu của khán giả;
5. tạo consequence hoặc bridge cần thiết.

Fact dùng để chặn overclaim thường là `guardrail`: nó điều chỉnh câu chữ phía sau, không cần biến thành một đoạn giải thích riêng.

## Learning from benchmarks

Được học từ major history channels ở cấp **chức năng**:

- giữ một material/human anchor xuyên movement;
- tạo causal macro arc dễ theo dõi;
- chuyển scale giữa đời sống, thiết chế và hệ thống;
- để emotional weight đến từ consequence có evidence;
- dùng primary voice/object như điểm hiện diện của con người.

Mỗi thuộc tính vay mượn phải được chuyển thành constraint trung tính rồi thể hiện bằng cấu trúc và câu chữ nguyên bản của kênh. Không sao chép wording, cadence, motif mở đầu, chapter order, narrator persona hoặc signature transition của một creator cụ thể.

Mỗi product phải có `voice-profile.md`. Profile không phải lời nhắc “viết giống kênh X”; nó là bản dịch có kiểm soát từ benchmark sang các chức năng ta muốn học, cách thể hiện nguyên bản bằng tiếng Việt, điều cấm mô phỏng và các test dùng khi review draft.

## Failure modes

- Mở bằng catalogue: tên bảo tàng, mã số, niên đại nối tiếp trước khi có tension.
- Dùng một hiện vật làm cái cớ để đọc toàn bộ evidence pack.
- Tổ chức đoạn theo claim/source thay vì progression của câu chuyện.
- Liên tục nói điều ta không biết mà không cho thấy uncertainty làm thay đổi câu chuyện thế nào.
- Kết thúc bằng abstraction khái quát mà khán giả không thể hình dung consequence.
- Đúng fact nhưng không rõ tác giả muốn khán giả hiểu điều gì.
# END INSTRUCTION: system/standards/voice.md

# BEGIN INSTRUCTION: system/standards/writing-vi.md
# Vietnamese Narration Standard

- Viết để nói thành tiếng: rõ, chính xác, giàu hình ảnh có chứng cứ.
- Một câu gánh một quan hệ logic chính; sau chuỗi tên/ngày phải giải thích consequence.
- Dùng động từ cụ thể thay tính từ đánh giá.
- Cảm xúc đến từ tình thế lịch sử, không từ hyperbole.
- Không dùng câu cụt, dấu ba chấm hoặc câu hỏi tu từ như công thức “cinematic”.
- Mỗi đoạn phải dựng scene, giải thích mechanism, đưa evidence, xử lý contradiction, chuyển scale, payoff hoặc handoff.
- Dùng `chúng ta biết`, `bằng chứng cho thấy`, `một cách giải thích cho rằng`, `chưa thể xác định` đúng mức certainty.
- Quote chỉ ở lại khi voice/evidence mất đi nếu paraphrase; không hiện đại hóa nghĩa của văn bản cổ.
- Không mô phỏng giọng của *Fall of Civilizations* hay creator khác.
- Narration pack là trần sự thật, không phải checklist. Claim `support` chỉ dùng khi câu chuyện thực sự cần thêm độ chính xác; claim `guardrail` không được biến thành đoạn thuyết minh; claim `omit` không xuất hiện.
- Ưu tiên từ phổ thông. Thuật ngữ học thuật hoặc từ dịch sát tiếng Anh chỉ được giữ khi không có cách nói thường ngày đủ chính xác, và phải được giải thích ngay lần đầu.
- Mỗi đoạn chỉ gánh một bước thay đổi trong hiểu biết. Người nghe phải có thể trả lời: “Tôi vừa hiểu thêm điều gì, và vì sao điều đó dẫn sang đoạn kế tiếp?”
- Sau bản nháp, paraphrase test từng đoạn bằng một câu nói đời thường. Nếu không làm được, đoạn đó đang quá trừu tượng hoặc chưa có ý đồ rõ.
- Không xếp fact theo thứ tự packet, claim ID, source hoặc chronology nếu thứ tự đó không tạo ra tension và payoff.
# END INSTRUCTION: system/standards/writing-vi.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Responsibility

Viết narration cho đúng một section từ story plan đã được duyệt và narration pack đã đóng gói.

## Rules

- Không mở source index hoặc raw workstreams ngoài packet.
- Đi theo logic của story beats nhưng không biến tên beat thành đề mục hay viết như điền biểu mẫu.
- Narration pack là ceiling, không phải checklist. Không buộc mọi support claim xuất hiện; guardrail chỉ giới hạn cách diễn đạt; omitted claim phải ở ngoài draft.
- Không giải thích nội dung đã được boundary giao cho section khác.
- Nếu narration pack thiếu claim cần thiết, ghi blocker; không tự research hoặc kéo claim đã bị loại trở lại.
- Draft phải đạt entry→exit state, narrative job, payoff và word budget.
- Opening phải tạo ra vấn đề cần theo dõi, không mở như bản mô tả hiện vật. Ending phải trả payoff cụ thể, không kết bằng khái quát trừu tượng.
- Chỉ giữ chi tiết khi người nghe cần nó để hiểu hành động, mechanism hoặc consequence tiếp theo.
- Comment biên tập cho quote/claim locator được phép; không để citation phá narration.

## Handoff

`handoff.md` tối đa 500 từ, gồm state đạt được, entities/terms đã giới thiệu, setup chưa payoff, fact continuity và bridge mong đợi. Không tóm tắt toàn bộ prose.
# END INSTRUCTION: system/operations/draft-section.md

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

# BEGIN INPUT: 02_outline/story-bible.md
# Story Bible — Sumer Writing

Status: draft

## Premise

Một hệ ghi dấu ban đầu chỉ lưu selected quantities, categories và relations đã trở thành hạ tầng cho action, knowledge và memory như thế nào—và vì sao nó sống lâu hơn các xã hội đầu tiên tạo ra nó?

Title question là proposition được kiểm nghiệm. Payoff: **writing không đơn độc tạo civilization; institutions và record practices co-developed, rồi records embedded in people, procedures and archives multiplied bounded capacities.**

## Causal spine

institutional scale pressure → information ecology → expanding graphic/language capacity → functional uptake → trained communities → procedural embedding → capacity/power feedback → adaptation → contraction → competence break → recovery-mediated legacy

Continuity nằm ở a reproducible practice of turning selected relations into durable, standardized and retrievable marks, maintained by communities able to interpret and act on them.

## Global chronology

- Pre/Late Uruk: tokens, bullae, seals, images, numerical and metrological practices coexist.
- Uruk IV, c. 3350/3300–3200 BCE: earliest substantial proto-cuneiform horizon.
- Uruk III/Jemdet Nasr, c. 3200–3000 BCE: larger corpus, more visible lexical material.
- Third millennium BCE: wedge ductus and language-explicit logo-syllabic use expand unevenly.
- Ur III, c. 2112–2004 BCE: bounded archives test record-to-capacity mechanisms.
- Old Babylonian, c. 2000–1600 BCE: strong training, lexical, epistolary and retrospective-memory evidence.
- Later second/first millennia BCE: multilingual adaptation and learned Sumerian continue.
- First centuries BCE/CE: ecosystem narrows; latest currently known dated tablet is 75 CE.
- Nineteenth century CE: comparative decipherment restores access after competence break.

## Canonical terminology

- **Accounting device:** stores quantity/identity without stable two-dimensional sign system.
- **Proto-writing/semasiography:** marks convey meaning/quantity without demonstrated language-specific encoding.
- **Writing/glottography:** signs can encode linguistic units; continuous speech is not required.
- **Proto-cuneiform:** Uruk IV–III ancestral system; writing threshold remains definition-dependent.
- **Cuneiform:** later wedge-impressed, usually logo-syllabic script family.
- **Sumerian:** always specify language, tradition, region or population.
- **Living tradition:** competent teaching, copying, interpretation and reuse—not object survival.
- **Legacy:** direct transmission, recovery-mediated influence or analogy.

## Central entities and functions

- **P005390 / MMA 1988.433.2:** opening administrative object; structured grain/quantity relations plus limits. Met image Public Domain.
- **MMA 86.11.111:** exceptional report and failed written order. Met image Public Domain; paraphrase translation pending rights.
- **P228744 / Q000001:** lexical school witness. Penn photo requires permission.
- **ETCSL 3.1.19:** later composite and retrospective memory, not eyewitness dispatch.
- **House F, Nippur:** high-resolution but non-universal training context.
- **Umma and Puzriš-Dagan:** later bounded tests of record-to-capacity return arrow.
- **Behistun/comparative chain:** cumulative recovery, not one-person eureka.

## Thematic rules

1. Every capacity gain identifies writer/reader, procedure, archive, actor, beneficiary and invisible/burdened group.
2. Separate technical capacity from attested use, and record from enforcement.
3. Preserve contradiction; do not select the cinematic hypothesis.
4. Rhythm: object → institution → system → human consequence.
5. Later evidence may test but not silently prove an origin-horizon mechanism.
6. Archive is organizational residue, never neutral census.

## Setup/payoff map

- P01 incomplete tablet → P10 recovered reading with remaining uncertainty.
- P02 rejects token ladder → P08 survival by recombination/adaptation.
- P03 institution→record pressure → P07 qualified record→capacity return arrow.
- P04 separates script/language → P08 separates script, language, institution timelines.
- P05 written order/report → P07 non-compliance proves writing does not enforce itself.
- P06 trained community creates reproducibility → P09 loss of community defines endpoint.
- P07 asymmetrical visibility → P10 avoids deterministic verdict.
- P09 mute archive → P10 recovery without direct lineage.

## Global exclusions

No ethnic inventor/exact year; no uncontested world-first; no token ladder; no alphabet progress story; no literacy percentage or universal gender rule; no text-equals-enforcement; no archive as whole society; no smartphone lineage; no FoC structure/cadence; no narration, invented scene or interiority.
# END INPUT: 02_outline/story-bible.md

# BEGIN INPUT: 02_outline/voice-profile.md
# Product Voice Profile — Sumer Writing

Status: active

## Product voice

Người kể là một điều tra viên điềm tĩnh, đứng cùng phía với khán giả trước những dấu vết khó đọc. Giọng văn sáng rõ, gần với lời nói và có sức nặng nhưng không khoa trương. Nó không kể tổng sử Sumer; nó theo một phát minh dần biến thành thiết chế, quyền lực, ký ức và cuối cùng là di sản. Khán giả luôn phải biết ta đang nhìn điều gì, chưa hiểu điều gì và phát hiện kế tiếp thay đổi cách hiểu ra sao.

## Borrowed functions

- Từ *Fall of Civilizations*: giữ một vật thể, văn bản hoặc con người làm điểm tựa hiện diện thay vì giảng giải trong khoảng không.
- Duy trì một causal macro arc đủ rõ để khán giả không lạc trong thời lượng dài.
- Chuyển scale giữa thao tác đời thường, thiết chế và biến đổi văn minh; mỗi lần chuyển phải trả lời “điều này thay đổi được gì?”.
- Dùng primary text hoặc primary object vừa làm evidence vừa tạo human presence.
- Để cảm xúc đến từ khoảng cách giữa điều con người cố giữ lại và điều lịch sử thực sự cho phép còn lại.

## Original expression

Mỗi section mở ở khoảng cách gần: một vật, một dấu, một hành động hoặc một giới hạn cụ thể. Từ đó xuất hiện một vấn đề thực dụng, không phải một lời tuyên bố hùng vĩ. Evidence tạo explanatory turn; người kể lùi ra để giải thích mechanism, rồi trở lại một consequence mà người nghe có thể hình dung. Câu chữ dùng tiếng Việt thông thường, động từ cụ thể và nhịp tương phản: giải thích đủ chậm, phát hiện đủ gọn. Uncertainty chỉ ở lại khi nó đổi kết luận hoặc tạo tension.

Giọng riêng của sản phẩm nằm ở câu hỏi xuyên suốt: bằng cách nào những dấu vết nhỏ bé khiến một hành động có thể tiếp tục sau khi người tham gia đã rời đi? Mỗi phần phải làm năng lực ấy lớn hơn, phức tạp hơn hoặc đắt giá hơn.

## Prohibited imitation

- Không dùng motif nhìn tàn tích ở hiện tại như opening mặc định.
- Không sao chép cadence, narrator persona, câu chuyển, chapter order hoặc cách dàn dựng của episode Sumer.
- Không dùng mỹ từ suy tàn, định mệnh hoặc “nền văn minh đầu tiên” để thay cho causal tension.
- Không kéo myth, proverb, voice actor hay recreated music vào chỉ vì benchmark dùng chúng; chỉ dùng khi chúng có narrative job và evidence/rights rõ.
- Không mở như catalogue bảo tàng hoặc biến caveat học thuật thành nhịp kể chính.

## Draft tests

1. Sau mỗi đoạn, người nghe có thể nói bằng một câu đơn giản mình vừa hiểu thêm điều gì không?
2. Nếu bỏ một fact, tension, mechanism hoặc consequence có mất không? Nếu không, bỏ fact đó.
3. Section có ít nhất một explanatory turn làm thay đổi mô hình ban đầu không?
4. Scale shift có trở lại hệ quả đối với người hoặc thiết chế, hay chỉ phô bày kiến thức?
5. Opening tạo một vấn đề cần theo dõi, hay chỉ giới thiệu hiện vật? Ending trả payoff cụ thể, hay chỉ khái quát?
6. Cảm giác về FoC đến từ chức năng kể chuyện, hay từ câu chữ/cadence có thể nhận ra? Trường hợp thứ hai phải viết lại.
# END INPUT: 02_outline/voice-profile.md

# BEGIN INPUT: 03_sections/P01/section.json
{
  "schema_version": 1,
  "id": "P01",
  "title": "Một mảnh đất sét không chịu nói",
  "order": 1,
  "status": "ready_for_draft",
  "human_approved": false,
  "dependencies": [],
  "target_words": {
    "min": 550,
    "max": 700
  },
  "budget_rationale": "Section chỉ có một hiện vật, một nghịch lý và một explanatory turn. Khoảng này đủ đặt object, giải thích ngưỡng tranh luận, trả payoff và mở P02 mà không lặp ý hoặc bổ sung fact để kéo dài."
}
# END INPUT: 03_sections/P01/section.json

# BEGIN INPUT: 03_sections/P01/brief.md
# P01 — Một mảnh đất sét không chịu nói

## Narrative job

Thiết lập object, mystery và causal question bằng một tablet sớm; nó lưu relations nhưng không cho phép chuyện phát minh đơn giản.

## Entry state

Khán giả xem writing như phát minh hoàn chỉnh do người Sumer tạo ra để ghi ngôn ngữ.

## Exit state

Khán giả hiểu earliest evidence nằm trên ngưỡng tranh luận; câu hỏi thật là nó trở thành hạ tầng xã hội thế nào.

## Question

Nếu tablet sớm nhất chưa kể được câu hoàn chỉnh, vì sao nó quan trọng?

## Payoff

Giá trị đầu tiên là làm quantities, categories và relations tồn tại ngoài trí nhớ tức thời.

## Anchor requirements

- P005390/MMA 1988.433.2; Met Public Domain image; preserve uncertain provenance/language.
- Declare Uruk IV/III ranges and writing-threshold dispute.

## Bridge in

Cold open on physical object and constrained modern reading.

## Bridge out

Step backward into earlier information practices.

## Boundary

Không giải thích toàn bộ formation hoặc tuyên bố world-first.

## Risk

Definition must stay attached to what the object can/cannot do.
# END INPUT: 03_sections/P01/brief.md

# BEGIN INPUT: 03_sections/P01/story-plan.json
{
  "schema_version": 2,
  "section": "P01",
  "status": "approved",
  "governing_idea": "Bước thay đổi quan trọng không phải ghi trọn lời nói, mà là khiến một phần thông tin tồn tại bền hơn trí nhớ tức thời.",
  "audience_question": "Một tablet không ghi thành câu hoàn chỉnh thì đã thay đổi điều gì?",
  "audience_payoff": "P005390 cho thấy loại và lượng ngũ cốc đã có thể được giữ trên vật thể bền dù chưa ghi trọn lời nói.",
  "structure_shape": "object_puzzle → payoff → formation_turn",
  "word_budget": {
    "recommended": {
      "min": 550,
      "max": 700
    },
    "rationale": "Section chỉ có một hiện vật, một nghịch lý và một explanatory turn. Khoảng này đủ đặt object, giải thích ngưỡng tranh luận, trả payoff và mở P02 mà không lặp ý hoặc bổ sung fact để kéo dài.",
    "accepted_resize_from": {
      "min": 950,
      "max": 1200
    }
  },
  "evidence_roles": {
    "narrated": [
      "CLM-0042",
      "CLM-0001"
    ],
    "support": [
      "CLM-0002"
    ],
    "guardrail": [
      "CLM-0006",
      "CLM-0007",
      "CLM-0008"
    ],
    "omit": [
      "CLM-0004",
      "CLM-0009",
      "CLM-0034"
    ]
  },
  "claim_use": {
    "CLM-0042": "Tạo object puzzle: ta đọc được ngũ cốc và số lượng nhưng không phục hồi được câu hoàn chỉnh, ngôn ngữ hay giao dịch chính xác.",
    "CLM-0001": "Đổi mô hình hiểu và trả payoff: năng lực cố định một phần thông tin có thể xuất hiện trước khả năng ghi trọn lời nói.",
    "CLM-0002": "Chỉ đặt P005390 trong khoảng thời gian tối thiểu theo yêu cầu brief; không tạo chronology turn hay lập luận nguồn gốc."
  },
  "beats": [
    {
      "id": "B01",
      "function": "object_puzzle",
      "purpose": "Đặt P005390 ở khoảng cách gần: dấu cho biết ngũ cốc và số lượng, nhưng thiếu động từ nên không cho ta một câu hay giao dịch chắc chắn.",
      "audience_change": "Khán giả thôi mặc định một tablet cổ là lời nói đang chờ được dịch.",
      "claim_ids": [
        "CLM-0042",
        "CLM-0002"
      ]
    },
    {
      "id": "B02",
      "function": "payoff",
      "purpose": "Dùng ngưỡng tranh luận để đổi câu hỏi từ nó có phải chữ viết hay không sang năng lực đã xuất hiện: giữ lại loại và lượng trên đất sét.",
      "audience_change": "Khán giả hiểu giá trị của hiện vật nằm ở thông tin được cố định, không ở một câu hoàn chỉnh.",
      "claim_ids": [
        "CLM-0042",
        "CLM-0001"
      ]
    },
    {
      "id": "B03",
      "function": "formation_turn",
      "purpose": "Không nhắc lại payoff; chuyển thẳng sang câu hỏi P02: những thực hành lưu giữ thông tin nào đã khiến năng lực này hình thành?",
      "audience_change": "Khán giả rời câu hỏi về khoảnh khắc phát minh và bước vào cuộc điều tra về quá trình hình thành.",
      "claim_ids": []
    }
  ],
  "terminology": [
    {
      "term": "proto-cuneiform",
      "plain_language": "hệ dấu sớm ở Uruk, tổ tiên của chữ hình nêm nhưng chưa ghi lời nói rõ như các giai đoạn sau"
    }
  ],
  "opening_move": "Mở trên những gì P005390 cho phép đọc và điểm nó đột ngột im lặng; chỉ sau khi mystery hình thành mới nêu tên hiện vật và niên đại tối thiểu.",
  "ending_move": "Sau payoff duy nhất, không diễn giải lại; đặt ngay câu hỏi về những thực hành có trước tablet để chuyển sang P02.",
  "comprehension_test": "Khán giả có thể nói: P005390 chưa ghi trọn lời nói nhưng đã giữ được loại và lượng ngũ cốc trên đất sét.",
  "approved_by": "user",
  "approved_at": "2026-08-13T16:48:45.843046+00:00"
}
# END INPUT: 03_sections/P01/story-plan.json

# BEGIN INPUT: 03_sections/P01/narration-pack.json
{
  "schema_version": 1,
  "section": "P01",
  "created_at": "2026-08-13T16:48:45.845764+00:00",
  "story_plan_sha256": "f5c6958e8e24c514b7ada46ba2fd1a690b6404657b1da968138c54b1ab04b1ed",
  "evidence_pack_sha256": "7f8c60be19754fee95b69315d0ddb20942e2801145a0b6fd9197e2e2ad598f5d",
  "narrated_claims": [
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
    }
  ],
  "support_claims": [
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
    }
  ],
  "claim_use": {
    "CLM-0042": "Tạo object puzzle: ta đọc được ngũ cốc và số lượng nhưng không phục hồi được câu hoàn chỉnh, ngôn ngữ hay giao dịch chính xác.",
    "CLM-0001": "Đổi mô hình hiểu và trả payoff: năng lực cố định một phần thông tin có thể xuất hiện trước khả năng ghi trọn lời nói.",
    "CLM-0002": "Chỉ đặt P005390 trong khoảng thời gian tối thiểu theo yêu cầu brief; không tạo chronology turn hay lập luận nguồn gốc."
  },
  "guardrails": [
    {
      "id": "CLM-0006",
      "constraint": "Do not convert 'found in southern Mesopotamia/Uruk' into 'written by ethnic Sumerians in Sumerian'.",
      "counterevidence": "Some rare rebus/phonetic readings may fit Sumerian, and the later descendant script unquestionably writes Sumerian; this makes Sumerian plausible but not demonstrated for the earliest horizon."
    },
    {
      "id": "CLM-0007",
      "constraint": "Use 'Uruk/southern Mesopotamian tradition' for the earliest phase; reserve 'Sumerian writing' for contexts with linguistic evidence.",
      "counterevidence": "Uruk's corpus dominance may partly reflect excavation and preservation; related early practices are attested beyond Uruk and transmitted toward Susiana/Iran."
    },
    {
      "id": "CLM-0008",
      "constraint": "Claim 'one of the earliest independently developed writing traditions' or 'earliest large writing corpus', not an uncontested world first.",
      "counterevidence": "Uruk provides one of the earliest and by far the largest early corpora and may precede Egyptian material under some chronologies; neither establishes a universally accepted single winner."
    }
  ],
  "omitted_claim_ids": [
    "CLM-0004",
    "CLM-0009",
    "CLM-0034"
  ],
  "sources": [
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
      ],
      "status": "reviewed",
      "limitations": [
        "Chronological ranges and corpus counts reflect the state of publication in 2004; some causal interpretation belongs to WS02.",
        "Older chronology; causal interpretation remains debated.",
        "Earliest corpus only."
      ],
      "notes": [
        "Supports ca. 3300 BCE emergence, relative Uruk IV→III sequence, overwhelmingly administrative earliest corpus, and caution around token continuity.",
        "Selected for this workstream's bounded question."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-001"
        },
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-002"
        },
        {
          "workstream": "WS05",
          "local_id": "WS05-SRC-001"
        }
      ]
    },
    {
      "id": "SRC-0002",
      "title": "Uruk and I",
      "author": "Hans J. Nissen",
      "year": 2024,
      "type": "scholarly excavation historiography",
      "authority": "CDLI Journal article by a senior Uruk specialist auditing excavation records and chronology.",
      "url": "https://cdli.earth/articles/cdlj/2024-1",
      "locators": [
        "§15.8; §16.1–16.4; §17.3; §18.2"
      ],
      "status": "reviewed",
      "limitations": [
        "Author explicitly foregrounds failures in legacy excavation documentation; exact absolute dates remain model-dependent."
      ],
      "notes": [
        "Uruk IVa is the most probable archaeological placement of the oldest script, slightly earlier cannot be excluded; find context is often insufficient and unreliable."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-002"
        }
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
      ],
      "status": "reviewed",
      "limitations": [
        "The chapter advocates a fluid continuum; terminology is analytical rather than a universally accepted threshold definition.",
        "Framework-oriented rather than a new excavation report."
      ],
      "notes": [
        "Useful counterweight to a binary true-writing/proto-writing distinction and to a linear token→tablet story.",
        "Selected for this workstream's bounded question."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-003"
        },
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-004"
        }
      ]
    },
    {
      "id": "SRC-0004",
      "title": "The Origins of Writing",
      "author": "Ira Spar",
      "year": 2004,
      "type": "museum scholarly essay",
      "authority": "Metropolitan Museum of Art Heilbrunn Timeline essay by a cuneiform specialist.",
      "url": "https://www.metmuseum.org/essays/the-origins-of-writing",
      "locators": [
        "paragraphs 62–69",
        "paragraph 69"
      ],
      "status": "reviewed",
      "limitations": [
        "Introductory synthesis and now older; statements about possible mid-fourth-millennium Syrian/Turkish systems are provisional.",
        "Introductory; dates rounded.",
        "Broad chronological compression."
      ],
      "notes": [
        "States that Sumerian identification of Uruk tablets is popular but not universal; phonetic use is sparse before 3000 and consistently apparent much later.",
        "Selected for this workstream's bounded question."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-004"
        },
        {
          "workstream": "WS03",
          "local_id": "WS03-SRC-001"
        },
        {
          "workstream": "WS05",
          "local_id": "WS05-SRC-002"
        }
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
      "id": "SRC-0008",
      "title": "The Origins of Writing",
      "author": "Metropolitan Museum of Art, object and corpus context",
      "year": 2004,
      "type": "museum corpus overview",
      "authority": "Major museum collection context linked to excavated and collected early tablets.",
      "url": "https://www.metmuseum.org/art/collection/search/327385",
      "locators": [
        "object description: earliest tablets around 3300 BCE; two early phases"
      ],
      "status": "reviewed",
      "limitations": [
        "Single object is illustrative, not representative; provenance and dating of market-derived tablets can be weaker than excavated material."
      ],
      "notes": [
        "Material anchor for the approximate 3300 BCE date and phase distinction."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-008"
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
  "rule": "This pack is a ceiling, not a checklist. Narrated claims may appear only where assigned to a story beat. Support claims are optional precision. Guardrails constrain wording and are not exposition. Omitted claims stay out."
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
