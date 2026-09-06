# Output Quality Contract v1.3 — Historical Podcast Prose

Status: **ARCHITECTURE FROZEN FOR PILOT / NOT CERTIFIED**  
Construct: `OWNER_PRODUCT_FIT`  
Target: Vietnamese long-form historical podcast prose  
Craft reference family: Fall of Civilizations (`CRAFT_ONLY`, post-vote only)

## 1. Frozen construct

Benchmark V1 measures:

> blind preference of the product owner between two Vietnamese historical-podcast outputs performing the same editorial function, while historical truth is audited independently.

This is not a claim about general-audience preference, objective literary quality, FoC similarity, or AI-judge preference.

The benchmark is the product-side root of the future trace tree:

`output -> observed preference/failure -> failure signature -> later white-box trace -> root cause`

Output diagnosis must never silently become upstream blame.

## 2. Evaluation unit primitive

Every comparison belongs to an explicit evaluation unit:

`historical_topic × editorial_function × granularity × modality × evidence_condition`

Granularity:

- `FUNCTION_CLIP` — same editorial function, frequent iteration signal;
- `SECTION_SENTINEL` — longer flow/accumulation check;
- `EPISODE_SENTINEL` — occasional macro Goodhart check.

Do not define evaluation units by fixed word counts.

Schema: `schemas/eval-unit.schema.json`.

## 3. Independent measurement lanes

The benchmark has four non-compensatory/independent surfaces.

### Lane A — Product preference

Primary optimization signal.

The owner or shadow judge sees only anonymized A/B material for the same evaluation unit. Before any taxonomy, Truth result, or craft reference appears, record:

`A | B | TIE | BOTH_FAIL | UNCERTAIN`

plus:

`LOW | MEDIUM | HIGH` confidence.

The first-pass vote is then frozen.

`BOTH_FAIL` is distinct from `TIE`: it prevents the benchmark from treating "less bad" as a positive target.

Primary preference schema: `schemas/pairwise-preference.schema.json`.

### Lane B — Truth

Historical truth is audited claim by claim against approved historical authority. Truth does not receive FoC references or Product preference.

Truth runs even when Product preference is also being measured. A preferred output can still be blocked from release by a material truth failure.

Truth is never numerically traded against craft.

Schema: `schemas/truth-gate.schema.json`.

### Lane C — Spoken evidence

Spoken claims are constrained by the evidence mode:

- `TEXT_PREDICTION`
- `AUDIO_OBSERVATION`
- `LISTENER_REPORT`

Text can identify risks such as referent ambiguity, syntactic load, concept stacking, or difficult transitions. Text alone cannot certify prosody, listening effort, comprehension, memory, or actual desire to continue.

Schema: `schemas/spoken-observation.schema.json`.

### Lane D — Target gap

FoC or other craft references appear only after primary preference has frozen.

Target-gap analysis is function-matched and descriptive. It must not score stylistic similarity, change the primary vote, or treat FoC as historical authority.

Schema: `schemas/target-gap.schema.json`.

## 4. Post-vote Product diagnostics

Rubric priming is forbidden. Diagnostics happen only after first-pass preference freezes.

The legacy six-dimension score surface (`continue`, `movement`, `specificity`, `connections`, `spoken_comprehension`, `payoff`) is not the primary decision mechanism in Benchmark V1.

Instead, an observable weakness is represented as a failure signature.

Schema: `schemas/failure-signature.schema.json`.

### Failure scope

- `SPAN`
- `MULTI_SPAN`
- `UNIT_GLOBAL`

Macro defects do not need an invented single culprit sentence.

### Minimal Product taxonomy

```text
PRODUCT_DEFECT
├── NARRATIVE_FUNCTION
│   ├── STALLED_PROGRESSION
│   ├── UNMOTIVATED_TRANSITION
│   ├── LOST_ORIENTATION
│   ├── SETUP_WITHOUT_PAYOFF
│   └── PAYOFF_NOT_EARNED
├── EXPOSITION_LOAD
│   ├── CONCEPT_STACK
│   ├── BACKGROUND_DETOUR
│   ├── CAVEAT_STACK
│   └── EXPLANATION_BEFORE_NEED
├── SPOKEN_COMPREHENSION
│   ├── REFERENT_AMBIGUITY
│   ├── SYNTACTIC_OVERLOAD
│   ├── ORAL_AMBIGUITY
│   └── PROSODY_OR_PRONUNCIATION_FAILURE
├── GROUNDING_SPECIFICITY
│   ├── ABSTRACT_WITHOUT_ANCHOR
│   ├── GENERIC_ACTOR_OR_ACTION
│   └── SCENE_WITHOUT_MATERIAL_DETAIL
├── VOICE_STANCE
│   ├── LECTURE_MODE
│   ├── META_EXPLANATION
│   ├── EXCESSIVE_AUTHORITY
│   ├── EXCESSIVE_HEDGING
│   └── TONAL_MISMATCH
└── REDUNDANCY
    ├── PROPOSITION_RESTATEMENT
    ├── CONCEPTUAL_LOOP
    └── REDUNDANT_SUMMARY
```

Canonical taxonomy artifact: `benchmarks/p01/taxonomy.json`.

### Anti-double-counting invariant

One observable failure has exactly one `primary_family`.

Secondary effects belong in `contributes_to` rather than becoming several supposedly independent failures.

If owner preference is clear but the taxonomy cannot explain it, keep the Product preference and mark the diagnostic `UNRESOLVED`. The taxonomy does not have authority to erase a preference it cannot explain.

`root_cause` in a failure signature is always `null` during Phase 1.

## 5. Truth semantics

Truth audit first identifies what kind of claim exists before verifying it.

Claim types include:

- `EXPLICIT`
- `IMPLIED_PREMISE`
- `CAUSAL`
- `DATE_QUANTITY`
- `QUOTATION_PARAPHRASE`
- `RECONSTRUCTION`

Verifiability:

- `VERIFIABLE`
- `PARTLY_VERIFIABLE`
- `NONFACTUAL`

Source relation:

- `SUPPORTS`
- `QUALIFIES`
- `CONFLICTS`
- `ABSENT`

Verdict:

- `SUPPORTED`
- `QUALIFIED`
- `RECONSTRUCTION`
- `UNSUPPORTED`
- `NONFACTUAL`

A rhetorical question is not automatically nonfactual if it carries an implied factual premise. Temporal sequence or association does not prove causality. Exact quotation establishes location, not entailment.

A high-materiality unsupported claim or a material reconstruction narrated as settled fact may be a release blocker.

## 6. Owner preference protocol

The owner workflow is deliberately lightweight:

1. hide system/model/prompt/source identity;
2. randomize A/B position where controls require it;
3. collect first-pass `A/B/TIE/BOTH_FAIL/UNCERTAIN`;
4. collect confidence;
5. freeze preference;
6. only then ask optional free reason and decisive spans;
7. only after that map the reason into the taxonomy, allowing `UNRESOLVED`.

The owner is the gold signal only for the declared construct `OWNER_PRODUCT_FIT`. The owner cannot override Truth.

## 7. LLM judge policy

LLM judges begin in `SHADOW_ONLY` mode.

A shadow judge predicts owner preference but cannot:

- drive optimization;
- overturn owner labels;
- become gold because several models agree;
- receive FoC during the primary vote.

Reliability must be evaluated on unseen owner-labelled evidence using at least:

- owner agreement;
- owner self-consistency reference ceiling;
- position reversal;
- duplicate consistency;
- evidence-span validity;
- confidence-conditioned behavior;
- abstention behavior;
- Vietnamese slice;
- long-context slice;
- topic transfer.

There is no universal agreement threshold in V1. Any tolerance must be pre-registered before the sequestered set is opened.

Schema: `schemas/judge-reliability.schema.json`.

## 8. Dataset roles

### DEV

Anything used to design/tune the benchmark, including all historical P01 material already visible in this repository.

### CALIBRATION

Fresh owner-labelled pairs collected under a frozen protocol. Used to understand owner behavior and tune a shadow judge. Not final out-of-sample evidence.

### SEQUESTERED

Private/restricted fresh-topic evidence not visible while benchmark/judge rules are being tuned.

The public repository may contain only a metadata/hash manifest, never sequestered prose or labels.

Once a sequestered set is opened and used for tuning it becomes calibration history; the next blind claim requires `REFRESHED_SEQUESTERED`.

Public shell: `benchmarks/p01/sequestered-manifest.json`.

The three existing historical P01 owner packets are `PILOT_ONLY_NOT_CALIBRATION_EVIDENCE`.

## 9. Aggregation

Benchmark V1 does not produce:

- one global quality score;
- Elo ranking;
- mandatory Bradley–Terry ranking;
- majority-of-agents gold.

Preserve raw paired outcomes, uncertainty, failure signatures, Truth blockers, spoken evidence, and reliability slices by topic/editorial function/granularity.

## 10. FoC/reference boundary

FoC remains `CRAFT_ONLY_NOT_TRUTH`.

It is absent from the first-pass Product vote and appears only in post-vote function-matched target-gap analysis.

Style similarity must never be a quality score.

## 11. Phase 1 readiness layers

### Structural readiness

Schemas/versioning/blinding/lane boundaries and public/private dataset boundaries are mechanically coherent.

### Human calibration readiness

Pilot protocol is usable; fresh calibration pairs can be collected; tie/both-fail/uncertainty and unresolved diagnostics are representable.

### Benchmark validity

A frozen benchmark/judge configuration is tested on a real private/restricted sequestered set without retroactive threshold tuning.

### Transfer validity

The measurement architecture remains useful on new historical topics and multiple editorial functions/granularities.

`all files exist`, `two AI reviewers agree`, `P01 improved`, or `output looks more like FoC` are not Phase 1 exit criteria.

The strongest state after Iteration 04 is `ARCHITECTURE_FROZEN_READY_FOR_PILOT`, not Phase 1 complete.
