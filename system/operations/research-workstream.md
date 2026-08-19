# Operation — Research Workstream

## Responsibility

Research đúng một workstream. Web notes và quá trình tìm kiếm không phải deliverable; các task sau chỉ nhận structured evidence và synthesis.

## Outputs

- `sources.json`: source records có ID namespaced `{WS##}-SRC-{###}`, type, authority, locators, access status, limitation và notes.
- `claims.json`: claim có ID namespaced `{WS##}-CLM-{###}`, classification, confidence, local source IDs, counterevidence, status và narrative implication.
- `materials.json`: candidate material có ID namespaced `{WS##}-MAT-{###}` để giữ thực tại lịch sử có thể tái dựng mà không bịa.
- `synthesis.md`: tối đa khoảng 2.500 từ, trả question, nêu mechanism, chronology, strongest evidence, contradictions, unknowns và handoff cho synthesis toàn cục.

ID local được namespace để các workstream có thể chạy độc lập mà không collision. Operation `research_synthesis` sẽ nhận ledger đã được remap và giữ provenance về ID local.

## Three distinct layers

Đừng trộn:

- **claim** — ta được phép khẳng định điều gì;
- **material** — narrator có thể thuật lại vật thể/người/hành động/quá trình/trạng thái/hậu quả nào;
- **interpretation** — material đó có ý nghĩa gì đối với mechanism hoặc movement.

`narrative_implication` là interpretation/handoff note, không phải prose và không thay thế material.

## Story material contract

Chỉ ghi material khi evidence đủ để lớp sau dựng lại nó trung thực. Mỗi material gồm:

- `id`, `kind`, `label`;
- `what_audience_follows`: orientation ngắn về thứ audience có thể theo;
- `narratable_reconstruction`: raw reconstructable reality. Có thể chứa `entities`, `initial_state`, `spatial_relations`, `documented_actions`, `state_changes`, `observable_details`, `time_place`, `uncertain_or_absent`. Chỉ điền field evidence support; không cần field rỗng;
- `sequence`: các bước/thay đổi được evidence hỗ trợ, theo thứ tự nếu có;
- `claim_ids`: local claim IDs giới hạn assertion;
- `source_refs`: local source ID kèm locator hẹp cho chính material;
- `representativeness`: representative, exceptional, illustrative hoặc unknown;
- `limitations`: điều không được suy rộng hoặc chi tiết chưa chắc;
- `narratability`: `high`, `medium` hoặc `low`.

`high`: có state/action/change đủ để thuật lại mà explanation không gánh phần lớn movement. `medium`: object/process rõ nhưng một phần movement vẫn cần synthesis. `low`: chủ yếu support conclusion, ít reconstructable detail. Đây không phải score phức tạp.

Locator của material phải đủ hẹp để truy lại chi tiết cần dùng. Page range rộng có thể support synthesis claim nhưng không đủ để coi là material evidence.

Một workstream có thể bàn giao `materials: []` nếu không có candidate đủ chắc. Không ép scene, person hay event.

## Preserve raw reconstructable reality

Nếu source support “teacher model ở bên trái, student copy bên phải bị erase”, giữ chi tiết đó. Đừng chỉ nén thành “scribal education required repeated practice”; câu sau là interpretation.

Không thêm weather, cảm xúc, dialogue, motive, action, spatial relation hoặc sensory detail nếu source không support. Researcher không viết cinematic prose.

`synthesis.md` phải gọi đúng material ID khi một material có thể mang thay đổi và nói rõ limitation. Không kể lại mọi nguồn, không săn anecdote chỉ vì hấp dẫn.
