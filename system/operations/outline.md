# Operation — Outline

## Responsibility

Biến research synthesis thành outline nhiều phần, story bible compact và voice profile riêng cho product. Không viết narration.

## `outline.json`

Mỗi section gồm:

- `id` dạng `P##`, title làm việc và order;
- narrative job duy nhất;
- entry/exit state;
- `question` và `payoff` là hai field riêng;
- claim IDs và dependencies;
- anchor requirements;
- bridge in/out;
- target word range;
- boundary và risk.

Outline phải có status `draft` cho tới khi người dùng approve.
`section_count` phải bằng đúng số section thực tế. Contract này được dùng chung bởi validator, approval và materializer.

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
