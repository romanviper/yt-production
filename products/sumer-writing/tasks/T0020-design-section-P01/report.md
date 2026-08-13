# Task Report — T0020 design_section P01

## Result

Đã lưu lại `story-plan.json` như artifact schema v2 chính thức cho vòng duyệt này. Không sửa prose, không sinh narration pack và không approve.

## Exact alignment requested

- `schema_version`: `2`.
- `status`: `draft`.
- `structure_shape`: `object_puzzle → payoff → formation_turn`.
- `word_budget.recommended`: `min 550`, `max 700`.
- Beat functions theo đúng thứ tự: `object_puzzle`, `payoff`, `formation_turn`.
- Evidence roles:
  - narrated: `CLM-0042`, `CLM-0001`;
  - support: `CLM-0002`;
  - guardrail: `CLM-0006`, `CLM-0007`, `CLM-0008`;
  - omit: `CLM-0004`, `CLM-0009`, `CLM-0034`.

## Field changed from T0020 baseline

- `structure_shape`: thay mô tả diễn giải bằng đúng canonical sequence `object_puzzle → payoff → formation_turn`, loại bỏ chênh lệch giữa phần bàn giao và artifact.

## Validation

Artifact đạt story-plan contract v2, có đúng ba beat theo thứ tự yêu cầu, budget 550–700, evidence roles đầy đủ và status `draft`.

