# Operation — Outline

## Responsibility

Design the audience's complete three-act journey before cutting it into bounded production work units. Do not write narration.

Human review must reveal most of the film before prose exists: what the audience follows, what happens/changes, which evidence carries it and why the next section becomes necessary.

## Design order

1. Define central question, audience promise and final change in understanding.
2. Design exactly three audience-facing acts: opening, body and ending.
3. Design as many narrative movements as the causal material requires.
4. Match each important movement to concrete material from the evidence pack.
5. Test whether material itself can carry the state change without narrator commentary manufacturing it.
6. Only then place `P##` work-unit boundaries.

Three acts are invariant. Movement count, section count, relative length and local form are adaptive.

## Outline as a story preview

For every material-aware section include:

- `audience_experience`: concise preview of the **reconstructable reality** the listener will follow from entry to exit;
- `material_ids`: `MAT-####` records that make the experience reconstructable;
- `transition`: why the resulting state creates the next section or closes the central question.

`audience_experience` should primarily say what exists, is done, changes, fails or leaves a consequence. Do not replace the sequence with its interpretation.

Weak:

> Viewer nhận ra thông tin đã chuyển lên bề mặt.

Stronger:

> Viewer gặp clay envelope còn tokens bên trong, rồi một numerical tablet khác có numeral marks trực tiếp trên surface. Hai vật cùng tồn tại nên section can show a change in where numerical information is carried without inventing a direct genealogy.

Interpretation belongs mainly in narrative job, exit state or payoff—not as a substitute for material.

Set `script_architecture.story_material_contract_version: 1` for material-aware outlines.

A human should be able to read P01 → P02 → ... and roughly imagine the film without waiting for narration. Wording, paragraph order, exact reveal timing and cadence remain writer decisions.

## Carrier and boundary check

A carrier may be object, person, action, process, consequence, contrast, failure or bounded puzzle. Event chain is not mandatory. But selected material must create an evidenced before/after, action/change or consequence.

For every section ask:

- What does the listener actually picture or follow besides an argument?
- Which `MAT-####` records make it possible?
- Do section `claim_ids` cover every substantive assertion required by those materials?
- If all narrator explanation were removed, would the remaining material still contain a reconstructable state/action/change/consequence?
- Can the same experience be followed by audio without relying on visual annotation to perform the reasoning?
- Does the section boundary cut the process so one section gets only analysis while another gets all action?

If no because research lacks detail → route to research. If material exists but boundary is wrong → fix outline. Do not pass the rescue job to writer.

## Evidence use

Claims answer **what may be asserted**. Materials answer **what may be recounted**. Interpretation answers **what it means**. A section needs the first two; the third must not replace either.

`material_ids` do not replace `claim_ids`. Every material must fit inside the section claim ceiling. The story-material map is recommendation/gap metadata, not a mandatory section structure.

## Current outline contract

Schema v4 contains:

- central question, audience promise and duration-derived word envelope;
- exactly three ordered acts;
- ordered movements assigned once to those acts;
- contiguous movement/section mappings;
- section narrative job, entry/exit state, evidence allowance, dependencies and estimated word range;
- for material-aware revisions: `audience_experience`, `material_ids`, `transition`.

Do not lock opening sentence, paragraph order, exact reveal timing, cadence or fixed beats. Outline decides **what story happens**; writer decides **how to tell it**.

`story-bible.md` keeps global causal spine, chronology, terms, entities, setup/payoff continuity and exclusions. `voice-profile.md` captures product-specific variation without copying benchmark surface style.

All three artifacts remain `draft` until user approval. If a critical movement lacks recountable material, surface that gap rather than calling the architecture production-ready.
