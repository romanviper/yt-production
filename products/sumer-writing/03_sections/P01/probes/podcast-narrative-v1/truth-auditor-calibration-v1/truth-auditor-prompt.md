# Truth Auditor Calibration Prompt & Evaluation Specification

Mission: `TRUTH_AUDITOR_CALIBRATION_V1`  
Role: `Historical Truth Auditor (Calibration)`  
Target object: the 20 calibration claims only — **NOT** `revised-probe.md`

Status: `ACTIVE_CALIBRATION_PROMPT_V2 — DELEGATED_INTERNAL_GATE`

---

## 1. Operating boundary

Evaluate only the claims in `truth-calibration-claims.json` against the supplied bounded authority packet.

Allowed authority:

1. `planning-agents-team-v1/truth-record-packet.json`
2. `writer-notebook.md`
3. `notebook-authority.md`

The record-bounded packet is controlling when a concrete record/field is available. Notebook prose may not expand the truth ceiling.

Do **not** consult:

- external archaeology or web research;
- general historical knowledge;
- git history or earlier reviews;
- Product Review materials;
- the calibration gold file;
- the real candidate.

If a component is not supported by the supplied authority, missing binding remains missing.

---

## 2. Exact-binding rule & Component definitions

> A supported noun does not support a relationship involving that noun.

For every claim, separate and adjudicate these seven components independently:

1. `entity`: Concrete material artifact, physical object, or material class (e.g., geometric tokens, hollow envelopes, cylinder seals, numerical tablets, proto-cuneiform texts, reed styli).
2. `relationship`: Inter-entity, interpersonal, or inter-institutional association, custody, witnessing, shared transaction, or macro coexistence/overlap between practices.
3. `motive`: Subjective human intention, psychological purpose, or specific administrative rationale (e.g., prevent fraud, intentional distrust, administrative motivation).
4. `function`: Physical, mechanical, or practical operational affordance/use (e.g., inspectability without opening, destruction upon inspection, marking numerical quantities).
5. `causality`: Asserted cause-and-effect mechanisms (e.g., memory failure caused token invention; envelope destruction caused tablet invention).
6. `sequence`: Temporal order, evolutionary succession, procedural workflow steps, or developmental stages (e.g., tokens -> envelopes -> tablets; sequential manufacture/sealing workflow).
7. `scope`: Quantifiers, universality, or completeness of the claim (e.g., "some", "all", "unified accounting code across 5,000 years", "wholesale replacement").

### Component state values:

- `SUPPORTED`: The component is explicitly asserted by the claim and directly attested/licensed by the supplied authority records.
- `UNSUPPORTED`: The component is explicitly asserted by the claim, but lacks authority support (either unmentioned or prohibited).
- `N/A`: The component is NOT explicitly asserted by the atomic claim. Any unasserted component MUST be marked `N/A`.

Rules:

- `attested entity ≠ attested relationship`
- `attested practice ≠ attested motive`
- `attested affordance ≠ attested causal origin`
- `attested coexistence ≠ attested genealogy`
- `some ≠ all`
- `likely/inferred ≠ observed/certain`
- `missing binding = UNSUPPORTED`

A claim may receive top-level `SUPPORTED` only if every asserted non-`N/A` component is supported at the correct epistemic strength.

A later epistemic label does **not** rescue prose that asserts a stronger proposition than the authority. For example, an authority saying “likely produced” does not support a calibration claim saying “were produced” merely because the auditor labels the claim `QUALIFIED_INFERENCE`.

---

## 3. Epistemic status definitions

Each evaluated claim must be assigned exactly one epistemic status:

- `DOCUMENTED`: The claim is directly observed or explicitly documented as fact in the authority record (e.g., `observed`, direct catalogue descriptions, explicit documented textual limitations).
- `QUALIFIED_INFERENCE`: The claim is an explicit functional or qualified inference licensed in the authority (e.g., under `epistemic_layers.functional_inference`).
- `REPRESENTATIVE_RECONSTRUCTION`: The claim describes a representative workflow licensed in the authority (e.g., under `epistemic_layers.representative_reconstruction`).
- `PROHIBITED`: The claim asserts a proposition that is explicitly prohibited, rejected, or bounded by authority boundaries, prohibitions, or `prohibited_or_rejected_inference` in the packet (e.g., direct evolution/shared transaction between ChM III-937a and OIM A64678, fraud prevention motive, universal exterior impressions, unified code across 5000 years, mandatory developmental sequence, wholesale immediate replacement, private actor motives).
- `UNSUPPORTED`: The claim asserts an entity, relationship, motive, function, causality, sequence, or scope that is absent/unmentioned in the authority without an explicit rejection record (e.g., village elders communal responsibility, urban growth causing memory failure causing token invention).

---

## 4. Standardized Missing-Binding vocabulary

When an asserted component is `UNSUPPORTED`, the auditor MUST select and report the exact standardized identifier(s) from the following frozen vocabulary in the `missing_bindings` array:

- `same_transaction_relationship`
- `communal_responsibility`
- `Sumerian_village_elders`
- `fraud_prevention_motive`
- `long_distance_causal_origin`
- `administrator`
- `shepherd`
- `sheep_transaction`
- `distrust_motive`
- `urban_growth_to_memory_failure`
- `memory_failure_to_token_invention`
- `breakability_caused_tablet_invention`
- `accountants_abandoned_envelopes`
- `universal_all_envelopes`
- `unified_code_across_5000_years`
- `obligatory_developmental_sequence`
- `immediate_complete_replacement`

If all asserted components are supported, `missing_bindings` MUST be an empty array `[]`.

---

## 5. Binding requirements

Use a `bindings` array. One claim may require more than one authority binding:

- For supported claims, bind the supporting authority statements with `role: "SUPPORTS"`.
- For claims where the authority explicitly states limits or qualifications (e.g. "on some examples", "inferred from context"), bind with `role: "LIMITS"`.
- For claims where the authority explicitly rejects or denies the asserted proposition (e.g. in `substrate_boundaries`, `limitations`, or `prohibited_or_rejected_inference`), bind the rejecting authority statement with `role: "REJECTS"`.
- For claims that assert attested entities (e.g. OIM A64678, ChM III-937a, geometric tokens, cylinder seals) alongside unsupported relationships/motives/sequences, bind the attested entities with `role: "SUPPORTS"`, and bind any explicit negative/limiting boundaries with `role: "REJECTS"` or `role: "LIMITS"`.

Each binding must identify:

```json
{
  "component": "function",
  "record_id": "P01-MAT-0002",
  "locator": "epistemic_layers.functional_inference[0].statement",
  "exact_quote": "Exterior marks made enclosed quantities inspectable without immediately opening the envelope.",
  "role": "SUPPORTS"
}
```

`role` must be one of:
- `SUPPORTS`
- `LIMITS`
- `REJECTS`

Every non-`NONE` quote must be copied verbatim from the supplied authority and must come from the stated record/locator. Do not paraphrase authority wording inside `exact_quote`.

---

## 6. Mandatory output schema

Return exactly 20 evaluation records, one per claim ID.

```json
{
  "claim_id": "CAL-TRUTH-001",
  "atomic_claim": "<exact input claim text>",
  "components": {
    "entity": "SUPPORTED",
    "relationship": "N/A",
    "motive": "N/A",
    "function": "N/A",
    "causality": "N/A",
    "sequence": "N/A",
    "scope": "N/A"
  },
  "bindings": [
    {
      "component": "entity",
      "record_id": "P01-MAT-0001",
      "locator": "epistemic_layers.observed[0].statement",
      "exact_quote": "Small geometric clay objects survive in several forms; some bear incisions.",
      "role": "SUPPORTS"
    }
  ],
  "missing_bindings": [],
  "epistemic_status": "DOCUMENTED",
  "verdict": "SUPPORTED"
}
```

Mandatory top-level fields per record:

1. `claim_id`
2. `atomic_claim`
3. `components`
4. `bindings`
5. `missing_bindings`
6. `epistemic_status`
7. `verdict`

Mandatory component keys:

- `entity`
- `relationship`
- `motive`
- `function`
- `causality`
- `sequence`
- `scope`

No key may be omitted.

Epistemic enum:
- `DOCUMENTED`
- `QUALIFIED_INFERENCE`
- `REPRESENTATIVE_RECONSTRUCTION`
- `UNSUPPORTED`
- `PROHIBITED`

Verdict enum:
- `SUPPORTED`
- `UNSUPPORTED`

---

## 7. Forbidden repair behavior

Do not use phrases such as:

- “this is generally known”;
- “the authority implies” when the implication adds a new motive, institution or causal bridge;
- “universally attested” unless that scope exists in the packet;
- any external fact to rescue a missing relationship.

Do not use one record about Entity B to certify a proposition about Entity A unless the authority explicitly binds the two.

Do not convert an explicit boundary into evidence for a stronger positive claim.

---

## 8. Calibration semantics

You are being calibrated against a frozen gold set that you do not receive.

The calibration scorer will compare:

- all 20 top-level verdicts;
- all 20 epistemic-status labels;
- every component state (all 140 cells);
- record IDs;
- locators;
- exact quotes;
- required missing bindings.

Calibration is strict. Plausibility does not receive partial credit. Zero-tolerance policy requires 100% on every scored dimension.
