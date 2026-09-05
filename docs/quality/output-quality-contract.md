# Output Quality Contract v1.1 — Historical Podcast Prose

Status: **PHASE 1 / READY FOR CALIBRATION, NOT CERTIFIED**  
Target: Vietnamese long-form historical podcast prose  
Primary craft reference family: Fall of Civilizations (`CRAFT_ONLY`, never historical authority)

## 1. Measurement philosophy

The benchmark exists to answer two different questions without conflating them:

1. **Does this output work better for the intended product?**
2. **What observable defect is present when it does not?**

It does not answer which upstream agent caused the defect. Root-cause attribution belongs to later diagnostic work.

The design adapts four established evaluation patterns:

- HELM: explicit scenario/metric separation, multi-metric measurement, visible coverage gaps.
- MQM: span-grounded hierarchical defect annotation with severity.
- Chatbot Arena / Bradley-Terry: anonymized pairwise preference for open-ended output comparison.
- LitBench: creative-writing judges must be calibrated against human preference; model agreement is not ground truth.

## 2. Product scenario

The benchmark is scoped to:

- language: Vietnamese;
- medium: spoken-first historical narration;
- product: long-form 60–120 minute history podcast / video essay;
- current pilot: history of writing in the Sumerian / Late Uruk context;
- requirements: historical grounding, one-pass comprehensibility, sustained listener interest, meaningful progression, earned local payoff;
- craft target: FoC-like narrative effectiveness without copying distinctive wording, cadence, motifs, or chapter structure.

A benchmark result outside this scenario is not automatically transferable.

## 3. Layer A — Absolute gates

Hard gates are not style scores. A failed gate blocks a production-quality claim even if the prose is compelling.

### `G_TRUTH`

Observable question: Does each factual proposition stay within approved historical authority and its uncertainty boundary?

Defects include unsupported fact, unsupported causal relationship, overstated certainty, hidden factual premise, or reconstruction stated as witnessed fact.

Exact quotation establishes location only; it does not establish entailment.

### `G_COHERENCE`

Observable question: Does the prose contradict itself or require mutually incompatible states to be true?

### `G_SCOPE`

Observable question: Does the passage remain within the requested historical and editorial scope?

### `G_LANGUAGE`

Observable question: Is the Vietnamese intelligible and natural enough to evaluate the intended product?

Gate result:

`PASS | FAIL | UNCERTAIN`

`UNCERTAIN` cannot be silently converted to PASS.

## 4. Layer B — Primary craft measurement: anonymized pairwise preference

For old/new comparison, the primary signal is pairwise preference, not an absolute scalar or adjective score.

Allowed result per criterion:

`A | B | TIE | UNCERTAIN`

Each verdict requires exact spans from both samples where applicable, an observation about the text, and a separate interpretation of likely listener consequence.

### `continue`

Observable question: After this unit, which sample leaves a more concrete reason to keep listening?

Valid evidence may be unresolved consequence, curiosity, developing situation, accumulating pattern, emotional stake, or intellectual pressure. A rhetorical question or cliffhanger is not required.

False proxies:

- number of question marks;
- danger or suspense by itself;
- every paragraph ending unresolved.

### `movement`

Observable question: Which sample produces the more meaningful change in understanding, situation, or inquiry through the supplied text?

Required evidence: before span, after span, and the textual step that causes the change.

False proxies:

- number of events or verbs;
- number of beats;
- the specific token -> envelope -> tablet sequence.

### `specificity`

Observable question: In which sample do concrete details do more explanatory or narrative work?

A detail is useful when removing it would weaken the listener's ability to understand, imagine, distinguish, or infer something relevant.

False proxies:

- raw count of names, dates, measurements, artifact IDs, or sensory adjectives.

### `connections`

Observable question: Which sample supplies the clearer transition between adjacent ideas without requiring the reviewer to invent a bridge?

A connection may be causal, contrastive, spatial, temporal, evidentiary, or conceptual. Historically unsupported causality is a truth defect, not a craft strength.

False proxies:

- transition words alone;
- reviewer background knowledge filling a missing step.

### `spoken_comprehension`

Observable question: Which sample is easier to follow in one pass under the available medium evidence?

Every judgment declares one evidence medium:

- `TEXT_PREDICTION`
- `AUDIO_OBSERVATION`
- `LISTENER_REPORT`

Text-only judgments are predictions. No universal syllable, clause, or word-count threshold is assumed without calibration.

### `payoff`

Observable question: Which sample earns a more useful local understanding from what it has actually set up and developed?

A local payoff need not resolve the entire episode. A summary is not automatically a payoff; an open question is not automatically a failure.

## 5. Layer C — Diagnostic defect taxonomy

Defects explain observable weaknesses but do not replace pairwise preference.

Each annotation requires:

- defect family and subtype;
- exact span;
- severity;
- observation;
- product/listener consequence;
- uncertainty/counterevidence when relevant.

Severity:

- `MINOR`: noticeable but does not materially disrupt the unit's function;
- `MAJOR`: materially weakens comprehension, progression, trust, or desire to continue;
- `CRITICAL`: makes the sample unfit for the intended purpose or breaches a hard gate.

Initial taxonomy:

```text
TRUTH
  UNSUPPORTED_FACT
  CAUSAL_OVERREACH
  OVERSTATED_CERTAINTY
  HIDDEN_PREMISE

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

`essay-like` is therefore a pattern across one or more concrete defects, not a mandatory seventh score and not an automatic veto on exposition.

## 6. Failure signature

A failure signature is strictly output-side evidence:

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

A separate diagnostic hypothesis may later point to upstream regions, but that hypothesis is not part of benchmark truth.

## 7. Layer D — Target-gap analysis

Target gap is descriptive, not a scalar distance.

Do not use `NEAR | MODERATE | FAR` as the primary representation.

A target-gap record requires:

- matched craft-reference ID;
- matched editorial function;
- exact candidate span;
- exact reference span;
- observable similarity;
- observable difference;
- specific remaining gap;
- retained strength;
- medium limitation.

No single excerpt establishes a global distance from FoC.

FoC remains `CRAFT_ONLY`; its historical claims are not P01 truth authority.

## 8. Reviewer grounding rules

Every Product verdict must preserve the distinction:

- **observation:** what is present/absent in the supplied text;
- **interpretation:** why that may affect the intended listener.

Required evidence:

- stable sample/pair ID;
- exact quoted span(s);
- criterion ID;
- observation;
- interpretation;
- result and uncertainty;
- evidence medium.

A reviewer may not use plan, Writer report, Worker process log, intended winner, historical verdict, or upstream diagnostic hypothesis.

## 9. Dataset partitions

The benchmark maintains disjoint roles:

### DEV

May be inspected while criteria are designed. Previously discussed P01 samples belong here.

### CALIBRATION

Used to compare judge predictions against real owner/human preference. Expected labels remain absent until supplied by the owner/human.

### HOLDOUT

Not used to tune criteria. It is reserved for a fresh transfer check after definitions stabilize.

A sample used to tune the contract can never later be called a blind holdout.

## 10. Evaluator reliability

Phase 1 evaluates the evaluator as well as the prose.

Required calibration signals include:

- owner/judge pairwise agreement;
- A/B position consistency;
- duplicate/same-text consistency;
- uncertainty rate;
- exact-span validity;
- separation of clearly different versus subtle pairs.

Agent-agent agreement alone is insufficient for Phase 1 closure.

## 11. Completion boundary

A structural verifier may establish that artifacts are internally consistent and ready to dispatch.

It cannot establish:

- aesthetic validity;
- actual listening quality from text alone;
- owner alignment;
- held-out transfer.

Until owner/human calibration and a fresh transfer check are completed, the strongest valid status is `READY_FOR_HUMAN_CALIBRATION`.
