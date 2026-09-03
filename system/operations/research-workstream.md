# Operation — Research Workstream

## Responsibility

Research đúng một workstream và bàn giao **authoritative evidence**, không pre-author story. Web notes và quá trình tìm kiếm không phải deliverable.

Research owns truth:

- source, locator và provenance;
- claim, classification, confidence và status;
- chronology;
- contradiction, counterevidence và qualification;
- factual limitation;
- concrete source detail khi detail đó dễ mất qua compression.

Research không quyết định audience nên follow gì, carrier nào nên dùng, opening/reversal/ending, narrative route, reveal strategy hay sequence nào phải trở thành storytelling.

## Required outputs

- `sources.json`: source records có ID namespaced `{WS##}-SRC-{###}`, type, authority, locators, access status, limitation và notes.
- `claims.json`: claim có ID namespaced `{WS##}-CLM-{###}`, classification, confidence, local source IDs, counterevidence, status và narrative implication.
- `synthesis.md`: tối đa khoảng 2.500 từ, trả question, chronology/mechanism, strongest evidence, contradictions, unknowns và handoff cho synthesis toàn cục.

ID local được namespace để các workstream có thể chạy độc lập. `research_synthesis` nhận ledger đã remap và provenance local được giữ lại.

## Optional evidence-preservation artifact

`materials.json` có thể tồn tại khi một primary object/case/process có concrete detail dễ mất hoặc provenance/limitation phức tạp. Nó là **evidence-preservation artifact**, không phải story plan.

Nếu dùng, mỗi record nên giữ các trường sự thật khi source trực tiếp support:

- `id`, `kind`, `label`;
- `claim_ids` liên quan;
- `source_refs` với locator hẹp;
- `actor` hoặc acting system khi được support trực tiếp;
- `object_or_trace`: vật thể, di tích hoặc dấu vết;
- `documented_action`: hành động được ghi lại trong tư liệu;
- `explicit_sequence`: trình tự các bước hoặc biến cố được source nêu rõ;
- `time`, `place`, `physical_description`, `measurement`, `spatial_relation`;
- `unresolved_question`: câu hỏi lịch sử còn bỏ ngỏ mà tư liệu phản ánh;
- `later_evidence`: bằng chứng/phát hiện về sau làm thay đổi cách hiểu;
- `source_relation`: `contemporary_material`, `contemporary_interested_account`, `later_copy`, `retrospective_literature`, `cultural_tradition`, `modern_hypothesis`;
- concrete source-supported detail dưới `details` (để tương thích ngược);
- `limitations` và, khi hữu ích, `representativeness`.

Legacy material fields như `what_audience_follows`, `sequence` hoặc `narratable_reconstruction` vẫn có thể được đọc để không phá artifact cũ, nhưng output mới **không được bắt buộc** tạo chúng và downstream không được coi chúng là creative authority.

Không tạo narratability score/class. Không gắn opening/reversal/ending role. Không đánh giá material có “carry motion” hay không.

## Compression rule

Do not isolate information ownership. Isolate decision ownership.

Research có thể bảo tồn chi tiết source-level như measurement, physical description, documented action, spatial relation, chronology detail hoặc explicit sequence nếu source support. Mục đích là tránh mất evidence qua compression, không phải quyết định cách kể.

Không thêm weather, cảm xúc, dialogue, motive, action, spatial relation hoặc sensory detail nếu source không support. `narrative_implication` là handoff note về giới hạn/ý nghĩa của claim, không phải prose để copy và không phải route bắt buộc cho writer.
