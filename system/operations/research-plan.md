# Operation — Research Plan

## Responsibility

Chia product đã khóa thành các research workstream độc lập. Không đánh giá lại việc có làm subject hay không.

## Output contract

`plan.json` gồm:

- `status: draft`;
- `central_research_question`;
- `hypotheses_to_test`;
- `shared_research_protocol`: chronology, terminology, case selection, cross-cutting ownership và common handoff contract;
- `workstreams[]`: `id` dạng `WS##`, title, question, in/out boundary, ownership, required evidence classes, completion criteria và `synthesis_handoff`;
- `coverage_matrix`: mỗi lifecycle stage được workstream nào chịu trách nhiệm;
- `synthesis_questions` cần nối các workstream.

Không để hai workstream cùng sở hữu một question. Dependency phải được khai báo, không ngầm hiểu.

## Evidence for explanation and evidence for story

Research phải đủ để kiểm tra claim, nhưng cũng phải giữ lại vật liệu cụ thể để các lớp sau có thể kể được lịch sử mà không bịa.

Khi một lifecycle stage có thể được mang bởi một vật thể, con người, thao tác, process, documented encounter, failure hoặc consequence, plan phải giao rõ workstream nào chịu trách nhiệm tìm và giữ evidence đó. Narrative value một mình không đủ để chọn case; nhưng một research plan chỉ thu abstract claims mà không ai sở hữu concrete carrier evidence cho các state change quan trọng cũng chưa đủ cho production.

Không bắt mỗi workstream phải tìm anecdote. Nếu evidence không cho phép một carrier cụ thể, workstream phải được phép bàn giao `không có carrier đủ chắc` thay vì ép tạo câu chuyện.

Mọi field ảnh hưởng đến execution phải được materializer truyền vào isolated workstream brief; không đặt instruction chỉ có global synthesis nhìn thấy.
