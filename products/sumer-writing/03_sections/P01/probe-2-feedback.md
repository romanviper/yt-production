# Probe 2 correction feedback — P01

Status: `changes_requested_before_probe_2_writer_task`

Reviewed branch: `codex/foc-editorial-probe2-corrections`

Reviewed commit: `3d8be1d10cd10abb770e474eb4a71fc973782e90`

## Decision

Do not create the Probe 2 Writer task yet.

The correction branch moves in the right direction and successfully removes two major sources of thesis priming:

- `historical_change` is now framed as an observable/evidentiary transition rather than an explicit inadequacy→solution story;
- `earned_meaning` is no longer projected into Writer-facing draft/excerpt context.

The branch also correctly marks Probe 1 as rejected and the old review as stale/non-authoritative.

However, the new epistemic material model is not yet closed. A Writer created from the current branch could still receive causal/reconstructed content through fields that appear factual, or be primed by rejected causal hypotheses. That would make Probe 2 an invalid experiment because we would not know whether essay-like output came from Writer behavior or from contradictory upstream authority.

## Finding 1 — P1 blocker: top-level factual fields still bypass the epistemic layers

`materials.json` now adds `epistemic_layers`, but several records still duplicate inferred or reconstructed activity into legacy top-level fields such as `documented_action`.

Examples:

- `P01-MAT-0004` labels the record-maker workflow as `representative_reconstruction`, but the top-level `documented_action` still states the shaping, stylus pressing and seal rolling as if they were documented actions.
- `P01-MAT-0005` similarly places a multi-step recording workflow in a top-level `documented_action` while its epistemic layer correctly calls the workflow representative reconstruction.

This is not only a schema cleanliness issue. `draft_evidence.py` exposes preserved material fields and now also exposes `epistemic_layers`. The Writer can therefore receive two conflicting signals for the same content:

```text
legacy field: documented_action → appears factual
new layer: representative_reconstruction → explicitly reconstructed
```

The more permissive legacy field can still dominate model behavior.

### Required correction

For schema v2 materials, make the authority unambiguous.

Preferred rule:

- top-level factual affordance fields contain only directly/materially attested observations;
- inferred function exists only under `functional_inference`;
- composite or reconstructed workflow exists only under `representative_reconstruction`;
- causal synthesis exists only in a qualified interpretation/constraint channel.

If a complete action or sequence is reconstructed from artifact morphology, remove it from `documented_action` / `explicit_sequence` rather than duplicating it there.

Add a negative test proving that a schema-v2 material cannot expose the same workflow as both documented fact and representative reconstruction.

## Finding 2 — P1 blocker: rejected causal hypotheses are now Writer-visible material

The branch adds `interpretive_hypothesis` and then forwards `epistemic_layers` through the Writer evidence broker.

Some entries in `interpretive_hypothesis` are not live hypotheses the Writer may responsibly develop. They are specifically the interpretations this architecture is trying to prevent, for example:

- bullae emerged specifically to prevent fraud or solve verification at distance;
- numerical tablets were a necessary direct step toward proto-cuneiform;
- a reconstructed ration workflow proves redistribution caused writing to emerge.

Even when accompanied by a qualification saying the proposition is unsupported or contested, presenting the causal proposition itself inside Writer material creates exactly the priming path Probe 2 is supposed to remove.

### Required correction

Separate **usable interpretation** from **forbidden/rejected interpretation**.

A suitable model would be conceptually:

```text
observed
functional_inference
representative_reconstruction
qualified_live_hypothesis
prohibited_or_rejected_inference
```

The exact names are flexible, but the Writer broker must not treat a rejected causal claim as ordinary story material.

Recommended routing:

- Writer retrieval: observed material + qualified functional inference + clearly signaled reconstruction permission + any genuinely approved live hypothesis;
- Writer constraint/red-line surface: concise prohibited inference or limitation;
- Reviewer: full epistemic record, including rejected alternatives and source-distance warnings.

Do not make rejected thesis language discoverable as a positive material affordance.

Add a broker test proving that a rejected causal interpretation cannot appear in Writer search/source results as ordinary usable content.

## Finding 3 — P1 contract weakness: `historical_change` semantic validation is still lexical and currently lets thesis-shaped changes pass

`validate_historical_change_semantics()` only rejects a change when an inadequacy keyword is found in `from` and a solution keyword is found in `to`.

That is too easy to bypass and one of the tests demonstrates the problem. `test_valid_historical_change_passes_outline_contract` still treats this as valid:

```text
from: Kế toán bằng token đất sét rời rạc không thể theo kịp quy mô đô thị hóa

to: Tập hợp các ký hiệu số và dấu ấn hình thành hệ thống lưu trữ ngoại thân đầu tiên
```

Semantically this is still inadequacy → replacement/capability, which is the exact structure Probe 1 followed. It passes only because the `to` string does not contain one of the small solution-marker tokens.

### Required correction

Do not rely on the current keyword pair as if it proves semantic route-neutrality.

At minimum:

1. change the supposedly valid test above into a negative fixture;
2. keep the current P01 observable movement as the positive fixture;
3. add English and Vietnamese negative fixtures that express problem→solution without using `therefore`, `allowing`, `cho phép`, etc.;
4. document that deterministic validation is a guardrail, while the owner checkpoint remains the authority for semantic route-neutrality.

If the contract can be made structurally stronger without adding story planning, prefer observable-state fields over increasingly long lexical blacklists.

## Finding 4 — P2: `earned_meaning` is correctly hidden from Writer, but it remains an unsafe Reviewer target

Removing `earned_meaning` from Writer-facing context is a strong correction and should remain.

However, P01 still stores:

> Chữ viết ban đầu không phải là một nỗ lực ghi lại lời nói, mà là một công nghệ vật chất để neo giữ các cam kết thực tế khi trí nhớ con người không còn gánh nổi.

The last clause — `khi trí nhớ con người không còn gánh nổi` — is the same explanatory pressure that Probe 1 converted into a causal essay. The current material territory does not directly establish a historical moment in which memory failed and writing emerged as its solution.

Because `earned_meaning` remains an owner/reviewer evaluation target, a Reviewer can still reward or demand the unsupported thesis even though Writer never saw it.

### Required correction

Rewrite `earned_meaning` into an evidence-bounded insight, or explicitly demote it to a non-binding owner hypothesis.

A safer target would describe what the surviving evidence permits the audience to learn without asserting the cause of emergence, for example:

```text
Late-Uruk recording did not begin as one sudden invention event: numerical and authentication information was already being materialized across several clay practices, including durable surfaces that could remain inspectable after the immediate transaction.
```

Do not require this exact wording. Preserve the distinction:

```text
historical observation → permitted earned insight
not
historical observation → preselected causal verdict
```

## Finding 5 — P2 process hygiene: stale review still contains a live-looking `Verdict: pass`

The branch correctly adds `Status: stale_mismatched_non_authoritative` and records the binding error in `section.json`.

That is good provenance handling.

But the archived file still contains a normal-looking `Verdict: pass` and a complete passing production-gate block. Any future human or tool that reads the Markdown without respecting the new status metadata can misread it as current authority.

### Required correction

Preserve the old review for provenance but make its archived nature impossible to mistake.

For example:

- change `Verdict: pass` to `Original verdict (invalidated): pass`; and/or
- place the old production-gate content under an explicit archived/non-authoritative section;
- add a test or lifecycle guard that stale/mismatched review provenance can never satisfy a current review/approval gate.

Do not delete the historical artifact.

## What is already correct and should not be reopened

Keep these decisions unless a correctness failure requires otherwise:

1. The current P01 `historical_change` wording is substantially better:

```text
From: evidence preserves quantity/authentication across several clay media/practices.
To: numerical information increasingly appears directly on durable clay surfaces beside authentication marks.
```

This is an observable movement rather than a causal invention theory.

2. Keep `earned_meaning` out of Writer-facing draft and excerpt packets.

3. Keep inferred actors explicitly unknown/inferred rather than silently naming clerks, storekeepers or transacting parties as documented historical actors.

4. Keep representativeness bounded to the cited corpus/context; do not restore `universal`, `standard`, or `canonical` unless directly justified.

5. Keep Probe 1 rejected and preserved as a diagnostic artifact.

6. Do not create a new Writer task before regenerating a fresh material snapshot after the final material corrections.

7. Do not add new style rules, scene rules, carrier rules, pacing formulas or FoC-derived choreography to `draft-section.md` in this round.

## Experimental-control instruction for Probe 2

Do not broaden the correction round unnecessarily.

The purpose of Probe 2 is to test whether removing thesis priming from historical movement and material authority changes Writer behavior.

Therefore, after the blockers above are fixed:

1. rerun validation/tests;
2. update the P01 owner checkpoint;
3. obtain owner approval of the evidence territory and observable movement;
4. generate a fresh immutable material snapshot;
5. create a completely fresh Writer task;
6. keep old Probe 1 prose, stale review, FoC analysis, architecture diagnosis and this feedback out of Writer context;
7. use the same contiguous 450–650 word probe form so Probe 1 and Probe 2 remain meaningfully comparable.

Do not change the Writer prompt or add a third architectural theory before seeing Probe 2 unless one of the corrections above requires it for epistemic correctness.

## Probe 2 evaluation after generation

When the new excerpt exists, judge it with the same five questions:

1. Am I following something that is happening or changing, rather than following an argument being proved?
2. Do I want to know what happens next?
3. Does meaning emerge from what I followed, or does the narrator explain the conclusion in advance?
4. Can I retell the progression after one hearing?
5. Did any inference, reconstruction, hypothesis or source-distance issue masquerade as documented fact?

If questions 1–3 still fail after the upstream authority is clean, do not immediately expand the material schema again. The next suspect should be Writer objective/task framing/model behavior, including whether the mission itself pulls the model toward explanatory essay mode.

## Exit criteria for this feedback round

The checkpoint can move from `changes_requested` to owner approval only when:

- schema-v2 top-level factual fields cannot contradict epistemic-layer classification;
- rejected causal hypotheses are not surfaced to Writer as usable material;
- the misleading historical-change positive test is corrected and route-neutrality has stronger coverage;
- Reviewer target meaning no longer requires the unsupported memory-failure causal thesis;
- stale review cannot be mistaken for current approval authority;
- no Probe 2 prose has been generated before the corrected material snapshot is bound.
