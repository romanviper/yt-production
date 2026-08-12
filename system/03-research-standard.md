# 03 — Research Standard

## Research là claim engineering

Agent không “thu thập thông tin về chủ đề”. Agent phải xây một chuỗi claim có thể kiểm tra, biết claim nào chịu lực cho premise và biết bằng chứng nào có thể làm nó sai.

Chu trình mặc định:

> claim → falsification criterion → evidence hierarchy → contradiction → classification → narrative use

## Evidence hierarchy

1. **Primary evidence:** văn bản, hiện vật, dữ liệu khảo cổ, inscription, corpus hoặc bản dịch học thuật có provenance.
2. **Scholarly synthesis:** monograph, chapter, peer-reviewed paper, handbook hoặc catalogue bảo tàng có chuyên môn.
3. **Expert interpretation:** lecture, interview hoặc essay của chuyên gia xác định được.
4. **High-quality orientation:** encyclopedia học thuật, đại học, bảo tàng lớn.
5. **Discovery only:** báo phổ thông, documentary, podcast, Wikipedia, blog và video khác.

Nguồn tầng 5 có thể tìm keyword và bibliography nhưng không được một mình gánh claim trụ cột.

## Source index

Mỗi source phải có:

- ID ổn định `SRC-####`;
- tác giả/tổ chức, title, năm, loại nguồn;
- URL, DOI, ISBN hoặc archive locator;
- phạm vi trang/tablet/catalogue/timestamp đã dùng;
- access status và quyền sử dụng nếu trích dài hoặc dùng hình;
- đánh giá thẩm quyền và giới hạn;
- notes viết lại bằng lời của researcher, không copy dài.

“Có link” không đồng nghĩa “đã đọc”. Chỉ source có `status: reviewed` mới được gắn vào claim đã xác nhận.

## Claim ledger

Mỗi claim substantive phải có:

- ID `CLM-####`;
- câu claim đủ cụ thể để đúng hoặc sai;
- loại `fact`, `inference`, `contested` hoặc `unknown`;
- confidence `high`, `medium`, `low` hoặc `unrated`;
- source IDs và locator;
- counterevidence hoặc competing interpretation;
- chapter sử dụng claim;
- trạng thái `open`, `supported`, `qualified`, `rejected` hoặc `blocked`.

Claim chưa được ghi ledger không được xuất hiện như fact trong script.

## Contradiction protocol

Khi nguồn bất đồng:

1. viết chính xác điểm bất đồng;
2. tách bất đồng dữ liệu khỏi bất đồng diễn giải;
3. so provenance, phương pháp, niên đại và mức chuyên môn;
4. ghi điều gì sẽ làm mỗi giả thuyết mạnh/yếu đi;
5. chọn cách kể `resolved`, `weighted`, `contested` hoặc `unresolved`;
6. không chọn phương án chỉ vì cinematic hơn.

## Scene integrity

Một historical scene phải có scene card nêu:

- thời gian và địa điểm với độ chính xác thật sự có thể biết;
- nhân vật/nhóm người;
- source cho hành động hoặc lời nói;
- chi tiết vật chất được chứng thực;
- phần reconstruction và mức suy luận;
- narrative job.

Không viết suy nghĩ nội tâm, hội thoại hoặc chi tiết giác quan không có cơ sở. Có thể mô tả khả năng bằng ngôn ngữ xác suất, nhưng không làm giả certainty.

## Citation trong prose

Draft narration không cần citation học thuật phá nhịp. Claim IDs được khai báo trong chapter manifest; delivery có companion source notes. Direct quote phải gắn source và locator ngay trong file draft bằng comment biên tập.

