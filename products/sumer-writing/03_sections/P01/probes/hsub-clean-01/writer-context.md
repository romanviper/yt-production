# TASK-LOCAL EXPERIMENT BOUND

{
  "schema_version": 1,
  "experiment": "P01-HSUB-CLEAN-PROBE-01",
  "canonical_output": false,
  "section": "P01",
  "output_language": "vi",
  "target_words": {
    "min": 450,
    "max": 650
  },
  "output_scope": "Write one contiguous passage from the larger unfinished P01. Do not compress, summarize, or complete the whole section.",
  "completion_rule": "P01 must remain unfinished after this passage.",
  "context_rule": "Use only this task-local bound plus the canonical Writer context below. Do not inspect the repository or previous probes, feedback, reviews, or competitor prose."
}

# CANONICAL P01 WRITER CONTEXT

# Context Packet — T9900-draft-section-P01

- Product: `sumer-writing`
- Operation: `draft_section`
- Context profile: `creative_draft`
- Section: `P01`
- Unit: `-`
- Allowed writes: `03_sections/P01/draft.md`, `03_sections/P01/handoff.md`, `tasks/T9900-draft-section-P01/report.md`, `tasks/T9900-draft-section-P01/operator-brief.json`

Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.
The final chat response must use the rendered operator brief, not the task report.

Only the material inside this packet is task context. Do not scan the repository.

# Canonical evidence routing
Evidence access is secondary verification only. Historical Substrate is the primary history model.
Use evidence only after choosing a telling from that model, to verify, sharpen, or qualify a specific detail.
Do not survey evidence to discover the story route or to decide what historical reality exists to tell.
Every capability call is audit-logged; new claims or causal generalizations remain evidence-authority work.
Evidence adapter: `python scripts/draft_evidence.py products/sumer-writing T9900-draft-section-P01 <capability>`.
Capabilities: `scope`, `attest_scope`, `source`, `search`, `record`.
Submission requirement: call `attest_scope` successfully before submitting this task.

# BEGIN INSTRUCTION: system/core/creative-boundaries.md
# Creative Boundaries

These are authorship limits, not story instructions.

1. Make no factual historical claim beyond approved evidence. Preserve qualifications, uncertainty, disagreement and counterevidence.
2. Distinguish documented fact, qualified inference and naturally signaled representative reconstruction. Reconstruction may add plausible ordinary action, perception or spatial detail around a composite person or local event embodying approved conditions. It is not evidence and cannot invent named actors, attributed quotes, chronology, measurements, institutions, motives, dialogue, private thoughts or causal conclusions.
3. Stay inside the section mission and established continuity unless explicitly authorized.
4. Keep evidence metadata out of narration.
5. Do not imitate another creator's wording, cadence, motifs, persona or signature structure.
6. Report a blocker when evidence or authority is insufficient.

Within these boundaries, every creative choice belongs to the writer. No creative method or sequence is compulsory unless the user locks it for this task.
# END INSTRUCTION: system/core/creative-boundaries.md

# BEGIN INSTRUCTION: system/operations/substrate/draft-section.md
# Operation — Draft Section

## Objective

Tell a compelling historical story within truth and continuity. Optimize for the listener wanting to keep following it. Let meaning emerge through what unfolds; do not announce and defend a thesis. Explanation serves the story. Hook and retention are outcomes, not required techniques.

## Primary historical input

Author from `historical-substrate.json`, the section's historical territory/change and continuity. Historical Substrate is the primary model of the bounded historical world. Its `boundaries` constrain what may be asserted; they are not lines that must appear in narration.

## Evidence access

The bounded evidence broker is secondary. Use it only to verify, sharpen or qualify details needed by a telling already chosen from Historical Substrate. Call `attest_scope` before submission. If the assigned historical change cannot be authored within the substrate and truth boundaries, report a Historical Substrate/evidence blocker.

## Assignment and authority

Write original long-form historical narration that is natural aloud. Choose telling, composition, exposition, reconstruction and language. Use this style compass: calm, clear, weighty, investigative, grounded, causally meaningful and trustworthy rather than spectacular.

Respect uncertainty without inventing beyond the boundaries. The word target is a forecast.

## Feedback boundary

In rework, the observed problem and desired audience outcome bind. Repair examples and method hypotheses are non-binding. Only `owner_locked_for_single_task` compels a method.

Keep metadata out of narration. Block when the assigned historical change exceeds substrate or continuity bounds.
# END INSTRUCTION: system/operations/substrate/draft-section.md

# BEGIN INPUT: 03_sections/P01/section.json
{
  "section": "P01",
  "title": "Trước chữ viết đã có một bài toán phải giải",
  "mission": "Các thực hành ghi nhận và xác thực bằng đất sét trong Late Uruk, đặc biệt sự dịch chuyển toward việc đặt thông tin số trực tiếp trên bề mặt bền trong khi nhiều phương tiện cũ vẫn cùng tồn tại.",
  "historical_change": {
    "from": "Số lượng và sự xác thực được xử lý qua nhiều thiết bị và thực hành đất sét cùng tồn tại, gồm counters, envelopes, sealings và các bề mặt ghi số.",
    "to": "Thực hành ghi nhận ngày càng đặt thông tin số trực tiếp trên bề mặt đất sét bền, đôi khi cùng dấu xác thực, trong khi các phương tiện cũ vẫn tiếp tục chồng lấn."
  },
  "length_forecast_words": {
    "min": 1050,
    "max": 1550
  }
}
# END INPUT: 03_sections/P01/section.json

# BEGIN INPUT: 03_sections/P01/historical-substrate.json
{
  "schema_version": 2,
  "contract_version": 1,
  "section": "P01",
  "historical_territory": "Các thực hành ghi nhận và xác thực bằng đất sét trong Late Uruk, đặc biệt sự dịch chuyển toward việc đặt thông tin số trực tiếp trên bề mặt bền trong khi nhiều phương tiện cũ vẫn cùng tồn tại.",
  "historical_change": {
    "from": "Số lượng và sự xác thực được xử lý qua nhiều thiết bị và thực hành đất sét cùng tồn tại, gồm counters, envelopes, sealings và các bề mặt ghi số.",
    "to": "Thực hành ghi nhận ngày càng đặt thông tin số trực tiếp trên bề mặt đất sét bền, đôi khi cùng dấu xác thực, trong khi các phương tiện cũ vẫn tiếp tục chồng lấn."
  },
  "primitives": [
    {
      "id": "HS-P01-0001",
      "kind": "practice",
      "world": {
        "participants": [],
        "operation": "record and authenticate administrative information through several coexisting clay-based practices",
        "object_or_medium": [
          "clay counters/tokens",
          "clay envelopes",
          "sealings",
          "numerical tablets",
          "early written clay surfaces"
        ],
        "information_or_relation_handled": [
          "quantities",
          "authentication"
        ],
        "context": "Late-Uruk administrative practice"
      },
      "epistemic_status": "documented",
      "time_scope": "Late Uruk, especially the late fourth millennium BCE",
      "place_scope": "Southern Mesopotamia and associated Late-Uruk administrative contexts"
    },
    {
      "id": "HS-P01-0003",
      "kind": "object_affordance",
      "world": {
        "object": "hollow clay envelope",
        "permits": [
          "enclose small clay counters"
        ],
        "carries": [
          "enclosed counters",
          "on some examples exterior impressions or sealings"
        ],
        "constrains": [
          "enclosed counters are not directly inspectable while the envelope remains closed"
        ]
      },
      "epistemic_status": "documented",
      "time_scope": "Late Uruk",
      "place_scope": "Late-Uruk administrative contexts represented in the approved source set"
    },
    {
      "id": "HS-P01-0004",
      "kind": "object_affordance",
      "world": {
        "object": "numerical clay tablet",
        "permits": [
          "place quantity information directly on a durable exterior surface"
        ],
        "carries": [
          "numerical impressions",
          "on some examples sealing or authentication marks"
        ],
        "constrains": []
      },
      "epistemic_status": "documented",
      "time_scope": "Late Uruk",
      "place_scope": "Southern Mesopotamia and related Late-Uruk administrative sites in the approved source set"
    },
    {
      "id": "HS-P01-0007",
      "kind": "change",
      "world": {
        "dimension": "physical placement and inspectability of numerical information",
        "earlier_state": "quantities and authentication were handled across several coexisting physical devices and clay practices",
        "later_state": "numerical information increasingly appeared directly on durable clay surfaces, sometimes alongside authentication marks",
        "coexistence": "older and parallel clay practices continued to overlap with direct surface recording",
        "qualification": "the shift does not identify one invention event or an immediate complete replacement"
      },
      "epistemic_status": "qualified_inference",
      "time_scope": "Late Uruk, late fourth millennium BCE",
      "place_scope": "Southern Mesopotamia and related Late-Uruk administrative contexts"
    }
  ],
  "boundaries": [
    {
      "source": "HS-P01-0001",
      "rule": "Parallel practices must not be converted into a single mandatory developmental sequence."
    },
    {
      "source": "HS-P01-0003",
      "rule": "Exterior impressions are not universal to every envelope."
    },
    {
      "source": "HS-P01-0003",
      "rule": "The affordance does not establish a single transitional step toward tablets."
    },
    {
      "source": "HS-P01-0004",
      "rule": "A numerical tablet alone does not identify a commodity, transaction mechanism or named actor."
    },
    {
      "source": "HS-P01-0004",
      "rule": "Direct surface recording must not be described as wholesale replacement of envelopes or tokens."
    },
    {
      "source": "HS-P01-0007",
      "rule": "Increasing direct surface recording does not imply immediate or complete replacement of other clay practices."
    },
    {
      "source": "HSC-P01-0001",
      "applies_to": [
        "HS-P01-0001",
        "HS-P01-0003",
        "HS-P01-0004",
        "HS-P01-0007"
      ],
      "rule": "Do not convert overlapping clay practices into a direct token-to-tablet replacement genealogy."
    },
    {
      "source": "HSC-P01-0003",
      "applies_to": [
        "HS-P01-0001",
        "HS-P01-0004",
        "HS-P01-0007"
      ],
      "rule": "Do not label a specific economic mechanism such as market exchange, tax, tribute, redistribution, labor obligation or ownership unless independent transaction evidence supports it."
    }
  ],
  "authority_binding": {
    "product_substrate_sha256": "eb7ada6dc9414e5cd629fdc262e09bcf6fdb3afa6327ba0d8dcb19adf93ef818",
    "outline_sha256": "22ba42e198615bb75bcb6db0aac25bc468a0c06a7c0858f114ce5c5b564f2d25",
    "section_overlay_sha256": "5db68ce464d768dfbe59854208f8ecd5c9317878ebce96b062e176b2365e3973",
    "section_binding_sha256": "a4fe962b6fe8a094085fbe8f152e5bb6033dd51ebf6d8c8fa6168150e0143332"
  },
  "writer_contract": "Historical Substrate is the primary model of historical reality. Evidence lookup is secondary and only verifies, sharpens or qualifies details needed by a telling already chosen from this model."
}
# END INPUT: 03_sections/P01/historical-substrate.json

# BEGIN INPUT: 03_sections/P01/narration-pack.json
{
  "section": "P01",
  "cycle_id": "C003",
  "evidence": {
    "mode": "writer_directed_on_demand_v1",
    "access": "search_or_open_only_when_chosen_telling_needs_it"
  }
}
# END INPUT: 03_sections/P01/narration-pack.json

# BEGIN INPUT: 03_sections/P01/continuity-in.md
# Continuity Input — P01

Cycle: `C003`

Dependencies: Không có.

## Prior handoff

Chưa có hoặc sẽ được task owner cập nhật trước drafting.

## Canonical terms required here

Tham chiếu story bible.
# END INPUT: 03_sections/P01/continuity-in.md
