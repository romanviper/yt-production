# Planning Agents Team — Calibration-Gated Handoff

Status: `CALIBRATION_GATED_TEAM_HANDOFF_READY — NO_REAL_CANDIDATE_REVIEW — NO_WRITER`

## Context

`PLANNING_AGENTS_TEAM_V1` remains preserved as a failed validation experiment. Commit `5de377be1fd8994d0d86868588ca54ac43f4e9a7` is failure evidence, and commit `2d5225a0ecd8e193b6ded2fb9568e5b963a108f4` is the valid supersession/correction record.

The multi-agent operating model is **not abandoned**. What is abandoned is the assumption that sibling concurrence can manufacture truth or reliability.

The next operating principle is:

> Multi-agent redundancy may test stability, but only a calibrated role may be trusted to adjudicate a real candidate.

Agreement between two uncalibrated agents is not validation.

---

## 1. Primary objective

Before any new review of `revised-probe.md`, prove that the specialist roles themselves can perform their assigned jobs on owner-locked test cases with known answers.

Run two separate calibration missions in sequence:

1. `TRUTH_AUDITOR_CALIBRATION_V1`
2. `PRODUCT_REVIEWER_CALIBRATION_V1`

Only after both calibration gates pass may the owner authorize a new real-candidate review mission.

The Writer remains outside this process and receives nothing.

---

## 2. Team topology retained

```text
Owner
  |
  v
Planning Commander
  |
  +---- Packet Custodian
  |
  +---- Truth Auditor calibration role(s)
  |
  +---- Product Reviewer calibration role(s)
  |
  +---- Protocol Auditor (process only)
  |
  v
Owner calibration gate
  |
  +---- fail -> STOP / revise evaluator protocol or model objective
  |
  +---- pass -> owner may authorize real-candidate review mission
```

The topology remains multi-agent. The semantic meaning of concurrence changes:

```text
A == B
```

means only:

> the two executions are stable with respect to one another.

It does **not** mean:

> their conclusion is true.

---

## 3. Commander authority

The Commander is an orchestrator, not a meta-reviewer.

### Commander may

- freeze mission scope;
- commission deterministic calibration packets;
- record owner approvals;
- launch bounded specialist runs only after gates clear;
- preserve raw outputs and hashes;
- mechanically compare specialist answers against owner-locked gold labels where the mission explicitly authorizes such comparison;
- stop execution when a gate fails;
- return raw scores, mismatches and blockers to the owner.

### Commander may not

- reinterpret authority wording to save an auditor answer;
- choose which calibration errors are “close enough” unless the owner-approved scoring policy permits it;
- convert sibling agreement into validation;
- create Writer instructions;
- create repair routes for the real candidate;
- promote calibration insights into canonical story architecture;
- silently alter gold answers, prompts or packets after runs begin;
- automatically create Team V2 or rerun until consensus appears.

---

## 4. Mission A — `TRUTH_AUDITOR_CALIBRATION_V1`

### Goal

Demonstrate that a Truth Auditor can distinguish:

- attested entity;
- attested relationship;
- attested motive;
- attested function;
- attested causal direction;
- attested sequence;
- qualified inference;
- unsupported but plausible claim;
- prohibited claim.

The calibration target is the **auditor**, not `revised-probe.md`.

The real candidate must not be used as the calibration test.

### Calibration set

Create an owner-reviewable gold set of approximately 15–25 atomic claims drawn from the already approved P01 authority.

The set should deliberately mix categories such as:

1. direct documented fact;
2. qualified functional inference;
3. allowed representative reconstruction;
4. entity correct but relationship unsupported;
5. entity correct but motive unsupported;
6. plausible causal explanation with no binding;
7. scope/quantifier overreach (`some` -> `all`);
8. coexistence incorrectly converted into genealogy;
9. exact supported negative statement;
10. inference whose epistemic status must remain visible.

Representative examples of test *shape* only:

```text
SUPPORTED:
Exterior marks on some envelopes can make information about enclosed quantity inspectable without immediately opening the envelope.

UNSUPPORTED:
Bullae were invented to prevent fraud.

SUPPORTED:
Cylinder-seal impressions can mark an association with authority, custody or witnessing.

UNSUPPORTED:
Cylinder seals guaranteed institutional legitimacy and communal responsibility.
```

These examples do not replace the actual owner-approved calibration set.

### Gold-answer creation

The calibration gold file must be created and frozen **before any auditor run**.

For every atomic test claim, the gold record must include:

- calibration claim ID;
- exact claim text;
- expected verdict;
- exact authority record ID;
- exact authority field/locator;
- exact authority wording quoted verbatim;
- component type: entity / relationship / motive / function / causality / sequence / scope / inference;
- required epistemic status;
- short deterministic rationale limited to what the quoted authority licenses.

The owner must approve the calibration set, gold answers, scoring policy and auditor prompt before execution.

### Mandatory auditor schema

For every candidate calibration claim, the auditor must output:

```text
claim_id
atomic_claim
claim_components
exact_authority_record_id
exact_authority_field_or_locator
exact_authority_quote
entity_supported
relationship_supported
motive_supported
function_supported
causal_direction_supported
sequence_supported
scope_or_quantifier_supported
epistemic_status
verdict
```

Fields not applicable may be `N/A`, but may not be silently omitted.

### Exact-binding rule

The central calibration rule is:

> If a relationship, motive, consequence, causal direction, sequence, or quantifier is not present in exact authority wording or a logically direct equivalent licensed by that exact wording, the auditor may not mark that component `SUPPORTED`.

The auditor may not use:

- “this is generally known”;
- “the authority implies” when the implication adds a new causal or institutional relationship;
- external archaeology;
- plausible historical background;
- nouns elsewhere in the packet as evidence for an unsupported relationship.

Missing binding remains missing.

### Scoring

The scoring policy must be owner-approved before runs.

Default proposed hard requirements:

- zero false `SUPPORTED` verdicts on unsupported motive/causal/relationship test cases;
- zero invented authority quotes;
- zero external-knowledge repairs;
- all scope/quantifier traps correctly detected;
- all prohibited genealogy cases correctly detected;
- exact-authority locator/quote present for every supported component;
- overall classification accuracy threshold chosen and approved by owner before run.

A sibling pair is optional for calibration stability testing, but sibling agreement cannot override gold-answer failure.

If the auditor fails a hard requirement:

`TRUTH_AUDITOR_CALIBRATION_FAIL`

Stop. Do not review the real candidate.

The next action must be to change the evaluator protocol, schema, model objective or model configuration under a separately authorized mission—not to add more votes.

---

## 5. Mission B — `PRODUCT_REVIEWER_CALIBRATION_V1`

This mission begins only after the Truth calibration mission is frozen. It is logically independent from Truth calibration and does not use truth answers to score product quality.

### Goal

Demonstrate that a Product Reviewer evaluates the text actually present rather than mentally constructing a stronger story and scoring the constructed story.

### Calibration set

Prepare a small owner-approved set of product passages/examples representing deliberately different modes, for example:

- genuine narrative/investigative movement;
- fluent explanatory essay;
- material-rich catalogue/exposition;
- passage with apparent momentum created by an invented causal chain;
- passage with strong sensory prose but no persistent narrative movement;
- passage with a real documented carrier and progressive expansion of meaning.

The set may use synthetic or carefully selected non-P01 examples if doing so reduces anchoring to the current candidate. It must not expose previous reviewer verdicts.

### Gold labels

Gold labels should not dictate one prose formula. They should specify observable product functions and known failure modes, such as:

- whether a persistent carrier actually exists in the text;
- whether a question is actually established and sustained;
- whether stakes/consequence are present or merely inferred by the reviewer;
- whether scale transitions occur in the prose;
- whether the reviewer invented fraud, transport, actor, motive, scene or causality not stated by the passage;
- whether product judgment is separated from factual certification.

The owner must approve the calibration examples, rubric, expected labels and prompt before execution.

### Critical reviewer rule

> Review only the story/movement evidenced by the supplied passage. Do not improve the passage in your head and then grade the imagined version.

If a reviewer writes an unstated chain such as:

```text
memory overload -> fraud/transport problem -> bulla solution -> redundancy -> tablet
```

that chain must be tagged `REVIEWER_ADDED_INTERPRETATION` unless each element is actually present in the candidate text supplied to the reviewer.

Product Reviewer is forbidden from certifying historical accuracy.

### Calibration failure

If a reviewer repeatedly rewards reviewer-added narrative or crosses into truth certification:

`PRODUCT_REVIEWER_CALIBRATION_FAIL`

Stop. Do not review the real candidate.

---

## 6. Protocol Auditor role under the calibration-gated model

Protocol Auditor remains process-only.

It may verify:

- owner approval IDs/dates;
- frozen prompt hashes;
- frozen calibration packet hashes;
- run IDs and model/config metadata when available;
- start/finish timestamps;
- allowed-input enforcement evidence;
- tool/read logs where available;
- raw output custody and hashes;
- schema completeness;
- exact quoted-span existence;
- deterministic score computation against the already frozen gold file.

It may **not**:

- decide whether a gold answer is historically correct;
- change a gold answer after seeing auditor output;
- decide whether a product judgment is aesthetically right;
- reinterpret an authority binding;
- declare truth compliance for the real candidate;
- turn calibration failures into Writer advice.

If the required access evidence is unavailable, use:

`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`

Do not downgrade this to a softer pass by self-attestation.

---

## 7. Required owner gates

No calibration role may run until the corresponding owner gate is explicit and recorded.

### Before Truth calibration

Owner must approve:

- calibration claim set;
- gold answers;
- exact authority quotes/locators;
- truth-audit schema;
- scoring policy;
- auditor prompt;
- model/config selection if selectable;
- process-evidence standard.

Otherwise:

`TRUTH_CALIBRATION_PACKET_BLOCKED`

### Before Product calibration

Owner must approve:

- calibration passage set;
- product rubric;
- gold/expected labels;
- benchmark excerpt, if any;
- Product prompt;
- scoring policy;
- model/config selection if selectable;
- process-evidence standard.

Otherwise:

`PRODUCT_CALIBRATION_PACKET_BLOCKED`

---

## 8. Real-candidate review is a later mission

Passing calibration does **not** itself validate `revised-probe.md`.

If both evaluator calibration missions pass, the Commander must stop and return:

`EVALUATOR_CALIBRATION_COMPLETE — REAL_CANDIDATE_REVIEW_REQUIRES_OWNER_AUTHORIZATION`

A later mission may then review the real candidate with calibrated roles and newly frozen packets.

That later mission must preserve:

- Product and Truth authority separation;
- raw output immutability;
- no voting as truth;
- concurrence as stability signal only;
- exact claim binding for Truth;
- no reviewer-added story rewarded by Product;
- Protocol Auditor as process-only;
- Owner as the only route-selection authority.

---

## 9. Writer hard boundary

No part of this handoff authorizes:

- new Writer prose;
- revision of `revised-probe.md`;
- a fresh Writer sample;
- a Writer repair brief;
- canonical section planning changes;
- Historical Substrate changes;
- evidence expansion;
- benchmark imitation;
- automatic Team V2 execution.

Writer status remains:

`STOPPED — NO_WRITER`

---

## 10. Interpretation of V1 going forward

`PLANNING_AGENTS_TEAM_V1` is retained because its failure is informative.

It demonstrated:

1. anonymization and packet bounding are useful but insufficient;
2. duplicated reviewers can share correlated hallucinations;
3. consensus does not establish truth;
4. Product Reviewers can hallucinate a better causal story than the passage contains;
5. Truth Auditors can turn attested nouns into unsupported relationships;
6. Protocol Auditors can become semantic reviewers if authority is not kept narrow;
7. Commander synthesis can launder bad specialist outputs into actionable-looking routes.

The correction is not “use fewer agents.”

The correction is:

> Calibrate each semantic role against owner-locked ground truth before granting it authority over a real production candidate.

---

## 11. Immediate next action

The next authorized planning action after this handoff is only:

> Prepare the proposed `TRUTH_AUDITOR_CALIBRATION_V1` packet and gold set for owner review.

Do not run the auditors yet.

Do not create Product calibration artifacts yet unless needed only to reserve a directory/name.

Do not touch the Writer.

Final state:

`HANDOFF_COMPLETE — PREPARE_TRUTH_CALIBRATION_FOR_OWNER_APPROVAL — NO_EXECUTION — NO_WRITER`
