# Modular Production Workflow

## 1. Mental model

Repo tách ba thứ vốn dễ bị trộn:

| Layer | Chức năng | Nơi thực thi |
|---|---|---|
| Hard boundaries | authority, write scope, state, approval, packet integrity, evidence provenance, hard cap | router, permissions, validators |
| Soft logic | opening form, fact order, local structure, rhythm, paragraph count, phrasing | Agent phán đoán từ material |
| Outcome evaluation | story motion, voice, causality, repetition, listening experience | review Agent rồi human gate |

Product Agent không sửa control plane. System Architect không trộn system change với product content trong cùng commit.

## 2. Task packets

`scripts/task.py create` biên dịch đúng một operation thành:

- immutable `context.md`;
- `packet.json` có input hashes, context profile, instruction/input token metrics và evaluation gate;
- `work-order.json` có allowed writes;
- `operator-brief.json` cho handoff ngắn.

Hard-policy files và operator-interface không được nạp vào prompt sáng tạo. Creative packet chỉ dùng allowlist ngắn và bị chặn nếu evaluation-only policy lọt vào writer context.

Registry chỉ route operation, input, output, profile và budget. Tiêu chí semantic nằm đúng một lần trong operation instruction, Channel Constitution hoặc Outcome Evaluation; compiler không lặp lại chúng thành một acceptance prompt thứ hai.

Agent đọc đúng ACTIVE → work order → packet. Nó không quét repo.

Riêng POC `outline`, operator có thể chọn runtime DSH on-demand:

```bash
python scripts/task.py create products/<slug> outline --runtime dsh
python scripts/outline_runtime.py run products/<slug> <task-id>
```

DSH phải được cài riêng ở đúng version POC đã audit (`@deepseek-ai/dsh@0.1.0-rc.5`) và cung cấp executable `dsh`; repo không phụ thuộc npm package này để chạy control plane hoặc test. Trước model call, runner dump fully composed config và fail-closed nếu một guarded tool row không bị disable hoặc MCP broker không đúng interface. Runtime headless chạy trong thư mục tạm rỗng, tắt telemetry và chỉ nhìn thấy capability broker theo scope của packet. `runtime-trace.jsonl` giữ nguyên payload context/evidence đã trả cho model; `runtime-run.json` giữ version, composed config, seed/patch hash và kết quả run. Hai file là runtime-owned, không phải factual authority hay product artifact.

Không truyền `--runtime` thì task dùng packet precompile hiện tại. Nếu DSH lỗi hoặc bị loại bỏ, cancel/replace task và tạo lại `outline --runtime legacy`; không cần convert outline, story bible hay voice profile.

## 3. Research

`research_plan` chia câu hỏi thành workstreams không trùng ownership. Mỗi `research_workstream` trả source/claim ledgers có locator, limitation, contradiction và provenance. Deterministic consolidation remap/deduplicate trước `research_synthesis`.

Raw browsing context không đi vào outline hay writing.

Trước outline, router sinh `outline-evidence-pack.json` quyết định từ claim ledger. Pack chỉ giữ claim ID, statement, type, confidence, status, source IDs và contradiction register; provenance chi tiết vẫn nằm ngoài creative prompt trong ledgers gốc.

## 4. Whole-product architecture

Outline schema v4 thiết kế theo thứ tự:

1. central question và audience promise;
2. đúng ba act toàn phim: `opening`, `body`, `ending`;
3. số narrative movement cần cho causal arc;
4. số `P##` cần cho context/review.

Ba act là invariant. Movement count, section count và relative length là adaptive. Một movement có thể trải qua nhiều work unit; một work unit có thể chứa nhiều movement trong cùng act. Work unit không được băng qua act boundary vì assembly phải giữ ba phần rõ ràng.

Section contract mới chỉ cần narrative job, entry/exit state, evidence allowance, dependencies và target range. Question/payoff/beat/shape ở cấp section không phải schema bắt buộc.

Approve rồi materialize:

```bash
python scripts/approval.py approve-outline products/<slug>
python scripts/materialize_sections.py products/<slug>
```

## 5. Lean story design

`design_section` tạo story-plan schema v3:

- `audience_shift`;
- `story_strategy` dạng free-form, không phải beat sheet;
- `core / optional / guardrail / exclude`;
- `word_budget.recommended` như estimate;
- optional design risks.

Không có compulsory payoff beat, numbered beats, claim-use explanation, opening move, ending move, paragraph count hoặc cadence.

Human approval tạo narration-pack schema v2. Pack chỉ giữ compact claims và source refs; full authority/notes/limitations/provenance vẫn ở evidence artifacts, không chiếm writer context.

## 6. Drafting

Writer nhận:

- Creative Boundaries;
- Channel Constitution;
- product story bible và voice profile;
- local brief;
- approved lean story plan;
- compact narration pack;
- approved dependency handoffs.

Nó tự chọn local route. Target range không phải quota: submit không lỗi chỉ vì draft ngắn hơn estimate. Padding bị cấm; hard cap 3.000 từ/work unit vẫn được máy giữ.

## 7. Outcome evaluation

`review_section` là gate bắt buộc trước human section approval. Nó kiểm tra outcome và route lỗi về đúng layer:

- `prose_execution`;
- `local_design`;
- `product_architecture`;
- `evidence`.

Review phải có verdict `pass / changes_requested / blocked`, observable diagnosis và acceptance test. `approve-section` chỉ mở khi review hoàn chỉnh và verdict là `pass`.

## 8. Feedback routing

- Wording/pacing/arrangement hỏng, plan vẫn đúng → `request-changes` rồi `revise_section`.
- Audience shift hoặc evidence selection hỏng → `request-story-plan-changes` rồi `design_section`.
- Section boundary hoặc three-act arc hỏng → mở production cycle mới ở `outline`.
- Evidence thiếu/contradicted → research escalation.

Không thêm một writer rule toàn cục cho một lỗi một lần. Chỉ pattern lặp mới trở thành eval; chỉ invariant thật sự mới vào constitution/hard boundary.

## 9. Production cycles

```bash
python scripts/approval.py start-new-cycle products/<slug> --request "Yêu cầu kiến trúc"
python scripts/task.py state products/<slug> <active-task> cancelled
python scripts/task.py create products/<slug> outline
```

Cycle mới giữ research đã duyệt, pause sections cũ và buộc outline output dùng cycle ID mới. Sau khi approve outline, lệnh sau chuyển section workspaces cũ vào `03_sections/_history/<cycle>/` rồi materialize workspaces mới:

```bash
python scripts/materialize_sections.py products/<slug> --archive-previous-cycle
```

Archive là recoverable; Git history và task reports vẫn giữ audit trail.

## 10. Assembly

`assemble.py` chỉ ghép section đã human-approved. Với schema v4, delivery hiển thị ba act audience-facing; production IDs chỉ nằm trong comment/manifest, không biến thành chapter giả.

## Minimal handoff prompt

```text
Đọc AGENTS.md, rồi thực hiện task active của products/<slug>. Chỉ dùng compiled packet, không quét repo và không tự approve output.
```
