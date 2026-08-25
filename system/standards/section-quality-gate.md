# Section Production Quality Gate

Evaluation-only; never expose to the writer.

Emit one `schema_version: 1` JSON object between `<!-- production-gate:start -->` and `<!-- production-gate:end -->`.

Hard gates (`status: pass|fail|blocked`):

- `evidence_integrity`: supported and qualified
- `mission_and_exit`: answerable mission, achieved exit
- `adjacent_section_boundary`: complete current job, preserve next
- `one_hearing_narration`: intelligible and retellable once heard

Evidence-adjusted dimensions (integer 1–10):

- `hook_and_audience_promise`
- `historical_progression`
- `causal_clarity`
- `concrete_specificity`
- `narrative_momentum_and_stakes`
- `supported_human_work_orientation`
- `explanatory_economy`
- `spoken_rhythm_and_clarity`
- `ending_payoff_and_transition`

Record `score`, `evidence_scope: full|limited` and `basis`. Score supported opportunity, not volume. Limited evidence never licenses invention. Human/work orientation may score highly without a person or scene when evidence lacks one. Fabrication fails evidence integrity.

Derived verdict: `blocked` for any blocked gate; else `changes_requested` for any failed gate or score below 8; else `pass`. Diagnose the smallest issue set. Do not prescribe benchmark surface style.
