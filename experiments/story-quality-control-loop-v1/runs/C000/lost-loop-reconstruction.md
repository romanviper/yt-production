# Lost loop reconstruction — chuỗi post-run-05 `6,6 -> 8,1`

Cycle C000 · forensic only · không có generation hay evaluation mới trong cycle này.

## Phạm vi bằng chứng

| Provenance class | Nguồn |
|---|---|
| Verified fact (git-resolved tại pin SHA) | `2cebbbd9…` (pause checkpoint), `e29a984d…` (audit run-01..05), `dd93c67e…` (p01-voice-v1 log/review metadata), `7b0328ac…` (writer-outcome prototype diff), blob `391febd8…` (benchmark, chỉ metadata) |
| Checkpoint assertion | Mọi score, breakdown, cost và validation state dưới đây — chỉ còn dạng văn bản trong `pause-checkpoint-20260824.md`; raw usage/test output không còn |
| Thread-only assertion | Không có mục nào được đưa vào timeline: cả 4 thread ID được giữ lại (`6a8c0f91`, `6a869f7b`, `6a8417c3`, `6a8482d8`) không resolve được trong môi trường chạy → `unverified` theo work order |
| Inference | Được ghi tường minh ở từng bước, không trộn vào fact |

## Timeline theo score

### Bước 1 — Clean replay đầu: `6,6/10`

- Input state: trạng thái sau run-01..05 trên nhánh audit; kết luận "harness v2 đã đủ" bị checkpoint tự supersede vì cả 5 run dùng cùng writer tự viết–tự sửa–tự diễn giải.
- Intervention: không có — replay sạch trên đường harness hiện hành, FoC chỉ dùng làm external calibration.
- Role topology: writer đơn, không evaluator độc lập (inference từ việc đây là "first clean replay" trước khi các điều chỉnh prototype tách vai được ghi nhận có hiệu lực).
- Evaluation còn biết: composite `6,6/10` (checkpoint assertion). Evaluator identity/model, rubric đầy đủ, comparator snapshot: missing.
- Cost còn biết: không gắn riêng cho bước này (missing).
- Missing fields: candidate text/hash, evaluator output, usage.

### Bước 2 — Một bounded revision: `7,3/10`

- Input state: output của bước 1.
- Intervention: đúng một lượt sửa có chẩn đoán (bounded revision) — hướng đi mà checkpoint liệt kê là điều chỉnh prototype "limited revision to one diagnosed pass".
- Role topology: writer tách reviewer độc lập (checkpoint assertion ở mức prototype; chi tiết từng vai của bước này: missing).
- Evaluation còn biết: composite `7,3/10`. Còn lại: missing như bước 1.
- Cost còn biết: nhóm cost "revision packet ~5,9–6,6k token vs ~13,3k đường cũ" thuộc lớp revision nói chung (checkpoint assertion), không đóng băng cho đúng bước này.
- Missing fields: diff giữa hai bản, defect list đầu vào của revision.

### Bước 3 — Clean replay mới sau evidence work: `6,7/10`

- Input state: sau khi research đã resolve material detail cụ thể hơn ("later clean replay after evidence work").
- Intervention: thay đổi dữ liệu evidence đầu vào, không phải prose edit.
- Role topology: như bước 1 (replay sạch; inference tương tự).
- Evaluation còn biết: composite `6,7/10`.
- Cost còn biết: "clean first-pass packet ~1.900 token"; "direct writer instruction 878/1.500 ceiling"; "evidence lookups giảm 10 -> 7 sau neutral material ledger" (checkpoint assertion, gắn giai đoạn này).
- Missing fields: ledger nội dung, trace, usage raw.

### Bước 4 — Revision của replay mới: `6,9/10` dù internal gate false-positive pass

- Input state: output bước 3.
- Intervention: một bounded revision.
- Role topology: internal gate + writer; điểm mấu chốt là **gate nội bộ PASS trong khi calibration ngoài cho `6,9 < 7`** — bằng chứng sớm nhất còn lại rằng approval kiểu comment-only/gate nội bộ có false positive.
- Evaluation còn biết: composite `6,9/10`; ghi chú "despite an internal false-positive pass" (checkpoint assertion).
- Cost còn biết: không tách riêng (missing).
- Missing fields: gate output gốc, tiêu chí gate lúc đó.

### Bước 5 — Senior-edited candidate: `8,1/10`

- Input state: chuỗi trên + chẩn đoán nghiêm ngặt hơn ("after stricter diagnosis").
- Intervention: một lượt senior edit có chẩn đoán (checkpoint assertion về nhãn vai; identity/model của senior editor: missing).
- Role topology: writer + senior editor khác vai; chưa qua reusable production gate, chưa có independent evidence audit, chưa xác nhận không bleed sang mission P02 — tức **không phải draft P01 chính thức**.
- Evaluation còn biết: composite `8,1/10` kèm breakdown `causal_chain 8,6 · question/payoff 8,7 · density 8,5 · continuity 9,0 · human_immediacy 6,7`. Human immediacy giữ `6,7` vì evidence P01 đã duyệt không có named human anchor/primary voice so sánh được với FoC và việc bịa ra là cấm.
- Composite KHÔNG tái tạo được: trung bình cộng 5 dimension là `8,3`, không khớp `8,1`; trọng số/rubric/judge/comparator snapshot đều missing → composite mang nhãn `historical_summary_only`, non-reproducible.
- Candidate KHÔNG thể phục hồi byte-for-byte: text, hash, diff, evaluator output, replay artifacts đều không có trong tree của `2cebbbd9…` cũng như bất kỳ ref nào đã kiểm tra (`e29a984d`, `dd93c67e`, `7b0328ac`, `main`). Chỉ tìm thấy exact artifact mới đổi được kết luận này.
- Missing fields: candidate body/hash, rubric, judge artifact, comparator snapshot, usage.

## Điều còn bằng chứng vs điều chỉ còn summary

- **Còn bằng chứng (git-durable):** tồn tại và nội dung của pause checkpoint; cây run-01..05 (drafts + writer-notes + audit + harness v1/v2); log/review metadata p01-voice-v1 (negative controls: Goodhart khi metric vào brief writer — vòng G; self-review cùng session — ghi nhận xung đột lợi ích trong `REVIEW-C-r2.md`; multi-role PROCESS-V4 tách planner/writer×2/reviewer-truth/reviewer-narrative/verifier/user); writer-outcome prototype là đúng một dòng instruction trong `system/operations/draft-section.md` tại `7b0328ac`; benchmark blob hash/path/size.
- **Chỉ còn summary:** toàn bộ 5 score, breakdown `8,1`, mọi con số cost, regression `81/82` với `42` stale product errors (whole-product cleanliness), ba constraint được isolate.
- **Mất hẳn:** candidate `8,1`, prototype diff runtime, evaluator outputs, replay artifacts, raw telemetry.

## Hệ quả bắt buộc

1. `8,1` = `historical_summary_only`: không baseline, không champion, không bằng chứng ngang FoC.
2. `run-05` và chuỗi post-run-05 là hai giai đoạn forensic riêng; không resume từ nhánh cũ.
3. Mọi hypothesis rút từ checkpoint phải được retest trên `main` bằng clean roles trước khi dùng làm căn cứ thiết kế harness.
