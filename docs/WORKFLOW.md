# Modular Production Workflow

## Mục tiêu vận hành

Một Agent mới phải có thể hoàn thành một nghiệp vụ mà không cần biết toàn bộ lịch sử cuộc trò chuyện hay đọc toàn repo. Mỗi lượt làm việc nhận một context packet có version, token budget, input hash và write scope.

Work order, packet manifest, compiled context và `ACTIVE.json` là control artifact do router sinh ra. Agent thực hiện nội dung chỉ ghi các output được packet cho phép; không dựng hoặc vá các control artifact bằng tay. Packet version 2 mang định danh compiler và hash của chính compiled context, nên validator phát hiện cả input stale lẫn context bị thay thế.

## Ranh giới theo SOLID

| Nguyên tắc | Cách repo áp dụng |
|---|---|
| Single responsibility | Mỗi operation chỉ sở hữu một loại biến đổi artifact; research, outline, draft, review và revision không trộn nhau. |
| Open/closed | Thêm operation qua `registry.json` và contract riêng; router không cần biết nội dung lịch sử cụ thể. |
| Liskov substitution | Agent nào thực hiện task cũng nhận cùng work-order/packet/report contract và phải qua cùng validator. |
| Interface segregation | Task chỉ thấy instruction và input nó cần; P06 không nhận raw research hoặc draft P01–P10. |
| Dependency inversion | Operation sau phụ thuộc vào artifact chuẩn hóa và hash, không phụ thuộc chat history hay memory của Agent trước. |

Số section là cấu hình của outline, không hard-code trong engine. Pilot Sumer đặt target 10; product khác có thể đặt số khác.

## Quyền hạn: nội dung không được sửa hệ thống

Repo phân biệt hai trách nhiệm:

- **Product Agent:** research, outline, draft hoặc review đúng một product operation. Không được sửa control plane.
- **System Architect:** bảo trì kiến trúc dùng chung trong một architecture task riêng do repository owner giao.

Protected system gồm `AGENTS.md`, `.github/`, `system/`, `scripts/`, `templates/`, `tests/`, `docs/`, `Makefile` và repo `README.md`.

Nếu Product Agent phát hiện một lỗi hệ thống, nó chỉ báo cáo:

1. hành vi nào đang bị chặn;
2. ảnh hưởng đến product hiện tại;
3. system change request cần route cho System Architect.

Nó không được sửa hệ thống, ngay cả khi biết cách fix. Architecture commit cũng không được chứa thay đổi nội dung product. Boundary này được scope checker và governance test kiểm tra, thay vì chỉ dựa vào prompt discipline.

## Operator interface: đúng độ sâu, đúng thời điểm

Người dùng không cần xem process diary. Mỗi task giữ hai output giao tiếp khác nhau:

- `report.md`: toàn bộ phân tích, issue, evidence, validation và chi tiết triển khai để audit khi cần;
- `operator-brief.json`: phần thông tin đủ để người dùng hiểu tình hình và ra quyết định.

Brief dùng cho status, handoff, blocker và checkpoint được render theo contract:

- tối đa 140 từ;
- kết luận ở dòng đầu;
- tối đa ba điểm có ảnh hưởng thực sự;
- nếu cần duyệt: một khuyến nghị, một câu hỏi quyết định và hiệu lực của các lựa chọn;
- nếu không cần duyệt: đúng một bước kế tiếp.

Không phải mọi câu trả lời đều bị giới hạn 140 từ:

- hỏi concept hoặc `tại sao/như thế nào`: Agent dùng guided explanation, kết luận trước rồi giải thích vừa đủ;
- yêu cầu evidence/audit/phản biện sâu: Agent dùng deep review, executive summary trước rồi mở chi tiết;
- yêu cầu xem outline/draft: Agent dùng deliverable mode, brief trước rồi đưa artifact thật để kiểm duyệt.

| Cách người dùng nói tự nhiên | Mode Agent nên chọn | Kết quả mong đợi |
|---|---|---|
| “Tình hình hiện tại thế nào?” | Brief | Trạng thái, tối đa ba điểm quan trọng, một bước/decision. |
| “Tại sao phải tách WS07 và WS08?” | Guided explanation | Mental model và trade-off vừa đủ để hiểu. |
| “Audit đầy đủ research plan và cho tôi evidence.” | Deep review | Executive summary rồi phân tích/evidence có cấu trúc. |
| “Cho tôi xem bản P04 để duyệt.” | Deliverable | Brief rồi nội dung thật hoặc liên kết trực tiếp tới P04. |

Người dùng không cần gọi tên mode; Agent suy ra từ intent. Các câu như `tóm tắt lại`, `chỉ cho tôi phần cần quyết định`, `mở chi tiết điểm 2` hoặc `cho tôi xem evidence` dùng để zoom thông tin lên/xuống mà không tạo lại công việc.

Agent không mặc định kể file đã đọc, command đã chạy, hash, test bình thường hoặc mọi rủi ro nhỏ. Những thứ này vẫn được lưu trong report nên giao tiếp gọn không làm mất khả năng audit; ngược lại, brevity cũng không được che blocker hoặc uncertainty cần cho quyết định.

Ví dụ mặc định:

```text
Chờ bạn duyệt: Research plan đủ mạnh và chỉ cần chỉnh nhẹ trước khi chạy.

- Làm rõ ranh giới WS07–WS08.
- Giao ownership cho exchange và social memory.
- Giữ tám workstream; không cần thiết kế lại.

Khuyến nghị: sửa ba điểm trên rồi duyệt.

Cần bạn quyết định: Chỉnh plan trước hay duyệt nguyên trạng?
- Chỉnh trước: Agent tạo một patch giới hạn, research chưa chạy.
- Duyệt: Mở workstream research với rủi ro overlap còn giữ nguyên.
```

Khi người dùng yêu cầu `mở chi tiết`, Agent mới đọc report và mở đúng phần được hỏi. Đây là progressive disclosure: thông tin không bị mất, nhưng không chiếm giao diện mặc định.

## 1. Research không phải một task khổng lồ

### 1.1 Research plan

Agent đọc product brief và benchmark, rồi tạo `01_research/plan.json`. Plan chia chủ đề thành các workstream có câu hỏi, boundary và deliverable riêng.

Người dùng duyệt trước khi materialize:

```bash
python scripts/approval.py approve-plan products/<slug>
```

### 1.2 Research workstream

Chạy `materialize_research.py` để tạo workspace cho từng workstream. Mỗi Agent chỉ research một workstream và ghi:

- `sources.json`;
- `claims.json`;
- `synthesis.md` giới hạn dung lượng.

Agent không cần đọc workstream khác.

Source/claim ID ở cấp workstream được namespace (`WS02-SRC-001`, `WS02-CLM-001`) để các unit có thể chạy độc lập. Synthesis mới cấp ID toàn cục và lưu provenance, nên hai Agent song song không thể vô tình collision ID.

### 1.3 Research synthesis

Trước task AI, router chạy deterministic consolidation để remap ID, deduplicate source theo canonical identity, giữ provenance và tạo global source/claim ledgers. Đây là biến đổi dữ liệu có quy tắc, không tiêu tốn context AI.

Task synthesis chỉ đọc `consolidation.json` cùng các workstream `synthesis.md`; nó không nạp 16 local ledger hoặc toàn bộ web notes. Nó tạo:

- `research-synthesis.md`;
- contradictions và unknowns cần outline xử lý.

Nhờ vậy số workstream có thể tăng mà context synthesis vẫn tỷ lệ với các handoff cô đọng, không tỷ lệ với toàn bộ research corpus.

## 2. Outline là interface giữa research và writing

Task `outline` chỉ đọc product brief, research synthesis và claim ledger đã lọc. Output:

- `02_outline/outline.json` gồm đúng số phần đã chọn;
- `02_outline/story-bible.md` — context toàn cục được giữ ngắn.

Mỗi phần phải có ID ổn định, narrative job, entry/exit state, claim IDs, dependencies và word budget. Con người review outline trước khi materialize.

```bash
python scripts/approval.py approve-outline products/<slug>
```

## 3. Section workspace

Sau khi outline được duyệt:

```bash
python scripts/materialize_sections.py products/<slug>
```

Script tạo cho mỗi phần:

```text
03_sections/P04/
  section.json
  brief.md
  evidence-pack.json
  continuity-in.md
```

Evidence pack chỉ chứa claim/source cần cho P04. Nó là interface giữa research và drafting.

## 4. Người dùng gọi phần nào, Agent chỉ viết phần đó

```bash
python scripts/task.py create products/<slug> draft_section --section P04
```

Packet của P04 chứa:

- invariants tối thiểu;
- contract của `draft_section`;
- chuẩn viết tiếng Việt;
- story bible compact;
- brief P04;
- evidence pack P04;
- continuity input/handoff liên quan.

Nếu dependency đã được con người duyệt, packet tự thêm đúng handoff của dependency đó; nó không mở full draft của dependency. Nếu viết out-of-order, Agent dựa vào bridge/story bible và ghi rõ continuity chưa xác lập.

Nó không chứa raw research, brief của chín phần còn lại hoặc draft toàn phim.

Agent chỉ được tạo/sửa:

- `03_sections/P04/draft.md`;
- `03_sections/P04/handoff.md`;
- task report của chính task đó.

## 5. Review và revision tách khỏi drafting

- `review_section`: chỉ đọc và chẩn đoán P04; chỉ viết `review.md`.
- `revise_section`: chỉ đọc draft, review/change request và evidence pack của P04; sửa draft P04.
- Người dùng đặt `section.json.status = approved` sau khi chấp nhận.

Thay vì sửa JSON bằng tay:

```bash
python scripts/approval.py approve-section products/<slug> P04
python scripts/approval.py request-changes products/<slug> P04 --request "Sửa ISSUE-02; giữ nguyên opening và claim set."
```

AI viết không tự review để rồi tự phê duyệt output của chính nó.

## 6. Integration không kéo toàn bộ prose vào mọi task

Mỗi phần đã duyệt tạo `handoff.md` gồm entry/exit state, setup/payoff, entities và continuity changes. `integration_review` đọc story bible và các handoff trước để tìm conflict. Chỉ section có issue mới được mở trong revision task.

## 7. Assembly không dùng AI

`assemble.py` ghép các `draft.md` có status `approved` theo outline, tạo hash và word count. Bản delivery không phải source of truth và không sửa bằng tay.

## Prompt tối thiểu cho Agent khác

```text
Mở repo romanviper/yt-production tại root. Đọc AGENTS.md và thực hiện task active của products/sumer-writing. Không đọc toàn repo, không bỏ qua context packet và không tự approve output.
```

Để viết phần cụ thể:

```text
Trong products/sumer-writing, tạo và thực hiện operation draft_section cho P04. Chỉ làm đúng phần P04 và bàn giao để tôi review.
```
