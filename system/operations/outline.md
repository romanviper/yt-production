# Operation — Outline

## Responsibility

Biến research synthesis thành outline nhiều phần và story bible compact. Không viết narration.

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
