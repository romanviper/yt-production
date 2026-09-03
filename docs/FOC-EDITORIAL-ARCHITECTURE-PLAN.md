# FoC-Informed Editorial Architecture — Execution Plan

Status: `pre_draft_execution_plan_recorded`

Recorded: 2026-09-03

Branch base: canonical `main` at `1f22bc0c188e4b4aedc8dd134095277837405561`.

Scope: structural changes to the research → outline → writer → review path, followed by a bounded P01 migration and first clean Writer probe. This document records the implementation order and gates. It does not itself implement the changes or approve product prose.

## Decision

The harness must give the Writer high-resolution historical material and bounded authorship. It must not give only propositions, and Research must not pre-author a story plan for the Writer to assemble.

The target relationship is:

`source-rich material + truth boundary → Writer-authored nonfiction story`

not:

`ordered claims → illustrated essay`

and not:

`upstream story plan → mechanical prose assembly`.

The pre-draft objective is now explicit:

> Writer must not be the component that discovers that upstream lacks usable story material.

Before the first Writer task is created, the production path must be able to prove that the section has a valid truth ceiling, usable source-grounded material, a route-neutral historical movement, immutable task provenance, and deterministic routing when those conditions are absent.

## FoC audit findings that control the design

The full Sumerians script demonstrates four distinct operations:

1. **Document-led scene:** an artefact, letter, inscription or travel account already supplies an actor, action, place, object and partial sequence. The Writer selects, orders and focalizes it. The Stele of the Vultures is the strongest model.
2. **Representative reconstruction:** archaeology and social evidence are composed into a plausible local experience, such as the walk through Uruk. This is authored texture, not a documented event.
3. **Causal montage:** facts are compressed and arranged so that one pressure appears to produce the next. The causal path is an editorial product even when every component fact is supported.
4. **Speculative fusion:** later legends, contemporary inscriptions, literary texts and modern hypotheses are merged into one continuous biography or scene. The Sargon and Ishbi-Erra passages show the main failure mode.

The architecture should reproduce operations 1–3 under explicit evidence limits and detect operation 4 before publication.

## Current structural defect

### 1. Evidence is preserved primarily as conclusions

The research path can preserve `materials.json`, but the architecture still permits the main handoff to be dominated by claim statements, counterevidence and qualifications.

This preserves truth but often discards the raw elements from which a story can be authored: acting subject, documented action, object, place, explicit sequence, unresolved question and later evidence that changes interpretation.

### 2. The outline can still assign an intellectual correction

A section framed mainly as misconception → corrected model gives the Writer a proposition to prove. A prompt that later asks for compelling or cinematic prose cannot reliably reverse this upstream essay logic.

### 3. Claims-first priming has been reduced but material readiness is not yet an enforced production gate

The new Writer-directed interface removes the mandatory whole-scope claim brief and replaces it with scope attestation plus bounded search/source retrieval. That is the correct priming direction.

However, a Writer task can still exist without deterministic proof that the section territory contains usable story material. A prompt-level blocker is insufficient because the Writer can still fall back to explanation.

### 4. Material provenance is not yet task-immutable

The broker can read global and section-local material records, but the Writer task is not yet bound to one immutable material snapshot. If material artifacts change while a task is alive, retrieval can observe a different evidence state than the state under which the task was created.

### 5. The outline/Writer boundary can overcorrect by hiding historical movement

Removing entry/exit route information protects Writer authorship, but a generic mission alone may be too weak. The Writer needs to know what supported historical change the section must make followable without being told how to tell it.

### 6. Material validation is distributed rather than authoritative

Source relation, source scope, claim scope, locator requirements and forbidden narrative-role fields should be enforced by one executable contract shared by all material producers and consumers.

### 7. Evidence review must test source distance and editorial transformation

Truth checks must distinguish contemporary material, interested accounts, later copies, retrospective literature, cultural tradition and modern hypotheses. Otherwise later texts or propaganda can silently become eyewitness narration.

## Target production architecture

```text
Research
   ↓
approved claims + sources + preserved source material
   ↓
Outline
   ↓
historical movement + truth territory
   ↓
Material preflight
   ├── enough material ──────────────┐
   │                                ↓
   └── insufficient → Evidence Resolution
                       │
                       ├── resolved ─┘
                       │
                       └── impossible → HUMAN BLOCKER

                                      ↓
                           Fresh Writer Task
                                      ↓
                          Writer discovers material
                                      ↓
                           Writer authors story
                                      ↓
                         Outcome + Evidence Review
```

The production path must not skip from outline directly to drafting merely because claim coverage exists.

---

# Pre-first-draft closure plan

The following six steps are required before the first Writer Agent is allowed to generate P01 prose under the new architecture.

The first four are system commits. After they pass, the system architecture is frozen for the first probe. The next two are P01 product commits. Only after the product migration and human gate may a clean Writer task be created.

## SYSTEM COMMIT 1 — Make materials a single executable evidence contract

### Goal

Turn `materials` from a useful convention into an authoritative evidence object with one canonical validator.

### Required implementation

Create a shared contract, preferably:

```text
scripts/material_contract.py
```

All material-producing and material-consuming paths must use this contract rather than implementing partial local checks.

A canonical material record should be able to preserve fields such as:

```json
{
  "id": "MAT-0001",
  "kind": "object",
  "label": "...",
  "claim_ids": ["CLM-0001"],
  "source_refs": [
    {
      "source_id": "SRC-0001",
      "locators": ["p. 42"]
    }
  ],
  "source_relation": "contemporary_material",
  "actor": null,
  "object_or_trace": "...",
  "documented_action": "...",
  "explicit_sequence": [],
  "time": null,
  "place": "...",
  "physical_description": "...",
  "measurement": null,
  "spatial_relation": null,
  "unresolved_question": null,
  "later_evidence": null,
  "limitations": [],
  "representativeness": null
}
```

The exact optional field set can remain compact, but the contract must preserve the distinction between evidence observations and narrative decisions.

### Required validation

At minimum validate:

- material ID and schema version;
- linked claim IDs are inside the approved claim ceiling;
- linked source IDs are inside approved sources;
- narrow source locators are present where required;
- `source_relation` is required when the architecture depends on source distance;
- source relation belongs to the approved ontology;
- `explicit_sequence` records source/document sequence, not a proposed storytelling order;
- material does not widen the truth ceiling;
- material does not contain upstream creative-authority fields.

Forbidden creative-authority fields include, at minimum:

```text
opening
hook
focal_carrier
reversal
climax
ending
emotional_beat
story_role
narrative_route
narratability_score
```

### Shared consumers

The shared material contract must be used by the relevant paths, including:

```text
scripts/consolidate_research.py
scripts/draft_evidence.py
scripts/validate.py
evidence_resolution output validation
research workstream material validation
```

### Gate

This commit does not pass if a malformed or out-of-scope material record can still be loaded by the Writer evidence broker.

---

## SYSTEM COMMIT 2 — Put material preflight and evidence resolution into the real lifecycle

### Goal

Make material readiness a routing requirement rather than a Writer prompt instruction.

### Required routing

Before any `draft_section` task is created, operator/lifecycle code must run a deterministic section material readiness check.

The result must be one of:

```text
material_ready
needs_evidence_resolution
blocked
```

### Route: `material_ready`

Only this result may authorize creation of a fresh `draft_section` task.

### Route: `needs_evidence_resolution`

Do not create a Writer task.

Route one bounded:

```text
evidence_resolution
```

The operation may recover source-level material only from already approved sources and within the existing truth ceiling.

After evidence resolution completes, run material preflight again.

```text
resolved          → draft allowed
still insufficient → owner blocker
```

Do not create an autonomous AI repair loop that repeatedly invents or expands research until something becomes narratable.

### Route: `blocked`

Stop before drafting and surface an owner decision. The system must not manufacture a generic illustrative incident to compensate for inadequate evidence.

### Authority boundary

`material_preflight` is an operator/router responsibility, not a Writer capability.

The Writer should not have to decide whether the section deserves to exist as a narrative task. It should only receive a territory that already passed readiness.

### Required integration

Reconcile the flow across the relevant executable components, including:

```text
scripts/lifecycle.py
scripts/context_packet.py
scripts/replay.py
scripts/draft_evidence.py
system/operations/registry.json
associated tests
```

Replay semantics must understand the conditional evidence-resolution checkpoint. The canonical path must no longer behave conceptually as only:

```text
outline → draft
```

but as:

```text
outline
  ↓
material preflight
  ↓
[evidence_resolution]
  ↓
material preflight
  ↓
draft
```

### Gate

This commit does not pass if a claims-only or conclusions-only section can create a Writer task merely by completing scope attestation.

---

## SYSTEM COMMIT 3 — Bind one immutable material snapshot to every Writer task

### Goal

Make the evidence state used by a Writer reconstructable and immutable for the life of the task.

### Required task authority

When a Writer task is created, bind at least:

```json
{
  "evidence_authority": {
    "evidence_pack_sha256": "...",
    "material_snapshot_sha256": "..."
  }
}
```

A compiled deterministic snapshot is preferred, for example:

```text
03_sections/P01/material-snapshot.json
```

Conceptual structure:

```json
{
  "schema_version": 1,
  "section": "P01",
  "cycle_id": "C004",
  "claim_ids": [],
  "source_ids": [],
  "material_ids": [],
  "inputs": [
    {"path": "...", "sha256": "..."}
  ]
}
```

The snapshot is an authority/provenance artifact, not a Writer story brief.

### Broker rule

Once the task exists, Writer retrieval should resolve against the bound snapshot or verify that live inputs still match it. The broker must not silently expose a new material state to an old task.

If any authority-bearing input changes, including relevant evidence/material artifacts, the old Writer task becomes stale and must be recreated.

### Required behavior

A task created under material state A must never:

- attest scope under state A;
- retrieve material from state B;
- submit prose while claiming state A provenance.

### Gate

This commit does not pass until tests prove that material mutation invalidates or rejects an existing Writer task.

---

## SYSTEM COMMIT 4 — Transmit historical movement without transmitting a story route

### Goal

Give the Writer enough section-level trajectory to author a story while preserving creative control over how the story is told.

### Separate two concepts

#### Historical movement

This describes what changes in the historical world or surviving evidence.

It must not be phrased primarily as an audience misconception being corrected.

Bad:

> Audience moves from believing writing was invented suddenly to understanding that it developed gradually.

Better:

> Administrative records move from quantity/accounting marks tied to specific goods toward signs capable of carrying increasingly abstract linguistic information.

The second statement is a historical/evidentiary movement. It tells the Writer what must become followable without assigning a scene, carrier, opening, climax or reveal order.

#### Earned meaning

This describes what the listener should be able to understand because the historical movement was made followable.

For example:

> Writing did not arrive fully formed; its expressive capacity grew out of earlier information systems.

This is meaning to earn, not a thesis the draft must announce and defend.

### Section contract

Normalize the outline around a route-neutral structure such as:

```json
{
  "mission": "...",
  "historical_change": {
    "from": "...",
    "to": "..."
  },
  "earned_meaning": "..."
}
```

Exact field names may change during implementation, but the authority boundary must remain:

```text
historical_change = Outline authority
earned_meaning    = destination
telling           = Writer authority
```

### Writer projection

The Writer packet should expose the section mission and route-neutral historical movement.

It must not expose:

```text
claim order
material order
story plan
recommended focal carrier
opening suggestion
beat sequence
reveal order
camera instructions
benchmark decomposition
evaluator diagnosis
old rejected draft
repair hypothesis
```

Whether `earned_meaning` is exposed directly to Writer should be decided conservatively. If exposed, it must remain a destination/constraint rather than an ordered proposition to prove. A minimal projection of mission + historical movement is preferred for the first probe if it preserves adequate trajectory.

### Outline contract validation

A section must be able to answer:

- What changes in the historical world or surviving evidence?
- What approved concrete material can make that change followable?
- Why does the next section become necessary because of the resulting state?

The outline must not prescribe prose route, camera, scene, character, focal carrier, beat order or reveal sequence.

### Gate

This commit does not pass if the Writer receives only a generic mission with no meaningful supported trajectory, or if the fix restores a hidden story plan upstream.

---

# SYSTEM FREEZE

After SYSTEM COMMIT 4 passes validation, stop changing the harness before the first product probe.

Do not respond to every disappointing sentence by immediately adding another Writer rule, style heuristic or benchmark-derived craft instruction.

The purpose of the first probe is to test whether the architecture itself changed the optimization problem. The probe is not useful if the system changes continuously while the product is being evaluated.

Only a hard correctness failure, provenance failure or truth-authority failure should break the freeze before the first probe.

---

## PRODUCT COMMIT 1 — Resolve P01 evidence into source-grounded story material

### Goal

Make P01 a materially usable historical territory without pre-authoring its story.

### Allowed inputs

The evidence-resolution agent is bounded to:

```text
approved P01 claim scope
approved P01 sources
approved locators
existing research artifacts
```

It must not widen the research question or automatically add new web research.

If P01 requires evidence outside the approved ceiling, stop for an owner decision rather than silently enlarging authority.

### Expected material affordances

The resulting evidence handoff should preserve as many genuinely supported answers as available to questions such as:

```text
What physical objects survive?
Who or what acts?
What documented action occurs?
What changes physically or administratively?
What sequence is directly present in a source?
Where does it occur?
What can be measured?
What spatial relation matters?
What uncertainty remains?
What later evidence changes an interpretation?
How far is each source from the event it describes?
```

The evidence-resolution agent must not answer creative questions such as:

```text
What should the opening be?
What should the Writer follow?
Which object should be the focal carrier?
What is the emotional beat?
What is the climax?
What is the reveal order?
```

### Required output quality

Material records should preserve:

- actual objects or traces;
- documented actions;
- source sequences where present;
- narrow locators;
- physical/spatial/measurement details where supported;
- unresolved questions and later interpretive evidence;
- source-distance limitations;
- representativeness and uncertainty.

### Gate

After P01 evidence resolution, run deterministic material preflight.

Only:

```text
material_ready
```

may advance.

If the result remains `needs_evidence_resolution` or `blocked`, stop before Writer generation. Do not "let the Writer try anyway."

---

## PRODUCT COMMIT 2 — Amend the P01 section contract around historical movement

### Goal

Make P01's section contract describe a supported historical movement rather than a misconception rebuttal, while leaving the telling entirely to Writer.

### Allowed changes

Product-only changes may include:

```text
mission
historical_change
section boundary
evidence territory if it must be narrowed
transition into P02
earned meaning if retained as an outline field
```

Do not write prose and do not create a story plan.

### Required questions

P01 must have explicit answers to:

#### Historical change

What changes in the historical world or surviving evidence during P01?

#### Followability

Does approved material allow a listener to follow that change through concrete evidence rather than only hear an explanation of the conclusion?

#### Necessity

Why does the state reached at the end of P01 make P02 necessary?

### Gate

P01 does not advance if the section contract is still primarily equivalent to:

```text
viewer believes X → narrator explains correct Y
```

---

# HUMAN GATE BEFORE WRITER

Before the first Writer task is created, present a compact owner review containing only the product-level contract needed to verify the territory:

```text
P01 mission
P01 historical change
P01 evidence boundary
available material summary
source-distance warnings
```

The owner approves whether this is the historical story territory P01 should be able to tell.

The owner does not approve or prescribe:

```text
opening
scene
carrier
POV
beat order
climax
ending
reveal sequence
sentence style
```

This protects Writer authorship while retaining owner authority over product intent and truth territory.

---

# First clean Writer task

Only after all six steps and the human gate may the first Writer Agent be created.

The Writer must be a clean task. It must not receive hidden contamination from architecture diagnosis or previous rejected prose.

Do not expose:

```text
FoC analysis
competitor prose
old P01 drafts
old rejected probes
architecture discussion
evaluator reports
repair hypotheses
benchmark-derived scene instructions
```

The Writer receives only the authorities needed for the current task, including:

```text
creative boundaries
draft operation
P01 mission
P01 historical movement
continuity-in
bounded evidence interface
immutable evidence/material authority
```

The evidence interface begins with route-neutral scope attestation, not a whole-scope ordered claim brief.

The Writer independently decides what it needs to retrieve and how to compose the telling, including:

```text
which object or action to inspect
which source detail to open
where to begin
whether a focal carrier is useful
whether no single carrier is better
how much exposition is necessary
whether representative reconstruction is useful
how to order supported material
how to earn meaning
```

---

# First probe design

Do not generate the full P01 immediately.

The first probe is a contiguous excerpt from the future full section, not a compressed summary of the whole section.

Target instruction:

> Write a contiguous 450–650 word passage from P01 as part of the full section. Do not compress the whole P01 mission into the excerpt. Treat this as an excerpt from a larger unfinished section.

The Writer should not be forced to make the excerpt the opening. Let the Writer choose a passage that demonstrates how it would make the section followable.

The word range is a probe boundary, not a permanent prose optimization target.

---

# First probe evaluation

Do not evaluate the probe against a long method checklist. Use a small outcome test plus evidence integrity.

Ask:

1. **Am I following something that is happening or changing?**
2. **Do I want to know what happens next?**
3. **Does meaning emerge from what I followed, or is the narrator mainly explaining a thesis?**
4. **Can I retell the progression I just heard?**
5. **Did any reconstruction, hypothesis, later source or interested account masquerade as documented contemporary fact?**

Questions 1–4 diagnose whether the architecture escaped essay-first composition. Question 5 protects the truth boundary.

If 1–4 fail despite demonstrably adequate source material and a valid historical movement contract, treat the result as evidence of a Writer objective/model problem rather than immediately adding another upstream schema or craft rule.

---

# Commit sequence

Execute in this order:

```text
SYSTEM COMMIT 1
material evidence contract

SYSTEM COMMIT 2
preflight + evidence-resolution routing

SYSTEM COMMIT 3
immutable material snapshot / provenance binding

SYSTEM COMMIT 4
historical-movement contract + Writer projection

──────────────────── SYSTEM FREEZE ────────────────────

PRODUCT COMMIT 1
P01 evidence resolution

PRODUCT COMMIT 2
P01 historical-movement outline amendment

──────────────────── HUMAN GATE ───────────────────────

CLEAN WRITER TASK
450–650 word contiguous P01 excerpt
```

Do not combine protected system changes with product content in one commit.

Do not regenerate P01 prose during SYSTEM COMMITS 1–4.

Do not use product output to justify silently widening system scope inside a product commit.

---

# Evidence and reconstruction model

Keep one truth model across Research, Writer and Reviewer.

## 1. Documented fact

An assertion maps to reviewed evidence and preserves relevant qualification.

## 2. Qualified inference

The inference is supported but uncertainty remains visible. Confident prose must not convert it into documented fact.

## 3. Representative reconstruction

Plausible ordinary particulars may embody approved conditions, but reconstruction cannot establish a new:

- named historical actor;
- quotation;
- institution;
- technology;
- chronology;
- measurement;
- motive;
- causal conclusion;
- unique historical incident;
- private thought;
- secret plan;
- dialogue.

Representative reconstruction may create experiential continuity and texture only inside the approved truth ceiling.

---

# Source relation and editorial-transformation review

Source relation should distinguish at least:

```text
contemporary_material
contemporary_interested_account
later_copy
retrospective_literature
cultural_tradition
modern_hypothesis
```

Review must detect transformations such as:

- later copy narrated as live contemporary testimony;
- royal or institutional propaganda narrated as neutral report;
- heterogeneous legends fused into one factual biography;
- multiple centuries compressed into one unqualified incident;
- correlation promoted to sole or inevitable causation;
- invented motive, dialogue, plan or private thought;
- representative reconstruction used as proof of the section conclusion.

Review should distinguish an unsupported factual assertion from a permissible authored transition. It should not demand archival support for every connective word.

---

# Acceptance criteria before first Writer probe

The system is ready for the first Writer probe only when all of the following are true:

- one shared executable material contract governs producers and consumers;
- source relation and source scope are machine-validated where required;
- forbidden narrative-role fields cannot enter material authority;
- material preflight executes before Writer task creation;
- insufficient material routes to evidence resolution or a blocker;
- evidence resolution cannot silently widen the approved truth ceiling;
- a Writer task cannot be created from a claims-only territory that lacks usable story material;
- a Writer task binds one immutable evidence/material snapshot;
- material mutation invalidates or rejects a stale Writer task;
- Writer packet no longer begins with an ordered proposition list;
- Writer receives a supported route-neutral historical movement rather than only a generic mission;
- Writer does not receive a pre-authored story route;
- P01 has passed evidence-resolution material readiness;
- P01 outline describes historical movement rather than misconception correction;
- owner has approved the P01 territory before prose generation;
- old P01 drafts and diagnosis artifacts are absent from the clean Writer task.

---

# Validation

For every system implementation commit:

```text
python -m unittest discover -s tests
python scripts/validate.py products/sumer-writing
git diff --check
git status --short --branch
```

Add focused positive and negative fixtures.

## Positive fixtures

- a source-rich artefact sequence passes material readiness and supports Writer retrieval;
- a source-grounded action/object/place record remains unordered and route-neutral;
- a signaled representative reconstruction adds no new historical claim;
- material mutation invalidates an existing Writer task;
- a valid historical movement reaches Writer without scene or beat instructions.

## Negative fixtures

- claims-only input attempts to create a draft task without material resolution;
- material record references an out-of-scope claim or source;
- material record omits required source-distance information;
- material record contains `focal_carrier`, `opening`, `climax` or another creative-authority field;
- a later school copy is presented as a live dispatch;
- heterogeneous legends are fused into an unqualified biography;
- a reconstructed incident is used as evidence for the conclusion;
- an old Writer task retrieves evidence after its bound material snapshot changes.

---

# Stop conditions

Stop implementation or drafting when:

- the proposal starts assigning story routes upstream;
- the schema expands without changing Writer input, routing or reviewer observability;
- material readiness remains advisory rather than executable;
- P01 requires evidence outside its approved ceiling;
- a representative reconstruction needs a new practice, chronology, motive or causal conclusion;
- system and product changes cannot be separated;
- the Writer is being asked to solve an evidence insufficiency problem that routing should have caught;
- the first probe remains essay-like despite adequate material and a valid movement contract.

The last condition is especially important. Once upstream provides adequate material, a valid truth ceiling and route-neutral movement while preserving Writer authorship, continued essay-like output should be diagnosed as a Writer objective/model problem rather than answered automatically with another architecture rule.

---

# Architectural invariant

The architecture is successful only if each layer owns a different decision:

```text
Research owns: what the sources can support.
Evidence resolution owns: preserving usable source-grounded material.
Outline owns: what historical movement the section must make followable.
Router owns: whether the territory is ready to draft.
Writer owns: how to tell the story.
Reviewer owns: whether the resulting audience experience and evidence integrity succeed.
Owner owns: product intent, truth-boundary exceptions, and approval gates.
```

No layer should perform another layer's work merely to make the next AI call easier.
