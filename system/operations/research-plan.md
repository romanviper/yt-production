# Operation — Research Plan

## Responsibility

Chia product đã khóa thành các research workstream độc lập để acquisition factual có ownership rõ ràng. Không đánh giá lại việc có làm subject hay không và không pre-author cách kể.

> **Research plans evidence acquisition, not narrative execution.**

Research Plan chịu trách nhiệm thiết kế cấu trúc nghiên cứu factual:

- central research question;
- hypotheses cần kiểm tra;
- chronology và terminology protocol;
- factual/mechanism questions;
- required evidence classes;
- scope ownership và dependency;
- contradiction/counterevidence responsibilities;
- cross-cutting factual ownership;
- completion criteria;
- synthesis handoff.

Research Plan không quyết định hoặc phân công story carrier, object/person/process để audience follow, narrative material, opening/reversal/ending candidate, narratability, sequence kể chuyện, storytelling value hay carrier cho một state change.

## Output contract

`plan.json` gồm:

- `status: draft`;
- `central_research_question`;
- `hypotheses_to_test`;
- `shared_research_protocol`: chronology, terminology, case selection, cross-cutting factual ownership và common handoff contract;
- `workstreams[]`: `id` dạng `WS##`, title, question, in/out boundary, ownership, required evidence classes, completion criteria và `synthesis_handoff`;
- `coverage_matrix`: mapping factual/research coverage sang workstream chịu trách nhiệm; đây không phải story/lifecycle architecture;
- `synthesis_questions` cần nối các workstream về chronology, mechanism, contradiction, qualification hoặc factual relationship.

Không để hai workstream cùng sở hữu một question. Dependency phải được khai báo, không ngầm hiểu.

## Evidence preservation

Plan có thể yêu cầu một workstream giữ source-level concrete detail khi detail đó có nguy cơ mất qua compression hoặc có provenance/limitation phức tạp. Lý do là **evidence preservation**, không phải để chọn cách kể.

Ví dụ có thể giữ measurement, physical description, documented action, spatial relation, chronology detail hoặc explicit source-supported sequence nếu chúng cần để reconstruct factual evidence sau này. Việc detail đó có trở thành narration, carrier hay không thuộc downstream authorship.

Không bắt mỗi workstream phải tìm anecdote, carrier hoặc “story material”. Absence of such material không làm workstream thất bại nếu factual questions, evidence classes, contradictions và completion criteria đã được đáp ứng.

Mọi field ảnh hưởng đến execution factual phải được materializer truyền vào isolated workstream brief; không đặt instruction chỉ có global synthesis nhìn thấy.
