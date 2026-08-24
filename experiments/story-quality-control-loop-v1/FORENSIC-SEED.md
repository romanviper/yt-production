# Forensic Seed — planner-reviewed

Worker C000 phải **verify và chuẩn hóa**, không cần tự khám phá lại từ đầu.

## Đã xác nhận bằng Git

- Canonical source of truth tại thời điểm lập packet: `main` ở `95ca1f9703733153f3b32476af3ed8de94ccdb46`; worker phải ghi current SHA mới khi bắt đầu.
- Audit cũ `run-01..05` bền vững tới `e29a984dfbda80cc52afa66af0a42a34ba136669`.
- Pause checkpoint bền vững: `2cebbbd9f45ffa68bec453db1616cd740455825a`.
- Checkpoint tự supersede kết luận cũ rằng harness v2/run-05 đã đủ.
- Candidate `8,1`, post-run-05 replay artifacts, prototype diff và evaluator outputs không có trong tree của checkpoint.
- `origin/validation/p01-harness-20260824` quan sát ở `7b0328aca7142a6e83f0caa65a0b5df2270a9963`; branch này chỉ giữ một writer-outcome prototype nhỏ và không phải resume lineage.
- FoC P01-equivalent benchmark trên `main` có Git blob `391febd843f0d99a8ba3730ae447b4e2eefb9061`. C000 chỉ dùng metadata/hash, không đọc text.

## Chuỗi post-run-05 chỉ còn checkpoint assertion

Checkpoint ghi:

- clean replay: `6,6/10`;
- bounded revision: `7,3/10`;
- later clean replay after evidence work: `6,7/10`;
- revision: `6,9/10` dù internal gate false-positive pass;
- senior-edited candidate: `8,1/10`.

Breakdown còn lại của candidate `8,1`:

- causal chain `8,6`;
- question/payoff `8,7`;
- density `8,5`;
- continuity `9,0`;
- human immediacy `6,7`.

Không biết evaluator identity/model, full rubric, weighting hoặc exact comparator snapshot. Năm score dimension được lưu không tự tái tạo composite `8,1`; vì thế composite là non-reproducible.

## Prototype direction chỉ còn summary

- Bounded, route-neutral retrieval cho material detail với evidence trace.
- Neutral `details` contract; reject story-routing fields cho record mới nhưng đọc legacy record.
- Clean writer tách independent reviewer; tối đa một diagnosed revision.
- FoC nằm ngoài writer pipeline, chỉ dùng external calibration.
- Scored production gate theo minimum dimension, không pass bằng aggregate.
- Separate supported task orientation khỏi human/work orientation.
- Independent evidence audit và P01/P02 boundary audit chưa chạy xong.

Các điểm trên là hypothesis seed, không phải implementation spec đã được chứng minh.

## Cost/test assertion còn lại

- Clean first-pass packet khoảng `1.900` token.
- Direct writer instruction `878/1.500` token ceiling.
- Revision packet khoảng `5,9–6,6k`, cũ khoảng `13,3k`.
- Evidence lookup `10 -> 7` sau neutral material ledger.
- Regression được báo `81/82`; failure còn lại là whole-product cleanliness với `42` stale errors.

Không còn raw usage/test output, nên tất cả mang nhãn `checkpoint_assertion` cho tới khi retest.

## Historical controls, không phải resume baseline

- `run-01..05`: chứng minh outcome wording, evidence resolution và prose edit có tín hiệu, nhưng bị confound bởi same-writer self-review.
- `agent/ox-alpha-p01-alt`: chứng minh metric trong writer prompt gây Goodhart/stiffness; self/machine score từng lệch mạnh với user verdict; multi-writer merge có thể làm mất voice consistency.

## Planner diagnosis cần giữ

1. Không score nếu thiếu candidate/rubric/judge/benchmark hash.
2. Không cho writer viết–sửa–chấm chính mình.
3. Evidence, structure và prose là biến khác nhau; không đổi cùng cycle.
4. Minimum critical dimension và hard gates quan trọng hơn composite.
5. `human immediacy` phải tách raw FoC affordance khỏi `supported human/work orientation`; không bịa named anchor.
6. P01/P02 boundary là gate độc lập.
7. Internal/external discrepancy phải tạo `inconclusive + diagnosis`, không tự mở thêm revision.
8. Metrics chỉ ở evaluator; writer nhận outcome/defect functional, không quota.

## C000 chỉ còn phải làm

- Verify exact refs/task-history evidence.
- Chuyển seed thành source index và timeline có provenance class.
- Ghi rõ trường nào vẫn missing/unverified.
- Tách các hypothesis thành smallest clean tests.
- Chứng minh worker có thể tạo checkpoint đầy đủ, hash được và commit bền vững trước khi tiêu usage cho draft mới.
