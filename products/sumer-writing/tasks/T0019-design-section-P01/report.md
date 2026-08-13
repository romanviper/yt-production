# Task Report — T0019 design_section P01

## Result

P01 đã được thiết kế lại theo story-plan contract v2. Draft cũ chỉ được dùng để chẩn đoán repetition/padding; không có prose nào được sửa. Story plan ở trạng thái `draft`, chờ người dùng duyệt.

## Fields changed

- `schema_version`: 1 → 2.
- `status`: giữ ở `draft` sau khi mở lại story design; xóa metadata approval cũ theo router.
- `governing_idea`: chuyển từ câu payoff lặp lại sang nguyên tắc thay đổi trong năng lực lưu thông tin.
- `audience_question`: hỏi hiện vật đã thay đổi điều gì thay vì hỏi lại nội dung payoff.
- `audience_payoff`: cụ thể hóa ở loại và lượng ngũ cốc trên P005390.
- `structure_shape`: thêm object-led hinge riêng cho section.
- `word_budget`: đề xuất 550–700 từ thay cho 950–1200, kèm rationale theo narrative load.
- `evidence_roles`: narrated giảm từ ba xuống hai; support giảm từ hai xuống một; ba claim không làm câu chuyện tiến lên chuyển sang omit.
- `claim_use`: chỉ còn lý do cho hai narrated claim và một support claim.
- `beats`: giảm từ năm beat template xuống ba movement riêng; payoff chỉ xuất hiện ở B02 và không được diễn giải lại ở B03.
- `opening_move`, `ending_move`, `comprehension_test`: sửa để phục vụ shape mới và chặn repetition.

## Structure decision

Shape: `object_puzzle → payoff → formation_turn`.

- B01 dùng giới hạn của P005390 để phá mô hình “tablet = câu đang chờ dịch”.
- B02 vừa thực hiện explanatory turn vừa trả payoff; không tách reveal/payoff thành hai lần nói cùng ý.
- B03 không thêm fact và không nhắc lại kết luận; chỉ đổi câu hỏi sang quá trình hình thành ở P02.

## Evidence decision

- Narrated: `CLM-0042`, `CLM-0001`.
- Support: `CLM-0002`, chỉ dùng để định hướng niên đại tối thiểu theo brief.
- Guardrail: `CLM-0006`, `CLM-0007`, `CLM-0008`.
- Omit: `CLM-0004` không cần để trả câu hỏi; `CLM-0009` tạo chronology/bridge load không cần thiết; `CLM-0034` trùng `CLM-0004`.

## Word-budget assessment

Narrative load gồm một object, một complication, một explanatory turn/payoff và một câu hỏi chuyển tiếp. Range 550–700 từ đủ để giữ clarity và qualification; range 950–1200 đã khiến draft cũ phải diễn giải lại payoff và kéo thêm chronology/context không tạo chuyển động mới.

## Validation

Story plan đạt contract v2, phân loại đủ chín claim, có hai narrated claim, ba beat và đúng một payoff beat. Không sửa draft hoặc handoff.

