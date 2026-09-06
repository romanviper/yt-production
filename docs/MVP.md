# Owner-first MVP

Request changes 02 đã được implement ở controller/test layer. Đường MVP hiện tại dùng **một phiên Sol vận hành repo kiêm chuẩn bị Plan** và **hai Writer riêng** (Gemini 3.8 Flash và GPT-5.6 Sol), với budget thời gian phải được Owner phê duyệt trước khi bắt đầu agent work.

Đây vẫn là đường tối thiểu để đưa hai bản đọc mới tới Owner trước khi quay lại benchmark/coordinator/diagnostic architecture. Implementation không tự gọi model host và không phải bằng chứng một vòng live đã chạy.

## Mục tiêu

```text
Owner giao mục tiêu
  → snapshot P01 authority + Sol repo brief
  → Owner chốt budget
  → Sol repo chuẩn bị một Plan
  → freeze Plan
  → tạo hai Writer packet có cùng common-content hash
      ├─ Writer Gemini 3.8 Flash → sample A
      └─ Writer GPT-5.6 Sol     → sample B
  → freeze đủ hai mẫu + báo cáo thời gian/budget
  → Owner đọc, chọn A/B/TIE/UNSELECTED và phản hồi
  → STOP
```

Không có Planner agent riêng, reviewer agent, time-auditor agent hay coordinator trong MVP này. Sol repo không viết thay draft và không tự chọn Writer thắng.

## 1. Prepare: chưa được dispatch agent

Từ repo root:

```bash
python scripts/learning.py prepare \
  --run p01-owner-001 \
  --request "Viết một đoạn P01 độc lập để tôi đọc và phản hồi" \
  --code-ref <commit-or-config-ref>

python scripts/learning.py status --run p01-owner-001
```

Sau `prepare`, state là:

```text
AWAITING_OWNER_BUDGET_APPROVAL
```

Artifact đầu tiên là `agents/sol_repo/sol-repo-001/input/brief.json`, nhưng **chưa được dispatch Sol repo** trước khi budget được Owner duyệt.

Runtime artifacts nằm dưới `runs/<id>/` và không phải production content.

## 2. Chốt budget trước agent work

Budget dùng đơn vị chính:

```text
CUMULATIVE_AGENT_SESSION_SECONDS
```

Ví dụ chỉ để minh họa lệnh; các con số thực phải do Owner duyệt cho vòng live:

```bash
python scripts/learning.py budget-propose \
  --run p01-owner-001 \
  --budget-id B-P01-001 \
  --cap-seconds 900 \
  --sol-seconds 300 \
  --gemini-seconds 300 \
  --writer-sol-seconds 300 \
  --scope "P01 two-writer round" \
  --code-ref <commit-or-config-ref>
```

Controller không coi proposal là approval. Quyết định Owner được ghi nguyên văn:

```bash
python scripts/learning.py budget-decision \
  --run p01-owner-001 \
  --request-id B-P01-001:initial \
  --decision APPROVED \
  --owner-text "<quyết định nguyên văn của Owner>" \
  --source-ref "<tham chiếu tới nguồn quyết định>"
```

Manual approval record là provenance do operator ghi, **không phải hệ thống xác thực**. Writer không có quyền ghi budget/approval.

## 3. Sol repo chuẩn bị Plan

Sau initial budget approval, state là `READY_FOR_SOL_PLAN`. Sol repo dùng đúng brief đã freeze và trả một Plan ngắn:

```json
{
  "section": "P01",
  "telling_scope": "Đoạn này kể phần nào",
  "source_refs": ["overlay:P01", "HS-P01-0001"],
  "stop_condition": "Dừng ở đâu"
}
```

Freeze Plan kèm timing quan sát được. Với chuyển thủ công, dùng `OPERATOR_OBSERVED_SESSION_WINDOW`; đó là cửa sổ phiên quan sát được, không phải active inference time:

```bash
python scripts/learning.py freeze-plan \
  --run p01-owner-001 \
  --session sol-repo-001 \
  --file /path/to/plan.json \
  --reason "Lý do ngắn" \
  --uncertainty "Điểm còn chưa chắc" \
  --start-utc 2026-09-06T10:00:00+00:00 \
  --end-utc 2026-09-06T10:02:00+00:00 \
  --timestamp-source OPERATOR_OBSERVED_SESSION_WINDOW
```

Nếu timing không đo được, bỏ timestamp/duration; controller ghi `UNKNOWN`, không suy runtime từ `agent_created_at` hay thời điểm operator nhận file.

Nếu work đã vượt budget, Plan vẫn được giữ làm evidence nhưng controller dừng ở `AWAITING_OWNER_BUDGET_APPROVAL` trước bước mới.

## 4. Hai Writer từ cùng một nhiệm vụ

Khi Plan hợp lệ và budget còn đủ, controller tạo hai packet:

```text
agents/writer_gemini/writer-gemini-001/input/packet.json
agents/writer_sol/writer-sol-001/input/packet.json
```

Hai packet có:

- cùng `common` payload;
- cùng `common_content_sha256`;
- cùng Owner request, Plan, authority, scope và output requirement;
- session/model metadata riêng.

Writer Gemini và Writer Sol phải là hai phiên riêng. Writer Sol không được tái dùng context của Sol repo. Mỗi Writer chỉ thấy packet của mình và workspace riêng; không thấy draft của Writer còn lại.

Mỗi Writer có đúng một content attempt. Một lỗi kỹ thuật có thể được ghi và retry cùng nhiệm vụ, nhưng attempt lỗi và thời gian của nó không bị xóa; không reroll để tìm bản đẹp hơn.

Freeze sample A:

```bash
python scripts/learning.py freeze-draft \
  --run p01-owner-001 \
  --session writer-gemini-001 \
  --file /path/to/gemini.md \
  --reason "Realized the frozen Plan" \
  --uncertainty "..." \
  --actual-model "Gemini 3.8 Flash" \
  --actual-config "<host config>" \
  --start-utc <...> --end-utc <...> \
  --timestamp-source OPERATOR_OBSERVED_SESSION_WINDOW
```

Freeze sample B tương tự với session `writer-sol-001` và model host thực tế. Nếu host trả model khác model Owner yêu cầu, controller lưu cả requested/actual identity; không giả nhãn.

Draft đầu tiên không kết thúc vòng. Chỉ khi đủ hai output hợp lệ và budget accounting không bị block, controller copy byte-identical sang:

```text
owner/sample-A.md
owner/sample-B.md
```

Một Writer fail/timeout không được thay bằng output cũ, Writer thứ ba hay draft do Sol repo viết. Cặp khi đó vẫn incomplete.

## 5. Timing: work, elapsed và wait là ba số khác nhau

`control/work-intervals.jsonl` giữ các interval quan sát được. `status` tổng hợp riêng:

- **total work seconds**: tổng work của Sol repo + hai Writer, kể cả lỗi/retry;
- **elapsed seconds**: thời gian lịch của vòng/checkpoint;
- **waiting seconds**: Owner reading/approval, transfer hoặc queue khi quan sát được;
- **UNKNOWN**: timing không đủ evidence.

Hai Writer chạy song song 120 giây mỗi phiên tạo 240 giây work nhưng khoảng elapsed của cặp là 120 giây. Owner chờ 10 phút không cộng thêm 600 giây vào work budget.

Controller từ chối interval work chồng lấn của cùng actor để tránh tính cha/con hai lần. Timestamp đảo chiều hoặc duration không khớp wall timestamps cũng bị reject.

## 6. Hết budget và gia hạn

Khi budget hết, bị vượt hoặc timing UNKNOWN làm accounting không đáng tin, controller giữ artifact/log và dừng phát sinh bước mới tại:

```text
AWAITING_OWNER_BUDGET_APPROVAL
```

Extension request phải gắn đúng actor/scope và hiển thị trần ban đầu, extension đã duyệt, work đã dùng, remaining, actual overrun, số giây xin thêm, reason và evidence.

```bash
python scripts/learning.py request-extension \
  --run p01-owner-001 \
  --actor writer_gemini \
  --seconds 30 \
  --scope write_draft \
  --reason "<lý do>" \
  --evidence "<artifact/log ref>"
```

Resume chỉ xảy ra sau Owner approval gắn đúng request/actor/scope/số giây. Rejection hoặc im lặng không phải approval. Extension cộng vào lịch sử; không reset used time, không tạo run khác để né budget và không cấp thêm content attempt.

Controller hiện không tự gọi/cancel external model host, nên với phiên ngoài controller nó chỉ có thể chặn **bước kế tiếp** và ghi overrun/pending output; không tuyên bố hard-timeout nếu host không cung cấp cơ chế đó.

## 7. Owner đọc hai mẫu và STOP

Khi đủ sample A/B, state là `AWAITING_OWNER_FEEDBACK`.

```bash
python scripts/learning.py feedback \
  --run p01-owner-001 \
  --text "<feedback nguyên văn>" \
  --selection A \
  --primary-writer writer_gemini
```

`--selection` nhận `A`, `B`, `TIE`, `UNSELECTED`. `--primary-writer` chỉ ghi khi Owner thật sự quyết định writer chính.

Feedback bind với SHA-256 của cả hai mẫu. Một lần chọn A/B không được controller suy rộng thành “model A tốt hơn” hay cấu hình Writer mặc định. State kết thúc:

```text
OWNER_FEEDBACK_RECORDED
```

Từ đây MVP dừng. Không tự review, reroll, FoC diagnosis, root-cause attribution hay vòng mới.

## 8. Status và chi phí kiến trúc

```bash
python scripts/learning.py status --run p01-owner-001
```

Status trả về state, waiting person/role, artifact, Writer identity/status, common-content hash, timing/budget và bảng theo actor/task gồm allocation, used, overrun, UNKNOWN và waiting-for.

`record_cost_item(...)` trong controller tách:

- `ROUND_EXECUTION` khỏi `ARCHITECTURE_REPAIR`;
- `ESTIMATE` khỏi `OBSERVED`;
- observed repair phải gắn commit + evidence.

Synthetic tests chỉ chứng minh phép tính/controller behavior, không phải benchmark runtime model thật.

## Authority và immutability

`prepare` snapshot và kiểm tra liên kết giữa:

- `products/sumer-writing/02_outline/section-overlays/P01.json`;
- `products/sumer-writing/03_sections/P01/historical-substrate.json`.

Controller từ chối packet/Plan/draft bị sửa sau freeze, sai session, Plan mở rộng authority, overwrite output, hoặc Owner feedback trên mẫu bị tamper.

## Workspace boundary

`scripts.learning.WorkspaceBroker` giới hạn mỗi role vào `input/output/scratch` của workspace riêng bằng resolved path, gồm `..`, absolute path và symlink escape; access được audit vào `control/access-events.jsonl`.

Đây **không phải OS sandbox**. Chỉ được nói read/write isolation được enforce khi host cấp broker này làm filesystem surface duy nhất và không đồng thời cấp shell/network/general-filesystem access.

## TEST_ONLY và trạng thái live

Tests dùng fake/declared timing để chứng minh M1–M6 + RC1–RC6 mà không sleep dài hoặc gọi model thật. Chúng không chứng minh Gemini/GPT-5.6 đã chạy.

Implementation có thể merge sau CI phù hợp ngay cả khi chưa có budget live cụ thể. **Vòng live không được bắt đầu** cho tới khi Owner đưa và phê duyệt budget thực tế.

Production router hiện có vẫn là luồng riêng. Phase 1–3/coordinator experiments là lịch sử/tham khảo cho tới khi Owner tái ủy quyền một phần cụ thể.
