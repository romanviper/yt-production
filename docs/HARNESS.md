# Harness v3 — Hard Boundaries, Soft Logic

## Decision

The harness controls what must never happen and what outcome must be reviewed. It does not prescribe the creative path between them.

## Layer classification

| Concern | Layer | Mechanism |
|---|---|---|
| Product/system authority | HARD | governance and scope checker |
| Allowed write paths | HARD | router-generated work order |
| Task state and human approval | HARD | preconditions and approval commands |
| Input freshness/context integrity | HARD | hashes and packet schema |
| Evidence provenance/narration ceiling | HARD | ledgers, evidence roles and narration-pack hashes |
| Context/instruction/section caps | HARD | compiler and validators |
| Global three-act identity | CONSTITUTION | schema v4 plus Channel Constitution |
| Opening form, order, beats, paragraphs, cadence | SOFT | Agent judgement |
| Target word range | SOFT ESTIMATE | planning and evaluation; not submit quota |
| Voice, causal motion, semantic repetition | EVAL-ONLY | outcome review |
| Failure ownership | EVAL-ONLY | prose/design/architecture/evidence routing |

## Prompt composition

Creative prompts may contain only:

1. four short content boundaries;
2. Channel Constitution;
3. one short operation objective;
4. product/local material needed for the current decision.

`system/harness.json` blocks hard-policy and eval-only files from leaking into writer prompts and limits instruction tokens independently from total context tokens. Operator-interface is validated outside the creative context.

Operation inputs are compact and hash-bound. Outline design receives a deterministic claim catalog instead of the full claim ledger; drafting receives the approved narration pack instead of the full section evidence archive. Detailed provenance remains authoritative outside the creative prompt.

## Authoritative homes

This document explains the layout; it is not another policy source.

| Concern | Authoritative home |
|---|---|
| Authority, write scope and task lifecycle | `AGENTS.md` plus deterministic scripts |
| Context profiles, caps and layer allowlists | `system/harness.json` |
| Content safety and evidence ceiling | `system/core/creative-boundaries.md` |
| Three-act identity, voice and channel values | `system/standards/channel-constitution.md` |
| One operation's reasoning problem | its file in `system/operations/` |
| Outcome criteria and failure routing | `system/standards/outcome-evaluation.md` |
| Machine routing, inputs and outputs | `system/operations/registry.json` |
| Product decisions and feedback | product artifacts and local change requests |

Generated hashes, allowed paths and validation commands may repeat across router artifacts because they enforce integrity. Manually authored behavioral prose must have one home.

## Anti-accretion rule

Feedback is absorbed at the smallest valid layer:

- one draft failure → local change request;
- repeated outcome failure → evaluator/rubric;
- stable cross-product identity → constitution;
- safety, authority or integrity requirement → hard boundary.

Never add a global negative writer rule merely because one draft failed.

## Compatibility

Approved outline schema v2/v3, story-plan v1/v2 and packet v1-v3 remain readable. New output uses outline v4, story-plan v3, compact narration-pack v2 and packet v4.

## Success criteria

- creative instructions stay under their profile budget;
- writer packets exclude hard-policy and evaluation files;
- registry entries contain routing data rather than creative acceptance prose;
- no minimum word count can force padding;
- every section is outcome-reviewed before approval;
- three acts remain stable across runtimes while movement/section counts remain adaptive.
