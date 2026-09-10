# YT Production

YT Production là môi trường xây dựng tác phẩm lịch sử từ những câu hỏi đáng theo đuổi về con người và thế giới của họ. Evidence bảo vệ tính trung thực; nó không tự chọn câu chuyện. Research phát hiện và kiểm tra các khả năng kể; outline tổ chức hành trình; Writer kể hành trình đó; review đọc sản phẩm trước rồi mới chẩn đoán lỗi.

## Canonical creative flow

```text
Owner question / work order
  → editorial question + scope
  → exploratory research + route comparison
  → targeted research for the selected journey
  → whole-work outline
  → narrative compression
  → product-first review + evidence check
  → Owner reading / approval
  → full prose only when separately ordered
```

Một direct Owner work order có thể authorize toàn chuỗi bounded ở trên. Không tự dựng lại các intermediate approval gate của flow cũ khi Owner đã giao end-to-end execution. Owner vẫn giữ quyền chấp nhận nội dung cuối cùng.

## Decision ownership

- **Research** xác định điều có thể nói trung thực **và** phát hiện situations, processes, relationships, voices, texts, objects, disputes hoặc discoveries có thể gánh câu chuyện. Research có thể làm yếu hoặc thay đổi route ban đầu.
- **Outline** sở hữu whole-work journey: người nghe theo gì, vì sao từng movement tồn tại, quan hệ giữa các movement, thứ tự discovery, nơi exposition được earned và cách ending tích lũy trọng lượng.
- **Writer** sở hữu execution trong architecture và truth boundary: pacing, local selection, prose, imagery, transitions, scale, viewpoint. Nếu material/architecture không gánh được route, Writer phải flag/sửa đúng lớp thay vì trang trí câu chữ.
- **Review** đọc output trước; kiểm tra progression, accumulation và listening experience; sau đó kiểm tra riêng historical integrity và route failure về đúng layer.

Production unit như `P##` chỉ là context/revision unit. Không suy ra story structure từ taxonomy về function/capability của đối tượng.

## Historical integrity

Source URL/locator, provenance, uncertainty, chronology và ranh giới giữa documented event, documented tradition, hypothesis, inference và reconstruction phải được giữ. Myth/literary tradition có thể là story material khi được frame đúng tư cách. Hypothesis/guided inference có thể gánh narrative weight khi listener thấy clue, support và phần chưa ngã ngũ. Không biến qualification thành thay thế cho storytelling và không dùng storytelling để vượt source.

## Current product: `products/sumer-writing`

Narrative identity reset hiện dùng:

1. `products/sumer-writing/00_brief/product-brief.md`
2. `products/sumer-writing/01_research/narrative-identity-reset-01.md`
3. `products/sumer-writing/02_outline/outline.md` — canonical human-readable narrative architecture
4. `products/sumer-writing/02_outline/story-bible.md`
5. `products/sumer-writing/02_outline/voice-profile.md`

Whole-work compression chờ Owner đọc:

`writer-output/full-script/narrative-identity-reset-01/compression.md`

`outline.json`, section overlays và các P01–P08 workflow cũ được giữ để compatibility/audit cho tới khi một runtime task thật sự cần materialize lại; chúng không được quyền kéo route mới quay về eight-function architecture. Bản mới không mang `approved_by`/`approved_at` của cycle cũ.

## Harness principle

**Hard boundaries, creative ownership.** Code/validator nên giữ authority, allowed writes, lifecycle, provenance, source/evidence integrity và resource limits. Creative method, route và listening quality không được hard-code thành một taxonomy hay score tự động.

Xem thêm:

- `AGENTS.md` — router/authority hiện hành.
- `WRITER.md` — whole-work compression contract.
- `system/standards/channel-constitution.md` — creative identity dùng được cho nhiều đề tài.
- `docs/WORKFLOW.md` — ownership và production workflow.
- `docs/HARNESS.md` — ranh giới hard/soft/evaluation.

Các experiment/MVP cũ vẫn được giữ làm bằng chứng và compatibility surface nhưng không phải default creative path.