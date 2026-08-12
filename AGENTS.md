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
7. Ghi task report và chạy `python scripts/task.py submit products/<slug> <task-id>`.
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

## Handoff

Kết thúc bằng:

- `Completed:` artifact nào đã tạo;
- `Changed:` đúng các đường dẫn đã sửa;
- `Checks:` validation/context scope;
- `Needs review:` quyết định của con người;
- `Next operation:` operation hợp lệ kế tiếp, không tự chạy nếu chưa được yêu cầu.
