# FoC Editorial Architecture — Probe 1 Diagnosis and Probe 2 Correction Plan

Status: `probe_1_rejected_diagnostic_value_retained`

Recorded: 2026-09-04

Branch: `codex/foc-editorial-architecture`

Probe commit reviewed: `bfb72140624587f6c301d1b12a40568dc0b08802`

Scope: record the result of the first clean Writer probe, identify the remaining upstream failure path, and lock the minimum changes allowed before Probe 2. This document does not itself modify harness behavior, product evidence, outline authority, or prose.

---

# Decision

Probe 1 is rejected as a production-quality narrative sample.

It is retained as a successful diagnostic experiment because it narrows the failure from a broad "Writer keeps producing essays" problem to a specific upstream transmission path:

```text
outline encodes explanatory thesis
        ↓
material records encode interpreted causal operations as if they were direct evidence
        ↓
Writer receives concrete nouns and actions inside an already-decided explanatory model
        ↓
Writer produces historical explanation with concrete texture
        ↓
essay structure survives
```

The architecture has therefore improved one major failure mode but has not yet escaped essay-first composition.

Probe 1 no longer relies on a long invented warehouse scene. That is progress.

However, the replacement output still behaves primarily as:

```text
context
→ problem/thesis
→ evidence examples
→ limitation
→ causal solution
→ conclusion
```

rather than as a historical story whose meaning emerges from following evidence, people, objects, actions, uncertainty, or change.

The next iteration must not add more style rules to Writer before correcting the two upstream contracts below.

---

# Probe 1 outcome against the five agreed gates

## Gate 1 — Am I following something that is happening or changing?

Verdict: `partial_fail`

There is a clear conceptual progression, but the listener mainly follows an explanatory model about why durable records became useful rather than following historical reality or surviving evidence unfolding under uncertainty.

## Gate 2 — Do I want to know what happens next?

Verdict: `weak_fail`

The narrator repeatedly announces the function or meaning of the next material step before the listener has discovered it. This reduces forward curiosity because the prose explains why each device matters as soon as it is introduced.

## Gate 3 — Does meaning emerge, or is it explained?

Verdict: `fail`

Meaning is stated directly and early. The Writer tells the audience what the historical problem was, why face-to-face trust failed, why memory failed, why bullae solved the problem, and what external memory meant.

The prose therefore earns clarity, but not discovery.

## Gate 4 — Can the listener retell the progression?

Verdict: `pass`

The progression is easy to summarize:

```text
large Uruk administration
→ tokens/seals
→ limitations of direct memory and loose counters
→ bullae
→ durable external record
```

This is useful but insufficient. A strong essay is also highly retellable.

Retellability must therefore remain necessary but not sufficient for narrative success.

## Gate 5 — Does evidence/source distance remain honest?

Verdict: `material_concern`

The main concern is not only Writer wording. Some material records themselves encode reconstructed actors, operations, purposes, causal functions, and representative workflows under fields such as `documented_action` or similarly authoritative language.

That makes it difficult for Writer and Reviewer to distinguish:

```text
what survives materially
what a source directly establishes
what scholarship infers from material patterns
what represents a plausible operational reconstruction
what is an explanatory causal interpretation
```

This must be corrected before Probe 2.

---

# Important invalidation: current automated review cannot approve Probe 1

The current `review.md` must not be treated as a valid owner approval signal for Probe 1.

Its evaluation refers to content and progression not present in the current probe draft, including later material steps and concepts beyond the actual excerpt. It is therefore stale or mismatched relative to the current `draft.md`.

Required action before Probe 2 work:

```text
mark Probe 1 review as stale / non-authoritative
```

Do not rewrite the stale review into a passing or failing review yet. Preserve it as provenance showing that task/output binding must be checked.

Any future Reviewer task must bind explicitly to the exact draft SHA or task/output identity it evaluates.

---

# Root cause 1 — `historical_change` is route-neutral in form but thesis-led in semantics

The new outline contract successfully removed scene, carrier, beat order and reveal sequence.

However, P01's actual `historical_change` still contains a causal explanatory model.

Conceptually, it currently says:

```text
small-scale / point-to-point token and seal practices become insufficient
        ↓
durable external sign systems emerge
        ↓
institutions can maintain obligations across time and distance
```

That is not merely a historical state transition.

It already determines:

- the historical problem;
- which previous mechanism was insufficient;
- why the next mechanism emerged;
- what functional outcome it solved;
- the causal meaning of the section.

Writer therefore receives a thesis to execute even without receiving a story plan.

This is the central lesson of Probe 1:

> Removing narrative route is not enough if the remaining movement contract still pre-authors the explanatory argument.

---

# Correction 1 — Redefine `historical_change` as observable/evidentiary state change only

## Required semantic rule

`historical_change` may describe a bounded change visible in the historical record or material/evidentiary configuration.

It must not encode a complete explanation of why that change happened or what human cognitive/social failure it solved unless that causal relation is itself directly within the evidence ceiling and intentionally belongs to the section contract.

Prefer:

```text
observable state A
→ observable state B
```

Avoid:

```text
problem X became insufficient
→ therefore solution Y emerged
→ creating capability Z
```

## P01 target shape

A safer P01 movement should resemble:

```text
FROM
Late-Uruk evidence preserves quantities and authentication across multiple material devices and practices.

TO
Numerical information increasingly appears directly on durable clay surfaces alongside authentication practices.
```

This wording is an example of semantic shape, not mandatory final prose.

It deliberately does not state:

```text
memory failed
face-to-face trust failed
loose tokens were inadequate
institutions needed external memory
bullae arose to solve this need
writing emerged because administration outgrew humans
```

Those are interpretations that Writer may earn, qualify, partially use, reject, or leave unresolved depending on the evidence it retrieves.

## Outline authority after correction

The outline may still own:

```text
section mission
truth territory
observable historical/evidentiary transition
section boundary
continuity / dependency
non-goals
```

It must not own:

```text
causal explanation route
problem-solution chain
reason each device appears
meaning of each material step
preferred causal mechanism
preferred emotional/intellectual reveal
```

## `earned_meaning`

Do not use `earned_meaning` as a Writer-facing thesis in Probe 2.

For Probe 2, either:

1. keep it reviewer/owner-only, or
2. remove it from the Writer projection entirely while retaining it upstream for product evaluation.

Preferred experiment for Probe 2:

```text
Writer receives mission + observable historical_change
Writer does NOT receive earned_meaning
```

This gives the experiment a cleaner test of whether the Writer can discover meaning rather than paraphrase it.

---

# Root cause 2 — Material records mix evidence preservation with operational reconstruction and interpretation

Probe 1 material resolution succeeded in producing concrete objects, measurements, actions and sequences.

However, several records are too assertive about actors, workflows, purposes, standardization, representativeness and causal role.

Problematic categories include patterns such as:

```text
temple precinct accounting clerk
institutional storehouse official and transacting parties
storeroom keeper and inspecting officer
assemble laborers at granary gate
verify allocation tablet
scoop grain
disburse daily portion
tally remaining balance
```

These may be plausible or scholarly reconstructed practices, but they are not equivalent to a directly observed ancient incident.

Similarly, labels such as:

```text
universal authentication device
standard administrative material
direct material predecessor
widespread verification practice
```

can smuggle synthesis or causal genealogy into what Writer treats as source-grounded material.

The result is an evidence ledger that is concrete but not epistemically clean.

---

# Correction 2 — Split material affordances by epistemic layer

## Required principle

Material records must distinguish at least four layers rather than placing everything under `documented_action` or free-text detail.

### Layer A — Observed / materially attested

What survives or is directly observable from the artifact/corpus/context.

Examples:

```text
shape
size
material
impression
seal rolling
contents
find context
surface marks
spatial relation
artifact sequence visible in manufacture
```

### Layer B — Source-supported functional inference

What specialist scholarship infers about use/function from the evidence.

Examples:

```text
used for numerical accounting
used for authentication
associated with administrative transfer
probably records quantity/category
```

This layer must retain qualification and source attribution.

### Layer C — Representative operational reconstruction

A plausible human workflow assembled from material and comparative evidence.

Examples:

```text
a storekeeper verifies an allocation
workers receive measured grain portions
an official seals a container after inspection
```

This layer may help Writer imagine human work but must never masquerade as a documented unique event.

### Layer D — Interpretive / causal hypothesis

Explanations about why practices changed or what pressure produced the change.

Examples:

```text
administrative scale made memory insufficient
bullae evolved to prevent fraud
surface impressions solved verification at distance
record systems expanded institutional capacity
```

These are claims or interpretations, not raw story material.

They must remain bounded by claims/evidence authority and should not be silently promoted into material facts.

---

# Material schema adjustment plan

Do not rebuild the entire material architecture from scratch.

Make the minimum semantic correction necessary to preserve epistemic distance.

Preferred direction:

```json
{
  "observed": {...},
  "functional_inference": {...},
  "representative_reconstruction": {...},
  "interpretive_hypothesis": {...}
}
```

Exact schema may differ if a flatter representation integrates better with existing code.

The invariant matters more than field names:

```text
Writer must be able to know whether a detail is:
observed
inferred
reconstructed
interpretive
```

## `documented_action`

Audit or narrow this field.

It should only contain action directly supported at the claimed epistemic level.

If an artifact demonstrates a manufacture sequence, that sequence can be preserved as material process.

If a complete ancient administrative workflow is reconstructed from multiple sources, it belongs under representative reconstruction or functional inference, not `documented_action`.

## `actor`

Do not assign a specific ancient role merely because that role is the most plausible operator.

Where direct actor identity is absent, prefer neutral forms such as:

```text
possible operator role
associated institutional role
inferred user class
unknown actor
```

## `representativeness`

Require source-backed qualification.

Avoid global terms such as `universal`, `standard`, or `canonical` unless the scope and evidence actually justify them.

---

# Probe 2 implementation sequence

Execute only the following sequence before generating new prose.

## COMMIT A — Record Probe 1 rejection and stale review state

Product/provenance only.

Required changes:

- mark Probe 1 as rejected by owner/architecture review;
- mark existing automated review stale/mismatched and non-authoritative;
- preserve the draft and review artifacts for diagnosis;
- do not revise Probe 1 prose in place.

The rejected draft must remain available as a historical test artifact.

## COMMIT B — Tighten historical-change semantics

System/contract change only.

Required changes:

- update outline contract semantics;
- prohibit causal problem→solution chains from masquerading as route-neutral `historical_change`;
- add fixtures distinguishing observable change from explanatory thesis;
- ensure Writer projection does not expose `earned_meaning` for Probe 2;
- do not add style rules to Writer.

Positive fixture:

```text
A material/evidentiary configuration changes from A to B without explaining why.
```

Negative fixture:

```text
X became inadequate, therefore Y emerged to solve X and produced Z.
```

## COMMIT C — Tighten material epistemic contract

System/evidence change only.

Required changes:

- distinguish observed / inferred / reconstructed / interpretive material;
- narrow `documented_action`;
- audit actor-role authority;
- require qualification for representativeness;
- update evidence-resolution operation to preserve layer explicitly;
- update Writer broker projection so epistemic layer remains visible during retrieval;
- update Reviewer evidence-integrity guidance accordingly.

Do not tell Writer which layer makes the best story.

## COMMIT D — Re-resolve P01 materials under corrected contract

Product-only.

Rebuild or migrate P01 `materials.json` from the already approved evidence ceiling.

Do not add new research merely to improve narratability.

The material ledger should become epistemically cleaner even if this makes it less dramatically complete.

If cleaning the ledger removes the apparent story movement and P01 no longer has adequate material, material preflight must fail rather than encouraging reconstruction to fill the gap.

## COMMIT E — Amend P01 historical change

Product-only.

Replace the explanatory/cognitive problem→solution movement with a bounded observable/evidentiary transition.

Do not change Writer prompt.

Do not add a prescribed carrier, scene, sequence or reveal order.

Do not pass `earned_meaning` to Writer for Probe 2.

## HUMAN CHECKPOINT

Before Probe 2, owner reviews only:

```text
P01 mission
new observable historical_change
evidence territory
material layer summary
source/epistemic warnings
```

Owner should verify:

1. The movement is historically meaningful.
2. It does not already contain the explanation the Writer is supposed to discover.
3. The materials are concrete enough to work with.
4. The material layers honestly reflect evidence distance.
5. No story route has been pre-authored.

## PROBE 2 — Fresh clean Writer task

Create a new Writer task after all changed authority artifacts are rebound to a fresh snapshot.

Do not reuse the Probe 1 Writer task.

Do not expose:

```text
Probe 1 draft
Probe 1 review
this diagnostic document
competitor prose
FoC prose
evaluator diagnosis
repair examples
preferred story route
```

Writer receives only current task authority.

Use the same experiment shape as Probe 1:

> Write a contiguous 450–650 word passage from P01 as part of a larger unfinished section. Do not compress the whole P01 mission into the excerpt.

Do not specify opening, carrier, object sequence, scene requirement, or explanatory method.

---

# Probe 2 evaluation

Use the same five gates so the experiment remains comparable.

## Gate 1

Am I following something that is happening, being examined, or changing rather than following a narrator's argument?

## Gate 2

Is there a genuine reason to continue because something remains unresolved or in motion?

## Gate 3

Does the meaning become clear because of what I followed, or because the narrator states the explanatory model?

## Gate 4

Can I retell the progression after one hearing?

## Gate 5

Can I distinguish observed evidence, inference, reconstruction and causal interpretation without internal metadata leaking into narration?

### Additional diagnostic distinction

If Probe 2 remains essay-like after the historical-change thesis and material-layer contamination are removed, then the remaining problem should be classified primarily as:

```text
Writer objective / model behavior
```

At that point it becomes justified to experiment with Writer-level objective design.

Until then, do not add narrative craft rules merely to compensate for upstream argument encoding.

---

# Explicit non-goals for this iteration

Do not:

- restore `story-plan.json`;
- prescribe focal carrier;
- require scenes;
- require a character;
- require object-led openings;
- prescribe chronology;
- add beat counts;
- imitate FoC syntax or lexical style;
- add banned essay phrases;
- add rhetorical-device quotas;
- ask Writer to "show, don't tell" as a hard rule;
- add another claims summary;
- expand P01 evidence beyond approved sources without owner decision;
- revise old Probe 1 prose instead of creating a clean Probe 2.

The purpose of this iteration is epistemic and architectural, not stylistic.

---

# Acceptance criteria before Probe 2

Probe 2 may run only when:

- Probe 1 remains preserved and explicitly rejected;
- stale/mismatched review cannot be mistaken for current approval;
- Reviewer binding includes exact draft/task identity;
- `historical_change` no longer encodes the section's causal explanatory thesis;
- `earned_meaning` is absent from Probe 2 Writer projection;
- material records distinguish observed evidence from functional inference, representative reconstruction and causal interpretation;
- `documented_action` no longer carries reconstructed workflows by default;
- actor-role inference is labeled honestly;
- representativeness is qualified and source-backed;
- P01 materials have been migrated/re-resolved under the corrected contract;
- P01 passes material preflight after epistemic cleanup;
- a fresh material snapshot is bound to a fresh Writer task;
- Writer prompt has not been expanded with new craft prescriptions.

---

# Stop conditions

Stop before Probe 2 if:

- cleaning material layers reveals that P01 lacks enough source-grounded material;
- observable historical movement cannot be stated without embedding a causal explanation;
- the team starts solving the problem by scripting the Writer's route upstream;
- the team starts adding style rules before the upstream experiment is complete;
- P01 requires new evidence beyond current authority;
- a stale Writer or Reviewer task would survive changed evidence authority;
- product and system changes become mixed in a way that obscures diagnosis.

If any stop condition occurs, surface the blocker instead of generating prose.

---

# Architectural lesson from Probe 1

The architecture should now preserve a sharper distinction:

```text
Outline tells Writer WHAT HISTORICAL CHANGE EXISTS.
Evidence tells Writer WHAT CAN BE KNOWN ABOUT IT.
Writer decides WHAT STORY MAKES THAT CHANGE DISCOVERABLE.
Reviewer decides WHETHER THE AUDIENCE ACTUALLY DISCOVERED IT.
```

The outline must not tell Writer why the change happened in a way that already constitutes the section's argument.

The material ledger must not turn plausible scholarly reconstruction into directly documented historical action.

Probe 2 is designed to test whether removing those two forms of upstream pre-authorship is enough to make Writer behave like an author rather than an essayist.
