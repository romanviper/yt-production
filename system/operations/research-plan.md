# Operation — Research Plan

## Responsibility

Chia product đã khóa thành các research workstream độc lập. Không đánh giá lại việc có làm subject hay không.

## Output contract

`plan.json` gồm:

- `status: draft`;
- `central_research_question`;
- `hypotheses_to_test`;
- `workstreams[]`: `id` dạng `WS##`, title, question, in/out boundary, required evidence classes, seed claims và completion criteria;
- `coverage_matrix`: mỗi lifecycle stage được workstream nào chịu trách nhiệm;
- `synthesis_questions` cần nối các workstream.

Không để hai workstream cùng sở hữu một question. Dependency phải được khai báo, không ngầm hiểu.

