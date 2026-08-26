# Harness v3 — Hard Boundaries, Soft Logic

## Decision

The harness controls what must never happen and what outcome must be reviewed. It does not prescribe the creative path between them.

## Layer classification

| Concern | Layer | Mechanism |
|---|---|---|
| Product/system authority | HARD | governance and scope checker |
| Allowed write paths | HARD | router-generated work order |
| Task state and human approval | HARD | preconditions and approval commands |
| Human-directed creative edits | HARD | explicit user request, output allowlist, validators and amendment log |
| Input freshness/context integrity | HARD | hashes and packet schema |
| Evidence provenance/narration ceiling | HARD | ledgers, evidence roles and narration-pack hashes |
| Context/instruction/section caps | HARD | compiler and validators |
| Global three-act identity | CONSTITUTION | schema v4 plus Channel Constitution |
| Opening form, order, beats, paragraphs, cadence | SOFT | Agent judgement |
| Target word range | SOFT ESTIMATE | planning and evaluation; not submit quota |
| Voice, causal motion, semantic repetition | EVAL-ONLY | outcome review |
| Failure ownership | EVAL-ONLY | prose/design/architecture/evidence routing |

## Prompt composition

Canonical creative prompts may contain only:

1. short content boundaries and positive authorship ground;
2. Channel Constitution;
3. one short operation objective;
4. product/local material needed for the current decision.

`system/harness.json` blocks hard-policy and eval-only files from leaking into writer prompts and limits instruction tokens independently from total context tokens. Operator-interface is validated outside the creative context.

Operation inputs are compact and hash-bound. Outline design receives a deterministic claim catalog instead of the full claim ledger; drafting receives the approved narration pack instead of the full section evidence archive. Detailed provenance remains authoritative outside the creative prompt.

Non-canonical excerpt calibration uses `scripts/excerpt_packet.py`, not `draft_section`. Its packet binds the product language, approved section and narration/evidence hashes but projects only a local job, local stopping rule, excerpt word range and one to three selected in-scope claims. It omits the full section exit state and cannot write, submit or approve product artifacts.

The Ken Follett/Kingsbridge literary compass in `draft-excerpt` is a reference experiment scoped only to non-canonical probes. It is not a canonical channel style and must not enter `draft_section` or be promoted without human comparison of the resulting prose.

Excerpt probes default to `evidence_bound`. An explicit `representative_fiction` mode lets the writer invent a composite protagonist, local stakes, connective events and focal movement while the selected claims remain the historical world boundary rather than a plot outline. This permission is recorded in the compiled packet and does not alter canonical `draft_section` behavior.

## Outline execution-runtime POC

`outline` may be compiled explicitly with `--runtime dsh`. This changes only the execution path:

- the Python router still owns preconditions, work order, hashes, write scope, validators, submission and human approval;
- product artifacts keep the same outline/story-bible/voice-profile contracts and contain no DSH fields;
- `context.md` becomes a minimal seed containing bounded operation instructions, not product facts;
- DSH runs headless in an empty temporary workspace with telemetry disabled;
- a Cordis overlay disables filesystem, shell, code, web, skill, workflow and subagent tools, then inserts one `yt_outline` MCP broker;
- the runner accepts only the audited `0.1.0-rc.5` CLI and preflights the fully composed Cordis config before any model call; a version or row mismatch fails closed;
- the broker reads only packet-declared inputs and current declared outputs, enforces fresh hashes and exact write paths, and records every returned context/evidence payload in `runtime-trace.jsonl`;
- `validate` and `submit` delegate to the existing deterministic Python control plane.

The capability interface is versioned independently of product schemas: `get_task_state`, `get_product_direction`, `get_research_summary`, `search_evidence`, `get_claims`, `get_benchmark`, `get_current_outline`, `write_outputs`, `validate`, `submit`.

DSH remains opt-in because v0.1 is a developer preview. A DSH upgrade requires re-auditing the base/headless rows, updating `TESTED_DSH_VERSION` and rerunning the boundary tests. Omitting `--runtime` preserves the precompiled-context harness. Rollback requires no artifact migration: cancel/replace the task and create `outline` again with `--runtime legacy`, or remove the adapter and the two runtime routing fields from the outline registry entry.

## Authoritative homes

This document explains the layout; it is not another policy source.

| Concern | Authoritative home |
|---|---|
| Authority, write scope and task lifecycle | `AGENTS.md` plus deterministic scripts |
| Context profiles, caps and layer allowlists | `system/harness.json` |
| Content safety and evidence ceiling | `system/core/creative-boundaries.md` |
| Three-act identity, voice and channel values | `system/standards/channel-constitution.md` |
| One operation's reasoning problem | its file in `system/operations/` |
| Non-canonical excerpt compilation | `scripts/excerpt_packet.py` plus `system/operations/draft-excerpt.md` |
| Outcome criteria and failure routing | `system/standards/outcome-evaluation.md` |
| Machine routing, inputs and outputs | `system/operations/registry.json` |
| Optional outline runtime boundary and audit trace | `scripts/outline_runtime.py` plus the task packet |
| Product decisions and feedback | product artifacts and local change requests |
| Direct human amendments | `scripts/approval.py` and product-local `human-amendments.jsonl` |

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
- every AI-authored section is outcome-reviewed before approval, unless the user directly edits or explicitly accepts a bounded amendment;
- three acts remain stable across runtimes while movement/section counts remain adaptive.
