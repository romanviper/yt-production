# Writer Harness — observable direct-output MVP

The immediate goal is to produce a Writer draft quickly **and make the Writer's observable decisions understandable to the Owner**.

If the Owner tells you to write P01, write immediately. Do not wait for an assignment, controller state, budget, Planner, Reviewer, or other agent.

This harness does not decide whether your writing is good or bad. Do not emit PASS/FAIL, scores, rankings or a verdict. The Owner evaluates the prose.

Do not store chain-of-thought, private reasoning, hidden scratchpad or internal-monologue transcripts. Record only observable facts, final decisions, brief stated rationales tied to the supplied inputs, material changes, uncertainties and the resulting artifact.

## Read these three Writer inputs

1. `products/sumer-writing/02_outline/P01-creative-brief.md` — what product/experience you are making and P01's role in it.
2. `products/sumer-writing/02_outline/section-overlays/P01.json` — bounded section territory/change/discovery.
3. `products/sumer-writing/03_sections/P01/historical-substrate.json` — historical reality model and claim boundaries.

The creative brief already distills the approved product brief, benchmark, channel/story/voice direction needed for this attempt. Do not load the old workflow or legacy task contexts just to reconstruct those goals.

If you access any other repo file or external source before finishing the draft, disclose it in `meta.json` and `writing-report.md`. Do not read another Writer's output or Owner feedback on another Writer before finishing.

## Output partition

Use your own partition:

`writer-output/P01/<writer>/`

Current partitions:

- Gemini → `writer-output/P01/gemini/`
- GPT-5.6 Sol → `writer-output/P01/sol/`
- GPT-6 → `writer-output/P01/gpt6/`

A new model may create one short model-name partition.

Each completed attempt contains exactly:

- `draft.md` — listener-facing prose;
- `meta.json` — compact factual execution metadata;
- `writing-report.md` — Owner-readable trace of the writing behavior.

Do not write the draft into `products/`, `runs/` or controller folders.

## Execution sequence

### 1. Write the PRE-WRITE SNAPSHOT first

Create `writing-report.md` and fill only the pre-write sections below **before drafting prose**. Keep this concise. It is not a Planner artifact.

### 2. Write one draft attempt

Write one Vietnamese historical-podcast excerpt for P01.

The goal is not merely to explain the substrate correctly. Use the creative brief to create the intended listener experience while remaining inside the evidence boundaries. For a 450–650-word excerpt, state which part of P01 you are sampling and its local listener change; do not compress the whole section or force its complete exit state into the sample.

Choose the telling freely. Do not force essay structure, hook formulas, beat counts or a generic explanatory template.

Follow the creative brief's viewpoint and pacing guide: default to a broad historical narrator for the P01 opening; move close to a character when their perspective has a purpose, and use first-person voices when useful. Summary and historical explanation are valid storytelling. There is no required scene, dialogue, viewpoint rotation or cinematic technique.

The Owner permits bounded fiction as an optional tool: reconstructed scenes, anonymous/composite characters, plausible dialogue, sensory detail and interiority. Historical inputs constrain claims presented as history, not every invented gesture or line. Distinguish a scene from documentary evidence with light framing where needed; disclose substantial reconstruction by scene in the report. Never use an invented event as evidence for a historical conclusion.

Suggested size is roughly 450–650 words for this learning excerpt, but this is not a hard gate.

### 3. Freeze the draft

Once `draft.md` is complete, do not rewrite or reroll it because of observations made while filling the report. The report must describe the draft that actually existed at completion.

### 4. Finish the POST-WRITE TRACE

Inspect your frozen draft and append the post-write sections. Do not change the draft afterward.

### 5. Write `meta.json`, commit the three files, stop

There is no Writer time budget. Timing is telemetry only. Never fabricate unknown model/session/timing information; use `UNKNOWN` or `null`.

---

# `meta.json` contract

Keep metadata factual and compact.

```json
{
  "schema": "writer-observability-v2",
  "writer": "<partition name>",
  "model": "<actual model if known, otherwise UNKNOWN>",
  "task": "P01",
  "attempt": 1,
  "owner_instruction": "<short faithful summary of the instruction that started this attempt>",
  "branch": "<current branch if known, otherwise UNKNOWN>",
  "starting_commit": "<HEAD before this attempt if known, otherwise UNKNOWN>",
  "inputs_read": [
    "products/sumer-writing/02_outline/P01-creative-brief.md",
    "products/sumer-writing/02_outline/section-overlays/P01.json",
    "products/sumer-writing/03_sections/P01/historical-substrate.json"
  ],
  "extra_context_accessed": [],
  "other_writer_outputs_read": false,
  "owner_feedback_on_other_writer_read_before_draft": false,
  "rerolled": false,
  "draft_word_count": 0,
  "timing": {
    "seconds": null,
    "source": "UNKNOWN"
  },
  "outputs": ["draft.md", "writing-report.md"]
}
```

If a fact cannot be known truthfully, use `UNKNOWN`/`null` rather than guessing.

---

# Quy ước cho `writing-report.md`

`writing-report.md` phải được viết bằng **tiếng Việt tự nhiên, rõ ràng, dễ đọc đối với Owner**.

Không viết report theo giọng tài liệu kỹ thuật hoặc prompt engineering. Không dùng tiếng Anh làm nhãn mặc định nếu có thể nói tự nhiên bằng tiếng Việt. Chỉ giữ nguyên tên file, path, model, ID nguồn như `HS-P01-0004`, hoặc thuật ngữ chuyên môn khi việc dịch sẽ làm mất nghĩa.

Ưu tiên câu ngắn, bảng và bullet. Mục tiêu là để Owner đọc và hiểu Writer đã làm gì, không phải để Writer tự biện hộ hay chứng minh mình đúng.

Dùng đúng các heading dưới đây theo thứ tự.

## TRƯỚC KHI VIẾT

### 1. Tôi hiểu nhiệm vụ lần này là gì

Trong 1–3 câu, nói lại bằng tiếng Việt tự nhiên Writer hiểu Owner đang yêu cầu tạo ra sản phẩm gì.

### 2. Tôi hiểu câu chuyện lớn và vai trò của P01 như thế nào

Nói bằng lời của mình:

- podcast dài này đang kể câu chuyện lớn nào;
- P01 đóng vai trò gì trong hành trình đó;
- điều gì sẽ bị mất nếu P01 chỉ còn là một đoạn giải thích về sự thận trọng khảo cổ học.

Bám vào `P01-creative-brief.md`, không tự phát minh mục tiêu sản phẩm mới.

### 3. Tôi muốn người nghe thay đổi nhận thức như thế nào

Ghi rõ:

- trước đoạn này người nghe có thể đang hình dung điều gì;
- sau đoạn này họ nên hiểu khác đi như thế nào;
- câu hỏi hoặc sự tò mò nào nên kéo họ sang phần tiếp theo;
- nếu chất liệu cho phép, cảm giác hoặc sức nặng nào Writer muốn tạo ra.

Đây không chỉ là kết luận factual. Hãy mô tả trải nghiệm mà Writer định tạo ra cho người nghe.

### 4. Tôi định kể đoạn này như thế nào

Ghi những lựa chọn cuối cùng trước khi bắt đầu viết prose:

- mở ở đâu hoặc bằng điều gì;
- trục kể hoặc câu hỏi trung tâm;
- đích đến của đoạn;
- điểm nhìn chủ đạo và điều nó giúp người nghe biết/cảm nhận; nếu định tiến gần nhân vật hoặc dùng ngôi thứ nhất, nói ngắn mục đích và lúc nào nên rời điểm nhìn đó (không cần dùng đủ ba cách);
- nơi định tóm lược hoặc kể gần hơn, và điều đáng khám phá khiến bạn chọn nhịp ấy.

Chỉ ghi lựa chọn cuối cùng trong vài dòng, không lập kế hoạch từng câu hoặc cam kết số cảnh, số lần chuyển điểm nhìn. Nhịp và điểm nhìn có thể thay đổi trong lúc viết; report ghi nhận điều thực tế đã làm.

Với mỗi lựa chọn quan trọng, nếu có thể hãy chỉ ra creative-brief clause, overlay field, substrate ID hoặc chỉ dẫn của Owner đã tác động tới lựa chọn đó.

### 5. Tôi dự định dựa vào bằng chứng nào

Liệt kê những overlay field / historical-substrate ID Writer dự định dùng và mỗi nguồn sẽ giúp làm gì trong đoạn kể.

### 6. Những ranh giới bằng chứng tôi đang mang theo

Chỉ liệt kê những boundary thực sự có thể ảnh hưởng tới cách kể.

Với mỗi boundary, nói rõ Writer dự định xử lý nó theo cách nào, bằng ngôn ngữ tự nhiên, chẳng hạn:

- bỏ chi tiết không đủ căn cứ;
- thêm một qualifier ngắn trong prose;
- chỉ ghi trong report, không đưa vào lời kể;
- biến uncertainty thành nội dung listener-facing vì bản thân uncertainty đó có ý nghĩa kể chuyện.

Không mặc định rằng một boundary phải được nói cho người nghe chỉ vì nó tồn tại.

---

## SAU KHI VIẾT

### 7. Bản draft thực tế đi như thế nào

Map bản draft đã freeze từ đầu tới cuối.

| Vị trí trong draft | Đoạn này đang làm gì với người nghe | Nguồn / substrate ID | Loại nội dung |
| --- | --- | --- | --- |
| ¶1 | ... | HS-P01-... | dữ kiện / suy luận / framing / tái dựng sáng tạo |

### 8. Mục tiêu sản phẩm đã đi vào prose ở đâu

Cho thấy những mục tiêu lớn hơn và vai trò P01 thực sự xuất hiện ở đâu trong draft.

| Mục tiêu/chức năng đã định | Vị trí trong draft | Người nghe thực sự nhận được gì |
| --- | --- | --- |
| đặt ra bài toán lịch sử trước khi có “writing” | ¶... | ... |
| tạo lực kéo sang câu hỏi tiếp theo | ¶... | ... |

Nếu một mục tiêu đã định trước khi viết nhưng không xuất hiện trong draft, nói thẳng điều đó. Không PASS/FAIL.

### 9. Từ nguồn tới câu chữ

Với mỗi khẳng định lịch sử quan trọng hoặc cầu nối nhân quả được trình bày như thật, chỉ ra căn cứ. Chi tiết tái dựng gom theo cảnh ở mục 10: nêu nền lịch sử, phần đã sáng tạo và cách báo hiệu; không ép từng cử chỉ, âm thanh hay câu thoại hư cấu phải có nguồn riêng.

| Vị trí hoặc cụm từ ngắn trong draft | Nguồn/căn cứ | Nguồn thực sự cho phép nói gì | Writer đã thêm hoặc biến đổi gì |
| --- | --- | --- | --- |
| ... | HS-P01-0004 | ... | nén ý / suy luận / framing / không thêm |

Không được nói nguồn support nhiều hơn nội dung thực tế của nguồn.

### 10. Những phần Writer tự thêm hoặc suy ra

Liệt kê những nội dung đáng kể không được nói trực tiếp trong historical inputs. Với mỗi mục, dùng một mô tả tiếng Việt dễ hiểu như:

- suy luận thận trọng từ bằng chứng;
- framing để kể chuyện;
- tái dựng sáng tạo;
- chưa được support chắc chắn / còn bất định.

Nếu không có, ghi `Không có`.

### 11. Ranh giới bằng chứng đã ảnh hưởng draft thực tế ra sao

| Boundary | Writer đã xử lý thế nào | Nếu lọt vào lời kể thì ở đâu | Nó có biến thành giọng giải trình phương pháp không? |
| --- | --- | --- | --- |
| ... | bỏ / qualifier ngắn / kể trực tiếp | ¶... / không có | có / không |

Mục này tồn tại để Owner thấy evidence discipline đã âm thầm bảo vệ độ chính xác hay đã tràn ra thành methodological exposition.

### 12. Những gì thay đổi so với ý định trước khi viết

| Trước khi viết định làm gì | Cuối cùng đã viết gì | Điều quan sát được nào khiến hướng đi thay đổi |
| --- | --- | --- |
| ... | ... | ... |

Nếu không có thay đổi đáng kể, ghi `Không có thay đổi đáng kể`.

### 13. Phần nào là do đầu vào thiếu, phần nào là do lựa chọn của Writer

Tách rõ hai nhóm:

**Giới hạn của đầu vào:** chất liệu lịch sử nào còn thiếu khiến Writer khó tạo human action, pressure, consequence, scene detail hoặc causal movement phong phú hơn.

**Lựa chọn của Writer:** những nơi chất liệu cho phép một cách triển khai khác nhưng Writer chọn nhịp, mức chi tiết hoặc điểm nhìn hiện tại. Giải thích và tóm lược không tự thân là điểm yếu; một cảnh rất chi tiết cũng có thể ít khám phá.

Không dùng “đầu vào thiếu” như lời bào chữa chung cho toàn bộ draft.

### 14. Những rủi ro Writer tự nhìn thấy trong output

Không chấm điểm và không tuyên bố draft thành công/thất bại. Chỉ ra những chỗ cụ thể có thể có vấn đề, ví dụ:

- giải thích lặp hoặc rời mạch chuyện; không coi mọi lời giải thích của narrator là lỗi;
- bám động tác vụn trong khi tình thế/nhận thức không tiến;
- hạn tri trước khi người nghe có lý do quan tâm, hoặc chuyển điểm nhìn mà không rõ ai biết điều gì;
- câu chuyện không tiến lên;
- mục tiêu sản phẩm biến mất phía sau một điểm factual hẹp;
- quá trừu tượng thay vì có object/action/process cụ thể;
- thiếu sự hiện diện của con người dù evidence cho phép;
- quy mô không dịch chuyển;
- nén quá mức hoặc lặp ý;
- đi quá xa bằng chứng;
- quá thận trọng làm câu chuyện phẳng;
- boundary bằng chứng tràn vào lời kể thành giọng phương pháp luận;
- một instruction nào đó làm prose bị méo rõ rệt.

Dùng số đoạn hoặc một cụm ngắn để Owner có thể nhìn đúng cùng vị trí.

### 15. Những gì đã xảy ra trong phiên viết

Nói rõ:

- có đọc thêm file repo nào ngoài ba input chính không;
- có dùng nguồn/search bên ngoài không;
- có nhìn thấy/đọc output Writer khác không;
- có nhìn thấy/đọc feedback của Owner về Writer khác không;
- có tạo hơn một prose attempt không;
- timing nếu thực sự biết, nếu không ghi `UNKNOWN`.

Sau đó dừng. Không review Writer khác, không rank model, không sửa lại draft đã freeze và không sửa harness.
