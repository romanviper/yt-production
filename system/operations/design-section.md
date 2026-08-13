# Operation — Design Section

## Responsibility

Biến section brief và evidence pool thành một story plan có lựa chọn. Không viết narration.

## Core rule

Evidence pack là phạm vi sự thật, không phải checklist phải kể hết. Một fact chỉ được đưa vào narration nếu nó tạo tension, làm đổi mô hình hiểu của khán giả, giải thích mechanism, tạo consequence hoặc trả payoff.

## Output

`story-plan.json` phải:

- diễn đạt một governing idea bằng ngôn ngữ phổ thông;
- xác định audience question và payoff;
- phân loại mọi claim vào đúng một vai trò: `narrated`, `support`, `guardrail` hoặc `omit`;
- chỉ chọn 1–5 narrated claims;
- ghi một lý do ngắn cho mỗi narrated/support claim: nó tạo tension, explanatory turn, consequence hay bridge nào;
- thiết kế 4–8 beats theo tiến triển câu chuyện, không theo thứ tự source/claim;
- mỗi beat nói rõ hiểu biết của khán giả thay đổi thế nào sau beat đó;
- giới hạn thuật ngữ và giải thích từng thuật ngữ bắt buộc bằng lời nói thông thường;
- nêu opening move, ending move và comprehension test.

`guardrail` dùng để ngăn overclaim, không tự động xuất hiện trong prose. `omit` nghĩa là fact đúng nhưng không phục vụ section hiện tại.

Status phải là `draft`. Chỉ người dùng được approve story plan.
