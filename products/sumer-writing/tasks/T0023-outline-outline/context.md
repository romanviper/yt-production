# Context Packet — T0023-outline-outline

- Product: `sumer-writing`
- Operation: `outline`
- Context profile: `architecture`
- Section: `-`
- Unit: `-`
- Allowed writes: `02_outline/outline.json`, `02_outline/story-bible.md`, `02_outline/voice-profile.md`, `tasks/T0023-outline-outline/report.md`, `tasks/T0023-outline-outline/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Only the material inside this packet is task context. Do not scan the repository.

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

A system, institution, technology or idea becomes the protagonist. The story follows how pressure forms it, how it expands what people can do, what conflicts and consequences it creates, and how it transforms, weakens or survives as a legacy.

## Whole-script architecture

Every script has three clear audience-facing acts, whether it lasts 30 minutes or three hours:

- **Opening:** begin with a concrete object, person, action or situation; establish the central tension and the promise of the journey without resolving it immediately.
- **Body:** follow causal change through formation, expansion, conflict, consequence and adaptation. Each movement changes the state of the story.
- **Ending:** answer the central question, trace the final consequence or legacy, and reconnect it to the opening tension.

These acts belong to the whole script. A production section is only a bounded work unit and must not repeat opening–body–ending as a miniature template.

## Voice

The narrator is calm, clear, weighty and investigative. Start concrete, widen only when a mechanism needs explanation, then return to what that mechanism allows or costs people. Prefer causality to chronology, consequence to trivia and ordinary Vietnamese to abstract terminology. Emotional weight comes from evidenced consequences, not rhetorical intensity.

The identity is stable; its expression remains adaptive. The Agent chooses local structure, pace and phrasing from the material instead of filling a house style formula.
# END INSTRUCTION: system/standards/channel-constitution.md

# BEGIN INSTRUCTION: system/operations/outline.md
# Operation — Outline

## Responsibility

Design the audience's complete three-act journey before cutting it into bounded production work units. Do not write narration.

## Design order

1. Define the central question, audience promise and final change in understanding.
2. Design exactly three audience-facing acts: opening, body and ending.
3. Within those acts, design as many narrative movements as the causal material requires.
4. Only then place `P##` work-unit boundaries at meaningful state changes or context/review limits.

The three acts are a channel invariant. Movement count, section count, relative length and local form are not. Never choose ten sections first or make every section repeat a hook–explanation–payoff template.

## Current outline contract

Schema v4 contains:

- a whole-script architecture with the central question, audience promise and duration-derived word envelope;
- exactly three ordered acts, each with its own job and entry/exit state;
- ordered narrative movements assigned once to those acts;
- contiguous movement/section mappings that may be many-to-many inside one act;
- for each section: one narrative job, entry/exit state, evidence allowance, dependencies and an estimated word range.

Section-level question, payoff, planned beats, structural-role labels and budget justifications are optional creative notes, not required fields.

`story-bible.md` keeps only global causal spine, chronology, terms, entities, setup/payoff continuity and exclusions. `voice-profile.md` captures product-specific variation inside the Channel Constitution in 150–450 words. It learns functions from benchmarks without imitating surface style.

All three artifacts remain `draft` until the user approves them.
# END INSTRUCTION: system/operations/outline.md

# BEGIN INPUT: product.json
{
  "schema_version": 1,
  "slug": "sumer-writing",
  "working_title": "Chữ viết đã tạo ra nền văn minh Sumer như thế nào?",
  "language": "vi",
  "format": "long_form_history_documentary",
  "status": "outline_redesign",
  "created_at": "2026-08-12",
  "target": {
    "duration_minutes": {
      "min": 60,
      "max": 120
    },
    "narration_wpm": 140
  },
  "locked_decisions": [
    {
      "id": "DEC-0001",
      "statement": "Sản phẩm đầu tiên kể câu chuyện về chữ viết của nền văn minh Sumer.",
      "locked": true,
      "by": "user",
      "date": "2026-08-12"
    },
    {
      "id": "DEC-0002",
      "statement": "Fall of Civilizations là benchmark và đối thủ tham chiếu, không phải khuôn để sao chép.",
      "locked": true,
      "by": "user",
      "date": "2026-08-12"
    },
    {
      "id": "DEC-0003",
      "statement": "Kịch bản dự kiến dài 1–2 giờ và phải được tạo, review, sửa theo module thay vì generate một lần toàn bộ.",
      "locked": true,
      "by": "user",
      "date": "2026-08-12"
    },
    {
      "id": "DEC-0004",
      "statement": "Global research synthesis và causal model được chấp nhận làm handoff cho outline.",
      "locked": true,
      "by": "user",
      "date": "2026-08-13"
    }
  ],
  "scope": {
    "in": [
      "Các áp lực và thực hành dẫn đến những hệ thống ghi dấu sớm ở miền nam Mesopotamia.",
      "Sự biến đổi của chữ viết về hình thức, công dụng, người sử dụng và thiết chế kiểm soát.",
      "Hệ quả đối với quản trị, trí nhớ, quyền lực, ngôn ngữ và truyền thống tri thức.",
      "Sự lan truyền, thích nghi, suy yếu và di sản của truyền thống chữ hình nêm liên quan."
    ],
    "out": [
      "Tổng sử chính trị đầy đủ của Sumer nếu không phục vụ causal chain.",
      "Danh mục toàn bộ vua, thành bang, thần thoại hoặc thành tựu.",
      "Sao chép structure, câu chữ, cadence hoặc persona của Fall of Civilizations."
    ]
  },
  "benchmarks": [
    {
      "name": "Fall of Civilizations — The Sumerians: Fall of the First Cities",
      "role": "direct_adjacent_competitor",
      "url": "https://www.youtube.com/watch?v=d2lJUOv0hLA",
      "differentiate_on": "Theo vòng đời chữ viết như công nghệ–thiết chế."
    }
  ],
  "stages": {
    "direction": "approved",
    "research_plan": "approved",
    "research": "approved",
    "outline": "changes_requested",
    "sections": "paused",
    "integration": "not_started",
    "delivery": "not_started"
  },
  "production_cycle": {
    "id": "C002",
    "status": "outline_design",
    "previous": "C001",
    "started_at": "2026-08-13T18:18:51.170286+00:00",
    "reason": "Bắt đầu production cycle C002 dưới harness Hard Boundaries, Soft Logic. Thiết kế lại toàn bộ kịch bản từ research đã duyệt: giữ ba act toàn phim opening–body–ending rõ ràng; thiết kế macro movements trước rồi mới cắt P## theo causal load và context/review boundaries; không dùng section count, beat sheet, payoff formula hay word quota làm khuôn mặc định. Giữ ổn định channel values, voice identity và causal system-as-protagonist; cho phép opening form, local route, movement count, section count và relative length thích ứng với vật liệu. Không dùng P01 hoặc story plan của cycle cũ làm template."
  }
}
# END INPUT: product.json

# BEGIN INPUT: 00_brief/product-brief.md
# Product Brief — Chữ viết Sumer

Status: direction approved by user on 2026-08-12.

## Locked direction

- Đây là sản phẩm đầu tiên theo North Star mới của kênh.
- Subject là câu chuyện về chữ viết trong nền văn minh Sumer.
- *Fall of Civilizations* là benchmark/đối thủ tham chiếu, không phải template để sao chép.
- Kịch bản dự kiến dài 1–2 giờ và được tạo, review, sửa theo module.
- Research xác định historical mechanism và boundary; không quyết định lại subject.

## Product question

> Một hệ thống ghi dấu xuất hiện trong những cộng đồng ngày càng phức tạp ở miền nam Mesopotamia đã hình thành, mở rộng chức năng, tái phân phối năng lực xã hội, biến đổi qua các ngôn ngữ và thiết chế, rồi để lại di sản lâu hơn thế giới tạo ra nó như thế nào?

Đây là research frame, không phải verdict. Mọi causal verb phải được evidence kiểm tra.

## In scope

- Điều kiện và information practices trước/sát thời điểm writing hình thành.
- Medium, sign system, language, function và community of practice.
- Hệ quả đối với quản trị, trao đổi, quyền lực, ký ức và tri thức khi có bằng chứng.
- Adaptation, persistence, decline và legacy của các truyền thống liên quan.

## Out of scope

- Tổng sử chính trị Sumer nếu không phục vụ causal chain của writing.
- Catalogue vua, thành bang, thần thoại hoặc thành tựu.
- Đường tiến bộ tất định từ pictograph tới alphabet hiện đại.
- “Sumer invented writing” hoặc “writing created civilization” như premise fact chưa kiểm chứng.

## Known risks

- Nhầm Sumerian language, population label, proto-cuneiform và cuneiform.
- Monocausal administration story.
- Token → tablet → phonetic writing như đường thẳng tất định.
- Survival bias của clay archives.
- Presentism về literacy, bureaucracy, author và ownership.
- Legacy bằng analogy thay vì transmission chain.

## Target

- Ngôn ngữ: tiếng Việt.
- Thời lượng: 60–120 phút.
- Section count dự kiến cho pilot: 10, được outline quyết định và người dùng duyệt.
# END INPUT: 00_brief/product-brief.md

# BEGIN INPUT: 00_brief/benchmark.md
# Benchmark — Sumer Writing

Status: orientation, audited 2026-08-12.

## Direct adjacent competitor

**Fall of Civilizations, Episode 8: “The Sumerians — Fall of the First Cities”**

- Duration được công bố: 2 giờ 29 phút.
- Promise: đi từ nguồn gốc bí ẩn và những thành phố đầu tiên tới sự sụp đổ của nền văn minh Sumer.
- Experience signals: ruins/rediscovery opening, myths, proverbs, voice actors và recreated music.
- Episode này đã bao phủ writing như một thành tựu nằm trong tổng sử Sumer.

Sources:

- [YouTube episode](https://www.youtube.com/watch?v=d2lJUOv0hLA)
- [Apple Podcasts listing and duration](https://podcasts.apple.com/ee/podcast/8-the-sumerians-fall-of-the-first-cities/id1449884495?i=1000454904678)
- [Official recommended reading page](https://fallofcivilizationspodcast.com/recommended-reading/)

## Không gian khác biệt cần bảo vệ

Sản phẩm này không cạnh tranh bằng việc kể lại nhiều thông tin hơn về Sumer. Nó đổi historical object:

| FoC episode | Pilot này |
|---|---|
| một civilization | một công nghệ–thiết chế |
| rise and fall của Sumer | formation → adoption → expansion → consequence/conflict → transformation → legacy của writing |
| writing là một thành tựu trong arc lớn | writing là causal object được điều tra |
| payoff là sự sụp đổ/impermanence | payoff dự kiến là thứ có thể sống lâu hơn xã hội tạo ra nó |

## Benchmark attributes được phép học

- Causal macro arc dễ hiểu trong thời lượng dài.
- Material/sensory anchor có provenance.
- Primary voices và văn bản cổ như evidence lẫn human presence.
- Chuyển nhịp giữa đời sống thường ngày, thiết chế và biến đổi hệ thống.
- Thừa nhận uncertainty và giới hạn source.
- Emotional weight đến từ evidence, không từ hyperbole.

## Những thứ không được sao chép

- Wording, cadence và motif “ruins in the present” như công thức bắt buộc.
- Chapter order hoặc sequence của episode Sumer.
- Giọng narrator, câu chuyển và cách dàn dựng đặc trưng.
- Claim “invented writing” chỉ vì benchmark đã dùng trong description năm 2019.
# END INPUT: 00_brief/benchmark.md

# BEGIN INPUT: 01_research/research-synthesis.md
# Global Research Synthesis — Sumer Writing

Status: ready_for_review

## Central answer

Writing did not create Sumerian civilization in a single causal act. A more defensible model is **co-development followed by feedback**: late-fourth-millennium institutions in southern Mesopotamia generated pressure to stabilize quantities, categories, persons and obligations; several clay, sealing, numerical and visual practices were combined into proto-cuneiform; once records became embedded in trained communities, authentication, retrieval and enforcement, they increased what institutions could coordinate across time, space and personnel. That increased capacity generated further demand for records.

The object that supplies continuity is therefore not one fixed script, language or tablet form. It is a **reproducible practice of turning selected relations into durable, standardized and retrievable marks**, maintained by communities that knew how to create, interpret, copy and act on them.

This model rejects three shortcuts: “ethnic Sumerians invented writing in 3200 BCE”; token → tablet → civilization as a linear ladder; and writing as an autonomous force that commanded labor or created the state.

## Proposed causal spine

### 1. A problem of scale selects for durable records

Before proto-cuneiform, numerical objects, bullae, seals, metrological conventions and images already handled parts of accounting and authentication. The strongest continuity is numerical, but the devices formed a parallel ecology rather than one universal token code.

As urban and institutional operations expanded, memory held in persons, gestures and local encounters became less sufficient for some tasks. The preserved Uruk IV–III corpus is overwhelmingly administrative, supporting administration as a major selection pressure. It does not by itself distinguish market exchange from redistribution, labor coordination, tax, tribute, obligation or ownership; each mechanism requires different evidence.

### 2. The first system is powerful precisely because it is incomplete

Uruk IV proto-cuneiform, approximately 3350/3300–3200 BCE, can stabilize quantities, commodities, offices and structured relations, often through tablet layout as much as language. Whether it already counts as “writing” depends on the declared threshold. Phonology is sparse, the underlying language is uncertain and the earliest marks are largely incised rather than mature wedges.

Uruk/southern Mesopotamian attribution is strong. Direct attribution to Sumerian language is low-to-medium and ethnic attribution is unsupported. Egypt overlaps chronologically, so “one of the earliest independently developed traditions” is safer than “the world’s first.”

### 3. Technical capacity and social use diverge

Across the third millennium, impressed wedge ductus, logo-syllabic values and more explicit language encoding expanded what cuneiform could express. This was not a march toward the alphabet. Nor did every technically possible use immediately become routine.

Functions accumulated and recombined: administration remained; lexical organization, letters, legal and normative documents, literature, cult and political memory expanded in different places and periods. Four bounded anchors can make this visible without becoming a genre catalogue: P005390 for early administrative classification; MMA 86.11.111 for a documentary report whose written order was not implemented; P228744 for lexical schooling; and ETCSL 3.1.19 for later copies transforming royal correspondence into political/literary memory.

### 4. Specialists turn marks into infrastructure

Earliest scribes are visible mainly through their products. Later contexts, especially Old Babylonian households and institutions, reveal training through copying, calculation, lexical lists and genre conventions. “Edubba” cannot be projected backward as a uniform temple-school, and modern mass-literacy categories do not fit.

The infrastructure is a chain: tablet affordance → trained writer/reader → seal, witness or convention → archive and retrieval → institution capable of acting. Break a link and a record may document a command without producing compliance.

### 5. Embedded records enlarge capacity and redistribute visibility

Ur III Umma and Puzriš-Dagan provide later, bounded evidence for the return arrow in the feedback loop. Classifications, equivalencies, responsible officials, seals and archives allowed institutions to aggregate labor, reconcile accounts and make obligations retrievable. Some later private actors also gained documentary leverage.

The distribution was asymmetric. Officials gained an aggregate view; workers and dependents became legible through imposed categories. Yet oral negotiation, household practice, embodied expertise and much exchange remained outside surviving archives. Archives are organizational residues shaped by clay durability, discard, excavation and the antiquities market—not neutral samples of society.

### 6. Survival comes from adaptation, not purity

Cuneiform spread through courts, specialists, diplomacy, apprenticeship, copying and lexical/bilingual curricula. It survived by changing sign values and orthographic conventions for Akkadian, Hittite and other languages. Script, language and institution followed different timelines: Sumerian could persist as learned content after probable vernacular decline while cuneiform encoded other languages.

The true unit of survival was the trained community capable of competent reuse. Old tablets alone do not constitute a living tradition.

### 7. The tradition contracts, breaks and is recovered

Cuneiform declined over centuries as language competition, political economy, temple contraction and the cost of specialist training narrowed its ecosystem. The tablet dated 75 CE is the latest currently known, not a proven final act. When institutional reproduction ceased, clay survived but competence did not.

Nineteenth-century recovery proceeded cumulatively through copied signs, Old Persian, Behistun, comparative testing of Akkadian and later reconstruction of Sumerian. This break defines the defensible legacy: modern access to ancient societies is recovery-mediated. Direct transmission must be proven case by case; parallels with databases are analogy, not lineage.

## Claim decisions for outline use

- **Supported spine:** administrative/institutional pressure was central; writing and institutions co-developed; procedural records later enlarged bounded capacities; trained communities enabled expansion and transmission; decline was multicausal; modern recovery followed a competence break.
- **Must remain qualified:** the writing threshold; absolute dates; earliest underlying language; strength and direction of the early feedback loop; literacy/access scale; regional timing of spoken Sumerian decline; the final date of competence.
- **Reject as premise facts:** ethnic Sumerians invented writing in a single year; an uncontested Mesopotamian world-first; a universal token genealogy; writing alone created the state or enforced law; archives represent the whole population; direct Sumer-to-modern-writing lineage.

## Contradictions retained

1. **Definition:** strict language encoding versus broader conventional lexical recording.
2. **Formation:** strong numerical continuity versus rejection of a universal token ladder.
3. **Causation:** writing as record of complexity versus writing as capacity multiplier; evidence supports a phase-bound feedback loop, not one timeless answer.
4. **Access:** restricted specialist practice versus later non-professional/private appropriation; no population rate follows.
5. **Continuity:** script, language and institution survive differently.
6. **Legacy:** living transmission ends before modern decipherment; recovery is not direct lineage.

## Open decisions before outline

1. **Framing of the title question.** Recommended: treat “created civilization” as the proposition to test and replace it with co-development/feedback in the payoff, not as a fact announced at the start.
2. **Chronological architecture.** Recommended: use a lifecycle with recurring causal returns—pressure → encoding → institutional embedding → expansion → adaptation → contraction/recovery—rather than eight workstream chapters.
3. **Human anchors.** The four WS05 cases are evidence-ready, but the outline must decide which two or three carry narrative weight. Rights currently favor the two Met objects; Penn imagery and direct ETCSL/CTMMA quotation remain uncleared.
4. **Opening/ending pair.** Strong candidate: open on an early tablet whose meaning is constrained and end with a once-readable tradition becoming mute, then recovered. The 75 CE tablet is a compelling late anchor but its latest-known status must stay explicit.

## Gaps that may block or constrain outline

- **No blocker to constructing a causal outline.**
- A precise claim about the proportion of administrative versus other early tablets would require a current corpus-count audit; use qualitative “overwhelmingly administrative” meanwhile.
- Claims about everyday experience, literacy rates, gender distribution or population-wide compliance remain unavailable and must not become section premises.
- Direct quotation and visual use for Penn/CDLI/ETCSL/CTMMA materials require production-stage rights checks; attributed paraphrase and cleared Met images are currently safer.
- If the outline wants a direct bridge from the Uruk origin horizon to Ur III capacity effects, it must mark the chronological gap and present later archives as tests of a possible return mechanism, not proof of what happened at Uruk.
# END INPUT: 01_research/research-synthesis.md

# BEGIN INPUT: 01_research/outline-evidence-pack.json
{
  "schema_version": 1,
  "product": "sumer-writing",
  "status": "complete",
  "claim_ledger_sha256": "5b316543e9d25b449066ba6986edea2f88631dfcf440cfcb26b1062fed8e088a",
  "claims": [
    {
      "id": "CLM-0001",
      "statement": "For this project, 'writing' should be treated as a graded analytical threshold: durable conventional marks that encode repeatable linguistic or lexical values count as writing, while devices that communicate quantities or meanings without demonstrable language encoding remain accounting/proto-writing; proto-cuneiform lies across this disputed boundary.",
      "type": "contested",
      "confidence": "medium",
      "status": "qualified",
      "sources": [
        "SRC-0003",
        "SRC-0004",
        "SRC-0005"
      ]
    },
    {
      "id": "CLM-0002",
      "statement": "The earliest substantial proto-cuneiform horizon is conventionally placed near the end of the Late Uruk period, approximately 3350/3300–3200 BCE (Uruk IV), followed by Uruk III/Jemdet Nasr approximately 3200–3000 BCE.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0001",
        "SRC-0002",
        "SRC-0008"
      ]
    },
    {
      "id": "CLM-0003",
      "statement": "Uruk IVa is the most probable context for the oldest script at Uruk, but the original find documentation is too weak to make the stratigraphic placement definitive.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0002"
      ]
    },
    {
      "id": "CLM-0004",
      "statement": "The earliest Uruk IV corpus known to scholarship is overwhelmingly administrative; lexical texts become materially more visible in Uruk III.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0001"
      ]
    },
    {
      "id": "CLM-0005",
      "statement": "Calling the earliest system 'cuneiform' is potentially anachronistic: proto-cuneiform signs were initially drawn/incised and only later acquired the systematic wedge-impressed form associated with mature cuneiform.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0003",
        "SRC-0004"
      ]
    },
    {
      "id": "CLM-0006",
      "statement": "The language underlying Uruk IV–III proto-cuneiform cannot be securely identified as Sumerian because the texts encode little phonology and can often be interpreted without recovering continuous speech.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0003",
        "SRC-0004"
      ]
    },
    {
      "id": "CLM-0007",
      "statement": "The safest attribution is regional and institutional: proto-cuneiform is first securely attested as a large corpus in the Uruk cultural sphere of southern Mesopotamia, especially Uruk, rather than securely attributable to a named ethnic population.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0001",
        "SRC-0002",
        "SRC-0004",
        "SRC-0007"
      ]
    },
    {
      "id": "CLM-0008",
      "statement": "An unqualified claim that Sumer or Uruk produced the world's first writing is not defensible, because early Egyptian writing at Abydos overlaps the late-fourth-millennium date range and priority depends on calibration and definition.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0006"
      ]
    },
    {
      "id": "CLM-0009",
      "statement": "The relative sequence Uruk IV proto-cuneiform → Uruk III proto-cuneiform → later language-explicit cuneiform is much more secure than the absolute dates or a sharp boundary between proto-writing and writing.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0001",
        "SRC-0002",
        "SRC-0003",
        "SRC-0007"
      ]
    },
    {
      "id": "CLM-0010",
      "statement": "The claim 'Sumer invented writing' should remain rejected as a premise fact but retained as a researchable shorthand whose components—place, system, language, population and priority—must be tested separately.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0002",
        "SRC-0004",
        "SRC-0005",
        "SRC-0006"
      ]
    },
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
      ]
    },
    {
      "id": "CLM-0019",
      "statement": "Proto-cuneiform and mature cuneiform differ in ductus: early signs were largely drawn, while wedge impressions became systematic later.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0004",
        "SRC-0005"
      ]
    },
    {
      "id": "CLM-0020",
      "statement": "Tablet cases, subcases and spatial organization carried relations that later writing could encode more linguistically.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005"
      ]
    },
    {
      "id": "CLM-0021",
      "statement": "Rare rebus/phonetic uses appear early, but consistent phonetic writing becomes evident mainly in the third millennium BCE.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0004",
        "SRC-0005"
      ]
    },
    {
      "id": "CLM-0022",
      "statement": "Cuneiform developed as a logo-syllabic system with semantic and phonological values, not as a stage naturally progressing toward alphabetic writing.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0004",
        "SRC-0013"
      ]
    },
    {
      "id": "CLM-0023",
      "statement": "Changes in metrology and sign standardization were pragmatic adaptations, not uniform replacement of old systems.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0012"
      ]
    },
    {
      "id": "CLM-0024",
      "statement": "Proto-cuneiform sign distribution and tablet position can reveal structural regularities even when a sign's spoken value or underlying language remains uncertain.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0005",
        "SRC-0010"
      ]
    },
    {
      "id": "CLM-0025",
      "statement": "A system's technical capacity to encode a relation is not evidence that communities used it consistently for that purpose.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0004",
        "SRC-0005",
        "SRC-0012",
        "SRC-0010"
      ]
    },
    {
      "id": "CLM-0026",
      "statement": "The earliest writing implies trained specialists, but their identities, recruitment and institutional status are poorly recoverable.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0016"
      ]
    },
    {
      "id": "CLM-0027",
      "statement": "The best archaeological evidence for formal curricula comes from later household and institutional contexts, especially the Old Babylonian period.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0014",
        "SRC-0015",
        "SRC-0016"
      ]
    },
    {
      "id": "CLM-0028",
      "statement": "Edubba was not necessarily a single standardized temple-run school system across Mesopotamian history.",
      "type": "contested",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0014",
        "SRC-0015"
      ]
    },
    {
      "id": "CLM-0029",
      "statement": "Scribal competence included copying, calculation, lexical knowledge and genre conventions, not merely decoding signs.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0014",
        "SRC-0016",
        "SRC-0017"
      ]
    },
    {
      "id": "CLM-0030",
      "statement": "Access was restricted and socially consequential, but no reliable percentage for literacy or a universal male-only rule can be derived.",
      "type": "unknown",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0014",
        "SRC-0015"
      ]
    },
    {
      "id": "CLM-0031",
      "statement": "House F at Old Babylonian Nippur provides an unusually contextualized household training sequence, not proof of a universal Mesopotamian school system.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0018"
      ]
    },
    {
      "id": "CLM-0032",
      "statement": "Professional title, functional competence and broad literacy must be mapped separately; some later archives show on-the-job or non-professional use outside a single formal school track.",
      "type": "inference",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0017",
        "SRC-0019"
      ]
    },
    {
      "id": "CLM-0033",
      "statement": "Named women and female-authored or female-voiced texts demonstrate access in some settings but cannot establish population rates or unmediated authorship.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0020"
      ]
    },
    {
      "id": "CLM-0034",
      "statement": "Uruk IV evidence is overwhelmingly administrative, while lexical texts become substantially more visible in Uruk III.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0001"
      ]
    },
    {
      "id": "CLM-0035",
      "statement": "By the middle third millennium BCE cuneiform served economic, religious, political, literary and scholarly domains.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0004"
      ]
    },
    {
      "id": "CLM-0036",
      "statement": "Lexical lists form a continuous knowledge-organizing tradition from the earliest writing through later cuneiform cultures.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0001",
        "SRC-0016"
      ]
    },
    {
      "id": "CLM-0037",
      "statement": "Legal documents, letters and contracts provide human-scale cases but are mediated by scribal formula and institutional context.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0021"
      ]
    },
    {
      "id": "CLM-0038",
      "statement": "Functional expansion should be narrated as successive additions and recombinations, not a ladder from accounting to literature.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0001",
        "SRC-0004",
        "SRC-0016",
        "SRC-0021"
      ]
    },
    {
      "id": "CLM-0039",
      "statement": "ETCSL's 394 literary compositions are modern composites based on late-third- and early-second-millennium manuscripts, so they are evidence for textual tradition rather than transparent transcripts of an original speaker.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0022"
      ]
    },
    {
      "id": "CLM-0040",
      "statement": "The bounded primary-text shortlist is fixed to four cases: administrative tablet P005390/MMA 1988.433.2, private letter MMA 86.11.111, lexical school tablet P228744, and literary composition ETCSL 3.1.19.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0023",
        "SRC-0024",
        "SRC-0025",
        "SRC-0026",
        "SRC-0027"
      ]
    },
    {
      "id": "CLM-0041",
      "statement": "Published English translations are editorial products and require attribution and rights review before direct quotation.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0021",
        "SRC-0022",
        "SRC-0024",
        "SRC-0025",
        "SRC-0026",
        "SRC-0027",
        "SRC-0028"
      ]
    },
    {
      "id": "CLM-0042",
      "statement": "P005390/MMA 1988.433.2 is a physical Uruk III administrative tablet recording grain-related quantities; its language and exact transaction remain uncertain.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0023",
        "SRC-0024"
      ]
    },
    {
      "id": "CLM-0043",
      "statement": "MMA 86.11.111 is a ca. 1632 BCE Old Babylonian letter in which Marduk-mushallim reports failure to implement a royal security order.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0021",
        "SRC-0025"
      ]
    },
    {
      "id": "CLM-0044",
      "statement": "P228744 is a fragmented Old Babylonian lexical school tablet excavated at Nippur and a witness to the OB Nippur Ura 03 composite Q000001.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0016",
        "SRC-0026"
      ]
    },
    {
      "id": "CLM-0045",
      "statement": "ETCSL 3.1.19 is a modern composite of the Puzur-Shulgi royal letter tradition assembled from multiple Old Babylonian manuscripts, not a contemporary Ur III dispatch.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0022",
        "SRC-0027",
        "SRC-0028"
      ]
    },
    {
      "id": "CLM-0046",
      "statement": "Administrative writing increased capacity to classify, aggregate and audit labor, goods and obligations when tied to institutional procedure.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0029",
        "SRC-0030"
      ]
    },
    {
      "id": "CLM-0047",
      "statement": "Ur III labor records reveal ordinary people mainly through top-down categories and required work.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0029",
        "SRC-0030"
      ]
    },
    {
      "id": "CLM-0048",
      "statement": "Writing’s power distribution changed over time: uses once concentrated in royal/institutional systems were later appropriated by urban private actors.",
      "type": "inference",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0031"
      ]
    },
    {
      "id": "CLM-0049",
      "statement": "A written law, norm or transaction is evidence of recording and claim-making, not automatic evidence of enforcement.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0031"
      ]
    },
    {
      "id": "CLM-0050",
      "statement": "Archive survival is structurally biased by clay durability, institutional discard, excavation history and antiquities-market provenance.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0029",
        "SRC-0032"
      ]
    },
    {
      "id": "CLM-0051",
      "statement": "At Puzriš-Dagan, more than 13,500 tablets reconstruct an archival agency tied to livestock, taxation, royal gifts and diplomacy; the archive should not be read as a literal inventory of one stockyard.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0033"
      ]
    },
    {
      "id": "CLM-0052",
      "statement": "Agency belongs to people and institutions using records: tablets stabilize classifications, scribes and sealers authenticate them, archives make them retrievable, and authorities supply enforcement.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0029",
        "SRC-0030",
        "SRC-0033"
      ]
    },
    {
      "id": "CLM-0053",
      "statement": "Distributional effects were asymmetric: record systems improved institutional visibility and elite/private claims while exposing workers and dependents through imposed categories.",
      "type": "inference",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0029",
        "SRC-0030",
        "SRC-0031",
        "SRC-0033"
      ]
    },
    {
      "id": "CLM-0054",
      "statement": "Oral negotiation, embodied skill, household practice and much routine exchange remained partly or wholly outside surviving writing.",
      "type": "unknown",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0029",
        "SRC-0032"
      ]
    },
    {
      "id": "CLM-0055",
      "statement": "Cuneiform was adapted from Sumerian-associated use to Akkadian and then to multiple unrelated languages.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0034",
        "SRC-0016",
        "SRC-0036"
      ]
    },
    {
      "id": "CLM-0056",
      "statement": "Adaptation required modification of sign values and orthographic conventions rather than simple substitution of words.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0034",
        "SRC-0036"
      ]
    },
    {
      "id": "CLM-0057",
      "statement": "Lexical lists and bilingual curricula were key transmission infrastructure across regions and centuries.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0016",
        "SRC-0035",
        "SRC-0036"
      ]
    },
    {
      "id": "CLM-0058",
      "statement": "Sumerian outlived probable vernacular use as a learned literary, cultic and scholarly language.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0034",
        "SRC-0035"
      ]
    },
    {
      "id": "CLM-0059",
      "statement": "The living-tradition endpoint is institutional reproduction: active teaching, copying and competent reuse, not the survival of old tablets alone.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0016",
        "SRC-0035"
      ]
    },
    {
      "id": "CLM-0060",
      "statement": "Transmission moved through courts, traveling or imported specialists, diplomatic contact, copying and formal curricula rather than by script diffusion alone.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0036",
        "SRC-0037",
        "SRC-0038"
      ]
    },
    {
      "id": "CLM-0061",
      "statement": "The Hittite case shows selective transfer: scholarly and literary cuneiform practices traveled, while Mesopotamian bookkeeping and metrology did not necessarily travel with them.",
      "type": "fact",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0037"
      ]
    },
    {
      "id": "CLM-0062",
      "statement": "Script survival, language survival and institutional survival are separable: cuneiform could encode new languages, Sumerian could persist as learned content, and both depended on training communities.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0034",
        "SRC-0016",
        "SRC-0035",
        "SRC-0037"
      ]
    },
    {
      "id": "CLM-0063",
      "statement": "Cuneiform use contracted over centuries rather than ending through one event.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0035",
        "SRC-0034"
      ]
    },
    {
      "id": "CLM-0064",
      "statement": "Lexical and scholarly traditions persisted into the first centuries CE in narrowed institutional settings.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0035"
      ]
    },
    {
      "id": "CLM-0065",
      "statement": "Material tablets survived after living reading competence disappeared, creating a break between ancient transmission and modern knowledge.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0035",
        "SRC-0039",
        "SRC-0040"
      ]
    },
    {
      "id": "CLM-0066",
      "statement": "Nineteenth-century decipherment was cumulative and comparative, not a single eureka moment.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0039",
        "SRC-0040"
      ]
    },
    {
      "id": "CLM-0067",
      "statement": "Cuneiform’s defensible modern legacy is recovery-mediated knowledge of ancient societies and influence through ancient Near Eastern textual transmission; resemblance to digital record systems is analogy, not lineage.",
      "type": "inference",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0035",
        "SRC-0039",
        "SRC-0040"
      ]
    },
    {
      "id": "CLM-0068",
      "statement": "The latest currently known dated cuneiform tablet is an astronomical text from 75 CE, but this is a latest-discovered datum, not a proven final act of writing.",
      "type": "fact",
      "confidence": "high",
      "status": "qualified",
      "sources": [
        "SRC-0041"
      ]
    },
    {
      "id": "CLM-0069",
      "statement": "Cuneiform decline combined language competition, institutional contraction, changing political economies and the cost of specialist training; no surviving evidence isolates one sufficient cause.",
      "type": "inference",
      "confidence": "medium-high",
      "status": "qualified",
      "sources": [
        "SRC-0035",
        "SRC-0034",
        "SRC-0041"
      ]
    },
    {
      "id": "CLM-0070",
      "statement": "Modern recovery proceeded through copied inscriptions, the partial decipherment of Old Persian, multilingual comparison at Behistun, and subsequent testing of Akkadian and Sumerian readings.",
      "type": "fact",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0039",
        "SRC-0040",
        "SRC-0042"
      ]
    },
    {
      "id": "CLM-0071",
      "statement": "Legacy claims fall into three classes: direct ancient transmission, recovery-mediated modern knowledge, and analogy without lineage.",
      "type": "inference",
      "confidence": "high",
      "status": "supported",
      "sources": [
        "SRC-0035",
        "SRC-0039",
        "SRC-0040",
        "SRC-0042"
      ]
    }
  ],
  "contradiction_register": [
    {
      "id": "CTR-0001",
      "question": "Earliest proto-cuneiform đã là writing hay vẫn là proto-writing?",
      "positions": [
        "Strict glottography excludes much of Uruk IV material.",
        "Broader lexical/conventional definition includes it."
      ],
      "provenance": [
        "WS01-CLM-001"
      ],
      "outline_rule": "State the definition before making invention/first claims."
    },
    {
      "id": "CTR-0002",
      "question": "Token có phát triển tuyến tính thành tablet và writing không?",
      "positions": [
        "Numerical continuity is strong for selected late devices.",
        "A universal millennia-long token code and direct genealogy are unsupported."
      ],
      "provenance": [
        "WS02-CLM-001",
        "WS02-CLM-002",
        "WS02-CLM-003"
      ],
      "outline_rule": "Use an information ecology, not a single ancestor story."
    },
    {
      "id": "CTR-0003",
      "question": "Writing caused institutional power or merely recorded it?",
      "positions": [
        "Later procedural archives show capacity effects.",
        "Co-development and enforcement by people/institutions prevent technological determinism or back-projection to Uruk."
      ],
      "provenance": [
        "WS02-CLM-005",
        "WS06-CLM-001",
        "WS06-CLM-007"
      ],
      "outline_rule": "Present a phase-bound feedback loop."
    },
    {
      "id": "CTR-0004",
      "question": "Sumerian continuity is language, script or institution?",
      "positions": [
        "Sumerian persisted as learned content after probable vernacular decline.",
        "Cuneiform also survived by adapting to other languages; timelines are not identical."
      ],
      "provenance": [
        "WS07-CLM-004",
        "WS07-CLM-008"
      ],
      "outline_rule": "Track script, language and training community separately."
    },
    {
      "id": "CTR-0005",
      "question": "Modern legacy is direct transmission or rediscovery?",
      "positions": [
        "Recovery-mediated knowledge is strongly supported.",
        "Direct lineage to modern writing or databases is unproven; resemblance alone is analogy."
      ],
      "provenance": [
        "WS08-CLM-003",
        "WS08-CLM-005",
        "WS08-CLM-009"
      ],
      "outline_rule": "End at the break and recovery, not a smartphone lineage."
    }
  ],
  "scope_note": "This catalog is for architecture allocation. Claim provenance and research detail remain authoritative in claim-ledger.json and source-index.json outside the creative prompt."
}
# END INPUT: 01_research/outline-evidence-pack.json

# BEGIN INPUT: 02_outline/outline-change-request.md
# Outline Change Request — C002

Requested by: user

Requested at: 2026-08-13T18:18:51.170286+00:00

Previous cycle: C001

## Required architecture change

Bắt đầu production cycle C002 dưới harness Hard Boundaries, Soft Logic. Thiết kế lại toàn bộ kịch bản từ research đã duyệt: giữ ba act toàn phim opening–body–ending rõ ràng; thiết kế macro movements trước rồi mới cắt P## theo causal load và context/review boundaries; không dùng section count, beat sheet, payoff formula hay word quota làm khuôn mặc định. Giữ ổn định channel values, voice identity và causal system-as-protagonist; cho phép opening form, local route, movement count, section count và relative length thích ứng với vật liệu. Không dùng P01 hoặc story plan của cycle cũ làm template.
# END INPUT: 02_outline/outline-change-request.md
