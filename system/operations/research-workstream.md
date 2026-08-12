# Operation — Research Workstream

## Responsibility

Research đúng một workstream. Web notes và quá trình tìm kiếm không phải deliverable; các task sau chỉ nhận structured evidence và synthesis.

## Outputs

- `sources.json`: source records có ID namespaced `{WS##}-SRC-{###}`, type, authority, locators, access status, limitation và notes.
- `claims.json`: claim có ID namespaced `{WS##}-CLM-{###}`, classification, confidence, local source IDs, counterevidence, status và narrative implication.
- `synthesis.md`: tối đa khoảng 2.500 từ, trả question, nêu mechanism, chronology, strongest evidence, contradictions, unknowns và handoff cho synthesis toàn cục.

ID local được namespace để các workstream có thể chạy độc lập mà không collision. Operation `research_synthesis` sẽ cấp ID toàn cục và giữ provenance về ID local.

Không kể lại mọi nguồn. Không viết đoạn narration có thể copy thẳng vào script.
