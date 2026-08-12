# 08 — Agent Playbooks

Agent chọn đúng một playbook theo `task_type`.

## `premise_research`

Output: premise candidates có falsification test và recommendation. Không viết outline hoặc title list nếu work order không yêu cầu.

## `source_hunt`

Output: source records ở trạng thái `discovered`. Không nâng lên `reviewed` nếu chưa đọc phần liên quan và ghi locator.

## `claim_audit`

Output: claim ledger được cập nhật, counterevidence và confidence. Không viết narration.

## `story_architecture`

Output: causal spine, state-change map và chapter manifest. Chỉ dùng claim đã đủ trạng thái cho planning; đánh dấu rõ gap.

## `chapter_brief`

Output: một brief có narrative job, evidence, entry/exit, payoff, bridges và word budget. Không draft prose.

## `chapter_draft`

Output: một chapter hoặc sequence. Không sửa brief đã khóa hoặc chapter lân cận. Nếu bridge cần thay đổi ở file khác, ghi change request.

## `local_review`

Output: diagnosis có vị trí, loại lỗi, mức severity và đề xuất phạm vi sửa. Không rewrite nếu work order chỉ cấp quyền review.

## `targeted_revision`

Output: patch nhỏ nhất vượt acceptance test; cập nhật revision log. Không làm “polish toàn bộ” ngoài scope.

## `integration_review`

Output: continuity, redundancy, pace và payoff audit cấp toàn phim. Mặc định chỉ viết report/change requests, không sửa prose.

## `assembly`

Output: build artifact qua script. Không hand-edit delivery.

## Handoff format

Mọi task kết thúc bằng bốn dòng:

1. `Completed:` outcome đã đạt;
2. `Changed:` đường dẫn chính xác;
3. `Evidence/Checks:` validation đã chạy;
4. `Blocked/Next gate:` điều còn thiếu và ai có quyền quyết định.

