# Black-Box Product Evaluation Trial Protocol

Status: **CANONICAL / PHASE 1 PROTOCOL**  
Context: [Output Quality Contract](output-quality-contract.md) & [docs/phase1/START.md](../../docs/phase1/START.md)

---

## 1. Nguyên tắc Đánh giá Mù (Black-Box Isolation Boundary)

Để loại trừ hoàn toàn thiên kiến xác nhận (confirmation bias) và ảo tưởng tự báo cáo (self-reporting illusion):

1. **Cách ly tuyệt đối với Upstream:**
   - Người đánh giá (Product Reviewer) TUYỆT ĐỐI KHÔNG được nhận:
     - Kế hoạch viết (Writing Plan / Beats).
     - Báo cáo của người viết (Writer Report).
     - Lịch sử sửa đổi hay nhật ký trace của agent.
     - Kỳ vọng mẫu nào là "ứng viên mới" hay "mốc cũ".
     - Các đánh giá hoặc điểm số lịch sử trước đó.
   - Gói dữ liệu đánh giá chỉ bao gồm:
     - Văn bản văn xuôi cần đánh giá (hoặc cặp mẫu $A/B$ ẩn danh).
     - Trích đoạn tham chiếu thủ pháp được phê duyệt (`CRAFT_ONLY_NOT_TRUTH`).
     - Bản hợp đồng chất lượng và quy tắc trích dẫn bằng chứng.

2. **Cân bằng vị trí mù ngẫu nhiên (Blind Position Counterbalancing):**
   - Trong các phép thử so sánh cặp (paired comparison), thứ tự trình bày mẫu $A$ và $B$ phải được đảo ngược đối xứng giữa hai Reviewer độc lập (Reviewer 1 nhận Candidate=A/Baseline=B; Reviewer 2 nhận Candidate=B/Baseline=A).

3. **Yêu cầu Bằng chứng Đoạn văn (Evidence Grounding):**
   - Không chấp nhận phán quyết nếu không có trích dẫn câu văn cụ thể làm bằng chứng (`evidence_spans`).
   - Bắt buộc phân tích hậu quả tâm lý/nhận thức của người nghe (`listener_consequence`).
