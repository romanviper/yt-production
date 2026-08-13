# Operation — Revise Section

## Responsibility

Áp dụng change request đã được con người chọn lên một section.

## Rules

- Review không đồng nghĩa mọi suggestion đều được duyệt; `change-request.md` là authority.
- Dùng patch nhỏ nhất vượt acceptance test.
- Ngoại lệ: nếu change request cho phép revision class R5 hoặc yêu cầu thiết kế lại narrative, có thể thay toàn bộ prose của section. Khi đó vẫn phải giữ section boundary, evidence ceiling và exit state.
- Nếu fix phá brief, evidence hoặc section khác, dừng và tạo impact report.
- Cập nhật handoff nếu exit state/setup/continuity thực sự đổi.
- Revision log ghi issue IDs, vị trí và kết quả; không ghi “polished”.
