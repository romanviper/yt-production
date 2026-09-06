# Work order cho Sol 5.6 — đưa repo về MVP do người đọc dẫn dắt

Trạng thái: **PLAN ONLY — chưa triển khai, chưa có vòng live mới**.

Owner yêu cầu tinh giản sau khi việc phối hợp kiến trúc–thi công phát sinh nhiều
vòng chỉnh sửa nhưng chưa đưa được một bản nháp mới tới người đọc. Work order này
thay thế hướng tiếp tục hoàn thiện coordinator/telemetry trước lần đọc đầu tiên.
Sol thực hiện công việc `system_architect`; không tự tạo hoặc duyệt nội dung production.

## 1. Kết quả cần giao

Một người mở repo phải trả lời được ngay: đang làm gì, bản nháp ở đâu, ai đang được
làm việc và phải chờ ai. Đường hoạt động duy nhất của MVP:

```text
Owner giao một đoạn cần viết
  → đóng băng brief và tài liệu được phép dùng
  → Planner tạo một Plan ngắn
  → Writer tạo một bản nháp từ Plan
  → dừng, đưa bản nháp cho Owner đọc
  → lưu nguyên văn phản hồi
  → dừng, chờ Owner chọn thay đổi tiếp theo
```

Lần đầu tạo mẫu để đọc, chưa phải phép thử chứng minh một can thiệp thắng baseline.
Không bắt buộc A/B, FoC comparison, đánh giá tự động hoặc chẩn đoán nguyên nhân trước
lần đọc này. Một bản nháp chưa hay vẫn là đầu ra hợp lệ để thu phản hồi.

## 2. Bắt đầu đúng chỗ, không nhập nhầm phần dang dở

- Checkout bàn giao sạch: `D:/yt-production/.worktrees/owner-first-mvp`.
- Nhánh: `codex/owner-first-mvp`, tạo từ `origin/main` tại
  `3af8d9ef6161f10818c33b1f714ecd95c64139d6`. Fetch và kiểm tra main hiện tại trước khi sửa.
- `D:/yt-production` đang detached ở commit cũ `2fccaf6`; không dùng làm điểm bắt đầu.
- `codex/p01-phase3-coordinator-round-01` tại `fb1faec` là implementation cần tham khảo,
  không phải đường MVP đã hoạt động. Nó chứa toàn bộ chuỗi thay đổi Phase 1–3 chưa merge vào main.
- `D:/yt-production/.worktrees/first-owner-learning-round` là nhánh tích hợp bị thay thế
  bởi yêu cầu tinh giản: đang có merge chưa commit và code sửa dở. **Không merge, cherry-pick
  nguyên khối hoặc xem các kiểm thử tại đó là bằng chứng nghiệm thu MVP này.**
- Tính đến khi viết work order, chưa PR/merge nào được thực hiện trong đợt điều chỉnh này.

Giữ lịch sử và artifact cũ nguyên trạng. Tinh giản bằng cách thu nhỏ đường hoạt động;
không cần xóa repo, di chuyển hàng loạt hoặc nhập mọi branch để rồi dọn lại.

## 3. Phạm vi bản đọc đầu tiên

Dùng P01 hiện có làm phạm vi thử, dựa trên lãnh thổ lịch sử và giới hạn đã được duyệt.
Đề xuất một đoạn tiếng Việt đủ để đọc độc lập, khoảng 450–650 từ; đây là kích thước
thử dự kiến, không phải thước đo chất lượng hay điều kiện ép agent viết thêm.

Đầu vào khởi đầu đã có trên main:

- `products/sumer-writing/02_outline/section-overlays/P01.json`;
- `products/sumer-writing/03_sections/P01/historical-substrate.json`.

Kiểm tra liên kết với outline/substrate nguồn bằng các hàm hiện có nếu cần. Đưa vào
packet đúng phần lịch sử và giới hạn cần thiết; không đưa toàn bộ policy repo vào
context sáng tạo. Chỉ bổ sung tài liệu kiểm chứng đã thuộc authority hiện có khi
cần một chi tiết cụ thể; không tự nghiên cứu mở rộng trong vòng này.

Không dùng B03, `EXPLANATION_BEFORE_NEED`, can thiệp cũ hoặc dự đoán reviewer làm mục
tiêu sửa mặc định. Đó là giả thuyết lịch sử, chưa phải phản hồi của Owner cho bản mới.
Không lấy notebook chuyển thể, benchmark craft hoặc verdict cũ làm nguồn sự thật mới.

Plan chỉ cần nói đoạn này kể phần nào, sử dụng tài liệu nào và dừng ở đâu. Writer
được chọn cách kể trong phạm vi ấy. Không quy định thêm công thức hook, số beat hoặc
ngữ pháp kể chuyện nhằm chiều lòng bộ kiểm thử.

Đóng băng Plan là ghi nhận phiên bản để bàn giao, không phải duyệt story plan hay
thay thế kế hoạch production đã được Owner duyệt. Giữ các checkpoint duyệt nội dung
của Owner khi áp dụng; agent không được tự nhận quyền phê duyệt từ thao tác freeze.

## 4. Implementation nhỏ nhất

Ưu tiên một lệnh điều khiển, dự kiến `python scripts/learning.py`, một file hướng dẫn
`docs/MVP.md`, và kiểm thử cho hành vi thực sự cần giữ. Tái sử dụng hàm nhỏ khi hữu ích;
không kéo cả production router hoặc coordinator Phase 3 vào làm dependency.

Lệnh cần làm được đúng các việc sau; tên subcommand cụ thể do Sol chọn:

1. Tạo phiên mới, snapshot brief/authority và xuất packet Planner.
2. Nhận và đóng băng kết quả Planner; xuất packet Writer từ Plan đó và cùng authority.
3. Nhận và đóng băng bản nháp Writer; trả ngay đường dẫn bản đọc cho Owner.
4. Ghi nguyên văn phản hồi Owner, gắn với đúng hash bản nháp; không tự tạo bản kế tiếp.
5. Xem trạng thái hiện tại, bước tiếp theo và lỗi cụ thể nếu có.

Đường chạy qua Owner chuyển packet giữa những phiên agent riêng phải sử dụng được
mà không cần xây thêm host API. Nếu tìm thấy host thật có sẵn thì nối tối thiểu vào
đường này; không tạo thêm một hệ điều phối để đạt nhãn “ready”.

Hiện chỉ xác minh được repo có giao diện spawner và test giả lập, chưa xác minh được
adapter live. Owner cũng đã nói chưa hiểu rõ phần này. Không lấy câu trả lời trước
“đã có API/host” làm bằng chứng kỹ thuật hoặc yêu cầu Owner tự thiết kế adapter.

Giao tiếp thủ công phải được ghi đúng là giao tiếp thủ công. Không tạo spawn receipt,
timestamp thực thi hay chứng nhận độc lập giả để lấp chỗ thiếu tích hợp.

## 5. Workspace và quyền giữ ở mức đủ dùng

Layout dự kiến, có thể rút gọn tên nhưng phải giữ ranh giới:

```text
runs/<id>/
  control/                 trạng thái, input identities, bàn giao và phản hồi Owner
  agents/plan/{input,output,scratch}/
  agents/writer/{input,output,scratch}/
  owner/draft.md            bản đọc trỏ về đúng Writer output đã đóng băng
```

| Vai trò | Đọc | Ghi | Không được quyết định |
| --- | --- | --- | --- |
| Planner | Packet của mình | Plan, ghi chú và scratch của mình | Mở rộng evidence hoặc tự gọi Writer |
| Writer | Plan đóng băng, brief và authority trong packet | Một draft, ghi chú và scratch của mình | Sửa Plan/tiêu chuẩn, tự reroll |
| Review/Audit, khi Owner giao riêng | Bundle đã đóng băng được cấp | Báo cáo trong workspace riêng | Sửa draft, đổi chuẩn hoặc mở vòng mới |
| Bộ điều khiển do operator dùng | Artifact cần để chuyển bước | `control/`, bản copy bàn giao | Viết thay nội dung hoặc phản hồi Owner |
| Sol triển khai hệ thống | Code và tài liệu trong scope PR | System paths của PR | Đổi nội dung/duyệt production |

Agent không được cấp repo chung cùng shell toàn quyền rồi gọi CWD là sandbox.
Với phiên chat chuyển packet thủ công, dùng phiên riêng chỉ có packet và không có
tool truy cập repo/filesystem/network. Với host dùng tool, chỉ cấp broker giới hạn
vào workspace tương ứng; mọi thao tác qua broker phải ghi nhận allowed/denied.

Chống vượt đường dẫn phải xét đường dẫn đã resolve, gồm `..`, absolute path và
symlink/junction. Output đã bàn giao không được ghi đè; sửa đổi phải là phiên bản mới.

Chỉ tuyên bố enforcement nào đã kiểm chứng được. Nếu context isolation hoặc truy
cập ngoài broker chưa được host xác nhận, ghi hạn chế đó; không kết luận rằng đã
ghi được toàn bộ thực thi hoặc chứng minh được nguyên nhân chất lượng. Không âm
thầm cấp quyền rộng hơn để làm cho lệnh chạy qua.

## 6. Quan sát tối thiểu, dùng được ngay

Mỗi bàn giao giữ: role/session được khai báo, hash input, artifact output gốc, lý do
ngắn do agent khai báo, điểm chưa chắc, thời điểm nhận và kết quả kiểm tra. Giữ nguyên
log thực thi host nếu có; không phát minh log cho phiên thủ công hoặc yêu cầu private
chain-of-thought. Phân biệt thời điểm operator nhận kết quả với thời điểm agent tạo nó.

Nếu báo lỗi, lệnh phải chỉ ra artifact/đường dẫn, điều kiện không đạt và bước sửa nhỏ
nhất. Không bắt Owner mở nhiều file mới biết trạng thái. Một `status` phải cho biết
đang chờ Planner, Writer hay Owner và đường dẫn cần mở.

Mỗi thay đổi có ý nghĩa trong quá trình Sol thi công ghi một dòng vào work log của PR:
`vấn đề quan sát được → tiêu chí mục 8 → thay đổi → bằng chứng kiểm tra`.
Đề xuất ngoài scope ghi vào một mục Deferred; không triển khai registry hoặc dashboard
riêng để quản lý chính work log này.

## 7. Quyền quyết định và điểm dừng

- Owner quyết định chất lượng bản đọc và điều gì đáng cải thiện tiếp theo.
- Agent có thể chỉ ra lỗi, giả thuyết và đề xuất. Các đề xuất không tự trở thành lệnh thi công.
- Phản hồi thích/không thích không tự biến thành “symptom reduced” hay “causal proof”.
- Sau draft: trạng thái `AWAITING_OWNER_FEEDBACK`, không tự sửa, gọi reviewer hoặc chạy lại.
- Sau phản hồi: `OWNER_FEEDBACK_RECORDED`, giữ nguyên bản cũ, chờ Owner chọn thay đổi.
- Lỗi dữ liệu/quyền/ghi file ngăn thực thi có thể được sửa tối thiểu trong scope đã giao.
  Kết quả văn chương yếu không phải lý do tự mở một dự án cải thiện kiến trúc.

Chuẩn chung của mọi vai trò là: giúp Owner có bản đọc và kiểm chứng thay đổi từ phản
hồi thật, giữ đúng authority, giữ dấu vết trung thực. Không cần một điểm số chung cho
mọi công việc; mỗi vai trò chịu trách nhiệm trước cùng mục tiêu và các ranh giới này.

## 8. Nghiệm thu hữu hạn — sáu điều kiện

| ID | Điều phải chứng minh | Kiểm tra đủ để đóng |
| --- | --- | --- |
| M1 | Một cửa vào, một trạng thái | Từ README đi đến đúng lệnh; lệnh status nêu artifact cần mở và người đang được chờ |
| M2 | Packet đúng và cố định | Đổi input sau freeze hoặc nộp output cho sai phiên bị phát hiện; không ghi đè bản đã nhận |
| M3 | Workspace giữ ranh giới | Thử đọc/ghi chéo vùng qua surface thực tế bị từ chối; không tuyên bố sandbox từ CWD hoặc hash |
| M4 | Có đường đến bản đọc | Dùng fixture ghi rõ TEST_ONLY đi hết prepare → Plan handoff → Writer handoff → bản đọc; không cần API giả |
| M5 | Owner giữ quyền mở vòng sau | Nhận draft và phản hồi đều dừng; không có nhánh tự sinh candidate mới hoặc coi verdict agent là phản hồi Owner |
| M6 | PR không làm hỏng trạng thái cũ | Kiểm thử thích hợp và CI qua; không sửa production, archive, authority hay giảm gate chỉ để xanh |

Đo thời gian thực tế của kiểm tra M2–M5 và ghi kết quả, không đặt ngưỡng tùy ý để mở
thêm việc tối ưu. Fixture test chứng minh thao tác bàn giao, không chứng minh đã có
agent thật hay người đọc thật tham gia.

Khi sáu điều kiện đạt, dừng thi công MVP. Reviewer muốn chặn phải chỉ ra ID, lỗi quan
sát được và ảnh hưởng đến lần đọc đầu tiên. Ý tưởng tốt hơn nhưng chưa cần cho các
điều kiện này đi vào Deferred. Chỉ đổi acceptance khi có lỗi mới cụ thể hoặc Owner đổi scope.

## 9. Thứ tự thi công và bàn giao

1. Kiểm tra main, viết `docs/MVP.md` ngắn và cập nhật README/AGENTS để có một entrypoint.
   Gắn nhãn tài liệu Phase 1–3 và production workflow là lịch sử/tham khảo hoặc luồng
   production riêng; chúng không phải prerequisite của bản nháp thử nghiệm.
2. Làm đường bàn giao tối thiểu và workspace; giữ input/output/response đúng danh tính.
3. Chạy kiểm tra sáu điều kiện; chốt PR theo scope cuối cùng, không kể lại toàn bộ
   phương án đã bỏ. Owner đã giao việc tạo PR và merge phần chuẩn bị hệ thống; thực
   hiện sau validation, không merge work order này như thể implementation đã xong.
4. Bàn giao cho Owner: link PR, commit main, lệnh bắt đầu, nơi bản nháp sẽ xuất hiện,
   điều gì còn chưa được kiểm chứng ở host thật. Chờ lệnh bắt đầu viết.

Trong đợt này chỉ chuẩn bị đường chạy. Không viết nội dung production, tự chạy live,
tạo bản nháp giả hoặc đánh dấu “đã học” để làm đẹp nghiệm thu.

Ghi chú kiểm thử đã phát hiện khi xem implementation cũ: test probe lịch sử có thao
tác ghi rồi xóa hai fixture trong repo; đường dẫn overlay serialize khác nhau trên
Windows/Linux; một test đòi thông báo lỗi đã cũ. Nếu chúng xuất hiện trên main, sửa
đúng tính bất biến/khả năng chạy đa nền tảng hoặc kỳ vọng lỗi hiện hành. Không sửa
product để chiều test, không tiếp tục chạy legacy experiment trên dữ liệu thật.

## 10. Những việc chủ động để sau lần đọc

Coordinator nhiều tầng, host adapter mới, agent Product/Audit bắt buộc, spawn
certification, decision-before-output gates nâng cao, A/B mù, benchmark calibration,
FoC diagnosis, root-cause graph, invariant registry, agent registry, dashboard và
framework tự cải thiện. Chỉ lấy lại phần nào khi phản hồi hoặc lỗi thực thi cụ thể
cho thấy nó cần cho một thay đổi Owner muốn kiểm chứng.
