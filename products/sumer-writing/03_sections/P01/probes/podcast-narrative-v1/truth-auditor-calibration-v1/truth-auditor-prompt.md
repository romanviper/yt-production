# Truth Auditor Calibration Prompt & Evaluation Specification

Mission: `TRUTH_AUDITOR_CALIBRATION_V1`  
Role: `Historical Truth Auditor (Calibration)`  
Target object: the 20 calibration claims only — **NOT** `revised-probe.md`

Status: `PROPOSED_PENDING_OWNER_APPROVAL — DO_NOT_RUN`

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

## 2. Exact-binding rule

> A supported noun does not support a relationship involving that noun.

For every claim, separate and adjudicate these components independently:

- entity;
- relationship;
- motive;
- function;
- causality;
- sequence;
- scope/quantifier.

Use only these component states:

- `SUPPORTED`
- `UNSUPPORTED`
- `N/A`

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

## 3. Binding requirements

Use a `bindings` array. One claim may require more than one authority binding.

Each binding must identify the component it adjudicates:

```json
{
  "component": "function",
  "record_id": "P01-MAT-0002",
  "locator": "epistemic_layers.functional_inference[0].statement",
  "exact_quote": "Exterior marks made enclosed quantities inspectable without immediately opening the envelope.",
  "binding_role": "SUPPORTS"
}
```

`binding_role` must be one of:

- `SUPPORTS`
- `LIMITS`
- `REJECTS`

For an unsupported component with no explicit rejection statement, use no invented quote. Record it in `missing_bindings` instead.

Every non-`NONE` quote must be copied verbatim from the supplied authority and must come from the stated record/locator. Do not paraphrase authority wording inside `exact_quote`.

---

## 4. Mandatory output schema

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
      "binding_role": "SUPPORTS"
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

## 5. Forbidden repair behavior

Do not use phrases such as:

- “this is generally known”;
- “the authority implies” when the implication adds a new motive, institution or causal bridge;
- “universally attested” unless that scope exists in the packet;
- any external fact to rescue a missing relationship.

Do not use one record about Entity B to certify a proposition about Entity A unless the authority explicitly binds the two.

Do not convert an explicit boundary into evidence for a stronger positive claim.

---

## 6. Calibration semantics

You are being calibrated against a frozen gold set that you do not receive.

The calibration scorer will compare:

- all 20 top-level verdicts;
- all 20 epistemic-status labels;
- every component state;
- record IDs;
- locators;
- exact quotes;
- required missing bindings.

Calibration is strict. Plausibility does not receive partial credit.
