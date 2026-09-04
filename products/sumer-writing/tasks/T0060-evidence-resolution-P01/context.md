# Context Packet — T0060-evidence-resolution-P01

- Product: `sumer-writing`
- Operation: `evidence_resolution`
- Context profile: `research`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/materials.json`, `tasks/T0060-evidence-resolution-P01/report.md`, `tasks/T0060-evidence-resolution-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Only the material inside this packet is task context. Do not scan the repository.

# BEGIN INSTRUCTION: system/standards/evidence.md
# Evidence Standard

## Claim protocol

`claim → falsification criterion → evidence hierarchy → contradiction → classification → narrative use`

Claim được phân loại `fact`, `inference`, `contested`, `unknown`; trạng thái `open`, `supported`, `qualified`, `rejected`, `blocked`.

## Hierarchy

1. Primary evidence/corpus/artefact có provenance.
2. Scholarly monograph, chapter, paper, handbook, catalogue.
3. Expert interpretation xác định được chuyên môn.
4. University/museum/academic encyclopedia.
5. Documentary, podcast, báo, blog và video: discovery, không tự gánh claim trụ cột.

Source `reviewed` phải có locator và note về giới hạn. Link không đồng nghĩa đã đọc.

## Historical restraint

- Bất đồng học thuật phải được lưu dưới `counterevidence`/`alternatives`.
- Không chọn giả thuyết vì cinematic hơn.
- Không biến absence of evidence thành evidence of absence.
- “First”, “oldest”, “invented”, “caused” luôn cần definition và comparison scope.
- Direct quote cần source, locator, translation attribution và rights flag.

Accuracy governs assertions about the historical world; it does not require every non-evidentiary connective particular in a clearly representative reconstruction to have happened as narrated. Keep three layers legible:
1. **Documented fact:** assertion maps to reviewed evidence and preserves qualification.
2. **Qualified inference:** uncertainty remains visible and cannot become fact through confident prose.
3. **Representative reconstruction:** plausible ordinary particulars may embody approved conditions, but cannot establish a new practice, institution, technology, chronology, measurement, motive, causal conclusion or unique historical outcome.

## Source relation and distance

Every source must be understood by its relation and temporal distance to the narrated event:
- `contemporary_material`: physical artefact, inscription, administrative record from the time.
- `contemporary_interested_account`: royal display, self-serving decree, official bulletin.
- `later_copy`: scribal exercise or transmission preserved centuries after the event.
- `retrospective_literature`: epic, legend, commemorative chronicle.
- `cultural_tradition`: enduring folklore or subsequent oral synthesis.
- `modern_hypothesis`: scholarly model or reconstructive theory.

Later literary copy must never be presented as contemporary eyewitness testimony; royal propaganda must not masquerade as neutral report; heterogeneous legends cannot be fused into an unqualified biography; and modern hypothesis must remain qualified.

## Decision ownership

Research owns truth; Outline owns architecture/evidence territory; Writer owns authorship inside that territory.

Evidence compression may preserve source-level detail, but preserved detail must not become an upstream creative decision about how the story must be told.

## Material affordances and evidence preservation

Do not compress every source into propositions alone. When available inside scope, retain the raw material from which a story can be authored:
- `kind` and neutral `label`;
- linked claim and source IDs with narrow locators;
- `actor` or acting system, `object_or_trace` when directly supported;
- `documented_action` or `explicit_sequence`;
- `time`, `place`, `physical_description`, `measurement` or `spatial_relation`;
- `unresolved_question` or `later_evidence` that changes an interpretation;
- `source_relation` and temporal distance;
- `limitations` and `representativeness`.

These fields are evidence observations. They must not assign an opening, focal carrier, reversal, climax, ending, emotional beat or narrative route. Do not introduce a narratability score.

Every material record keeps four epistemic layers visible to downstream retrieval:
observed/materially attested detail; source-supported functional inference;
representative operational reconstruction; qualified live hypothesis; and
prohibited/rejected inference.
Concrete wording must not collapse those layers. In particular, a plausible actor
or reconstructed workflow is not `documented_action`, and representativeness is
always qualified to the source-supported corpus or context.

## Writer retrieval boundary

A writer may increase evidence resolution inside the approved section territory through the bounded evidence capability.

Permitted retrieval includes reviewed source records, locators, notes and preserved source-level details that support approved section claims. Retrieval must be scoped to source IDs already reachable from those claims and must be logged so the context can be reconstructed.

Writer may use retrieved factual detail such as measurement, physical description, location, documented action, chronology detail or an explicit source sequence when the source directly supports it.

Writer may **not** silently turn retrieval into a larger truth ceiling. A new claim, causal conclusion, thesis, contradiction or generalization must return to research/evidence authority before it enters narration as approved fact.

No free repo scan. No uncited session-memory fact may override repository evidence authority.
# END INSTRUCTION: system/standards/evidence.md

# BEGIN INSTRUCTION: system/operations/evidence-resolution.md
# Operation — Evidence Resolution

## Responsibility

Recover and preserve high-resolution, source-level material affordances for a bounded section from already approved sources, without widening the section's truth ceiling or pre-authoring narrative routes.

When a section's evidence territory contains only abstract claims and propositions, `evidence_resolution` inspects the approved source records and locators to extract concrete historical particulars that allow a writer to author a nonfiction story:
- actual objects, artefacts, tablets, inscriptions, or physical traces;
- documented actions and actors/systems directly supported by the source;
- explicit source sequences (e.g. administrative steps, excavation strata, or inscription order);
- physical descriptions, measurements, and spatial/topographical relations;
- unresolved questions visible in surviving evidence;
- subsequent discoveries or later evidence that changed historical interpretation;
- source genre and temporal distance (`contemporary_material`, `contemporary_interested_account`, `later_copy`, `retrospective_literature`, `cultural_tradition`, `modern_hypothesis`).

`evidence_resolution` owns evidence preservation resolution, **not** story design:
- It does **not** author a story plan, scene, camera angle, opening, or climax.
- It does **not** assign narrative roles or narratability scores.
- It does **not** introduce new claims, new causal conclusions, or synthetic generalizations outside approved research authority.
- If the approved sources cannot support a nonfiction movement, it must stop and report a blocker for owner decision rather than manufacturing historical incidents or inventing details.

## Required inputs

- `02_outline/outline.json`
- `03_sections/{section}/section.json`
- `03_sections/{section}/brief.md`
- `03_sections/{section}/evidence-pack.json`
- `03_sections/{section}/materials.json`

## Optional inputs

- `03_sections/{section}/evidence-resolution-request.md`

## Required outputs

- `03_sections/{section}/materials.json`

## Contract rules

1. Every material record must specify:
   - `id`: namespaced identifier (e.g. `{section}-MAT-###` or global `MAT-####`);
   - `kind`: `object`, `actor`, `place`, `process`, `record`, or `trace`;
   - `label`: neutral descriptive label;
   - `claim_ids`: subset of approved section claims;
   - `source_refs`: source IDs from the section evidence pack with narrow, specific locators;
   - `limitations`: explicit boundaries on what the evidence does and does not prove;
   - `source_relation`: classification of source proximity to the narrated reality.
   - `epistemic_layers`: five explicit lists named `observed`,
     `functional_inference`, `representative_reconstruction`, and
     `qualified_live_hypothesis`, plus `prohibited_or_rejected_inference`.
     Each entry has a `statement`; every
     non-observed entry also has a source-honest `qualification`.
2. Concrete factual affordances must preserve their epistemic layer. A manufacture
   action visible in an artifact may be `documented_action`; a complete workflow
   assembled from several sources is a representative reconstruction, never a
   documented incident. Unknown actors remain unknown; plausible roles are labeled
   inferred. Representativeness claims require a qualified inference and bounded
   source scope—never unsupported `universal`, `standard`, or `canonical`.
   Rejected inference is a red-line surface, not a positive Writer affordance.
3. Output materials must be consolidated into the section territory and available to the writer via the bounded evidence broker.
# END INSTRUCTION: system/operations/evidence-resolution.md

# BEGIN INPUT: 02_outline/outline.json
{
  "schema_version": 4,
  "status": "approved",
  "cycle_id": "C003",
  "sections": [
    {
      "id": "P01",
      "order": 1,
      "title": "Trước chữ viết đã có một bài toán phải giải",
      "mission": "Điều gì khiến việc giữ thông tin bằng những dấu bền trên đất sét trở nên hữu ích?",
      "movement_ids": [
        "M01"
      ],
      "narrative_job": "Thiết lập các pressure và information practices trước/sát thời điểm proto-cuneiform xuất hiện, đồng thời phá hai shortcut: một invention event duy nhất và token→tablet như đường tiến hóa tất định. Section phải kết thúc khi audience đã hiểu vì sao durable, inspectable records trở nên đáng giá mà chưa cần biết 'ai phát minh chữ viết'.",
      "entry_state": "Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.",
      "exit_state": "Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.",
      "historical_change": {
        "from": "Bằng chứng Late Uruk lưu giữ số lượng và sự xác thực trên nhiều vật mang và thực hành bằng đất sét khác nhau.",
        "to": "Thông tin số ngày càng xuất hiện trực tiếp trên các bề mặt đất sét bền, bên cạnh các dấu xác thực."
      },
      "earned_meaning": "Việc ghi chép Late Uruk không xuất hiện như một invention event duy nhất: thông tin số và xác thực đã được vật chất hóa qua nhiều thực hành đất sét, trong đó có những bề mặt bền có thể tiếp tục được kiểm tra sau tình huống trực tiếp.",
      "claim_ids": [
        "CLM-0011",
        "CLM-0012",
        "CLM-0013",
        "CLM-0014",
        "CLM-0015",
        "CLM-0016",
        "CLM-0017",
        "CLM-0018"
      ],
      "dependencies": [],
      "transition": "Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.",
      "target_words": {
        "min": 1050,
        "max": 1550
      },
      "non_goal": "Không invention scene; không ethnic attribution; không universal token code; không direct token→tablet genealogy; không biến administrative pressure thành monocause."
    }
  ]
}
# END INPUT: 02_outline/outline.json

# BEGIN INPUT: 03_sections/P01/section.json
{
  "schema_version": 4,
  "id": "P01",
  "title": "Trước chữ viết đã có một bài toán phải giải",
  "order": 1,
  "status": "needs_evidence_resolution",
  "human_approved": false,
  "dependencies": [],
  "narrative_job": "Thiết lập các pressure và information practices trước/sát thời điểm proto-cuneiform xuất hiện, đồng thời phá hai shortcut: một invention event duy nhất và token→tablet như đường tiến hóa tất định. Section phải kết thúc khi audience đã hiểu vì sao durable, inspectable records trở nên đáng giá mà chưa cần biết 'ai phát minh chữ viết'.",
  "entry_state": "Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.",
  "exit_state": "Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.",
  "target_words": {
    "min": 1050,
    "max": 1550
  },
  "cycle_id": "C003",
  "outline_sha256": "22ba42e198615bb75bcb6db0aac25bc468a0c06a7c0858f114ce5c5b564f2d25",
  "mission": "Điều gì khiến việc giữ thông tin bằng những dấu bền trên đất sét trở nên hữu ích?",
  "transition": "Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.",
  "historical_change": {
    "from": "Bằng chứng Late Uruk lưu giữ số lượng và sự xác thực trên nhiều vật mang và thực hành bằng đất sét khác nhau.",
    "to": "Thông tin số ngày càng xuất hiện trực tiếp trên các bề mặt đất sét bền, bên cạnh các dấu xác thực."
  },
  "earned_meaning": "Việc ghi chép Late Uruk không xuất hiện như một invention event duy nhất: thông tin số và xác thực đã được vật chất hóa qua nhiều thực hành đất sét, trong đó có những bề mặt bền có thể tiếp tục được kiểm tra sau tình huống trực tiếp.",
  "movement_ids": [
    "M01"
  ],
  "macro_movements": [
    {
      "id": "M01",
      "title": "Trước chữ viết đã có một bài toán phải giải",
      "narrative_job": "Xác lập formation pressure và ecology: nhu cầu giữ thông tin hành chính/xác thực tăng trong bối cảnh thiết chế lớn hơn, nhưng evidence không cho phép một nguyên nhân duy nhất hay một genealogy tuyến tính. Movement phải khiến câu hỏi chuyển từ 'ai phát minh?' sang 'những áp lực và thực hành nào khiến durable recording trở nên hữu ích?'.",
      "entry_state": "Nguồn gốc được tưởng như một invention event đơn lẻ.",
      "exit_state": "Nguồn gốc được hiểu như một quá trình nhiều thực hành và nhiều áp lực cùng hội tụ; administration là trọng tâm nhưng không phải monocause."
    }
  ],
  "acts": [
    {
      "id": "A01",
      "role": "opening",
      "title": "Khi một xã hội cần trí nhớ ngoài con người"
    }
  ],
  "prose_provenance": {
    "task_id": "T0059-draft-section-P01",
    "operation": "draft_section",
    "submitted_at": "2026-09-04T03:58:22.782874+00:00",
    "draft_sha256": "3d96ddf19ed7633d4f23c61b2cb1d15b863cf202e7cad433b183c9fed38cb9ff",
    "handoff_sha256": "2a3c98abf960f58e52e844b394503b96c53d7faafee715b6122f6ad6c3cf348d",
    "schema_version": 2,
    "packet_schema_version": 5,
    "task_packet_sha256": "fd2c493a4d18d59fc941e448beaeda9e854948a39564b7d82103579e5fa5a78f"
  }
}
# END INPUT: 03_sections/P01/section.json

# BEGIN INPUT: 03_sections/P01/brief.md
# P01 — Trước chữ viết đã có một bài toán phải giải

Cycle: `C003`

## Whole-script acts

- opening — Khi một xã hội cần trí nhớ ngoài con người

## Macro movements

- M01 — Trước chữ viết đã có một bài toán phải giải

## Section objective

Thiết lập các pressure và information practices trước/sát thời điểm proto-cuneiform xuất hiện, đồng thời phá hai shortcut: một invention event duy nhất và token→tablet như đường tiến hóa tất định. Section phải kết thúc khi audience đã hiểu vì sao durable, inspectable records trở nên đáng giá mà chưa cần biết 'ai phát minh chữ viết'.

## Entry state

Chữ viết được hình dung như một ý tưởng xuất hiện đột ngột.

## Exit state

Khán giả hiểu formation là một ecology gồm numerical practices, seals/bullae/tablets và institutional demand; administration là pressure lớn nhưng không phải nguyên nhân duy nhất.

## Evidence territory

- CLM-0011
- CLM-0012
- CLM-0013
- CLM-0014
- CLM-0015
- CLM-0016
- CLM-0017
- CLM-0018

## Transition

Nếu nhu cầu và các recording practices đã tồn tại, câu hỏi tiếp theo là điều gì khiến hệ thống dấu mới thực sự khác biệt và hữu ích.

## Continuity in

Không có.

## Continuity out

Không có.

## Non-goal

Không invention scene; không ethnic attribution; không universal token code; không direct token→tablet genealogy; không biến administrative pressure thành monocause.
# END INPUT: 03_sections/P01/brief.md

# BEGIN INPUT: 03_sections/P01/evidence-pack.json
{
  "schema_version": 3,
  "section": "P01",
  "claims": [
    {
      "id": "CLM-0011",
      "statement": "Numerical systems provide the strongest material continuity between pre-writing devices and proto-cuneiform.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ],
      "counterevidence": "Continuity of individual non-numerical sign shapes is much less secure.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-001"
        }
      ]
    },
    {
      "id": "CLM-0012",
      "statement": "Neolithic clay objects called tokens were multifunctional; their existence does not prove a millennia-long standardized accounting code.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0009"
      ],
      "counterevidence": "Some late simple tokens in bullae clearly served numerical/accounting functions.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-002"
        }
      ]
    },
    {
      "id": "CLM-0013",
      "statement": "The direct token→tablet→writing sequence is too linear; seals, iconography, bullae, numerical tablets and institutional practice formed a parallel ecology.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0009",
        "SRC-0003"
      ],
      "counterevidence": "Exact contribution of each component cannot be quantified.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-003"
        }
      ]
    },
    {
      "id": "CLM-0014",
      "statement": "Administrative scale is a major formation pressure but not evidence that administration was the sole cause of writing.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ],
      "counterevidence": "Preserved earliest texts are overwhelmingly administrative, but corpus survival is selective.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-004"
        }
      ]
    },
    {
      "id": "CLM-0015",
      "statement": "The evidence supports a feedback model: expanding institutions demanded records, and better records could expand institutional capacity.",
      "type": "inference",
      "confidence": "medium",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0003"
      ],
      "counterevidence": "Downstream effects require WS06 case studies; WS02 cannot establish them alone.",
      "narrative_implication": "Use only with the stated confidence and boundary.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-005"
        }
      ]
    },
    {
      "id": "CLM-0016",
      "statement": "The preserved proto-cuneiform corpus can distinguish accounting contexts more securely than it can distinguish market exchange from tax, tribute or redistribution.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0001",
        "SRC-0010"
      ],
      "counterevidence": "Named agents, commodities, metrology and document structure sometimes narrow the transaction, but sign readings and institutional context remain incomplete.",
      "narrative_implication": "Use 'accounting/administrative transfer' unless reciprocity or institutional flow is independently demonstrated.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-006"
        }
      ]
    },
    {
      "id": "CLM-0017",
      "statement": "Redistribution, labor coordination, obligation and ownership are not interchangeable formation mechanisms: each requires different evidence beyond the presence of numbers and commodities.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0005",
        "SRC-0001",
        "SRC-0010"
      ],
      "counterevidence": "A single tablet may participate in more than one mechanism, and early terminology is partly reconstructed.",
      "narrative_implication": "Label the mechanism only when flows, persons, quotas, duration, seals or transfer conditions support it.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-007"
        }
      ]
    },
    {
      "id": "CLM-0018",
      "statement": "Co-occurrence between urban institutional growth and record systems establishes pressure and compatibility, not a one-way proof that either caused the other.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0003",
        "SRC-0011"
      ],
      "counterevidence": "Later cases may demonstrate capacity effects, but those belong to WS06 and cannot be back-projected.",
      "narrative_implication": "Present the WS02 feedback loop as a hypothesis to be tested, not as a completed causal verdict.",
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-CLM-008"
        }
      ]
    }
  ],
  "sources": [
    {
      "id": "SRC-0001",
      "title": "Proto-Cuneiform Account-Books and Journals",
      "author": "Robert K. Englund",
      "year": 2004,
      "type": "scholarly chapter / corpus synthesis",
      "authority": "Leading specialist synthesis grounded in the archaic tablet corpus and CDLI work.",
      "url": "https://cdli.earth/files-up/publications/englund2004a.pdf",
      "locators": [
        "pp. 24–27 (PDF pp. 2–5), especially chronology figure and discussion of Uruk IV/III corpus",
        "pp. 24–31",
        "pp. 28–31"
      ],
      "status": "reviewed",
      "limitations": [
        "Chronological ranges and corpus counts reflect the state of publication in 2004; some causal interpretation belongs to WS02.",
        "Older chronology; causal interpretation remains debated.",
        "Earliest corpus only."
      ],
      "notes": [
        "Supports ca. 3300 BCE emergence, relative Uruk IV→III sequence, overwhelmingly administrative earliest corpus, and caution around token continuity.",
        "Selected for this workstream's bounded question."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-001"
        },
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-002"
        },
        {
          "workstream": "WS05",
          "local_id": "WS05-SRC-001"
        }
      ]
    },
    {
      "id": "SRC-0003",
      "title": "Writing in Early Mesopotamia: Beyond the Meme",
      "author": "Massimo Maiocchi",
      "year": 2019,
      "type": "peer-reviewed scholarly chapter",
      "authority": "Assyriological synthesis focused on early Mesopotamian writing, semiotics and material systems.",
      "url": "https://iris.unive.it/retrieve/e4239dde-83dd-7180-e053-3705fe0a3322/Maiocchi%20M.%202019%2C%20Writing%20in%20Early%20Mesopotamia%20--%20Beyond%20the%20Meme.pdf",
      "locators": [
        "pp. 410–412 (PDF pp. 15–17), especially discussion of glottographic/semasiographic boundary",
        "pp. 410–412"
      ],
      "status": "reviewed",
      "limitations": [
        "The chapter advocates a fluid continuum; terminology is analytical rather than a universally accepted threshold definition.",
        "Framework-oriented rather than a new excavation report."
      ],
      "notes": [
        "Useful counterweight to a binary true-writing/proto-writing distinction and to a linear token→tablet story.",
        "Selected for this workstream's bounded question."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-003"
        },
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-004"
        }
      ]
    },
    {
      "id": "SRC-0005",
      "title": "Visible Language: Inventions of Writing in the Ancient Middle East and Beyond",
      "author": "Christopher Woods (ed.)",
      "year": 2010,
      "type": "academic museum catalogue / comparative synthesis",
      "authority": "University of Chicago Oriental Institute catalogue curated by a Sumerologist.",
      "url": "https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/oimp32.pdf",
      "locators": [
        "comparative chronology and essays on earliest Mesopotamian and Egyptian writing; catalogue overview",
        "pp. 33–50; development of accounting systems",
        "Mesopotamian writing essays"
      ],
      "status": "reviewed",
      "limitations": [
        "Catalogue compresses specialist disagreements for comparative presentation; use for comparison scope, not exact Uruk stratigraphy.",
        "Comparative overview; some pathways remain hypothetical.",
        "Catalogue compresses disagreements."
      ],
      "notes": [
        "Treats Mesopotamia and Egypt as roughly contemporary independent inventions; supports avoiding an unqualified unique 'world first' claim.",
        "Selected for this workstream's bounded question."
      ],
      "provenance": [
        {
          "workstream": "WS01",
          "local_id": "WS01-SRC-005"
        },
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-001"
        },
        {
          "workstream": "WS03",
          "local_id": "WS03-SRC-002"
        }
      ]
    },
    {
      "id": "SRC-0009",
      "title": "Reconsidering ‘Tokens’",
      "author": "Lucy E. Bennison-Chapman, 2019",
      "year": null,
      "type": "peer-reviewed article",
      "authority": "Systematic archaeological reassessment",
      "url": "https://www.cambridge.org/core/journals/cambridge-archaeological-journal/article/reconsidering-tokens-the-neolithic-origins-of-accounting-or-multifunctional-utilitarian-tools/7E6C04CB040AD8AA0EA84B94D4D275C4",
      "locators": [
        "abstract and pp. 233–259"
      ],
      "status": "reviewed",
      "limitations": [
        "Full text access limited; abstract supports multifunctionality critique."
      ],
      "notes": [
        "Selected for this workstream's bounded question."
      ],
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-003"
        }
      ]
    },
    {
      "id": "SRC-0010",
      "title": "A Quantitative Analysis of Proto-Cuneiform Sign Use in Archaic Tribute",
      "author": "Logan Born and Kathryn Erin Kelley, 2021",
      "year": null,
      "type": "peer-reviewed corpus study",
      "authority": "CDLI corpus-based quantitative analysis",
      "url": "https://cdli.earth/articles/cdlb/2021-6",
      "locators": [
        "§§1–3; corpus definition, sign-frequency and genre limits",
        "§§1–3; 6,726-artifact working corpus and sign-use method"
      ],
      "status": "reviewed",
      "limitations": [
        "Sign-frequency patterns do not by themselves establish sign meanings or causal direction.",
        "Readability, sign variants, genre assignment and corpus growth constrain quantitative conclusions."
      ],
      "notes": [
        "Used to test how far administrative subgenres can be distinguished from the preserved corpus.",
        "Used to separate observed sign distribution from reconstructed linguistic value."
      ],
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-005"
        },
        {
          "workstream": "WS03",
          "local_id": "WS03-SRC-005"
        }
      ]
    },
    {
      "id": "SRC-0011",
      "title": "Cuneiform Script and the Origin of the Oldest Writing Systems in Comparative Perspective",
      "author": "Massimo Maiocchi, 2015",
      "year": null,
      "type": "specialist institutional essay",
      "authority": "Institute for the Study of Ancient Cultures",
      "url": "https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/nn227.pdf",
      "locators": [
        "pp. 6–9; token frequency mismatch and multiple antecedent practices"
      ],
      "status": "reviewed",
      "limitations": [
        "Short comparative synthesis, not a primary excavation report."
      ],
      "notes": [
        "Used for the non-linear formation model and token-continuity limit."
      ],
      "provenance": [
        {
          "workstream": "WS02",
          "local_id": "WS02-SRC-006"
        }
      ]
    }
  ],
  "rule": "These claims define the section truth territory. Writer may use any subset and any narrative route. Source-level resolution may increase through bounded retrieval; new interpretation/generalization requires evidence authority.",
  "cycle_id": "C003",
  "outline_sha256": "22ba42e198615bb75bcb6db0aac25bc468a0c06a7c0858f114ce5c5b564f2d25",
  "claim_ids": [
    "CLM-0011",
    "CLM-0012",
    "CLM-0013",
    "CLM-0014",
    "CLM-0015",
    "CLM-0016",
    "CLM-0017",
    "CLM-0018"
  ],
  "source_ids": [
    "SRC-0001",
    "SRC-0003",
    "SRC-0005",
    "SRC-0009",
    "SRC-0010",
    "SRC-0011"
  ]
}
# END INPUT: 03_sections/P01/evidence-pack.json

# BEGIN INPUT: 03_sections/P01/materials.json
{
  "schema_version": 2,
  "section": "P01",
  "materials": [
    {
      "id": "P01-MAT-0001",
      "kind": "object",
      "label": "Geometric clay tokens in Late Uruk administrative levels",
      "claim_ids": [
        "CLM-0011",
        "CLM-0012",
        "CLM-0015"
      ],
      "source_refs": [
        {
          "source_id": "SRC-0005",
          "locators": [
            "pp. 33–38"
          ]
        },
        {
          "source_id": "SRC-0009",
          "locators": [
            "pp. 12–16"
          ]
        }
      ],
      "source_relation": "contemporary_material",
      "object_or_trace": "Small unbaked or lightly fired clay geometric shapes (spheres, cones, disks, cylinders), some plain and some incised with geometric marks",
      "actor": "Unknown; an administrative user role is inferred from context",
      "time": "Late Uruk period (ca. 3400–3200 BCE)",
      "place": "Eanna precinct, Uruk / Warka",
      "physical_description": "Hand-modeled clay objects generally between 1 and 3 cm in dimension, with matte earthen surface and fingernail or stylus incisions",
      "measurement": "1 to 3 cm in diameter / height",
      "limitations": [
        "Contexts in early excavations often disturbed; Neolithic antecedents vary in function and do not represent a single unified code across 5000 years"
      ],
      "representativeness": "Attested in Late Uruk administrative levels; broader function and continuity remain contested",
      "epistemic_layers": {
        "observed": [{"statement": "Small geometric clay objects survive in several forms; some bear incisions."}],
        "functional_inference": [{"statement": "Some Late Uruk examples participated in numerical or administrative practices.", "qualification": "Supported for bounded late administrative contexts, not a universal code across millennia."}],
        "representative_reconstruction": [],
        "qualified_live_hypothesis": [],
        "prohibited_or_rejected_inference": [{"statement": "Tokens formed a direct linear precursor to writing.", "qualification": "Contested; approved evidence supports a parallel ecology of practices."}]
      }
    },
    {
      "id": "P01-MAT-0002",
      "kind": "object",
      "label": "Hollow clay bulla (envelope) with enclosed tokens and exterior impressions",
      "claim_ids": [
        "CLM-0011",
        "CLM-0013",
        "CLM-0016"
      ],
      "source_refs": [
        {
          "source_id": "SRC-0005",
          "locators": [
            "pp. 41–46"
          ]
        },
        {
          "source_id": "SRC-0001",
          "locators": [
            "pp. 20–25"
          ]
        }
      ],
      "source_relation": "contemporary_material",
      "object_or_trace": "Globular hollow clay sphere sealed shut while moist, containing tokens inside and displaying surface impressions of those tokens and cylinder seals on the outside",
      "actor": "Unknown; possible institutional operators are inferred",
      "time": "Late Uruk period (ca. 3350–3200 BCE)",
      "place": "Uruk and Susa administrative precincts",
      "physical_description": "Spherical to ovoid clay ball 5 to 7 cm across, with thick walls, hollow core, and overlapping impressed marks and rolled figurative seal impressions",
      "measurement": "5 to 7 cm diameter, wall thickness 1 to 1.5 cm",
      "limitations": [
        "Breakable verification device; once opened to inspect contents, the sealed envelope is permanently destroyed"
      ],
      "representativeness": "Attested at Uruk and Susa; prevalence and exact function vary by context",
      "epistemic_layers": {
        "observed": [{"statement": "Hollow clay envelopes contain tokens and bear exterior impressions and seal rollings."}],
        "functional_inference": [{"statement": "Exterior marks made enclosed quantities inspectable without immediately opening the envelope.", "qualification": "Functional inference from the relation between contents and surface marks."}],
        "representative_reconstruction": [{"statement": "An operator deposits counters, closes the envelope, marks and seals it, then lets it dry.", "qualification": "Manufacture workflow reconstructed from artifact features, not a witnessed event."}],
        "qualified_live_hypothesis": [],
        "prohibited_or_rejected_inference": [{"statement": "Bullae emerged specifically to prevent fraud or solve verification at distance.", "qualification": "Causal hypothesis; the artifacts alone do not establish a single motive."}]
      }
    },
    {
      "id": "P01-MAT-0003",
      "kind": "object",
      "label": "Cylinder seal and impressed clay rollings",
      "claim_ids": [
        "CLM-0013",
        "CLM-0018"
      ],
      "source_refs": [
        {
          "source_id": "SRC-0005",
          "locators": [
            "pp. 47–52"
          ]
        },
        {
          "source_id": "SRC-0010",
          "locators": [
            "pp. 70–75"
          ]
        }
      ],
      "source_relation": "contemporary_material",
      "object_or_trace": "Carved hard stone cylinder (limestone, lapis, calcite) engraved with negative relief of captive processions, animal herds, or administrative activities",
      "actor": "Unknown; an authorized agent or witness role is inferred",
      "time": "Middle to Late Uruk period (ca. 3500–3100 BCE)",
      "place": "Uruk, Susa, Habuba Kabira",
      "physical_description": "Perforated stone cylinder 2 to 5 cm in length, diameter 1 to 2.5 cm, engraved with micro-relief scenes",
      "measurement": "length 2–5 cm, diameter 1–2.5 cm",
      "limitations": [
        "Identifies institutional authority or witness presence, not spoken syntax or linguistic phonology"
      ],
      "representativeness": "Widely attested in the cited contexts; not established here as universal",
      "epistemic_layers": {
        "observed": [{"statement": "Engraved cylinders and continuous rolled impressions survive on several clay media."}],
        "functional_inference": [{"statement": "Seal impressions marked an association with authority, custody or witnessing.", "qualification": "Inferred from context; no unique event or speaker is identified."}],
        "representative_reconstruction": [],
        "qualified_live_hypothesis": [],
        "prohibited_or_rejected_inference": []
      }
    },
    {
      "id": "P01-MAT-0004",
      "kind": "record",
      "label": "Solid numerical tablet with stylus impressions",
      "claim_ids": [
        "CLM-0011",
        "CLM-0013",
        "CLM-0017"
      ],
      "source_refs": [
        {
          "source_id": "SRC-0001",
          "locators": [
            "pp. 22–27"
          ]
        },
        {
          "source_id": "SRC-0005",
          "locators": [
            "pp. 45–50"
          ]
        }
      ],
      "source_relation": "contemporary_material",
      "object_or_trace": "Cushion-shaped clay tablet bearing impressed circular, semi-circular, and stroke-shaped numerical signs without pictographic script signs",
      "actor": "Unknown; an administrative record-maker role is inferred",
      "time": "Late Uruk period, Uruk V to early IV (ca. 3300–3200 BCE)",
      "place": "Eanna district, Uruk; Susa",
      "physical_description": "Thick rounded rectangular clay tablet, roughly palm-sized, with distinct deep round depressions and oblique circular cups",
      "measurement": "4 to 6 cm length, 3 to 5 cm width, 1.5 to 2.5 cm thickness",
      "limitations": [
        "Records quantities and transaction categories without specifying full grammatical sentences or spoken words"
      ],
      "representativeness": "Attested before and alongside pictographic tablets; a single direct genealogy is not established",
      "epistemic_layers": {
        "observed": [{"statement": "Clay tablets bear round and oblique numerical impressions and sometimes seal rollings."}],
        "functional_inference": [{"statement": "The impressed marks record numerical information.", "qualification": "Supported by specialist comparison and administrative context."}],
        "representative_reconstruction": [{"statement": "A record-maker shapes damp clay and applies differently angled impressions before drying it.", "qualification": "Reconstructed manufacture sequence, not a documented individual act."}],
        "qualified_live_hypothesis": [],
        "prohibited_or_rejected_inference": [{"statement": "Numerical tablets were a necessary direct step toward proto-cuneiform.", "qualification": "Genealogical interpretation remains non-linear and contested."}]
      }
    },
    {
      "id": "P01-MAT-0005",
      "kind": "record",
      "label": "Archaic proto-cuneiform administrative account (Uruk IV)",
      "claim_ids": [
        "CLM-0011",
        "CLM-0014",
        "CLM-0017"
      ],
      "source_refs": [
        {
          "source_id": "SRC-0001",
          "locators": [
            "pp. 28–35"
          ]
        },
        {
          "source_id": "SRC-0005",
          "locators": [
            "pp. 52–60"
          ]
        }
      ],
      "source_relation": "contemporary_material",
      "object_or_trace": "Clay tablet ruled into compartments (cases), combining impressed numerical notations with incised pictographic signs representing commodities, persons, and institutions",
      "actor": "Unknown; a trained administrative record-maker is inferred",
      "time": "Uruk IV period (ca. 3300–3100 BCE)",
      "place": "Eanna Temple Complex, Uruk",
      "physical_description": "Convex clay tablet 5 to 8 cm square, light buff or greyish clay, clearly divided by incision lines with deeply impressed numerals and thin drawn pictographs",
      "measurement": "5 to 8 cm length, 4 to 7 cm width, 1.5 to 2 cm thickness",
      "limitations": [
        "Texts are ledger-style administrative allocations; do not record running continuous spoken discourse, poetry, or historical narrative"
      ],
      "representativeness": "Representative of the cited Uruk IV administrative corpus, not a universal canonical form",
      "epistemic_layers": {
        "observed": [{"statement": "Ruled tablets combine impressed numerals with incised pictographic signs in compartments."}],
        "functional_inference": [{"statement": "The layout organizes quantities and categories for accounting.", "qualification": "Inferred from corpus, sign distribution and document structure."}],
        "representative_reconstruction": [{"statement": "A record-maker rules compartments, enters marks, and may total entries on the reverse.", "qualification": "Representative recording workflow; no named writer or event survives."}],
        "qualified_live_hypothesis": [],
        "prohibited_or_rejected_inference": []
      }
    },
    {
      "id": "P01-MAT-0006",
      "kind": "object",
      "label": "Pointed and round-ended reed styluses",
      "claim_ids": [
        "CLM-0011",
        "CLM-0017"
      ],
      "source_refs": [
        {
          "source_id": "SRC-0001",
          "locators": [
            "pp. 36–39"
          ]
        },
        {
          "source_id": "SRC-0005",
          "locators": [
            "pp. 55–58"
          ]
        }
      ],
      "source_relation": "contemporary_material",
      "object_or_trace": "Cut marsh reed (Phragmites australis) stalks with carved pointed end for incising curved lines and blunt rounded/semi-circular ends for numerical punches",
      "actor": "Unknown record-maker",
      "time": "Late Uruk period (ca. 3300–3000 BCE)",
      "place": "Southern Mesopotamian riverine and marsh landscape",
      "physical_description": "Short slender reed stalk 10 to 15 cm long, smooth exterior siliceous rind, cut diagonally and rounded on opposite ends",
      "measurement": "10–15 cm length, 0.5–0.8 cm diameter",
      "limitations": [
        "Organic material rarely preserved directly in archaeological record; tool morphology reconstructed from impressions and incisions in clay"
      ],
      "representativeness": "Tool form inferred from marks; organic implements rarely survive directly",
      "epistemic_layers": {
        "observed": [{"statement": "Clay surfaces preserve rounded impressions and incised lines made by differently shaped tips."}],
        "functional_inference": [{"statement": "Reed tools likely produced these marks.", "qualification": "Tool morphology is reconstructed from impressions because the tools rarely survive."}],
        "representative_reconstruction": [{"statement": "A record-maker shapes a reed, then presses or draws it at different angles in wet clay.", "qualification": "Plausible reconstruction, not a directly observed workflow."}],
        "qualified_live_hypothesis": [],
        "prohibited_or_rejected_inference": []
      }
    },
    {
      "id": "P01-MAT-0007",
      "kind": "trace",
      "label": "Administrative sealing assemblage on clay jar stoppers and door pegs",
      "claim_ids": [
        "CLM-0013",
        "CLM-0014",
        "CLM-0018"
      ],
      "source_refs": [
        {
          "source_id": "SRC-0010",
          "locators": [
            "pp. 82–88"
          ]
        },
        {
          "source_id": "SRC-0005",
          "locators": [
            "pp. 60–64"
          ]
        }
      ],
      "source_relation": "contemporary_material",
      "object_or_trace": "Clay sealings (cretulae) pressed over woven reed mats, jar cloth covers, wooden pegs inserted into storeroom walls, with cord impressions on underside and seal rollings on top",
      "actor": "Unknown; custody and inspection roles are inferred",
      "time": "Late Uruk period (ca. 3400–3100 BCE)",
      "place": "Institutional storehouses in Eanna, Uruk",
      "physical_description": "Irregular lumps of clay bearing negative impressions of rope, wood pegs, or coarse cloth on interior face and multiple seal rollings on exterior",
      "measurement": "3 to 8 cm width",
      "limitations": [
        "Documents physical custody and unauthorized entry prevention, not textual content"
      ],
      "representativeness": "Attested sealing practice in the cited institutional contexts",
      "epistemic_layers": {
        "observed": [{"statement": "Clay sealings preserve impressions of cord, cloth or wood and exterior seal rollings."}],
        "functional_inference": [{"statement": "Sealings participated in controlling or evidencing access.", "qualification": "Inferred from attachment traces and find contexts."}],
        "representative_reconstruction": [{"statement": "An operator binds a closure, presses clay over it and rolls a seal; later access breaks it.", "qualification": "Representative custody workflow, not a documented incident."}],
        "qualified_live_hypothesis": [],
        "prohibited_or_rejected_inference": []
      }
    },
    {
      "id": "P01-MAT-0008",
      "kind": "process",
      "label": "Institutional ration accounting and disbursement procedure",
      "claim_ids": [
        "CLM-0014",
        "CLM-0017"
      ],
      "source_refs": [
        {
          "source_id": "SRC-0001",
          "locators": [
            "pp. 40–48"
          ]
        },
        {
          "source_id": "SRC-0010",
          "locators": [
            "pp. 95–102"
          ]
        }
      ],
      "source_relation": "contemporary_material",
      "object_or_trace": "Standard bevel-rimmed clay bowls (mass-produced mold-made coarse pottery) used in conjunction with tabular lists of barley portions",
      "actor": "Unknown; proposed distributors, recipients and record-keepers are reconstructed roles",
      "time": "Late Uruk period (ca. 3300–3100 BCE)",
      "place": "Central storehouses, Eanna district, Uruk",
      "physical_description": "Standardized conical coarse clay bowls, roughly 0.8 liter capacity, roughly made by pressing straw-tempered clay into earth mold, found discarded in thousands",
      "measurement": "rim diameter ca. 18 cm, capacity ca. 0.8 liter",
      "limitations": [
        "Connection between bowl volume and specific sign for ration (GAR / NINDA) is analytical; exact operational link varies by site"
      ],
      "representativeness": "Bowls are abundant in cited contexts; their link to particular ration signs varies by site",
      "epistemic_layers": {
        "observed": [{"statement": "Many similarly formed bevel-rimmed bowls occur in Uruk-period contexts alongside records."}],
        "functional_inference": [{"statement": "The bowls may have served standardized portions in provisioning.", "qualification": "The bowl-volume and ration-sign connection is analytical and varies by site."}],
        "representative_reconstruction": [{"statement": "Workers assemble, an official checks an allocation, grain is measured, and a record is updated.", "qualification": "Composite reconstruction; not a documented unique event."}],
        "qualified_live_hypothesis": [],
        "prohibited_or_rejected_inference": [{"statement": "This workflow proves a redistribution system caused writing to emerge.", "qualification": "Causal synthesis exceeds what the association alone proves."}]
      }
    }
  ]
}
# END INPUT: 03_sections/P01/materials.json

# BEGIN INPUT: 03_sections/P01/evidence-resolution-request.md
# Evidence Resolution Rework — P01

Requested by: user

Requested at: 2026-09-04T04:12:23.080138+00:00

## Request

Within the already approved P01 claim/source ceiling, recover genuinely instance-level artifact or document records with source-bound identity, context, locators, exact surviving features and epistemic classification. Preserve class-level records; do not invent instances or assign narrative roles.
# END INPUT: 03_sections/P01/evidence-resolution-request.md
