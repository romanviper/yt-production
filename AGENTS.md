# Agent Instructions

Các chỉ dẫn này áp dụng cho toàn repo.

## 1. Read order và precedence

Trước khi làm bất kỳ task nào, đọc:

1. `system/00-operating-contract.md` rồi toàn bộ `system/*.md` theo số thứ tự;
2. `products/<slug>/product.json`;
3. `products/<slug>/work-order.json`;
4. đúng các file trong `required_reads` của work order.

Khi có xung đột, thứ tự ưu tiên là:

1. yêu cầu trực tiếp mới nhất của người dùng;
2. quyết định có `locked: true` trong product workspace;
3. work order hiện hành;
4. `system/`;
5. suy luận hoặc kiến thức nền của Agent.

Không dùng ký ức ngoài repo để ghi đè một quyết định đã khóa.

## 2. Atomic work only

- Chỉ sửa các file khớp `allowed_write_paths` trong work order.
- Không tái sinh toàn bộ kịch bản để sửa một lỗi cục bộ.
- Không sửa `06_delivery/script.md` bằng tay; dùng `scripts/assemble.py`.
- Không tự đổi trạng thái gate thành `approved`. Chỉ con người mới phê duyệt.
- Nếu task đòi sửa file đã khóa nhưng work order không cấp quyền, dừng và báo impact.
- Nếu thiếu bằng chứng hoặc quyết định, ghi blocker; không lấp khoảng trống bằng prose nghe hợp lý.

## 3. Historical integrity

- Tách `fact`, `inference`, `contested` và `unknown` trong claim ledger.
- Một cảnh lịch sử không được chứa hành động, suy nghĩ, hội thoại, thời tiết hoặc chi tiết giác quan do Agent tự bịa.
- Claim quan trọng phải truy được đến source có locator cụ thể.
- Không biến một giả thuyết học thuật thành sự thật chỉ vì nó tạo câu chuyện hay hơn.
- Không sao chép hoặc mô phỏng sát cách diễn đạt đặc trưng của bất kỳ creator nào, kể cả *Fall of Civilizations*.

## 4. Long-form rules

- Không bao giờ draft toàn bộ script 1–2 giờ trong một task.
- Đơn vị draft mặc định là một chapter 5–12 phút hoặc một sequence nhỏ hơn.
- Trước khi draft chapter, chapter đó phải có brief, evidence set và entry/exit state.
- Mọi revision phải bắt đầu bằng impact analysis và kết thúc bằng cập nhật revision log.

## 5. Completion contract

Trước khi kết thúc task:

1. chạy `python scripts/validate.py products/<slug>`;
2. chạy `python scripts/check_scope.py products/<slug>` nếu đang trong git worktree;
3. nêu chính xác file đã thay đổi, claim bị ảnh hưởng và gate còn thiếu;
4. không tuyên bố “hoàn tất kịch bản” nếu mới hoàn tất một module.

