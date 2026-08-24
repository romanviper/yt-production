# CHECKPOINT — C000 lost story-quality loop reconstruction

## 1. Outcome và trạng thái

C000 hoàn tất ở mức forensic-only: tái dựng chuỗi post-run-05 `6,6 -> 7,3 -> 6,7 -> 6,9 -> 8,1` với provenance class cho từng mốc, registry hypothesis 7 mục kèm smallest clean test, và source-index hash-resolve đầy đủ. Không sinh draft, không đụng harness/product/system. Trạng thái: `awaiting_planner_review`, `next_authority=planner_reviewer`, recommendation duy nhất của worker: **một bước nhỏ C010 evaluator calibration** (mục 8). Base commit: `aa778ac3e7f5823b1b1a3bf2d5b1138ee3970b78` (`main`).

## 2. Frozen baseline

- Work order: `experiments/story-quality-control-loop-v1/WORK-ORDER-C000.md` sha256 `f628aff5…90537`.
- Protocol `CONTROL-LOOP.md` `54be114e…83e5`; contracts và seed đã hash trong `manifest.json`.
- Active task bind read-only: `T0031-draft-section-P01` (state `ready`) — không thực thi.
- Không có hypothesis generation nào được freeze trong C000 (cycle không có treatment); registry là đầu vào cho planner khóa, không phải cam kết chạy.

## 3. Chính xác điều đã thay đổi

Chỉ các run-ledger file dưới `runs/C000/` (manifest, events.jsonl có event-hash chain, source-index, changes=`[]`, hypotheses, decision, CHECKPOINT này) và một trường trong `STATE.json` (`ready_for_worker` -> `awaiting_planner_review`, `next_authority=planner_reviewer`, `last_checkpoint` path; `last_checkpoint_commit` để planner điền). Zero mutation system/product/candidate — `changes.json = []`.

## 4. Kết quả hard gates / quality / usage

| Gate | Kết quả |
|---|---|
| G0 reproducibility | pass — mọi ref dùng đều resolve bằng SHA pin; mọi claim score gắn nhãn nguồn |
| G4 governance | pass — write set ⊆ allowlist; subagent read-only; benchmark text không đọc |
| Quality | n/a — không candidate mới; composite cũ bị hạ nhãn (mục 6) |
| Usage | token telemetry `unknown` trung thực (runtime không cấp) |

## 5. Evidence paths/hashes cho kết luận chính

- Chuỗi score + breakdown + cost: `git show 2cebbbd9f45ffa68bec453db1616cd740455825a:experiments/p01-harness-audit-20260824/pause-checkpoint-20260824.md` (blob `96db3a28…11ba`) — toàn bộ mang nhãn `checkpoint_assertion`.
- Run-01..05 durable controls: tree `e29a984d…36669` subtree `b7ff0c9b…c783`.
- Negative controls (Goodhart vòng G; self-review conflict trong REVIEW-C-r2; multi-role PROCESS-V4): `dd93c67e…70d3c9` subtree `3140ca4f…4a5e` (chỉ log/review metadata; drafts/pack không mở).
- Writer-outcome prototype = đúng 1 dòng trong `system/operations/draft-section.md`: diff parent `581e44a2` -> `7b0328ac`.
- Benchmark P01-equivalent: blob `391febd8…b9061`, 3591 bytes, path trên main — chỉ metadata.
- Chi tiết đầy đủ: `runs/C000/source-index.json`, timeline: `runs/C000/lost-loop-reconstruction.md`.

## 6. Failure, disagreement, deviation, dữ liệu không còn

- **Candidate `8,1` không thể phục hồi byte-for-byte**: body/hash/diff/evaluator output/replay artifacts vắng mặt trên mọi ref đã kiểm tra (kể cả transient paths ngoài checkpoint tree). Nhãn bắt buộc: `historical_summary_only`; không baseline, không champion.
- **Composite `8,1` non-reproducible**: trung bình 5 dimension còn lưu là `8,3 ≠ 8,1`; weighting/rubric/judge/comparator missing.
- **Internal gate false-positive**: bước `6,9` PASS gate nội bộ trong khi external calibration <7 — bằng chứng trực tiếp cho nhu cầu evaluator độc lập.
- **Thread evidence `unverified`**: cả 4 thread ID giữ lại không resolve được bằng session-read tool hiện có; theo work order không tìm theo title gần giống, không gửi message vào thread cũ. Không có thread-only assertion nào được đưa vào timeline.
- Deviation: không có so với work order. Subagent thứ ba (`method_auditor`) không cần thiết vì hai agent đầu không để lại câu hỏi phương pháp nào ngoài FORENSIC-SEED.
- Disagreement giữa lead và subagents: không có — mapper resolve độc lập trùng khớp giá trị blob/tree của lead.

## 7. Planner nên tự kiểm tra gì

1. `runs/C000/source-index.json` — đặc biệt durability/permitted-use của SRC-OLD-AUDIT-TREE (`evaluator_only`) và 4 thread (`unverified`).
2. `runs/C000/hypotheses.json` — priority P1/P2/P3 và invalidation criteria; xác nhận không hypothesis nào được gộp thành mega-treatment.
3. `runs/C000/events.jsonl` — event-hash chain (sha256 canonical, prev-link).
4. Diff commit: chỉ `runs/C000/**` + `STATE.json`.

## 8. Recommendation duy nhất

**Chạy C010 evaluator calibration ở scope nhỏ nhất:** 0 draft, chỉ dùng artifact đã bền vững (run-01..05 drafts + writer-notes tại `e29a984d…`) làm calibration anchors — gồm case từng được self/machine chấm cao nhưng user đánh giá thấp — để khóa rubric v1, judge prompt, defect taxonomy, comparator matching và benchmark blob `391febd8…` trước bất kỳ generation nào. Kèm 1 kiểm chứng định lượng trong C010: replay gate minimum-dimension trên obvious-defect/close-call fixtures, gold-direction accuracy ≥85%. **Không đề nghị chạy lại full multi-round loop**; C020 durability enforcement và mọi A/B generation phải chờ review C010 và authority tương ứng.

## 9. Hard stop xác nhận

Sau khi commit checkpoint này: dừng toàn bộ subagent (đã kết thúc tự nhiên, không còn process sống); KHÔNG tự chạy C010, KHÔNG sửa harness, KHÔNG viết P01. Worker dừng tại đây; quyền tiếp theo thuộc planner/reviewer.
