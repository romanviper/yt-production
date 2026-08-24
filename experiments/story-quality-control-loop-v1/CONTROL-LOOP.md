# Story Quality Control Loop v1

## Mục tiêu

Xây một vòng phản hồi có thể lặp để đưa script hiện tại tới mức kể chuyện ngang FoC, đồng thời giữ nguyên:

- hướng tư duy, mission, entry/exit state và transition đã được phê duyệt trong outline;
- truth ceiling và provenance;
- quyền tự quyết sáng tác của writer;
- ranh giới phê duyệt của người dùng.

FoC là benchmark về **hiệu quả kể chuyện**, không phải nguồn câu chữ, motif, nhân vật, cadence hay beat sequence cho writer.

## Sự thật forensic đã khóa

Không được gộp hai giai đoạn thử nghiệm:

1. `run-01` đến `run-05` là giai đoạn cũ, được lưu trên branch `experiment/p01-harness-audit-20260824`. Cùng một writer đã viết, sửa và diễn giải tiến bộ nên kết quả bị confound.
2. Chuỗi quan trọng hơn xảy ra sau đó: clean replay `6,6` -> bounded revision `7,3` -> clean replay mới `6,7` -> revision `6,9` -> senior-edited candidate `8,1`.

Chuỗi thứ hai chỉ còn summary ở commit `2cebbbd9f45ffa68bec453db1616cd740455825a`. Candidate `8,1`, prototype diff, rubric đầy đủ, evaluator output và replay artifacts đã mất. Vì thế:

- `8,1` có nhãn `historical_summary_only`;
- không được dùng làm baseline, champion hay bằng chứng đã ngang FoC;
- `run-05` chỉ là historical control, không phải resume point;
- mọi giả thuyết rút từ checkpoint phải được retest trên `main` bằng clean roles.

## Quyền hạn và vai trò

### Planner/reviewer

- Phát hành đúng một work order cho mỗi cycle.
- Khóa hypothesis, rubric, budget, read/write scope và stop conditions trước khi worker chạy.
- Đọc checkpoint, diff quan trọng và artifact gốc; phát hành cycle kế tiếp.
- Chỉ ghi `recommend_approve`, `recommend_rework`, `recommend_reject`, `recommend_stop` hoặc `inconclusive`.
- Không implement harness và không viết/sửa draft.

### Worker lead

- Là filesystem writer duy nhất trong cycle.
- Điều phối tối đa ba subagent cùng lúc.
- Truyền snapshot/đường dẫn được phép cho subagent; không bảo họ tự scan repo.
- Tổng hợp artifact, chạy validation, commit checkpoint trên `main`, rồi dừng.
- Không tự sửa work order, rubric hoặc hypothesis sau khi thấy output.

### Subagent

- Mặc định read-only; không ghi file, không commit, không route task.
- Nhận một workstream độc lập, có read set và output schema rõ ràng.
- Không tự duyệt kết quả của mình.

### Người dùng

- Là người duy nhất phê duyệt research plan, outline, story plan và section.
- Quyết định promotion/rework thực tế sau recommendation.

## Bất biến của toàn bộ loop

1. Bắt đầu từ current `main`; branch cũ chỉ là forensic evidence, không phải production lineage.
2. Một cycle chỉ kiểm tra **một causal hypothesis chính**.
3. Writer không được thấy FoC, rubric số, scorecard của đối thủ hoặc draft của writer khác.
4. Metric thuộc evaluator; không biến metric thành quota trong creative prompt.
5. Claim là truth boundary, không phải content checklist.
6. Detail mới phải đi qua bounded evidence access và giữ source/locator.
7. Không average qua hard failure: factuality, outline fidelity, boundary bleed và imitation đều là gate riêng.
8. Không có score nếu thiếu candidate hash, rubric hash, judge artifact và benchmark hash.
9. Harness/system change và product prose change luôn ở cycle/commit riêng.
10. Worker dừng sau mỗi checkpoint. Chỉ planner phát hành vòng tiếp theo.

## State machine

Các enum persisted dùng chữ thường:

```text
ready_for_worker
  -> running
  -> evaluating
  -> awaiting_planner_review
  -> recommend_rework | recommend_promote | inconclusive | stopped
  -> ready_for_worker (chỉ sau work order mới)
```

| Transition | Owner |
|---|---|
| `ready_for_worker -> running` | worker lead |
| `running -> evaluating` | worker lead, khi cycle có evaluation |
| `running/evaluating -> awaiting_planner_review` | worker lead |
| `ready_for_worker -> awaiting_planner_review` | worker lead, chỉ cycle forensic không có generation/evaluation như C000 |
| `awaiting_planner_review -> recommend_* / inconclusive / stopped` | planner/reviewer |
| recommendation -> `ready_for_worker` | planner/reviewer sau khi phát hành work order mới |

Worker đồng thời đặt `next_authority=planner_reviewer` khi bàn giao. Planner có quyền cập nhật `last_checkpoint_commit` và recommendation trong review commit riêng. Worker không được tự chuyển sang `recommend_promote`. Mọi thay đổi scope, budget, hypothesis hoặc rubric làm invalid cycle hiện tại và cần work order version mới.

## Roadmap theo checkpoint

### C000 — Lost-loop reconstruction

- Không sinh draft.
- Không sửa harness, product, system, scripts, tests hoặc router state.
- Tái dựng decision trail của chuỗi `6,6 -> 8,1` từ checkpoint và task history còn lại.
- Phân loại từng artifact: `durable`, `summary_only`, `missing` hoặc `unverified`.
- Trả về hypothesis registry và smallest retest matrix.

### C010 — Evaluator calibration

- Không sinh draft mới.
- Dùng artifact cũ còn bền vững như calibration anchors, gồm cả case từng được máy/self-review chấm cao nhưng người dùng đánh giá thấp.
- Kiểm tra label/order bias, duplicate consistency và việc aggregate che dimension yếu.
- Khóa rubric, judge prompt, benchmark blob và defect taxonomy trước generation.

### C020 — Observability/system task

- Chỉ bắt đầu sau review C010 và explicit user authority cho `system_architect`.
- Implement tối thiểu durability/logging cần để không thể mất candidate, scorecard hoặc diff lần nữa.
- Không đổi creative behavior trong cùng cycle.
- Full relevant tests và product validation phải được ghi riêng với baseline failures.

### C030 — Fresh P01 A/B

- Freeze cùng mission, truth ceiling, evidence interface, target length và model tier.
- Baseline và đúng một treatment; mỗi arm dùng clean writer không thấy arm kia.
- Một pair trước. Chỉ chạy replicate thứ hai nếu kết quả `inconclusive` và planner cho phép.
- FoC vẫn bị giấu khỏi writer.

### C040 — One diagnosed revision

- Chỉ candidate thắng development gate mới được một revision.
- Editor mới chỉ thấy candidate, evidence note và defect taxonomy của chính candidate; không thấy FoC excerpt hoặc quota số.
- Không retrieval/thêm fact nếu hypothesis là prose-only; không prose edit nếu hypothesis là evidence-only.

### C050 — Strict P01 gates

- Independent evidence audit.
- Independent outline + P01/P02 boundary audit.
- Blind FoC calibration bằng panel tách khỏi writer/editor.
- Kết quả tối đa là `P01-calibrated`; chưa đủ để promote reusable harness.

### C100 — Cross-section regression

- Kiểm tra ít nhất một section mechanism-heavy và một section abstraction-heavy ngoài P01.
- Dùng fresh writers và cùng budget policy.
- Báo median, p10, failure rate và tokens per passing script; không báo mỗi best sample.
- Với P01 + hai section, nhãn tối đa là `single-product provisional`.

### C150 — Decision-grade expansion

- Mở rộng locked matched set tới ít nhất 24 cases qua nhiều section/product, hoặc một sample size khác được power analysis và người dùng phê duyệt trước generation.
- Giữ judge panel, comparator, retry/selection policy và budget tier đã khóa.
- Trước ngưỡng này không dùng nhãn `reusable_harness_promoted` hoặc tuyên bố toàn hệ thống ngang FoC.

### C200 — Harness promotion

- Chỉ khi decision-grade threshold C150 và mọi hard gate cùng pass.
- System/harness commit riêng, trên `main`, có tests và rollback note.
- Không chứa product draft.

### C210 — Canonical product replay

- Dùng `scripts/rework.py` cho một operation hoặc `scripts/replay.py` cho đường nhiều operation.
- Viết đúng active packet/allowed write paths, submit canonical task rồi dừng ở human checkpoint.

## Cách dùng subagent theo wave

Tối đa ba subagent chạy song song; các wave phụ thuộc nhau chạy tuần tự.

```text
Wave A: forensic / evidence / methodology (read-only)
    -> lead khóa packet/hypothesis
Wave B: clean writers độc lập (exclusive outputs hoặc message-only)
    -> lead anonymize, không merge voice mặc định
Wave C: evidence auditor / outline-boundary auditor / blind narrative judge
    -> lead tổng hợp checkpoint
```

Không cho nhiều agent cùng sửa một file. Nếu cần lưu output subagent, lead chép nguyên result artifact vào path riêng có attribution và hash.

## Budget và stop rules

Nếu người dùng cung cấp token cap, worker phải copy nguyên số đó vào manifest. Nếu chưa có cap số, dùng operation cap:

- C000: 0 draft, tối đa 3 subagent, 1 synthesis pass.
- C010: 0 draft, tối đa 3 evaluator, chỉ artifact đã tồn tại.
- Development cycle: tối đa 2 fresh drafts và 1 revision của winner.
- Không chạy replicate, new treatment hoặc new section nếu chưa qua planner checkpoint.

Mốc an toàn khi có token telemetry:

- 70% budget: không mở candidate/retrieval mới.
- 85% budget: chỉ validation, durability và checkpoint.
- 100%: hard stop; không hy sinh log để cố hoàn tất prose.

Dừng ngay khi:

- HEAD, work-order hash hoặc frozen input hash đổi giữa cycle;
- packet stale/malformed hoặc cần evidence ngoài ceiling;
- subagent ghi filesystem hoặc có changed path ngoài allowlist;
- benchmark leak vào generator;
- judge disagreement vượt contract;
- hai cycle liên tiếp không cải thiện cùng defect;
- implementation yêu cầu protected path ngoài authority hiện tại;
- worker định tự approve, tự route cycle kế tiếp hoặc gộp system/content commit.

## Feedback trả về writer

Chỉ trả defect theo chức năng và evidence span thuộc candidate, ví dụ:

- `causal_bridge_missing`;
- `question_without_payoff`;
- `analysis_restates_inference`;
- `historical_world_too_thin`;
- `supported_human_work_missing`;
- `section_boundary_bleed`;
- `spoken_delivery_friction`.

Không trả FoC excerpt, beat order, signature motif, numeric quota hay hướng “viết giống” benchmark.

## Định nghĩa thành công

Ba nhãn không được đánh tráo:

- `diagnostic_improvement`: có tín hiệu trên một pair/case, chưa đáng promote.
- `section_calibrated`: section cụ thể pass mọi gate và blind comparison.
- `reusable_harness_promoted`: đạt decision-grade sample/power target đã khóa, cải thiện lặp lại qua nhiều section, cùng budget tier, không regression outline/evidence/imitation và được người dùng duyệt.

Mục tiêu tối thượng chỉ hoàn thành ở nhãn thứ ba; một best sample `8,1` không đủ.
