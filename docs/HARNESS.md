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

## Anti-accretion rule

Feedback is absorbed at the smallest valid layer:

- one draft failure → local change request;
- repeated outcome failure → evaluator/rubric;
- stable cross-product identity → constitution;
- safety, authority or integrity requirement → hard boundary.

Never add a global negative writer rule merely because one draft failed.

## Compatibility

Approved outline schema v2/v3 and story-plan v1/v2 remain readable. Any new or revised architecture must use outline v4; any new or revised section design must use story-plan v3. Current plans generate compact narration-pack v2.

## Success criteria

- creative instructions stay under their profile budget;
- writer packets exclude hard-policy and evaluation files;
- no minimum word count can force padding;
- every section is outcome-reviewed before approval;
- three acts remain stable across runtimes while movement/section counts remain adaptive.
