# P01 Podcast Narrative Probe v1 — Review-Agent Feedback After the Four-Commit Loop

Status: `REJECT_CURRENT_POST_REVISION_VERDICTS_AND_REAUDIT`

## Authority and scope

This is direct owner feedback after reviewing the interaction among the Review Agent, Product Editor, Truth Auditor, and Writer across these commits:

1. `dca7a57c7fd26619b96a12c1f9c174215723c8fc` — reset review loop around the absolute product bar;
2. `20c229a83c472bcc820d0be145f1499bbcc8012b` — complete evaluation-loop stages A, B, and C;
3. `2463d2f3e73d68665d6c6bd9ae1fb1c099ddfda8` — authorize the same-draft editorial revision experiment;
4. `2a48bb01c4abb99b82bdb02a0beb6eca0b02b0f5` — execute the revision and post-revision reviews.

This feedback reviews the evaluation process itself. It does not authorize another Writer pass, additional line polishing, canonical integration, architecture work, or wider evidence access.

Preserve every existing artifact as experimental evidence. Do not delete or silently overwrite the rejected reviews.

## Corrected verdict

The four-commit sequence does **not** prove editorial convergence.

The correct process-level verdict is:

`REVIEWER_CONTAMINATION_AND_FALSE_PASS`

The current post-revision conclusions must not control the next decision:

- reject `EDITORIAL_CONVERGENCE_PROVEN_AND_CLEARED_FOR_OWNER_REVIEW` as unsupported;
- reject the post-revision truth verdict `PASS (LOW_RISK, 0 Hard Violations, 0 Epistemic Overreach)`;
- reject `NEAR_BAR` as an unverified product verdict;
- retain `revised-probe.md` only as a raw experimental sample pending a valid re-audit.

The provisional corrected statuses are:

| Target | Corrected status |
|---|---|
| Product quality of `revised-probe.md` | `FAIL — EXPLANATORY, NOT DEMONSTRABLY_NEAR_BAR` |
| Historical integrity of `revised-probe.md` | `FAIL — NEW_UNSUPPORTED_CAUSAL_AND_FUNCTIONAL_CLAIMS` |
| Editorial revision experiment | `INCONCLUSIVE — ROLE_SEPARATION_AND_REVIEW_ORDER_NOT_AUDITABLE` |

## Commit-level assessment

### Commit `dca7a57` — directionally correct reset

The Review Agent correctly acknowledged:

- relative-ranking bias;
- premature promotion of editorial hypotheses into Writer constraints;
- proxy optimization;
- collapse of product editing and truth auditing into one role;
- confusion between fresh sampling and editorial revision;
- the possibility of a material-route blocker.

It also correctly required absolute product status before relative ranking and prohibited Writer Round 5 before a separated evaluation loop.

This was a strong process correction on paper.

### Commit `20c229a` — evaluation contamination and unsupported confidence

The apparent blind-review design had useful elements: candidates were relabeled and reordered, and no candidate received `PASS`.

However, the evaluation is not reliable enough to support route selection without qualification:

1. `blind-product-review.md` added *Hardcore History* as a benchmark even though it was not part of the approved repository benchmark.
2. The Product Editor mixed product judgment with historiographical judgment, including assertions about teleology, invention myths, and historical correctness.
3. It generated unsupported illustrative stakes and scenes—grain theft, 5,000 sheep, 40,000 strangers, a memory crisis, an archaeologist opening a bulla, and an ancient accountant at a temple gate.
4. It called Passage Beta `NEAR_BAR` while also describing it as a high-end educational essay lacking embodied human stakes, atmosphere, and immersive narrative movement.
5. It rewarded Beta primarily for the causal hinge that the separate Truth Auditor identified as historically impermissible.
6. The Truth Auditor introduced external material such as CT radiography and rattling counters that was not in the approved audit packet.
7. The retrospective promoted the hypothesis that an envelope-only slice **cannot** sustain the passage into a settled conclusion. The later owner decision correctly reduced this to an unverified competing hypothesis.

The candidate ordering may have been blind, but Git does not prove evaluator isolation. The product review, truth audit, and retrospective were created in one commit without agent identities, input hashes, or a separately frozen product verdict.

### Commit `2463d2f` — strongest control document, conditional on real owner authorization

This document correctly repaired several problems from `20c229a`:

- restored the FoC-only approved benchmark;
- prohibited auditor-added external facts;
- treated material insufficiency as unverified;
- explicitly prohibited replacement causal stories such as memory crisis or urban pressure causing writing;
- selected same-draft revision instead of another fresh sample;
- separated a positive Product Editor note from a bounded Truth Repair card;
- required product review before truth review;
- required an owner stop after one revision experiment.

The document states that it records owner-requested continuation. Git cannot independently establish that provenance. If the owner did explicitly choose this route, the gate is satisfied; otherwise this file is not a substitute for owner approval.

### Commit `2a48bb0` — Writer noncompliance followed by reviewer confirmation bias

The Writer removed several surface forms of the old errors:

- the table/basket tampering vignette;
- the explicit rhetorical question that made envelopes unnecessary;
- the universal exterior-impression claim;
- the immediate-replacement framing.

But it replaced those errors with a new version of the same causal mechanism. The post-reviewers then rationalized those claims as compliant.

## Hard findings the re-audit must address

### 1. The Writer used the replacement causal story explicitly prohibited by the owner decision

`owner-route-decision-after-evaluation-reset.md` states:

> Do not inject phrases such as “memory crisis”, “urban pressure caused writing”, “temple bureaucracy required writing”, or similar causal explanations merely because they create stakes.

`revised-probe.md` nevertheless claims:

- expanding Uruk cities produced flows of grain, livestock, and labor beyond human oversight;
- people therefore needed a physical means to anchor information outside memory;
- thousands of increasingly complex transactions would soon require clay surfaces to carry more than numbers.

The individual categories may exist somewhere in the approved evidence universe. The causal chain does not follow:

```text
urban expansion
→ biological memory overwhelmed
→ recording device became necessary
→ flat clay would soon advance beyond numbers
```

The post-revision Truth Auditor incorrectly marked this chain `VERIFIED` and `FLAWLESS`.

### 2. The Writer replaced the anti-tampering motive with transaction, integrity, and legitimacy motives

The revision says that when quantities needed to be transferred or preserved intact in transactions, envelopes were used. It says the intact envelope guarantees the integrity of the counter set. It describes cylinder seals as confirming legitimacy, supervisory rights, and communal responsibility.

The approved notebook permits narrower statements:

- envelopes enclose counters;
- closed contents are not directly visible;
- opening destroys the sealed state;
- seal impressions can mark an association with authority, custody, or witnessing.

It does not license a particular transaction, a universal transfer/preservation purpose, guaranteed integrity, legal legitimacy, supervisory rights, or communal accountability.

The Truth Auditor explicitly converted these new claims into “documented custody and transfer,” which is an audit error rather than a repair.

### 3. The Product Editor’s own retelling contradicts its verdict

The post-revision Product Editor paraphrased the passage as:

```text
expanding cities could not track grain, sheep, and labor
→ tokens
→ seal tokens to prevent tampering
→ exterior marks solve destructive inspection
→ people realized the hollow envelope could be skipped
→ flat tablets
→ writing
```

That is the forbidden problem-solution genealogy.

This creates a decisive fork:

- if the paraphrase faithfully captures the listener’s takeaway, the revised passage still fails the truth boundary;
- if it does not faithfully capture the passage, the Product Editor hallucinated a causal story and cannot support the product verdict.

The same review then claimed that the passage contains zero fabrications and dismantles the unilinear ladder. Those statements cannot all be true at once.

### 4. The “blind” Product Editor crossed into truth adjudication

The post-revision Product Editor assigned high historiographical discipline, claimed zero factual fabrication, and declared compliance with coexistence boundaries. Those are Truth Auditor judgments, not product-only observations.

The Product Editor should have reported listener experience only. Its role crossing concealed the later Truth Auditor’s errors instead of creating an adversarial check.

### 5. The Truth Auditor misbound claims to authority

The audit treated the presence of grain, livestock, labor, proto-cuneiform categories, and administrative context as proof that:

- those flows exceeded human memory;
- urban expansion created that pressure;
- this pressure made recording devices necessary;
- envelopes served transfer across transactions;
- seals established supervision and accountability;
- clay would soon progress beyond numbers.

Evidence for a category is not evidence for the causal mechanism attached to that category.

For every nontrivial claim, the re-audit must distinguish:

```text
attested entity or practice
≠ attested motive
≠ attested causal origin
≠ attested consequence
≠ attested historical sequence
```

If the exact relationship cannot be bound to approved authority, it must be marked unsupported or qualified inference rather than inferred from plausibility.

### 6. Review independence and order are not auditable

Commit `2a48bb0` added all of the following at once:

- the Writer revision brief;
- the revised output;
- the Writer’s self-report;
- the post-revision Product Review;
- the post-revision Truth Audit;
- the final comparison and convergence verdict.

There is no immutable commit boundary demonstrating:

```text
raw Writer output frozen
→ independent Product verdict frozen
→ separate Truth Audit
→ synthesis
```

Self-declarations of independence are not execution evidence. The commit lacks agent IDs, model/config identity, context hashes, and a verifiable run sequence.

### 7. A basic metric in the Product Review is wrong

`post-revision-product-review.md` reports approximately 610 words. The prose actually contains 860 whitespace-delimited words, which is also the count recorded in `revision-report.md`.

An error of roughly 250 words in a basic input metric materially weakens the unsupported claims of excellent cadence, runtime, and complete cold evaluation.

### 8. The product did not demonstrate convergence toward the FoC-level target

The revised passage remains a typological explanation:

- approximately 860 prose words;
- 32 sentences, averaging about 26.9 whitespace-delimited words per sentence;
- ten uses of the generic construction “người ta”;
- no documented historical actor;
- no witnessed event;
- no primary voice;
- no sustained provenanced carrier;
- no actual narrative or investigative question.

The passage moves from tokens to envelopes, seals, impressions, tablets, coexistence, and a thesis statement. That is organized exposition. Macro stakes are supplied by unbound causal assertions rather than by evidence-supported historical development.

Calling it `NEAR_BAR` repeats the original reviewer bias: a relatively polished explainer is being mistaken for proximity to a high-quality narrative history podcast.

### 9. The synthesis overclaims what one invalidly reviewed sample can prove

`old-beta-vs-revised-beta-comparison.md` says editorial convergence has been definitively proven.

That conclusion is not supported because:

- the product verdict is not reliable;
- the truth verdict is false;
- reviewer separation is not auditable;
- there was no independent listener test;
- the revision retained or introduced causal overreach;
- a single sample cannot establish general convergence.

At most, the experiment shows that direct revision can remove some explicit phrases while preserving an explanatory structure. It does not show that the workflow has reached, or is reliably approaching, the product target.

## Required Review-Agent correction

Do not send another brief to the Writer.

First create a correction artifact that:

1. acknowledges each contradiction above;
2. marks the current post-revision Product Review, Truth Audit, and convergence synthesis as superseded rather than deleting them;
3. restores the provisional statuses in this feedback;
4. separates observations, subjective judgments, causal hypotheses, and verified authority bindings;
5. records which claimed execution properties are unverified from Git.

## Required re-audit protocol

### Stage 1 — freeze the raw sample

Use the existing `revised-probe.md` byte-for-byte. Do not repair it before evaluation.

Record its blob hash and measured word count.

### Stage 2 — independent product-only review

Run a Product Editor in a separate context with only:

- the anonymized revised passage;
- the approved product brief;
- the repository-approved FoC craft benchmark and bounded reference excerpt.

Do not provide:

- the Writer report;
- the Truth Repair card;
- prior product or truth verdicts;
- round identities;
- evaluator hypotheses;
- *Hardcore History* or another unapproved benchmark;
- historical authority files.

The Product Editor may not certify factual correctness. It must answer the listening questions and return an absolute verdict before comparison with any previous draft.

Treat `NEAR_BAR` as a demanding threshold, not a label for fluent explanatory prose. The evaluator must state concrete evidence that the passage has a persistent carrier, an unfolding historical question, changing human/institutional stakes, and a reason to continue listening.

### Stage 3 — independent truth audit

After the product verdict is committed and frozen, run a different Truth Auditor in a separate context with only:

- the unchanged revised passage;
- `writer-notebook.md`;
- `notebook-authority.md`;
- only the explicitly referenced approved P01 authority records required to verify claims.

Do not provide the Product Editor’s verdict or FoC prose.

For every nontrivial causal, functional, institutional, transaction, or reconstruction claim, require a claim-binding table containing:

- exact draft text;
- claim type;
- exact authority ID and locator;
- authority wording;
- whether the authority supports the entity, relationship, motive, consequence, or sequence actually asserted;
- verdict: supported, qualified inference, unsupported, or prohibited.

No outside archaeological knowledge may repair a missing binding. Missing authority must produce a blocker, not an invented citation.

### Stage 4 — synthesis only after both verdicts are immutable

Use a separate synthesis step after the two review commits exist.

The synthesis may compare verdicts but may not upgrade either one. It must not claim proof from a single sample.

Return the result to the owner with bounded options. Do not launch another Writer automatically.

## Minimum audit metadata

Each stage must record:

- agent/role identity available to the orchestrator;
- model/config if available;
- exact input file list and blob hashes;
- output commit;
- measured word count where applicable;
- confirmation of excluded inputs;
- execution order.

Store these outside the creative Writer context.

## Stop condition

Stop after:

1. committing the correction/supersession artifact;
2. committing a genuinely separated product-only review;
3. committing a genuinely separated truth audit;
4. committing a bounded synthesis for owner review.

Do not modify `revised-probe.md`, generate another revision, widen evidence authority, change architecture, or claim broadcast readiness until the owner reviews the corrected evidence and explicitly chooses the next route.
