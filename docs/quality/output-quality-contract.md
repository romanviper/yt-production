# Output Quality Contract v1.2 — Historical Podcast Prose

Status: **PHASE 1 / CALIBRATION CANDIDATE, NOT CERTIFIED**  
Target: Vietnamese long-form historical podcast prose  
Primary craft reference family: Fall of Civilizations (`CRAFT_ONLY`, never historical authority)

## 1. Measurement philosophy

The benchmark is the product-side root of the future trace tree. It must identify an observable failure before any upstream process log is opened.

It answers three different questions through three independent measurement lanes:

1. **Truth lane:** Is this individual sample historically admissible?
2. **Product lane:** Which anonymized sample works better for the intended podcast product?
3. **Target-gap lane:** After Product preference is frozen, what observable craft differences remain to a function-matched reference?

These questions must not be collapsed into one evaluator record. A reviewer may not use evidence from a later lane to justify an earlier result.

The design adapts established patterns rather than inventing a single custom scoring system:

- HELM: explicit scenario/metric separation, multi-metric measurement, visible coverage gaps.
- MQM: span-grounded hierarchical defect annotation with severity.
- Chatbot Arena / Bradley-Terry: anonymized pairwise preference for open-ended output comparison.
- LitBench: creative-writing judges require calibration against human preference; model agreement is not ground truth.

## 2. Product scenario

The benchmark is scoped to:

- language: Vietnamese;
- medium: spoken-first historical narration;
- product: long-form 60–120 minute history podcast / video essay;
- current pilot: history of writing in the Sumerian / Late Uruk context;
- requirements: historical grounding, one-pass comprehensibility, sustained listener interest, meaningful progression, earned local payoff;
- craft target: FoC-like narrative effectiveness without copying distinctive wording, cadence, motifs, or chapter structure.

A result outside this scenario is not automatically transferable.

---

# Lane A — Truth / scope gate

Lane A evaluates one sample at a time against approved P01 historical authority only.

It receives no FoC craft references, Product preference, target-gap analysis, Writer/Planner/Worker trace, or legacy reviewer verdict used as gold truth.

### `G_TRUTH`

Observable question: Does each factual proposition stay within approved historical authority and its uncertainty boundary?

Relevant defects include unsupported fact, unsupported causal relationship, overstated certainty, hidden factual premise, or reconstruction presented as witnessed fact.

Exact quotation establishes location only; it does not establish semantic entailment.

### `G_COHERENCE`

Observable question: Does the prose contradict itself or require mutually incompatible states to be true?

### `G_SCOPE`

Observable question: Does the passage remain within the requested historical and editorial scope?

### `G_LANGUAGE`

Observable question: Is the Vietnamese intelligible enough to evaluate the intended product?

Gate result:

`PASS | FAIL | UNCERTAIN`

`UNCERTAIN` cannot be silently converted to PASS.

Lane A output conforms to `schemas/truth-gate.schema.json`.

---

# Lane B — Primary Product measurement: anonymized pairwise preference

Lane B is the primary open-ended craft comparison.

It receives only anonymized Sample A and Sample B, the frozen Product criteria, and the Product output schema.

It MUST NOT receive:

- FoC or other craft-reference excerpts;
- Truth reviewer results;
- target-gap records;
- candidate/baseline/new/old labels;
- historical verdicts;
- Planner/Writer/Worker process logs;
- intended winner;
- upstream diagnostic hypotheses.

Allowed result per criterion:

`A | B | TIE | UNCERTAIN`

Each verdict requires exact spans, an observation about the supplied prose, a separate interpretation of likely listener consequence, and uncertainty/counterevidence.

### `continue`

Observable question: After this unit, which sample leaves a more concrete reason to keep listening?

Valid evidence may be unresolved consequence, curiosity, a developing situation, an accumulating pattern, emotional stake, or intellectual pressure. A rhetorical question or cliffhanger is not required.

False proxies include question-mark count, danger by itself, or requiring every paragraph to end unresolved.

### `movement`

Observable question: Which sample produces the more meaningful change in understanding, situation, or inquiry through the supplied text?

Required evidence should identify the relevant before/after states and the textual step that causes the change.

False proxies include event count, verb count, beat count, or the specific token → envelope → tablet sequence.

### `specificity`

Observable question: In which sample do concrete details do more explanatory or narrative work?

A detail is useful when removing it would weaken the listener's ability to understand, imagine, distinguish, or infer something relevant.

False proxies include raw counts of names, dates, measurements, artifact IDs, or sensory adjectives.

### `connections`

Observable question: Which sample supplies the clearer transition between adjacent ideas without requiring the reviewer to invent a bridge?

A connection may be causal, contrastive, spatial, temporal, evidentiary, or conceptual. Historically unsupported causality is handled in Lane A; it is never rewarded as a craft strength.

### `spoken_comprehension`

Observable question: Which sample is easier to follow in one pass under the available medium evidence?

Every judgment declares one medium:

- `TEXT_PREDICTION`
- `AUDIO_OBSERVATION`
- `LISTENER_REPORT`

Text-only judgments are predictions. No universal syllable, clause, or word-count threshold is assumed without calibration.

### `payoff`

Observable question: Which sample earns a more useful local understanding from what it has actually set up and developed?

A local payoff need not resolve the entire episode. A summary is not automatically a payoff; an open question is not automatically a failure.

Lane B output conforms to `schemas/output-quality.schema.json`.

## Lane B diagnostic defect taxonomy

Defects explain observable Product weaknesses but do not replace pairwise preference.

Each annotation requires defect family/subtype, exact span, severity, observation, consequence, and uncertainty.

Severity:

- `MINOR`: noticeable but does not materially disrupt the unit's function;
- `MAJOR`: materially weakens comprehension, progression, or desire to continue;
- `CRITICAL`: makes the Product unit unusable for its intended function. Historical gate breaches remain Lane A findings.

Initial Product taxonomy:

```text
PROGRESSION
  STAGNANT_STATE
  REPETITIVE_STATE
  UNEARNED_PAYOFF

EXPOSITION
  CONCLUSION_BEFORE_EXPERIENCE
  ABSTRACT_THESIS_TRANSITION
  EXPLANATION_CLOSES_QUESTION

CONNECTION
  MISSING_BRIDGE
  REVIEWER_SUPPLIED_BRIDGE

SPOKEN
  PROCESSING_OVERLOAD
  SYNTACTIC_BACKTRACK
  REPETITIVE_PHRASING
```

`essay-like` is a pattern across concrete defects, not a mandatory seventh score and not an automatic veto on exposition.

## Lane B failure signature

A Product failure signature is strictly output-side evidence:

```text
signature_id
sample_or_pair_id
criterion_ids
primary_defect
supporting_defects
exact_spans
severity
observation
uncertainty
```

It MUST NOT contain `suspect_upstream_regions`, `planner_fault`, `writer_fault`, or equivalent root-cause claims.

A separate diagnostic hypothesis may later use white-box process evidence, but it is not benchmark truth.

---

# Lane C — Post-preference target-gap analysis

Lane C starts only after the Lane B Product result has been frozen.

It receives one selected sample/passage and pre-frozen function-matched `CRAFT_ONLY` reference excerpts.

It MUST NOT change, reinterpret, or retroactively justify the frozen Lane B preference.

Target gap is descriptive, not a scalar distance. Do not use `NEAR | MODERATE | FAR` as the primary representation.

A target-gap record requires:

- frozen Product evaluation reference;
- matched craft-reference ID and editorial function;
- exact sample and reference spans;
- observable similarity;
- observable difference;
- specific remaining gap;
- retained strength;
- medium limitation.

No single excerpt establishes a global distance from FoC.

FoC remains `CRAFT_ONLY_NOT_TRUTH`; its historical claims are never P01 truth authority.

Lane C output conforms to `schemas/target-gap.schema.json`.

---

# Reviewer grounding rules

Every verdict preserves the distinction:

- **observation:** what is present or absent in the supplied material;
- **interpretation:** why that may matter to the intended listener/product.

Missing evidence means `UNCERTAIN`, not an inferred PASS.

Product reviewers may not use Worker process logs as proof that an intended feature exists. Process is opened only after an output defect has been observed and only for downstream diagnosis.

# Dataset partitions

### DEV

May be inspected while criteria are designed. Previously discussed P01 samples belong here.

### CALIBRATION

Used to compare judge predictions against real owner/human preference. Expected owner labels remain absent until actually supplied.

### HOLDOUT / transfer sample

Not used to tune criteria and reserved for a fresh transfer check after definitions stabilize.

Because the current sample is stored in a shared repository, its reliability must be described as `FRESH_EXPOSED_NOT_BLIND`, not as a sequestered blind holdout. A sample used to tune the contract can never later be called a holdout.

# Evaluator reliability

Phase 1 evaluates the evaluator as well as the prose.

Required calibration signals include:

- owner/judge pairwise agreement;
- A/B position consistency;
- duplicate/same-text consistency;
- uncertainty rate;
- exact-span validity;
- separation of clearly different versus subtle pairs.

Agent-agent agreement alone is insufficient for Phase 1 closure.

# Completion boundary

A structural verifier may establish that artifacts are internally consistent and ready to dispatch.

It cannot establish aesthetic validity, actual listening quality from text alone, owner alignment, or transfer performance.

Until owner/human calibration and a fresh transfer check are completed, the strongest valid status is `READY_FOR_HUMAN_CALIBRATION`.
