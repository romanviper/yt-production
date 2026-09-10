# Operation — Outline

## Responsibility

Design the historical journey the audience will actually follow before prose begins. Outline is not a taxonomy of facts and is not limited to abstract objectives while every meaningful story decision is postponed to Writer.

Outline owns:

- central question, audience promise, scope and final understanding;
- opening: what becomes concretely worth following and why;
- whole-work movements selected for their role in that journey;
- the circumstances, event/process/discovery and change each movement develops;
- structural relationships among movements and why information appears where it does;
- recurring relationship, case, point of inquiry, discovery order or viewpoint when these choices are necessary to make the whole work coherent;
- where exposition is needed and what story problem it resolves;
- evidence/material refs, uncertainty boundaries and dependencies;
- production-section boundaries and flexible duration estimates when needed by runtime.

Writer still owns local execution: sentence/paragraph construction, exact transitions, local pacing, imagery, scale shifts, phrasing and evidence-safe choices within the architecture. Writer may propose reopening the outline when the promised movement cannot be told from available material.

## Design order

1. State the question, promise, scope and what would count as a meaningful ending.
2. Decide what historical reality the listener first follows.
3. Add only movements that develop, complicate or transform that reality.
4. For each movement identify: starting circumstance; event/process/discovery; what changes; why the next movement follows; evidence/material anchors; unresolved boundaries.
5. Place exposition only where it helps the audience continue something already worth understanding.
6. Check the middle for accumulation: if movements merely restate the same conclusion through different examples, reorganize or replace them.
7. Cut `P##` units only for production/context/review needs. Production units need not equal narrative movements.

No fixed movement count is required. A whole work may have three acts, another structure, montage or an investigative return pattern if the material supports it.

## Human-readable authority and machine mirror

For substantial narrative work, `outline.md` is the human-readable canonical story architecture. If `outline.json` remains required by runtime, mirror the same question, movement order, evidence territory, status and section mapping there. Do not maintain two independent creative versions.

New/revised content remains `draft`/pending human approval. Never inherit approval metadata from a prior outline.

## Freedom test

The outline may make consequential story choices; it must not script every sentence, camera cut or micro-beat. A competent Writer should retain meaningful execution freedom while being able to tell why each movement exists and why reordering/removing it would change the work.
