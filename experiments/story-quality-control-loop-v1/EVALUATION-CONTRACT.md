# Evaluation Contract v1

## 1. Ba lớp không được bù điểm cho nhau

1. **Hard gates**: governance, factuality, outline fidelity, section boundary và anti-imitation.
2. **Story quality**: hiệu quả kể chuyện và nghe thành lời.
3. **System efficiency**: độ ổn định, usage, retry, latency và failure rate.

Một draft kể hay nhưng lệch outline, bịa detail hoặc vay cấu trúc đặc trưng của FoC là fail, bất kể score trung bình.

## 2. Hard gates

### G0 — Reproducibility

Pass khi có đủ:

- main/base SHA;
- work-order và protocol hash;
- frozen input hashes;
- candidate hash/text;
- model/effort/role topology;
- usage hoặc giá trị `unknown` trung thực;
- rubric/judge/benchmark hashes;
- validator output digest.

Score không có candidate hoặc evaluator artifact chỉ được ghi `historical_summary_only`.

### G1 — Evidence/factuality

- Zero unsupported hoặc contradicted critical/major claim.
- Tên riêng, số, ngày và quote: 100% khớp evidence được phép.
- Mọi detail mới có evidence ID, source và locator trong trace.
- Không đạt factuality bằng cách né required mission answer.
- Không browse để mở rộng truth ceiling; blocker quay về evidence authority.

### G2 — Outline fidelity

Không tạo story-plan/beat checklist mới. Đánh giá trực tiếp các invariants đã được phê duyệt:

- mission có được trả lời;
- entry state thực sự chuyển thành exit state;
- causal/intellectual direction không bị đảo;
- emphasis/thesis không bị thay bằng thesis mới;
- transition mở đúng nhu cầu của section sau;
- draft không viết hộ mission của section sau.

Pass khi zero hard violation và median `Outline Fidelity >= 8,5/10`.

### G3 — Anti-imitation

- Generator không được đọc FoC corpus hoặc evaluator scorecard.
- Distinctive matching run trên 14 token là hard fail trừ factual/source phrase bắt buộc.
- Matching run trên 10 token hoặc rare normalized 5-gram overlap trên 1% phải review.
- Hai câu liên tiếp cùng map vào một FoC passage, hoặc cùng hook mechanism + distinctive beat order + analogy/payoff sequence, phải fail structural review.
- Median `derivative resemblance <= 2/10`; hai trong ba judge chấm `>=3` là fail.

Lexical checker chỉ là signal; factual terminology chung không tự tạo violation.

### G4 — Governance/scope

- Changed paths là tập con exact allowlist.
- System và product prose không ở cùng cycle/commit.
- Worker/subagent không self-approve.
- Canonical task/replay đi qua CLI được repo quy định.

## 3. Story rubric

Judge chấm từng dimension 0–10, kèm defect tag và candidate-owned evidence span. Không chấp nhận score trần trụi.

| Dimension | Weight | Câu hỏi |
|---|---:|---|
| Hook + audience promise | 10% | Người nghe có biết điều đáng theo dõi và muốn tiếp tục không? |
| Narrative architecture + escalation | 15% | Section có movement, turn và tăng tiến, thay vì list kết luận không? |
| Causal/intellectual progression | 15% | Mỗi bước có làm phát sinh nhu cầu cho bước sau và dẫn tới thay đổi hiểu biết không? |
| Question/payoff chain | 15% | Câu hỏi được gieo, phát triển và trả đúng lúc không? |
| Concrete historical world | 10% | Evidence-supported vật thể, thao tác, nơi chốn hoặc quá trình có làm lịch sử hình dung được không? |
| Supported human/work orientation | 10% | Section có cho thấy việc con người phải làm/giải quyết trong giới hạn evidence, không bịa named anchor không? |
| Spoken clarity, rhythm, economy | 10% | Nghe một lần có hiểu, không report-mode, không caveat/repetition thừa không? |
| Payoff, continuity, transition | 10% | Kết luận có earned, giữ distinct section job và mở đúng câu hỏi tiếp theo không? |
| Voice/originality/audience fit | 5% | Có giọng riêng, không derivative, phù hợp kênh không? |

Anchor:

- `0–2`: hỏng hoặc vắng mặt.
- `3–4`: yếu, làm mất hiểu/mất hứng thú.
- `5–6`: dùng được nhưng còn kiểu giải thích thông thường.
- `7–8`: mạnh, ít lỗi đáng kể.
- `9`: xuất sắc và nhất quán.
- `10`: gần như không còn sửa đổi có giá trị trong scope.

`Raw human immediacy versus FoC` được ghi riêng như diagnostic. P01 không bị ép bịa named traveller, danger hoặc primary voice để đuổi raw score; gate dùng `supported human/work orientation` trong evidence affordance thực tế.

## 4. Blind paired evaluation

Hai comparison riêng:

1. Challenger vs current internal champion: đo thay đổi harness.
2. Challenger vs FoC matched reference: đo mục tiêu cuối.

Protocol:

- Hash và khóa comparator trước generation.
- Chuẩn hóa label/format; randomize A/B.
- Judge không biết writer, arm, score cũ hoặc hypothesis.
- Judge chọn `A`, `B` hoặc `tie`, rồi chấm dimensions độc lập.
- Ít nhất 20% pair được lặp với order đảo khi chạy promotion panel.
- Judge làm độc lập; lead không tham gia chấm.
- FoC evaluator trả score/defect taxonomy, không trả excerpt cho writer.

Primary preference metric:

```text
P_WE = mean(win + 0.5 * tie)
```

Không cộng số lượt judge thành sample độc lập; case/section mới là đơn vị chính.

## 5. Evaluation tiers

### T0 — Historical/forensic

- Có thể không còn candidate/rubric.
- Chỉ tạo hypothesis.
- Không dùng để claim quality.

### T1 — Diagnostic development

- Một frozen section, một A/B pair.
- Dưới ba blind judges chỉ được tạo diagnostic notes; không có pass decision.
- Với ba judge, vẫn chỉ là development signal.
- Pass hard gates.
- Median total `>=7,5`, không critical dimension `<7`.
- Majority win/tie vs internal champion.
- Critical dimensions ở tier này: causal progression, question/payoff, spoken clarity và outline fidelity.
- Winner chỉ được gọi `development_leader`; không thay internal champion cho tới independent replicate.

### T2 — Section calibration

- Fresh candidate + tối đa một diagnosed revision.
- Ba blind judges; order audit; judge disagreement range `<=1,5` trên critical dimensions.
- Mỗi production dimension median `>=8,0`.
- Không judge nào `<7` ở causal progression, question/payoff, spoken clarity hoặc outline fidelity.
- Majority của panel win/tie vs FoC matched reference.
- Tất cả hard gates pass.
- Chỉ gắn `section_calibrated`.
- Model tier/family, candidate count, retries và usage phải kiểm chứng được; `unknown` làm tier này fail reproducibility.

### T3 — Reusable harness promotion

- Tối thiểu 24 matched cases qua nhiều section/product, hoặc sample size khác được power analysis và người dùng khóa trước generation. P01 + hai section chỉ đủ `single-product provisional`.
- Ba judge/case và locked promotion set.
- Report median, p10, gate-failure rate và tokens per passing script.
- Ít nhất 95% outputs pass hard gates; zero critical outline/evidence violation.
- Không stratum/section type regression nghiêm trọng.
- Blind non-inferiority vs FoC ở matched set; không tuyên bố toàn hệ thống từ một P01.
- Model tier/family, candidate count, retries và usage phải kiểm chứng được; `unknown` làm tier này fail reproducibility.

Khi chưa đủ sample, kết quả phải mang nhãn `single-product provisional` hoặc `single-family provisional` và không được canonical-promote reusable harness.

## 6. Calibration và disagreement

Trước promotion:

- Calibration set có obvious defect, close call, outline trap và factual trap.
- Gold-direction accuracy `>=85%`.
- Duplicate consistency `>=85%`.
- Reversed-order consistency `>=80%`.
- Position bias `<=5` percentage points.
- Median anchor-score error `<=0,75`.
- Evidence-span validity `>=90%`.

Nếu hơn 35% case không có majority, hoặc within-case score SD `>1,5`, kết quả là `INCONCLUSIVE`. Không average để che disagreement.

## 7. Cost-aware sequential testing

Funnel:

1. `S0`: schema, provenance, evidence, outline, boundary và imitation gates.
2. `S1`: một development A/B pair để loại treatment hỏng rõ.
3. `S2`: replicate chỉ khi S1 inconclusive và planner cho phép.
4. `S3`: sealed promotion panel chỉ cho candidate đã qua development.

Không promote sớm từ dev score. Nếu thử nhiều variant trên cùng holdout, phải ghi submission count; tối đa ba submission trước khi rotate holdout.

## 8. Promotion rules

### Provisional internal champion

- Tất cả hard gates pass.
- `P_WE` point estimate vs champion `>=0,55`.
- Median story delta `>=+0,2`.
- Không critical dimension giảm hơn `0,3`.
- Cùng budget tier hoặc treatment được gắn tier cao hơn.

### Claim “ngang FoC”

Đơn vị phân tích là matched case/section. Ba judgment trong cùng case được aggregate thành một case result trước khi tính interval; không coi ba judge là ba sample độc lập. Mặc định dùng clustered bootstrap theo case và one-sided 95% lower confidence bound, trừ khi C010 khóa một estimator hợp lệ khác trước generation.

Chỉ dùng khi locked matched set cho thấy đồng thời:

- `P_WE(candidate, FoC) >=0,50` point estimate;
- one-sided 95% lower bound của `P_WE` `>0,45` (non-inferiority margin `0,05` quanh parity `0,50`);
- story delta point estimate `>=0` và one-sided 95% lower bound `>-0,30/10`;
- tất cả hard gates pass;
- không section type regression nghiêm trọng;
- panel không chỉ là cùng một model family, hoặc có human audit bổ sung.

Nếu sample chưa đủ cho confidence interval, dùng câu: `chưa có bằng chứng thua FoC trên calibration set`, không dùng `ngang FoC`.

C010 phải khóa comparator matching, analysis unit, estimator/CI method, margin và judge aggregation trước generation. Thiếu trường nào thì kết quả bắt buộc `inconclusive`.

## 9. System fairness

- So cùng source/outline, model tier và budget policy.
- Khóa candidate count, retry policy và selection rule.
- Timeout/fail vẫn tính vào system failure rate.
- Nếu treatment dùng senior editor hoặc nhiều subagent hơn, toàn bộ usage đó thuộc treatment.
- Không chọn best-of-many rồi so với single baseline mà bỏ chi phí selection.
