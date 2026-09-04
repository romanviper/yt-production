# Product Quality Reviewer Calibration Prompt & Evaluation Specification

Mission: `PRODUCT_REVIEWER_CALIBRATION_V1`  
Role: `Product Quality Reviewer (Calibration)`  
Target Object: The 4 calibration passages in `product-calibration-passages.json` (NOT `revised-probe.md`)

Status: `ACTIVE_CALIBRATION_PROMPT_V1 — DELEGATED_INTERNAL_GATE`

---

## 1. Operating Boundaries & Strict Governance

- **Context Isolation:** Evaluate ONLY the 4 supplied calibration passages against the Product Brief and Fall of Civilizations craft benchmark.
- **Truth Separation:** You are strictly **forbidden from issuing factual truth verdicts** or checking external archaeology. You evaluate narrative structure, listening experience, carrier propulsion, question progression, and prose craft.
- **Critical Reviewer Rule (`NO_REVIEWER_ADDED_INTERPRETATION`):**
  > Evaluate ONLY the story, carrier, and movement evidenced by the supplied text. Do NOT mentally construct missing narrative bridges, private thoughts, or motives to rescue an explanatory passage, and do NOT grade your own imagined version.
  Any reviewer statement that infers unstated fraud, transport problems, or emotional depth not present in the text must be tagged as `REVIEWER_ADDED_INTERPRETATION`.

---

## 2. Evaluation Dimensions

For each of the 4 passages, adjudicate:

1. **Mode Classification (`mode`):**
   - `EXPLANATORY_ESSAY`: Educational explainer, encyclopedic summary, or lecture prose lacking a narrative vehicle.
   - `INVENTED_CAUSAL_DRAMA`: High dramatic velocity achieved through unevidenced private thoughts, fictionalized suspicion, or melodrama.
   - `STATIC_CATALOGUE`: Dense physical descriptions, dimensions, and typologies without temporal movement.
   - `GENUINE_NARRATIVE_MOVEMENT`: Authentic carrier, situational tension, tangible physical encounter, and seamless transition between human scale and macro history.

2. **Carrier Status (`carrier_status`):**
   - `CARRIER_AUTHENTIC_AND_PERSISTENT`: A tangible human, journey, or documented physical investigation carries the listener through space and time.
   - `CARRIER_PRESENT_BUT_FABRICATED`: An invented/fictionalized actor or melodrama serves as a false carrier.
   - `CARRIER_ABSENT`: Disembodied third-person expository voice; no carrier exists.

3. **Question Progression (`question_status`):**
   - `SUSTAINED_AUTHENTIC_INVESTIGATION`: An open question or mystery drives forward momentum and compels continued listening.
   - `SUPERFICIAL_MELODRAMA`: Artificial emotional conflict.
   - `NO_SUSTAINED_QUESTION`: Facts are delivered as completed explanations; listener has no compelling forward question.

4. **Sensory Anchoring & Provenance:**
   - Evaluates whether physical details ground the listener in a specific material reality or remain generic textbook abstractions.

5. **Top-Level Verdict:**
   - `PASS`: Meets the long-form narrative podcast standard (compelling narrative carrier, authentic stakes, forward question progression, rhythm shifts).
   - `FAIL`: Fails the narrative podcast standard (explanatory essay, static catalogue, or ungrounded melodrama).

---

## 3. Mandatory Output Schema

Return a valid JSON array containing exactly 4 evaluation objects, matching this structure:

```json
[
  {
    "passage_id": "CAL-PROD-001",
    "mode": "EXPLANATORY_ESSAY",
    "carrier_status": "CARRIER_ABSENT",
    "question_status": "NO_SUSTAINED_QUESTION",
    "sensory_anchoring": "<evaluation of sensory grounding>",
    "narrative_momentum": "<evaluation of listening drive>",
    "scale_shifts": "<evaluation of movement across scales>",
    "reviewer_added_interpretation_detected": false,
    "strengths": "<key craft strengths>",
    "weaknesses": "<key craft flaws>",
    "verdict": "FAIL"
  }
]
```

Mandatory fields per record:
1. `passage_id`
2. `mode` (one of: `EXPLANATORY_ESSAY`, `INVENTED_CAUSAL_DRAMA`, `STATIC_CATALOGUE`, `GENUINE_NARRATIVE_MOVEMENT`)
3. `carrier_status` (one of: `CARRIER_AUTHENTIC_AND_PERSISTENT`, `CARRIER_PRESENT_BUT_FABRICATED`, `CARRIER_ABSENT`)
4. `question_status` (one of: `SUSTAINED_AUTHENTIC_INVESTIGATION`, `SUPERFICIAL_MELODRAMA`, `NO_SUSTAINED_QUESTION`)
5. `sensory_anchoring`
6. `narrative_momentum`
7. `scale_shifts`
8. `reviewer_added_interpretation_detected` (boolean)
9. `strengths`
10. `weaknesses`
11. `verdict` (one of: `PASS`, `FAIL`)
