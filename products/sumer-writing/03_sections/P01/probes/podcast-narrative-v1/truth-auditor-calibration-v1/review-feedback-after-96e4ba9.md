# Review Feedback After `96e4ba9` — Truth Auditor Calibration V1

Status: `REJECT_CALIBRATION_PASS — CONTENT_GATE_FAIL — PROCESS_BLOCKED — NO_PRODUCT_CALIBRATION — NO_WRITER`

Target commit: `96e4ba9ca9e50250f1d997276d1b49b2a6cbd846`

## 1. Top-level correction

The report status:

`TRUTH_AUDITOR_CALIBRATED — ZERO_FALSE_PASSES — READY_FOR_PRODUCT_CALIBRATION`

is invalid under the frozen calibration policy.

The current calibration result must not be used to certify the Truth Auditor role, to begin Product Reviewer calibration as a downstream consequence, to review the real candidate, or to authorize Writer work.

Correct state:

```text
TRUTH_AUDITOR_CALIBRATION_V1
— CONTENT_GATE_FAIL
— PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE
— CALIBRATION_NOT_PROVEN
— NO_PRODUCT_CALIBRATION
— NO_REAL_CANDIDATE_REVIEW
— NO_WRITER
```

## 2. The report contradicts the frozen scoring policy

`scoring-policy-and-protocol.md` requires:

- TVA = 20/20;
- ESA = 20/20;
- CSMA = 140/140;
- BA = 100%;
- VQE = 100%;
- MBA = 100%;
- zero hard-failure classes;
- PROCESS_VALID.

The report itself records:

- Auditor A epistemic alignment = 17/20;
- Auditor B epistemic alignment = 18/20.

Therefore both auditors fail ESA immediately. Under the zero-tolerance rule, this alone makes `TRUTH_AUDITOR_CALIBRATION_PASS` impossible.

Concrete examples:

- `CAL-TRUTH-007`: gold requires `UNSUPPORTED`; both auditors return `PROHIBITED`.
- `CAL-TRUTH-013`: gold requires `UNSUPPORTED`; both auditors return `PROHIBITED`.
- Auditor A also mismatches `CAL-TRUTH-010` (`UNSUPPORTED` vs gold `PROHIBITED`).

These are not ignorable because Calibration V1 intentionally requires exact epistemic-status agreement.

## 3. Component Support Matrix also fails

The report does not publish the mandatory `CSMA` score even though it is a hard gate.

Direct comparison of raw outputs to gold shows multiple component-state mismatches.

Examples include:

### Auditor A

- `CAL-TRUTH-010`: gold `causality = N/A`; Auditor A returns `causality = UNSUPPORTED`.
- `CAL-TRUTH-011`: gold `relationship = N/A`, `sequence = N/A`; Auditor A returns both as `UNSUPPORTED`.
- `CAL-TRUTH-012`: gold `relationship = N/A`, `motive = N/A`; Auditor A returns both as `UNSUPPORTED`.
- `CAL-TRUTH-013`: gold `function = N/A`; Auditor A returns `function = SUPPORTED`.

### Auditor B

- `CAL-TRUTH-008`: gold `motive = N/A`; Auditor B returns `motive = UNSUPPORTED`.
- `CAL-TRUTH-010`: gold `causality = N/A`; Auditor B returns `causality = UNSUPPORTED`.
- `CAL-TRUTH-014`: gold `relationship = N/A`, `function = UNSUPPORTED`; Auditor B returns `relationship = UNSUPPORTED`, `function = N/A`.

Therefore `CSMA = 100%` is false for both runs.

The fact that these extra negative classifications are often conservative does not permit a calibration pass. The purpose of this test is to verify precise component discrimination, not merely avoid top-level false support.

## 4. Binding Accuracy was not satisfied or reported

The report claims VQE = 100% but does not report the mandatory Binding Accuracy (`BA`) metric.

Exact quote existence is not equivalent to correct binding completeness.

Several raw answers omit gold-required bindings. For example:

- `CAL-TRUTH-007` gold requires support bindings for both attested entities plus the rejecting relationship binding; raw outputs provide only a subset.
- `CAL-TRUTH-008` gold requires an entity support binding, a bounded function `LIMITS` binding, and a relationship `LIMITS` binding; raw outputs omit part or most of this structure.
- `CAL-TRUTH-009` gold requires two rejecting motive bindings (statement and qualification); raw outputs provide only one.
- `CAL-TRUTH-012` gold requires the supported breakability function plus two rejecting sequence/coexistence bindings; raw outputs do not reproduce the full set.

Thus the required statement:

`BA = 100%`

has not been demonstrated and is contradicted by inspection of the raw files.

## 5. Missing-Binding scoring is not auditable as deterministic

The gold file uses frozen identifiers such as:

- `same_transaction_relationship`;
- `fraud_prevention_motive`;
- `urban_growth_to_memory_failure`;
- `universal_all_envelopes`.

The raw auditors generally return free-form natural-language descriptions instead.

The report states `MBA = 100% (17/17 caught)` but does not include a deterministic normalization/mapping artifact showing how free-form strings were matched to the frozen gold items.

Without a frozen normalization rule or exact item mapping, this is semantic adjudication disguised as deterministic scoring.

Protocol Auditor must not invent equivalence mappings after seeing outputs.

## 6. Process gate is not established

Commit `96e4ba9` adds only:

- `truth-auditor-a-raw.json`;
- `truth-auditor-b-raw.json`;
- `truth-calibration-report.md`.

It does not commit auditable evidence for the process requirements still relevant after `owner-interaction-operating-rule.md`, including:

- exact frozen prompt/input hashes used at execution time;
- model/config metadata sufficient for reproduction;
- start/finish timestamps;
- read/tool-access logs or equivalent platform evidence;
- output custody lineage from run to committed raw artifact;
- deterministic scoring artifact showing every metric cell.

`owner-interaction-operating-rule.md` supersedes the old requirement to wait for owner approval of internal technical calibration. It does **not** waive the evidence required to claim context isolation or `PROCESS_VALID`.

Therefore the process result is:

`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`

unless and until the required execution evidence exists.

## 7. Overclaim in the calibration report

The statement that the exact-binding rule and component-level breakdown:

> "completely eliminate the correlated false pass failure mode"

is not supportable.

Even a perfect 20-case calibration run would establish only bounded performance on that frozen fixture. It would not prove that a model failure mode is eliminated generally.

Allowed conclusion after a valid pass would be closer to:

> The tested auditor configuration passed the frozen Calibration V1 fixture without false support on the included relationship/motive/causality traps.

No stronger general reliability claim is authorized.

## 8. Required internal correction

Do not run Product Reviewer calibration yet.

The next internal action is:

1. supersede `truth-calibration-report.md` pass status;
2. generate a deterministic machine-readable scorecard covering all 20 verdicts, 20 epistemic statuses, 140 component cells, every required binding, every quote, and every required missing binding;
3. resolve the mismatch between free-form `missing_bindings` output and deterministic MBA scoring;
4. harmonize stale owner-approval language in the scoring policy with `owner-interaction-operating-rule.md` without weakening process-evidence requirements;
5. decide internally whether to rerun the same auditor configuration under the identical corrected fixture/prompt or revise the auditor schema/configuration;
6. preserve this run as calibration failure evidence;
7. do not surface process artifacts to the owner as a decision request.

## 9. Product objective remains unchanged

This correction must not become another long detour that displaces the product objective.

The system exists to reach a meaningful new P01 probe that:

- sounds like compelling history podcast rather than explanatory essay;
- does not obtain momentum through invented historical causality;
- passes internal product/truth controls before owner review.

The owner-facing human gate remains the completed meaningful probe.
