# Task report — T0034-review-section-P01

## Result

- Operation: `review_section`
- Section: `P01`
- Verdict: `changes_requested`
- Review contract: v2
- Scope: chỉ ba allowed write paths của work order

## Review outcome

Hai required outcome questions đều đạt: audience có thể trả lời mission bằng lời của mình và có thể retell historical path từ token/bulla qua dấu bề mặt, bảng số, formation ecology và institutional pressure. Mission/exit, adjacent boundary và one-hearing narration đều pass.

`evidence_integrity` fail ở một câu duy nhất: draft chắc hóa rằng token bên trong và dấu ngoài bulla giữ “cùng một lượng”. Approved source detail cho biết token tạo dấu ngoài không nhất thiết là token nằm trong envelope. Vấn đề được route tới `evidence`; revision scope nhỏ nhất là câu đó và tối đa câu liền kề. Không có yêu cầu rewrite cấu trúc hay benchmark-style prose.

## Evidence activity

- `resolve_claims`: thành công cho 8 claim (`CLM-0011`–`CLM-0018`), 6 approved sources; `truth_ceiling_unchanged: true`.
- `SRC-0001`, pp. 24–27: xác minh Uruk 200 hectare / population xấp xỉ 40.000+ và dấu token ngoài bulla phù hợp với numerical signs sớm; chi tiết đã `record`.
- `SRC-0011`, pp. 6–9: xác minh Tushan coexistence và qualification rằng impressed tokens không nhất thiết là contents của bulla; chi tiết đã `record`.
- Không dùng nguồn ngoài allowlist và không đưa claim mới vào review.

## Production gate

- Hard gates: evidence integrity `fail`; mission and exit `pass`; adjacent boundary `pass`; one-hearing narration `pass`.
- Dimensions: 8–9/10; không dimension nào dưới 8.
- Derived verdict: `changes_requested` theo contract v2.

## Validation

- Task verification: pass (`Task packet is fresh and within budget`).
- Product validation: pass, do operator xác minh.
- Scope validation: pass trên baseline sạch trước submit, do operator xác minh.
- Review output contract: pass sau khi chuẩn hóa exact verdict và required headings.
- Submit/approve/commit: không thực hiện theo yêu cầu.
