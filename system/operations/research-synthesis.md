# Operation — Research Synthesis

## Responsibility

Hợp nhất các workstream handoff thành một mental model có thể dùng để dựng outline. Global source/claim/material ledgers đã được router hợp nhất bằng code trước khi task bắt đầu và không phải output của AI task này.

## Outputs

- `research-synthesis.md`: causal model, chronology, contradictions, claim decisions và open decisions.
- `story-material-map.json`: bản đồ vật liệu lịch sử đủ chắc để outline có thể dùng làm carrier cho các chặng chính.

## Rules

- Không mở hoặc rewrite toàn bộ local/global ledger; `consolidation.json` xác nhận provenance.
- Dùng workstream synthesis làm bounded handoff. Thiếu evidence thì trả blocker đúng workstream.
- Conflict trở thành contradiction, không trung bình hóa.
- Phân biệt chronology, mechanism, magnitude, lived experience và reconstructable detail.
- `research-synthesis.md` tổ chức theo causal chain, không theo WS01, WS02…

## Story material map

Map không phải outline. Với mỗi major phase, nó trả hai câu hỏi riêng:

1. material có support movement không?
2. narration bằng âm thanh có thể thuật lại **cái gì tồn tại, được làm, thay đổi, thất bại hoặc để lại hậu quả** mà không để scholarly interpretation gánh phần lớn movement?

Phân loại:

- **A — strong recountable material:** có trạng thái cụ thể → action/change → trạng thái/hệ quả mới;
- **B — illustrative material:** có object/case/process nhưng movement vẫn phụ thuộc đáng kể vào synthesis;
- **C — material gap:** logic có support nhưng thiếu reconstructable detail để story hóa trung thực.

Không yêu cầu mọi phase phải là scene. Process kéo dài nhiều thế kỷ vẫn hợp lệ nếu sequence thay đổi có evidence.

Schema mới nên dùng `schema_version: 2` và giữ các field cũ, đồng thời mỗi `phases[]` thêm:

- `carrier_class`: `A`, `B` hoặc `C`;
- `audio_reconstruction`: một câu ngắn nói listener có thể hình dung/thuật lại điều gì;
- `material_ids`, `evidence_strength`, `gap` như trước.

`opening_candidates`, `reversal_candidates`, `ending_candidates` chỉ dùng `MAT-####` có trong ledger. Map không tạo material mới.

Legacy map schema 1 vẫn đọc được cho product đã khóa outline; mọi synthesis mới/rework phải xuất schema 2.

## Carrier sufficiency

Nếu opening, major reversal hoặc ending rơi vào loại C, surface gap trước khi outline khóa architecture. Loại B có thể dùng có chủ đích nhưng outline phải biết explanation vẫn đang gánh movement.

Đừng coi object là carrier chỉ vì visual tốt. Audience phải có thể theo một state/action/change/failure/consequence. Không nâng inference thành fact và không săn anecdote để lấp gap.
