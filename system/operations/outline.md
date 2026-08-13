# Operation — Outline

## Responsibility

Biến research synthesis thành kiến trúc của toàn bộ kịch bản, rồi mới chia thành các production section đủ nhỏ để Agent xử lý độc lập. Không viết narration.

## Thứ tự thiết kế

1. Xác định audience promise, đường biến đổi tổng thể và các macro movement của toàn câu chuyện.
2. Ước lượng tải kể chuyện của từng movement trong tổng thời lượng.
3. Chỉ sau đó mới đặt ranh giới `P##` tại những state change hoặc điểm review có nghĩa.

Không chọn trước một con số đẹp rồi chia đều research để lấp ô. Section count và độ dài phải là kết quả của kiến trúc. Một chapter mà khán giả cảm nhận có thể gồm nhiều production section; `P##` trước hết là work unit để giới hạn context và revision scope, không bắt buộc là chapter hiện trên màn hình.

## `outline.json`

`script_architecture` phải mô tả:

- audience promise và design rationale của toàn kịch bản;
- total word envelope suy ra từ duration × narration WPM;
- các macro movement có entry state, exit state, narrative job và danh sách section liên tục theo đúng thứ tự.

Mỗi section gồm:

- `id` dạng `P##`, title làm việc và order;
- narrative job duy nhất;
- macro movement mà nó phục vụ và structural role riêng;
- entry/exit state;
- `question` và `payoff` là hai field riêng;
- `planned_moves`: phác họa bố cục riêng của section bằng số move thực sự cần, không dùng template chung;
- claim IDs và dependencies;
- anchor requirements;
- bridge in/out;
- target word range và lý do phân bổ dựa trên narrative load;
- boundary và risk.

Outline phải có status `draft` cho tới khi người dùng approve.
`section_count` phải bằng đúng số section thực tế, nhưng không có default 10. Không cân bằng độ dài cho đẹp: prologue/bridge có thể ngắn, causal hinge có thể dài. Mỗi production section tối đa 3.000 từ; nếu một movement cần dài hơn, chia work unit mà không bịa thêm chapter cho khán giả. Tổng các range phải còn ít nhất một độ dài khả thi trong total word envelope. Contract này được dùng chung bởi validator, approval và materializer.

## `story-bible.md`

Chỉ giữ premise, causal spine, global chronology, canonical terminology, central entities, thematic rule, setup/payoff map và global exclusions. Không nhét research notes vào story bible.

## `voice-profile.md`

Đọc benchmark như dữ liệu về chức năng kể chuyện, không như prose để bắt chước. Profile phải có:

- một mô tả cụ thể về vai người kể, độ gần/xa và emotional register của product;
- 3–5 chức năng đáng học từ benchmark;
- cách mỗi chức năng được chuyển thành lựa chọn nguyên bản bằng tiếng Việt;
- surface signatures bị cấm mô phỏng;
- các test ngắn để reviewer nhận ra draft đúng fact nhưng sai giọng.

Profile có status `draft` và được duyệt cùng outline. Nó phải đủ cụ thể để hai writer khác nhau tạo prose cùng một family, nhưng không được chứa câu mẫu bắt chước creator tham chiếu.
