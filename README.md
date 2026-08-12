# YT Production

Hệ điều hành biên tập cho phim lịch sử dài 1–2 giờ, được thiết kế để nhiều AI task có thể cộng tác mà không phải mang toàn bộ context của dự án vào mỗi context window.

## Kiến trúc

Repo có ba lớp độc lập:

- `system/`: contracts và standards cố định.
- `products/`: trạng thái và artifact của từng video.
- `scripts/`: orchestration thuần cơ học; không quyết định lịch sử hay văn phong.

Product Agent chỉ được làm việc trong `products/<slug>/`. Tầng control plane do System Architect quản lý qua architecture task riêng; system change và product content không được trộn trong cùng commit.

Agent không đọc toàn bộ `system/`. `scripts/task.py` biên dịch đúng instruction và input cần thiết thành một context packet cho từng task.

Giao tiếp cũng có hai lớp: task report giữ chiều sâu, operator brief giữ bức tranh điều hành. Status/handoff mặc định ngắn; explanation, audit và artifact được mở rộng khi mục đích cần.

## Production flow

```text
research plan
  → research workstreams độc lập
  → research synthesis
  → outline 10 phần
  → materialize section workspaces
  → draft/review/revise từng phần
  → integration qua handoff summaries
  → deterministic assembly
  → optional final audit
```

Research thô không đi vào task viết. Mỗi phần nhận một evidence pack đã lọc; các phần khác được đại diện bằng story bible và handoff ngắn.

## Lệnh thường dùng

```bash
# Tạo product
python scripts/new_product.py ten-san-pham --title "Tên làm việc"

# Tạo/activate một task research plan
python scripts/task.py create products/ten-san-pham research_plan

# Tạo task viết riêng phần P04
python scripts/task.py create products/ten-san-pham draft_section --section P04

# Xem context packet Agent sẽ nhận
python scripts/task.py show products/ten-san-pham

# Sau khi Agent hoàn thành output và report
python scripts/task.py submit products/ten-san-pham <task-id>

# Render đúng brief ngắn mà Agent phải trả trong chat
python scripts/task.py brief products/ten-san-pham <task-id>

# Kiểm tra product, task packet và context budget
python scripts/validate.py products/ten-san-pham

# Ghép các phần đã approved
python scripts/assemble.py products/ten-san-pham
```

Chi tiết cho người vận hành: [`docs/WORKFLOW.md`](docs/WORKFLOW.md).

## Pilot

`products/sumer-writing/` đã khóa subject: câu chuyện về chữ viết trong nền văn minh Sumer. Research sẽ kiểm tra causal chain; không dùng research để quyết định lại subject.

*Fall of Civilizations* là benchmark/đối thủ liền kề. Repo học từ bar về evidence, causal clarity và human presence, nhưng cấm mô phỏng câu chữ, cadence hoặc structure đặc trưng.
