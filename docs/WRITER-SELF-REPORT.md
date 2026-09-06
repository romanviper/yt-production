# Dynamic Writer submission — Owner-first MVP v3

Writer không cần được đăng ký trước và không có per-Writer time budget.

Nếu có frozen round assignment, Writer nhận `assignment.json`. Nếu Owner launch Writer trực tiếp mà không có assignment, Writer vẫn có thể nộp artifact nhưng phải khai `assignment_binding=NOT_PREBOUND`.

Writer trả:

- `draft.md` nếu `status=COMPLETED`;
- `execution-report.json`.

Repo/controller chỉ validate/freeze metadata đã khai; không tự điền model, timing hay input provenance thay Writer.

## Metadata bắt buộc

- unique `submission_id`;
- provider/model/config/session khi biết;
- `assignment_binding`: `PREBOUND` hoặc `NOT_PREBOUND`;
- `assignment_sha256` nếu PREBOUND;
- `inputs_used[]` với `ref` + `sha256`;
- attempt = 1;
- status;
- timing telemetry (`duration_seconds` có thể null);
- `draft_sha256` nếu completed;
- issues/uncertainty nếu có.

Writer timing không có budget gate. Một Writer viết 2 phút hay 20 phút đều không tự tạo extension request. Timing chỉ phục vụ observability.

Không ghi private chain-of-thought/raw scratch reasoning.

## Controlled comparison

`PREBOUND` + matching assignment hash:

```text
controlled_comparison_eligible = true
```

`NOT_PREBOUND`:

```text
controlled_comparison_eligible = false
```

NOT_PREBOUND không có nghĩa prose vô dụng; chỉ có nghĩa controller không được nói nó giải chính xác cùng frozen assignment.
