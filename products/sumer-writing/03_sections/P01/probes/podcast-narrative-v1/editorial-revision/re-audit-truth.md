# P01 Revised Probe — Separated Historical Truth Re-Audit

Status: `TRUTH_VERDICT_FROZEN_FAIL_HIGH_RISK`

## Stage identity and execution boundary

- stage: `TRUTH_AUDIT`
- execution parent: `09fbb8c0aae32a2c273bf38c11cf078d4e53beec`
- prerequisite: Product Review already committed and frozen in the parent history
- auditor role: Historical Truth Auditor
- model/config identity: not exposed by the GitHub connector; current ChatGPT review session
- independent model instance: **not verifiable / not available in this execution surface**
- procedural isolation: adjudication below is restricted to the truth packet listed here; the frozen Product verdict is not used to support, repair, upgrade or downgrade any truth finding

This artifact does not claim stronger evaluator independence than Git can prove. It does establish a separate immutable commit boundary after the Product Review.

## Exact input packet

1. Unchanged raw sample
   - file: `editorial-revision/revised-probe.md`
   - blob: `c44a417ad2a92c1d6df9c24042e4a88f9b8f725c`
   - measured prose word count excluding title: `860`
2. Writer-facing bounded notebook
   - file: `writer-notebook.md`
   - blob: `98198175c783931e8ca32a84d69e08df8a0b4064`
3. Notebook authority / ceiling notes
   - file: `notebook-authority.md`
   - blob: `97206a404499955ff5f044728a27b8318ddcd5f6`
4. Approved P01 material authority required for bindings
   - file: `products/sumer-writing/03_sections/P01/materials.json`
   - blob: `d1fe747395991d96cf9ae93d00c7af38b002650d`
   - records used: `P01-MAT-0001` through `P01-MAT-0007` where explicitly identified below
5. Approved P01 Historical Substrate
   - file: `products/sumer-writing/03_sections/P01/historical-substrate.json`
   - blob: `5d90cea0b398a1421e2a0932595388937380a8e6`
   - records used: `HS-P01-0001`, `HS-P01-0003`, `HS-P01-0004`, `HS-P01-0007`, boundaries `HSC-P01-0001`, `HSC-P01-0003`

## Explicitly excluded from adjudication

- Product Editor verdict or FoC prose
- prior truth-audit conclusions
- Writer self-report
- external archaeological knowledge
- web research
- any source not already bound through the approved P01 authority above

Missing binding is a finding. It must not be repaired with plausible outside knowledge.

---

# Executive truth verdict

**TRUTH VERDICT: `FAIL — HIGH_RISK`**

The revision successfully removes several surface forms of the original Round-1 errors, but it introduces or retains multiple unsupported relationships and causal claims. The most serious problems are not the existence of the entities named; they are the **relationships, motives, functions, consequences and sequences attached to those entities**.

Core rule applied throughout:

```text
attested entity/practice
≠ attested motive
≠ attested causal origin
≠ attested consequence
≠ attested transaction
≠ attested historical sequence
```

The revised passage cannot receive `LOW_RISK` or `0 Epistemic Overreach` under the approved authority ceiling.

---

# Claim-binding table

| # | Exact draft claim | Claim type | Authority binding and authority wording | What is actually supported? | Verdict |
|---|---|---|---|---|---|
| 1 | “những vật thể đất sét… viên bi… hình nón, đĩa dẹt hay ống trụ… một đến hai centimet” | entity / physical description | `P01-MAT-0001 > object_or_trace / physical_description / measurement`: small geometric clay forms; generally 1–3 cm; some plain/incised. | Entity, morphology and hand scale. | `SUPPORTED` |
| 2 | “những mẩu đất này… là những đại lượng, những con số có thể cầm nắm được” | function / representativeness | `P01-MAT-0001 > functional_inference`: **some Late Uruk examples** participated in numerical or administrative practices; qualification rejects a universal code. | Bounded numerical/administrative use for some Late Uruk examples, not a universal shape→quantity code. | `QUALIFIED_INFERENCE / OVERSTATED AS WRITTEN` |
| 3 | “Khi các đô thị Uruk mở rộng, dòng chảy ngũ cốc, đàn gia súc hay ngày công lao động dần vượt khỏi tầm bao quát… Người ta cần… neo giữ thông tin bên ngoài trí nhớ.” | causal origin / institutional pressure / motive | No approved P01 record binds urban expansion to biological-memory overload or states that such overload caused the need for the recording practices. `notebook-authority.md` explicitly licenses no undocumented causal events. `HS-P01-0001` documents coexisting clay practices handling quantities/authentication, not their cause. | Administrative practices and quantity handling exist; the proposed urban-growth→memory-overload→need chain is not bound. | `PROHIBITED / UNSUPPORTED CAUSAL CLAIM` |
| 4 | “Khi các đại lượng cần được chuyển giao hay lưu giữ trọn vẹn trong giao dịch… bọc kín các con tính” | motive / transaction mechanism / function | `P01-MAT-0002 > observed`: hollow envelopes contain tokens and bear impressions/seals. `representative_reconstruction`: operator deposits counters, closes, marks/seals, dries. `prohibited_or_rejected_inference`: artifacts do not establish a single motive. Notebook says exact transaction/motive usually does not survive. | Manufacture and enclosure practice. No binding that transfer/preservation in transactions was the general reason the envelope was used. | `UNSUPPORTED RELATIONSHIP / MOTIVE` |
| 5 | “dàn mỏng… miết liền, vo tròn thành một phong bao…” | representative reconstruction | `P01-MAT-0002 > representative_reconstruction`: deposit counters, close envelope, mark/seal, dry; notebook permits ordinary bounded reconstruction. | Enclosing and closing moist clay is supported; exact flattening/seam-smoothing technique is not separately documented in the supplied binding. | `QUALIFIED_INFERENCE` |
| 6 | “Chừng nào phong bao còn lành lặn, sự toàn vẹn của tập hợp vật đếm được bảo đảm.” | function / guarantee | `P01-MAT-0002` and `HS-P01-0003` support hidden/non-directly-inspectable contents and destructive opening. They do **not** state an absolute guarantee of integrity or anti-tamper security. | Closed contents are not directly visible; opening destroys sealed state. | `UNSUPPORTED OVERSTRONG FUNCTION` |
| 7 | “muốn kiểm tra… buộc phải đập vỡ… phải phá hủy” | object affordance / consequence | `P01-MAT-0002 > limitations`: opening to inspect permanently destroys sealed envelope. `HS-P01-0003`: contents not directly inspectable while closed. | Destructive inspection of enclosed contents. | `SUPPORTED` |
| 8 | “Để xác nhận tính chính danh… dùng một con dấu…” | motive / institutional function | `P01-MAT-0003 > functional_inference`: seal impressions marked **an association with authority, custody or witnessing**, with no unique event/speaker. | Association with authority/custody/witnessing. “Tính chính danh” as the purpose is not bound. | `UNSUPPORTED FUNCTION / MOTIVE` |
| 9 | “vết tích… của quyền giám sát, của việc làm chứng và ràng buộc trách nhiệm trong cộng đồng” | institutional relationship / consequence | `P01-MAT-0003` permits association with authority, custody or witnessing. It does not bind “supervisory rights” or communal responsibility/accountability. | Authority/custody/witness association only. | `PARTLY SUPPORTED; EPISTEMIC OVERREACH` |
| 10 | “Trên một số phong bao… vết ấn ngoài… số lượng… Nhờ vậy… nhận biết đại lượng mà không cần đập vỡ” | functional inference | `P01-MAT-0002 > functional_inference`: exterior marks made enclosed quantities inspectable without immediately opening; `HS-P01-0003` requires “some examples”. | This exact bounded affordance, with subset qualification. | `SUPPORTED AS QUALIFIED INFERENCE` |
| 11 | “Bề mặt đất sét bắt đầu vượt khỏi vai trò vỏ bọc, trở thành nơi mang thông tin đọc được trực tiếp từ bên ngoài.” | historical change / interpretation | `HS-P01-0007`: qualified shift in physical placement/inspectability, with numerical information increasingly appearing directly on durable clay surfaces while older practices overlap. | A qualified change in where information resides and is inspectable. “Bắt đầu” must not be read as a direct genealogical step caused by envelopes. | `QUALIFIED_INFERENCE` |
| 12 | “Song hành với… phong bao… người ta còn sử dụng… phiến đất số đặc.” | coexistence / entity | `P01-MAT-0004 > representativeness`: numerical tablets attested before/alongside pictographic tablets; direct genealogy not established. `HS-P01-0001/0004/0007`: multiple practices overlap. | Coexistence and numerical surface recording. | `SUPPORTED` |
| 13 | “Đầu que sậy vát… ấn… những lỗ tròn… biểu thị các con số.” | tool reconstruction / function | `P01-MAT-0004`: impressed marks record numerical information. `P01-MAT-0006`: reed tools **likely** produced these marks; tool morphology reconstructed because organic tools rarely survive. | Numerical impression is supported; reed-tool morphology is an inference, not directly observed fact. | `QUALIFIED_INFERENCE / EPISTEMIC STATUS OMITTED` |
| 14 | “con dấu… chứng thực cho quyền giám sát” | institutional function | `P01-MAT-0003`: association with authority, custody or witnessing; no unique event. `P01-MAT-0004`: some tablets carry seal rollings. | Seal rolling may be present and associated with authority/custody/witnessing. “Chứng thực quyền giám sát” is stronger. | `UNSUPPORTED OVERSTATEMENT` |
| 15 | “Trong các phế tích… phong bao… nằm cạnh… phiến đất… cùng… niêm phong… trên miệng bao tải hay then cửa kho.” | spatial relationship / sealing context | `HS-P01-0001` supports coexistence, not literal adjacency. `P01-MAT-0007` supports clay sealings over closures with cord/cloth/wood impressions, including institutional storehouse contexts and door pegs/covered containers. | Coexisting assemblage families and closure sealings. Literal “nằm cạnh” and every named closure form are not established by the substrate alone. | `PARTLY SUPPORTED; SPATIAL OVERCLAIM` |
| 16 | “Có những việc… bọc kín… lại có những giao dịch… ghi thẳng dấu số…” | transaction assignment / practice | `HS-P01-0001/0004` supports multiple administrative practices and direct numerical surface recording. `HSC-P01-0003` forbids assigning specific economic mechanisms without independent transaction evidence. `P01-MAT-0004` does not identify a specific transaction mechanism. | Generic administrative use and numerical recording; no binding for the contrast as specific “transactions”. | `QUALIFIED AT BEST; UNSUPPORTED TRANSACTION FRAMING` |
| 17 | “Thông tin số lượng… có thể phơi bày trực tiếp trên mặt phẳng bền vững… kiểm tra mà không… phá hủy” | object affordance / change | `HS-P01-0004`: numerical tablets place quantity information directly on durable exterior surfaces. | Direct exterior numerical information; unlike enclosed contents it does not require opening a hollow container. | `SUPPORTED` |
| 18 | “sự tái định hình… từ… vật thể… trong lòng đất kín, đến… bề mặt đất sét… số… ngoài trí nhớ” | historical change / synthesis | `HS-P01-0007` supports a qualified change in placement/inspectability and coexistence, not one mandatory genealogy. Durable records existing outside immediate recollection is a reasonable description of external material storage, but no authority here establishes a social memory crisis. | Placement/inspectability shift if explicitly kept non-linear and coexistent. | `QUALIFIED_INFERENCE` |
| 19 | “khi những đô thị Uruk tiếp tục phình to, với hàng ngàn giao dịch phức tạp cần theo dõi, bề mặt… sẽ sớm không chỉ dừng lại ở những con số.” | causal sequence / forecast / origin of expanded writing | `P01-MAT-0005` supports existence of later Uruk IV tablets combining numerals and pictographic signs. It does **not** bind city growth or “thousands of transactions” as the cause of that development. `HSC-P01-0001` and notebook authority prohibit undocumented causal sequence/genealogy. | Later richer sign surfaces exist; the proposed growth/transaction-pressure→beyond-numbers causal bridge is not supported. | `PROHIBITED / UNSUPPORTED CAUSAL SEQUENCE` |

---

# Hard findings

## A. Replacement causal story remains

The old anti-tampering story was removed, but the passage now opens and closes with a different unsupported engine:

```text
Uruk urban expansion
→ flows exceed human oversight/memory
→ external material record becomes necessary
→ growing transaction complexity
→ clay surface soon advances beyond numbers
```

The approved authority documents the practices and a qualified material change. It does not bind this causal origin or forecast mechanism.

This is a substantive truth failure, not a line-level wording issue.

## B. Entity evidence is repeatedly used as relationship evidence

The passage names attested categories—grain, livestock, labor, envelopes, seals, numerical tablets, authority, witnessing—and then attaches stronger relationships:

- necessity;
- transaction transfer/preservation;
- guaranteed integrity;
- legitimacy;
- supervisory rights;
- communal responsibility;
- causal pressure toward more complex writing.

Those relationships require their own binding. Their component nouns being historically plausible or attested does not supply it.

## C. Some valid inferences are narrated as observed fact

The clearest example is the reed tool. `P01-MAT-0006` treats tool morphology as reconstructed from marks because organic implements rarely survive. The prose narrates a bevelled reed as a direct fact. This is repairable by preserving the inference status, but it contributes to the overall epistemic overreach.

## D. The coexistence correction is real but insufficient

The passage does correctly state that envelopes and numerical tablets coexist and rejects a simple unilinear ladder. That repair is supported by `HS-P01-0001`, `HS-P01-0004`, `HS-P01-0007`, and `HSC-P01-0001`.

However, an explicit coexistence disclaimer does not neutralize unsupported causal claims elsewhere in the passage.

---

# Frozen truth verdict

`revised-probe.md = FAIL — HIGH_RISK`

Minimum classification:

- hard/prohibited causal problems: **2 major** (#3 and #19)
- unsupported motive/function/relationship claims: **multiple** (#4, #6, #8, #9, #14, #16)
- qualified inferences stated too strongly: **multiple** (#2, #5, #11, #13, #18)
- supported core material facts and coexistence: **substantial but insufficient to clear the passage**

This is not a repair brief. No Writer action is authorized by this audit.

## Audit metadata

- raw sample rechecked unchanged at input: `c44a417ad2a92c1d6df9c24042e4a88f9b8f725c`
- measured prose word count: `860`
- product verdict used as authority: **no**
- external archaeological knowledge used: **no**
- missing relationship bindings treated as blockers/findings: **yes**
- review order: correction commit → frozen Product Review commit → this Truth Audit commit → synthesis not yet run
