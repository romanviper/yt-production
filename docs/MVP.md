# Owner-first MVP

**Yêu cầu sửa đang chờ:** [Request changes 02](MVP-REQUEST-CHANGES-02.md) bổ sung
hai Writer và budget thời gian do Owner kiểm soát. Tài liệu bên dưới mô tả
implementation một Writer hiện có; không phải bằng chứng tính năng mới đã hoàn tất.

Đây là đường hoạt động tối thiểu để đưa một bản đọc mới tới Owner trước khi quay lại các vòng chẩn đoán/benchmark phức tạp.

## Mục tiêu

```text
Owner giao đoạn cần viết
  → snapshot brief + authority
  → Planner tạo Plan ngắn
  → freeze Plan
  → Writer tạo một draft
  → freeze draft
  → Owner đọc
  → ghi nguyên văn feedback
  → STOP
```

MVP **không** tự chạy reviewer, A/B, FoC diagnosis, root-cause analysis hoặc reroll Writer. Một draft chưa hay vẫn là output hợp lệ để Owner phản hồi.

## Bắt đầu

Từ repo root:

```bash
python scripts/learning.py prepare \
  --run p01-owner-001 \
  --request "Viết một đoạn P01 độc lập để tôi đọc và phản hồi"

python scripts/learning.py status --run p01-owner-001
```

`status` luôn trả về:

- state hiện tại;
- đang chờ Planner, Writer hay Owner;
- artifact cần mở;
- hành động nhỏ nhất tiếp theo.

Runtime artifacts nằm dưới `runs/<id>/` và không phải production content.

## 1. Planner

Sau `prepare`, mở packet mà `status` chỉ ra, mặc định:

```text
runs/<id>/agents/plan/plan-001/input/packet.json
```

Đưa **chỉ packet này** cho một Planner session riêng. Với chuyển packet thủ công, session đó không cần repo/filesystem/network tools.

Planner trả một JSON ngắn:

```json
{
  "section": "P01",
  "telling_scope": "Đoạn này kể phần nào",
  "source_refs": ["overlay:P01", "HS-P01-0001"],
  "stop_condition": "Dừng ở đâu"
}
```

Không dùng source ngoài `source_refs_allowed` trong packet.

Khi nhận kết quả:

```bash
python scripts/learning.py freeze-plan \
  --run p01-owner-001 \
  --session plan-001 \
  --file /path/to/plan.json \
  --reason "Lý do ngắn do Planner khai báo" \
  --uncertainty "Điểm Planner còn chưa chắc"
```

Nếu host có execution log thật, có thể thêm `--host-log /path/to/log`. Nếu không có, bỏ qua; controller ghi đúng là `MANUAL_PACKET_TRANSFER` và không phát minh spawn receipt/log.

## 2. Writer

Sau khi Plan được freeze:

```bash
python scripts/learning.py status --run p01-owner-001
```

Mở Writer packet, mặc định:

```text
runs/<id>/agents/writer/writer-001/input/packet.json
```

Đưa chỉ packet này cho Writer session riêng. Writer được tự chọn cách kể trong Plan + authority đã freeze; 450–650 từ chỉ là kích thước thử dự kiến, không phải hard gate.

Nhận một draft Markdown rồi freeze:

```bash
python scripts/learning.py freeze-draft \
  --run p01-owner-001 \
  --session writer-001 \
  --file /path/to/draft.md \
  --reason "Lý do ngắn do Writer khai báo" \
  --uncertainty "Điểm Writer còn chưa chắc"
```

Controller tạo bản đọc hash-identical tại:

```text
runs/<id>/owner/draft.md
```

State lập tức trở thành `AWAITING_OWNER_FEEDBACK`. Không tự review hay reroll.

## 3. Owner feedback

Owner đọc `owner/draft.md`, sau đó ghi **nguyên văn** feedback:

```bash
python scripts/learning.py feedback \
  --run p01-owner-001 \
  --text "Phản hồi nguyên văn của Owner"
```

Hoặc dùng `--file feedback.txt`.

Feedback được bind với SHA-256 của đúng draft và state chuyển thành:

```text
OWNER_FEEDBACK_RECORDED
```

Từ đây MVP dừng. Owner chọn thay đổi tiếp theo; hệ thống không tự suy ra `symptom reduced`, causal proof hoặc candidate mới.

## Authority của P01

`prepare` snapshot và kiểm tra liên kết giữa:

- `products/sumer-writing/02_outline/section-overlays/P01.json`;
- `products/sumer-writing/03_sections/P01/historical-substrate.json`.

Planner/Writer packet chỉ mang P01 overlay + historical substrate đã snapshot. Không tự nghiên cứu mở rộng trong vòng đọc đầu tiên; không dùng B03, `EXPLANATION_BEFORE_NEED`, benchmark verdict hoặc FoC target làm mục tiêu mặc định.

## Immutability và session identity

Controller từ chối:

- sửa packet sau khi freeze rồi mới submit output;
- output từ sai `session_id`;
- Plan cite source ngoài authority;
- ghi đè Plan/draft đã nhận;
- feedback nếu draft copy đã bị thay đổi;
- rerun Writer sau khi đã chuyển draft cho Owner.

Mỗi handoff lưu input hash, output hash, role/session khai báo, lý do ngắn, uncertainty, thời điểm operator nhận và host log nếu thực sự được cung cấp.

## Workspace boundary

`scripts.learning.WorkspaceBroker` giới hạn role vào workspace riêng bằng resolved path, gồm `..`, absolute path và symlink escape. Nó ghi allowed/denied access vào `control/access-events.jsonl`.

**Giới hạn:** broker không phải OS sandbox. Chỉ được tuyên bố read/write isolation khi host cấp broker này làm filesystem surface duy nhất và không đồng thời cấp shell/network/general-filesystem tools. Chuyển packet bằng chat thủ công không chứng minh fresh-agent context isolation.

## TEST_ONLY fixture

Tests dùng `test_only=true` để chứng minh thao tác:

```text
prepare → Plan handoff → Writer handoff → owner/draft.md → Owner feedback stop
```

Fixture không chứng minh agent thật hoặc Owner thật đã tham gia.

## Luồng production và Phase 1–3

Production router hiện có vẫn là một luồng riêng. Các tài liệu/experiment Phase 1–3 và coordinator prototype là lịch sử/tham khảo cho đến khi Owner yêu cầu lấy lại một phần cụ thể. Chúng không phải prerequisite để tạo bản đọc MVP đầu tiên.
