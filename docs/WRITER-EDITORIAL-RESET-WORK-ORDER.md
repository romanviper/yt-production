# Work order — đưa vòng Writer trở lại bản đọc của Owner

**Trạng thái hiện tại:** lượt 01 đã giao tại `217348c`. Owner thấy comparison dễ đọc nhưng từ chối phần mở; chưa có cải thiện được Owner chấp nhận. Điều chỉnh bên dưới là work order cho lượt 02; chưa thực hiện lượt viết đó.
**Nhánh đích:** `codex/owner-first-mvp`; fetch HEAD hiện tại trước khi làm. Không sửa output lượt 01.

## Điều chỉnh hiện hành — lượt 02: viết được một phần mở đáng nghe

Owner nói rõ: “writer thậm chí không biết cách mở bài”. Người thực hiện phải chọn lại cách mở, không tiếp tục minh họa chức năng giữ số lượng bằng một danh sách vật hoặc chỉnh câu cho cụ thể hơn. Mục tiêu của lượt này là cho người chưa quan tâm một lý do nghe tiếp, bằng lời kể đủ rõ để hình dung.

Khi Owner giao thực hiện lượt 02, điều chỉnh này thay mục tiêu, baseline và đường dẫn đầu ra của lượt 01 ở phần lịch sử bên dưới. Giữ cách làm một Writer, một comparison ngắn và dừng cho Owner đọc. Không tạo task/router hay report 15 mục; không mở nghiên cứu, sửa harness, gọi thêm agent hoặc viết toàn P01.

**Đọc đúng đầu vào:** work order này; phần “Bản biên tập” trong `writer-output/P01/editorial-reset-01/comparison.md` tại `217348c` làm baseline; creative brief hiện hành; overlay và historical substrate đã cố định tại `3b117553a987e8c9c6b8c3661511042c988f8678` như mục 3 bên dưới. Không đọc thêm các report hoặc draft khác. Baseline là văn bản so sánh, không phải cấu trúc buộc phải giữ.

**Việc phải làm:** viết lại một đoạn mở ngắn từ cùng bộ chất liệu. Được bỏ cả hai câu mở cũ, đổi điểm vào, chọn lại facts và tổ chức lại toàn bộ đoạn. Không có yêu cầu tiếp tục lấy “vị trí thông tin” hoặc “mặt đất sét” làm trục. Chọn một điều đáng quan tâm, định hướng đủ để người nghe tiếp cận nó và phát triển lý do nghe câu tiếp theo. Sự tò mò phải phát sinh từ nội dung; không chữa bằng một câu hỏi tu từ, lời hứa lớn hoặc tình huống bịa. Không ép số cảnh, số câu hỏi hay nhân vật. Tự biên tập cấu trúc trong một lượt, chỉ giao một bản.

**Chỉ tạo:** `writer-output/P01/editorial-reset-02/comparison.md`. Nếu đã có file, dừng, không ghi đè. File gồm đúng ba phần:

1. **Bản gốc:** nguyên văn phần “Bản biên tập” của lượt 01, ghi commit `217348c`.
2. **Bản mở viết lại:** prose để đọc, không chú giải kỹ thuật; giữ quy mô đoạn mở ngắn, không kéo thành bản 450–650 từ.
3. **Đã sửa gì:** tối đa ba ghi chú ngắn về lựa chọn mở, điều trong prose được dùng để tạo lý do nghe tiếp và thay đổi nguồn/tái dựng nếu có. Dẫn cụm từ thật; không tự nhận hook hiệu quả hoặc khán giả đã tò mò. Ghi chú không dài hơn một đoạn gốc.

**Bàn giao và dừng:** commit đúng comparison lên nhánh đích theo cách thông thường, không force-push; gửi link để Owner đọc và trả lời tự do: “Bạn có muốn nghe tiếp từ đoạn mở này không? Câu nào khiến bạn dừng lại hoặc muốn đi tiếp?” Không yêu cầu report, điểm số hoặc giải thích kỹ thuật. Dễ hình dung hơn nhưng Owner vẫn không muốn nghe chưa đáp ứng mục tiêu lượt này. Chưa có phản hồi thì ghi chưa biết, không tự kết luận cải thiện. Không tự mở lượt 03, viết tiếp P01 hoặc sửa harness sau khi giao.

---

Phần bên dưới lưu work order lượt 01 để giữ lịch sử; mục tiêu và đường dẫn của nó không áp dụng cho lượt 02.

**HEAD khi soạn lượt 01:** `326022f`.
**Mục tiêu lượt 01:** Owner đọc bản trước–sau và nhận thấy có dễ hình dung hơn hay không, không cần đọc report để hiểu thay đổi.

## 1. Vấn đề cần sửa và quyết định reset

Owner đã xác định lỗi: lời kể nêu thuật ngữ, vật thể và chức năng nhưng không cung cấp đủ điểm tựa để tưởng tượng; ngay cửa vào, người nghe phải tự dựng hình và đoán quan hệ. Nhiều lần sửa hướng dẫn đã tạo thêm report nhưng chưa cho Owner thấy cải thiện rõ trong trải nghiệm đọc.

Trong lượt này, dừng việc tạo draft toàn P01, sửa thêm harness, so sánh model và mở rộng kiến trúc. Không giao lại cho Owner việc đọc báo cáo dài để tìm nguyên nhân. Đưa một phản hồi cụ thể tới một đoạn sửa có thể đối chiếu trực tiếp.

Phản hồi gốc của Owner:

> trí tưởng tượng của tôi hầu như không có gì bám vào để hình dung

Đây là nhận xét trải nghiệm thực tế của Owner, không phải số đo retention hay bằng chứng về dopamine.

## 2. Giao đúng một việc

Một Writer chịu trách nhiệm biên tập hai đoạn mở dưới đây. Đây là sửa một bản đã có, không phải bài thi viết mới từ đầu. Không gọi thêm Planner, Reviewer, subagent hoặc chọn nhiều model. Không tạo ba phương án để Owner phải lựa chọn.

Khi Owner giao thực hiện work order này, các quy định cụ thể dưới đây thay quy trình report 15 mục và ba artifact của `WRITER.md` **chỉ cho lượt `editorial-reset-01`**. Được đọc đúng baseline và phản hồi được chỉ định; không áp dụng lệnh cấm đọc bản cũ cho chính công việc biên tập nó. Không thay hướng dẫn chung của repo bằng cách sửa file khác.

Đọc mã và hướng dẫn từ HEAD hiện tại của nhánh đích. Commit lịch sử dưới đây chỉ cố định văn bản so sánh và nguồn, không phải điểm bắt đầu checkout hay một experiment cần chạy lại.

## 3. Đoạn gốc và đầu vào hữu hạn

Baseline: hai đoạn đầu, không tính dòng trắng, của `writer-output/P01/codex-clean-59c41ac/draft.md` tại commit `3b117553a987e8c9c6b8c3661511042c988f8678`.

> Ở miền nam Lưỡng Hà, vào cuối thiên niên kỷ thứ tư trước Công nguyên, đất sét đã tham gia vào một công việc khác hẳn việc làm đồ đựng: giữ thông tin. Có những vật nhỏ dùng để đếm, những vỏ đất sét rỗng, những dấu niêm, những bảng ghi số. Với chúng ta, đó có thể là những hình thù cần giải nghĩa. Với những người từng sử dụng chúng, chúng thuộc về công việc đang phải làm.
>
> Đếm được một lượng là một việc. Giữ lại thông tin về lượng ấy là việc khác. Trong thế giới Late Uruk, việc ghi nhận và xác thực được thực hiện bằng nhiều cách trên đất sét, cùng tồn tại bên nhau. Khi quy mô quản lý lớn lên, nhu cầu lưu giữ những thông tin như thế cũng là một áp lực đáng kể. Trước khi theo dõi chữ viết sẽ kể được những gì, ta có thể bắt đầu từ một đòi hỏi khiêm tốn hơn: làm sao để một con số còn ở đó, sau lúc người ta đếm xong?

Writer chỉ cần work order này và hai đầu vào lịch sử tại cùng commit baseline:

- `products/sumer-writing/02_outline/section-overlays/P01.json`;
- `products/sumer-writing/03_sections/P01/historical-substrate.json`.

Hai đầu vào này không đổi từ baseline tới `326022f`. Giữ bộ chất liệu đó trong lượt sửa. Không tìm thêm nguồn, đọc report cũ, đọc các draft khác hoặc chạy workflow legacy. Nếu không lấy được đúng input, báo ngắn đường dẫn thiếu; không tự thay bằng phiên bản khác.

Mục đích sản phẩm cần biết: podcast tiếng Việt khám phá Sumer qua chữ viết; phần mở giúp người nghe tiếp cận những dấu đất sét qua một thế giới vật chất và công việc có thể hình dung. Không cần giải hết nguồn gốc chữ viết hoặc phản biện một ngộ nhận khảo cổ trong đoạn thử.

## 4. Biên tập để người nghe hình dung, không biểu diễn kỹ thuật

Viết cho người chỉ nghe, chưa biết hình dạng hay cách dùng các hiện vật. Chọn điểm tựa và quan hệ đủ rõ để họ biết đang hình dung thứ gì; để câu tiếp theo phát triển hình dung đó. Lời giải thích có thể đi cùng hình ảnh. Không buộc người nghe tự dịch liên tiếp các từ “ghi nhận”, “xác thực”, “quản lý” thành một công việc chưa được mô tả.

Được cắt, gộp, đổi thứ tự, thay trục kể hoặc chọn lại facts trong **cùng bộ chất liệu**. Không giới hạn biên tập ở sửa chữ. Nếu một ý không giúp đoạn mở, không cần giữ chỉ để chứng minh đã đọc input. Giữ quy mô một đoạn mở ngắn, không tăng thành excerpt 450–650 từ hay thu nhỏ toàn P01 vào đây; không đặt quota khiến Writer phải thêm chữ.

Người kể toàn tri có thể dẫn qua vật liệu, thao tác, không gian và quy mô mà không cần một nhân vật hay sự kiện có sẵn. Bài học Taurus là tổ chức các facts thành một đường hình dung; không phải mọi liên kết đều là nhân quả. Một trục kể phải phát triển điều người nghe thấy hoặc hiểu, không chỉ nhắc lại một thuộc tính bằng nhiều cách.

Chọn chi tiết phục vụ việc hình dung và mạch kể. Không dùng bụi, ánh sáng, tiếng động hoặc cử chỉ vụn chỉ để chứng minh “có hình ảnh”. Không bắt buộc cảnh, đối thoại, nội tâm, đủ giác quan, mở bằng vật cụ thể hoặc kết bằng câu hỏi. Không sao chép lời FoC. Không mặc định thiếu tên người hay giao dịch đầy đủ khiến narration bất khả thi.

Giữ mức chắc chắn của nguồn. Không đổi “nguồn chưa cho biết” thành “người xưa không thể biết”. Không dựng nguyên nhân, giao dịch hoặc hình dạng ký hiệu rồi coi là fact. Tái dựng hợp bối cảnh vẫn được phép nếu được nhận diện nhẹ khi cần; nó không làm bằng chứng cho kết luận lịch sử. Không nhập nhằng hiện vật Chogha Mish với ví dụ ngũ cốc Jemdet Nasr.

Trước khi giao, tự đọc lại bản đang sửa như lời nghe một lượt: chỗ nào còn bắt người nghe đoán, mất điểm tựa hoặc chờ quá lâu cho một ý nhỏ thì sửa ngay trong bản ấy. Đây là biên tập trong cùng một lượt, không sinh nhiều bản hoàn chỉnh để tuyển chọn. Sau khi giao thì giữ nguyên, chờ Owner.

## 5. Đầu ra: một file để đọc

Chỉ được tạo `writer-output/P01/editorial-reset-01/comparison.md`. Không ghi đè draft, report, metadata cũ; không sửa `products/`, harness, code hay trạng thái production. Nếu file đích đã tồn tại, dừng và báo để tránh ghi đè một lượt đã giao.

File gồm đúng ba phần theo thứ tự:

1. **Bản gốc:** nguyên văn hai đoạn ở mục 3; kèm đường dẫn và commit baseline trên một dòng.
2. **Bản biên tập:** lời kể liền mạch để Owner đọc, không chen chú giải kỹ thuật.
3. **Đã sửa gì:** tối đa ba bullet ngắn, nêu vị trí/cụm từ và quyết định cụ thể. Nếu thêm chi tiết từ input chưa có trong đoạn gốc, chỉ rõ substrate ID; nếu tái dựng đáng kể, nhận diện tại đây. Tổng ghi chú không dài hơn một đoạn gốc; không tự chấm chất lượng hay tuyên bố khán giả đã dễ hình dung.

Không tạo `writing-report.md`, `meta.json`, plan riêng, scorecard, dashboard hoặc bản tổng kết nguyên nhân. Không yêu cầu chain-of-thought. Khi được giao thực hiện, commit đúng file này lên nhánh đích theo cách thông thường, không force-push. Bàn giao bằng link bản đọc và một câu mời Owner chỉ chỗ còn khó hình dung.

## 6. Owner đọc và quyết định

Hai câu hỏi đọc, không phải biểu mẫu bắt Owner điền:

- So với bản gốc, lần này có dễ hình dung hơn không; câu nào vẫn phải tự đoán?
- Có chỗ nào rõ hình ảnh hơn nhưng chậm, vụn hoặc vẫn chưa muốn nghe tiếp?

Owner có thể trả lời tự do bằng một câu hoặc chỉ một cụm từ. Không yêu cầu đọc report, đánh giá toàn bộ outline, chấm điểm hay chứng minh cảm nhận. Tính đúng nguồn do người thực hiện kiểm tra trong phạm vi input, không đẩy việc kiểm chứng ấy sang Owner.

Giao được file chỉ hoàn thành công việc biên tập, chưa chứng minh cải thiện. Chỉ phản hồi thực tế của Owner mới cho biết thay đổi có giải quyết khó chịu hay không. Không kết luận đạt chuẩn FoC, tăng retention hoặc tìm được nguyên nhân duy nhất từ một bản trước–sau.

## 7. Điểm dừng bắt buộc

Giao một bản rồi dừng. Không tự chạy Writer tiếp, sửa harness, mở nghiên cứu hoặc chuyển sang phần kế tiếp. Nếu Owner vẫn thấy khó hình dung, bám vào đúng vị trí họ chỉ ra; chờ lệnh sửa tiếp trên cùng trường hợp thay vì tạo thêm báo cáo hoặc đổi toàn bộ cách làm.

Nếu Owner thấy cải thiện, giữ cặp trước–sau làm ví dụ thực tế. Chỉ khi Owner yêu cầu mới rút bài học vào harness; không tự tổng quát một lần thành quy tắc cho mọi đoạn. Vòng reset này kết thúc ở lần đọc của Owner, không ở số tài liệu đã hoàn thành.
