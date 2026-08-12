# AI Agent Router

This file is the only repo-wide instruction an Agent reads automatically.

## Do not load the repository

Không đọc đệ quy `system/`, `products/` hoặc toàn bộ script. Repo được thiết kế để tránh context bloat. Một task hợp lệ phải có context packet tự chứa.

## Khi người dùng nói “tiếp tục task hiện tại”

1. Xác định product được nêu; nếu không nêu và repo chỉ có một product, dùng product đó.
2. Đọc `products/<slug>/tasks/ACTIVE.json`.
3. Đọc work order và đúng **một** packet được trỏ trong file này.
4. Không đọc thêm file ngoài packet trừ khi work order liệt kê hoặc packet báo thiếu input.
5. Chỉ sửa `allowed_write_paths`.
6. Chạy validation được ghi trong packet.
7. Ghi full detail vào `report.md`, ghi executive brief vào `operator-brief.json`, rồi chạy `python scripts/task.py submit products/<slug> <task-id>`.
8. Không tự phê duyệt output.

## Khi người dùng gọi một nghiệp vụ cụ thể

Ví dụ: “viết phần P04”, “review phần P07”, “research workstream WS02”.

1. Tạo task bằng router:

   ```bash
   python scripts/task.py create products/<slug> <operation> --section P04
   ```

   Dùng `--unit WS02` cho research workstream.
2. Router phải tạo work order và context packet thành công trước khi làm nội dung.
3. Sau đó thực hiện đúng packet. Nếu task cũ còn active, không ghi đè im lặng.

Các operation hợp lệ nằm trong `system/operations/registry.json`. Không tự chế operation ngoài registry.

## Khi người dùng chỉ hỏi tình trạng, giải thích hoặc review read-only

- Không tạo task hay sửa file nếu yêu cầu chỉ là đọc và báo cáo.
- Nếu có `ACTIVE.json`, chỉ đọc work order và packet của task đó.
- Nếu chưa có active task, đọc `product.json` và đúng artifact của checkpoint hiện tại; không quét product.
- Trả lời theo Operator Interface bên dưới. Chỉ mở phân tích dài khi người dùng yêu cầu rõ.

## Invariants

- Một task = một nghiệp vụ = một target chính.
- Không generate toàn bộ kịch bản dài trong một task.
- Không draft một section nếu chưa có brief và evidence pack.
- Không dùng raw research khi section evidence pack đã tồn tại.
- Không sửa section khác để “giữ continuity”; tạo impact/change request.
- Không sửa delivery artifact bằng tay.
- `approved` chỉ do con người đặt.
- Không chạy `scripts/approval.py` nếu người dùng không vừa đưa ra quyết định approve/request-changes rõ ràng.
- Packet stale, thiếu source hoặc vượt context budget là blocker, không phải giấy phép suy diễn.

## Operator Interface

Chọn độ sâu theo mục đích, không theo lượng công việc Agent đã làm:

- **Brief:** status, handoff, blocker và approval — kết luận trước, tối đa 140 từ, tối đa ba điểm quan trọng.
- **Guided explanation:** câu hỏi `tại sao/như thế nào`, concept hoặc trade-off — giải thích vừa đủ, không có trần 140 từ.
- **Deep review:** yêu cầu evidence/audit/phản biện chi tiết — executive summary trước, chi tiết có cấu trúc sau.
- **Deliverable:** người dùng muốn xem outline/draft/artifact thật — brief trước rồi hiển thị hoặc liên kết artifact; không thay nội dung cần duyệt bằng tóm tắt.

Trong mọi mode:

- Chỉ nêu điều liên quan tới mục đích hiện tại; không kể process, command, hash, test bình thường hoặc tuyên bố dài về những gì Agent không làm.
- Nếu cần quyết định: đưa một khuyến nghị, đúng một câu hỏi hiện tại và hiệu lực của tối đa ba lựa chọn.
- Blocker, uncertainty và trade-off quan trọng không được giấu để giữ câu trả lời ngắn.
- Chi tiết kỹ thuật mặc định ở `report.md`; mở khi người dùng yêu cầu hoặc khi cần để quyết định an toàn.

Với task, lớp đầu của câu trả lời phải là output của:

```bash
python scripts/task.py brief products/<slug> <task-id>
```

Chỉ nối thêm explanation/deep review/deliverable khi người dùng đã yêu cầu lớp đó. Không thêm nhật ký thực thi. Contract đầy đủ nằm trong packet tại `system/standards/operator-interface.md`.
