# 06 — Modular Drafting and Revision

## Kích thước module

Đơn vị draft mặc định là một chapter 5–12 phút, thường khoảng 700–1.600 từ ở tốc độ 130–150 từ/phút. Chapter phức tạp có thể tách thành sequence nhỏ hơn.

Đây là budget, không phải quota. Không kéo dài prose để đạt số từ.

## Stable identity

- Chapter dùng ID `CH##`; sequence dùng `CH##-S##`.
- ID không đổi khi đổi tiêu đề hoặc di chuyển thứ tự.
- Mọi claim, source, visual note và revision tham chiếu ID, không tham chiếu “chapter thứ ba”.

## Three-file separation

Mỗi chapter có ba loại dữ liệu tách biệt:

1. brief trong `03_outline/chapters/CH##-*.md`;
2. prose trong `04_script/chapters/CH##-*.md`;
3. review trong `05_review/chapters/CH##-*.md` khi cần.

Không chôn yêu cầu biên tập vào prose narration.

## Draft protocol

Trước khi viết:

1. xác nhận gate và trạng thái chapter;
2. đọc brief, claim ledger entries, source notes và continuity ledger liên quan;
3. liệt kê blocker;
4. nếu không có blocker, chỉ draft file được cấp quyền;
5. tự review local nhưng không tự phê duyệt.

## Revision protocol

Mỗi change request phải nêu:

- lỗi quan sát được, không chỉ “chưa hay”;
- target file/sequence;
- invariant phải giữ;
- claim hoặc continuity fact có thể bị ảnh hưởng;
- acceptance test.

Sau đó chạy `scripts/impact.py`. Chỉ mở rộng write scope khi dependency map chứng minh cần thiết.

### Revision classes

| Class | Ví dụ | Scope mặc định |
|---|---|---|
| R1 — copy | câu khó đọc, lặp từ | một đoạn |
| R2 — local logic | causal link thiếu | một sequence |
| R3 — chapter structure | payoff sai vị trí | một chapter + bridges |
| R4 — cross-chapter | contradiction, chronology | affected chapters từ impact graph |
| R5 — premise | central question hoặc scope sai | dừng draft, quay gate |

Không giải lỗi R1/R2 bằng regeneration R4/R5.

## Assembly

`scripts/assemble.py` ghép các chapter `approved` theo manifest, tạo hash cho từng source file và ghi `assembly-manifest.json`. Khi một chapter đổi, bản delivery được coi là stale cho tới lần assemble kế tiếp.

Assembly không phải integration review. Nó chỉ bảo đảm thứ tự và tính toàn vẹn file.

