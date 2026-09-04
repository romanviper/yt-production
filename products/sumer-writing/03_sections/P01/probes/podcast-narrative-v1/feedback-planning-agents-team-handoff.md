# P01 Podcast Narrative Probe — Feedback and Handoff to the Planning Agents Team

Status: `PLANNING_AGENTS_TEAM_HANDOFF_READY — NO_WRITER_RUN_AUTHORIZED`

## Owner direction

The single Review Agent loop is no longer sufficient for this experiment.

For this bounded P01 probe, replace the one-reviewer/one-writer loop with a temporary multi-agent operating unit named:

`PLANNING_AGENTS_TEAM_V1`

The team has one Commander. The Commander coordinates a Packet Custodian, two context-separated Product Reviewers, two context-separated Truth Auditors, and a Protocol Auditor; preserves their outputs; and returns a decision packet to the owner. The Commander is not a super-reviewer and may not replace, average, or rewrite specialist verdicts.

The Writer remains outside the Planning Agents Team. The Writer receives nothing until the owner approves a route and an exact bounded brief.

This handoff is limited to the experimental branch and the P01 podcast-narrative probe. It does not authorize a canonical workflow change, system architecture change, evidence expansion, new research, or another Writer pass.

## Branch state at handoff

- branch: `codex/p01-podcast-narrative-probe-v1`
- feedback commit: `9e35ed096b5b9ce3876fd6e167f61380fc3bf9c9`
- latest re-audit synthesis reviewed: `80db5d4653ef667c6a3b369de9ad9d7728a31b49`
- frozen candidate path: `editorial-revision/revised-probe.md`
- frozen candidate blob: `c44a417ad2a92c1d6df9c24042e4a88f9b8f725c`
- verified prose word count excluding title: `860`

The candidate must remain byte-identical during the first Planning Agents Team mission.

## Feedback on the four re-audit commits

Commits `1fd00e1`, `09fbb8c`, `2f8cf70`, and `80db5d4` made important corrections:

- the contaminated `NEAR_BAR`, truth pass, and convergence verdicts were superseded;
- the raw sample remained unchanged;
- Product and Truth artifacts were committed separately;
- the product diagnosis now recognizes fluent exposition as distinct from high-quality narrative history;
- the truth diagnosis now tests relationships, motives, functions, consequences, and sequences rather than accepting attested nouns as proof;
- the synthesis preserves both `FAIL` verdicts, rejects convergence, and stops before another Writer run.

These corrections are substantively useful. Preserve them.

They do not, however, validate that reviewer bias has been removed.

Both review artifacts identify their execution as the current ChatGPT review session and state that an independent model instance is not verifiable. The Product Review received no auditable anonymized candidate artifact or bounded FoC excerpt. The Truth Audit used whole authority files rather than a materialized record-only packet and did not inventory every nontrivial claim. The synthesis acknowledges that clean model isolation is unverified but still declares the protocol complete.

The corrected process verdict is therefore:

`SEPARATED_ARTIFACTS_COMPLETE — REVIEWER_INDEPENDENCE_UNVERIFIED — BIAS_CORRECTION_NOT_VALIDATED`

Treat the two new `FAIL` verdicts as strong, content-supported diagnostic hypotheses. Do not treat them as independent confirmation and do not reverse them merely to appear adversarial.

## Why a team is required

Adding more agents does not by itself improve reliability. A group can reproduce the same anchoring, share the same hallucination, or vote a plausible error into consensus.

The Planning Agents Team exists to enforce five properties that the single-agent loop did not provide:

1. **Context isolation** — each specialist receives only the packet needed for its role.
2. **Authority separation** — product judgment, truth adjudication, and process validation cannot certify one another.
3. **Immutable outputs** — each raw verdict is frozen before another role can inspect it.
4. **Sibling replication** — two context-separated runs test whether each gate verdict is stable rather than the preference of one evaluator.
5. **Owner control** — no synthesis becomes a Writer instruction without explicit owner approval.

## Team topology

```text
Owner direction
      |
      v
Planning Commander
      |
      +----> Packet Custodian ---- content-blind product packet ----> Product Reviewer A
      |                                                        +----> Product Reviewer B
      |
      +----> Packet Custodian ---- record-bounded truth packet -----> Truth Auditor A
                                                               +----> Truth Auditor B
      |
      +---- run evidence + four frozen outputs ----> Protocol Auditor
      |
      v
mechanical gate matrix preserving all verdicts
      |
      v
Owner decision gate
      |
      +---- no approval ----> STOP
      |
      +---- explicit approval ----> separately authorized route/brief-planning mission
```

The two Product Reviewers and two Truth Auditors should run as sibling executions from separate fresh contexts. None may receive another specialist's verdict. Do not call them independent models unless model diversity and isolation are separately proven.

## Role 1 — Planning Commander

The Commander has seen owner feedback and prior verdicts. Its content-review eligibility must therefore be recorded as:

`CONTEXT_CONTAMINATED_FOR_CONTENT_REVIEW`

### Duties

- receive owner direction and this handoff;
- freeze the candidate and the scope;
- commission content-addressed, role-specific input packets from the Packet Custodian;
- launch specialist agents in fresh, non-inherited contexts;
- record orchestrator evidence for each run;
- freeze specialist outputs without rewriting them;
- send manifests and frozen outputs to the Protocol Auditor;
- assemble a mechanical gate matrix only after the Protocol Auditor returns a process-validity verdict;
- return the unchanged verdicts, disagreements, limitations, and bounded options to the owner and stop.

### Prohibitions

The Commander must not:

- write or revise podcast prose;
- act as Product Reviewer or Truth Auditor;
- select evidence or benchmark excerpts based on a desired content outcome;
- tell a specialist the desired verdict;
- provide prior verdicts, owner dissatisfaction, or evaluator hypotheses to a clean specialist;
- convert heuristics such as “carrier + question” into a mandatory story formula;
- resolve specialist disagreement by majority vote;
- soften, upgrade, average, or silently rewrite a frozen verdict;
- choose an owner route or turn a route option into a Writer brief;
- widen evidence authority;
- authorize the Writer.

The Commander may invalidate a run for process failure. It may not invalidate a specialist merely because the result is surprising.

## Role 2 — Packet Custodian

The Packet Custodian performs deterministic preparation, not review. Because it receives this handoff, it is also `CONTEXT_CONTAMINATED_FOR_CONTENT_REVIEW`.

### Duties

- create a title-free candidate derivative and record the exact transformation from the frozen source;
- verify that the Product and Truth candidate bodies are identical;
- create exact allowed-input and denied-input manifests;
- materialize a record-bounded Truth packet by a deterministic, owner-approved selection rule without adding prose or interpretation;
- prepare a proposed bounded FoC excerpt using a content-independent selection rule, exact locators, source/version identity, byte count, and content hash;
- obtain owner approval for the FoC selection rule, excerpt, and frozen Product prompt/rubric before Product review;
- freeze the exact orchestrator-supplied prompts and hash them before any content-review run;
- freeze all packets before any specialist run begins.

### Prohibitions

The Packet Custodian must not:

- evaluate the candidate;
- choose records, rubric terms, or excerpt boundaries in response to this candidate's apparent strengths or weaknesses;
- summarize prior feedback inside a specialist packet;
- add claims, explanations, or repair language;
- broaden authority;
- expose branch, round, revision, or verdict labels to clean reviewers.

If no owner-approved bounded FoC excerpt exists, return:

`BENCHMARK_PACKET_BLOCKED`

The Commander may not silently select one as a substitute for owner approval.

The Truth record-selection rule must be fixed before review and must not depend on a contaminated agent first deciding which claims deserve which records. For this mission, use the complete predeclared authority family enumerated by the frozen `notebook-authority.md`, including its cited Historical Substrate primitives and boundaries, unless the owner approves another deterministic record-ID list. The Custodian copies exact record bytes; it does not summarize or bind them.

The whole `writer-notebook.md` and `notebook-authority.md` may be supplied only if their frozen versions predate the candidate verdicts and contain no prior-review findings. Otherwise materialize and hash exact control sections under an owner-approved rule.

If a neutral product rubric and FoC selection rule were not frozen independently of this candidate and its feedback, return `PRODUCT_RUBRIC_BLOCKED` or `BENCHMARK_PACKET_BLOCKED` rather than deriving an answer key from this handoff.

## Role 3 — Product Quality Reviewers A and B

Reviewer A and Reviewer B are context-separated sibling replications. They receive the exact same frozen packet, use separate no-history executions, do not see one another, and produce separate raw outputs. Agreement tests verdict stability; it does not by itself prove model independence or absence of shared bias.

### Allowed input

Only:

1. a genuinely anonymized candidate artifact with neutral filename and all round/revision labels removed;
2. the approved product brief;
3. the approved benchmark attributes;
4. an exact, bounded FoC craft excerpt with a declared locator, byte count, and blob/content hash;
5. a neutral, pre-frozen review prompt and general product rubric that were not derived from this candidate or the feedback about it.

The anonymized artifact must have its own hash. Reusing the original candidate hash while claiming its title was removed is invalid.

### Excluded input

- this handoff;
- commit `9e35ed0` and every earlier feedback artifact;
- correction and re-audit commits `1fd00e1` through `80db5d4`;
- Writer reports, revision briefs, and round numbers;
- Truth packets, truth findings, and historical authority files;
- the owner's dissatisfaction or expected verdict;
- any unapproved benchmark.

### Required output

Each reviewer must first state the evaluation dimensions it derives from the supplied, pre-frozen product documents, then apply them without access to a prior finding list. Its output must include:

- top-level verdict from the frozen Product enum;
- exact candidate locators supporting the verdict;
- a description of the listening experience in the reviewer's own terms;
- strongest and weakest product properties under the supplied rubric;
- material uncertainties and confidence;
- a clear separation between textual observation and subjective product judgment.

This handoff intentionally does not prescribe a carrier, question, protagonist, scene, stakes pattern, or other expected narrative mechanism. The reviewer must identify what actually drives the candidate, if anything, without treating prior feedback as an answer key.

Listener-behavior claims must be labeled as a single-evaluator prediction unless an actual listener test exists.

Neither Product Quality Reviewer may make or imply a factual-truth verdict.

## Role 4 — Historical Truth Auditors A and B

Auditor A and Auditor B are context-separated sibling replications. They receive the exact same frozen packet, use separate no-history executions, do not see one another or either Product output, and produce separate raw outputs. Agreement tests verdict stability; it does not by itself prove model independence or absence of shared bias.

### Allowed input

Only:

1. the same candidate body under a neutral filename;
2. `writer-notebook.md`;
3. `notebook-authority.md`;
4. a machine-materialized, record-bounded authority packet selected by the frozen deterministic rule;
5. a neutral, pre-frozen truth-audit prompt and schema with no prior finding list or desired verdict.

The record-bounded packet must have its own path and hash. Passing the whole `materials.json` while declaring only a subset “used” is not sufficient isolation.

### Excluded input

- this handoff;
- all Product Review inputs and outputs;
- FoC prose and product benchmark analysis;
- prior truth audits and repair cards;
- Writer self-reports and round identities;
- owner expectations and anticipated findings;
- external archaeology or web research.

### Required method

1. Independently inventory every material claim under the pre-frozen general truth-audit schema before adjudication.
2. Quote each claim span and bind it to an exact record ID, field/locator, and authority wording.
3. Split mixed claims into separately adjudicated components.
4. Apply the pre-frozen epistemic-status enum at claim-component level; missing binding remains missing rather than being repaired through plausibility.
5. Return the top-level verdict from the frozen Truth enum, with material uncertainty and confidence, without repairing the prose.

Each Truth Auditor must derive its own inventory. Do not seed either with the omissions found in earlier audits. The Protocol Auditor may compare inventories after all truth outputs are frozen.

## Role 5 — Protocol Auditor

The Protocol Auditor is the team's process red team. It does not decide whether the prose is good or historically correct. It decides whether the Product and Truth runs are valid evidence and is therefore ineligible for content review.

It receives only after all four specialist outputs are frozen:

- this handoff;
- input manifests and packet hashes;
- orchestrator run evidence;
- the four unedited specialist outputs;
- the frozen candidate hash and a deterministic span/sentence map for mechanical coverage checks;
- prior review artifacts only for contamination comparison.

It must check:

- fresh-context and non-inheritance evidence;
- identity/config/run metadata;
- exact allowed and denied input enforcement;
- true candidate anonymization;
- exact FoC excerpt bounding;
- truth record-packet bounding;
- raw candidate equality across roles;
- output immutability;
- product/truth authority separation;
- required-field, enum, locator, and quoted-span schema conformance;
- A/B inventory and verdict deltas, without deciding which semantic judgment is correct;
- exact text overlap with prior feedback, reported without content adjudication;
- whether every gate-matrix statement is traceable to a frozen specialist or process output.

The Protocol Auditor may mechanically verify that quoted spans exist and report coverage differences. It may not decide whether a missing span is historically important, whether a binding is correct, or whether a reviewer made a category error. A semantic meta-audit would require a separately authorized clean specialist role.

Its verdict is one of:

- `PROCESS_VALID`;
- `PROCESS_VALID_WITH_DECLARED_LIMITATION`;
- `PROCESS_INVALID — RERUN_REQUIRED`;
- `PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`.

Only `PROCESS_VALID` counts as a successful independence-validation gate.

- `PROCESS_VALID` requires fresh run identities plus enforceable access controls or complete platform read/tool logs demonstrating packet compliance.
- `PROCESS_VALID_WITH_DECLARED_LIMITATION` applies when fresh no-history contexts and auditable no-read/tool evidence exist but a shared runtime boundary prevents a stronger claim; outputs remain diagnostics and cannot yield `BIAS_CORRECTION_VALIDATED`.
- self-attestation, denied-input lists without enforcement, or missing access evidence produce `PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`.
- a demonstrated packet, context, candidate, output-custody, or cross-role violation produces `PROCESS_INVALID — RERUN_REQUIRED`.

The Protocol Auditor may request at most one process-only rerun for a technically failed role. The rerun must use the identical frozen packet, prompt, and model/configuration in a fresh context with a new run ID and no verdict-derived feedback. A/B disagreement must not trigger retries to hunt for consensus. A second technical failure returns the mission to the owner.

The Protocol Auditor may not rewrite any specialist verdict.

## Writer boundary

The Writer is not a member of the Planning Agents Team.

The Writer must not receive:

- reviewer deliberations;
- competing verdicts;
- process-audit discussion;
- raw owner frustration;
- benchmark prose as a style template;
- a list of attractive but unsupported replacement stakes.

If the owner later authorizes a route, it begins a separate mission. A newly assigned Brief Planner—not the Commander and not any evaluator from this mission—may draft a compact proposed Writer brief containing only:

- the owner-selected product objective;
- exact truth constraints and disallowed claims;
- the unchanged evidence ceiling;
- output scope and validation requirements.

The owner must then approve the exact brief before it reaches the Writer.

## No-voting and double-gate rule

This team does not use majority voting.

Freeze these semantics in the run manifest before launch:

- Product top-level enum: `PASS`, `NEAR_BAR`, `FAIL`, `BLOCKED`.
- Truth top-level enum: `PASS`, `FAIL`, `BLOCKED`; risk severity is a separate field: `LOW`, `MEDIUM`, or `HIGH`.
- A/B concurrence means an exact match on the top-level verdict. A severity or material-finding mismatch is preserved as a declared delta even when the top-level Truth verdict matches.
- `NEAR_BAR` does not clear the absolute product gate for this mission. It may support a later owner decision to commission revision, but it is not `PASS`.
- Only Product `PASS` clears the Product gate; only Truth `PASS` clears the Truth gate.
- Only `PROCESS_VALID` satisfies `PROTOCOL_PASS`. A declared-limitation result preserves diagnostic value but does not validate reviewer independence.
- `REVIEWER_STABILITY_UNVALIDATED` means an A/B pair differs at top level or has a disagreement that would change a gate or owner route.

For a candidate to advance:

1. Product Reviewers A and B must return the same top-level verdict and both must clear the Product gate.
2. Truth Auditors A and B must return the same top-level verdict and both must clear the Truth gate.
3. Protocol Auditor must validate all four runs.
4. Owner must explicitly approve the next route.

A failure or invalid run at any gate stops advancement. A gate-critical disagreement inside an A/B pair returns `REVIEWER_STABILITY_UNVALIDATED`; it is not resolved by voting or Commander judgment. Disagreement remains visible.

The eligibility expression is:

```text
PROTOCOL_PASS
AND PRODUCT_A_B_CONCUR
AND TRUTH_A_B_CONCUR
AND BOTH_CONTENT_GATES_CLEAR
→ ELIGIBLE_FOR_OWNER_DECISION
```

Eligibility is not authorization to brief or run the Writer.

Pair agreement measures reproducibility for this sample. It must not be described as proof that shared model bias is absent.

## Required run evidence

For every specialist run, the Commander must record outside the specialist's creative context:

- team mission ID;
- Commander ID;
- specialist role and unique task/thread/run ID;
- model and reasoning/configuration, if exposed;
- context lineage and whether history was inherited;
- runtime isolation mode, including the exact `fork_turns` or equivalent setting;
- exact hash of the orchestrator-supplied prompt payload;
- exact allowed-input manifest with paths, blob/content hashes, byte counts, and locators;
- explicit denied-input manifest;
- start and finish timestamps;
- raw transport byte hash and output custodian identity;
- Git blob hash, artifact path, and commit;
- every encoding, newline, or wrapper transformation between raw transport and Git blob;
- tool/capability access available to the specialist;
- actual read/tool-access log where the runtime exposes one;
- any limitation that prevents independent verification.

The prompt hash covers only the exact payload supplied by the orchestrator. Hidden system/developer instructions or other unobservable platform context must be recorded as an execution limitation, not silently treated as part of that hash.

Use a fresh/no-history execution mode such as `fork_turns: none` when available. Prefer embedding the bounded packet directly and denying repository, filesystem, shell, and web access to content reviewers. Agents sharing a filesystem are at most `PROCEDURALLY_ISOLATED` unless access controls or read logs prove a stronger boundary. A role label, separate Markdown file, separate commit, or self-declaration is not proof of a clean context.

If the runtime cannot expose enough evidence to distinguish separate contexts, stop with:

`PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE`

Do not silently fall back to one agent role-playing all reviewers.

## First team mission

Mission ID: `P01-REVIEWER-INDEPENDENCE-VALIDATION-01`

Objective: test whether context-separated sibling evaluations of the frozen candidate produce stable Product and Truth verdicts under an auditable process. Do not claim that agreement alone proves independence or absence of shared bias.

### Required sequence

1. Commander verifies branch tip, freezes blob `c44a417...`, declares itself content-contaminated, and creates the run-evidence ledger.
2. Packet Custodian materializes and hashes:
   - a title-free, neutral candidate for Product Review;
   - a proposed exact bounded FoC excerpt, then stops for owner approval of that excerpt;
   - a separate neutral candidate for Truth Audit;
   - an exact record-bounded truth packet selected by the frozen rule.
3. After packet approval, Commander launches Product Reviewers A/B and Truth Auditors A/B as sibling runs in distinct fresh contexts with no inherited conversation. All four runs must be launched before any specialist output is materialized into the shared repository or another specialist context.
4. Hold outputs in orchestrator-managed or access-controlled storage until all four runs finish. If the runtime cannot prevent sibling agents from reading earlier outputs, return `PROCESS_VALID_WITH_DECLARED_LIMITATION` or `PROCESS_BLOCKED — INDEPENDENCE_UNAVAILABLE` according to the available access logs; do not claim full isolation.
5. The Commander or declared output custodian records the raw transport bytes and hash before any Git write. Where Git integration changes newline, encoding, or wrappers, record the transformation and both hashes. Preserve specialist wording byte-for-byte otherwise.
6. Where Git integration is used, preserve each source output hash and provenance; sequential integration commits must not be represented as execution isolation.
7. Commander launches Protocol Auditor in another fresh context.
8. If process is invalid, independence unavailable, or either A/B pair is gate-critically unstable, stop and return the status to the owner.
9. If process is valid, Commander writes a bounded gate matrix that reproduces verdicts without upgrading, averaging, or adding unsupported cross-probe conclusions.
10. Commander returns only gate status, frozen findings, A/B deltas, process evidence, and blockers to the owner. Route generation is outside this mission.
11. Stop. Do not launch Writer.

### Required deliverables

Store the mission artifacts under one new, bounded probe subdirectory:

- `run-manifest.json`
- `candidate-product-anonymized.md`
- `foc-craft-excerpt.md`
- `product-review-a-raw.md`
- `product-review-b-raw.md`
- `candidate-truth-neutral.md`
- `truth-record-packet.json`
- `truth-audit-a-raw.md`
- `truth-audit-b-raw.md`
- `protocol-independence-audit.md`
- `commander-gate-matrix.md`
- `owner-decision-packet.md`

The raw specialist outputs must not be polished by the Commander.

## Handoff access policy

This document is an orchestration and red-team input only.

Allowed to read it:

- owner;
- Planning Commander;
- Packet Custodian;
- Protocol Auditor.

Forbidden from receiving it before their outputs are frozen:

- Product Reviewers A/B;
- Historical Truth Auditors A/B;
- Writer.

This restriction prevents the corrective feedback from becoming the next answer key.

## Final stop

The Planning Agents Team is authorized to plan and execute only the bounded re-audit mission above. It is not authorized to revise the candidate, research new evidence, modify canonical production state, change system architecture, or run the Writer.

Return to the owner after `owner-decision-packet.md` with the raw verdicts, process-validity status, disagreements, limitations, and blockers. Any route generation requires a new owner-authorized Route Planner mission.
