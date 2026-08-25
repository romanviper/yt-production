# Context Packet — T0035-revise-section-P01

- Product: `sumer-writing`
- Operation: `revise_section`
- Context profile: `creative_revision`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `03_sections/P01/revision-log.md`, `tasks/T0035-revise-section-P01/report.md`, `tasks/T0035-revise-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Task context is this packet plus the bounded evidence capability below. Do not scan the repository.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T0035-revise-section-P01 <capability>`.
Capabilities: `scope`, `resolve_claims`, `claims`, `sources`, `source`, `search`, `record`.
Use it only to increase source-level resolution inside the approved claim/source scope.
Every capability call is audit-logged. If external source reading adds detail, record it through the adapter before relying on it.
New claims, causal conclusions, contradictions or generalizations must be routed back to evidence authority.

# BEGIN INSTRUCTION: system/core/creative-boundaries.md
# Creative Boundaries

These are the only content boundaries the creative Agent must actively carry:

1. Stay inside the current section's approved evidence ceiling and continuity scope.
2. Do not invent people, scenes, thoughts, dialogue, sensory details or causal certainty.
3. Do not imitate a reference creator's wording, cadence, motifs, narrator persona or signature structure.
4. If the intended narrative move needs missing evidence or conflicts with the section's entry/exit state, report the blocker instead of hiding it with prose.

Everything else about ordering, paragraph count, rhythm, opening form and local structure is a creative decision.
# END INSTRUCTION: system/core/creative-boundaries.md

# BEGIN INSTRUCTION: system/standards/channel-constitution.md
# Channel Constitution

## Core value

A system, institution, technology or idea is the protagonist. Follow how pressure forms it, what capabilities it creates, what conflicts/consequences follow, and how it changes, weakens or survives.

## Whole-script architecture

Every script has three audience-facing acts:

- **Opening:** establish the central tension, question and promise.
- **Body:** develop formation, expansion, conflict, consequence and adaptation.
- **Ending:** answer the question and close through consequence or legacy.

The three acts belong to the whole script, not each production section. Local storytelling form is adaptive.

## Voice and authorship

Narration should feel deliberate, clear, weighty and investigative, with expression suited to the subject. It need not be conversational.

Prefer causality to chronology dumps and consequence to trivia. Emotional weight must come from evidenced consequences, not rhetoric.

Inside approved truth/continuity boundaries, the writer owns local structure, POV, pace, factual selection, scale, imagery, reveal timing and phrasing. No carrier, concrete-first, before/after or recount-before-interpret route is universal.

## Conditional audience agency

Only when narration stages discovery/inference, the audience must have had access to the relevant cue before specialist classification. This is an integrity rule for that technique, not a requirement that every section use it.
# END INSTRUCTION: system/standards/channel-constitution.md

# BEGIN INSTRUCTION: system/operations/revise-section.md
# Operation — Revise Section

## Responsibility

Resolve only the user-approved change request.

For canonical direct-authorship work, the packet contains current prose, the approved change request, compact mission/boundary and narration truth-ceiling control, plus a hash-bound diagnosis projection with the review verdict, Issues and Routing only. A legacy packet may retain its full approved story-plan, voice and review context; use those only to preserve established choices. Together, the review diagnosis and user request must identify the observable target, bounded change and pass condition. If the combined authority does not, report a blocker instead of reconstructing omitted context.

This task is the section's single diagnosed revision pass. Do not open another polish loop or broaden the issue set.

Preserve successful creative choices. Use the smallest change that passes the stated acceptance test, unless the approved request explicitly routes the issue back from local design and permits a full section rewrite.

The evidence ceiling, act role, entry/exit state and continuity remain fixed. If the requested fix actually belongs to product architecture or missing evidence, report that blocker instead of compensating with prose.

Update the handoff only when the achieved exit state or continuity facts changed. Record issue IDs and observable results in the revision log; do not describe generic polishing.
# END INSTRUCTION: system/operations/revise-section.md

# BEGIN INPUT: 02_outline/outline.json
{
  "projection_kind": "review_current_next_boundary",
  "outline_sha256": "d707db0c172a9db579593a136791d2b1e629892315e31bedfa0d795b8c92da9d",
  "current": {
    "id": "P01",
    "title": "Trước chữ viết đã có một bài toán phải giải",
    "narrative_job": "Thiết lập các pressure và information practices trước/sát thời điểm proto-cuneiform xuất hiện, đồng thời phá hai shortcut: một invention event duy nhất và token→tablet như đường tiến hóa tất định. Section phải kết thúc khi audience đã hiểu vì sao durable, inspectable records trở nên đáng giá mà chưa cần biết 'ai phát minh chữ viết'.",
    "entry_state": "Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.",
    "exit_state": "Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.",
    "transition": "Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.",
    "non_goal": "Không invention scene; không ethnic attribution; không universal token code; không direct token→tablet genealogy; không biến administrative pressure thành monocause."
  },
  "next": {
    "id": "P02",
    "title": "Hữu ích trước khi thành câu",
    "narrative_job": "Giải thích early record có thể làm công việc có thật trước khi continuous speech hoặc underlying language được recover chắc chắn. Section phải land được usefulness trước khi mở các guardrail về writing threshold, chronology, language và world-first.",
    "entry_state": "Khán giả vẫn có thể nghĩ 'chưa thành câu' đồng nghĩa 'chưa phải công nghệ có sức nặng'.",
    "exit_state": "Khán giả hiểu structured signs/layout có thể giữ repeatable relations đủ để vận hành administration; ranh giới writing/proto-writing và language attribution vẫn phải qualified.",
    "transition": "Một system đã có thể làm việc. Bây giờ câu chuyện cần theo dõi điều gì xảy ra khi writing được dùng cho ngày càng nhiều loại việc khác nhau.",
    "non_goal": "Không definition-first lecture; không chắc hóa Sumerian language; không uncontested world-first; không kể proto-cuneiform như mature cuneiform hay một bước tất định hướng tới alphabet."
  }
}
# END INPUT: 02_outline/outline.json

# BEGIN INPUT: 03_sections/P01/section.json
{
  "section": "P01",
  "title": "Trước chữ viết đã có một bài toán phải giải",
  "mission": "Điều gì khiến việc giữ thông tin bằng những dấu bền trên đất sét trở nên hữu ích?",
  "entry_state": "Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.",
  "exit_state": "Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.",
  "transition": "Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.",
  "target_words": {
    "min": 1050,
    "max": 1550
  }
}
# END INPUT: 03_sections/P01/section.json

# BEGIN INPUT: 03_sections/P01/narration-pack.json
{
  "section": "P01",
  "cycle_id": "C003",
  "truth_ceiling": {
    "claim_ids": [
      "CLM-0011",
      "CLM-0012",
      "CLM-0013",
      "CLM-0014",
      "CLM-0015",
      "CLM-0016",
      "CLM-0017",
      "CLM-0018"
    ]
  }
}
# END INPUT: 03_sections/P01/narration-pack.json

# BEGIN INPUT: 03_sections/P01/draft.md
# P01 — Trước chữ viết đã có một bài toán phải giải

Đừng bắt đầu lịch sử chữ viết bằng một tấm bảng. Hãy bắt đầu bằng một vật còn lạ hơn: một **bulla**. Đó là lớp vỏ đất sét khép quanh những vật nhỏ cũng bằng đất sét, thường được gọi là **token**. Một số token muộn trong bulla rõ ràng có liên quan đến số lượng và kế toán. Nhưng bulla tạo ra một nghịch lý. Khi lớp vỏ đóng lại, các token được gom vào một chỗ—và đồng thời biến khỏi tầm mắt. Muốn nhìn những gì ở trong, phải mở vật đang giữ chúng. Muốn giữ lớp vỏ nguyên vẹn, phải tìm cách đưa thông tin ra ngoài.

Trước câu chuyện về chữ, đã có bài toán vật chất ấy: làm sao giữ một lượng thông tin cho bền mà vẫn khiến nó có thể được sử dụng?

Bây giờ hãy đặt vật nhỏ này trở lại Uruk. Ở giai đoạn liên quan đến sự xuất hiện của chữ hình nêm sơ khai, khu đô thị ấy được ước tính rộng khoảng hai trăm hecta, với hơn bốn mươi nghìn cư dân. Cả hai con số chỉ là ước tính, nhưng quy mô mà chúng gợi ra thì rất rõ. Một lần đếm không còn đứng một mình. Nó nằm giữa nhiều lần chuyển giao, nhiều đối tượng được tính và nhiều hoạt động của các thiết chế.

Trong công việc kế toán, chuyển một lượng hàng mới chỉ là nửa việc. Lượng ấy còn phải có một hình thức để người ta có thể tiếp tục xử lý nó sau khi thao tác ban đầu đã kết thúc. Token cho lượng một hình thức vật chất: thay vì chỉ nói “bao nhiêu”, có những vật nhỏ hiện diện để mang việc đếm. Không phải mọi token thời đồ đá mới đều là một phần của cùng một mã kế toán kéo dài hàng thiên niên kỷ. Nhưng ở những trường hợp muộn đã được đặt trong bulla, chức năng số của một số token đủ rõ để ta theo tiếp đường đi của thông tin.

Đường đi ấy đổi hướng ngay trên lớp vỏ. Ở một số bulla, token được ấn lên phía ngoài; những vết ấn này tương ứng với các dấu số sớm. Bulla lúc đó mang hai cách giữ cùng một lượng: các vật nằm bên trong và dấu hiện ra trên bề mặt. Đây chưa phải một tấm bảng chữ hoàn chỉnh. Nhưng một thay đổi quan trọng đã xảy ra. Muốn biết lượng, người ta không còn nhất thiết chỉ nhìn vào tập vật được cất kín. Bề mặt đất sét cũng có thể làm lượng hiện diện.

Các bảng ghi số đưa khả năng đó đi xa hơn. Trên bảng, dấu số không chỉ gợi về những token đang nằm sau một lớp vỏ. Chính bề mặt trở thành nơi bản ghi tồn tại. Việc đếm vẫn là sợi dây nối chắc nhất giữa các thiết bị có trước chữ và những bảng proto-cuneiform: lượng đi qua nhiều vật mang tin, nhưng thực hành số vẫn có thể được nhận ra. Với các dấu không phải số, mối nối về hình dạng kém chắc chắn hơn nhiều.

Tuy vậy, đừng nghe chuỗi này như một niên biểu thẳng: token rồi bulla, bulla rồi bảng, bảng rồi chữ. Đó là một logic vật chất, không phải một hàng quân thay thế nhau. Tại Tushan, token còn tồn tại cùng các tài liệu viết. Một hình thức mới có thể xuất hiện mà hình thức cũ vẫn tiếp tục làm việc. Vì thế, token, bulla, con dấu, hình ảnh, bảng số và thực hành của các thiết chế nên được nhìn như một **hệ sinh thái ghi nhận**: nhiều giải pháp chồng lấn quanh cùng một bài toán, chứ không phải một phát minh đơn độc xóa sạch mọi thứ trước nó.

Nhìn theo cách đó, điều đáng nhớ không phải tên của từng vật mà là những động tác chúng cho phép. Token làm lượng có hình dạng. Bulla gom những vật mang lượng vào một đơn vị khép kín. Dấu ngoài vỏ đưa một phần thông tin ra bề mặt. Bảng số cho bề mặt tự mang bản ghi. Giữ, gom, niêm phong, đánh dấu: mỗi động tác sắp xếp lại quan hệ giữa lượng, vật và nơi thông tin có thể được tìm thấy.

Đây là nơi quy mô hành chính trở thành một áp lực lớn. Phần tư liệu proto-cuneiform còn bảo tồn được nghiêng mạnh về kế toán và hành chính. Nó cho ta nhận ra bối cảnh ghi nhận chắc hơn là cho phép gọi mọi bảng là trao đổi thị trường, thuế, cống nạp hay phân phối. Những cơ chế ấy không thể đổi tên cho nhau chỉ vì cùng có số và hàng hóa. Dù vậy, điểm chung vẫn hiện ra: các thiết chế đang vận hành cần những lượng có thể được giữ lại và tiếp tục xử lý.

Hành chính không vì thế trở thành nguyên nhân duy nhất của chữ viết. Corpus còn lại có tính chọn lọc, và việc đô thị, thiết chế cùng hệ thống ghi nhận phát triển bên nhau không chứng minh một mũi tên nhân quả một chiều. Cách hiểu hợp lý hơn là một khả năng phản hồi: thiết chế mở rộng tạo thêm áp lực cho hồ sơ; hồ sơ hữu dụng hơn lại có thể tăng năng lực của thiết chế. Đây là mô hình phù hợp với bằng chứng hiện có, không phải một phán quyết rằng ta đã định lượng xong đóng góp của từng thành phần.

Giờ ta có thể trả lời câu hỏi mở đầu. Những dấu bền trên đất sét trở nên hữu ích vì chúng chuyển lượng từ chỗ chỉ được mang bởi vật rời hoặc giấu trong một lớp vỏ sang một bề mặt có thể làm việc như hồ sơ. Ở quy mô Uruk, sự chuyển chỗ ấy gặp đúng áp lực của những hoạt động tổ chức đang mở rộng. Độ bền giúp thông tin còn hiện diện; bề mặt giúp thông tin có thể được tiếp cận; còn quy mô khiến hai khả năng đó đáng để đầu tư.

Câu trả lời ngắn có thể nhớ là: **quy mô tạo nhu cầu, bề mặt làm lượng nhìn thấy, và độ bền giúp công việc tiếp tục.**

Nhưng nhu cầu cùng các thực hành ghi nhận chưa tự động tạo ra một hệ thống dấu mới. Nếu token, bulla, con dấu và bảng số đã cùng góp mặt, điều gì khiến hệ thống dấu mới thực sự khác trước? Đó là câu hỏi tiếp theo.
# END INPUT: 03_sections/P01/draft.md

# BEGIN INPUT: 03_sections/P01/handoff.md
# Handoff — P01

## Trạng thái sau phần

Khán giả rời P01 với một hình ảnh trung tâm: bulla giữ token bên trong nhưng khiến lượng biến khỏi tầm mắt, còn dấu trên bề mặt đưa lượng trở lại nơi có thể tiếp cận. Ở quy mô Uruk, khả năng giữ thông tin bền và tiếp tục xử lý nó gặp áp lực của hoạt động thiết chế.

## Đường kể phải giữ

1. Nghịch lý inside/outside của bulla đặt ra bài toán trước chữ viết.
2. Token → bulla → dấu ngoài vỏ → bảng số là logic thao tác vật chất, không phải niên biểu thay thế tuyến tính.
3. Continuity chắc nhất nằm ở thực hành số; token, bulla, con dấu, hình ảnh, bảng số và thiết chế tạo một ecology chồng lấn.
4. Hành chính là áp lực lớn nhưng không phải nguyên nhân duy nhất; feedback giữa hồ sơ và năng lực thiết chế chỉ là mô hình có điều kiện.
5. Payoff cần nhớ: quy mô tạo nhu cầu, bề mặt làm lượng nhìn thấy, độ bền giúp công việc tiếp tục.

## Continuity sang P02

P01 dừng ở pressure, material recording practices và giá trị của hồ sơ bền. Nó không giải thích cách cấu trúc dấu hay bố cục vận hành, cũng không giải quyết ngưỡng biểu đạt ngôn ngữ. P02 giữ toàn bộ reveal về điều khiến hệ thống dấu mới thực sự khác biệt và hữu ích.

## Evidence boundary

- Không biến toàn bộ token thành một mã kế toán thống nhất.
- Không kể token → tablet → writing như một tuyến tiến hóa duy nhất.
- Không đồng nhất accounting với market, tax, tribute hay redistribution.
- Không biến co-occurrence hoặc feedback thành nhân quả một chiều đã được chứng minh.

Claims sử dụng: CLM-0011–CLM-0018.
# END INPUT: 03_sections/P01/handoff.md

# BEGIN INPUT: 03_sections/P01/review.md
{
  "projection_kind": "revision_diagnosis",
  "section": "P01",
  "review_sha256": "52ca1a0d8e0aaa0d377ee59bfea349922365141c59a96ff21afcd5f03e213ee3",
  "verdict": "changes_requested",
  "issues": "### 1. Bulla bị mô tả như hai bản biểu diễn chắc chắn của cùng một lượng\n\n- **Vị trí quan sát được:** đoạn bắt đầu “Đường đi ấy đổi hướng ngay trên lớp vỏ”, câu “Bulla lúc đó mang hai cách giữ cùng một lượng: các vật nằm bên trong và dấu hiện ra trên bề mặt.”\n- **Failure:** câu khẳng định quan hệ tương đương giữa nội dung bên trong và dấu ngoài bề mặt. Bounded source detail từ `SRC-0011`, locator pp. 6–9, nêu rằng dấu ngoài có thể được tạo bằng token nhưng token được ấn không nhất thiết là token nằm trong bulla; quan hệ contents-to-surface vì vậy chưa được phép chắc hóa.\n- **Effect:** người nghe có thể tin rằng bằng chứng đã xác lập phép đối chiếu một-một giữa hai lớp thông tin, làm yếu trust và vô tình kéo lập luận gần hơn tới direct token→tablet genealogy mà section đang chủ động bác bỏ.\n- **Responsible layer:** `evidence`.\n- **Smallest valid revision scope:** chỉ câu khẳng định tương đương này và, nếu cần để giữ mạch nghe, câu liền kề; không cần đổi cấu trúc section.\n- **Acceptance test:** passage không còn khẳng định dấu ngoài và token bên trong giữ đúng cùng một lượng khi chưa có support; nó vẫn cho người nghe hiểu được việc thông tin số đi ra bề mặt, đồng thời giữ nguyên guardrail chống genealogy tuyến tính.",
  "routing": "Route tới `evidence`. Chỉ sửa câu khẳng định tương đương contents-to-surface và tối đa câu liền kề; không mở lại cấu trúc section hoặc truth ceiling. Sau sửa, review lại đúng acceptance test trên."
}
# END INPUT: 03_sections/P01/review.md

# BEGIN INPUT: 03_sections/P01/change-request.md
# Change Request — P01

Requested by: user

Requested at: 2026-08-25T03:25:57.940538+00:00

## Request

Áp dụng đúng formal review T0034: chỉ sửa câu 'Bulla lúc đó mang hai cách giữ cùng một lượng' và tối đa câu liền kề để bỏ certainty rằng dấu ngoài tương đương chính xác contents bên trong. Vẫn giữ mạch thông tin số đi ra bề mặt, không đổi cấu trúc, hook, payoff, ranh giới P02 hay truth ceiling. Acceptance: không còn contents-to-surface equivalence unsupported.
# END INPUT: 03_sections/P01/change-request.md
