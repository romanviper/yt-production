# Operation — Research Workstream

## Responsibility

Research đúng một workstream. Web notes và quá trình tìm kiếm không phải deliverable; các task sau chỉ nhận structured evidence và synthesis.

## Outputs

- `sources.json`: source records có ID namespaced `{WS##}-SRC-{###}`, type, authority, locators, access status, limitation và notes.
- `claims.json`: claim có ID namespaced `{WS##}-CLM-{###}`, classification, confidence, local source IDs, counterevidence, status và narrative implication.
- `materials.json`: candidate material có ID namespaced `{WS##}-MAT-{###}` để giữ những vật liệu lịch sử cụ thể có thể mang một phần câu chuyện.
- `synthesis.md`: tối đa khoảng 2.500 từ, trả question, nêu mechanism, chronology, strongest evidence, contradictions, unknowns và handoff cho synthesis toàn cục.

ID local được namespace để các workstream có thể chạy độc lập mà không collision. Operation `research_synthesis` sẽ nhận ledger đã được remap và giữ provenance về ID local.

## Story material contract

`materials.json` không phải danh sách anecdote hay ý tưởng viết. Chỉ ghi một material candidate khi evidence đủ để lớp sau dựng lại nó mà không bịa.

Mỗi material gồm:

- `id`, `kind`, `label`;
- `what_audience_follows`: một câu ngắn mô tả vật thể, người, hành động, process, encounter, failure, consequence hoặc sequence mà audience thực sự có thể theo;
- `sequence`: các bước hoặc thay đổi được evidence hỗ trợ, theo thứ tự nếu có;
- `claim_ids`: local claim IDs giới hạn điều có thể khẳng định;
- `source_refs`: local source ID kèm locator hẹp cho chính material này;
- `representativeness`: representative, exceptional, illustrative hoặc unknown;
- `limitations`: điều không được suy rộng hoặc chi tiết chưa chắc.

Locator của material phải đủ hẹp để truy lại chi tiết cần dùng. Page range rộng có thể support synthesis claim nhưng không đủ để coi là material evidence.

Một workstream có thể bàn giao `materials: []` nếu không có candidate đủ chắc. Không ép mọi workstream phải tìm người, scene hay event.

## Preserve usable historical material

Đừng chỉ bàn giao kết luận trừu tượng. Khi evidence cho phép, `synthesis.md` phải gọi đúng material ID và giải thích nó có thể giúp audience theo sự thay đổi nào.

`narrative_implication` của claim không phải prose để copy vào script. Nó chỉ nói claim support phần nào của object/process/consequence và giới hạn nào phải giữ.

Không kể lại mọi nguồn. Không viết narration có thể copy thẳng vào script. Không săn anecdote chỉ vì hấp dẫn nếu provenance hoặc representativeness yếu.
