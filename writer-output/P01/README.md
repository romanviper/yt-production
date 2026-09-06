# P01 Writer Outputs

Use this folder only for Owner-readable Writer outputs.

Partitions:

- `gemini/`
- `sol/`
- `gpt6/`

Each Writer writes only inside its own partition:

- `draft.md` — the prose output
- `meta.json` — minimal metadata (`model`, `inputs`, `attempt`, optional `notes`)

Do not put controller state, plans, budgets, reviews, logs, scratch work, or architecture artifacts here.
