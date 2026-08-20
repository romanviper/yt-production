# Modular Production Workflow

## 1. Mental model

Repo separates **decision ownership**, not information ownership.

| Layer | Owns | Does not own |
|---|---|---|
| Research | truth, source, locator, claim, confidence, contradiction, qualification, provenance | story route, carrier, reveal strategy |
| Outline | central question, progression, section objective, entry/exit state, evidence territory, boundaries, continuity | paragraph order, carrier, exact narrative route |
| Writer | factual selection inside allowance, narrative/causal route, POV, scale, imagery, reveal timing, prose craft | truth-ceiling expansion, approval |
| Review | observable outcome judgment and diagnosis | enforcing one preferred storytelling method |
| Harness | authority, write scope, lifecycle, approval, provenance, evidence ceiling, cycle/hash integrity, resource caps | authorship |

Product Agent không sửa control plane. Human approval remains external.

## 2. Current pipeline

`Research`
→ authoritative evidence store

`Outline`
→ architecture + objectives + evidence scope

`Materialize`
→ deterministic section state + truth/evidence handoff

`Draft`
→ creative authorship + bounded on-demand evidence resolution

`Review`
→ outcome-first evaluation

Không có intermediate creative-planning layer trên path mới. `design_section` / `story-plan` chỉ còn compatibility cho legacy products.

## 3. Research: authoritative evidence, not pre-authored story

Mỗi workstream bắt buộc trả:

- `sources.json`;
- `claims.json`;
- `synthesis.md`.

Research giữ source/locator/provenance, chronology, claim/confidence/status, contradiction/counterevidence, qualification và factual limitation.

`materials.json` là **optional evidence-preservation artifact**. Dùng khi primary object/case có detail dễ mất qua compression hoặc provenance/limitation phức tạp. Nó không phải mandatory abstraction giữa claim và writer.

Output mới không bắt buộc `what_audience_follows`, narratability class, carrier role, opening/reversal/ending candidate hay sequence kể chuyện. Legacy fields vẫn có thể tồn tại nhưng không có creative authority.

`consolidate_research.py` luôn giữ source/claim ledgers authoritative. Nếu optional materials tồn tại, chúng được remap provenance như evidence preservation; absence of material không block synthesis/outline.

`research_synthesis` trả `research-synthesis.md`: causal/chronological model, contradictions, confidence/qualification và evidence gaps. `story-material-map.json` là legacy compatibility artifact, không còn output bắt buộc.

## 4. Outline: architecture of inquiry/progression

Current/revised outline dùng schema v4 và đặt:

`script_architecture.writer_authorship_contract_version = 1`

Outline quyết định:

- central question và audience promise;
- đúng ba whole-script acts;
- narrative movements;
- section objective (`narrative_job`);
- entry / exit state;
- section boundary;
- `claim_ids` làm evidence territory;
- dependencies / continuity;
- `transition`;
- word envelope.

Outline không được bắt writer theo một carrier, object sequence, mental imagery sequence, reveal order hay paragraph route.

Legacy C003/older artifacts có thể còn `story_material_contract_version`, `audience_experience`, `material_ids`. Materializer mới đọc được chúng để migration không phá product, nhưng bỏ các field creative-route đó khỏi writer handoff.

Human review ở outline stage đánh giá architecture/evidence scope. Không cần nhìn thấy gần như toàn bộ prose trước khi approve; deep storytelling judgment có thể hợp lệ chỉ xuất hiện ở draft.

## 5. Deterministic section handoff

Sau human-approved outline:

```bash
python scripts/materialize_sections.py products/<slug> --archive-previous-cycle
```

Direct-authoring section được tạo ở `ready_for_draft` với:

- `section.json`: cycle/hash, objective, entry/exit, movements, dependencies, transition;
- `brief.md`: objective, state change, evidence territory, continuity;
- `evidence-pack.json`: approved claims + reviewed supporting source records;
- `narration-pack.json`: truth ceiling, qualifications, guardrails và bounded retrieval scope;
- `continuity-in.md`.

Không tạo `material-pack.json`. Không cần `story-plan.json` trên path mới.

Claims là permissions, không phải danh sách paragraph bắt buộc.

## 6. Writer authorship

`draft_section` nhận destination và truth boundary, không nhận route.

Writer tự quyết:

- fact nào dùng/bỏ trong allowance;
- narrative/causal route;
- POV/scale;
- object/person/process/contrast nếu hữu ích;
- reveal timing;
- exposition placement;
- imagery, vocabulary, rhythm, sentence craft.

Target là **crafted narration intended to be spoken aloud**, không mặc định conversational.

Một route mà Research/Outline/Harness chưa dự đoán vẫn hợp lệ nếu đạt objective, evidence-safe, continuity đúng và không invent.

Concrete-first, before/after, recount-before-interpret, process sequence, raw clue, deletion pass… là optional heuristics. Chúng có thể giúp sửa document mode nhưng không phải schema validity.

## 7. Bounded evidence retrieval

Draft/revision packet có `evidence_access` dùng:

```bash
python scripts/draft_evidence.py products/<slug> <task-id> scope
python scripts/draft_evidence.py products/<slug> <task-id> claims
python scripts/draft_evidence.py products/<slug> <task-id> sources
python scripts/draft_evidence.py products/<slug> <task-id> source --id SRC-0001
python scripts/draft_evidence.py products/<slug> <task-id> search --query "term"
```

Scope được suy ra từ `claim_ids` của section và các reviewed sources support chúng. Không có arbitrary path argument và không scan repo.

Writer có thể tăng factual resolution: measurement, physical description, location, documented action, chronology detail hoặc source detail. Optional evidence-preservation `details` có thể được trả nếu nằm trong cùng claim/source graph.

Nếu Agent đọc thêm passage từ approved source URL/locator và muốn dùng detail mới, ghi nó vào audit trace:

```bash
python scripts/draft_evidence.py products/<slug> <task-id> record \
  --source-id SRC-0001 \
  --parent-locator "reviewed locator" \
  --locator "narrower locator" \
  --detail "source-level factual detail"
```

Mọi capability call ghi full request/response vào `tasks/<task-id>/evidence-trace.jsonl`, file này nằm ngoài model write scope.

Boundary:

> Writer may increase evidence resolution, but may not silently expand the truth ceiling.

New claim, causal conclusion, thesis, contradiction hoặc generalization phải quay về research/evidence authority trước khi được narration như approved fact.

## 8. Outcome-first review

Review hỏi trước:

- section có đạt objective không;
- listener có đi qua progression có ý nghĩa không;
- narration có cảm giác authored không;
- information có thành experience/world/process/relationship phù hợp không;
- listening experience có tốt không;
- causal logic, continuity và evidence integrity có giữ không.

Chỉ sau khi outcome fail mới dùng mechanics làm diagnostic heuristic. Không fail một draft chỉ vì thiếu carrier, raw clue, before/after, process sequence hoặc recount-before-interpret.

Routing hiện hành:

- `prose_execution` → sửa draft/revision;
- `product_architecture` → reopen outline/cycle;
- `evidence` → reopen research/evidence.

Không có `local_design/story-plan` authority trên path mới.

Pseudo-agency chỉ là conditional integrity rule: nếu narration staged audience discovery, evidence phải thực sự accessible trước specialist classification. Không yêu cầu mọi section cho audience tự suy luận.

## 9. Hard boundaries retained

Harness vẫn hard-enforce:

- task authority và allowed writes;
- packet freshness/integrity;
- lifecycle states;
- human approvals;
- cycle/hash integrity;
- source/claim provenance;
- evidence ceiling và qualification;
- no invention;
- contradiction handling;
- context/write caps.

Creative method không được đưa vào hard schema chỉ vì nó từng giúp một draft cụ thể.

## 10. Replay and migration

Current replay path:

`outline → materialize → draft_section`

Legacy products không có direct-authorship marker vẫn có thể dùng story-plan compatibility path. New/revised outline phải dùng `writer_authorship_contract_version: 1`.

Không rewrite product content chỉ để migration/test pass. Nếu một existing outline vẫn encode exact carrier/route từ harness cũ, rebuild outline bằng current architecture harness rồi chờ human approval trước clean draft replay.

## 11. Audit rule for future harness changes

Với mỗi schema/validator/lifecycle/instruction/compiler/evaluation rule, hỏi:

1. Nó bảo vệ hard boundary? → hard-enforce.
2. Nó là observable quality target? → evaluator judge.
3. Nó chỉ mô tả một cách cụ thể để đạt target? → optional heuristic, không schema validity.

Success criterion:

> Harness bảo vệ truth và workflow thật chặt, nhưng không quyết định hộ creative Agent cách kể câu chuyện.
