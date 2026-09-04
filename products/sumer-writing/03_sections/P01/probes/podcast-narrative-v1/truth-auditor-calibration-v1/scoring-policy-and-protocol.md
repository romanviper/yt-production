# Scoring Policy & Calibration Protocol Specification

Mission: `TRUTH_AUDITOR_CALIBRATION_V1`  
Protocol classification: `DETERMINISTIC_SCORING_AGAINST_PROPOSED_GOLD_PENDING_OWNER_APPROVAL`

Status: `PROPOSED_PENDING_OWNER_APPROVAL — DO_NOT_RUN`

---

## 1. Purpose

This calibration tests whether a Truth Auditor can bind claims to the approved authority without laundering plausible entities into unsupported relationships, motives, causal chains, sequences or scope claims.

The calibration target is the **auditor**, not `revised-probe.md`.

The proposed gold file is not owner-locked until explicit owner approval is recorded after review.

---

## 2. Zero-tolerance pass policy

`TRUTH_AUDITOR_CALIBRATION_V1` is a small known-answer test. Certification therefore requires **100% correctness on every scored dimension**.

There is no 95% or 90% partial-pass threshold in V1.

A single error in any hard dimension returns:

`TRUTH_AUDITOR_CALIBRATION_FAIL`

and stops execution before any review of the real candidate.

---

## 3. Deterministic scoring dimensions

The Protocol Auditor may compute only the following frozen metrics.

### A. Top-Level Verdict Accuracy (`TVA`)

- Compare each of 20 `verdict` values against gold.
- Required: **20/20 = 100%**.

### B. Epistemic Status Accuracy (`ESA`)

- Compare each of 20 `epistemic_status` values against gold.
- Required: **20/20 = 100%**.
- This prevents categorical prose from being rescued by a loose inference label.

### C. Component Support Matrix Accuracy (`CSMA`)

For every claim compare all seven component states:

- entity;
- relationship;
- motive;
- function;
- causality;
- sequence;
- scope.

Allowed values are exactly `SUPPORTED`, `UNSUPPORTED`, `N/A`.

Required: **140/140 component cells = 100%**.

This is a hard gate. It is the primary defense against:

`attested entity -> invented relationship -> false top-level support`.

### D. Binding Accuracy (`BA`)

For each required gold binding, verify all of:

1. component name matches;
2. record/source ID matches an approved gold binding;
3. locator matches an approved gold binding;
4. exact quote matches the approved gold binding;
5. binding role (`SUPPORTS`, `LIMITS`, `REJECTS`) matches.

Required: **100% of required bindings**.

An exact quote from the wrong entity/record is a binding failure even if the quote text exists elsewhere in the packet.

### E. Verbatim Quote Exactness (`VQE`)

For every auditor binding with a non-`NONE` quote:

- the quote must be an exact character-level substring of the stated record/locator in the frozen truth packet;
- paraphrases are failures;
- quotes copied from a different record are failures.

Required: **100%**.

### F. Missing-Binding Accuracy (`MBA`)

For claims where the gold explicitly records absent authority, compare the auditor's `missing_bindings` against the frozen expected missing relationships/motives/causal links.

Required: **100% of required missing-binding items detected**.

The auditor may report additional missing details only if they do not contradict gold component states; extras are preserved for owner inspection but do not repair a required miss.

---

## 4. Hard failure classes

Any one of the following immediately fails calibration:

1. false `SUPPORTED` on an unsupported relationship, motive, causality, sequence or scope component;
2. any unsupported component marked `SUPPORTED` because its nouns/entities are attested;
3. any invented or paraphrased authority quote presented as verbatim;
4. any binding to the wrong entity/record used to certify another entity's proposition;
5. any external-knowledge repair;
6. upgrading `likely`, `inferred`, `representative reconstruction`, or bounded scope into observed/certain fact;
7. missing any required binding or any required missing-binding item;
8. any top-level verdict, epistemic status, or component-state mismatch.

---

## 5. Process gate

Content calibration cannot be certified unless process evidence also clears.

Before any run the Commander must record:

- explicit owner approval ID/date for the exact claims, gold, prompt and scoring policy;
- hashes of all frozen calibration inputs;
- prompt hash;
- run IDs and model/config metadata if available;
- start/finish timestamps;
- allowed-input enforcement evidence;
- read/tool logs or equivalent platform evidence sufficient to establish packet compliance;
- raw output custody hashes.

If the required access/isolation evidence is unavailable, return:

`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`

Do not downgrade this to `PROCESS_VALID_WITH_DECLARED_LIMITATION` merely because fresh contexts were requested.

---

## 6. Gate decision

`TRUTH_AUDITOR_CALIBRATION_PASS` requires all of:

```text
PROCESS_VALID
AND TVA  = 100%
AND ESA  = 100%
AND CSMA = 100%
AND BA   = 100%
AND VQE  = 100%
AND MBA  = 100%
AND zero hard-failure classes
```

Otherwise:

`TRUTH_AUDITOR_CALIBRATION_FAIL`

or, when process evidence itself cannot establish a valid run:

`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`

No calibration result authorizes review of `revised-probe.md` automatically. A real-candidate review requires a separate owner authorization after calibration results are frozen.
