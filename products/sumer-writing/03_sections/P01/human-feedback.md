# Human Feedback — P01

Status: human_rejected_for_rework

Recorded: 2026-08-25

## Human verdict

Bản P01 hiện tại **không đạt trải nghiệm kể chuyện**, bất chấp formal reviewer đã cho `pass`.

Phản ứng trực tiếp của người duyệt ngay từ câu mở đầu:

> “Đừng bắt đầu lịch sử chữ viết bằng một tấm bảng. Hãy bắt đầu bằng một vật còn lạ hơn: một bulla.”

Người duyệt cho biết sau câu này **gần như không muốn tiếp tục review**, và mô tả giọng kể là **“cực kỳ máy móc và không tự nhiên, rất gượng gạo.”**

Đây là human creative verdict có thẩm quyền cao hơn machine quality score. Không được dùng `review.md: pass` để suy ra rằng P01 đã đạt chất lượng kể chuyện hoặc sẵn sàng phê duyệt.

## Failure quan sát được

Vấn đề không phải riêng từ `bulla`, cũng không phải vì mở bằng một vật thể là sai. Failure nằm ở **cảm giác cấu trúc kể chuyện đang lộ ra trên bề mặt câu chữ**.

### 1. Meta-narration thay cho narration

“Đừng bắt đầu… Hãy bắt đầu…” nói với khán giả về **cách tác giả đang lựa chọn kể câu chuyện** thay vì đơn giản đưa họ vào câu chuyện. Người nghe thấy bàn tay của writer trước khi thấy lịch sử.

### 2. Storytelling device bị thi hành như công thức

Opening cho cảm giác writer đang lần lượt thực hiện các bước: `concrete object -> contrast -> paradox -> thesis -> context`. Từng kỹ thuật có thể hợp lý riêng lẻ, nhưng tổng thể nghe như một template đang được chạy chứ không như một người kể chuyện đang suy nghĩ và kể tự nhiên.

### 3. Curiosity bị tuyên bố thay vì được tạo ra

Cụm “một vật còn lạ hơn” yêu cầu người nghe tin rằng vật này đáng tò mò trước khi draft tạo ra lý do để quan tâm. Sau đó thuật ngữ `bulla` xuất hiện ngay, khiến opening có thêm cảm giác writer đang cố dựng hook bằng novelty.

### 4. Writer gọi tên hiệu ứng thay vì để hiệu ứng tự xảy ra

Ngay sau đó draft dùng các thao tác như “bulla tạo ra một nghịch lý” và “trước câu chuyện về chữ, đã có bài toán vật chất ấy”. Cách diễn đạt này liên tục đóng khung, giải thích và đặt nhãn cho chính narrative move của nó. Vì vậy prose có vẻ được thiết kế quá lộ, thiếu sự tự nhiên.

### 5. Continuation pressure thực tế thấp dù hook mechanics đầy đủ

Formal evaluator chấm `hook_and_audience_promise = 9`, nhưng phản ứng human là muốn dừng ở câu đầu. Đây là một **false positive calibration**: evaluator đang thưởng cho sự hiện diện của các thành phần hook (object, contrast, paradox, question) nhưng không đo được việc chúng có thực sự khiến người nghe muốn nghe tiếp hay không.

## Chẩn đoán tầng hệ thống

### Draft problem

Current P01 có `designed-storytelling feel`: người nghe có thể nhìn thấy kỹ thuật kể chuyện đang vận hành. Điều này làm prose máy móc, gượng và thiếu giọng kể tự nhiên.

### Evaluator problem

Quality gate hiện có thể đánh đồng:

`concrete carrier + clear progression + explicit payoff = strong storytelling`

Trong case này phép đo đó sai. Một opening có thể rõ cấu trúc, cụ thể và dễ retell nhưng vẫn không hấp dẫn hoặc tự nhiên.

Machine pass vì vậy **không được coi là creative approval**. Human audience-experience judgment vẫn là authority cuối.

## Không được biến feedback này thành surface rules

Không sửa harness bằng các lệnh kiểu:

- cấm mở bằng “Đừng bắt đầu…”;
- cấm `bulla` ở câu đầu;
- bắt buộc/không bắt buộc object opening;
- cấm paradox;
- thêm một beat sequence mới.

Các rule như vậy chỉ Goodhart trên triệu chứng và sẽ tiếp tục làm writer máy móc.

## Điều cần thay đổi ở lần viết lại

Mục tiêu không phải “tìm một hook khác” theo công thức. Lần viết lại phải tạo cảm giác **một câu chuyện được kể vì bản thân lịch sử đang dẫn người kể đi**, chứ không phải writer đang trình diễn kỹ thuật storytelling.

Observable acceptance:

1. Opening không khiến người nghe chú ý tới kỹ thuật dựng opening.
2. Curiosity/stakes xuất hiện từ nội dung hoặc tình huống lịch sử, không từ lời tuyên bố rằng một vật/chi tiết là lạ, quan trọng hay nghịch lý.
3. Prose nghe tự nhiên khi đọc thành tiếng; framing chỉ xuất hiện khi thật sự cần cho nghĩa, không để báo cho người nghe biết writer đang làm narrative move nào.
4. Người duyệt có **mong muốn tiếp tục đọc/nghe sau đoạn mở**, thay vì chỉ có thể nhận ra rằng opening được cấu trúc đúng.
5. Mission, evidence ceiling và section boundary vẫn giữ nguyên; không cần thêm creative method bắt buộc.

## Routing recommendation

Feedback này đủ rộng để **không nên sửa thêm một câu cục bộ trên bản hiện tại**. Nếu P01 được rework, ưu tiên một fresh `draft_section` pass từ cùng mission/evidence ceiling với writer không nhìn machine score và không được yêu cầu giữ object/paradox opening hiện tại.

Evaluator sau đó nên xem `naturalness / visible technique / desire to continue` như chẩn đoán audience-experience, nhưng không biến chúng thành quota hoặc checklist cho writer.
