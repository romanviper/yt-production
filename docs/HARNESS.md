# Harness — Hard Boundaries, Creative Ownership

## Decision

The harness protects authority, integrity and truth boundaries. It must not choose the story by hard-coding a taxonomy, section sequence, carrier formula or evaluator-approved style.

## Layer classification

| Concern | Layer | Mechanism |
|---|---|---|
| Product/system authority | HARD | governance + write scope |
| Allowed paths / task lifecycle | HARD | deterministic routing when runtime tasks use it |
| Input freshness / provenance | HARD | hashes, source/claim records, audit trail |
| Historical integrity / evidence ceiling | HARD | sourced boundaries + validation |
| Resource/context limits | HARD | compiler/runtime caps where needed |
| Cross-product creative identity | CONSTITUTION | `system/standards/channel-constitution.md` |
| Research discovery method | CREATIVE/EDITORIAL | research operation + judgement |
| Whole-work route selection | EDITORIAL | research + outline |
| Movement order / structural relationships | OUTLINE | product architecture |
| Local pacing, POV, prose, imagery | WRITER | authorship |
| Listening quality / accumulation | REVIEW | outcome evaluation |

## Canonical creative path

```text
Owner question / work order
  → editorial question + scope
  → exploratory research + route comparison
  → targeted research for selected journey
  → whole-work outline
  → narrative compression
  → product-first review + evidence check
  → Owner reading / approval
```

Full prose is a later task unless explicitly included by the Owner.

A direct Owner work order is sufficient authority for the bounded chain it names. Deterministic approval/state machinery must not invent intermediate creative gates that contradict that authority.

## Prompt composition

Creative agents should receive only what materially helps their decision:

1. short cross-product creative identity;
2. operation objective;
3. product question/scope;
4. source-backed material and boundaries needed for the current decision;
5. prior approved/current architecture only when it is genuinely an input rather than a template to preserve.

Do not leak legacy evaluator rules, old section taxonomies or previous Writer output into a fresh creative pass unless comparison is explicitly requested.

## Research contract

Research is not limited to producing claims for an already-selected route. It must both:

- establish what can be said honestly; and
- discover situations, processes, relationships, voices, texts, objects, disputes and consequences capable of carrying a story.

A route may be reopened when source material does not support it. Source count, claim count and object count are not proxies for narratability.

## Outline contract

Outline owns the whole-work journey. It can decide structural cases, relationships, ordering, dependencies, discovery sequence and information placement when those choices determine the story. It must leave sentence-level execution and local pacing to Writer.

Production sections are implementation units, not a mandatory creative ontology. No validator should require a fixed P01–P08 narrative shape merely because a previous cycle used it.

## Writer contract

Writer receives architecture + material + truth boundary and tells the selected journey as an actual listening work. Explanation, summary, montage, scene, text/object reading, investigation and inference are all valid forms when they advance the journey.

Writer may identify an architecture/material failure instead of compensating with style. It may not silently widen factual/causal claims beyond source support.

## Review contract

Review reads the produced work first. It asks what the listener has to follow, what changes, whether the middle accumulates rather than enumerates, and whether the ending is earned. Historical integrity is checked separately.

Evaluation mechanics are diagnostic, not a creative route generator. Do not build an automatic “cinematic” score or require one storytelling device because it worked once.

Failure routing belongs in `system/standards/outcome-evaluation.md`.

## Authoritative homes

| Concern | Home |
|---|---|
| Router / Owner authority | `AGENTS.md` |
| Whole-work Writer contract | `WRITER.md` |
| Cross-product creative identity | `system/standards/channel-constitution.md` |
| Research operation | `system/operations/research-*.md` |
| Outline operation | `system/operations/outline.md` |
| Outcome/failure routing | `system/standards/outcome-evaluation.md` |
| Product question/scope | product brief |
| Selected journey | product outline |
| Historical material/provenance | product research + source/claim ledgers |
| Runtime integrity | existing scripts/registry/hashes when invoked |

Manually authored behavioral policy should have one home; supporting docs summarize rather than create competing constitutions.

## Current `sumer-writing` reset

Canonical creative inputs are listed in `AGENTS.md`. `products/sumer-writing/02_outline/outline.md` is the human-readable narrative architecture pending Owner review; `writer-output/full-script/narrative-identity-reset-01/compression.md` is the review artifact.

Legacy `outline.json`, overlays, P01-only packets and old approvals remain available for audit/compatibility but cannot override the new route. Synchronize machine artifacts only when a runtime dependency actually requires them, and never carry old `approved_by`/`approved_at` metadata into a new draft.

## Anti-accretion rule

For every new rule ask:

1. Is it required for authority, safety, provenance, historical integrity or deterministic interoperability? → hard-enforce only as narrowly as needed.
2. Is it an observable quality outcome? → evaluate after output.
3. Is it merely one technique for achieving quality? → keep optional.

A reset is proven by changed editorial decisions and changed work, not by the number of framework files modified.