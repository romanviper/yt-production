# 00 — Operating Contract

## Mục đích

Repo này là một state machine biên tập, không phải kho prompt. Agent phải tạo ra bằng chứng của từng quyết định trước khi chuyển sang bước tiếp theo.

## Hai lớp bất biến

### Production system

`system/`, `templates/` và `scripts/` là lớp cố định. Thay đổi ở đây có thể ảnh hưởng mọi sản phẩm, nên phải được xem như thay đổi hệ thống và cần review riêng.

### Product workspace

`products/<slug>/` chứa toàn bộ trạng thái, bằng chứng và output của một video. Không đưa fact hoặc quyết định chỉ có giá trị cho một video vào `system/`.

## Đơn vị công việc: work order

Mọi lượt Agent phải có `work-order.json` gồm:

- `task_type`: loại công việc;
- `objective`: một outcome kiểm chứng được;
- `required_reads`: input bắt buộc;
- `allowed_write_paths`: phạm vi write duy nhất;
- `acceptance_criteria`: điều kiện kết thúc;
- `blocked_by`: dependency chưa giải quyết;
- `state`: `ready`, `in_progress`, `blocked`, `review` hoặc `closed`.

Nếu task không vừa trong một work order, phải tách task. Không nới write scope chỉ để tiện.

## Quyền phê duyệt

Agent có thể đề xuất `candidate` hoặc `ready_for_review`. Chỉ người dùng mới được:

- khóa premise;
- chấp nhận một diễn giải gây tranh cãi;
- duyệt chapter;
- duyệt thay đổi phạm vi;
- đổi gate thành `approved`.

## Điều kiện dừng

Agent dừng thay vì suy diễn khi:

- premise chưa khóa nhưng task yêu cầu prose dài;
- claim trụ cột không có source đủ mạnh;
- hai nguồn có thẩm quyền mâu thuẫn mà chưa được trình bày;
- một revision có thể ảnh hưởng file ngoài write scope;
- yêu cầu chất lượng đòi asset, chuyên gia hoặc quyền sử dụng chưa có.

## Một source of truth cho mỗi loại dữ liệu

| Dữ liệu | Source of truth |
|---|---|
| trạng thái sản phẩm và gate | `product.json` |
| nhiệm vụ Agent hiện tại | `work-order.json` |
| thư mục và thứ tự chapter | `03_outline/manifest.json` |
| bằng chứng | `01_research/source-index.json` |
| claim và mức chắc chắn | `01_research/claim-ledger.json` |
| tên, ngày, thuật ngữ canonical | `02_story/continuity.md` |
| prose | `04_script/chapters/*.md` |
| lịch sử sửa | `05_review/revision-log.md` |
| bản ghép | `06_delivery/script.md` |

Không nhân đôi trạng thái sang nhiều file.

