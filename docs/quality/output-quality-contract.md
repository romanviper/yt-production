# Output Quality Contract v1.0 — Historical Podcast Prose

Status: **CANONICAL / PHASE 1 BASELINE**  
Target Product: Historical Narrative Spoken Script (Vietnamese)  
Context: Observable Learning Architecture ([docs/architecture/observable-learning-architecture-plan.md](../../docs/architecture/observable-learning-architecture-plan.md) & [docs/phase1/START.md](../../docs/phase1/START.md))

---

## 1. Mục đích & Nguyên tắc Cốt lõi

Hợp đồng này thiết lập chuẩn mực đo lường chất lượng đầu ra độc lập ở tầng sản phẩm (product-level benchmark) cho các đoạn văn bản podcast lịch sử.

### 3 Nguyên tắc Tối thượng
1. **Đo lường trên văn bản đầu ra (Output-grounded only):** Đánh giá dựa trên chính xác những gì người nghe tiếp nhận từ câu chữ. Không đánh giá dựa trên ý đồ của prompt, không xem xét mức độ "tuân thủ kế hoạch" của Writer hay các báo cáo tự khai (self-reported metrics) của Agent.
2. **Không chấp nhận phán quyết scalar vô căn cứ:** Tuyệt đối cấm các nhận định trừu tượng như `chất lượng = 8/10`, `diễn tiến = tốt`, `văn phong trôi chảy`. Mọi phán quyết phải được biểu diễn dưới dạng vector đa chiều kèm bằng chứng trích đoạn cụ thể (`evidence_spans`) và hậu quả nhận thức của người nghe (`listener_consequence`).
3. **Phân tầng độc lập:** Phân tách rành mạch giữa Cổng Đúng Sai Tuyệt Đối (Absolute Gates) và Các Chiều Kích Thủ Pháp (Craft Dimensions); phân tách Đánh giá So sánh Tương đối (Relative Improvement) với Khoảng cách tới Mục tiêu Đích (Target Gap).

---

## 2. Cấu trúc Đánh giá 3 Tầng (Three-Layer Evaluation)

Mỗi mẫu văn bản khi kiểm định phải đi qua 3 tầng đánh giá tuần tự:

```text
+-------------------------------------------------------------+
| TẦNG A: CỔNG ĐÚNG SAI TUYỆT ĐỐI (ABSOLUTE GATES)            |
| -> Vi phạm bất kỳ cổng nào = Mẫu vô hiệu (GATE_FAILED)      |
+-------------------------------------------------------------+
                              | (Nếu PASS tất cả)
                              v
+-------------------------------------------------------------+
| TẦNG B: CHIỀU KÍCH THỦ PHÁP KỂ CHUYỆN (CRAFT DIMENSIONS)   |
| -> Vector 7 chiều đánh giá trải nghiệm nghe nói              |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| TẦNG C: KHOẢNG CÁCH MỤC TIÊU & SO SÁNH (TARGET GAP)         |
| -> So với Baseline & Khoảng cách tới chuẩn mực thủ pháp     |
+-------------------------------------------------------------+
```

---

### Tầng A: Cổng Đúng Sai Tuyệt Đối (Absolute Gates)

Nếu vi phạm bất kỳ tiêu chí nào dưới đây, mẫu văn bản bị coi là không đạt yêu cầu sản xuất, bất kể thủ pháp văn chương hay đến đâu:

| Mã Cổng | Tên Cổng | Định nghĩa & Tiêu chuẩn Kiểm tra | Trạng thái |
| :--- | :--- | :--- | :--- |
| `G_TRUTH` | **Historical Truth & Qualification** | Mọi sự kiện, hiện vật, số đo, niên đại đều phải được bảo chứng bởi cứ liệu lịch sử đã duyệt. Phải nêu rõ tính phỏng đoán/không chắc chắn nếu sử liệu còn khuyết thiếu; không được khẳng định bừa. | `PASS` \| `FAIL` |
| `G_COHERENCE` | **Internal Coherence** | Không tự mâu thuẫn nội tại giữa các câu, không xung đột logic thực tế (ví dụ: vừa khẳng định phong bì kín mít không thấy bên trong, câu sau lại nói người nhìn thấy con tính qua vỏ đất lành). | `PASS` \| `FAIL` |
| `G_SCOPE` | **Scope Compliance** | Nằm trọn vẹn trong phạm vi đề mục được giao (ví dụ P01: công cụ ghi nhận bằng đất sét thời Hậu Uruk; không phóng đại sang chữ hình nêm hay các thời kỳ sau). | `PASS` \| `FAIL` |
| `G_LANGUAGE` | **Intelligible Vietnamese** | Tiếng Việt tự nhiên, đúng ngữ pháp, ngữ nghĩa rõ ràng, không lai căng dịch thô máy móc hay dùng từ tối nghĩa. | `PASS` \| `FAIL` |
| `G_CAUSALITY` | **Grounded Causality** | Không tự bịa đặt động cơ tâm lý sâu kín của nhân vật lịch sử hoặc gán ghép quan hệ nhân quả một chiều khi chứng cứ khảo cổ chỉ ghi nhận sự cùng tồn tại. | `PASS` \| `FAIL` |

---

### Tầng B: Các Chiều Kích Thủ Pháp Kể Chuyện (Craft Dimensions)

Chỉ kiểm định khi mẫu đã vượt qua toàn bộ Cổng Tầng A. Đánh giá theo vector 7 chiều, các giá trị hợp lệ: `PASS`, `GOOD`, `WEAK`, `FAIL`, hoặc `UNCERTAIN`.

#### 1. `continue` (Sức hút lôi cuốn nghe tiếp)
- **Định nghĩa:** Mức độ tạo dựng sự tò mò nhận thức, câu hỏi treo, hoặc tình huống kịch tính trí tuệ khiến người nghe muốn biết điều gì sẽ xảy ra tiếp theo.
- **Tiêu chuẩn tốt (`GOOD`):** Mỗi đoạn kết thúc đều để lại một mâu thuẫn vật lý hoặc nghi vấn chưa giải quyết, kéo tai người nghe sang đoạn sau một cách tự nhiên.
- **Dấu hiệu yếu (`WEAK` / `FAIL`):** Các đoạn khép lại quá tròn trịa như một kết luận bài thi, gây cảm giác bài nói đã kết thúc sớm.

#### 2. `movement` (Động lực dịch chuyển nhận thức)
- **Định nghĩa:** Sự thay đổi có ý nghĩa trong hiểu biết của người nghe qua từng câu từng đoạn. Người nghe bước vào đoạn với trạng thái nhận thức $A$ và bước ra ở trạng thái $B$.
- **Tiêu chuẩn tốt (`GOOD`):** Trạng thái vấn đề liên tục biến đổi (từ vật rời rạc -> nhu cầu giữ trọn -> phong bao kín -> nghịch lý mù thị giác -> giải pháp ấn ngoài -> bảng số phẳng).
- **Dấu hiệu yếu (`WEAK` / `FAIL`):** Văn bản dậm chân tại chỗ, viết nhiều câu nhưng chỉ lặp lại một ý niệm miêu tả.

#### 3. `specificity` (Chi tiết cụ thể gánh vác câu chuyện)
- **Định nghĩa:** Mức độ các chi tiết vật lý, kích thước, chất liệu, mã hiệu hiện vật thực tế trực tiếp tham gia thúc đẩy mạch tự sự chứ không chỉ đứng làm vật trang trí.
- **Tiêu chuẩn tốt (`GOOD`):** "kích thước 7,8 x 7,2 cm", "khoang rỗng ôm lấy con tính 1,6 cm", "vết vỡ cổ xưa để lộ bên trong".
- **Dấu hiệu yếu (`WEAK` / `FAIL`):** Dùng các danh từ chung chung, trừu tượng ("những phương tiện quản lý đa dạng", "các công cụ cổ xưa").

#### 4. `connections` (Mạch liên kết nhân quả hiện diện trong văn)
- **Định nghĩa:** Các khớp nối logic và cầu nối chuyển ý giữa các ý tưởng phải được thể hiện trực quan ngay trên bề mặt văn bản bằng quan hệ hệ quả, đối nghịch vật lý, không bắt người nghe phải tự suy diễn.
- **Tiêu chuẩn tốt (`GOOD`):** Cầu nối logic xuất phát từ mâu thuẫn cơ học ("chính khoảnh khắc lớp vỏ khép lại, nghịch lý nảy sinh").
- **Dấu hiệu yếu (`WEAK` / `FAIL`):** Chuyển đoạn bằng các từ nối cơ học rỗng tuếch kiểu tiểu luận ("Hơn nữa", "Bên cạnh đó", "Mặt khác").

#### 5. `listenability` (Nhịp điệu nói & Khả năng lĩnh hội một lần)
- **Định nghĩa:** Cấu trúc câu phù hợp với hơi thở người đọc và năng lực tiếp nhận âm thanh của người nghe. Đảm bảo người nghe hiểu ngay lập tức qua một lần nghe mà không cần tua lại.
- **Tiêu chuẩn tốt (`GOOD`):** Câu có cụm ngắt hơi hợp lý (15 - 25 âm tiết/mệnh đề), cấu trúc ngữ pháp xuôi chiều, từ ngữ giàu tính gợi hình gợi thanh.
- **Dấu hiệu yếu (`WEAK` / `FAIL`):** Câu phức lồng ghép quá nhiều tầng định ngữ, dài quá 40 từ không ngắt nghỉ, mật độ thông tin nén quá đặc khiến người đọc hụt hơi và người nghe quá tải.

#### 6. `payoff` (Điểm rơi nhận thức thỏa đáng)
- **Định nghĩa:** Phần thưởng hiểu biết cục bộ mà người nghe nhận được sau khi đi qua một chuỗi căng thẳng hoặc câu hỏi đặt ra từ trước.
- **Tiêu chuẩn tốt (`GOOD`):** Sự xuất hiện của bảng số phẳng ChM III-937a giải quyết trọn vẹn nghịch lý thị giác của phong bao rỗng ruột OIM A64678.
- **Dấu hiệu yếu (`WEAK` / `FAIL`):** Nêu câu hỏi lớn nhưng hạ màn mờ nhạt, hoặc giải thích qua loa bằng nhận định chung chung.

#### 7. `essay_tendency` (Khuynh hướng tiểu luận / Thuyết giảng)
- **Định nghĩa:** Lỗi văn bản sa vào giảng giải tri thức, trình bày kết luận và ý nghĩa trước khi người nghe kịp trải nghiệm sự việc hoặc nhìn thấy hiện vật.
- **Tiêu chuẩn đạt (`PASS`):** Hiện vật và hành động vật lý xuất hiện trước; ý nghĩa lịch sử tự toát ra qua diễn biến.
- **Dấu hiệu vi phạm (`FAIL`):** Mở đầu bằng tuyên ngôn học thuật, nhận xét bình luận như bài báo khoa học ("Trong các bối cảnh hành chính...", "Sự thay đổi không chỉ nằm ở hình dạng đồ vật mà ở vị trí vật lý của thông tin...").

---

## 3. Khoảng Cách Mục Tiêu & So Sánh Đối Chứng (Target Gap)

Một văn bản có thể vượt trội hơn baseline cũ nhưng vẫn còn cách rất xa chuẩn mực podcast cao cấp. Do đó, tầng C ghi nhận hai góc nhìn:

1. **So sánh tương đối với Baseline (`baseline_comparison`):**
   - `SUPERIOR`: Vượt trội rõ rệt trên đa số chiều kích then chốt mà không bị thụt lùi ở chiều kích nào.
   - `PARITY`: Ngang ngửa, ưu thế ở mặt này nhưng lại kém ở mặt khác.
   - `INFERIOR`: Kém hơn bản mốc baseline.
   - `UNCERTAIN`: Không đủ căn cứ để kết luận phân định.

2. **Khoảng cách tới Mục tiêu Thủ pháp (`target_gap`):**
   - So sánh với các mẫu chuẩn mực (như trích đoạn đối chứng Fall of Civilizations - FoC):
   - `NEAR`: Đã đạt nhịp điệu tự sự lôi cuốn, văn phong truyền cảm, sẵn sàng thu âm.
   - `MODERATE`: Mạch truyện và chứng cứ tốt, nhưng còn thô ráp ở nhịp thở hoặc chuyển ý.
   - `FAR`: Còn nặng tính sách vở, giải thích khô khan hoặc nhịp điệu chưa phù hợp với podcast.

---

## 4. Hệ thống Chữ Ký Lỗi (Failure Signatures)

Khi một mẫu văn bản có điểm yếu hoặc vi phạm, báo cáo đánh giá phải gán một **Chữ ký Lỗi (Failure Signature)** chuẩn tắc để làm đầu vào truy vết:

```text
+----------------------+---------------------------------------------------------------+
| Mã Chữ ký Lỗi        | Triệu chứng Chính & Đặc điểm Nhận dạng                        |
+----------------------+---------------------------------------------------------------+
| E01_TRUTH_BREACH     | Sai lệch sử liệu, khẳng định vượt quá bằng chứng, bịa nhân quả|
| E02_ESSAY_LECTURE    | Lời bình và kết luận trừu tượng đi trước trải nghiệm vật lý   |
| E03_DENSE_CADENCE    | Câu quá dài, thiếu điểm ngắt hơi, nén quá nhiều mệnh đề phụ   |
| E04_STAGNANT_MOVEMENT| Miêu tả tĩnh, lặp lại ý niệm, không dịch chuyển hiểu biết     |
| E05_UNEARNED_LEAP    | Bước nhảy logic đột ngột, thiếu cầu nối nhân quả cụ thể       |
+----------------------+---------------------------------------------------------------+
```

---

## 5. Bản Đồ Nghi Can Upstream (Diagnostic Ownership Map)

Bản đồ này chỉ định các vùng kiến trúc upstream cần khoanh vùng kiểm tra đầu tiên khi phát hiện chữ ký lỗi ở đầu ra (Lưu ý: Không thay thế cho trace thực tế ở Phase 3, mà đóng vai trò định hướng điều tra ban đầu):

| Chữ Ký Lỗi Đầu Ra | Vùng Nghi Can Cấp 1 (Primary Suspects) | Vùng Nghi Can Cấp 2 (Secondary Suspects) |
| :--- | :--- | :--- |
| `E01_TRUTH_BREACH` | Truth Gate / Historical Evidence Pack | Writer realization / Narrative Planner |
| `E02_ESSAY_LECTURE`| Narrative Planner (thiết kế Beat trừu tượng) | Writer realization (thói quen tóm lược thông tin) |
| `E03_DENSE_CADENCE`| Writer realization (câu phức tiếng Anh dịch ngầm) | Polish Module / Voice Profile constraints |
| `E04_STAGNANT_MOVEMENT`| Narrative Planner (Listener-State Transition) | Section Architecture / Outline beats |
| `E05_UNEARNED_LEAP`| Narrative Planner (thiếu cầu nối mâu thuẫn) | Writer realization (bỏ qua bước trung gian) |

---

## 6. Quy Chuẩn Báo Cáo Đánh Giá (Reviewer Grounding Rules)

Mỗi phán quyết của Người đánh giá (Reviewer) chỉ hợp lệ khi tuân thủ 3 điều kiện:
1. Phải trích dẫn ít nhất một câu văn cụ thể trong bài làm bằng chứng (`evidence_spans`).
2. Phải phân tích rõ vì sao câu văn đó dẫn tới trạng thái nhận thức tương ứng (`listener_consequence`).
3. Nếu phân vân hoặc bằng chứng không rõ ràng, phải ghi nhận `UNCERTAIN` thay vì phỏng đoán điểm số.
