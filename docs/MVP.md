# Owner-first MVP v3 — dynamic Writer pool

Đường MVP hiện tại tối giản theo nguyên tắc:

> **Freeze the work, not the worker.**

Chỉ `sol_repo` là actor được đăng ký trước và bị time-budget gate vì nó có quyền vận hành/sửa repo. Writer là participant động: Owner có thể khởi chạy Gemini, GPT-5.6 Sol, GPT-6, Claude hoặc model khác mà không sửa controller trước. Writer timing chỉ là telemetry; không có per-Writer time budget hay extension gate.

## Flow

```text
Owner request
  → snapshot P01 authority + Sol repo brief
  → Owner approves Sol repo budget
  → Sol repo prepares/freeze-binds one Plan
  → freeze one common writer-assignment.json
  → Owner launches any Writer(s)
      ├─ Gemini
      ├─ GPT-5.6 Sol
      ├─ GPT-6
      └─ ...
  → each Writer returns draft.md + execution-report.json
  → repo freezes dynamic submissions
  → Owner closes submission pool
  → Owner reads/compares frozen set and records feedback
  → STOP
```

Không có Planner riêng, Reviewer/Audit/time-auditor/coordinator trong MVP này. Controller không tự gọi model host, không tự review/reroll, không tự chọn Writer thắng và không biến một preference thành model-level conclusion.

## 1. Prepare và budget Sol repo

```bash
python scripts/learning.py prepare \
  --run p01-owner-001 \
  --request "Viết một đoạn P01 độc lập để tôi đọc và phản hồi" \
  --code-ref <commit-or-config-ref>

python scripts/learning.py budget-propose \
  --run p01-owner-001 \
  --budget-id B-P01-001 \
  --sol-seconds 1200 \
  --scope "P01 repo/Plan preparation" \
  --code-ref <commit-or-config-ref>

python scripts/learning.py budget-decision \
  --run p01-owner-001 \
  --request-id B-P01-001:initial \
  --decision APPROVED \
  --owner-text "<quyết định nguyên văn>" \
  --source-ref "<nguồn quyết định>"
```

Budget chỉ áp dụng cho `sol_repo`. Writer không có allocation, không mượn giây, không request extension và không bị reject vì viết lâu.

## 2. Freeze Plan và assignment chung

Sau approval, Sol repo trả một Plan ngắn:

```json
{
  "section": "P01",
  "telling_scope": "...",
  "source_refs": ["overlay:P01", "HS-P01-0001"],
  "stop_condition": "..."
}
```

Freeze:

```bash
python scripts/learning.py freeze-plan \
  --run p01-owner-001 \
  --session sol-repo-001 \
  --file /path/to/plan.json \
  --reason "..." \
  --uncertainty "..." \
  --duration-seconds 90 \
  --timestamp-source OPERATOR_OBSERVED_SESSION_WINDOW
```

Kết quả là `control/writer-assignment.json`, hash-bound với Owner request, frozen Plan và authority. Không có `writer_gemini`/`writer_sol` registry, model list hay sample A/B được định nghĩa trước.

## 3. Giao assignment cho bất kỳ Writer nào

Có thể đưa trực tiếp `control/writer-assignment.json`, hoặc export bundle portable:

```bash
python scripts/export_writer_assignment.py \
  --run p01-owner-001 \
  --out /path/to/writer-bundle
```

Bundle chứa:

```text
assignment.json
assignment-manifest.json
execution-report-template.json
START-HERE.md
```

Không có actor/model-specific packet.

## 4. Writer tự khai provenance sau khi viết

Writer trả:

```text
draft.md
execution-report.json
```

Metadata tối thiểu:

```json
{
  "schema_version": "DYNAMIC_WRITER_SUBMISSION_1",
  "submission_id": "p01-r01-gpt6-001",
  "provider": "OpenAI",
  "actual_model": "GPT-6",
  "actual_config": null,
  "provider_session_id": "...",
  "assignment_binding": "PREBOUND",
  "assignment_sha256": "...",
  "inputs_used": [
    {"ref": "control/writer-assignment.json", "sha256": "..."}
  ],
  "attempt": 1,
  "status": "COMPLETED",
  "timing": {
    "source": "WRITER_SELF_REPORTED_DURATION",
    "duration_seconds": 240
  },
  "draft_sha256": "...",
  "issues_encountered": [],
  "uncertainty": "..."
}
```

`actual_model` phải phản ánh điều Writer/host thực sự biết; nếu không biết thì dùng `UNKNOWN`. Không giả nhãn model.

Timing là telemetry. Có thể là:

```json
{"source": "UNKNOWN", "duration_seconds": null}
```

và submission vẫn có thể hợp lệ. Không ghi raw/private chain-of-thought.

## 5. PREBOUND vs NOT_PREBOUND

Nếu Writer thực sự nhận frozen assignment của round:

```text
assignment_binding = PREBOUND
```

và `assignment_sha256` phải match.

Nếu Writer được Owner chỉ đạo trực tiếp hoặc viết trước khi có assignment:

```text
assignment_binding = NOT_PREBOUND
```

Repo vẫn có thể nhận artifact như readable submission nếu provenance đầy đủ, nhưng đánh dấu:

```text
controlled_comparison_eligible = false
```

Không được dùng nó để tuyên bố controlled same-input comparison.

## 6. Nhận submission động

```bash
python scripts/writer_submission.py accept \
  --run p01-owner-001 \
  --report /path/to/execution-report.json \
  --draft /path/to/draft.md
```

Writer không cần xuất hiện trong code trước đó. `submission_id` là write-once; không dùng cùng ID để reroll.

Repo copy byte-identical sang:

```text
submissions/<submission-id>/draft.md
submissions/<submission-id>/execution-report.json
owner/submissions/<submission-id>.md
```

Có thể nhận bất kỳ số lượng Writer nào trước khi Owner đóng pool.

## 7. Writer timing không còn là budget gate

Các rule đã bỏ:

```text
writer allocation
writer overrun
writer extension request
AWAITING_OWNER_BUDGET_APPROVAL vì Writer viết quá lâu
transfer unused Writer budget
```

Timing vẫn được giữ để quan sát/so sánh chi phí, nhưng không quyết định acceptance.

Sol repo vẫn có budget gate và extension approval vì repo/architecture work có thể phình scope.

## 8. Owner đóng pool và feedback

Khi đủ mẫu:

```bash
python scripts/learning.py close-submissions --run p01-owner-001
```

Từ đó không nhận Writer mới trong run. State:

```text
AWAITING_OWNER_FEEDBACK
```

Feedback:

```bash
python scripts/learning.py feedback \
  --run p01-owner-001 \
  --text "<feedback nguyên văn>" \
  --selection p01-r01-gpt6-001 \
  --primary-writer p01-r01-gpt6-001
```

`selection` là `submission_id`, `TIE`, hoặc `UNSELECTED`.

Sau feedback:

```text
OWNER_FEEDBACK_RECORDED
```

và MVP dừng. Không auto-rerun, không set default model, không FoC diagnosis.

## 9. GPT-6 owner-directed draft hiện có

Draft ở `codex/p01-owner-directed-draft` được giữ như evidence lịch sử. Notes của chính Writer cho biết nó không có frozen packet và được viết theo Owner direction. Theo v3, nó được mô tả trung thực là:

```text
assignment_binding = NOT_PREBOUND
writer_budget = NOT_APPLICABLE
timing = UNKNOWN
```

Nó có thể được Owner đọc như một candidate, nhưng không được retroactively gọi là PREBOUND controlled submission.

## Hard stops

- Không Sol repo work trước matching Owner budget approval.
- Sol repo hết/UNKNOWN budget → dừng và xin Owner.
- Writer submission ID overwrite/reroll → reject.
- PREBOUND assignment hash mismatch → reject.
- Sau `close-submissions` → không nhận Writer mới.
- Sau Owner feedback → STOP.
