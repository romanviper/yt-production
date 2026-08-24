# CHECKPOINT — C010 evaluator preflight

## 1. Outcome và trạng thái

C010 kết thúc với nhãn **`needs_user_gold`** theo đúng nhánh Wave B của work order: bộ fixture calibration thật được xây và freeze, nhưng chỉ đạt **9/12 case tối thiểu** (thiếu 2 close_call, thiếu 1 factual/imitation trap) nên cycle **dừng trước khi gọi bất kỳ judge nào** (judges dispatched = 0). Không có generation, không đụng product/system/harness. Trạng thái: `awaiting_planner_review`, `next_authority=planner_reviewer`. Base: `15182f62c63c0b77a478002991d6347661f4dc9b`; commit C000 `1356872…` xác nhận là ancestor tại preflight.

## 2. Frozen baseline / hypothesis

Hypothesis planner khóa: *bộ evaluator mù, độc lập, frozen có thể phát hiện hard defect đã biết, giữ nguyên hướng thứ bậc do người dùng phê duyệt, lộ tradeoff giữa các dimension và kháng label/order effect đủ tốt cho đúng một T1 diagnostic sau này*. Đầu vào freeze: `CALIBRATION-SEED-C010.json` (`d4ba3b36…22932`), `JUDGE-PROMPT-C010.md` (`22195d9d…98da`), benchmark blob `391febd8…b9061`. Không threshold nào được tune; không có FoC parity claim.

## 3. Chính xác điều đã thay đổi

Chỉ run-ledger dưới `runs/C010/`: manifest, events (6 events, hash-chain), source-index, changes = `[]` literal, validation.json, subagent-summaries + transcript-hashes, anchor-registry, gold-key (CONFIDENTIAL — không bao giờ nằm trong bundle), fixture-build, leakage-audit, evaluation-lock, decision, CHECKPOINT này, cùng 10 file fixture trong `bundles/`. `STATE.json` chỉ chuyển state như quy định. Zero mutation hypothesis-bearing → `changes.json = []`.

## 4. Hard gates / quality / usage

| Gate | Kết quả |
|---|---|
| G0 reproducibility cycle | pass — mọi input/output hash-bound; transforms tái lập được |
| Fixture integrity (auditor độc lập) | pass — 10 files, 0 hash mismatch, 0 blob resolution fail |
| Leakage audit (lead + auditor độc lập) | clean — 0 FoC excerpt ≥12 token; 0 identifier/marker/prompt-string |
| Pass rule T1 | **không áp dụng được** — dừng trước judges; mọi metric ngưỡng ghi `not_estimable` trong evaluation-lock |
| Usage telemetry | `unknown` trung thực (runtime không cấp) |

## 5. Evidence paths/hashes chính

- Fixtures + thuật toán + hash từng file: `runs/C010/fixture-build.json` (C1 pair `4e67ca8c…/70e47297…`, D1 `fc3013bc…`, D2 `da538d56…`, D3 `b7dad60b…`, O1 `7764180a…`, O2 `b8f20ec2…`, O3 `c10450ac…`, F1 `bb4d800c…`, F2 `a5f486db…`).
- Gold key: `runs/C010/gold-key.json` (chỉ C1 có human gold: preference B, direction-only).
- Anchor registry: `runs/C010/anchor-registry.json` (4 anchors resolved exact-SHA; A1 verdict bind `7dcc1033…` vs `3424c985…` qua thread 6a8482d8/turn 75be696a — planner-attested).
- Audit: `leakage-audit.json`, `subagent-transcript-hashes.json` (6 transcripts SHA-256), `evaluation-lock.json`.
- Subagent summaries: `subagent-summaries.json` (6 calls, tất cả read-only).

## 6. Failure, disagreement, deviation, dữ liệu không còn

1. **A2 hỏng premise:** "cỡ bàn tay" **có nguồn** trong pack (blob `fbde42c4…`, entry CRR-02/SRC-0023); REVIEW-C-r2 chỉ flag nó ngoài locator khai báo và dành quyền keep/remove cho user → không thể dùng làm unsupported-detail trap nếu không có phân xử của user.
2. **Phương pháp n-gram bị bác bỏ cho A3:** variant-B (tiếng Việt) vs FoC (tiếng Anh) có **0** common run từ k=14 xuống k=6 — checker lexical sẽ false-clear một case nhiễm FoC về cấu trúc (cùng hook mechanism + beat order: 06/1625→chiến tranh→sư tử→công chúa Damascus→horizon→dời trại một dặm→vài đêm→đi phế tích→hồi ký gạch đóng dấu). Thay bằng presence-check chi tiết đặt tên (sư tử / sighting 18 tháng Sáu / công chúa Damascus: có trong variant-B, vắng trong pack/render/addendum trừ rule R7 cấm) + G3 structural clause.
3. **Thread evidence vẫn planner-attested-only** trong runtime worker (4/4 exact-ID read thất bại); không có turn bytes gốc.
4. Disagreement giữa lead và auditors: không có (integrity pass, leakage clean, methodology xác nhận stop là bắt buộc). Deviation so với work order: không có.
5. Không còn: numeric human anchors, durable blind human-vs-FoC verdict — hai khoảng trống seed đã khai báo từ đầu.

## 7. Planner cần tự kiểm tra

1. `fixture-build.json` + `bundles/` — tính deterministic của 9 transform; F1/F2/C1 phải byte-for-byte với blob nguồn.
2. `gold-key.json` — chỉ C1 mang gold; A4 phải ở ngoài mọi denominator.
3. `evaluation-lock.json` mục `unqualified_capabilities` — đây là phần giới hạn quan trọng nhất cho work order kế tiếp.
4. `decision.json.user_gold_request` — danh sách 3 yêu cầu dữ liệu user.

## 8. Recommendation duy nhất

Planner phát hành **work order bổ sung nhỏ (C010-b) thu thập user-gold**: (a) user chấm hướng G2 (`521ded0d`) vs H2 (`4e75f451`); (b) user chấm hướng thêm một cặp durable (khuyến nghị vs FoC-matched reference `391febd8`); (c) user phân xử keep/remove flag "cỡ bàn tay" trên variant-C-r2 (`1d803121`). Sau khi đủ 12 case (≥3/category), chạy lại Wave B-audit rồi Wave C/D theo đúng lock hiện có — không cần đổi prompt/rubric. **Không mở generation; không coi evaluator là calibrated.**

## 9. Hard stop xác nhận

Sau commit: mọi subagent đã kết thúc tự nhiên (0 process sống); KHÔNG chạy C020/C030, KHÔNG sửa harness, KHÔNG sinh P01, KHÔNG route task product active. Worker dừng tại planner review.
