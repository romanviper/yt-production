# Observable Learning Architecture — 3-Phase Plan

Status: **PLANNED / NOT IMPLEMENTED**  
Branch: `codex/p01-writer-trace-loop-v2`  
Starting point: round-01 execution at `6ba892646da5090828690928f8a90720b554022f`

## Purpose

The next architecture change is not another Writer prompt iteration. The goal is to turn the production-learning process into a system where output quality is measurable first, execution is then simplified, and only after that are agents modularized into observable white-box units that can be traced backward from a concrete product failure to a bounded root-cause region.

The ordering is intentional:

1. define what a good output is and how failure is observed;
2. reduce the repository/workflow to the smallest learning loop that can exercise that measurement system;
3. modularize agents and add white-box observability around actual failure classes revealed by the first loops.

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

FoC or other competitor material may be used as a craft reference, never as historical authority or a wording/cadence template.

## Measurement rules

A metric or verdict is valid only if it can point to observable output evidence.

Do not accept unsupported scalar judgments such as:

- `narrative quality = 8/10`;
- `movement = good`;
- `Writer followed the plan, therefore the prose works`.

A reviewer observation should instead identify the relevant prose span and explain the observable consequence.

Where possible, represent quality as a vector rather than a single score. Example:

```text
truth             PASS
movement          GOOD
continue          GOOD
listenability     WEAK
essay_tendency     FAIL
payoff             GOOD
```

The benchmark must preserve uncertainty. `UNCERTAIN` is preferable to false precision.

## Failure signatures

Each evaluated output should produce a compact **failure signature** that can become the entry point for upstream tracing.

Example:

```text
FAILURE SIGNATURE E03
truth              PASS
movement           PASS
listenability      WEAK
essay_tendency     FAIL
primary symptom    interpretation precedes experience
secondary symptom  paragraphs close arguments too completely
```

Repeated signatures across rounds are evidence that the architecture may be optimizing the wrong proxy even when local scores improve.

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

- a known weak/essay-like P01 sample;
- the current baseline;
- round-01 candidate;
- one or more approved craft-reference excerpts where applicable.

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
6. a human can look at a failure signature and identify which upstream branch should be inspected first;
7. no white-box agent trace is required to judge product quality.

Until these conditions are met, do not begin architecture expansion.

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

At this phase, this layout only needs enough metadata to reproduce inputs/outputs and benchmark results. Full white-box tracing belongs to Phase 3.

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

# Phase 3 — Modularize agents, add white-box observability, and begin learning loops

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
5. make the smallest architecture or contract change that targets that region;
6. run the next frozen comparison;
7. record whether the failure signature moved, disappeared, or merely changed proxy scores.

Avoid broad harness rewrites after every bad sample. The architecture should make narrow, attributable experiments possible.

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

Start Phase 1 by designing and calibrating the Output Quality Contract against frozen existing samples. Only after that contract is stable enough to produce useful failure signatures should the repo be simplified for the first new learning loop.
