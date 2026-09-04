# Operation — Historical Substrate

## Responsibility

Convert approved evidence authority into a bounded model of the historical world. This operation owns **what historical states, practices, processes, roles, objects, relations and changes the approved evidence supports**. It does not write narration and does not decide how a story should be told.

Historical Substrate sits between Research/Evidence Authority and Outline/Writer.

```text
Evidence Authority
→ Historical Substrate
→ Outline historical territory / change
→ Writer narration
→ Evidence Review
```

## Inputs and authority

Use only the approved claim ledger, reviewed source index and completed research synthesis. Optional material records may increase factual resolution only when they remain inside the same claim/source authority.

Each substrate record must preserve:

- historical-world statement;
- kind (`practice`, `state`, `process`, `relation`, `change`, `object_affordance`, `actor_role`, `constraint`);
- epistemic status;
- time/place scope;
- claim IDs;
- reviewed source references and useful locators;
- limitations / known unknowns.

A record may synthesize several approved claims into one bounded historical proposition. It may not silently widen their truth ceiling.

## Forbidden authority

Historical Substrate is **not** a story plan. Do not add or imply:

- opening, hook or ending;
- carrier or protagonist;
- scene or beat sequence;
- reveal order;
- climax or emotional turn;
- camera language;
- recommended paragraph/order;
- story role or narrative route.

Do not choose an artifact merely because it would make a good opening. An artifact may appear only as historical-world support or object affordance when the evidence supports it.

## Epistemic boundary

Encode uncertainty as metadata/limitations attached to the historical proposition. `unknown` does not mean the eventual narrator must say “we do not know.” `contested` does not require a historiographical aside. Those are authority limits for Writer and Reviewer.

Use:

- `documented` when the historical proposition is directly supported;
- `qualified_inference` when the proposition is supported but requires a stated boundary;
- `bounded_reconstruction` only for ordinary historical operations that remain within approved conditions and do not invent names, dialogue, motives, chronology or causal conclusions.

## Output

Write `01_research/historical-substrate.json` using `scripts/historical_substrate_contract.py` schema version 1.

For a normal new product, set `coverage.mode` to `product` and cover the historical territory needed by the whole outline. A bounded migration may use `section_migration` and explicitly list the sections covered; that partial artifact is not sufficient for creating a new whole-product outline.

Run:

```text
python scripts/historical_substrate.py validate <product>
```

A new outline requires product-complete coverage:

```text
python scripts/historical_substrate.py validate <product> --require-product-complete
```

## Stop conditions

Block instead of filling gaps when:

- a needed historical proposition has no approved claim/source authority;
- the evidence only supports an evidence-state statement, not the historical-world proposition being requested;
- chronology, actor identity, institution, motive or causality would have to be invented;
- a proposed record is actually narrative choreography.
