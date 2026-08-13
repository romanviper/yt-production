# Context Packet — T0011-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T0011-draft-section-P01/report.md`, `tasks/T0011-draft-section-P01/operator-brief.json`

## Acceptance criteria

- Chỉ viết section được chỉ định.
- Mọi substantive claim nằm trong evidence pack.
- Entry/exit state và bridge đúng brief.
- Handoff tóm tắt continuity, setup/payoff và không thay thế draft.

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
# END INSTRUCTION: system/standards/writing-vi.md

# BEGIN INSTRUCTION: system/operations/draft-section.md
# Operation — Draft Section

## Responsibility

Viết narration cho đúng một section từ section contract và evidence pack đã đóng gói.

## Rules

- Không mở source index hoặc raw workstreams ngoài packet.
- Không giải thích nội dung đã được boundary giao cho section khác.
- Nếu evidence pack thiếu claim cần thiết, ghi blocker; không tự research trong task viết.
- Draft phải đạt entry→exit state, narrative job, payoff và word budget.
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
    "min": 950,
    "max": 1200
  }
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

# BEGIN INPUT: 03_sections/P01/evidence-pack.json
{
  "schema_version": 1,
  "section": "P01",
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
      "id": "SRC-0006",
      "title": "Visible Language exhibition overview",
      "author": "Institute for the Study of Ancient Cultures, University of Chicago",
      "year": 2010,
      "type": "academic institutional overview",
      "authority": "Official ISAC summary of the Woods-curated exhibition.",
      "url": "https://isac.uchicago.edu/museum-exhibits/visible-language-inventions-writing-ancient-middle-east-fall-2010",
      "locators": [
        "paragraphs 46–51"
      ],
      "status": "reviewed",
      "limitations": [
        "Public-facing overview rather than full argument; dates are rounded."
      ],
      "notes": [
        "Places Mesopotamian tablets around 3200 BCE and early Egyptian tags around 3320 BCE, illustrating why 'first' depends on definition and dating."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-006"
        }
      ]
    },
    {
      "id": "SRC-0007",
      "title": "The State of Decipherment of Proto-Elamite",
      "author": "Robert K. Englund",
      "year": 2004,
      "type": "scholarly chapter / comparative script study",
      "authority": "Corpus-based comparison by a leading proto-cuneiform and proto-Elamite specialist.",
      "url": "https://cdli.earth/files-up/publications/englund2004c.pdf",
      "locators": [
        "pp. 124–127 and 139–140 (PDF pp. 24–27, 39–40)"
      ],
      "status": "reviewed",
      "limitations": [
        "Proto-Elamite comparison is secondary to WS01 and does not establish the spoken language of Uruk scribes."
      ],
      "notes": [
        "Supports relative order Uruk IV before Uruk III and contemporaneity/contact with proto-Elamite; shows attribution is regional and transmissional, not a simple ethnic label."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-007"
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
