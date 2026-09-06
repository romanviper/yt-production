# Owner-first MVP work log

Format: `observed problem → acceptance ID → change → verification evidence`.

## Request changes 02 — implemented RC1–RC6

Owner amendment tại `6bc35ff610c0604a3a519538ee58272c5a9b70dc` thay giả định Planner riêng/một Writer bằng một Sol repo session chuẩn bị Plan + hai Writer riêng, đồng thời thêm budget/timing/Owner-approved extension accounting.

Implementation không gọi live model host và không tạo production prose. Vòng live vẫn bị chặn cho tới khi Owner đưa một budget cụ thể và phê duyệt nó.

### RC1 — một Sol Plan, hai Writer riêng, cùng common content

Observed: controller tại `fff42d7` còn `plan-001` + `writer-001`.

Change:
- bỏ workspace Planner riêng khỏi MVP;
- `sol-repo-001` nhận frozen brief và freeze một Plan;
- tạo `writer-gemini-001` và `writer-sol-001` trong workspace riêng;
- hai packet có cùng `common` payload và `common_content_sha256`, session/model metadata nằm ngoài phần common;
- không thêm reviewer/time-auditor/coordinator agent.

Evidence: `test_rc1_one_sol_plan_two_isolated_writers_same_common_hash`.

### RC2 — đủ hai mẫu mới tới Owner comparison gate

Observed: flow cũ chuyển sang Owner ngay sau draft đầu tiên.

Change:
- sample A bind `writer_gemini`, sample B bind `writer_sol`;
- nhận theo A→B hay B→A đều được;
- draft đầu tiên không kết thúc vòng và không được truyền sang Writer còn lại;
- Writer FAILED/TIMEOUT giữ evidence/time nhưng không tạo cặp hoàn tất;
- feedback bind SHA của cả hai mẫu;
- selection là `A/B/TIE/UNSELECTED`; primary Writer chỉ được ghi khi Owner chỉ định;
- `model_generalization` luôn `NOT_PERFORMED` trong round record.

Evidence: `test_rc2_both_arrival_orders_failure_and_owner_selection_binding`.

### RC3 — timing tách work / elapsed / wait / UNKNOWN

Observed: controller cũ chỉ có timestamp handoff/optional host log, chưa có duration accounting.

Change:
- `control/work-intervals.jsonl` ghi actor/session/task/attempt/start/end/duration/source/status/reason/evidence;
- `OPERATOR_OBSERVED_SESSION_WINDOW` cần đủ start/end và không được gọi là inference time;
- không suy runtime từ `agent_created_at`/receive timestamp;
- missing timing là `UNKNOWN`, không phải 0;
- cùng actor không được có interval cùng kind chồng lấn;
- failure/retry vẫn tính vào work;
- Owner/queue wait tách khỏi work budget;
- writer-pair elapsed tính từ min start tới max end, nên hai Writer 120s song song = 240s work nhưng 120s pair elapsed.

Synthetic evidence trong RC3:
- Sol 10s + Gemini 120s + Sol Writer 120s song song → total work 250s;
- writer pair elapsed 120s;
- Owner wait 600s giữ riêng;
- sequential failure/retry vẫn cộng thời gian;
- unknown interval làm total remaining thành UNKNOWN và block bước mới.

Evidence: `test_rc3_time_accounting_parallel_sequential_wait_retry_and_unknown`.

### RC4 — Owner-approved budget là precondition

Observed: flow cũ không có budget record hay gate trước agent work.

Change:
- `prepare` kết thúc tại `AWAITING_OWNER_BUDGET_APPROVAL`;
- `control/budget.json` là initial budget proposal write-once, có ID/unit/scope/code ref/attempts/cap/actor allocations;
- proposal không phải approval;
- chỉ Owner decision record `APPROVED` mới mở `READY_FOR_SOL_PLAN`;
- budget overrun/UNKNOWN giữ artifact, block bước mới và chuyển lại `AWAITING_OWNER_BUDGET_APPROVAL`;
- Writer output vượt budget được giữ ở workspace dưới `PENDING_BUDGET_REVIEW`, chưa publish sang Owner sample để che việc vượt budget.

Evidence: `test_rc4_budget_required_overrun_blocks_and_preserves_pending_output`.

### RC5 — extension không thể tự phê duyệt hoặc reset lịch sử

Observed: chưa có extension lifecycle.

Change:
- extension request ghi initial cap, approved extensions, used, remaining, actual overrun, requested seconds, actor/scope/reason/evidence;
- Owner decision giữ verbatim text + source ref;
- sai request/actor/scope bị reject;
- rejection/silence không resume;
- approval chỉ cộng đúng số giây đã duyệt, không reset used history;
- extension không cấp thêm content attempt;
- nếu extension vừa đủ clear overrun, pending Writer output mới được publish hash-identical sang Owner sample.

Manual decision record được ghi rõ là provenance do operator nhập, không phải authentication system.

Evidence: `test_rc5_extension_approval_exact_scope_no_reset_or_extra_attempt`.

### RC6 — nhìn thấy chi phí và sửa Windows path

Observed:
- work order yêu cầu tách architecture-repair cost khỏi per-round execution;
- Windows review tại `fff42d7` có M1 fail do `.endswith("agents/plan/.../")` phụ thuộc `/`.

Change:
- `record_cost_item(...)` tách `ESTIMATE/OBSERVED` và `ROUND_EXECUTION/ARCHITECTURE_REPAIR`;
- observed repair gắn commit/evidence; estimate gắn expected runtime impact/confidence;
- `status` xuất budget table theo actor/task với allocated/used/overrun/UNKNOWN/waiting;
- path assertions dùng `Path(...).parts`, không bỏ boundary assertion.

Evidence: `test_rc6_cost_report_separates_estimate_observed_repair_round_and_paths`.

## Original M1–M6 retained under the amendment

- **M1**: `status` có một waiting person/role + artifact/next action; initial gate giờ là Owner budget approval.
- **M2**: authority/brief/Plan/Writer packets/drafts/Owner samples/feedback vẫn hash-bound và write-once; wrong session/tamper/authority expansion fail closed.
- **M3**: `WorkspaceBroker` vẫn dùng resolved-path boundary cho input/output/scratch và chặn traversal/symlink/cross-role access; không gọi nó là OS sandbox.
- **M4**: TEST_ONLY path giờ là `prepare → Owner budget → Sol Plan → two Writer samples → Owner gate`; không giả live model execution.
- **M5**: Owner feedback vẫn hard-stop; không tự review/reroll/diagnose/cấu hình default Writer.
- **M6**: system/docs/tests only; product prose không bị sửa. Full PR CI là closing evidence.

## Verification evidence

Focused local synthetic harness after RC implementation:

```text
13/13 Owner-first MVP tests PASS
```

Đây là controller/test timing, không phải runtime model.

PR #14 workflow tại head `36e3d242aaf1b9c067223a9dc3df76caa49027f2`:

```text
Validate production system — SUCCESS
run 34038923698
```

Workflow success đóng full-test/governance/product-validation evidence cho code+tests trước documentation-sync commits. Documentation-only commits tiếp tục được kiểm bằng cùng PR workflow trước khi merge.

## Important limitations

- Chưa có live Gemini/GPT-5.6 invocation trong implementation evidence.
- Chưa có budget live do Owner phê duyệt; vì vậy chưa được gọi vòng live là READY TO RUN.
- Controller hiện không sở hữu external host process nên không tuyên bố hard cancel/timeout; nó enforce budget ở dispatch/next-step boundary và giữ observed overrun.
- Manual timing windows có thể gồm waiting trong session và không phải active inference time.
- Manual Owner approval record không chống được operator tampering ngoài trust boundary của repo.

## Deferred by scope

Không implement:

- scheduler mới chỉ để chạy parallel;
- reviewer/audit/time-auditor agent;
- Round Coordinator/event bus/trace graph;
- dashboard;
- FoC benchmark/quality scorer;
- model winner auto-selection/default configuration;
- autonomous self-improvement;
- live host adapter chỉ để lấy benchmark thời gian.

Reintroduce chỉ khi Owner giao work item/budget riêng hoặc execution evidence cho thấy blocker cụ thể.
