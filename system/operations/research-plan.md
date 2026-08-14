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

Mọi field ảnh hưởng đến execution phải được materializer truyền vào isolated workstream brief; không đặt instruction chỉ có global synthesis nhìn thấy.
