# Operation — Outline

## Responsibility

Design **where the story must go**, not the route the writer must take to get there. Do not write narration and do not pre-author local storytelling mechanics.

Outline owns architecture of inquiry/progression:

- central question and audience promise;
- whole-product progression;
- section objective / narrative job;
- entry state and exit state;
- section boundaries;
- evidence territory through approved `claim_ids`;
- dependencies and continuity;
- why the next section becomes necessary;
- bounded word allocation.

It does not own exact carrier, object sequence, mental imagery sequence, precise narrative route, reveal strategy, paragraph order or storytelling mechanics.

## Design order

1. Define central question, audience promise and final change in understanding.
2. Design exactly three audience-facing acts: opening, body and ending.
3. Within those acts, design as many movements as the inquiry/causal progression requires.
4. Define each movement's objective and audience state change.
5. Assign approved evidence territory (`claim_ids`) broad enough for the writer to solve that objective without silently expanding the truth ceiling.
6. Only then place `P##` work-unit boundaries at meaningful state/context/review limits.

Three acts are invariant. Movement count, section count, relative length and local storytelling form are adaptive.

## Section abstraction level

A current section should let a human answer:

- Section này đang hỏi hoặc làm rõ điều gì?
- Audience bắt đầu với nhận thức nào?
- Audience cần kết thúc với nhận thức nào?
- Evidence territory nào được phép dùng?
- Section này đóng vai trò gì trong whole-product progression?
- Vì sao section kế tiếp trở nên cần thiết?

Use existing fields `narrative_job`, `entry_state`, `exit_state`, `claim_ids`, `dependencies`, `target_words` and `transition` for that architecture.

Set `script_architecture.writer_authorship_contract_version: 1` for new/revised outlines produced under this harness.

Legacy `story_material_contract_version`, `audience_experience` and `material_ids` may remain readable in older artifacts, but they are compatibility metadata only. New output must not require or generate them.

## Writer freedom test

Before approving a section architecture, ask:

> Could a competent writer achieve this objective through a different evidence-safe narrative route than the one I personally imagine?

If yes, the outline is at the right abstraction level.

If a section only works when one exact carrier, object sequence or reveal order is followed, either:

- the objective/evidence territory is too narrow and should be reframed; or
- the evidence itself is insufficient and research must be reopened.

Do not solve that problem by encoding the preferred route into the outline.

## Evidence use

`claim_ids` define the approved truth territory for substantive historical interpretation/generalization. They are an allowance, not a list of facts that must all appear.

Outline may identify factual gaps or evidence constraints, but it should not rank material by narratability or decide opening/reversal/ending carriers.

Optional preserved material may exist in research for source-detail retention. It is not a mandatory abstraction between claim and writer and does not become section authority merely because it exists.

## Current outline contract

Schema v4 contains:

- central question, audience promise and duration-derived word envelope;
- exactly three ordered acts;
- ordered movements assigned once to those acts;
- contiguous movement/section mappings;
- section narrative job, entry/exit state, evidence allowance, dependencies, transition and estimated word range.

`story-bible.md` keeps global causal spine, chronology, terms, entities, setup/payoff continuity and exclusions. `voice-profile.md` captures product-specific variation without copying benchmark surface style.

All three artifacts remain `draft` until user approval. Human review at outline stage judges architecture and evidence scope; deep storytelling judgment may legitimately wait until a draft exists.
