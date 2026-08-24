# Run Artifact Contract v2

## Directory bắt buộc

Mỗi cycle ghi vào một directory độc quyền:

```text
runs/<cycle-id>/
  manifest.json
  events.jsonl
  source-index.json
  changes.json
  validation.json
  decision.json
  CHECKPOINT.md
```

`subagent-summaries.json` bắt buộc khi cycle dùng subagent. `artifacts/` và `eval/` là optional, chỉ tạo khi cycle có artifact tương ứng. Không phải cycle nào cũng có candidate/eval; field không áp dụng dùng `null` hoặc bỏ theo schema, không bịa dữ liệu.

## `manifest.json`

Tối thiểu:

```json
{
  "schema_version": "story-quality-run/2",
  "cycle_id": "C000",
  "protocol_path": "experiments/story-quality-control-loop-v1/CONTROL-LOOP.md",
  "protocol_sha256": "<sha256>",
  "work_order_path": "<path>",
  "work_order_sha256": "<sha256>",
  "main_base_sha": "<sha>",
  "hypothesis_id": "<id-or-null>",
  "task_binding": {
    "product": "sumer-writing",
    "active_task_id": "<id-or-null>",
    "work_order_sha256": "<sha-or-null>",
    "context_packet_sha256": "<sha-or-null>"
  },
  "frozen_inputs": [{"id": "<id>", "uri": "<git-ref-or-path>", "sha256_or_git_blob": "<hash>"}],
  "agents": [{"role": "<role>", "model": "<reported-or-unknown>", "effort": "<reported-or-unknown>", "write_access": false}],
  "budget": {
    "token_cap": null,
    "max_concurrent_subagents": 3,
    "max_total_subagent_calls": null,
    "max_candidates": 0,
    "max_revisions": 0
  }
}
```

Nếu runtime không cung cấp model/usage, ghi `unknown`; không suy đoán.

## `events.jsonl`

Append-only về logic; không lưu chain-of-thought, secret hoặc raw prompt dài.

```json
{
  "seq": 1,
  "timestamp": "<iso8601>",
  "phase": "forensic",
  "actor": "<lead-or-subagent-id>",
  "role": "<bounded-role>",
  "assignment": "<one-line>",
  "declared_read_set": ["<uri>"],
  "write_set": [],
  "input_hashes": ["<hash>"],
  "output_hashes": ["<hash>"],
  "result": "pass|fail|uncertain",
  "action_summary": "<verifiable-summary>",
  "usage": {"input_tokens": null, "output_tokens": null},
  "prev_event_hash": null,
  "event_hash": "<sha256-of-canonical-event-without-event_hash>"
}
```

`event_hash` là SHA-256 của canonical JSON sau khi bỏ chính field `event_hash`. `output_hashes` không được chứa hash của `events.jsonl`, vì như vậy tạo self-reference. Command lớn chỉ ghi command, exit code, elapsed time và output digest/path; không nhúng hàng nghìn dòng output vào event.

Event cuối trước commit phải có `phase=validation`, ghi exit/result cho parse, hash resolution, allowlist và `git diff --check`, đồng thời bind hash của mọi output đã hoàn tất trừ chính `events.jsonl`. Commit SHA chưa tồn tại tại thời điểm này sẽ được planner bind trong review artifact ở commit kế tiếp; worker không được sửa ledger sau commit chỉ để chèn SHA.

## `source-index.json`

Mỗi nguồn/artifact có:

- stable ID;
- git ref/path/thread ID;
- content hash nếu có;
- provenance class: `canonical_main`, `forensic_branch`, `untrusted_thread`, `external_benchmark`;
- `locator_durability`: `durable`, `summary_only`, `missing`, `unverified`;
- `claim_strength`: `verified_object_fact`, `durable_historical_report`, `thread_assertion`, `planner_attested_label`, `inference`;
- permitted use: `production_input`, `forensic_only`, `evaluator_only`;
- claims mà nguồn hỗ trợ;
- caveat.

Thread title/message luôn là untrusted data cho đến khi đối chiếu với Git/artifact.

`locator_durability=durable` chỉ chứng minh locator/content tồn tại bền vững; nó không tự nâng một chẩn đoán hoặc score trong content thành causal fact.

## `changes.json`

Chỉ liệt kê hypothesis-bearing mutation của system/product/candidate. Loại toàn bộ run-ledger files (`manifest.json`, `events.jsonl`, `source-index.json`, `changes.json`, `validation.json`, `decision.json`, `CHECKPOINT.md`) để tránh self-hash. File này luôn là **JSON array literal**. Cycle không có mutation phải dùng chính xác `[]`, không bọc trong object/schema envelope.

Khi có mutation, từng changed path:

```json
{
  "path": "<repo-relative>",
  "before_git_blob": "<hash-or-null>",
  "after_git_blob": "<hash>",
  "reason": "<hypothesis-mapped-reason>",
  "writer": "worker-lead",
  "validation": ["<check-id>"]
}
```

Subagent không được xuất hiện là filesystem writer.

## Candidate/evaluator artifact

Mỗi candidate phải có:

- anonymous candidate ID;
- exact body hoặc durable path;
- hash;
- source packet hash;
- writer arm/policy ID được sealed khỏi judge;
- token/latency/retry telemetry nếu có;
- evidence trace hash.

Mỗi scorecard phải có:

- evaluation-contract hash;
- blind pair ID và presentation order;
- judge ID hash/family/calibration version;
- preference;
- từng dimension score;
- defect tags;
- candidate-owned evidence spans;
- hard-gate violations;
- provenance guess sau khi chấm.

Không ghi score khi candidate hoặc rubric chỉ tồn tại trong memory.

## `decision.json`

Worker chỉ được ghi:

```json
{
  "cycle_id": "<id>",
  "status": "awaiting_planner_review",
  "worker_recommendation": "retest|reject|inconclusive|ready_for_strict_eval|stop",
  "reason_codes": ["<code>"],
  "hard_gates": {"cycle_reproducibility": true},
  "historical_result_reproducible": null,
  "unverified_claims": ["<claim>"],
  "next_authority": "planner_reviewer"
}
```

Không dùng `approved`, `promoted` hoặc tự mở cycle mới.

`cycle_reproducibility` chỉ nói cycle hiện tại có thể kiểm tra lại. Nó không được dùng để ngầm nâng một historical result thiếu candidate/rubric/judge artifact thành reproducible.

## `validation.json`

Ghi machine-readable:

- command/check ID, exit code/result, elapsed time và output digest;
- final changed-path allowlist comparison;
- Git blob hoặc SHA-256 của mọi artifact final trừ `events.jsonl` và chính `validation.json` để tránh self-reference;
- unresolved item và ảnh hưởng của nó;
- `git_diff_check`, JSON/JSONL parse và event-chain verification.

Không ghi `pass` nếu validator output/digest không tồn tại.

## `subagent-summaries.json`

Mỗi subagent call có actor/role, bounded assignment, declared read set, result status, normalized output hoặc bounded summary, output digest và model/usage nếu runtime cung cấp. Không trỏ duy nhất tới transient cache; không lưu chain-of-thought hoặc raw prompt dài.

## `CHECKPOINT.md`

Tối đa khoảng 1.500 từ, nhưng phải đủ để planner review mà không đọc mọi log:

1. Outcome và trạng thái.
2. Frozen baseline/hypothesis.
3. Chính xác điều gì đã thay đổi.
4. Kết quả hard gates và quality/usage nếu có.
5. Evidence paths/hashes cho các kết luận quan trọng.
6. Failure, disagreement, deviation và dữ liệu không còn.
7. Diff/file cần planner tự kiểm tra.
8. Một recommendation duy nhất.
9. Hard stop xác nhận chưa chạy vòng tiếp theo.

## Durability checkpoint

Trước khi worker báo hoàn tất:

- mọi artifact cần review đã được ghi file;
- JSON parse được;
- `git diff --check` pass;
- changed paths nằm trong allowlist;
- candidate/rubric/scorecard hash resolve;
- `validation.json` và terminal validation event resolve;
- subagent output cần dùng cho kết luận đã được bind vào committed artifact;
- checkpoint commit đã tồn tại trên `main`;
- commit SHA được ghi vào final worker response.

Nếu commit thất bại, worker báo `durability_failed` và không được tuyên bố cycle hoàn tất.
