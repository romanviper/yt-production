# Planning Commander Proposal: Truth Auditor Calibration V1 — Corrected Packet

To: **Product & System Owner**  
From: **Planning Commander**  
Mission: `TRUTH_AUDITOR_CALIBRATION_V1`  
Status: `CORRECTED_PACKET_PENDING_OWNER_APPROVAL — NO_EXECUTION — NO_WRITER`

---

## 1. Purpose

This proposal submits the corrected calibration packet for owner review. It does **not** claim that the gold set is already owner-locked or semantically validated.

The mission tests whether a Truth Auditor can distinguish supported entities from unsupported relationships, motives, functions, causal directions, sequences and scope claims before the role is allowed to inspect any real production candidate.

No Truth Auditor, Product Reviewer or Writer run is authorized by this proposal.

---

## 2. Corrections applied after review of commit `7366eec`

The original proposal had four material design defects. They are corrected here:

1. **Wrong-entity gold binding removed**
   - Old `CAL-TRUTH-017` attempted to certify a token proposition with a cylinder-seal record.
   - New `CAL-TRUTH-017` is a cylinder-seal negative statement bound to the cylinder-seal record itself.

2. **Epistemic overstatement removed**
   - Old `CAL-TRUTH-019` said marks “were produced” by reed tools while authority said “likely produced”.
   - New claim preserves `likely` in the claim text and remains `QUALIFIED_INFERENCE`.

3. **Component-level binding introduced**
   - Auditor output now uses a `bindings` array and seven independently scored component states.
   - One supported noun can no longer mechanically rescue an unsupported relationship.

4. **Scoring tightened to 100%**
   - Top-level verdict, epistemic status, all component cells, required bindings, verbatim quotes and required missing bindings must all score 100%.
   - The previous 95%/90% partial thresholds are removed for Calibration V1.

---

## 3. Corrected packet

Directory:

`products/sumer-writing/03_sections/P01/probes/podcast-narrative-v1/truth-auditor-calibration-v1/`

| File | Current Git Blob Hash | Status |
|---|---|---|
| `truth-calibration-claims.json` | `ff44ef68a8e66e13f2d2e6a6c362bcdf70f6194f` | Proposed fixture pending owner approval |
| `truth-calibration-gold.json` | `412ac4baf92d19a4b38e5497c7333573e9e24f58` | `PROPOSED_GOLD_PENDING_OWNER_APPROVAL` |
| `truth-auditor-prompt.md` | `c7f2bdf6b81104fad4d9964055af4447d4767936` | Proposed prompt pending owner approval |
| `scoring-policy-and-protocol.md` | `f2457a7f380027f07a23def11543e023456b33cf` | Proposed zero-tolerance scoring policy |
| `../product-reviewer-calibration-v1/README.md` | `d7de8f5d770ad99a4edfcb1d09a28336d8dca882` | Reserved only; no Product mission started |

The pre-existing bounded authority packet remains:

`planning-agents-team-v1/truth-record-packet.json`  
Git blob: `d328b983a5582f8d8ecd039fd84e74b0a826ca29`

---

## 4. Calibration design

The fixture retains 20 claims across ten failure-mode categories:

1. direct documented fact;
2. qualified functional inference;
3. representative reconstruction;
4. correct entities with unsupported relationship;
5. correct entity with unsupported motive;
6. plausible causal explanation with no binding;
7. scope/quantifier overreach;
8. coexistence converted into genealogy/replacement;
9. exact supported negative statement;
10. inference whose epistemic qualification must remain visible.

The proposed verdict balance remains 10 `SUPPORTED` / 10 `UNSUPPORTED`.

The claims were rewritten where needed to reduce compound propositions and make the component under test explicit.

---

## 5. Gold semantics

`truth-calibration-gold.json` is presently a **proposal**, not an owner-approved answer key.

Each gold record now contains:

- expected top-level verdict;
- required epistemic status;
- expected support state for seven components;
- required exact bindings with component, record ID, locator, exact quote and binding role;
- explicit `missing_bindings` where unsupported relationships have no authority wording that could license them;
- bounded deterministic rationale.

Exact string existence alone does not establish semantic correctness. Owner review must confirm that each quote belongs to the correct record/entity/component before approval.

---

## 6. Proposed scoring gate

Calibration passes only if all dimensions are perfect:

```text
PROCESS_VALID
AND 20/20 top-level verdicts correct
AND 20/20 epistemic statuses correct
AND 140/140 component states correct
AND 100% required binding accuracy
AND 100% verbatim quote exactness
AND 100% required missing bindings detected
AND zero external-knowledge repair
AND zero wrong-entity binding
```

Any content error returns:

`TRUTH_AUDITOR_CALIBRATION_FAIL`

If platform evidence cannot establish packet compliance/context isolation:

`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`

Sibling agreement cannot override a gold failure.

---

## 7. Execution boundary after approval

Even after owner approval of this packet:

1. approval authorizes only the calibration run;
2. the gold file must be withheld from auditors;
3. raw auditor output must be frozen before scoring;
4. Protocol Auditor may score mechanically but may not alter gold or adjudicate historical semantics;
5. calibration PASS does **not** authorize review of `revised-probe.md`;
6. real-candidate review requires a separate owner authorization;
7. Product Reviewer calibration remains a separate later mission;
8. Writer remains stopped.

---

## 8. Owner decision requested

Please choose one:

- **APPROVE CALIBRATION PACKET** — freeze these exact blobs as owner-approved inputs and authorize only `TRUTH_AUDITOR_CALIBRATION_V1` execution;
- **MODIFY** — return specific corrections; no execution;
- **REJECT** — stop calibration design.

Current status:

`CORRECTED_PACKET_PENDING_OWNER_APPROVAL — NO_EXECUTION — NO_WRITER`
