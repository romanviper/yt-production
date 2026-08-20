# Sumer Writing — current production state

Product workspace: `sumer-writing`  
Current cycle: `C003`  
Current state: outline approved; 8 sections; no active task.

## Canonical authority

Agent bắt đầu từ `tasks/ACTIVE.json` và chỉ làm operation được task router/packet giao. Không tự quét toàn bộ product để lấy context.

Nếu instruction trong product mâu thuẫn với `system/operations/registry.json` hoặc packet của task hiện tại, system registry + task packet là authority.

## Writer boundary

Với `draft_section`, writer chỉ dùng các input được compile trong packet. Canonical product inputs hiện tại là:

- `02_outline/story-bible.md`
- `02_outline/voice-profile.md`
- `03_sections/{section}/section.json`
- `03_sections/{section}/brief.md`
- `03_sections/{section}/narration-pack.json`
- `03_sections/{section}/continuity-in.md`

Evidence cần thêm phải đi qua bounded evidence access (`scripts/draft_evidence.py`).

Các file upstream như full `outline.json`, `claim-ledger.json`, `source-index.json`, research workstreams, completed task packets và `_history/` không phải direct writer input trừ khi packet của operation hiện tại khai báo rõ.

Không dùng draft, handoff, story-plan, material route hoặc feedback từ cycle/run cũ làm context cho một clean writer regression.

## Current flow

`research → synthesis → outline → materialize section handoff → draft/review từng section → integration → assembly`

Research owns truth. Outline owns architecture. Writer owns authorship. Evaluation judges outcome.
