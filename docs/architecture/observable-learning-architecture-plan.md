# Observable Learning Architecture — 3-Phase Plan

Status: **PLANNED / NOT IMPLEMENTED**  
Branch: `codex/p01-writer-trace-loop-v2`  
Starting point: round-01 execution at `6ba892646da5090828690928f8a90720b554022f`

Design amendment: **2026-09-06, owner-requested; implementation not started**.
This revision expands the plan introduced at `3eec7ed8615bc74023f4313406775bade8601c47`.
It does not approve a benchmark, certify an evaluator, or authorize production
content changes. The detailed Phase 1 work order below is the next executable
design scope; Phase 2 and Phase 3 remain checkpoint-gated.

## Purpose

The next architecture change is not another Writer prompt iteration. The goal is to turn the production-learning process into a system where output quality is measurable first, execution is then simplified, and only after that are agents modularized into observable white-box units that can be traced backward from a concrete product failure to a bounded root-cause region.

The ordering is intentional:

1. define what a good output is and how failure is observed;
2. reduce the repository/workflow to the smallest learning loop that can exercise that measurement system;
3. modularize agents and expand observability around actual failure classes revealed by the first loops.

Minimal decision records begin in Phase 1, not Phase 3. They record consequential
choices and declared reasons, not private chain-of-thought. Otherwise the first
learning trials would still require reviewers to guess what Workers did.

Do not reverse this order. Observability without a stable output standard only creates more telemetry around an undefined target.

---

# Phase 1 — Build the output benchmark and measurement contract

## Goal

Create the stable root of the future trace tree: a product-level benchmark that can determine *what failed in the output* before the system attempts to determine *where upstream it failed*.

The benchmark must evaluate the output itself, not agent intent, planning quality, or self-reported execution quality.

## Core artifact

Create a versioned **Output Quality Contract** for the historical podcast product.

It should separate three layers:

### A. Absolute gates

Failures that invalidate the sample regardless of craft quality, such as:

- historical support and qualification;
- internal coherence;
- scope compliance;
- intelligible Vietnamese;
- no unsupported causal or motivational claims.

### B. Product-quality dimensions

Dimensions that describe whether the prose actually works as spoken narrative, initially including at least:

- continue / desire to keep listening;
- movement / meaningful change in listener understanding;
- specificity / concrete details doing narrative work;
- connections / transitions that exist in the prose rather than in reviewer imagination;
- listenability / spoken cadence and one-pass comprehension;
- payoff / earned local understanding;
- essay-or-lecture tendency / interpretation arriving before experience.

The final set may change during benchmark construction, but every retained dimension must be observable in the output.

### C. Target gap

A sample may improve over the current baseline and still remain far from the desired product.

The benchmark therefore records both:

- relative result against baseline;
- remaining gap against the intended craft target.

Actual FoC material is the required primary craft reference for this owner-directed
experiment, never historical authority or a wording/cadence template. Other
competitors are supplementary only; they cannot silently replace the target.

## Measurement rules

A metric or verdict is valid only if it can point to observable output evidence.

Do not accept unsupported scalar judgments such as:

- `narrative quality = 8/10`;
- `movement = good`;
- `Writer followed the plan, therefore the prose works`.

A reviewer observation should instead identify the relevant prose span and explain the observable consequence.

Where possible, represent quality as a vector rather than a single score. Example:

```text
truth             NO_UNRESOLVED_DEFECT_IN_COMPLETED_AUDIT
movement          BETTER        [before/after spans required]
continue          SAME          [support required]
listenability     UNCERTAIN     [text prediction only]
payoff             WORSE         [support required]
target_gap        STILL_PRESENT [reference comparison required]
```

The benchmark must preserve uncertainty. `UNCERTAIN` is preferable to false precision.

## Failure signatures

Each evaluated output should produce a compact **failure signature** that can become the entry point for upstream tracing.

Example:

```text
FAILURE SIGNATURE E03
truth              NO_UNRESOLVED_DEFECT_IN_COMPLETED_AUDIT
movement           BETTER
listenability      UNCERTAIN
diagnostic_pattern interpretation precedes experience
primary symptom    interpretation precedes experience
secondary symptom  paragraphs close arguments too completely
```

Repeated signatures warrant investigation of the intervention, material ceiling,
measurement and architecture. They do not by themselves identify which is wrong.

## Ownership map

Create an initial diagnostic map from output failure classes to likely upstream regions. This map does not prove root cause; it only determines the first branch to inspect.

Example:

| Output failure | Initial suspects |
| --- | --- |
| unsupported fact | Evidence / Planner / Writer / Truth gate |
| weak movement | Narrative planning / Writer realization |
| essay tendency | Narrative planning / Writer realization |
| weak spoken cadence | Writer realization / later spoken-polish module |
| weak payoff | Narrative planning / section architecture |
| invented causality | Planning / Writer / Truth gate |

## Benchmark calibration

Before Phase 1 is complete, run the benchmark against a small frozen set containing at least:

- an earlier P01 sample historically judged weak/essay-like, with that judgment withheld and re-tested;
- the current baseline;
- round-01 candidate;
- the function-matched FoC excerpts required by the detailed corpus specification below.

The purpose is not to rank everything perfectly. It is to test whether the measurement contract distinguishes the failures humans actually care about and whether different reviewers can ground judgments in inspectable spans.

## Deliverables

Expected Phase 1 artifacts:

```text
docs/quality/output-quality-contract.md
schemas/output-quality.schema.json
benchmarks/p01/benchmark-set.json
benchmarks/p01/evaluations/
```

Exact paths may change during implementation; the conceptual separation should not.

## Phase 1 exit criteria

Phase 1 is complete only when:

1. every retained quality dimension has a clear observable definition;
2. reviewer outputs require evidence spans and reasons;
3. absolute truth/coherence gates are separate from craft dimensions;
4. relative improvement is separate from target-gap assessment;
5. the frozen calibration set produces useful failure signatures rather than only scalar scores;
6. the signature separates the observed defect from an explicitly tentative upstream inspection route;
7. no white-box agent trace is required to judge product quality.

Until these conditions are met, do not begin architecture expansion.

The executable specification and stricter acceptance conditions immediately below
govern Phase 1. The example vectors above require their linked observations; labels
alone are not a scoring scale or sufficient exit evidence.

## Phase 1 detailed work order — establish a shared frame of reference

### 1. Scope and first checkpoint

Implement the measurement contract beside the current architecture. Do not build
a replacement runtime, new agent hierarchy, production router or generic trace
framework in this phase. Adapt only what prevents a bounded measurement trial;
record such a limitation with a failing example before proposing an adapter.

Use existing outputs as immutable samples, not as already-proven good/bad labels.
Prior reviewer findings, including this plan author's findings, are hypotheses
unless supported by the new comparison. A JSON handoff shows an output exists;
it does not show which decisions produced it or whether those decisions worked.

Initial checkpoint: deliver a benchmark specification, source manifest, trial
protocol and minimal decision-record schema. Validate source locators and field
semantics before dispatch. Do not spend this checkpoint writing new prose or
redesigning modules. Internal design decisions remain delegated; human input
is required for product ambiguity, evidence expansion and the listener-alignment
check below, not for approving every schema field.

### 2. Benchmark architecture: target, observations, decisions

Separate three artifacts with stable IDs:

1. **Product target:** Vietnamese history podcast about writing; preserve the
   approved topic, audience and 60–120 minute product direction. FoC is a craft
   target, not permission to turn this into a general civilization history.
2. **Measurement contract:** operational criteria, function-matched references,
   scope/medium limits, anchored observations and explicit uncertainty.
3. **Improvement contract:** one bounded change, its predicted observable effect,
   invariants and precommitted acceptance rule for a particular trial.

Criterion IDs link the target to feedback and decisions; they do NOT map one-to-one
to agents. A quality dimension is not a module specification. Let benchmark
failures guide investigation; create module boundaries only when ownership and
controlled trials justify them. Do not make the repository hierarchy a copy of
the rubric or a particular FoC episode's chapter order.

### 3. FoC reference corpus and provenance

Build a small, deliberate corpus first: initially 6–10 excerpts spanning at least
two FoC episodes, covering opening/investigation, mechanism explanation, changes
of scale, uncertainty, transitions and payoff. One excerpt may cover multiple
functions. This is a sampling requirement, not a claim of statistical adequacy.
Mark uncovered functions instead of filling them with agent-authored imitations.

Each reference entry must contain:

- stable ID, episode/title and original source locator;
- repository blob/content hash, exact excerpt boundaries and adjacent context;
- editorial function, relationship to the episode arc and reason for inclusion;
- medium: transcript-only or audio-verified; verified audio start/end timestamps
  and original episode link when audio has actually been checked;
- original language; any translation separately attributed and checked against
  the original, never substituted silently or treated as a new FoC original;
- observed craft features, limitations, and suspected transcript errors;
- explicit `CRAFT_ONLY` authority and copyright/provenance handling.

Use existing lawfully available repository scripts first. Do not fabricate
timestamps, assume transcript fidelity or copy an entire external episode merely
to fill the corpus. Missing references become a scoped acquisition request or a
documented coverage limitation. Historical claims in FoC never enlarge Writer's
approved evidence ceiling. The model must not imitate distinctive wording,
cadence or the ruins-opening motif as a mandatory recipe.

For each comparison, freeze the primary matched reference and supplementary
references BEFORE evaluating candidate outcomes. Match narrative function,
context and approximate listening extent. A whole chapter versus a short opening
is not a valid old/new comparison. Do not equate English word counts with
Vietnamese whitespace units, or infer duration without a stated estimate or
actual recording. Record differences in historical material richness; do not
reward invention merely because FoC has access to richer documented events.

### 4. Operational criteria, not shared adjectives

Every criterion definition requires: ID/version; observable question; unit of
assessment; applicability; positive and limiting real examples; common false
proxies; allowed conclusions; and evidence needed to distinguish those conclusions.

| Criterion | Observable question | Required evidence | Invalid shortcut |
| --- | --- | --- | --- |
| Continue | What specific interest remains after this beat? | Opening/next-beat spans and the relation between them | Count questions, danger or cliffhangers |
| Movement | What changes in understanding, situation or inquiry? | Before/after spans and the intermediate step that causes the change in the text | Count events, verbs or plan units |
| Specificity | Which detail does explanatory or narrative work? | Detail plus the inference/experience it enables; counterfactual removal as a hypothesis | Count names, dimensions or sensory adjectives |
| Connections | Is the transition actually supplied? | Both sides of the transition; distinguish textual connection from historically supported causality | Fill the gap using reviewer knowledge |
| Listenability | What can be followed on one hearing? | Exact overload/repetition sites; actual listener observations separately from text predictions | Declare musicality from punctuation |
| Payoff | What understanding is earned at the end? | Setup, development and local resolution; episode payoff assessed separately | Treat every summary as failure or teaser as success |

Essay/lecture tendency is initially a diagnostic pattern across these dimensions,
not a seventh automatic veto. Interpretation before experience is a testable
symptom in context, not a universal defect. FoC itself includes effective
exposition. A passage need not contain a named protagonist, incident or mystery
to work. Avoid counting the same observed weakness repeatedly as independent
failures. Never require a local segment to resolve an entire episode's promise.

Truth/scope/coherence gates are separate from craft. An unsupported factual
claim or contradiction is a blocker; stylistic preference is not. Distinguish
critical incomprehensibility from an ordinary spoken-prose weakness. Every gate
requires a location, rule and evidence; an empty/missing review is INCONCLUSIVE,
not PASS. Exact quotes establish location, not semantic entailment.

### 5. Evaluation output and common vocabulary

For each applicable dimension, require:

```text
criterion_id + contract_version
sample_hash + stable span locator + exact quotation
observation (what is present/absent in the supplied text)
interpretation (why that may affect the listener; mark as inference)
matched_reference_id + reference span + relevant similarity/difference
relative_result: BETTER | SAME | WORSE | UNCERTAIN
target_gap: specific remaining difference, not a scalar distance
medium: TEXT_PREDICTION | AUDIO_OBSERVATION | LISTENER_REPORT
counterevidence + confidence limitation
```

NOT_APPLICABLE needs an explicit predeclared scope reason; it cannot rescue a
failed dimension after evaluation. Missing evidence means UNCERTAIN. Do not let
confidence ratings replace argument quality. Actual listening reports record
participant/context and observed responses, not imaginary listener states.

Failure signatures contain symptom IDs, exact spans, criterion versions,
severity, uncertainty and links to underlying reviews. Root-cause labels live in
a separate diagnostic record. No signature may assert Writer fault simply
because the prose failed while a plan was labelled COHERENT.

### 6. Benchmark trials: relevance before agreement

Use the following staged protocol, with artifacts and allocation frozen before
reviewers see outputs:

**A — Development.** Include existing baseline, the v2 round-01 candidate,
earlier contested samples and genuine FoC references. Remove version labels,
prior verdicts and descriptive titles that reveal preferred answers. If a sample
was previously called weak, keep that historical judgment outside reviewer input.
Use developmental examples to clarify definitions, not to certify evaluators.

**B — Shared-understanding test.** Give Review and Planning the same criterion,
reference and observed defect independently. Ask each to state what observable
change would count as resolving it, what would NOT count, and what must remain
unchanged. Compare these interpretations BEFORE Writer runs. Exact wording need
not match; consequential disagreement about scope, success or constraints means
the improvement contract is not ready. Resolve by referring to examples and the
product goal, not by forcing one agent to repeat another's terminology.

**C — Measurement test.** Use two fresh Product contexts with counterbalanced
old/new order and no plan, rationale, Writer report or intended winner. Keep raw
responses. Score each review against textual support, not just mutual agreement.
Include a duplicate/same-text control: a claimed meaningful difference needs
investigation. An order reversal that changes preference is inconclusive evidence,
not an invitation to add voters. List actual tested comparisons and counts; do
not make population-level accuracy claims from a tiny set.

**D — Human relevance check.** Obtain brief owner/target-listener reactions to a
small anonymized subset spanning clearly different and borderline samples:
where attention drops, what changed in understanding, what was retained and why
continue. Preserve disagreement rather than invent a consensus gold answer.
Agent agreement alone cannot establish relevance. If humans are unavailable,
mark alignment UNVALIDATED and permit only exploratory trials, not Phase 1 closure.
Do not ask the owner to adjudicate technical schemas or every internal round.

**E — Fresh transfer check.** After definitions stabilize, use at least one
previously unused comparison with a contested/subtle difference, not only obvious
lecture versus dramatic story. Preselect it before scoring. A pool hidden only
by filename in a shared repo is not held out. Record who controlled access and
what each reviewer could read. Without enforced separation, call it a fresh
exposed sample, not a blind holdout, and retain that reliability limitation.
Examples used to tune the rubric become development data thereafter.

No zero-tolerance claim of aesthetic accuracy. Zero tolerance applies to leaking
answer labels, fabricating quotes/logs, silently changing inputs and falsely
reporting completed tests. Reviewer reliability remains scoped to observed tasks.

### 7. Minimal decision records: begin before new prose

Record consequential decisions at outline, section planning and draft boundaries.
Do not rerun all these phases solely to populate a trace. Historical missing
records stay UNKNOWN; retrospective reconstructions must be labelled as such
and cannot count as contemporaneous execution evidence.

Each new decision record contains:

```text
decision_id; module/run/version; recorded_at; lifecycle: PROPOSED | APPLIED | REVISED
input_artifact_hashes; inherited_decision_ids; criterion_ids
choice (the concrete selected treatment)
basis (instruction/evidence/constraint IDs and locators)
declared_reason (concise explanation, not private chain-of-thought)
intended_listener_effect (prediction, not observed success)
alternative_and_tradeoff (material option, or NONE with reason; no invented list)
planned_output_unit_ids
applied_output_hash_and_spans (filled after generation)
deviation: NONE | MODIFIED | OMITTED | NEW; deviation_reason
uncertainties; supersedes (old decision retained)
```

Plan choices are frozen before Writer dispatch. Writer logs material departures
when delivering prose, before Product feedback. Any later explanation is marked
RETROSPECTIVE, not backdated. Runtime captures actual input/output identities and
timestamps where possible; agent-authored rationale remains an assertion to
cross-check against artifacts. Recording it does not prove hidden mental causality.
No unrestricted reasoning dumps are requested or needed.

Outline owns macro promise/order/payoff; section planning owns local structure
within it; Writer owns prose realization and declares meaningful deviations.
They cannot silently rewrite upstream decisions. Invalid constraints return a
bounded conflict report rather than being repaired in another module unnoticed.
Do not require a decision record for every adjective; record choices that change
scope, evidence use, reveal order, narrative treatment, causal explanation or payoff.

### 8. Feedback is itself a falsifiable intervention

After black-box evaluation closes, diagnostic review can inspect decision records.
An improvement contract must link:

```text
feedback_id -> criterion/version -> observed defect and baseline span
-> relevant recorded decision(s), or UNKNOWN
-> proposed intervention and responsible module
-> predicted observable effect and matched FoC function
-> falsification condition and dimensions that must not regress
-> frozen comparison method, allowed attempts and stop rule
```

Review and Planning confirm shared interpretation through test B. Planning may
challenge a diagnosis with evidence. This handshake is not another prose review
or a demand for owner approval. Product evaluators do not see the intervention's
intended winner or Writer rationale; the decision layer checks precommitted targets
only after independent judgments are saved.

Distinguish OUTCOME_DEFECT_OBSERVED, FIRST_APPEARANCE_LOCATED,
CAUSE_SUSPECTED and INTERVENTION_SUPPORTED. A coherent plan plus poor prose does
not prove Writer fault. To test attribution, freeze the plan and change one
realization treatment, or freeze the Writer contract and change one planning
decision. Stochastic variation and other confounds remain explicit. These trials
support bounded causal hypotheses, not universal claims about a model.

If the Worker applies the requested change and its predicted benefit does not
appear, record evidence against the feedback hypothesis. Do not automatically
blame compliance or move the goalposts. New noncritical defects go to the next
contract; new critical truth defects still block retention. Successful compliance
and successful product improvement are separate fields.

### 9. First learning trial on the current architecture

Once A–C produce a usable provisional contract, run ONE bounded script treatment
using the current runtime, or a minimal logged manual adapter if a demonstrated
runtime limitation prevents the measurement. This is an exploratory Phase 1 trial,
not round-02 on the unchanged v2 decision logic and not a Phase 3 prerequisite.
Use new versioned inputs/run IDs; do not alter frozen historical runs.

Freeze one primary improvement target, other dimension guardrails, exact baseline
extent, evidence ceiling, model/config, references and acceptance rule. Limit to
one candidate per intervention; do not keep rerolling for a desired verdict.
An infrastructure retry preserves both attempts and records the technical reason.

Default conservative retention: no unresolved hard-gate defects; both independent
reviewers prefer the candidate on the primary dimension; neither identifies a
material regression; target-gap arguments are evidenced; process identity and
review custody are established. Ties, order instability or material disagreement
mean NO_DEMONSTRATED_GAIN or INCONCLUSIVE, not averaged success. Any alternative
rule must be justified and frozen BEFORE the trial, not negotiated after results.

Retained means PROVISIONAL_SCRIPT_IMPROVEMENT only. Audio comparisons use the same
voice/treatment for old/new, actual duration and reported production/language
confounds against FoC. Human listening evidence is a distinct gate. Do not claim
FoC-equivalent podcast quality from a short text trial. Two consecutive trials
without demonstrated gain stop the tactic: inspect hypothesis, material and
measurement before adding agents or changing architecture.

### 10. Worker deliverables and acceptance evidence

Phase 1 owns only its versioned contract, benchmark manifests/excerpts or locators,
schemas, measurement trials, decision records and short handoff. It does not own
production approvals or permission to expand historical authority. Final paths
must be declared before writes; the illustrative paths above are not router artifacts.

Required handoff:

1. Output contract with criterion examples/counterexamples, scope and medium limits.
2. Provenanced FoC manifest and coverage matrix; missing audio/source coverage explicit.
3. Development/fresh-sample allocation, sealed-input evidence or declared limitations.
4. Raw reviews, same-text/order checks, human relevance observations and disagreements.
5. Shared-understanding comparison and a frozen improvement contract.
6. Minimal decision schema and one new trial's contemporaneous records.
7. Result: compliance, product change, remaining target gap and feedback hypothesis outcome.
8. Trace drill: start at one exact defect, recover criterion, actual inputs, related
   decisions, first visible introduction and review handling; list every broken edge.

Measure the trace drill's elapsed inspection time, number of artifact opens and
unresolved links. Compare with a historical case, noting unequal case difficulty.
Set a local cost budget before the drill; do not assert tracing became cheap from
file counts alone. Initially retrieve a bounded case bundle, not the whole history.

Phase 1 can close only with evidence that the contract was applied consistently,
is meaningfully anchored to FoC and human product reactions, supports a shared
intervention, and exposes uncertainty rather than hiding it. It need not produce
a winning draft: an honestly falsified intervention is useful learning. Unresolved
reliability or runtime limitations must be named with an owner and next check;
they cannot be masked by completed files. Audio-incomplete work closes at most
a SCRIPT_CONTRACT checkpoint, never the full PODCAST_CONTRACT checkpoint.

### 11. Benchmark change control

Freeze contract/reference/schema hashes per trial. Criterion IDs retain their
meaning within a version. Changes require reason, affected dimensions/runs and
version migration notes. Corrections to leaked or invalid tests are mandatory,
but old results remain labelled INVALIDATED, not rewritten as new successes.

Benchmark changes and Writer interventions are separate experiments. If a metric
changes, re-evaluate old/new under the same revised contract; never compare scores
across versions as learning progress. A maintained public development set is not
a permanent certification exam. The benchmark itself is revisable through new
source/listener evidence, not through discomfort with a failed candidate.

---

# Phase 2 — Reduce the repository to the smallest first-learning loop

## Goal

Remove or isolate accumulated workflow complexity so the next experiments run through one understandable path. Phase 2 is a simplification phase, not an observability-expansion phase.

The repository currently contains production routing, task/approval mechanics, rework/replay conventions, branch-specific experiment exceptions, several packet formats, and multiple generations of experimental orchestration. These should not all become dependencies of the new learning architecture.

## Principle

Build the new learning loop beside historical artifacts rather than rewriting or deleting evidence from earlier experiments.

Historical runs remain immutable references. New runtime code should not need to understand v1/v2 internals except through explicit adapters if required.

## Minimal first-learning loop

Reduce the active experiment to four responsibilities:

```text
MISSION
  |
  +-- CONSTRUCT
  |     +-- PLAN
  |     +-- WRITE
  |
  +-- EVALUATE
        +-- TRUTH
        +-- PRODUCT
```

For the first simplified loop:

- no Commander agent is required as a creative role;
- no certification layer;
- no voting expansion;
- no repeated rerolls;
- no new specialist agents unless the benchmark demonstrates a failure class that cannot be isolated with the four responsibilities above;
- orchestration code should remain content-agnostic where practical.

## Cleanup work

Phase 2 should inventory current workflow pieces and classify them as:

- **KEEP** — required for the minimal loop;
- **ADAPT** — useful concept, but should be expressed through a simpler interface;
- **ARCHIVE / LEGACY** — historical experiment only;
- **DELETE LATER** — dead duplication, but only after provenance/history is safe.

Do not perform destructive cleanup merely to make the tree look tidy. The goal is to make the *active execution path* small and unambiguous.

## Single run layout

Introduce one predictable run layout for the simplified loop, for example:

```text
runs/<run-id>/
  manifest.json
  inputs/
  plan/
  write/
  truth/
  product/
  decision.json
```

At this phase, preserve Phase 1's minimal decision records and feedback links as
well as input/output identity. Full tracing infrastructure belongs to Phase 3;
do not simplify away the information needed to test a feedback hypothesis.

Before migrating, replay saved evaluator artifacts through old and proposed
decision paths. Investigate every status difference; do not regenerate prose to
hide incompatibility. Remove active duplicate verdict sources, not historical
evidence. A module ownership table must name allowed decisions, writable outputs,
handoff guarantees and conflict behavior. Keep this migration separately reviewed
from changes to benchmark semantics or creative content.

## Decision semantics

The decision layer must consume real evaluator artifacts mechanically. Avoid the round-01 v2 regression where the decision path could produce a status without actually deriving it from Product results.

At minimum, the simplified loop must enforce:

- exact candidate identity;
- evaluator packet identity;
- truth result;
- product result;
- explicit candidate/baseline labels;
- benchmark failure signature;
- process incompleteness as `INCONCLUSIVE`, not implicit success/failure.

## Tests

Tests for the simplified architecture should focus first on invariants rather than quantity:

- decision outcomes actually change when evaluator verdicts change;
- A/B reversal maps correctly to the candidate;
- unsupported truth claims block the appropriate result;
- missing artifacts cannot silently pass;
- old experimental artifacts are not mutated;
- the benchmark contract is the sole product-quality entry point.

## Phase 2 deliverables

Expected artifacts include:

```text
docs/architecture/minimal-learning-loop.md
<small learning runtime>
<minimal schemas>
<focused invariant tests>
```

The implementation should be noticeably smaller and easier to explain than the current accumulated experimental harness.

## Phase 2 exit criteria

Phase 2 is complete only when:

1. one command/path can execute or prepare the minimal P01 learning loop;
2. the active architecture can be explained from end to end without referring to legacy experiment-specific exceptions;
3. Product quality is determined only through the Phase 1 benchmark contract;
4. the decision engine is mechanically covered by tests;
5. previous v1/v2 runs remain readable and untouched;
6. adding another P01 learning round does not require adding another experiment-specific orchestration script;
7. no new agent specialization has been introduced merely for conceptual neatness.

---

# Phase 3 — Modularize agents and expand observability around established learning loops

## Goal

Turn the simplified loop into an observable modular agent system incrementally, using actual benchmark failures to decide where module boundaries are needed.

The system should evolve from a small monolith toward modules only when the split improves fault isolation.

## Module contract

Every agent/module must expose a bounded interface similar to an object with a single responsibility:

```text
Module
  Contract
  Inputs
  Execution
  Outputs
  Assertions
  Trace
```

A module should own a small, understandable class of decisions. It should not simultaneously research, plan, write, self-evaluate, and certify itself.

## White-box boundary

White-box observability means recording inspectable execution telemetry, not requesting private chain-of-thought.

Permitted trace material includes:

- input artifact IDs/hashes;
- selected evidence IDs;
- decision records stated in concise inspectable form;
- constraints triggered;
- alternatives explicitly rejected where the module can state them safely as decisions rather than hidden reasoning;
- output spans produced from plan nodes;
- deviations from the input contract;
- warnings and unresolved assumptions;
- assertions and the observations supporting those assertions.

Do not rely on unrestricted reasoning dumps as the observability mechanism.

## Trace direction

Traceability must work both forward and backward.

Forward:

```text
Evidence -> Plan node -> Writer unit -> Output span
```

Backward:

```text
Failed output span -> Writer decision -> Plan node -> Evidence
```

The backward path is the important debugging path.

## Hierarchical trace graph

The runtime may form a tree or DAG; it does not need to be literally binary. Diagnostic traversal, however, should use binary-style fault isolation whenever possible.

Initial shape:

```text
OUTPUT FAILURE
     |
     +-- Construction fault?
     |      +-- Planning?
     |      +-- Realization?
     |
     +-- Evaluation fault?
            +-- Truth?
            +-- Product measurement?
```

Further splits are introduced only when repeated evidence justifies them. For example, Planning may later split into Evidence Selection and Narrative Architecture; Writing may later split into Narrative Realization and Spoken-Language Polish.

## Execution capsule

Each module execution should eventually produce a self-contained capsule such as:

```text
nodes/<node-id>/
  manifest.json
  input.json
  output.*
  trace.jsonl
  assertions.json
  summary.json
```

`manifest.json` should capture stable provenance such as module/version, parent node, model/config, timestamps, and input/output hashes.

## Assertions vs observations

The architecture must distinguish observed facts from agent assertions.

Example:

```text
Observation: 6 planned units have exact mapped prose spans.
Assertion: Writer realization is ALIGNED.
```

An assertion without inspectable observations is weak evidence and should not close a diagnostic branch by itself.

This avoids repeating the v2 pattern where labels such as `COHERENT`, `ALIGNED`, or `PASS` can appear stronger than the underlying evidence.

## Module ownership and invariants

Each module should declare the invariants it is responsible for.

Possible initial examples:

### Narrative planning

- every unit has a meaningful intended listener-state change;
- questions are not merely pre-scripted essay transitions;
- planned payoff is earned from preceding evidence;
- truth boundaries remain explicit.

### Writer realization

- every planned unit maps to observable prose or a declared deviation;
- realization does not silently replace the plan with another structure;
- no unsupported causal bridge is introduced during prose generation.

### Truth evaluation

- every factual proposition resolves to authority, qualified inference, reconstruction, or unresolved status;
- rhetorical framing does not hide unsupported factual premises.

### Product evaluation

- every verdict is grounded in output spans;
- reviewer intent or Writer trace is unavailable during black-box quality judgment.

## Black-box vs white-box evaluation

Preserve a hard separation:

- **Product evaluation is black-box:** prose only, benchmark contract, no plan/trace/self-report.
- **Diagnostic auditing is white-box:** may inspect plan, module traces, evidence binding, execution reports, and provenance.

Product reviewers answer: *does the output work?*  
White-box auditors answer: *where did the failure enter the process?*

## Learning-loop policy

Begin real learning rounds as soon as the first useful module boundaries and trace paths exist; do not wait for a perfect framework.

For every failed or weak output:

1. generate the Phase 1 failure signature;
2. choose the first upstream branch using the ownership map;
3. inspect only the relevant module boundary and trace evidence;
4. classify the suspected fault region;
5. test the smallest editorial/evidence-selection/realization intervention first;
   change architecture or module contracts only when a demonstrated boundary or
   runtime defect prevents that intervention or its evaluation;
6. run the next frozen comparison;
7. record whether the failure signature moved, disappeared, or merely changed proxy scores.

Avoid broad harness rewrites after every bad sample. The architecture should make narrow, attributable experiments possible.

All diagnostic links retain their epistemic type: runtime-observed identity,
agent-declared decision, reviewer interpretation or intervention-supported
hypothesis. Missing edges remain explicit. Trace coverage cannot be used as a
quality score, and one well-mapped run does not establish reproducible model
behavior. A module split requires a before/after fault-isolation drill showing
less uncertainty or inspection cost without degrading benchmark outcomes.

## Progressive modularization rule

Do not split an agent because a cleaner diagram is desirable. Split it when at least one of the following is true:

- one output failure maps to two clearly different internal responsibilities that cannot be isolated;
- one module repeatedly produces useful output but its internal failure location remains ambiguous;
- separate contracts would allow independent evaluation or replacement;
- the split reduces the size of the fault region during real debugging.

This is the primary guard against rebuilding another over-engineered agent team.

## Phase 3 exit direction

Phase 3 is intentionally open-ended. The first milestone is reached when:

1. a benchmark failure can be traced from an exact output span backward through module artifacts to a bounded suspected root-cause region;
2. Planner failure can be distinguished from Writer realization failure without relying on self-report alone;
3. Product evaluator failure can be distinguished from construction failure;
4. module traces are reproducible and provenance-checked;
5. at least several real P01 learning rounds have used the same architecture rather than creating new one-off harnesses;
6. architectural changes become smaller and more attributable over time.

---

# Global constraints across all three phases

## 1. Output quality is the root of the trace

Never start diagnosis from `the agent said it succeeded`. Start from an observable product failure or uncertainty defined by the benchmark.

## 2. No scalar-score optimization loop

Scores may be used for convenience but must not become the primary optimization target. Preserve dimensional verdicts, evidence spans, failure signatures, and target gaps.

## 3. Historical artifacts are immutable

Existing experiment runs are evidence. Do not rewrite them to make the new architecture appear cleaner.

## 4. No premature agent proliferation

The initial simplified loop has four responsibilities: Plan, Write, Truth, Product. Additional modules require observed diagnostic value.

## 5. White-box does not mean unrestricted internal reasoning dumps

Capture observable decisions, evidence, constraints, provenance, mappings, deviations, and assertions. The system should be debuggable without depending on private chain-of-thought.

## 6. Every new layer must reduce uncertainty

A new reviewer, agent, schema, trace field, or runtime abstraction is justified only if it helps answer one of these questions more reliably:

- What exactly failed in the output?
- Which upstream region most likely introduced that failure?
- What observation supports that attribution?
- Did the next change remove the same failure rather than improve an unrelated proxy?

---

# Immediate next action

Do **not** start round-02 on the current v2 harness as the architectural next step.

Start Phase 1 by designing and testing the Output Quality Contract against frozen
existing samples. A bounded learning trial and minimal decision records belong
inside Phase 1; broader runtime simplification waits for its acceptance evidence.

Read the detailed Phase 1 work order as the controlling execution sequence:
benchmark specification and references first, shared-interpretation and measurement
trials next, minimal contemporaneous decision records before new prose, then one
bounded intervention on the current architecture. Do not begin a clean-sheet
platform build. Return the Phase 1 acceptance evidence and actual gaps before
starting Phase 2. This document is a plan, not evidence those checks have passed.
