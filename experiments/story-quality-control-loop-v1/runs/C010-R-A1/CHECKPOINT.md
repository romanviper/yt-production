# CHECKPOINT — C010-R/A1 anchor repair

## 1. Outcome và trạng thái

Sửa xong forensic binding của human gold **trước** khi xây bất kỳ fixture nào. Kết quả: đúng **0** human gold hợp lệ trong runtime hiện tại (C1 = `unusable_in_runtime`), 8 anchors rejected/unusable kèm reason code, binding C1 sai đã bị đánh dấu và thay bằng binding đúng đã freeze. Trạng thái: dừng chờ planner review. Base: `9ede6d825a541472409f3db48907e96eb3a7a24e` (đã push lên origin trước khi làm).

## 2. Frozen baseline

Phạm vi khóa theo lượt: chỉ forensic gold recovery; không fixture, không judge, không metric, không harness/product/STATE/C010-artifact changes. Đầu vào freeze: C010 work order + seed + judge prompt (không đổi), runs/C010/** (read-only), 4 retained thread IDs, exact git objects.

## 3. Chính xác điều đã thay đổi

Chỉ ba file mới dưới `runs/C010-R-A1/`: `anchor-registry.json`, `anchor-check.md`, `CHECKPOINT.md`. Zero mutation mọi nơi khác.

## 4. Kết quả kiểm tra

- Commit `324bc8f928824123bb6d5bfbc57ca2c69015c99f` resolve type=commit ("Draft C003 P01 with writer-authorship harness", 2026-08-20 15:08:47 +07:00); blob P01 draft tại commit đó **= `ceee1b9bb2f0813088b8a8a595ee22826f57f006`** — khớp kỳ vọng.
- Candidate cũ `7dcc1033cc76a61ae85a04bd699e9494d56f94cf` tồn tại (blob), sinh tại `246e4a0` 19/08.
- Binding C010 cũ `3424c985…` **rejected**: lần đầu xuất hiện `c3daaa3` 20/08 23:27 — postdates verdict ~8 giờ.
- Tính duy nhất: timeline P01 draft quanh 17–21/08 cho thấy tại thời điểm verdict chỉ có một ứng viên "mới" → binding sửa lỗi là duy nhất.
- Runtime read capability: 4/4 thread ID không đọc được; exhaustion được chứng minh bằng exact-ID fail + full browse + nhiều discovery sweep + filename scan (lead và subagent độc lập cùng kết luận).
- Usage telemetry: `unknown` trung thực.

## 5. Evidence paths/hashes

- Registry đầy đủ accepted/rejected + reason codes: `runs/C010-R-A1/anchor-registry.json`.
- Trả lời sáu câu hỏi ngắn: `runs/C010-R-A1/anchor-check.md`.
- Git objects tự chứng minh qua plumbing (`git cat-file`, `git rev-parse`, log timeline) — planner tái lập được từng dòng.

## 6. Failure / deviation / dữ liệu không còn

- Không đọc được raw user turn → C1 phải mang `unusable_in_runtime`; đây là giới hạn runtime, không phải bằng chứng chống lại verdict.
- Deviation so với lượt: không có. Hai yêu cầu user-gold cũ về G2-vs-H2 và "vs FoC" **vẫn đứng** (chưa được thỏa); yêu cầu adjudication A2 **đã rút khỏi danh sách** vì A2 retired (sai premise từ đầu, không phụ thuộc user).
- Subagent transcripts nằm ngoài repo (deleg_a47604a6, task-0/task-1) — digests không ghi vì lượt này cấm ledger lớn; conclusions đã lead-verify độc lập.

## 7. Planner nên tự kiểm tra

1. Chạy lại: `git rev-parse 324bc8f92…:products/sumer-writing/03_sections/P01/draft.md` → phải ra `ceee1b9b…`.
2. Timeline: `git log --all --format="%h %ad %s" -- …/P01/draft.md` → xác nhận `3424c985` postdates verdict.
3. So sánh `anchor-registry.json.corrected_binding` với seed C010 → xác nhận việc supersede.

## 8. Recommendation duy nhất

Planner phát hành **A2 với cơ chế thu thập user-gold trực tiếp**: cần chính xác 3 verdict user-authored (chi tiết loại/phạm vi ở mục 6 của `anchor-check.md`), trong đó mục (1) có thể auto-thỏa nếu raw turn `75be696a` được cấp dưới dạng đọc được. Sau khi đủ, mới quay lại fixture construction bổ sung rồi Wave C/D theo evaluation-lock C010.

## 9. Hard stop xác nhận

Sau commit: dừng tuyệt đối — không A2 phase, không fixture/judge/metric, không harness/system/product change, không work order vòng sau. Chờ planner review.
