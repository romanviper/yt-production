# Modular Production Workflow

## 1. Mental model

Repo tách ba thứ vốn dễ bị trộn:

| Layer | Chức năng | Nơi thực thi |
|---|---|---|
| Hard boundaries | authority, write scope, state, approval, packet integrity, evidence provenance, hard cap | router, permissions, validators |
| Soft logic | opening form, fact order, local structure, rhythm, paragraph count, phrasing | Agent phán đoán từ material |
| Outcome evaluation | story motion, voice, causality, repetition, listening experience | review Agent rồi human gate |

Product Agent không sửa control plane. System Architect không trộn system change với product content trong cùng commit.

Human authority có một đường ngắn riêng. Khi người dùng trực tiếp feedback hoặc yêu cầu sửa một output cụ thể, Agent có thể sửa file đó rồi chạy một lệnh `human-amend-*`; không tạo task mới chỉ để hợp thức hóa quyết định của human.

**Safety cứng, workflow mềm.** Packet integrity, evidence ceiling, write scope và human approval không được bypass. Nhưng human không phải tự sửa nhiều state để yêu cầu chạy lại một operation: semantic rework sẽ reopen đúng lifecycle state rồi tạo task canonical mới.

## 2. Task packets và lifecycle

`scripts/task.py create` biên dịch đúng một operation thành:

- immutable `context.md`;
- `packet.json` có input hashes, context profile, instruction/input token metrics và evaluation gate;
- `work-order.json` có allowed writes;
- `operator-brief.json` cho handoff ngắn.

Hard-policy files và operator-interface không được nạp vào prompt sáng tạo. Creative packet chỉ dùng allowlist ngắn và bị chặn nếu evaluation-only policy lọt vào writer context.

Registry chỉ route operation, input, output, profile và budget. Tiêu chí semantic nằm đúng một lần trong operation instruction, Channel Constitution hoặc Outcome Evaluation; compiler không lặp lại chúng thành một acceptance prompt thứ hai.

`work-order.json.state` và packet validity là authority cho lifecycle của task. `tasks/ACTIVE.json` chỉ là **routing pointer** để Agent biết task nào đang được giao; pointer không tự làm một task hợp lệ hoặc vô hiệu. `--replace` phải cancel/supersede task cũ trước khi route task mới, thay vì chỉ ghi đè ACTIVE.

Các rule canonical cho task state, section-operation entry state, submit state và rework state nằm trong `scripts/lifecycle.py`. `context_packet.py`, `task.py` và human rework cùng dùng mapping này; không tự định nghĩa state machine riêng ở từng script.

Agent đọc đúng ACTIVE → work order → packet. Nó không quét repo.

Riêng POC `outline`, operator có thể chọn runtime DSH on-demand:

```bash
python scripts/task.py create products/<slug> outline --runtime dsh
python scripts/outline_runtime.py run products/<slug> <task-id>
```

DSH phải được cài riêng ở đúng version POC đã audit (`@deepseek-ai/dsh@0.1.0-rc.5`) và cung cấp executable `dsh`; repo không phụ thuộc npm package này để chạy control plane hoặc test. Trước model call, runner dump fully composed config và fail-closed nếu một guarded tool row không bị disable hoặc MCP broker không đúng interface. Runtime headless chạy trong thư mục tạm rỗng, tắt telemetry và chỉ nhìn thấy capability broker theo scope của packet. `runtime-trace.jsonl` giữ nguyên payload context/evidence đã trả cho model; `runtime-run.json` giữ version, composed config, seed/patch hash và kết quả run. Hai file là runtime-owned, không phải factual authority hay product artifact.

Không truyền `--runtime` thì task dùng packet precompile hiện tại. Nếu DSH lỗi hoặc bị loại bỏ, cancel/replace task và tạo lại `outline --runtime legacy`; không cần convert outline, story bible hay voice profile.

## 3. Research: claim và material đi song song

`research_plan` chia câu hỏi thành workstreams không trùng ownership. Mỗi `research_workstream` trả ba ledger cục bộ:

- `sources.json`: nguồn và locator;
- `claims.json`: điều có thể khẳng định và mức chắc chắn;
- `materials.json`: object/person/action/process/encounter/failure/consequence/sequence đủ chi tiết để lớp sau có thể dựng lại mà không bịa.

`materials.json` không phải kho anecdote. Mỗi material phải gắn local claim IDs, source refs có locator hẹp, representativeness và limitation. Workstream không có material đủ chắc được phép trả danh sách rỗng.

Deterministic consolidation remap/deduplicate source và claim, đồng thời remap material thành `material-ledger.json` mà không làm mất locator riêng của carrier. Research cũ chưa có material ledger được ghi thành `legacy_workstreams_without_materials`; đó là gap rõ ràng để rework có mục tiêu, không buộc research lại toàn bộ product.

`research_synthesis` trả hai artifact:

- `research-synthesis.md`: causal model và claim decisions;
- `story-material-map.json`: phase nào có material đủ để mang story movement, candidate nào phù hợp opening/reversal/ending, và phase nào vẫn chỉ có abstract claims.

Raw browsing context không đi vào outline hay writing.

Trước outline, router sinh `outline-evidence-pack.json` quyết định từ claim ledger + material ledger + story-material-map. Pack giữ cả claim ceiling lẫn material candidates đã được synthesis chọn; provenance đầy đủ vẫn nằm ngoài creative prompt trong ledgers gốc.

## 4. Whole-product architecture là lần review đầu tiên của video

Outline schema v4 thiết kế theo thứ tự:

1. central question và audience promise;
2. đúng ba act toàn phim: `opening`, `body`, `ending`;
3. số narrative movement cần cho causal arc;
4. material cụ thể có thể mang từng movement;
5. số `P##` cần cho context/review sau khi story movement đã đứng được.

Ba act là invariant. Movement count, section count và relative length là adaptive. Một movement có thể trải qua nhiều work unit; một work unit có thể chứa nhiều movement trong cùng act. Work unit không được băng qua act boundary vì assembly phải giữ ba phần rõ ràng.

Material-aware outline revision thêm vào mỗi section:

- `audience_experience`: preview đủ để human hình dung audience sẽ theo cái gì từ entry tới exit, nhưng không viết narration hay beat sheet;
- `material_ids`: `MAT-####` thực sự mang trải nghiệm đó;
- `transition`: vì sao trạng thái mới khiến phần kế tiếp cần xuất hiện.

`script_architecture.story_material_contract_version = 1` đánh dấu outline đã đi qua harness mới. Claim IDs vẫn là evidence ceiling; material IDs không thay thế claim support.

Mục tiêu review: trước khi approve outline, human phải có thể đọc liên tục P01 → P02 → ... và nhìn thấy phần lớn trải nghiệm video. Nếu một section logic nghe đúng nhưng không có material đủ để kể, hoặc boundary cắt một process khiến section trước chỉ còn câu hỏi còn section sau giữ toàn bộ hành động, outline chưa production-ready.

Section contract vẫn giữ narrative job, entry/exit state, evidence allowance, dependencies và target range. `audience_experience` mô tả câu chuyện nào xảy ra; writer sau này vẫn tự quyết cách kể bằng câu chữ.

Approve rồi materialize:

```bash
python scripts/approval.py approve-outline products/<slug>
python scripts/materialize_sections.py products/<slug>
```

## 5. Lean story design — transitional layer

`design_section` hiện vẫn tạo story-plan schema v3:

- `audience_shift`;
- `story_strategy` dạng free-form, không phải beat sheet;
- `core / optional / guardrail / exclude`;
- `word_budget.recommended` như estimate;
- optional design risks.

Không có compulsory payoff beat, numbered beats, claim-use explanation, opening move, ending move, paragraph count hoặc cadence.

Human approval tạo narration-pack schema v2. Pack chỉ giữ compact claims và source refs; full authority/notes/limitations/provenance vẫn ở evidence artifacts, không chiếm writer context.

Lớp này đang được giữ trong giai đoạn chuyển đổi để không phá lifecycle đang active. Sau khi material-aware outline được regression-test, có thể collapse chức năng evidence handoff vào materializer và bỏ `design_section` như một approval layer riêng.

## 6. Drafting

Writer nhận:

- Creative Boundaries;
- Channel Constitution;
- product story bible và voice profile;
- local brief;
- approved lean story plan;
- compact narration pack;
- approved dependency handoffs.

Nếu draft được mở lại bằng semantic rework, writer còn nhận one-shot `draft-rework-request.md`. File này chỉ truyền human intent cho lần draft đó và được router bỏ sau submit; nó không trở thành writer rule toàn cục.

Nó tự chọn local route. Target range không phải quota: submit không lỗi chỉ vì draft ngắn hơn estimate. Padding bị cấm; hard cap 3.000 từ/work unit vẫn được máy giữ.

## 7. Outcome evaluation

`review_section` là gate bắt buộc trước human section approval. Nó kiểm tra outcome và route lỗi về đúng layer:

- `prose_execution`;
- `local_design`;
- `product_architecture`;
- `evidence`.

Review phải có verdict `pass / changes_requested / blocked`, observable diagnosis và acceptance test. `approve-section` chỉ mở khi review hoàn chỉnh và verdict là `pass`.

## 8. Feedback routing và semantic rework

Đường chuyên biệt vẫn giữ để operator có thể route feedback chính xác:

- Wording/pacing/arrangement hỏng, plan vẫn đúng → `request-changes` rồi `revise_section`.
- Audience shift hoặc evidence selection hỏng → `request-story-plan-changes` rồi `design_section`.
- Section boundary hoặc whole-product story architecture hỏng → mở production cycle mới ở `outline`.
- Evidence/material thiếu, contradicted hoặc quá trừu tượng để dựng carrier → research escalation.

Nhưng khi human đơn giản muốn **làm lại một process**, không yêu cầu human tự nhớ current state. Dùng một command semantic:

```bash
python scripts/rework.py products/<slug> draft_section --section P01 \
  --request "Rewrite from the same approved story plan"

python scripts/rework.py products/<slug> design_section --section P04 \
  --request "Redesign this section from the approved evidence"

python scripts/rework.py products/<slug> outline \
  --request "Reopen whole-product architecture"
```

`rework.py` thực hiện theo intent:

1. cancel task đang được route và clear ACTIVE;
2. reopen đúng operation state từ `scripts/lifecycle.py`;
3. invalidate downstream product stages khi section đã được mở lại;
4. tạo task mới bằng **canonical `scripts/context_packet.py`**;
5. ghi audit trail vào `rework-requests.jsonl`.

Human không cần gọi `task.py state`, sửa `section.json` hay hand-author `packet.json/context.md`. Low-level `task.py state` vẫn tồn tại cho recovery/debugging, nhưng terminal task không được reopen; muốn chạy lại thì tạo task mới hoặc dùng semantic rework.

Không thêm một writer rule toàn cục cho một lỗi một lần. Chỉ pattern lặp mới trở thành eval; chỉ invariant thật sự mới vào constitution/hard boundary.

### Human-directed amendment

Sau khi human trực tiếp sửa file, hoặc Agent áp đúng feedback đã được human chỉ định:

```bash
python scripts/approval.py human-amend-outline products/<slug> \
  --request "Human correction" --path outline.json

python scripts/approval.py human-amend-section products/<slug> P04 \
  --request "Human prose correction" --path draft.md
```

Có thể lặp `--path`. Outline allowlist chỉ gồm `outline.json`, `story-bible.md`, `voice-profile.md`; section allowlist chỉ gồm `story-plan.json`, `draft.md`, `handoff.md`.

Lệnh accept thực hiện trong một bước: validate contract/hard cap, giữ evidence ceiling, ghi SHA-256 vào `human-amendments.jsonl`, hủy task active bị supersede và xóa con trỏ ACTIVE. Human-edited draft hợp lệ có thể chuyển thẳng sang `approved` mà không cần `review_section` hoặc `revise_section`. Nếu `outline.json` đổi sau khi sections đã tồn tại, sections được đánh dấu `human_sync_required`; nội dung cũ không bị xóa nhưng không còn được coi là current.

## 9. Production cycles

Đường semantic được ưu tiên:

```bash
python scripts/rework.py products/<slug> outline --request "Yêu cầu kiến trúc"
```

Nếu outline đang approved, command này mở production cycle mới rồi tạo outline task canonical. Expert path cũ vẫn tồn tại:

```bash
python scripts/approval.py start-new-cycle products/<slug> --request "Yêu cầu kiến trúc"
python scripts/task.py create products/<slug> outline --replace
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
