# Anchor check — C010-R/A1 (forensic gold recovery)

## 1. C1 binding đúng là gì?

- **Candidate cũ:** blob `7dcc1033cc76a61ae85a04bd699e9494d56f94cf` (commit `246e4a0`, 19/08 17:35).
- **Candidate mới ("bản draft mới thêm ở commit 324bc8f"):** commit đầy đủ `324bc8f928824123bb6d5bfbc57ca2c69015c99f` — "Draft C003 P01 with writer-authorship harness", 20/08 15:08:47 +07:00; blob P01 draft tại commit đó **= `ceee1b9bb2f0813088b8a8a595ee22826f57f006`** (resolve chính xác).
- **Binding cũ của C010 (`3424c985…`) là sai**: blob đó sinh tại `c3daaa3` "Rewrite P01 from bounded evidence" lúc **23:27 ngày 20/08 — sau verdict ~8 tiếng**, không thể là bản user đã chấm. Đã đánh dấu rejected, không giữ làm human gold.
- Tính duy nhất: tại thời điểm verdict chỉ tồn tại đúng một ứng viên "mới" → binding `7dcc1033` vs `ceee1b9b` là duy nhất và đúng thứ tự thời gian.

## 2. Có bao nhiêu human ordinal gold hợp lệ?

**0.** Turn gốc `75be696a-d549-4783-b5cc-c2acfeac77b2` không đọc được trong runtime này (4/4 retained thread ID vắng mặt trong session DB; discovery sweeps chỉ trả về các session không liên quan) → C1 mang nhãn **`unusable_in_runtime`** theo đúng quy tắc của lượt. Planner attestation KHÔNG được dùng để giả lập human gold. Binding sửa lỗi đã freeze trong registry để anchor tự chuyển đổi dùng được ngay khi raw turn đọc được mà không phải hỏi lại user.

## 3. Có bao nhiêu verdict vs FoC hợp lệ?

**0.** Không tìm thấy bất kỳ verdict nào của user so candidate với FoC có thể bind thread+turn+blob.

## 4. Những anchor nào bị loại và vì sao?

| Anchor | Lý do loại |
|---|---|
| C010 legacy binding `3424c985` | sai thời gian (postdates verdict ~8h); `binding_incorrect_for_verdict_timestamp` |
| Checkpoint report 8.1 (turn `3fb89399`) | checkpoint/self-reported score, không có candidate blob |
| Lost-artifacts turn (`b6320753`) | artifacts đã mất, không có blob để bind |
| run-01..05 history | machine score / self-review, never gold |
| System/lifecycle thread | không phải quality evidence |
| A4 G2-vs-H2 | không tồn tại verdict user ở bất kỳ đâu (kể cả attestation) — vẫn chỉ là diagnostic |
| Planner attestations nói chung | bản ghi thứ cấp, không mô phỏng được human gold |

A2 "cỡ bàn tay": chi tiết **có nguồn thật** trong pack (CRR-02/SRC-0023, locator đã review) → không bao giờ là unsupported-factual gold; keep/remove của user chỉ là thẩm quyền biên tập. **Retire khỏi factual calibration pool** và không hỏi user về việc này trong checkpoint A1.

## 5. Sau khi exhaust history, có thật sự cần user cung cấp thêm gold không?

**Có.** Đã exhaust mọi đường đọc khả dĩ cho cả bốn retained thread trong runtime này (exact-ID read, full browse, nhiều discovery sweep, filename scan) — runtime hiện tại không chứa raw turns.

## 6. Nếu cần, cần chính xác bao nhiêu verdict và loại nào?

Tối thiểu **3**, tất cả phải là *user-authored*, bind exact thread/turn/timestamp + blob hai phía:

1. **Ordinal cặp P01 sửa-C1** — giữa `7dcc1033` (cũ) và `ceee1b9b` (mới @324bc8f); phạm vi: direction-only, non-blind, ~3→5–6 nhưng vẫn trung bình; cấm numeric calibration/FoC parity. *(Nếu user cung cấp lại nguyên văn turn `75be696a` đọc được thì mục này tự thỏa, không cần chấm lại.)*
2. **Ordinal G2 vs H2** — `521ded0d` vs `4e75f451` (đóng close_call #2).
3. **Một verdict vs FoC comparator** — một trong hai ứng viên trên so với blob `391febd843f0d99a8ba3730ae447b4e2eefb9061` (đóng luôn khoảng trống "human blind verdict vs FoC" nếu trình bày blind).

---
*Subagents: thread_verdict_mapper + artifact_linker (read-only, deleg_a47604a6). Worker lead độc lập xác minh toàn bộ git binding trước khi ghi.*
