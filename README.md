# YT Production

## Owner-first MVP — đường hiện tại để lấy hai bản đọc đầu tiên

Trước khi tiếp tục benchmark/coordinator/diagnostic architecture, dùng đường tối thiểu này. `prepare` chỉ snapshot authority + Sol brief và **dừng chờ Owner duyệt budget**; chưa dispatch agent:

```bash
python scripts/learning.py prepare --run p01-owner-001 --request "Viết một đoạn P01 độc lập để tôi đọc và phản hồi" --code-ref <commit-or-config-ref>
python scripts/learning.py status --run p01-owner-001
```

Hướng dẫn đầy đủ: [docs/MVP.md](docs/MVP.md). Owner amendment và acceptance RC1–RC6: [docs/MVP-REQUEST-CHANGES-02.md](docs/MVP-REQUEST-CHANGES-02.md).

Flow MVP hiện tại là:

```text
Owner request
  → frozen P01 authority + Sol repo brief
  → Owner-approved time budget
  → Sol repo prepares one frozen Plan
  → two equal-common-content Writer packets
      ├─ Gemini 3.8 Flash → sample A
      └─ GPT-5.6 Sol     → sample B
  → timing/budget report
  → Owner comparison feedback
  → stop
```

Không có Planner agent riêng, Reviewer/Audit/time-auditor/coordinator trong đường này. Controller không tự gọi model host, không tự reroll/chọn Writer thắng, và không được bắt đầu vòng live cho tới khi Owner duyệt budget cụ thể. Production router bên dưới vẫn là một luồng riêng; các experiment/Phase 1–3 là lịch sử/tham khảo trừ khi Owner tái ủy quyền cụ thể.

Hệ điều hành biên tập cho phim lịch sử dài, được thiết kế để nhiều AI task cộng tác mà không mang toàn bộ repo và toàn bộ policy vào mỗi context window.

## Source of truth

`main` là nhánh làm việc duy nhất. Agent mới luôn checkout `main` ở HEAD hiện tại và không chọn commit hay branch lịch sử để bắt đầu. Chỉ tạo branch/PR khi người dùng yêu cầu riêng một vòng review hoặc isolation.

## Harness

Hệ thống dùng nguyên tắc **Hard boundaries, Soft logic**:

- **Hard boundaries:** authority, write scope, task state, approval, freshness, provenance và hard cap được code/validator giữ bên ngoài prompt.
- **Soft logic:** Agent sáng tạo chỉ nhận Channel Constitution ngắn, product blueprint, vai trò work unit, continuity và evidence ceiling; nó tự chọn route, nhịp và câu chữ.
- **Eval-only:** storytelling, voice, causal clarity và semantic repetition được đánh giá sau draft. Evaluator chấm outcome, không chấm việc đi đúng một route định trước.

Machine-readable profiles nằm ở `system/harness.json`. Phân loại và lý do thiết kế nằm ở [docs/HARNESS.md](docs/HARNESS.md).

Quy trình canonical để sản xuất section nằm ở [system/workflows/section-production-harness.md](system/workflows/section-production-harness.md), với quality gate tại [system/standards/section-quality-gate.md](system/standards/section-quality-gate.md). Agent không dùng branch lịch sử hay artifact thử nghiệm làm production input.

## Kiến trúc câu chuyện

Mọi script có ba act rõ ràng ở cấp toàn phim:

`opening → body → ending`

Số narrative movement và số production section không cố định. `P##` là work unit để giới hạn context/revision; nó không phải mini-chapter bắt buộc có hook–body–payoff riêng. Length range là estimate; chỉ production-unit hard cap mới bị máy cưỡng chế.

## Production flow

```text
research plan
  → isolated research workstreams
  → research synthesis
  → three-act product architecture + narrative movements
  → bounded production sections
  → lean story design + human approval
  → autonomous draft
  → outcome evaluation
  → human approval / targeted revision
  → handoff integration
  → deterministic assembly
```

Story design chỉ khóa audience shift, evidence roles (`core / optional / guardrail / exclude`) và length estimate. Approval sinh narration pack compact có provenance refs; raw research và full source metadata không đi vào writer packet.

## Lệnh thường dùng

```bash
python scripts/new_product.py ten-san-pham --title "Tên làm việc"
python scripts/task.py create products/ten-san-pham research_plan
python scripts/task.py create products/ten-san-pham outline --runtime dsh  # optional POC
python scripts/outline_runtime.py run products/ten-san-pham <task-id>     # requires dsh executable
python scripts/task.py create products/ten-san-pham design_section --section P04
python scripts/approval.py approve-story-plan products/ten-san-pham P04
python scripts/task.py create products/ten-san-pham draft_section --section P04
python scripts/task.py create products/ten-san-pham review_section --section P04
python scripts/approval.py approve-section products/ten-san-pham P04
python scripts/assemble.py products/ten-san-pham
```

Human có thể sửa hoặc chỉ đạo sửa trực tiếp output mà không mở task mới:

```bash
python scripts/approval.py human-amend-outline products/ten-san-pham --request "..." --path outline.json
python scripts/approval.py human-amend-section products/ten-san-pham P04 --request "..." --path draft.md
```

Đường này vẫn giữ allowlist, evidence ceiling, hard cap và provenance; nó chỉ bỏ AI task/design/review trung gian khi authority đến trực tiếp từ người dùng.

Mở một vòng sản xuất mới từ research đã duyệt:

```bash
python scripts/approval.py start-new-cycle products/ten-san-pham --request "Yêu cầu kiến trúc mới"
python scripts/task.py state products/ten-san-pham <old-active-task> cancelled
python scripts/task.py create products/ten-san-pham outline
```

Sau khi outline mới được duyệt, archive workspaces cũ rồi materialize cycle mới:

```bash
python scripts/materialize_sections.py products/ten-san-pham --archive-previous-cycle
```

Chi tiết vận hành: [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Pilot

`products/sumer-writing/` kể vòng đời chữ viết như một công nghệ–thiết chế của văn minh Sumer. *Fall of Civilizations* là benchmark chức năng, không phải mẫu câu, cadence, persona hay structure để sao chép.
