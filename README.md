# YT Production

Hệ điều hành biên tập cho các phim lịch sử dài 1–2 giờ của kênh. Repo tách hoàn toàn hai lớp:

- `system/`: các chuẩn cố định mà AI Agent phải tuân theo ở mọi sản phẩm.
- `products/`: workspace và output có version của từng video.

Mục tiêu không phải khiến Agent viết một kịch bản dài trong một lượt. Mục tiêu là biến sản xuất thành chuỗi quyết định nhỏ, có bằng chứng, có điểm khóa và có thể sửa cục bộ mà không phá phần đã duyệt.

## Bắt đầu ở đâu

AI Agent phải đọc theo thứ tự:

1. [`AGENTS.md`](AGENTS.md)
2. [`system/00-operating-contract.md`](system/00-operating-contract.md)
3. toàn bộ các file còn lại trong `system/` theo số thứ tự
4. `product.json`, `work-order.json` và các file được liệt kê trong work order của sản phẩm hiện tại

Con người có thể bắt đầu bằng:

```bash
python scripts/new_product.py ten-san-pham --title "Tên làm việc"
python scripts/validate.py products/ten-san-pham
```

Các lệnh chính:

```bash
make check PRODUCT=sumer-writing
make impact PRODUCT=sumer-writing CLAIM=CLM-0001
make assemble PRODUCT=sumer-writing
make test
```

`assemble` chỉ lắp các chapter đã được duyệt. Nó không viết lại nội dung.

## Vòng đời sản phẩm

| Gate | Output chính | Điều bị cấm trước khi qua gate |
|---|---|---|
| G0 — Product brief | phạm vi, audience promise, đối thủ | research tràn phạm vi |
| G1 — Premise lock | câu hỏi nhân quả và payoff | viết outline dài |
| G2 — Evidence ready | source index, claim ledger, contradiction map | viết prose như fact khi chưa đủ nguồn |
| G3 — Story lock | causal spine, chronology, chapter manifest | generate toàn bộ script |
| G4 — Chapter ready | brief riêng cho từng chapter | draft chapter chưa đủ evidence |
| G5 — Local approval | chapter được duyệt độc lập | tự sửa chapter khác |
| G6 — Integration approval | continuity, pacing, redundancy, payoff | coi ghép file là final |
| G7 — Delivery | script lắp ráp và manifest hash | sửa trực tiếp file đã lắp ráp |

Chi tiết nằm trong [`system/07-quality-gates.md`](system/07-quality-gates.md).

## Pilot

`products/sumer-writing/` là sản phẩm đầu tiên: lịch sử chữ viết trong nền văn minh Sumer. *Fall of Civilizations* là benchmark và đối thủ liền kề, không phải giọng văn hay cấu trúc để sao chép.

## Nguyên tắc thiết kế

- Một file có một nhiệm vụ biên tập rõ ràng.
- Mỗi chapter có ID ổn định; đổi tiêu đề không đổi ID.
- Claim lịch sử có ID và source trail riêng, không chôn trong prose.
- File đã khóa chỉ được sửa qua change request có impact analysis.
- `06_delivery/script.md` là build artifact; nguồn thật nằm ở các chapter riêng lẻ.
- Agent chỉ được sửa các đường dẫn trong `work-order.json`.

