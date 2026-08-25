# Review — P01

Verdict: `changes_requested`

## Outcome judgment

1. **Sau khi nghe section, khán giả có thể tự trả lời mission không? — Có.** Draft cho người nghe một câu trả lời rõ: record bền và có thể kiểm tra trở nên đáng giá khi áp lực xử lý lượng ở quy mô thiết chế gặp các vật mang tin và bề mặt đất sét có thể giữ thông tin cho công việc tiếp tục.
2. **Khán giả có thể kể lại historical path dẫn tới câu trả lời đó không? — Có.** Đường kể có thể nhớ và kể lại: token mang lượng → bulla gom và niêm phong → dấu số xuất hiện trên bề mặt → bảng số biến bề mặt thành nơi record tồn tại → nhiều thực hành tiếp tục chồng lấn → quy mô hành chính tạo pressure nhưng không phải monocause.

Draft đạt exit state về một formation ecology, phá được shortcut “một phát minh đơn độc” và “token → tablet” như genealogy tất định. Nó cũng giữ đúng boundary với P02: section chỉ đặt câu hỏi về điều khiến hệ thống dấu mới khác biệt, chưa giải thích usefulness của structured signs/layout hay writing threshold thay cho section kế tiếp.

## Material issue

### 1. Bulla bị mô tả như hai bản biểu diễn chắc chắn của cùng một lượng

- **Vị trí quan sát được:** đoạn bắt đầu “Đường đi ấy đổi hướng ngay trên lớp vỏ”, câu “Bulla lúc đó mang hai cách giữ cùng một lượng: các vật nằm bên trong và dấu hiện ra trên bề mặt.”
- **Failure:** câu khẳng định quan hệ tương đương giữa nội dung bên trong và dấu ngoài bề mặt. Bounded source detail từ `SRC-0011`, locator pp. 6–9, nêu rằng dấu ngoài có thể được tạo bằng token nhưng token được ấn không nhất thiết là token nằm trong bulla; quan hệ contents-to-surface vì vậy chưa được phép chắc hóa.
- **Effect:** người nghe có thể tin rằng bằng chứng đã xác lập phép đối chiếu một-một giữa hai lớp thông tin, làm yếu trust và vô tình kéo lập luận gần hơn tới direct token→tablet genealogy mà section đang chủ động bác bỏ.
- **Responsible layer:** `evidence`.
- **Smallest valid revision scope:** chỉ câu khẳng định tương đương này và, nếu cần để giữ mạch nghe, câu liền kề; không cần đổi cấu trúc section.
- **Acceptance test:** passage không còn khẳng định dấu ngoài và token bên trong giữ đúng cùng một lượng khi chưa có support; nó vẫn cho người nghe hiểu được việc thông tin số đi ra bề mặt, đồng thời giữ nguyên guardrail chống genealogy tuyến tính.

## Evidence and continuity

- `resolve_claims` thành công cho `CLM-0011`–`CLM-0018`; truth ceiling không đổi.
- Các chi tiết Uruk khoảng 200 hectare / khoảng 40.000 người, dấu token trên bulla tương ứng với dấu số sớm, và sự đồng tồn tại ở Tushan đã được kiểm tra trong approved locators rồi ghi qua evidence broker.
- Các qualification về token đa chức năng, corpus chọn lọc, transaction labels và feedback model đều được draft giữ ở mức phù hợp.

<!-- production-gate:start -->
{
  "schema_version": 1,
  "verdict": "changes_requested",
  "hard_gates": {
    "evidence_integrity": {
      "status": "fail",
      "basis": "Một câu chắc hóa contents-to-surface equivalence của bulla dù approved source detail nói token tạo dấu ngoài không nhất thiết là token nằm bên trong. Các claim và qualification còn lại được support và giữ đúng mức."
    },
    "mission_and_exit": {
      "status": "pass",
      "basis": "Người nghe có thể trả lời vì sao durable, inspectable records trở nên đáng giá và rời section với formation ecology cùng administrative pressure không phải monocause."
    },
    "adjacent_section_boundary": {
      "status": "pass",
      "basis": "P01 hoàn tất formation pressure/ecology rồi chuyển bằng câu hỏi; không chiếm phần giải thích structured signs, language recovery hay writing threshold của P02."
    },
    "one_hearing_narration": {
      "status": "pass",
      "basis": "Bulla làm vật dẫn xuyên suốt, chuỗi biến đổi vật chất rõ và phần chốt ba vế giúp mission answer cùng historical path có thể kể lại sau một lần nghe."
    }
  },
  "dimensions": {
    "hook_and_audience_promise": {
      "score": 9,
      "evidence_scope": "full",
      "basis": "Bulla tạo ngay một câu hỏi vật chất cụ thể và hứa giải thích vì sao record vừa bền vừa dùng được trở nên cần thiết."
    },
    "historical_progression": {
      "score": 9,
      "evidence_scope": "full",
      "basis": "Path từ token/bulla qua dấu bề mặt và bảng số tới ecology cùng institutional pressure rõ, có thể retell và không bị kể như niên biểu tất định."
    },
    "causal_clarity": {
      "score": 8,
      "evidence_scope": "full",
      "basis": "Draft phân biệt pressure, compatibility và feedback với monocause; chỉ quan hệ giữa nội dung bulla và dấu ngoài bị diễn đạt chắc hơn evidence."
    },
    "concrete_specificity": {
      "score": 8,
      "evidence_scope": "full",
      "basis": "Vật thể, động tác và số liệu Uruk làm lập luận cụ thể; một chi tiết về cùng một lượng cần qualification để specificity không vượt support."
    },
    "narrative_momentum_and_stakes": {
      "score": 8,
      "evidence_scope": "full",
      "basis": "Mạch từ vật nhỏ tới quy mô thiết chế tăng stakes đều đặn và giữ câu hỏi điều tra hoạt động tới phần payoff."
    },
    "supported_human_work_orientation": {
      "score": 8,
      "evidence_scope": "limited",
      "basis": "Evidence không cung cấp cá nhân hay scene cụ thể, nhưng draft vẫn neo hệ thống vào các thao tác đếm, chuyển giao, gom, niêm phong, đánh dấu và xử lý hồ sơ."
    },
    "explanatory_economy": {
      "score": 8,
      "evidence_scope": "full",
      "basis": "Các qualification được đặt gần claim cần giới hạn và phần lớn repetition có chức năng củng cố progression cùng mission answer."
    },
    "spoken_rhythm_and_clarity": {
      "score": 8,
      "evidence_scope": "full",
      "basis": "Câu có nhịp biến đổi tốt, thuật ngữ được giải thích bằng thao tác và các đoạn phân tích vẫn intelligible khi nghe."
    },
    "ending_payoff_and_transition": {
      "score": 9,
      "evidence_scope": "full",
      "basis": "Ending trả lời trực tiếp mission bằng ba vế dễ nhớ rồi mở đúng câu hỏi mà P02 phải giải quyết."
    }
  }
}
<!-- production-gate:end -->

Derived verdict: `changes_requested` vì `evidence_integrity` fail; không có gate blocked và không có dimension dưới 8.
