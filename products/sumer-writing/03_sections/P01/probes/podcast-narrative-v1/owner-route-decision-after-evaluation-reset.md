# P01 Podcast Narrative Probe v1 — Owner Route Decision After Evaluation Reset

Status: `AUTHORIZED_EDITORIAL_REVISION_EXPERIMENT`

Decision authority: owner-requested continuation after evaluation-loop reset at commit `20c229a83c472bcc820d0be145f1499bbcc8012b`.

## Decision

Do **not** run another fresh Writer sampling round.

Authorize one bounded **same-draft editorial revision experiment** using **Passage Beta / Round 1** as the revision base.

This is not an endorsement of Beta as historically acceptable. Beta is selected because the blind product review identified the strongest listener pull in the batch, while the separate truth audit identified exactly why that pull is unsafe: it relies on invented anti-tampering motive, an illicit token→envelope→tablet causal bridge, and overstrong claims about exterior impressions.

The experiment question is:

> Can an already compelling draft be editorially revised so that it preserves listener pull while removing unsupported causality and truth overreach, without collapsing back into museum-guide or textbook prose?

This tests editorial convergence. It is intentionally different from the previous loop of repeatedly sampling fresh Writers from increasingly constrained prompts.

## Corrections to the evaluation reset before execution

The Stage A/B/C artifacts at `20c229a...` are useful but not treated as flawless authority.

### 1. Product benchmark purity

The approved craft benchmark remains the repository-approved *Fall of Civilizations* benchmark and the product brief. Product-editor observations that depend on any unapproved added benchmark (for example *Hardcore History*) must not be compiled into the Writer task as authority.

### 2. Truth-audit authority purity

The truth repair card may use only claims supported by the approved P01 notebook / notebook-authority and their already-bound research authority. Do not carry forward auditor-added external details such as CT-radiography or rattling counters unless separately authorized by the bound source material.

### 3. Material blocker remains unverified

Do not state that the envelope-only material *cannot* support the target product. The supported observation is narrower:

> None of the tested Writer/task configurations produced a high-quality 700–900-word envelope-only passage.

Material insufficiency remains a competing hypothesis, not a settled diagnosis.

### 4. Do not pre-author a replacement causal story

Do not inject phrases such as “memory crisis”, “urban pressure caused writing”, “temple bureaucracy required writing”, or similar causal explanations merely because they create stakes. If a later route needs wider historical stakes, those stakes must first be supported by approved research authority.

## Revision base

Use the preserved Round 1 / Passage Beta text as the base draft. Do not regenerate the passage from scratch before revision.

The revision agent must be able to see:

1. the base draft itself;
2. a compact **product-editor note** derived from the product-only review;
3. a compact **truth-repair card** derived only from approved authority;
4. the existing prose-facing historical notebook when factual grounding is needed.

Do not give the reviser the full accumulated reviewer history, all previous probe outputs, architecture discussion, or competitor prose.

If the exact same model/session instance that authored Beta is operationally unavailable, use a dedicated revision agent with the base draft explicitly supplied. The key variable is **revision of an existing authored draft**, not fresh one-shot resampling.

## Product-editor note for revision

This note is positive and product-facing. Do not turn it into a long prohibition list.

Preserve what made Beta the strongest listening product in the batch:

- immediate placement in Late Uruk Mesopotamia and an administrative world;
- concrete hand-scale clay material;
- a clear sense that information is becoming physically externalized;
- progression that carries the listener beyond a static envelope demonstration;
- an unfinished horizon toward the larger history of writing.

Improve the product by making the listener feel a wider historical world than a pottery demonstration. Meaning and consequence should arise from evidence-supported historical context, not invented drama. The passage should still create a reason to continue listening after the local clay operation is understood.

Do **not** prescribe a hook formula, protagonist, scene beats, climax, sensory quota, ruins motif, or benchmark imitation.

## Truth-repair card for revision

The following repairs are mandatory because they are directly supported by the existing truth audit and notebook authority:

1. Remove the invented setup in which loose counters on a table/basket are vulnerable to someone adding or removing pieces, and remove the implied conclusion that this vulnerability caused envelopes to appear.
2. Remove the rhetorical bridge implying that exterior marks made enclosed counters unnecessary and therefore led to solid numerical tablets.
3. Introduce envelopes, exterior impressions, and numerical tablets as attested overlapping Late Uruk practices / material arrangements unless approved authority supports a stronger relationship.
4. Qualify exterior-impression claims: on **some** envelopes they can make information about enclosed quantity inspectable; do not claim universal exact one-to-one correspondence of quantity and shape.
5. Do not invent named actors, private motives, undocumented transactions, universal anti-fraud purpose, or a single invention event.
6. Do not use a late disclaimer to neutralize a causal genealogy already enacted by the prose. The narration itself must remain within the evidence ceiling.

Apply these constraints silently where possible. Do not convert the revision into a recital of historiographical caveats.

## Revision method

The reviser may substantially rewrite sentences, paragraph order, transitions, and local composition. This is an editorial revision, not a line-edit-only task.

However:

- keep the same broad P01 territory;
- retain the useful material richness of the notebook;
- do not add new factual authority;
- do not add a new upstream story plan authored by the reviewer;
- do not modify canonical architecture, Historical Substrate, schemas, runtime, or CI;
- do not create another fresh Writer variant in parallel.

Target roughly the same passage scale as the existing experiment; do not optimize mechanically for exact word count if doing so harms the prose.

## Required outputs

Create a new experiment-local revision directory or clearly versioned files that preserve the original Beta unchanged.

At minimum produce:

- `revision-brief.md` — the compact Writer-facing revision packet actually used;
- `revised-probe.md` — the revised passage;
- `revision-report.md` — execution metadata only: base-draft identifier, model/config/run identity if available, input files, output word count, and confirmation that no competitor prose or unrelated feedback entered the revision context.

Do not overwrite the original Round 1 evidence needed for comparison.

## Evaluation after revision

Evaluate the revised passage in this order:

1. **Cold product review first** against the absolute product bar. Do not compare it to the old draft until the absolute verdict is frozen.
2. **Separate truth audit second** against approved P01 authority.
3. Only then compare old Beta vs revised Beta to answer whether editorial revision produced real convergence.

The revision succeeds only if both are true:

- product quality remains at least genuinely near the target rather than collapsing into explanatory/museum prose;
- hard truth violations in the original Beta are removed.

A safer but substantially less compelling rewrite is not success. A compelling rewrite that retains false causality is not success.

## Stop condition

Run exactly one editorial revision experiment from Beta, preserve the raw result, perform the two-stage review, and stop for owner review.

Do not widen the evidence route, create a new architecture, or launch another fresh Writer until this revision experiment has been evaluated.
