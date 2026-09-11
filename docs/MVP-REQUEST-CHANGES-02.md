# Request changes 02 — budget thời gian và hai Writer

**Owner amendment; chưa implement.** Áp dụng cho PR #14, branch
`codex/owner-first-mvp`, implementation đã review tại
`fff42d7c3b21cc30e7d12e7a8f7441f2fe59f481`.

Owner bổ sung yêu cầu sau work order đầu: cần biết thời gian agent làm việc, giới
hạn ngân sách từng vòng, biết khoản phát sinh và tự phê duyệt gia hạn; đồng thời
muốn so hai Writer để chọn writer chính. Đây là scope mới được Owner giao, không
phải các tiêu chí mà Sol được kỳ vọng tự đoán trong implementation trước.

Văn bản này thay thế các chỗ yêu cầu Planner riêng, một Writer/một draft và hoãn
mọi so sánh hai mẫu trong work order cũ. Các giới hạn về authority, artifact bất
biến, workspace và dừng chờ Owner vẫn giữ. Chưa merge PR trước khi hoàn tất các
thay đổi dưới đây. Vòng live chỉ bắt đầu khi có ngân sách do Owner duyệt; chưa có
số phút cho vòng live không ngăn merge implementation đã được kiểm chứng.

## 1. Chốt đội hình, không thêm agent

```text
Owner: giao mục tiêu, duyệt budget/gia hạn, đọc và chọn Writer
  ↓
Sol repo: chuẩn bị một brief/Plan, vận hành repo, kiểm thử, chuyển packet
  ├─ Writer Gemini 3.8 Flash: một draft
  └─ Writer Sol 5.6: một draft
  ↓
Hai mẫu + báo cáo thời gian → Owner phản hồi → STOP
```

Đây là **một phiên Sol vận hành repo và hai phiên Writer**, dùng hai dòng model.
Không có Planner agent riêng, reviewer agent riêng hoặc time-auditor agent.
Plan là một bước của Sol repo; freeze là ghi nhận phiên bản, không tự duyệt nội
dung production. Sol repo không viết thay draft hoặc tự chọn Writer thắng.

Writer Sol phải là phiên riêng với Sol repo, chỉ nhận packet Writer. Không tái sử
dụng context đã xem kiến trúc, baseline, dự đoán hoặc mẫu Gemini. Cả hai Writer
chỉ được đọc input và ghi output/scratch của mình. `control/`, log thời gian,
budget và phê duyệt nằm ngoài quyền ghi của Writer.

Ghi tên model theo yêu cầu Owner và model/config thực tế host trả về. Thiếu hoặc
khác model phải báo; không gắn nhãn Gemini/Sol cho nội dung do phiên khác tạo.

## 2. Hai mẫu từ cùng một nhiệm vụ

- Hai Writer nhận **cùng nội dung brief, Plan, authority, phạm vi, yêu cầu đầu ra**.
  Hash phần nội dung chung phải bằng nhau; session/model metadata được đặt riêng.
- Mỗi Writer đúng một attempt sinh draft. Retry kỹ thuật phải giữ attempt cũ,
  lý do và thời gian; không tự reroll để có kết quả đẹp hơn.
- Có thể chạy song song khi host hỗ trợ; ghi thực tế song song hay tuần tự.
  Không bắt xây scheduler mới chỉ để chạy song song.
- Draft đầu tiên tới không kết thúc vòng và không được đưa feedback vào Writer
  còn lại. Khi đủ hai draft hợp lệ thì bàn giao hai mẫu để Owner chọn.
- Một Writer lỗi/timeout: giữ mẫu còn lại, báo cặp chưa đủ; không lấy output cũ,
  gọi Writer khác hoặc tự tuyên bố đã hoàn thành so sánh.
- Dùng hai file đọc đơn giản, ví dụ `owner/sample-A.md`, `owner/sample-B.md`;
  giữ mapping writer/session/hash trong control và không sửa nội dung lúc copy.
  Không cần A/B framework hay agent chấm điểm. Owner được xem danh tính nếu muốn.
- Ghi nguyên văn feedback, mẫu được chọn (A/B/hòa/chưa chọn) và quyết định writer
  chính nếu Owner thực sự đưa ra. Một lần thích mẫu A không tự trở thành chứng
  nhận model A tốt hơn hoặc cấu hình writer mặc định cho các vòng sau.

## 3. Budget được chốt trước khi agent làm việc

Một budget record cho mỗi vòng: ID, code commit/config, scope, số attempt được
phép, đơn vị đo, trần ban đầu, phần phân bổ cho Sol repo/Gemini Writer/Sol Writer,
và bằng chứng Owner phê duyệt. Không tự điền một con số mặc định rồi coi là đã duyệt.
Owner chưa đưa số phút cụ thể trong yêu cầu này; lúc mở vòng thật phải chốt số đó.

Đề xuất đơn vị chính: **giây phiên agent làm việc cộng dồn**. Owner phải thấy rõ
đơn vị khi duyệt; không đánh tráo nó với thời gian lịch của vòng. Ngân sách bao gồm
chuẩn bị Plan, thao tác repo, kiểm thử, sửa lỗi và các attempt Writer, không chỉ
thời gian tạo prose. Nếu Owner đặt thêm hạn thời gian lịch, ghi như một giới hạn
riêng; không trộn hai phép đo.

Mỗi lượt làm việc được trừ khỏi phần đã phân bổ và trần chung. Không được tự lấy
phần còn dư của Writer này để gia hạn Writer khác hoặc chuyển sang sửa kiến trúc.
Nếu muốn cơ chế dự phòng/chuyển phân bổ, nó phải nằm trong chính budget Owner đã duyệt.

Các việc sửa kiến trúc giữa hai vòng cũng phải có work item và budget riêng trước
khi bắt đầu. Gắn nó với thay đổi/commit và vòng hưởng lợi; báo riêng để không mất
chi phí đó, đồng thời không cộng hai lần vào tổng của từng vòng.

## 4. Đo đúng thời gian, không biến timestamp nhận file thành runtime

Giữ ba số riêng:

| Số đo | Ý nghĩa |
| --- | --- |
| Elapsed của vòng | Thời gian lịch từ mở vòng đến checkpoint; các khoảng chờ được liệt kê |
| Tổng thời gian làm việc | Tổng khoảng làm việc của Sol repo và hai Writer, kể cả lỗi/retry; dùng để đối chiếu budget chính |
| Thời gian chờ | Chờ Owner duyệt/đọc, chuyển packet, host queue nếu quan sát được; không giả định là thời gian suy luận |

Ví dụ TEST_ONLY: hai Writer chạy đồng thời, mỗi phiên 120 giây → tổng 240 giây
phiên agent, nhưng phần elapsed của cặp là 120 giây. Thêm 10 phút chờ Owner không
làm tổng work tăng thêm 10 phút. Không cộng cả timer công việc cha và timer test
con như hai khoản công độc lập; dùng các khoảng không chồng lấn trong cùng actor.

Một record khoảng làm việc cần đủ: vòng/work-item, actor/session, công việc, attempt,
start/end/duration, nguồn timestamp, trạng thái, lý do, input/output hoặc commit/log
liên quan. Host duration là thời lượng invocation quan sát được, không phải bằng
chứng thời gian suy nghĩ nội bộ của model.

- Khi host do controller gọi: đo từ thực thi thật, dùng monotonic clock cho duration
  và UTC cho mốc đối chiếu; giữ log gốc. Ghi queue/retry riêng nếu host có bằng chứng.
- Khi chuyển packet thủ công: có start/stop phiên được operator ghi, gắn nhãn
  `OPERATOR_OBSERVED_SESSION_WINDOW`. Khoảng này có thể gồm chờ trong phiên; không
  gọi nó là active inference time. Không suy runtime từ `agent_created_at` hoặc
  `operator_received_at` hiện có. Chỗ không đo được là `UNKNOWN`, không phải 0.
- Interval thiếu end, đồng hồ đảo chiều, log bị thiếu hoặc host mất kết nối phải
  hiện rõ. Không cho nó tự giải phóng budget hoặc làm báo cáo dưới trần giả.
- Pause không đóng được timer của invocation vẫn đang chạy. Một actor không mở
  nhiều interval chồng lấn để làm méo phép tính; retry/resume có ID để tránh tính trùng.

Không cần trace graph hoặc event bus. Có thể mở rộng log JSONL hiện có, thêm một
budget record và một bảng tổng hợp được tính từ log.

## 5. Gia hạn chỉ có hiệu lực sau quyết định của Owner

Khi thiếu budget cho bước kế tiếp hoặc đạt trần trong lúc chạy:

1. Giữ artifact/log đã tạo, dừng phát sinh công việc mới và chuyển sang
   `AWAITING_OWNER_BUDGET_APPROVAL` (giữ checkpoint chuyên môn đang dở).
2. Request gia hạn phải cho Owner thấy: trần ban đầu; gia hạn đã duyệt; tổng đã dùng;
   còn lại; **đã vượt thực tế bao nhiêu**; **xin thêm bao nhiêu**; actor/task phát sinh;
   lý do và bằng chứng; phần sẽ hoàn thành nếu được duyệt.
3. Chỉ resume sau phê duyệt gắn đúng request/vòng/actor/scope/số giây. Từ chối hoặc
   chưa trả lời đều không phải phê duyệt. Không timeout rồi mặc nhiên tiếp tục.
4. Gia hạn là khoản cộng thêm có lịch sử; không reset thời gian đã dùng, sửa trần
   gốc, tạo run ID khác để né budget hoặc hợp thức hóa thời gian vượt trước đó.

Nếu host hỗ trợ timeout/cancel, truyền phần ngân sách còn lại và dừng invocation
khi hết hạn; ghi độ trễ cancel và phần vượt thực tế. Nếu phiên ngoài controller
không thể bị ngắt, phải nói rõ chỉ có thể chặn bước kế tiếp và ghi overrun, không
tuyên bố đã cưỡng chế hard timeout. Không hủy bằng chứng hay tự loại bỏ draft trễ
để che chi phí; Owner quyết định có dùng kết quả đó hay không.

Approval giữ nguyên văn quyết định Owner và nguồn tham chiếu bên cạnh phần đã parse.
Sol repo được chuyển quyết định thật thành record, không được tự phê duyệt, đổi
nghĩa lời Owner hoặc coi việc được giao implement là quyền tăng budget vô hạn.
Writer không có lệnh ghi approval. Một flag `--approved` do agent tự truyền không
phải bằng chứng Owner đã đồng ý. Với nhập thủ công, công khai giới hạn xác thực;
không xây hệ thống auth mới hoặc giả vờ local JSON chống được mọi sửa đổi của operator.

## 6. Nhìn thấy phát sinh do sửa kiến trúc

`status` hoặc một lệnh audit nhỏ xuất bảng:
`actor/task | đã phân bổ | đã dùng | phát sinh | lý do + evidence | đang chờ ai`.
Hiển thị cả tổng work, elapsed, thời gian chờ và phần UNKNOWN; không chỉ % tiến độ.

Trước sửa kiến trúc: ghi vấn đề, phạm vi code, chi phí sửa dự kiến, ảnh hưởng runtime
dự kiến và độ chắc chắn; đây là ước tính cần Owner duyệt scope/budget. Sau sửa: gắn
commit và báo số đo thật so với mốc trước trên công việc có thể so sánh.

Tách chi phí sửa một lần khỏi overhead thực thi lặp lại. So các vòng phải ghi rõ
code commit, model/config, số Writer/attempt, input/phạm vi và chế độ đo. Vòng hai
Writer không trực tiếp so tổng thời gian với vòng một Writer rồi kết luận code
chậm gấp đôi. Thiếu dữ liệu tương đương: `NOT_COMPARABLE`/`UNKNOWN`; không gán nguyên
nhân hay tỷ lệ trách nhiệm bằng ước lượng. Không tự chạy thêm vòng live chỉ để lấy
benchmark thời gian. Synthetic test chỉ chứng minh phép tính, không đo model thật.

## 7. Phần cần sửa trực tiếp và nghiệm thu cuối

Điểm nối hiện có tại head được review:

- `scripts/learning.py:175` `_run_paths`, `:214` `_workspace_dirs`, `:224` `prepare_run`
  đang cố định một `writer-001`; đổi thành hai Writer cố định và Sol repo giữ bước Plan.
- `:351` `freeze_plan`, `:440` `freeze_draft`: giữ freeze/hash hiện có, xuất hai packet
  cùng content hash, nhận hai kết quả riêng và kiểm tra budget ở bước chuyển trạng thái.
- `:506` `record_owner_feedback`, `:541` `status`: bind feedback đúng cặp mẫu, thêm
  lựa chọn Owner và bảng thời gian/approval; không tự chọn model hoặc chạy vòng mới.
- `:339` `_capture_optional_host_log` cùng timestamp handoff mới lưu được log/thời
  điểm nhận; chưa tính duration hoặc quản lý budget. Không gọi tính năng mới là đã có.
- Cập nhật README, AGENTS, `docs/MVP.md`, work log và kiểm thử cùng scope này.

Giữ M1–M6 của work order trước, thay giả định một Writer bằng hai Writer; bổ sung
**đúng sáu kiểm tra** sau, dùng fake clock thay vì sleep dài:

| ID | Bằng chứng để đóng |
| --- | --- |
| RC1 | Sol repo chuẩn bị một Plan; hai workspace Writer riêng, cùng content hash, model/session riêng; không nhận chéo draft/context; không có agent phụ |
| RC2 | Nhận mẫu theo cả hai thứ tự đều đúng; thiếu/lỗi một Writer không báo cặp hoàn tất; feedback gắn hai hash, chọn Writer chỉ khi Owner chỉ định |
| RC3 | Tính đúng thời gian tuần tự/song song, không cộng chờ Owner hoặc timer cha/con hai lần; lỗi/retry vẫn tính; thiếu timing hiện UNKNOWN |
| RC4 | Chưa có budget được duyệt không dispatch; hết trần chặn bước mới/timeout theo khả năng host; lưu overrun và pending output, không tự gia hạn |
| RC5 | Approval sai vòng/request/scope, bị từ chối hoặc chưa có đều không resume; approval đúng chỉ cộng phần duyệt, không reset lịch sử hoặc cấp thêm attempt ngoài scope |
| RC6 | Báo cáo chỉ ra khoản tăng theo actor/task/commit, tách estimate/observed và chi phí sửa/chi phí mỗi vòng; sửa lỗi đường dẫn Windows hiện có; CI phù hợp qua |

Review local tại head `fff42d7`: chạy `python -m unittest tests.test_owner_first_mvp -v`
trên Windows có **6/7 pass**, tổng unittest báo **0.487s**. M1 thất bại tại
`tests/test_owner_first_mvp.py:87` do `endswith` dùng `/` trong khi đường dẫn thật
dùng `\`. Sửa so sánh bằng Path hoặc chuẩn hóa biểu diễn; không bỏ kiểm tra đường
dẫn. Đây là thời gian test controller, không phải thời gian agent/vòng học.

Đạt scope này thì dừng và cập nhật PR #14 theo implementation cuối cùng. Không
thêm dashboard, time-auditor agent, benchmark chất lượng hoặc hệ điều phối mới.
Không báo READY cho budget/host mà chỉ mới có tài liệu hoặc fixture kiểm thử.
