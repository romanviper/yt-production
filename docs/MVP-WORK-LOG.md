# Owner-first MVP work log

Format: `observed problem → acceptance ID → change → verification evidence`.

## Owner amendment pending — RC1–RC6

Review tại `fff42d7`: controller hiện có một Writer, timestamp bàn giao và optional
host log; chưa có phép tính duration, budget, gia hạn hoặc lựa chọn giữa hai Writer.
Owner yêu cầu bổ sung đúng các phần này trong
[MVP-REQUEST-CHANGES-02.md](MVP-REQUEST-CHANGES-02.md). Đây là yêu cầu mới, chưa implement.

Chạy lại 7 test MVP trên Windows: 6 pass, M1 fail do so sánh `/` với đường dẫn Windows
tại `tests/test_owner_first_mvp.py:87`; unittest báo 0.487s. Không có agent live được gọi.
Các số đo này không thay thế dữ liệu thời gian thực thi agent hoặc phê duyệt budget.

## Implementation log

- Existing README/AGENTS routed new work through production/architecture-learning paths before a first fresh Owner reading → **M1** → added `docs/MVP.md`, `scripts/learning.py status`, and a top-level README/AGENTS entrypoint → `test_m1_status_has_single_waiting_role_and_artifact` passes locally.
- Manual role transfer had no small immutable identity check independent of the larger coordinator work → **M2** → freeze Planner/Writer packets and accepted outputs by SHA-256, require declared session IDs, reject changed packets, wrong sessions, authority expansion and repeated submissions → `test_m2_tampered_packet_wrong_session_and_overwrite_are_rejected`, `test_plan_cannot_expand_authority`, and `test_feedback_is_bound_to_unchanged_draft` pass locally.
- A workspace directory alone does not enforce role access boundaries → **M3** → added `WorkspaceBroker` with resolved-path checks for relative traversal, cross-role access, writes to input, and symlink escapes; broker logs allowed/denied operations and explicitly does not claim OS sandboxing → `test_m3_workspace_broker_blocks_cross_role_and_resolved_symlink_escape` passes locally.
- Repo had no bounded owner-first path that could be exercised without a fake live-agent provider → **M4** → implemented `prepare → freeze-plan → freeze-draft → owner/draft.md` using manual packet transfer or an optional real host log; TEST_ONLY fixture never claims live-agent execution → `test_m4_test_only_fixture_reaches_owner_reading_copy` passes locally.
- Previous learning architecture could continue into reviewer/diagnostic work before Owner decided what mattered → **M5** → draft handoff ends at `AWAITING_OWNER_FEEDBACK`; verbatim feedback is hash-bound to the frozen draft and ends at `OWNER_FEEDBACK_RECORDED`; no automatic next Plan/draft/reviewer path exists → `test_m5_feedback_stops_without_new_candidate` passes locally.
- System implementation must not modify product content or lower existing gates to make tests pass → **M6** → implementation touches only system/docs/tests plus `.gitignore`; full repository CI remains the required closing evidence → **pending PR CI at initial implementation commit**.

## Measured local checks

Environment: local Python unittest harness containing the new MVP controller/tests only. These numbers are observations, not performance gates.

| Check | unittest-reported test time |
| --- | ---: |
| M2 tamper/session/overwrite | 0.010 s |
| M3 workspace boundary | 0.004 s |
| M4 TEST_ONLY handoff to Owner copy | 0.007 s |
| M5 Owner feedback hard stop | 0.008 s |

Full local 7-test MVP suite: 7/7 passed. Repository-wide CI evidence must come from the PR workflow; this local harness does not substitute for M6.

## Deferred

Not implemented because the first-reading MVP does not require them:

- multi-layer Round Coordinator;
- new live host/sub-agent adapter;
- spawn certification;
- mandatory Product/Audit agents;
- decision-before-output advanced gates;
- blind A/B comparison;
- FoC diagnosis and benchmark calibration;
- root-cause graph;
- invariant/agent registry;
- dashboard or autonomous self-improvement framework.

Reintroduce only when an execution error or Owner feedback identifies a concrete need for the next Owner-selected change.
