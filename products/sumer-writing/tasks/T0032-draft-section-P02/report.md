# Task Report — T0032-draft-section-P02

## Result

Drafted P02 from scratch for the mission “Vì sao một hệ thống ghi dấu có thể hữu ích ngay cả trước khi nó ghi được một câu nói liên tục?” The section answers through structured relations rather than treating approved claim statements as prose: a concrete Uruk III tablet leads into cases/subcases, non-linear sign placement, repeatable administrative relations, and the qualified writing/proto-writing boundary.

Outputs produced:

- `03_sections/P02/draft.md`
- `03_sections/P02/handoff.md`
- `tasks/T0032-draft-section-P02/report.md`
- `tasks/T0032-draft-section-P02/operator-brief.json`

Draft length before submission: 1,713 whitespace-delimited words, inside the 1,150–1,750 target.

## Packet and authority

- Active task: `T0032-draft-section-P02`
- Authority: `product_agent`
- Operation: `draft_section`
- Packet state on entry: `ready`
- Context packet and manifest were consumed from the paths named by `ACTIVE.json` and the work order.
- Writes were limited to the four `allowed_write_paths`; the evidence adapter separately generated its audit trace at the packet-declared trace path.
- No repository research ledger, narration pack beyond the compiled packet, or unbounded evidence source was opened.

## Evidence retrieval and provenance

The adapter was used for `scope`, `claims`, `sources`, targeted `source` resolution, scoped `search`, and `record`.

Source-level detail recorded before use:

- `SRC-0005`, `pp. 33–50; development of accounting systems`: a representative text's omitted preposition/verb; cases partly resolving ambiguity; fluid graph order; omitted morphology; broader-context dependence; rare phonetic writing; no sharp symbolic/phonological boundary.
- `SRC-0010`, `§§1–3; corpus definition, sign-frequency and genre limits`: non-linear sign arrangement, artificial order introduced by transliteration, and corpus/search choices that affect sign-frequency conclusions.
- `SRC-0023`, P005390 artifact metadata and obverse/reverse text fields: clay material, dimensions, Uruk III date band, administrative genre, undetermined language, uncertain Uruk provenience, two-column organization on each face, numerical and non-numerical signs, and the absence of enough verbal information to settle the transaction.

The draft relies primarily on `CLM-0001`, `CLM-0002`, `CLM-0004`–`CLM-0007`, `CLM-0009`, `CLM-0019`–`CLM-0021`, `CLM-0024`, `CLM-0025`, `CLM-0034`, and `CLM-0042`. No new causal conclusion, contradiction, thesis, or generalization was added to the truth ceiling.

## Creative route

1. Open on P005390 as a bounded physical example whose structure is concrete but whose exact transaction is qualified.
2. Separate sentence completeness from functional usefulness.
3. Explain how quantity, conventional signs, and spatial grouping retain relations without mapping cases directly to spoken syntax.
4. Use modern corpus-analysis limits to separate observable graphic regularity from a guessed reading order.
5. Hold the writing/proto-writing and Sumerian-language questions open while distinguishing proto-cuneiform ductus from mature cuneiform.
6. Exit toward expansion into more kinds of use rather than a single invention threshold.

## Truth-ceiling safeguards

- No invented person, scene, thought, dialogue, or sensory detail.
- No exact transaction assigned to P005390.
- No tax, tribute, receipt, redistribution, or exclusive institutional model inferred.
- No equivalence between cases and spoken syntax.
- No claim that earliest proto-cuneiform securely encoded Sumerian.
- No world-first claim or single invention year.
- No administrative monocause.
- No inference from technical capacity to consistent historical uptake.

## Validation

All packet-declared checks passed before lifecycle submission:

- `scripts/validate.py products/sumer-writing`: `OK`
- `scripts/task.py verify products/sumer-writing T0032-draft-section-P02`: packet fresh and within budget
- `scripts/check_scope.py products/sumer-writing`: scope OK; four allowed artifacts plus the adapter-managed evidence trace changed, with no protected system writes
- `scripts/operator_brief.py validate .../operator-brief.json`: operator brief valid

The task is ready for `scripts/task.py submit`. Submission will stop at `ready_for_review`; no human approval action is included.
