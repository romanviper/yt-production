# Modular Production Workflow

## 1. Mental model

Repo tách ba lớp:

| Layer | Chức năng | Nơi thực thi |
|---|---|---|
| Hard boundaries | authority, write scope, state, approval, packet integrity, evidence provenance, cycle integrity, hard cap | router, permissions, validators |
| Soft logic | ordering, paragraph count, rhythm, phrasing | Agent phán đoán từ material |
| Outcome evaluation | story motion, reconstruction, voice, causality, listening experience | review Agent rồi human gate |

Product Agent không sửa control plane. System Architect không trộn system change với product content trong cùng commit.

Human không phải tự sửa nhiều state để yêu cầu chạy lại một operation. Semantic rework reopen đúng lifecycle state, invalidate downstream khi cần và tạo task canonical mới.

## 2. Pipeline hiện hành

Đường material-aware:

`research_workstream`
→ `research_synthesis`
→ `outline`
→ deterministic `materialize_sections`
→ `draft_section`
→ `review_section`

`story-plan` không còn là approval gate hoặc writer interface của material-aware cycle.

Artifact story-plan cũ vẫn có thể tồn tại trong cycle/history legacy. `design_section` chỉ còn compatibility route cho artifact cũ và không được semantic rework sử dụng để cứu lỗi của material-aware product.

## 3. Claim, material và interpretation

Ba lớp không được trộn:

- **Claim:** ta được phép khẳng định điều gì. Nó giữ evidence ceiling, qualification, counterevidence và causal boundary.
- **Material:** narrator có thể thuật lại vật thể, người, hành động, process, trạng thái, failure hoặc consequence nào. Đây là nguồn chính tạo narrative experience.
- **Interpretation:** material đó có ý nghĩa gì đối với movement hoặc thesis.

Nguyên tắc: `what evidence supports` ≠ `what narration can recount` ≠ `what it means`.

`materials.json` giữ `sequence`, locator hẹp, claim IDs, representativeness, limitations và khi research mới/rework cho phép thì thêm `narratable_reconstruction` + `narratability`. Research cũ có sequence đủ cụ thể không bị ép research lại chỉ để đổi schema.

Researcher giữ raw reconstructable reality; không thêm weather, cảm xúc, dialogue, motive, sensory detail hay action không được nguồn support.

## 4. Research synthesis

`research_synthesis` tạo causal model và `story-material-map.json`.

Với synthesis mới, map đánh giá không chỉ material có support logic hay không mà còn listener có thể hình dung/thuật lại điều gì qua audio:

- A: strong recountable material;
- B: illustrative material, vẫn cần synthesis đáng kể;
- C: material gap.

Critical phase loại C phải surface gap trước khi outline khóa architecture. Không yêu cầu mọi phase phải là scene hoặc event chain.

## 5. Outline là lần review đầu tiên của video

Outline quyết định **câu chuyện nào diễn ra**; writer quyết định **kể nó bằng prose như thế nào**.

Material-aware outline dùng `script_architecture.story_material_contract_version = 1` và mỗi section phải có:

- `narrative_job`, entry/exit state;
- `audience_experience` mô tả reconstructable reality audience theo dõi;
- `material_ids`;
- `claim_ids`;
- `transition`;
- dependencies và target range.

`audience_experience` không được chỉ là interpretation. Nếu bỏ lời giải thích, material vẫn phải còn state/action/change/failure/consequence có thể hình dung. Nếu không: thiếu detail → research; boundary/movement sai → outline. Không đẩy lỗi xuống writer.

## 6. Materialization và cycle integrity

Sau human approval:

```bash
python scripts/approval.py approve-outline products/<slug>
python scripts/materialize_sections.py products/<slug> --archive-previous-cycle
```

Materializer deterministic tạo cho material-aware section:

- `section.json` với đúng `cycle_id`, outline hash, `audience_experience`, `material_ids`, transition và status `ready_for_draft`;
- `brief.md` từ outline hiện tại;
- `material-pack.json` chứa trực tiếp reconstructable material + source locators + limitations;
- `evidence-pack.json` chứa claim allowance;
- `narration-pack.json` schema material-aware, nối claim ceiling và evidence limits;
- `continuity-in.md`.

Nó **không tạo story-plan** cho material-aware section.

Materializer fail-closed nếu material không tồn tại hoặc cần claim nằm ngoài claim ceiling của section. Validator fail nếu section/evidence/material/narration pack khác cycle hoặc stale so với approved outline.

Không được có trạng thái outline C003 nhưng section packet C002.

## 7. Drafting

Writer nhận:

- Creative Boundaries;
- Channel Constitution;
- story bible + voice profile;
- local section brief;
- material pack;
- narration pack;
- approved dependency handoffs.

Writer không nhận story-plan trong material-aware cycle.

Mặc định ưu tiên:

`reconstructable reality → evidenced action/change → consequence → only needed interpretation`

Đây không phải paragraph template. Writer tự quyết opening, ordering, paragraph, rhythm, transition và phrasing.

Guardrail mặc định là silent constraint. Trước handoff writer tự cắt explanation echo, repeated payoff, guardrail exposition và meta-commentary không tạo thêm fact/boundary/consequence.

Target range không phải quota; hard cap 3.000 từ/work unit vẫn được máy giữ.

## 8. Outcome evaluation

`review_section` kiểm tra outcome độc lập. Audio test mạnh là:

> Sau mỗi stretch chính, listener có thể kể lại cái gì vừa tồn tại, được làm, thay đổi, thất bại hoặc tạo consequence không?

Nếu listener chủ yếu chỉ có thể nói “narrator vừa giải thích rằng X có nghĩa Y”, flag `expository_reconstruction_failure`.

Routing mới của material-aware flow:

- `prose_execution`: material/outline đủ, writer dùng prose sai;
- `product_architecture`: movement, material selection hoặc section boundary sai;
- `evidence`: detail/claim cần thiết thiếu hoặc không đủ chắc.

Không dùng `local_design` như nơi mặc định cứu lỗi vì active flow không còn story-plan design layer.

## 9. Rework và replay

Semantic rework vẫn là interface ưu tiên:

```bash
python scripts/rework.py products/<slug> draft_section --section P01 --request "Rewrite prose from the same approved material handoff"
python scripts/rework.py products/<slug> outline --request "Rebuild the story architecture"
python scripts/rework.py products/<slug> research_workstream --request "Reopen material evidence"
```

Compatibility-only operations không được semantic rework route tới.

Replay active path chỉ còn:

`outline → materialize → draft_section`

```bash
python scripts/replay.py start products/<slug> --from outline --through draft_section --section P01 --request "Regression"
```

## 10. Production cycles và assembly

Cycle mới giữ research đã duyệt trừ khi rework bắt đầu từ research. Old section workspaces được archive recoverably dưới `03_sections/_history/<cycle>/` trước rematerialization.

`assemble.py` chỉ ghép section đã human-approved. Git history, task reports, hashes và product-local history giữ provenance/audit trail.

## Minimal handoff prompt

```text
Đọc AGENTS.md, rồi thực hiện task active của products/<slug>. Chỉ dùng compiled packet, không quét repo và không tự approve output.
```
