# Operation — Design Section

## Responsibility

Biến section brief và evidence pool thành một story plan có lựa chọn. Không viết narration.

## Core rule

Evidence pack là phạm vi sự thật, không phải checklist phải kể hết. Một fact chỉ được đưa vào narration nếu nó tạo tension, làm đổi mô hình hiểu của khán giả, giải thích mechanism, tạo consequence hoặc trả payoff.

## Output

`story-plan.json` phải:

- diễn đạt một governing idea bằng ngôn ngữ phổ thông;
- xác định audience question và payoff;
- mô tả `structure_shape` riêng của section thay vì chọn một bố cục mặc định;
- đề xuất word range đúng với material thực tế và giải thích vì sao; được phép ngắn hoặc dài hơn outline, không được kéo prose cho đủ quota;
- phân loại mọi claim vào đúng một vai trò: `narrated`, `support`, `guardrail` hoặc `omit`;
- chỉ chọn 1–5 narrated claims;
- ghi một lý do ngắn cho mỗi narrated/support claim: nó tạo tension, explanatory turn, consequence hay bridge nào;
- thiết kế 2–12 beats theo đúng số chuyển động câu chuyện cần, không theo thứ tự source/claim;
- mỗi beat nói rõ hiểu biết của khán giả thay đổi thế nào sau beat đó;
- giới hạn thuật ngữ và giải thích từng thuật ngữ bắt buộc bằng lời nói thông thường;
- nêu opening move, ending move và comprehension test.

`guardrail` dùng để ngăn overclaim, không tự động xuất hiện trong prose. `omit` nghĩa là fact đúng nhưng không phục vụ section hiện tại.

Status phải là `draft`. Chỉ người dùng được approve story plan.

Không bắt mọi section có cùng chuỗi hook → tension → reveal → bridge. Mọi section phải trả payoff của chính nó; tension hoặc bridge chỉ xuất hiện khi section thực sự cần. Tên `function` của beat có thể mô tả tự do bằng `snake_case` ngắn. Khi người dùng approve, budget recommendation được áp dụng đồng bộ vào section và outline; nếu tổng runtime ra ngoài envelope, approval dừng để re-balance thay vì padding.

Nếu packet có `story-plan-change-request.md`, đây là authority cho vòng hiện tại. Yêu cầu này có thể xuất hiện sau khi prose đã phơi bày lỗi kiến trúc; khi đó draft/review cũ chỉ là diagnostic input, output vẫn chỉ là story plan. Patch đúng các thay đổi được yêu cầu, giữ phần đã đạt và ghi rõ field nào đổi trong report. Không trả lại nguyên artifact cũ như một bản sửa.
