# Operation — Research Synthesis

## Responsibility

Hợp nhất workstream handoff thành **authoritative research model** cho outline. Global source/claim ledgers đã được router hợp nhất bằng code trước task và không phải output của AI task này.

Research synthesis owns truth integration, không owns storytelling architecture.

## Output

- `research-synthesis.md`: causal model, chronology, contradictions, claim decisions, confidence/qualification và open evidence decisions.

`story-material-map.json` là legacy compatibility artifact. Synthesis mới/rework không bắt buộc tạo hoặc cập nhật nó.

## Rules

- Không mở hoặc rewrite toàn bộ local/global ledger; `consolidation.json` xác nhận provenance.
- Dùng workstream synthesis làm bounded handoff. Thiếu evidence thì trả blocker đúng workstream.
- Conflict trở thành contradiction, không trung bình hóa.
- Phân biệt chronology, mechanism, magnitude, lived experience và source-level detail.
- Xác định claim trụ cột nào supported, qualified, contested, rejected hoặc vẫn unknown.
- `research-synthesis.md` tổ chức theo causal/chronological problem, không theo WS01, WS02…
- Concrete detail từ optional material ledger có thể được nhắc để tránh information loss, nhưng synthesis không quyết định detail nào phải trở thành carrier, scene, opening, reversal, ending hoặc narrative route.

## Separation of decision ownership

Research synthesis trả lời:

- Điều gì đã xảy ra / có thể khẳng định?
- Chronology nào đủ chắc?
- Mechanism nào được support đến mức nào?
- Bằng chứng nào mâu thuẫn hoặc giới hạn kết luận?
- Nguồn/locator nào support claim?
- Khoảng trống evidence nằm ở đâu?

Nó không trả lời:

- Audience phải theo object/person/process nào?
- Material nào “narratable” hơn?
- Story phải mở bằng gì?
- Reversal hay ending nên dùng case nào?
- Sequence nào writer phải kể?

Nếu một fact/source detail có thể hữu ích cho downstream nhưng không thuộc causal synthesis chính, giữ locator/provenance ở evidence store thay vì biến nó thành story recommendation.
