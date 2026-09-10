# Narrative Identity Reset — Handoff

Work order: `WO-NARRATIVE-IDENTITY-RESET-01`  
Status: `draft_pending_owner_review`  
Starting commit: `f9b5553ec750c47b9dd266a2725d317f90826a92`  
Implementation head before this handoff: `dc62f227a4345fc64c02a1dd1272bf174ed28781`  
Final delivery commit: the commit that adds this handoff (reported in the delivery response).

## Owner đọc trước

1. `products/sumer-writing/02_outline/outline.md`
2. `writer-output/full-script/narrative-identity-reset-01/compression.md`

Hai artifact trên là bản mới chờ Owner đọc. Không mang approval metadata cũ và không được coi là Owner-approved.

## Phạm vi đã chọn

Tác phẩm vẫn tập trung vào Mesopotamia/cuneiform thay vì mở thành universal history of writing. Decipherment mở sang Old Persian/Bisotun và nineteenth-century Assyriology chỉ ở mức cần thiết để hoàn tất story về việc living reading competence biến mất rồi được dựng lại.

Central route được chọn sau khi so sánh ba khả năng là **“Một lời nhắn tìm người đọc”**: khoảng cách giữa dấu/text và người có thể hiểu nó tăng dần qua memory, physical absence, social action, training, language change, specialist survival, competence break và decipherment.

Không chọn capacity catalogue làm spine; không chọn state-control thesis làm spine.

## Quyết định lớn đã đổi

- Topic không còn được materialize thành tám capability/function rồi yêu cầu Writer làm từng capability cinematic.
- Research vừa giữ truth/provenance vừa có trách nhiệm phát hiện situation/process/relationship đủ sức gánh story.
- Outline sở hữu whole-work journey, structural cases, ordering, dependencies, earned exposition và ending accumulation; không đẩy mọi route decision xuống Writer.
- Writer sở hữu local execution nhưng được quyền flag/reopen architecture/material failure thay vì che bằng style.
- Review đọc product trước rồi mới route lỗi về story choice / architecture / research / handoff / prose / historical integrity.
- `P##` được coi là production unit, không phải mandatory narrative taxonomy.

## Chất liệu cũ giữ lại và vai trò mới

- **Enmerkar:** giữ như documented later literary tradition tạo promise/mismatch; không invention proof.
- **Early Uruk administrative evidence:** giữ như archaeological reversal; không sole-cause thesis.
- **Phonetic/rebus development:** giữ vì giải quyết question opening đã earned, không phải một feature chapter độc lập.
- **Marduk-mushallim:** giữ và phát triển thành stress-test giữa message reception và action, không phải ví dụ ngắn cho “clay cannot obey”.
- **Scribal schooling:** chuyển thành mechanism tạo reader mới qua generations.
- **Sumerian–Akkadian bilingual tradition:** dùng để tăng linguistic distance giữa text và reader.
- **Late cuneiform / latest-known anchors:** dùng để kể contraction without invented last scribe.
- **Decipherment:** trở thành ending/reversal—một community mới manufacture reading competence sau rupture.

## Research mới / source checks

Research dossier: `products/sumer-writing/01_research/narrative-identity-reset-01.md`.

Nó chứa 2–3 route comparison, selected-route research cho opening/middle/ending, source URLs/locators, boundaries và remaining limitations. Trong final review pass, các source quan trọng đã được kiểm tra trực tiếp ở mức cần thiết:

- ETCSL lines 500–535 support messenger unable to repeat the extensive speech, Enmerkar writing on clay, and the tablet being examined at Aratta.
- The Met object 86.11.111 supports the Marduk-mushallim report, ca. 1632 BCE, and the warning that king's orders including night gate closure were not implemented.
- Encyclopaedia Iranica supports latest-known cuneiform texts in the 1st century CE, later oblivion, and a distributed nineteenth-century decipherment history rather than a lone-genius story.

ORACC Old Babylonian School remains a cited source in the dossier; the live page could not be retrieved by the external browser during this final pass, so its use remains grounded in the previously captured research record rather than a fresh browser verification here.

## Canonical instruction surfaces synchronized

- `AGENTS.md`
- `README.md`
- `WRITER.md`
- `system/standards/channel-constitution.md`
- `system/standards/outcome-evaluation.md`
- `system/operations/research-plan.md`
- `system/operations/research-workstream.md`
- `system/operations/research-synthesis.md`
- `system/operations/outline.md`
- `docs/WORKFLOW.md`
- `docs/HARNESS.md`
- product brief / story bible / voice profile

`outline.md` is explicitly the canonical human-readable architecture for this reset. Existing `outline.json`, old section overlays and old P01–P08 artifacts are retained for audit/compatibility and must not override the new narrative route. They should only be rematerialized/synchronized when an actual runtime/full-prose task requires them.

## Product review result

The new outline and compression agree on the same cumulative route. Major movements are not freely swappable: schooling supplies the mechanism for bilingual learned transmission; bilingual transmission gives historical substance to the later contraction; contraction creates the rupture that makes decipherment a true ending rather than an antiquarian appendix.

The compression tells the entire selected journey rather than stopping at P01. Historical limitations are embedded at the points where they affect interpretation (Enmerkar status, early language uncertainty, exceptional letter scope, gradual language change, latest-known vs absolute last, collective decipherment).

No automatic score or retention claim is attached. Owner remains final judge of story quality.

## Integrity / runtime checks

No production code was changed in the completion pass because no demonstrated runtime dependency required it for the two review artifacts. GitHub branch/commit state and file-level diffs were checked through the repository connector.

A local clone/test run was attempted for an additional filesystem-level check but the execution environment could not resolve `github.com`; therefore no local Python validator/test suite result is claimed. This is recorded as an environment limitation, not as a pass.

## Remaining limitations

- Early phonetic/rebus detail is deliberately reused from the existing reviewed evidence graph; full prose should resolve exact exemplars/locators before expanding that technical transition.
- Marduk-mushallim is one bounded case, not a representative sample of command compliance.
- The late endpoint remains a latest-known evidence anchor, not a biographical last-reader scene.
- `outline.json` still represents legacy machine state and carries old approval/section assumptions. It is deliberately removed from creative authority for this review pass rather than rewritten without an actual runtime consumer. Before any runtime that reads it is used for full-prose production, synchronize it to the Owner-reviewed architecture and strip inherited approval metadata.

## Stop condition

Work order stops here for Owner reading of outline + compression. Do not expand to the 60–120 minute full prose until separately ordered.