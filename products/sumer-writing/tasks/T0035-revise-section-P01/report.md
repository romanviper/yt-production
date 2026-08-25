# Task Report — T0035-revise-section-P01

## Status

`ready_for_review`

## Diagnosed change

Resolved formal review T0034, Issue 1, with a one-sentence revision in `03_sections/P01/draft.md`.

**Before:** “Bulla lúc đó mang hai cách giữ cùng một lượng: các vật nằm bên trong và dấu hiện ra trên bề mặt.”

**After:** “Bulla lúc đó vừa giữ các vật bên trong, vừa cho thông tin số hiện ra trên bề mặt; nhưng không thể mặc định rằng các dấu ngoài ghi đúng lượng của số token được cất kín.”

The replacement removes unsupported contents-to-surface equivalence while preserving the material logic that numerical information becomes available on the surface.

## Scope and continuity

- Changed exactly one diagnosed sentence; no adjacent sentence was changed.
- Preserved the hook, section structure, payoff, P02 boundary, truth ceiling and anti-linear-genealogy guardrail.
- Did not change `handoff.md` because the achieved exit state and continuity facts did not change.
- Did not use the evidence broker or any external source.
- Draft word count: 1,148 whitespace-delimited words, within the 1,050–1,550 target.

## Outputs

- Updated `03_sections/P01/draft.md`.
- Created `03_sections/P01/revision-log.md` with the issue and observable acceptance result.
- Created this report and updated `operator-brief.json`.

## Validation

- `scripts/validate.py products/sumer-writing`: pass.
- `scripts/task.py verify products/sumer-writing T0035-revise-section-P01`: packet fresh và trong budget.
- `scripts/check_scope.py products/sumer-writing`: pass; tám changed paths đều trong active-task scope.
