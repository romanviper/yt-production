# Dynamic Writer submission — Owner-first MVP v3

Writer không cần được đăng ký trước và không có per-Writer time budget.

## Hai cách Writer có thể bắt đầu

### 1. PREBOUND

Nếu Owner/Operator đưa frozen `assignment.json` trước khi viết, Writer dùng assignment đó làm task/evidence boundary và khai:

```text
assignment_binding = PREBOUND
assignment_sha256 = <hash của assignment đã nhận>
```

### 2. NOT_PREBOUND — direct Owner instruction

Nếu Owner trực tiếp yêu cầu một Writer viết một phần bounded như `P01` nhưng **không đưa `assignment.json`**, Writer **không được dừng chỉ vì thiếu assignment**. Direct Owner instruction là đủ authority để thực hiện đúng một content attempt.

Writer có thể tự resolve **context tối thiểu, canonical, hiện hành** cần cho phần được giao; ví dụ với P01 có thể đọc current P01 overlay và historical substrate. Writer không được:

- tự tạo/fabricate một frozen Plan;
- hồi sinh task production cũ/cancelled chỉ để hợp thức hóa assignment;
- đọc draft của Writer khác hoặc Owner comparison feedback;
- mở rộng sang historical experiment branch hay architecture context không cần cho phần viết;
- tự review/reroll sau khi đã tạo draft.

Sau khi viết, khai:

```text
assignment_binding = NOT_PREBOUND
assignment_sha256 = null
```

và ghi **mọi input thực tế đã dùng** vào `inputs_used[]`. Nếu direct Owner instruction là một input quan trọng, có thể ghi một stable ref cho instruction đó và SHA-256 của exact instruction text khi Writer có thể tính được.

`NOT_PREBOUND` không có nghĩa draft invalid. Nó chỉ có nghĩa draft không được dùng để tuyên bố một controlled same-assignment comparison.

## Output

Writer trả:

- `draft.md` nếu `status=COMPLETED`;
- `execution-report.json`.

Repo/controller chỉ validate/freeze metadata đã khai; không tự điền model, timing hay input provenance thay Writer.

## Metadata bắt buộc

- unique `submission_id`;
- provider/model/config/session khi biết;
- `assignment_binding`: `PREBOUND` hoặc `NOT_PREBOUND`;
- `assignment_sha256` nếu PREBOUND; `null` nếu NOT_PREBOUND;
- `inputs_used[]` với `ref` + `sha256` cho những input thật sự đã dùng để viết;
- `attempt = 1`;
- status;
- timing telemetry (`duration_seconds` có thể null);
- `draft_sha256` nếu completed;
- issues/uncertainty nếu có.

Writer timing không có budget gate. Một Writer viết 2 phút hay 20 phút đều không tự tạo extension request. Timing chỉ phục vụ observability.

Không ghi private chain-of-thought/raw scratch reasoning.

## Mẫu report cho direct Owner Writer

```json
{
  "schema_version": "DYNAMIC_WRITER_SUBMISSION_1",
  "submission_id": "p01-r01-writer-001",
  "provider": "OpenAI",
  "actual_model": "GPT-5.6 Sol",
  "actual_config": null,
  "provider_session_id": "UNKNOWN",
  "assignment_binding": "NOT_PREBOUND",
  "assignment_sha256": null,
  "inputs_used": [
    {
      "ref": "products/sumer-writing/02_outline/section-overlays/P01.json",
      "sha256": "<sha256 actually observed>"
    },
    {
      "ref": "products/sumer-writing/03_sections/P01/historical-substrate.json",
      "sha256": "<sha256 actually observed>"
    }
  ],
  "attempt": 1,
  "status": "COMPLETED",
  "timing": {
    "source": "WRITER_SELF_REPORTED_DURATION",
    "duration_seconds": 180
  },
  "draft_sha256": "<sha256 of draft.md>",
  "issues_encountered": [],
  "uncertainty": ""
}
```

Nếu model/session/timing không thực sự biết, dùng `UNKNOWN`/`null`; không bịa dữ liệu để làm report trông đầy đủ.

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
