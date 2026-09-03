# FoC-Informed Editorial Architecture — Execution Plan

Status: `ready_for_owner_review`

Recorded: 2026-09-03

Branch base: canonical `main` at `1f22bc0c188e4b4aedc8dd134095277837405561`.

Scope: structural changes to the research → outline → writer → review path. This document does not authorize implementation, regenerate P01, or approve product prose.

## Decision

The harness must give the Writer high-resolution historical material and bounded authorship. It must not give only propositions, and Research must not pre-author a story plan for the Writer to assemble.

The target relationship is:

`source-rich material + truth boundary → Writer-authored nonfiction story`

not:

`ordered claims → illustrated essay`

and not:

`upstream story plan → mechanical prose assembly`.

## FoC audit findings that control the design

The full Sumerians script demonstrates four distinct operations:

1. **Document-led scene:** an artefact, letter, inscription or travel account already supplies an actor, action, place, object and partial sequence. The Writer selects, orders and focalizes it. The Stele of the Vultures is the strongest model.
2. **Representative reconstruction:** archaeology and social evidence are composed into a plausible local experience, such as the walk through Uruk. This is authored texture, not a documented event.
3. **Causal montage:** facts are compressed and arranged so that one pressure appears to produce the next. The causal path is an editorial product even when every component fact is supported.
4. **Speculative fusion:** later legends, contemporary inscriptions, literary texts and modern hypotheses are merged into one continuous biography or scene. The Sargon and Ishbi-Erra passages show the main failure mode.

The architecture should reproduce operations 1–3 under explicit evidence limits and detect operation 4 before publication.

## Current structural defect on `main`

### 1. Evidence is preserved primarily as conclusions

`system/operations/research-workstream.md` permits `materials.json`, but the artifact is optional. P01 has no product-level material ledger and its current evidence handoff is dominated by claim statements, counterevidence and qualifications.

This preserves truth but often discards the raw elements from which a story can be authored: acting subject, documented action, object, place, explicit sequence, unresolved question and later evidence that changes interpretation.

### 2. The outline assigns an intellectual correction

P01's current `narrative_job`, entry state and exit state are framed mainly as misconception → corrected model. That gives the Writer a proposition to prove. A prompt that later asks for cinematic prose cannot reliably reverse this upstream essay logic.

### 3. The Writer is primed by a compact claim brief

The canonical path requires `resolve_claims` before drafting. The returned brief begins with abstractions and red lines, so the first coherent structure available to the model is an argument. Optional retrieval cannot solve this when the Writer has not first received enough concrete material to know what to search for.

### 4. Reconstruction permission is present but not operationally complete

`creative-boundaries.md` distinguishes evidence-bound narration from `representative_fiction`, but product artifacts and review do not yet carry a consistent source-ontology check. A Writer can therefore either retreat to essay mode or create a generic illustrative incident whose historical status is difficult to audit.

### 5. Evidence review does not explicitly test source distance

The current evidence gate checks support and honest reconstruction, but it does not require an explicit test for contemporary record versus later literary copy, royal propaganda, cultural memory or modern hypothesis. FoC's largest errors occur at exactly this boundary.

## Target architecture

### A. Research preserves unordered story affordances

Keep claims and sources as truth authority. Add or strengthen a compact evidence-preservation record only when source-level detail would otherwise disappear.

A material record should be able to retain:

- `kind` and a neutral label;
- linked claim and source IDs with narrow locators;
- actor, acting system, object or trace when directly supported;
- documented action or explicit source sequence;
- time, place, physical description, measurement or spatial relation;
- unresolved question or later evidence that changes an interpretation;
- source relation to the event: contemporary material, contemporary interested account, later copy, retrospective literature, cultural tradition or modern hypothesis;
- limitations and representativeness.

These fields are evidence observations. They must not assign an opening, focal carrier, reversal, climax, ending, emotional beat or narrative route. Do not introduce a narratability score.

### B. Add an evidence-resolution preflight, not a story-planning stage

Before a story-first draft, the evidence broker should determine whether the bounded section territory exposes usable actions, objects, places, sequences or evidence transitions.

- If usable material exists, expose it unordered through bounded search/source capabilities.
- If it does not exist but may be recoverable from already approved sources, route one `evidence_resolution` task.
- If the approved sources cannot support a nonfiction movement, stop for an owner decision instead of manufacturing a historical incident.

No `story-plan.json` stage should be restored.

### C. Change Writer priming from claims-first to material discovery

Replace the mandatory content dump from `resolve_claims` with a scope attestation that confirms the truth ceiling without presenting an ordered argument.

The Writer should then be able to:

1. search bounded evidence for people, objects, actions, places, sequences and interpretive changes;
2. open only relevant approved source records and preserved details;
3. choose its own focal carrier and ordering;
4. consult claim boundaries and red lines as constraints, not as the draft's default sequence;
5. record any retrieved factual detail through the existing audit trace.

Claims remain authoritative and fully available to Reviewer/evidence checks. This change affects priming, not the truth ceiling.

### D. Make the outline own historical movement without pre-authoring prose

Do not add another artifact layer. Reuse the existing section contract, but require `narrative_job`, `entry_state` and `exit_state` to describe a supported change that can be followed through historical reality, not merely a belief to rebut or a conclusion to explain.

The section mission becomes meaning the story must earn. It is not a thesis the opening must announce and defend.

An outline review must be able to answer:

- What changes in the historical world or in the surviving evidence?
- What concrete material inside the approved territory could let an audience follow that change?
- Does the next section become necessary because of what changed?

The outline must not prescribe camera, scene, character, beat order or reveal sequence.

### E. Use one reconstruction model across Writer and Reviewer

Keep three internal truth layers:

1. **Documented fact:** assertion maps to reviewed evidence and preserves qualification.
2. **Qualified inference:** uncertainty remains visible and cannot become fact through confident prose.
3. **Representative reconstruction:** plausible ordinary particulars may embody approved conditions, but cannot establish a new practice, institution, technology, chronology, measurement, motive, causal conclusion or unique historical outcome.

Private thoughts, dialogue, secret plans, emotional motives and named local incidents require direct support or an explicitly authorized fiction mode. Natural language may signal a composite once; the narration should not expose internal evidence machinery.

### F. Extend evidence review to editorial transformations

Add deterministic contract coverage and reviewer guidance for:

- source genre and temporal distance from the narrated event;
- later literary copy presented as contemporary testimony;
- propaganda presented as neutral report;
- multiple centuries compressed into one representative scene;
- correlation converted into sole or inevitable causation;
- invented motive, dialogue, plan or private thought;
- a representative reconstruction used as proof of the section's conclusion.

Review should distinguish a false factual assertion from a permissible authored transition. It should not require every connective detail to have an archival witness.

## P01 migration after the system change

Keep system and product changes in separate commits.

1. Run one bounded evidence-resolution task over P01's already approved sources.
2. Preserve actual objects, documented actions, locators, physical details, source sequences and source-distance limitations in the material handoff.
3. Rework P01's outline contract so it offers a historical movement rather than a misconception rebuttal; stop for owner approval.
4. Generate one fresh noncanonical 450–650 word excerpt. Do not expose old drafts, FoC prose, evaluator language or a prescribed scene.
5. Human-check only whether a story was followed, what changed, whether its meaning emerged, and whether reconstruction remained distinguishable from documented fact.
6. A pass authorizes one full P01 draft. It does not approve P01 or prove the harness reusable.

The existing fictional warehouse-transfer checkpoint is a negative control: it has scene shape, but most of its movement was supplied by the requested illustrative scenario rather than discovered from source material.

## Proposed implementation commits

After owner approval, execute in this order:

1. **Evidence contract and broker:** material/source ontology, bounded discovery, evidence-resolution routing and tests.
2. **Outline, Writer and Review contracts:** story-primary objective, non-essay outline responsibility, unified reconstruction rules and editorial-transformation checks.
3. **P01 evidence migration:** product-only evidence-resolution output and provenance.
4. **P01 outline amendment:** product-only, followed by explicit human approval.
5. **Single P01 probe:** noncanonical output and a blind owner decision.

Do not combine protected system changes with product content in one commit. Do not cherry-pick the experimental branch wholesale; reconcile each change against current `main` and this plan.

## Acceptance criteria

The structural change passes only when:

- a Writer packet no longer presents an ordered proposition list as its first usable content;
- an evidence-rich section exposes at least one real object, action, sequence or evidence transition without preselecting a story route;
- absence of usable material routes to evidence resolution or a blocker, not generic invented drama;
- a listener can retell what was followed and what changed, not only repeat the conclusion;
- every unique historical action, motive or causal assertion has appropriate evidence;
- later literature, propaganda and hypotheses cannot silently masquerade as eyewitness fact;
- representative reconstruction can add movement and texture without widening the truth ceiling;
- no story-plan stage, beat quota, benchmark imitation or lexical style formula is introduced;
- existing authority, packet isolation, provenance, human approval and bounded retrieval remain intact.

## Validation

For every implementation commit:

```text
python -m unittest discover -s tests
python scripts/validate.py products/sumer-writing
git diff --check
git status --short --branch
```

Add focused positive and negative fixtures:

- positive: a source-rich artefact sequence can support authored narration;
- positive: a signaled representative reconstruction adds no new historical claim;
- negative: claims-only input attempts to draft without material resolution;
- negative: a later school copy is presented as a live dispatch;
- negative: heterogeneous legends are fused into an unqualified biography;
- negative: a reconstructed incident is used as evidence for the conclusion.

## Stop conditions

Stop before implementation or drafting when:

- the proposal starts assigning story routes upstream;
- the schema expands without changing Writer input or reviewer observability;
- P01 requires evidence outside its approved ceiling;
- a representative scene needs a new practice, chronology, motive or causal conclusion;
- system and product changes cannot be separated;
- the first probe remains essay-like despite adequate material, indicating an objective/model problem rather than another missing rule.

Owner decision required: approve, amend or reject this plan before structural implementation.
