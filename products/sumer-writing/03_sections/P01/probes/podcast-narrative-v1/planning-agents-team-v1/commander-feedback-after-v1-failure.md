# P01 Planning Agents Team V1 — Commander Correction After Failed Validation

Status: `MISSION_INVALID — TRUTH_FALSE_PASS — PRODUCT_STABILITY_UNVALIDATED — PROCESS_EVIDENCE_INSUFFICIENT — COMMANDER_SCOPE_BREACH — NO_WRITER`

## Purpose

This memo is owner-authorized feedback to the Planning Commander after review of commit `5de377be1fd8994d0d86868588ca54ac43f4e9a7`.

Commit `5de377b` must be preserved as experimental evidence. It does **not** validate `revised-probe.md`, reviewer independence, truth compliance, product readiness, or canonical planning.

The Planning Commander must not use any route, recommendation, `PASS`, `NEAR_BAR`, truth verdict, or protocol verdict from that commit as authority for a Writer brief or production decision.

No Writer run is authorized by this memo.

---

## Corrected mission verdict

The correct status of `P01-REVIEWER-INDEPENDENCE-VALIDATION-01` is:

```text
MISSION_INVALID
— TRUTH_FALSE_PASS
— PRODUCT_STABILITY_UNVALIDATED
— PROCESS_EVIDENCE_INSUFFICIENT
— COMMANDER_SCOPE_BREACH
— NO_WRITER
```

The following conclusions from the V1 team are superseded and must not control later decisions:

- `Truth A = PASS / LOW` as validation evidence;
- `Truth B = PASS / LOW` as validation evidence;
- `TRUTH_A_B_CONCURRENCE = CONCURRENCE_VALIDATED` as evidence of truth reliability;
- `PROCESS_VALID_WITH_DECLARED_LIMITATION`;
- any statement that historical truth compliance was verified;
- any statement that reviewer bias was corrected or independently validated;
- any claim that the candidate's causal structure is historically supported;
- any proposed micro-amendment or canonical-planning route in `owner-decision-packet.md`.

Retain all raw artifacts and hashes unchanged as evidence of the failure mode.

---

# 1. P0 — Truth A/B produced a correlated false pass

Both Truth Auditors converted missing relationship bindings into `SUPPORTED` or acceptable inference.

The candidate asserts or strongly implies relationships such as:

```text
urban expansion
→ grain/livestock/labor flows exceed human oversight or memory
→ external material recording becomes necessary
```

and:

```text
transfer/preservation in transactions
→ use of hollow envelopes
```

and:

```text
intact envelope
→ guaranteed integrity of the enclosed counter set
```

and:

```text
seal impression
→ legitimacy / supervisory rights / communal responsibility
```

and:

```text
urban expansion + thousands of complex transactions
→ clay surfaces progress beyond numbers
```

The bounded authority packet does not establish those motives, causal origins, consequences, transaction assignments, or historical sequences.

The fact that both auditors produced the same error is not independent confirmation. It is evidence of **correlated model error**.

### Commander rule from now on

Never convert A/B concurrence into truth confidence unless the underlying bindings survive mechanical verification.

For truth adjudication:

```text
attested entity or practice
≠ attested motive
≠ attested causal origin
≠ attested consequence
≠ attested transaction
≠ attested historical sequence
```

Agreement among agents cannot manufacture a missing relation.

---

# 2. Exact authority wording is mandatory

A Truth Auditor may no longer paraphrase authority into stronger wording and then bind the candidate to that paraphrase.

Every nontrivial relationship claim must be checked against **exact authority text**.

The minimum binding record must contain:

```text
candidate_span
claim_component
claim_type
exact_authority_record_id
exact_authority_field_or_locator
exact_authority_wording
relationship_actually_asserted
relationship_explicitly_present_in_authority: yes/no
verdict
```

If the relationship actually asserted by the candidate does not appear in the exact authority wording, the auditor must return one of:

- `QUALIFIED_INFERENCE` only when the authority itself licenses that inference;
- `UNSUPPORTED`;
- `PROHIBITED`;
- `BLOCKED — MISSING_BINDING`.

It must **not** be upgraded because it is historically plausible, commonly believed, implied by context, or agreed upon by another auditor.

No number of sibling auditors can upgrade `MISSING_BINDING` into `SUPPORTED`.

---

# 3. Truth concurrence must not be treated as validation by itself

The V1 assumption:

```text
Truth A PASS
+
Truth B PASS
→ stable truth result
```

has failed.

A future team must distinguish:

```text
verdict concurrence
```

from:

```text
binding validity
```

A/B concurrence is only evidence that two executions produced the same judgment. It is **not** evidence that the judgment is correct.

If both agents cite authority wording that does not exist or does not support the asserted relation, the result is a correlated false pass.

---

# 4. Product A/B also reproduced the same invented causal narrative

Both Product Reviewers read the candidate through a stronger causal story than the text and authority can establish.

They reconstructed variants of:

```text
urban memory overload
→ tokens
→ secure transfer
→ bulla
→ destructive verification problem
→ exterior marks
→ envelope redundancy
→ numerical tablet
```

Some outputs additionally introduced fraud, transport/shipment, transaction security, or the question of why the hollow envelope was still necessary.

This means Product A/B did not merely evaluate the listening experience. They partly authored a more coherent story in their own reading and then rewarded the candidate for that story.

### Commander rule from now on

Product Reviewers may report:

- what the listener is likely to infer from the text;
- what they experience as the passage's apparent narrative engine;
- whether that inferred engine is compelling.

They may **not** certify that the inferred engine is historically true.

If a reviewer introduces a scene, actor, motive, fraud scenario, transaction, excavation method, site detail, or causal step not literally present in the candidate, it must be labeled:

`REVIEWER_ADDED_INTERPRETATION`

and must not be counted as a product strength of the candidate itself.

---

# 5. Product role may not cross into truth adjudication

Product Reviewers in V1 made claims about historical accuracy, anti-teleological rigor, factual validity, and proposed unsupported actors/sites/technical details.

That violates role separation.

A Product Review may judge whether a passage *sounds* confident, explanatory, causal, immersive, or academically self-conscious. It may not decide whether a historical relationship is supported by evidence.

Any future Product output containing a truth certificate such as:

- historically accurate;
- factually correct;
- archaeological reality verified;
- truth-safe;
- no fabrication;

must be marked `ROLE_BOUNDARY_BREACH` unless an explicitly authorized cross-role mission exists.

---

# 6. Protocol Auditor exceeded its authority

The V1 Protocol Auditor was authorized to validate process, not historical or product semantics.

It nevertheless adjudicated content, including whether specific claims were acceptable inferences, whether truth compliance was achieved, whether contamination was ideologically absent, and which craft defect was actionable.

Those judgments are outside the Protocol role.

### Correct Protocol role

The Protocol Auditor may verify only things such as:

- exact input/output hashes;
- candidate equality;
- prompt/schema conformance;
- file/packet boundaries;
- run identity evidence;
- timestamps;
- tool/read-access logs;
- output custody;
- whether required fields exist;
- whether quoted candidate spans mechanically exist;
- whether sibling verdicts differ.

It may not determine:

- whether an authority binding is semantically valid;
- whether a missing claim matters historically;
- whether the prose is good;
- whether a reviewer hallucinated a causal interpretation;
- whether a craft defect should be repaired.

A semantic meta-audit is a different role and requires separate owner authorization.

---

# 7. Process evidence did not satisfy the handoff

The handoff required stronger evidence for reviewer independence than a declared allowed/denied input list.

The committed `run-manifest.json` does not contain a complete audit trail for:

- full run/thread IDs for every execution in the manifest itself;
- exact model and reasoning configuration;
- `fork_turns` or equivalent inheritance evidence;
- frozen prompt bodies and prompt hashes;
- start/finish timestamps;
- complete read/tool-access logs;
- transcript or equivalent non-inheritance evidence;
- output-custody lineage from raw transport to committed file.

The Protocol Auditor later asserted that transcripts verified isolation and that all metadata were registered, but those claims are not fully supported by the committed manifest/evidence set.

Under the existing handoff, self-attestation or denied-input declarations without enforceable/access evidence require:

`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`

Therefore the corrected Protocol verdict for V1 is:

`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`

Do not describe V1 as an independence-validation success with a limitation.

---

# 8. Owner approval gate was skipped

The original handoff required owner approval of:

- the bounded FoC excerpt / selection rule;
- the frozen Product rubric/prompt;

before Product A/B could run.

If that approval is not represented by explicit owner authorization evidence in the mission record, the proper pre-run state was:

- `BENCHMARK_PACKET_BLOCKED`, and/or
- `PRODUCT_RUBRIC_BLOCKED`.

The Commander may not infer approval from the existence of repository benchmark files or from previous general product direction.

A future mission must record at minimum:

```text
approval_subject
approved_artifact_or_hash
owner_approval_reference
approval_timestamp_or_commit_context
```

before launching dependent specialists.

---

# 9. Commander scope correction

The Commander is an orchestrator, not an editor or planner.

It may return bounded owner decision states. It may not convert reviewer findings into a concrete repair plan unless a separate owner-authorized planning mission exists.

V1 crossed this boundary by proposing, among other things:

- replacing specific counts of `người ta`;
- introducing concrete administrative roles;
- adding specific excavation/site anchors;
- turning V1 findings into canonical planning insight.

Those are content-planning actions built on invalid content verdicts.

### Commander output after an invalid mission

When a mission is invalid, the Commander must return only:

```text
mission_status
process_failures
frozen_specialist_verdicts_as_untrusted_evidence
known_mechanical facts
blocked conclusions
owner decision required
```

It must not generate repair routes from invalid verdicts.

---

# 10. Mechanical validation must be independently recomputed

V1 propagated basic metric errors such as incorrect word count and incorrect count of `người ta`.

The Commander must never copy a specialist's mechanical metric into the gate matrix without recomputation.

For deterministic quantities such as:

- word count;
- paragraph count;
- exact substring count;
- hash;
- byte length;
- candidate identity;

use a deterministic tool/script and store the result separately from semantic reviewer output.

A content specialist's number is not mechanical authority.

---

# 11. What remains valid from V1

The following operational artifacts remain useful as evidence:

- anonymized candidate derivatives and their hashes;
- bounded truth packet as a deterministic artifact, subject to its original authority ceiling;
- raw Product A/B outputs;
- raw Truth A/B outputs;
- raw Protocol Auditor output;
- run manifest as a record of declared orchestration intent;
- proof that the Writer was not run.

Their correct purpose is diagnostic:

> V1 demonstrates that anonymization, sibling replication, role labels, and apparent consensus are insufficient to prevent correlated hallucination, role drift, and authority laundering.

They must not be used as validation of the candidate.

---

# 12. Explicitly blocked uses of commit `5de377b`

Do not use `5de377b` to claim any of the following:

- `revised-probe.md` is historically validated;
- `revised-probe.md` clears or nearly clears the product bar;
- Truth A/B concurrence proves factual reliability;
- reviewer independence was established;
- bias correction was validated;
- the candidate's causal engine is historically supported;
- the listed micro-amendments are safe or sufficient;
- canonical pipeline/planning should absorb V1's route recommendations.

Do not pass `owner-decision-packet.md` to a Writer or Brief Planner as an approved route source.

---

# 13. Stop condition

The Planning Commander must now stop.

No automatic `PLANNING_AGENTS_TEAM_V2`, re-review, re-vote, consensus hunt, Writer pass, evidence expansion, architecture change, or canonical integration is authorized by this memo.

The next mission, if any, requires explicit owner authorization and must begin from the corrected V1 status above.

Until then:

`NO_WRITER`
