# Writer self-report handoff — Owner-first MVP

Trong live round, Owner tự khởi chạy hai Writer. Repo/controller không tự suy đoán hoặc nhập hộ metadata thực thi của Writer.

Sau khi `freeze-plan` đã tạo hai Writer packet, controller chạy:

```bash
python scripts/writer_submission.py prepare --run <run-id>
```

Mỗi Writer được giao đúng hai input trong workspace/session của mình:

- `input/packet.json`
- `input/self-report-contract.json`

Writer trả đúng một content attempt cùng self-report:

- `draft.md` nếu `status=COMPLETED`
- `execution-report.json`

Controller nhận bằng:

```bash
python scripts/writer_submission.py accept \
  --run <run-id> \
  --report <writer-execution-report.json> \
  --draft <writer-draft.md>
```

Với `FAILED` hoặc `TIMEOUT`, không truyền `--draft`.

## Những gì Writer tự khai

`execution-report.json` phải bind đúng packet/common-content hash và tự khai:

- actor + logical `session_id` được packet giao;
- actual model/config mà Writer/host quan sát được;
- attempt + status (`COMPLETED`, `FAILED`, `TIMEOUT`);
- `work_summary`, `issues_encountered`, `uncertainty` ở mức operational/editorial declaration;
- timing tự quan sát (`WRITER_SELF_REPORTED_SESSION_WINDOW` hoặc `WRITER_SELF_REPORTED_DURATION`);
- `draft_sha256` nếu hoàn thành;
- `budget_extension` nếu thời lượng khai báo vượt phần budget còn lại.

Ví dụ tối thiểu:

```json
{
  "schema_version": "WRITER_SELF_REPORT_1",
  "actor": "writer_gemini",
  "session_id": "writer-gemini-001",
  "provider_session_id": "host-session-if-visible",
  "packet_sha256": "...",
  "common_content_sha256": "...",
  "actual_model": "Gemini 3.8 Flash",
  "actual_config": "...",
  "attempt": 1,
  "status": "COMPLETED",
  "work_summary": "Produced one draft from the frozen packet.",
  "issues_encountered": [],
  "uncertainty": "Owner judges literary quality.",
  "timing": {
    "timestamp_source": "WRITER_SELF_REPORTED_DURATION",
    "start_utc": null,
    "end_utc": null,
    "duration_seconds": 412
  },
  "draft_sha256": "...",
  "budget_extension": null
}
```

Nếu Writer vượt budget, `budget_extension` là bắt buộc:

```json
{
  "requested_seconds": 90,
  "reason": "Lý do thực tế khiến phiên vượt budget.",
  "remaining_work_if_approved": "Phần việc/khoản overrun cần Owner phê duyệt."
}
```

Controller giữ draft/report làm evidence nhưng **không publish sample cho Owner và không bắt đầu work mới**. Nó chuyển request do Writer khai thành `AWAITING_OWNER_BUDGET_APPROVAL`. Chỉ Owner có quyền phê duyệt gia hạn.

## Authority của self-report

Self-report là **Writer-declared provenance**, không phải host-attested active inference time. Repo không được đổi `UNKNOWN` thành 0, không được sửa lý do overrun cho đẹp hơn, và không được gắn nhãn model khác với model Writer khai.

Không ghi raw/private chain-of-thought. Các field như `chain_of_thought`, `private_reasoning`, `internal_monologue` bị từ chối; chỉ ghi decision/process metadata có thể audit và các vấn đề quan sát được.
