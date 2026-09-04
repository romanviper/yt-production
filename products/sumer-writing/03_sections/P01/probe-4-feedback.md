# Probe 4 feedback — macro architecture correction

Status: `stop_writer_loop_and_fix_historical_substrate`

Reviewed branch: `codex/foc-editorial-probe3`

Reviewed commit: `0ffe7d194d1c7ec1c704c970e36cdda4279659a2`

## Decision

Reject Probe 3 as production prose and stop creating another Writer probe until the architecture below is corrected.

Do not respond to Probe 3 by adding more narrative, scene, character, pacing, sensory, hook, carrier, immersion or prose instructions. The problem is now clearly upstream of local craft rules.

Probe 3 is epistemically safer than earlier probes, but the prose has become a historical-evidence analysis wrapped in narrative rhetoric. That failure is not caused by insufficient narrative technique. It is caused by the information architecture handed to Writer.

## What Probe 3 demonstrates

Across the three probes, the surface form changed while the underlying operation stayed substantially the same:

```text
Probe 1
ordered explanatory proposition
→ Writer turns proposition into an illustrated essay

Probe 2
artifact-class evidence
→ Writer turns artifact classes into museum-guide exposition

Probe 3
specific artifact instances
→ Writer turns catalogue instances into an evidentiary tour with narrative phrasing
```

The repeated invariant is not "Writer refuses to narrate."

The repeated invariant is:

> Writer is still being asked to manufacture historical prose directly from an evidence representation.

Changing the granularity of that evidence changes the wrapper, not the core writing operation.

Probe 3 makes this visible. The passage opens on OIM A64678 and ChM III-937a, but the actual progression remains:

```text
inspect object A
→ explain what it proves
→ explain what it cannot prove
→ inspect object B
→ explain what it proves
→ explain what it cannot prove
→ compare A and B
→ state the historical implication
```

That is a research interpretation workflow, not a historical story workflow.

## Root cause

The current architecture is missing an intermediate representation of **history itself**.

Today the effective pipeline is approximately:

```text
sources
→ claims / material records / epistemic layers
→ section mission + historical_change
→ Writer
→ prose
```

The system has a good representation of **what sources say and permit**, but it does not have a first-class representation of **the bounded historical world those sources support**.

As a result, Writer is forced to perform two fundamentally different jobs at once:

1. reconstruct a usable model of historical reality from evidence records;
2. author compelling narration from that model.

Because truth constraints are strong and evidence records are the most concrete information available, the model naturally keeps the research representation visible in the prose. It talks about what "the evidence permits," what "we cannot know," what an artifact "shows," and what a catalogue object "does not tell us."

This is not primarily a stylistic failure. It is an architectural coupling failure.

## The missing layer: Historical Substrate

Introduce a new canonical layer between evidence authority and Writer. Call it `historical_substrate`, `historical_model`, or another clear name. The name is less important than the authority boundary.

Its job is:

> Convert approved evidence into a bounded, source-backed model of historical states, practices, processes, actors/roles, objects, relations and changes — without deciding how the story should be told.

The target pipeline becomes:

```text
Research / Evidence Authority
        ↓
approved claims + sources + epistemic constraints
        ↓
Historical Substrate
        ↓
bounded model of the historical world
        ↓
Outline
        ↓
historical movement / section territory
        ↓
Writer
        ↓
prose
        ↓
Evidence Review checks prose back against authority
```

Writer should author from **history**, not directly from the research ledger.

## What belongs in Historical Substrate

The substrate is not a story outline and must not contain narrative choreography.

It may contain factual or qualified historical primitives such as:

```text
entities / roles
practices
objects and media
actions or operations
state changes
temporal coexistence / ordering where supported
spatial relations where supported
institutional relationships where supported
functional affordances
constraints
known unknowns
confidence / epistemic status
supporting claim/source references
```

For P01, a substrate might represent facts such as:

```text
- Late-Uruk administrative practice used multiple clay-based recording and authentication media.
- Some hollow clay envelopes enclosed counters.
- Some envelopes also carried exterior marks/sealings.
- Numerical tablets carried quantity information directly as impressions on a durable surface.
- Seal impressions could coexist on those surfaces.
- Tokens, envelopes, sealings and tablets overlap in time; a single replacement sequence is not established.
- The evidence supports a shift in recording practice toward making numerical information directly inspectable on durable surfaces.
```

Notice what this does **not** contain:

```text
start with a broken envelope
compare two Chogha Mish objects
use an artifact as carrier
reveal the tablet second
create tension around hidden contents
open on a mystery
build toward a visual surface metaphor
end on a rhetorical question
```

Those remain Writer choices.

## Critical distinction: evidence authority vs narrative substrate

The architecture must enforce this separation:

```text
Evidence layer answers:
What are we allowed to believe or claim?

Historical substrate answers:
What bounded historical reality follows from that evidence?

Outline answers:
What historical change must this section make followable?

Writer answers:
How do I make a listener experience and understand that change?
```

At present Evidence and Historical Substrate are effectively collapsed into the same representation. That is the root architectural defect exposed by Probe 3.

## Writer evidence access must become secondary, not primary

The bounded evidence broker should remain available, but its role should change.

Current behavior encourages Writer to discover its telling by searching evidence records. That makes evidence records the primary creative substrate.

For the next architecture:

```text
primary Writer input:
validated historical substrate + section movement

secondary Writer capability:
source/evidence lookup only when a chosen telling needs verification, specificity or qualification
```

Evidence retrieval should answer questions raised by authorship. It should not be the place where authorship is expected to discover what history exists to tell.

This is a macro routing change, not a wording change to `draft-section.md`.

## Epistemic integrity must not require epistemic commentary

Probe 3 repeatedly verbalizes internal safety reasoning:

```text
we do not know who...
the object cannot tell us...
the evidence does not permit...
we cannot turn this into a scene...
```

This happens because Writer receives uncertainty primarily as research metadata and must itself decide how to preserve it.

The substrate should encode uncertainty as an authority boundary attached to historical propositions, while review verifies that the final prose does not exceed it.

Architectural invariant:

> `unknown` means Writer may not invent the answer. It does not mean Writer must narrate the existence of the unknown.

Likewise:

> `contested` means Writer may not present the contested proposition as settled. It does not mean every contested point must become an explicit historiographical aside.

Do not solve this with a local instruction such as "avoid saying we don't know." Solve it by separating historical propositions from provenance/constraint metadata and changing what is primary in Writer context.

## Historical change must describe the historical world, not the evidence corpus

The current P01 `historical_change` is improved relative to Probe 1, but it is still framed partly through surviving evidence:

```text
From: Bằng chứng Late Uruk lưu giữ...
To: Thông tin số ngày càng xuất hiện...
```

That formulation pulls the task toward archaeological comparison.

Move the contract one level closer to historical practice while preserving route-neutrality.

Conceptually:

```text
from:
Quantities and authentication were handled through several separate physical devices and clay practices.

to:
Recording practices increasingly placed numerical information directly on durable clay surfaces, sometimes alongside authentication marks.
```

This is still not a story plan. It does not state a cause, a hero, a scene, a chronology of beats or a necessary genealogy. It simply defines the historical transformation rather than the evidence transformation.

Do not treat the exact wording above as a local patch. Update the semantic contract so all future sections distinguish:

```text
historical-world state/change
from
evidence-state/change
```

## Mission contract also needs architectural review

P01 currently asks:

> Điều gì khiến việc giữ thông tin bằng những dấu bền trên đất sét trở nên hữu ích?

An interrogative mission naturally invites the model to answer a question. That creates explanatory pressure even when the historical change is clean.

Do not merely rewrite this one sentence and declare the problem solved.

Review the mission contract system-wide. A Writer-facing mission should define the historical territory or audience discovery without forcing an answer-shaped essay.

Possible structural separation:

```text
historical_territory:
what part of history this section owns

historical_change:
what changes in the historical world

audience_discovery:
what becomes understandable by following that change
```

`audience_discovery` must be non-thesis-prescriptive and may be hidden from Writer if it creates conclusion priming.

The key macro requirement is that Writer should not receive a question whose natural completion is an explanatory answer and then be asked not to write an essay.

## Stop conditions before Probe 4

Do not generate Probe 4 until all of the following are true:

1. A first-class Historical Substrate contract exists.
2. P01 has been compiled into that substrate from already approved evidence.
3. The substrate is validated against claim/source authority.
4. The substrate contains historical-world primitives, not narrative roles or prose route.
5. Writer packet uses the substrate as primary historical input.
6. Raw material/evidence search remains optional verification rather than the Writer's main discovery substrate.
7. `historical_change` is expressed as historical-practice/world change rather than change in surviving evidence.
8. The mission contract has been reviewed so Writer is not structurally tasked with answering an explanatory question.
9. No new narrative-style rules have been added to compensate for the architecture.

## Proposed implementation sequence

### SYSTEM COMMIT A — Historical Substrate contract

Create a shared executable contract, for example:

` scripts/historical_substrate_contract.py `

Canonical substrate records should support bounded primitives such as:

```json
{
  "id": "HS-P01-0001",
  "kind": "practice | state | process | relation | change | object_affordance",
  "statement": "...",
  "epistemic_status": "documented | qualified_inference | bounded_reconstruction",
  "claim_ids": [],
  "source_refs": [],
  "time_scope": "...",
  "place_scope": "...",
  "limitations": []
}
```

The exact schema is open to implementation, but it must reject narrative-authority fields such as:

```text
opening
hook
carrier
scene
beat
reveal
climax
ending
emotional_turn
camera
story_role
recommended_order
```

### SYSTEM COMMIT B — Evidence → Historical Substrate compilation

Add an operation that synthesizes approved evidence into historical primitives.

This operation may infer only within the existing truth ceiling. It must preserve epistemic status and provenance.

It must not author prose or choose a story route.

The output should be reviewable and deterministic enough that changing evidence invalidates the substrate snapshot.

### SYSTEM COMMIT C — Outline consumes substrate

Update outline/section contracts so `historical_change` is validated against substrate states/practices rather than written directly from evidence descriptions.

The outline should select historical territory and movement, not artifacts to feature.

### SYSTEM COMMIT D — Writer packet consumes substrate

Writer-facing packet should include:

```text
section territory / mission contract
historical change
relevant historical substrate
continuity
truth boundaries
optional bounded verification interface
```

It should not expose the research ledger as the primary thing to follow.

### SYSTEM COMMIT E — Review maps prose back to evidence

Reviewer, not Writer narration, should carry the burden of checking:

```text
unsupported certainty
unmarked reconstruction where marking is necessary
source-distance violations
causal overreach
genealogical overclaim
```

This closes the loop:

```text
Evidence → Substrate → Writer → Prose → Evidence Review
```

rather than:

```text
Evidence → Writer talks about Evidence
```

## P01 migration after system changes

After the architecture exists, migrate P01 without widening research.

Compile the already approved material into a P01 historical substrate.

The migration should explicitly distinguish at least:

```text
historical practice/state
artifact evidence supporting it
epistemic qualification
```

The two Chogha Mish artifact instances may remain available as supporting evidence. They should not automatically appear in Writer context as the thing the story must follow.

If Writer wants to inspect them for specificity, it may retrieve them on demand.

## Probe 4 experiment

Only after the macro architecture is in place, create a fresh Writer task.

Experimental control:

- fresh Writer;
- no Probe 1/2/3 prose;
- no previous feedback documents;
- no competitor prose;
- no prescribed scene, character, carrier, artifact, opening or reveal order;
- same bounded P01 truth ceiling;
- no new narrative craft rules;
- historical substrate is the principal historical input;
- evidence broker remains available for verification;
- contiguous excerpt remains acceptable as a test boundary, but the instruction must be fully bound in task provenance.

The purpose of Probe 4 is not "make it more narrative."

The purpose is:

> Test whether Writer behaves differently when it is given a model of history to author from instead of an evidence ledger to translate into prose.

## Probe 4 evaluation

Evaluate the resulting passage on the original audience outcomes, but add one architectural diagnostic question:

1. Am I following historical reality changing, or am I following the narrator's analysis of evidence?
2. Do I want to know what happens/changes next?
3. Does meaning arise from the historical progression rather than being supplied as an answer?
4. Can I retell the progression after one hearing?
5. Did any inference/reconstruction/source-distance issue become false fact?
6. If the prose is still expository, is that exposition demanded by the historical substrate itself, or introduced by Writer despite a usable historical model?

If Probe 4 still collapses into essay-like narration after the Historical Substrate is clean, then the evidence architecture is no longer the primary suspect. The next investigation should target Writer task objective/model behavior and possibly separate nonfiction composition planning from prose generation.

## Architectural invariant to carry forward

```text
Research owns what can be supported.
Historical Substrate owns the bounded model of what happened / existed / changed.
Outline owns which historical movement the section covers.
Writer owns how that history becomes narration.
Reviewer owns whether narration remains within evidence authority and succeeds for the audience.
Owner owns product intent and approval.
```

No layer should make the next layer easier by silently doing that next layer's creative job.

Most importantly:

> Evidence is authority for the story. Evidence must not be mistaken for the story's native representation.
