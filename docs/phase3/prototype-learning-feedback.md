Review prototype learning — branch codex/p01-phase3-whitebox-mvp

Trạng thái: **OWNER-ACCEPTED FEEDBACK / WORKER IMPLEMENTATION PENDING**.
Vai trò triển khai tiếp theo: `system_architect`. Owner đã yêu cầu bổ sung workspace vật lý và giới hạn đọc/ghi theo role trước khi commit feedback này. Commit hiện tại chỉ ghi feedback và entrypoint, chưa triển khai enforcement hoặc cho chạy một production round mới.

Commit được review: `38a41e369bd8b03e5a8b3c67c4c92cd674289940`, fetch từ remote trong phiên review này. So sánh với mốc `0751c9f` trước sửa. Kiểm thử trên snapshot riêng; không sửa repo hoặc product, không gọi Writer/Planner và không ghi owner measurement thật.

**Kết luận:** chấp nhận bản sửa làm nền kỹ thuật cho prototype. Phạm vi tiếp theo gồm hai nhóm lỗi feedback dưới đây, một brief chung, và workspace được giới hạn quyền cho từng role theo yêu cầu owner. Không nên mở thêm đợt hoàn thiện kiến trúc trước khi có một vòng Plan–Writer–review thật.

**Phần đã đạt và nên giữ**

- 33 focused tests pass; unittest báo 2,408 giây trên máy Windows này.
- Benchmark verifier pass với trạng thái `ARCHITECTURE_FROZEN_READY_FOR_PILOT`.
- Cả guided pilot và comparison Phase 3 pass structural/source checks, vẫn ghi đang chờ owner.
- Case B03 prepare được, verify hợp lệ, chưa có measurement thì không nhận improvement.
- Mapping kiểm tra candidate thật, bắt quote rỗng/mơ hồ và field thiếu; có snapshot/hash; mapping certainty và attribution certainty đã tách.
- Nhận xét hợp lệ mới làm feedback đổi; stale candidate/scope bị từ chối; có focused CI riêng.

Đây là bằng chứng nền kỹ thuật đã tốt hơn. Nó chưa chứng minh Plan team, Writer, reviewer và auditor đã dùng cùng tiêu chuẩn trong một lần làm việc độc lập. Runtime vẫn dùng fixture lịch sử và manual B03 output, đúng giới hạn worker được giao.

**1. [P1] Quy tắc diễn giải feedback làm lệch điều người đánh giá thực sự nói.**

[feedback.py:373](https://github.com/romanviper/yt-production/blob/38a41e369bd8b03e5a8b3c67c4c92cd674289940/learning_runtime/feedback.py#L373) chuyển owner result trực tiếp thành symptom delta và next action.

Đã tái hiện bằng measurement `TEST_ONLY`, không dùng owner label:

| Input | Output hiện tại | Vấn đề |
|---|---|---|
| `UNCERTAIN` | delta `UNCERTAIN`, action `REJECT_OR_REVISE_BOUNDED_INTERVENTION` | Chưa biết bị biến thành chỉ thị sửa, dễ sinh thêm thay đổi không có căn cứ. |
| `YES` cho câu hỏi “AFTER có tiến gần trải nghiệm kể chuyện mong muốn không?” | `DIRECTIONALLY_REDUCED_NOT_RESOLVED` cho symptom | Thích hơn có thể vì một lý do khác; chưa chứng minh `EXPLANATION_BEFORE_NEED` giảm. |
| `YES` nhưng không gửi invariants | `invariant_state: {}` | Các mục Truth/continuity chưa đo ở case bị mất khỏi output feedback. |

Sửa tối thiểu: giữ riêng preference và symptom observation; thiếu đánh giá symptom thì ghi chưa đo. `UNCERTAIN` dẫn tới làm rõ/thu thập thêm quan sát, giữ nguyên can thiệp. `WRONG_TARGET` quay lại định nghĩa mục tiêu thay vì mặc định sửa Writer/Plan. Invariants vắng trong measurement phải kế thừa trạng thái chưa đo của case. Không cần thêm evaluator hoặc rubric mới; vài nhánh quyết định và test tương ứng là đủ.

**2. [P1] Nhận xét lần sau xóa mất dấu vết nhận xét lần trước.**

[feedback.py:436](https://github.com/romanviper/yt-production/blob/38a41e369bd8b03e5a8b3c67c4c92cd674289940/learning_runtime/feedback.py#L436) luôn ghi `measurement.json` và `feedback.json`, rồi tính lại bundle.

Probe nhập lần lượt `UNCERTAIN`, `YES`, `NO`: cuối cùng chỉ còn một `measurement.json` chứa `NO`, bundle vẫn `VALID`. `case.json` vẫn `AWAITING_MEASUREMENT`, còn `feedback.json` là `MEASUREMENT_INGESTED`.

Điều này dễ xảy ra trong tình huống bình thường: owner bổ sung ý kiến hoặc hai reviewer bất đồng. Nếu kết quả trước bị ghi đè, vòng sau có thể tưởng ý kiến cuối là toàn bộ bằng chứng, làm lịch sử học mất căn cứ.

Sửa tối thiểu cho prototype: từ chối ghi đè measurement đã nhận; nhận xét sửa đổi dùng file/ID mới có `supersedes` hoặc liên kết với bản trước. Chỉ định một trạng thái hiện tại để `show` đọc nhất quán. Không cần event bus, database hay framework audit mới.

**Một chỉnh nhãn nhỏ đi kèm:** [whitebox.py:263](https://github.com/romanviper/yt-production/blob/38a41e369bd8b03e5a8b3c67c4c92cd674289940/learning_runtime/whitebox.py#L263) ghi authority `INTERVENTION_SUPPORTED_HYPOTHESIS` ngay khi chưa có measurement can thiệp. Trong probe, nhãn này đã xuất hiện trước khi nhận nhận xét nào. Đổi về reviewer/diagnostic hypothesis; chỉ nâng mức bằng chứng khi có can thiệp được đo. Không cần mở rộng bộ máy suy luận.

**Khoảng trống đối với mục tiêu “một thước đo, một tiêu chuẩn, một tầm nhìn”**

Repo đã có chuẩn chung về mặt tài liệu: [Output Quality Contract v1.3](https://github.com/romanviper/yt-production/blob/38a41e369bd8b03e5a8b3c67c4c92cd674289940/docs/quality/output-quality-contract.md), taxonomy và target profile. Không nên tạo thêm chuẩn cạnh tranh.

Nhưng [prepare_case](https://github.com/romanviper/yt-production/blob/38a41e369bd8b03e5a8b3c67c4c92cd674289940/learning_runtime/feedback.py#L279) mới nối các input B03 cố định. Case đóng băng candidate/Plan/intervention, chưa tham chiếu rõ phiên bản contract/target profile dùng cho quyết định. Chưa có một lượt Planner, Writer và reviewer mới thực thi để kiểm tra sự hiểu chung. Đây là khoảng trống bằng chứng, không phải lý do xây thêm platform hoặc đòi chứng nhận evaluator trước vòng đầu.

Chỉ cần một brief của vòng học, dùng lại contract hiện có, chứa:

1. Mục tiêu trải nghiệm người nghe và chức năng đoạn đang thử.
2. Một defect/criterion cụ thể; dấu hiệu nào được tính là giảm, không giảm hoặc chưa biết.
3. Baseline, phần được thay đổi và evidence ceiling cụ thể.
4. Các điều phải giữ: Truth, độ rõ của vật thể và chuyển tiếp trong phạm vi thực sự được đo.
5. Contract/target version hoặc hash; cách xử lý preference, uncertainty, disagreement và quyết định sau review.

Mọi vai trò dùng cùng phần mục tiêu/tiêu chuẩn đó. Dữ liệu nhận được vẫn khác theo nhiệm vụ: Product reviewer không nhận Plan, trace, attribution hay đáp án mong muốn trước khi đánh giá. Chuẩn chung không có nghĩa là làm mù ranh giới black-box/white-box.

**Vòng đầu nên dùng để chứng minh điều gì**

- Có thể điều phối thủ công các agent, không cần live-execution adapter mới. Mỗi role nhận mục tiêu chung và input đúng quyền; không đọc toàn bộ lịch sử.
- Planner đề xuất một thay đổi có dự đoán observable; Writer hiện thực dưới cùng evidence ceiling; reviewer đánh giá output theo tiêu chí đã freeze; auditor chỉ truy ngược sau khi có lỗi/uncertainty.
- Trước thực thi, mỗi role nêu ngắn mục tiêu quan sát và giới hạn của mình bằng cùng criterion ID. Đây là kiểm tra cách hiểu, không phải tự chứng nhận chất lượng.
- Một quyết định cuối trích đúng observation/measurement, giữ bất đồng và phân biệt “người nghe thích hơn”, “symptom giảm”, “giả thuyết nguyên nhân được hỗ trợ”. Tất cả phải áp dụng cùng rule đã freeze.
- Một vòng âm tính hoặc inconclusive vẫn là learning thành công nếu nó cho biết giả thuyết nào chưa được hỗ trợ và không làm hệ thống tự thêm luật/prompt toàn cục.
- Chỉ sửa lại architecture khi vòng thật bộc lộ một điểm cụ thể ngăn thực thi hoặc làm mất bằng chứng. Tactic thử nghiệm ở phạm vi case; không biến một phát hiện B03 thành quy tắc chung cho mọi đoạn.

Kết quả của một vòng không thể chứng minh mọi agent tương lai sẽ luôn hiểu giống nhau. Nó có thể cung cấp bằng chứng kiểm tra được rằng các role trong vòng đó thực sự dùng chung chuẩn, thay vì chỉ cùng nhắc tên một file.

**Yêu cầu owner bổ sung: workspace vật lý theo role**

Mỗi role có cấu trúc workspace cố định, mỗi execution có thư mục riêng để không lẫn dữ liệu giữa các vòng. Writer không có quyền repo-wide chỉ vì được giao viết; auditor không được sửa output mà nó đang audit. Áp dụng cả cho reviewer, Truth và agent sửa hệ thống. Vai trò điều phối thực hiện handoff qua output đã kiểm tra; các agent không tự đọc/ghi workspace của nhau.

Prototype dùng một workspace root ngoài checkout production, hoặc một root riêng đã bị giới hạn truy cập tương đương. Ví dụ bố cục vật lý do launcher tạo:

```text
<workspace-root>/<run-id>/
  control/                         # launcher/operator only
    role-policy.json
    frozen-standard.json
    handoffs.jsonl
    access-events.jsonl
    measurements/                  # owner/reviewer records, immutable versions
  agents/
    plan/<execution-id>/
      input/                       # read-only, packet + role-safe common brief
      output/                      # role may write here
      scratch/                     # role-local temporary work
    writer/<execution-id>/{input,output,scratch}/
    truth/<execution-id>/{input,output,scratch}/
    review/<execution-id>/{input,output,scratch}/
    audit/<execution-id>/{input,output,scratch}/
```

Các dòng `{input,output,scratch}` là ký hiệu rút gọn cho ba thư mục, không phải tên thư mục literal. Mỗi reviewer có execution riêng. Không tái sử dụng một workspace mutable cho các vòng khác nhau. Không tạo thêm các role này chỉ để lấp đầy sơ đồ; chỉ materialize role thực sự được dùng trong vòng đã giao.

| Role | Được đọc trong input của mình | Được ghi | Không được truy cập trực tiếp |
|---|---|---|---|
| Plan | Brief chung đúng phiên bản, evidence được duyệt, baseline/context và feedback được chọn cho vòng này | Plan, dự đoán observable và declared decisions trong output; scratch riêng | Workspace Writer/review/audit, toàn repo, research ngoài evidence ceiling |
| Writer | Brief chung, Plan đã được handoff/duyệt theo checkpoint, evidence và context tối thiểu | Prose, mapping/deviations và report trong output; scratch riêng | Review/verdict, owner labels, audit hypotheses, Plan nguồn để sửa, product state |
| Truth | Một candidate đã freeze, historical authority được duyệt và Truth contract | Claim audit và limitations trong output; scratch riêng | Product preference, FoC craft evidence, Writer/Planner process |
| Product review | A/B đã ẩn danh, role-safe common goal và frozen Product criteria | Preference, confidence và output-grounded observations trong output; scratch riêng | Plan, trace, attribution, nhãn old/new/expected winner; FoC/diagnostic target chỉ được cấp trong lượt post-vote/guided riêng |
| Audit | Sau output failure/uncertainty: bounded case bundle gồm các bản sao Plan/Writer/evidence/measurement liên quan và chuẩn chung | Diagnosis, broken edges và đề xuất can thiệp trong output; scratch riêng | Sửa source prose, sửa verdict/measurement/standards, tự mở toàn bộ lịch sử |
| System architect / repair worker | Checkout hệ thống riêng và case bundle cần để tái hiện defect được giao | Chỉ file hệ thống trong allowlist của work order và scratch riêng | Product content, source evidence, owner labels và run đã freeze; không tự áp dụng policy mới vào vòng đang chạy |

Agent được đọc output/scratch của chính execution nó; chỉ input là bất biến. Không role nào tự sửa `control/`, policy, chuẩn chung hoặc quyền của mình. Agent không tự ghi owner labels. Launcher/operator nhập phản hồi thực tế với identity và quyền tương ứng; Product-agent verdict không được đổi nhãn thành owner verdict.

**Một chuẩn chung, handoff có ranh giới**

- Launcher đóng băng một phiên bản mục tiêu/contract cho run. Role-safe common brief giữ cùng mục tiêu và criterion IDs; phần riêng của từng role chỉ thêm nhiệm vụ và input được phép.
- Không đưa intended winner, intervention prediction hoặc attribution vào brief chung của Product reviewer. “Cùng tiêu chuẩn” không đồng nghĩa “cùng nhìn mọi dữ liệu”.
- Launcher kiểm tra output theo contract rồi copy snapshot sang input role kế tiếp, ghi source/destination, hash, role và run ID. Không dùng writable shared directory hay symlink trỏ sang workspace role khác.
- Mỗi role chỉ submit output của nó; launcher bảo toàn bản đã nhận. Auditor đề xuất sửa; việc sửa chạy trong execution mới được giao đúng role, không sửa vật chứng tại chỗ.
- Learning của một case ở lại case. Muốn nâng thành thay đổi tiêu chuẩn chung cần một amendment có version và lý do; các agent không chỉnh rubric/policy giữa vòng để hợp thức hóa output của mình.

**Enforcement tối thiểu, không coi CWD là sandbox**

Thư mục và prompt chưa tự chặn đọc/ghi ngoài vùng. Worker cần dùng cơ chế sandbox sẵn có của runtime hoặc một broker công cụ file chỉ expose allowlist của execution. Nếu dùng broker thì agent không được đồng thời có shell/file/network tool khác có thể bỏ qua broker. Các thao tác shell nếu cần phải chạy dưới cùng giới hạn filesystem; không cấp quyền bằng một shell tùy ý trên máy host.

Policy do launcher sở hữu, mặc định deny mọi task-data path ngoài workspace được cấp. Runtime dependencies có thể được mount read-only ở vùng riêng, không mở rộng sang repo, user home, credentials hoặc run khác. Role packet phải có dữ liệu cần dùng thay vì buộc agent đọc toàn repo. Không cấp web/network cho các role trong vòng evidence-bounded này nếu work order không cho phép.

Ràng buộc đường dẫn trên resolved path, bao gồm `..`, absolute paths, symlink/junction trên Windows và đường dẫn tới run khác. Input read-only cần được bảo vệ bởi công cụ/runtime thực thi, không chỉ một cờ ghi trong JSON. Đừng dùng OS ACL cùng một host identity rồi khẳng định đã cô lập các process nếu chúng vẫn có đường truy cập khác.

Vượt quyền phải bị từ chối trước thao tác, ghi tối thiểu role, execution/run ID, action, attempted/resolved path, kết quả DENIED và policy version. Event do launcher/sandbox ghi vào `control/access-events.jsonl`, agent không sửa được; không dựa vào self-report để xác nhận tuân thủ. Không ghi nội dung nhạy cảm của file bị từ chối. Có manifest/hash trước/sau để phát hiện ghi ngoài output được phép; hash không chứng minh agent chưa đọc ngoài vùng.

Nếu môi trường hiện tại chỉ hỗ trợ thư mục riêng và kiểm tra diff, worker phải ghi `READ_ISOLATION_NOT_ENFORCED`; chưa được gọi đó là sandbox hoặc dùng làm bằng chứng blind review. Xác định đúng capability thiếu và dùng cơ chế giới hạn sẵn có trước. Không xây nền tảng quyền tổng quát cho mọi agent; chỉ chứng minh launcher/profile của prototype và các role thực sự chạy.

**Acceptance cho workspace trước vòng agent thật**

| Ca kiểm tra qua đúng tool surface agent sẽ nhận | Kết quả cần thấy |
|---|---|
| Role đọc input hợp lệ, ghi output/scratch của mình | ALLOW; output dùng được cho handoff |
| Writer đọc review/owner labels hoặc input run khác | DENY; có event ngoài vùng agent kiểm soát |
| Writer sửa Plan/evidence trong input hoặc source product | DENY; hash không đổi |
| Reviewer đọc trace/Plan trước khi vote freeze | DENY; sanitized input không chứa các dữ liệu đó |
| Auditor sửa candidate, measurement hoặc policy | DENY; vật chứng bất biến |
| Đi vòng bằng `../`, absolute path, symlink/junction | DENY trên resolved target |
| Sửa code ngoài allowlist của system repair task | DENY hoặc workspace diff check chặn submit; ghi rõ mức enforcement thực tế |
| Output handoff sang role sau | Bản copy read-only, đúng hash; role sau không đọc trực tiếp source workspace |

Các test dùng fixture tạm và không cần tạo prose hay gọi LLM. Kiểm tra nơi deny thực sự xảy ra; không chỉ unit-test một hàm kiểm tra path mà vẫn đưa cho agent công cụ bypass. Một access-denied event chỉ là bằng chứng của lần thử đó, không phải chứng nhận tuyệt đối mọi hành vi của agent.

**Handoff giới hạn:** sửa decision semantics, bảo toàn measurement, sửa nhãn authority, gắn brief chung vào case và triển khai workspace quyền tối thiểu ở trên. Giữ các cơ chế vừa pass. Sau đó chuyển trọng tâm sang một vòng Plan–Writer–review có giới hạn khi owner giao chạy; không quay lại checklist kiến trúc dài. Những phần như benchmark certification toàn diện, nhiều topic, event framework và human-time instrumentation hoàn chỉnh có thể để sau.

Worker bàn giao thêm một manifest quyền đọc/ghi theo role, bằng chứng ALLOW/DENY thực tế qua launcher, một handoff đúng hash và các giới hạn enforcement còn lại. Không chạy sản phẩm mới chỉ để chứng minh sandbox.

Provenance kiểm thử review: các probe chỉ thao tác temporary case và measurement `TEST_ONLY`; các ca và kết quả đã được ghi trong tài liệu này. Full production suite và baseline failures ngoài phạm vi không được kiểm chứng lại trong phiên review; kết quả test nêu trên chỉ thuộc focused suite và verifiers mới.
