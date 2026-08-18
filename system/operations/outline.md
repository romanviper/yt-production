# Operation — Outline

## Responsibility

Design the audience's complete three-act journey before cutting it into bounded production work units. Do not write narration.

Outline không chỉ chứng minh rằng logic đúng. Khi human review outline, họ phải nhìn thấy phần lớn trải nghiệm của video: audience đang theo cái gì, cái gì thay đổi, bằng chứng nào mang thay đổi đó và vì sao phần kế tiếp trở nên cần thiết.

## Design order

1. Define the central question, audience promise and final change in understanding.
2. Design exactly three audience-facing acts: opening, body and ending.
3. Within those acts, design as many narrative movements as the causal material requires.
4. Match each important movement to concrete material from the outline evidence pack.
5. Test whether that material can carry the state change without narrator commentary manufacturing the movement.
6. Only then place `P##` work-unit boundaries at meaningful state changes or context/review limits.

The three acts are a channel invariant. Movement count, section count, relative length and local form are not. Never choose ten sections first or make every section repeat a hook–explanation–payoff template.

## Outline as a story preview

For every section, `outline.json` must preserve the existing schema fields and also include:

- `audience_experience`: a concise free-form preview of what the audience actually follows from entry to exit. Describe concrete object/person/action/process/consequence and the change it carries. This is not narration and not a beat sheet.
- `material_ids`: the `MAT-####` records that make that experience reconstructable. Do not invent a carrier that is absent from the pack.
- `transition`: why the resulting state naturally creates the next section or, for the ending, closes the central question.

In `script_architecture`, add `story_material_contract_version: 1` so a revised outline makes clear it was designed with the material-aware harness.

A useful outline should let a human read P01 → P02 → P03 and roughly imagine the film without waiting for a full draft. It should still leave wording, paragraph order, local reveal timing and cadence to the writer.

## Carrier and boundary check

A narrative movement may be carried by an object, person, action, process, consequence, contrast, failure or bounded puzzle. An event chain is not mandatory. But selected material must be able to carry the stated change rather than leaving the narrator to repeatedly explain that interpretation has changed.

Before assigning a section boundary, ask:

- What does the audience actually follow here besides an argument or conclusion?
- Which `MAT-####` records make that experience possible?
- Do the linked claims support what the material is being asked to do?
- If the visual is removed, is there enough concrete sequence or change for narration to reconstruct the experience?
- Does this boundary cut a useful process in half, leaving one section with only a question/puzzle and the next section with all of the action that would make it move?

If a movement needs material that research has not preserved, record a research gap instead of inventing a local strategy. If the material exists but sits across an artificial section boundary, move or merge the boundary.

Do not reject a cognitive/object puzzle merely because it lacks a historical event. Reject it only when its movement exists mainly because narrator commentary tells the audience that their interpretation has changed.

## Evidence use

Claims define what the script may assert. Materials define what concrete historical thing the story can follow. A section needs both.

`material_ids` do not replace `claim_ids`: every substantive inference still needs claim support. Conversely, a good claim list does not prove a section has enough material to tell.

The `story_material_map` from research synthesis is a recommendation and gap map, not a mandatory section structure. Outline may combine or reposition supported materials when causality and chronology allow, but it must not create missing historical detail.

## Current outline contract

Schema v4 contains:

- a whole-script architecture with the central question, audience promise and duration-derived word envelope;
- exactly three ordered acts, each with its own job and entry/exit state;
- ordered narrative movements assigned once to those acts;
- contiguous movement/section mappings that may be many-to-many inside one act;
- for each section: one narrative job, entry/exit state, evidence allowance, dependencies and an estimated word range;
- for material-aware revisions: `audience_experience`, `material_ids` and `transition` as the human-review story preview.

Section-level question, payoff, planned beats, structural-role labels and budget justifications are optional creative notes, not required fields.

`story-bible.md` keeps only global causal spine, chronology, terms, entities, setup/payoff continuity and exclusions. `voice-profile.md` captures product-specific variation inside the Channel Constitution in 150–450 words. It learns functions from benchmarks without imitating surface style.

All three artifacts remain `draft` until the user approves them. If a critical movement still has a material gap, surface that gap in the operator brief instead of presenting the architecture as production-ready.
