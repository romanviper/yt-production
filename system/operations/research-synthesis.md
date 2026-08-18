# Operation — Research Synthesis

## Responsibility

Hợp nhất các workstream handoff thành một mental model có thể dùng để dựng outline. Global source/claim/material ledgers đã được router hợp nhất bằng code trước khi task bắt đầu và không phải output của AI task này.

## Outputs

- `research-synthesis.md`: causal model, chronology, contradictions, claim decisions và open decisions.
- `story-material-map.json`: bản đồ vật liệu lịch sử đủ chắc để outline có thể dùng làm carrier cho các chặng chính.

## Rules

- Không mở hoặc rewrite toàn bộ local/global ledger trong task này; `consolidation.json` xác nhận chúng đã được remap và giữ provenance.
- Dùng workstream synthesis làm bounded handoff. Nếu handoff thiếu evidence cần thiết, trả blocker về đúng workstream thay vì nạp mọi ledger để bù.
- Conflict giữa workstream trở thành contradiction, không bị “giải quyết” bằng trung bình hóa.
- Phân biệt evidence về chronology, mechanism, magnitude và lived experience.
- Xác định claim trụ cột nào đủ support, cần qualify hoặc phải loại.
- `research-synthesis.md` tổ chức theo causal chain và open decisions, không theo WS01, WS02…

## Story material map

`story-material-map.json` không phải outline và không quyết định section. Nó chỉ trả lời: ở từng phase của causal chain, **có vật liệu cụ thể nào đủ chắc để audience theo một thay đổi hay không?**

Schema tối thiểu:

- `schema_version: 1`, `product`, `status: complete`;
- `phases[]`: mỗi phase có `id`, `story_function`, `state_change`, `material_ids`, `evidence_strength`, `gap`;
- `opening_candidates`, `reversal_candidates`, `ending_candidates`: danh sách material IDs phù hợp nếu có;
- `gaps`: những chặng logic quan trọng vẫn chỉ có abstract claims hoặc material quá yếu.

Chỉ dùng `MAT-####` có trong `material-ledger.json`. Một material có thể được dùng ở nhiều phase; map không tạo material mới và không được nâng inference thành fact.

## Carrier sufficiency

Một candidate carrier có thể là object, person, action, process, documented encounter, failure, consequence hoặc sequence. Không bắt buộc event chain và không ưu tiên anecdote hơn evidence.

Với mỗi major phase, phân biệt:

- material đủ sức mang một thay đổi mà audience có thể theo;
- material chỉ minh họa cho explanation;
- gap: chưa có vật liệu concrete đủ dùng.

Nếu opening/body reversal/ending dự kiến phụ thuộc vào carrier nhưng handoff chỉ có abstract claims hoặc locator quá rộng, ghi gap rõ ràng để trả về workstream trước khi outline khóa kiến trúc.

Đừng coi một object là carrier chỉ vì nó có hình ảnh tốt hoặc một claim thú vị. Phải có đủ evidence để biết audience có thể theo cái gì đang thay đổi, xảy ra, thất bại, được làm hoặc để lại consequence.
