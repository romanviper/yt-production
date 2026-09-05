# P01 diagnosis after the clean Historical Substrate probe

Status: `STOP_ARCHITECTURE_CHANGES_AND_RUN_CONTROLLED_WRITER_EXPERIMENT`

Reference probe commit: `e197386f4da7e79a5bfff7a33407a0136b03d6ef`

## Decision

Do not modify the harness, Historical Substrate schema, Writer instructions, evidence broker, outline contract, prompt budgets, or broad unit-test compatibility before the next experiment.

The clean Historical Substrate probe is a useful negative result. The Writer received the intended canonical context and did not receive old probes, evaluator feedback, competitor prose, raw claim ledgers, or material ledgers as primary inputs. Nevertheless, the prose became an even more compressed explanatory miniature of P01.

The next question is therefore not "how should the architecture be repaired?". The next question is:

> Is the failure caused by information abstraction/scarcity, by the Writer's composition process, or by the model's default behavior even when given richer historical material?

We need evidence that distinguishes those possibilities before changing architecture again.

## What the failed clean probe actually showed

The output followed the available four Historical Substrate primitives almost one-for-one:

1. coexisting clay recording practices;
2. envelope affordance;
3. numerical-tablet affordance;
4. historical change from distributed devices toward more directly visible numerical information.

It then closed the movement and transitioned forward. In effect, the Writer converted the complete bounded model into a 450–650 word miniature section.

This means the previous hypothesis — "if upstream representation becomes sufficiently route-neutral and world-shaped, the Writer will naturally discover a strong telling" — is not yet supported.

Historical Substrate may now be clean enough to stop causing evidence-analysis leakage, while also being too low-resolution to provide enough concrete historical material for the Writer to inhabit a local passage. That is one hypothesis, not yet a conclusion.

## Do not infer the wrong lesson

Do **not** respond to this probe by adding:

- more anti-essay instructions;
- required scenes, protagonists, hooks, tension, sensory detail, reversals, beats, or reveal order;
- more substrate fields merely to make the Writer "narrative";
- more claim records or every approved fact back into the primary packet;
- a pre-authored upstream story plan;
- broad unit-test work unrelated to the experiment.

Any of those changes would destroy the diagnostic value of the next test.

## Working hypotheses for the next experiment

### H1 — abstraction / material scarcity

The Writer can compose good historical narrative when given sufficiently rich source-grounded material, but the four-primitives Historical Substrate projection is too compressed to support local discovery.

Prediction: a clean Writer with richer approved historical material should substantially outperform the current substrate-only Writer even without an explicit composition stage.

### H2 — missing Writer-owned composition

Rich material alone is not enough. The model defaults to enumerating and explaining whatever input it receives unless it first performs a bounded composition step that it owns itself.

Prediction: a clean Writer given the same rich historical material plus an explicit Writer-owned prewriting/composition phase should substantially outperform the rich-material direct-draft Writer.

### H3 — model / objective behavior

Even with rich material and Writer-owned composition freedom, the current Writer objective/model still produces explanatory essay prose.

Prediction: all three clean Writers remain similarly weak. If this happens, stop changing evidence architecture; investigate Writer objective/model selection and nonfiction authorship behavior instead.

## Evaluation target

The experiment is not asking which output contains the most facts or best satisfies a checklist. The owner should judge whether a listener is following historical reality unfolding rather than following an explanation of evidence or a list of concepts.

Primary comparison questions:

- Does the passage feel like a real contiguous part of a larger narrative rather than a miniature completed section?
- Does it remain inside one locally interesting thread long enough for momentum to develop?
- Does meaning emerge from progression rather than from thesis statements and corrective qualifications?
- Can the passage be naturally continued without having already covered the whole P01 movement?
- Is historical truth preserved without turning uncertainty into repeated epistemic commentary?

## Architecture freeze

Until the three-Writer experiment is reviewed by the owner:

```text
NO HARNESS CHANGES
NO HISTORICAL SUBSTRATE SCHEMA CHANGES
NO NEW NARRATIVE RULES
NO BROAD TEST-DRIVEN COMPATIBILITY REWORK
NO NEW WRITER PROBE DERIVED FROM THE FAILED OUTPUT
```

Only experiment-local files and outputs may be added.