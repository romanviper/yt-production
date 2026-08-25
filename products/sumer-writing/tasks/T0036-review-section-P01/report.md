# Task report — T0036-review-section-P01

## Result

- Operation: `review_section`
- Section: `P01`
- Review contract: v3
- Derived verdict: `pass`
- Hard gates: 4/4 pass
- Dimension scores: 9, 9, 9, 9, 8, 8, 8, 9, 9
- Scores below 8: none
- Blockers: none

Both required outcome questions are affirmative. After one hearing, the audience can answer why durable clay-surface signs became useful and can retell the material-historical path from token and bulla through exterior marks and numerical tablets to an overlapping recording ecology under institutional pressure.

## Authority and scope followed

The review used only `ACTIVE.json`, this task's `work-order.json`, the single compiled `context.md` packet, and the packet-declared bounded evidence broker. No repository scan or prior review/output reading was used. Writes were limited to the three work-order allowlisted paths.

The work order identifies `bounded_claim_sources` evidence access with interface version 1. `resolve_claims` completed successfully for `CLM-0011` through `CLM-0018`, preserving the truth ceiling and resolving six approved sources: `SRC-0001`, `SRC-0003`, `SRC-0005`, `SRC-0009`, `SRC-0010`, and `SRC-0011`.

## Evidence checks

The packet did not include a receipt projection, so approved source locators were checked only where needed to resolve concrete draft details. Added source-level details were recorded through the broker before being relied upon.

- `SRC-0001`, p. 25: directly supports the draft's Uruk estimate of about 200 hectares and a population approaching 40,000 or more. The draft explicitly labels both numbers estimates. This resolves the apparent precision concern.
- `SRC-0005`, pp. 45–46: supports that some envelopes bear exterior token impressions and that exterior/interior matches apply only in some cases. The draft preserves that limitation and does not universalize exact matching.
- `SRC-0011`, p. 8: supports coexistence of tokens with written documents at Tushan and the point that writing did not simply supersede earlier information-storage practices.
- `CLM-0011` and `CLM-0012`: the draft correctly makes numerical practice the strongest continuity while rejecting a universal millennia-long token code.
- `CLM-0013`: the draft explicitly labels token → bulla → tablet as a material logic rather than a deterministic replacement chronology and presents seals, iconography, bullae, numerical tablets, and institutional practice as a parallel ecology.
- `CLM-0014`, `CLM-0015`, and `CLM-0018`: administrative scale remains a major pressure, not a sole cause. The feedback formulation is marked as a conditional model rather than a completed causal verdict.
- `CLM-0016` and `CLM-0017`: the preserved corpus is described as strongly accounting/administrative without relabeling market exchange, tax, tribute, redistribution, labor, obligation, or ownership as interchangeable mechanisms.

An approved comparative synthesis (`SRC-0005`) gives a different urban estimate from `SRC-0001`; that variation does not create a draft contradiction because the draft uses the exact approved `SRC-0001` estimate and explicitly signals estimate status.

## Outcome diagnosis

Mission answerability passes because the bulla inside/outside problem establishes the practical need before the final answer names the three linked values: scale raises pressure, surface access makes quantity inspectable, and durability lets work continue.

Historical progression passes because each physical operation changes where quantity can be found and processed. The audience receives the relevant sequence before the ecology interpretation, while the narration prevents that sequence from becoming an asserted universal genealogy.

The required exit state is achieved: the listener leaves with numerical practices, seals/bullae/tablets, and institutional demand as an ecology; administration is not monocausal. The adjacent boundary passes because P01 does not explain structured sign/layout operation, the writing threshold, or language attribution, leaving the approved P02 job intact.

## Production-gate basis

- `hook_and_audience_promise` 9: the bulla paradox opens a concrete information problem.
- `historical_progression` 9: operations form a retellable path without linear replacement.
- `causal_clarity` 9: material affordances and institutional pressure remain distinct.
- `concrete_specificity` 9: objects and actions make the thesis tangible.
- `narrative_momentum_and_stakes` 8: expanding record-handling pressure sustains practical stakes.
- `supported_human_work_orientation` 8: counting, transfer, sealing, marking, and later processing remain visible.
- `explanatory_economy` 8: repetition adds function rather than inventory.
- `spoken_rhythm_and_clarity` 9: varied sentence forms remain clear in spoken Vietnamese.
- `ending_payoff_and_transition` 9: the mnemonic answer lands and opens the exact next question.

No material issue requires revision. Per contract, `pass` makes P01 eligible for human approval only.

## Validation and operational notes

- `resolve_claims`: pass after rerunning the broker with UTF-8 console mode; all eight claims resolved.
- Source-detail recording: pass for the four audited details used in evaluation.
- `python scripts/task.py brief ...`: pass through the available `uv run python -X utf8` runtime; canonical v1 brief renders successfully.
- Official task verification: pass; `task.py verify` reports the packet fresh and within budget.
- Contract-v3 structural validation: pass; 628 words, exact H1/verdict/H2 order, one marker pair, schema version 1, four exact hard gates, nine exact dimensions, valid basis lengths, and derived verdict `pass`.
- Task submission: not run.
- Section approval: not run.
- Git commit: not run.

Initial direct `python`/`py` launches were unavailable, and the first broker serialization attempt hit Windows cp1252 on a right-arrow character. Running the same declared adapter through `uv run python -X utf8` resolved the environment issue without changing evidence scope.
