# Phase 3 — White-box Learning MVP

Status: **ACTIVE MVP**

## Goal

Prove one useful fault-isolation path, not build a general observability platform.

The first question is deliberately narrow:

> When an observable prose failure appears in a span that maps to one Writer beat, was the problematic behavior already encoded in the corresponding Plan node, or was it introduced during realization?

## Command

```bash
python -m learning_runtime.phase3 p01-rootcause-01 --out /tmp/p01-phase3-rootcause-01
```

The command first materializes the Phase 2 `Plan -> Write -> Truth -> Product` chain, then adds white-box traces only to Plan and Write.

Expected additional artifacts:

```text
plan/trace.jsonl
write/trace.jsonl
diagnosis.json
phase3-manifest.json
```

## Trace semantics

Trace contains engineering observations only:

- observed output failure span;
- exact Writer beat mapping;
- Writer realization/deviation status;
- exact Plan beat mapping;
- declared diagnostic observation about whether the symptom is already present in the Plan representation;
- derived bounded diagnosis.

It is not raw private chain-of-thought.

## First diagnostic fixture

`P3-F01` uses archived Round-01 B03.

Output symptom: `EXPOSITION_LOAD.EXPLANATION_BEFORE_NEED`.

The candidate explicitly states the resolved interpretation of the envelope condition. Writer report maps that prose to B03 as `REALIZED` with no deviations. The Plan's B03 already prescribes the listener-after state as the material paradox/security-versus-visibility conclusion.

Under the MVP rule this isolates the first fault region to **Plan**, not Writer realization.

This diagnosis is a bounded engineering attribution, not proof that all essay-like behavior comes from the Planner. The failure seed is diagnostic evidence, not owner-calibration gold.

## Bounded intervention

`learning_runtime/interventions/p01-rootcause-01-plan-only.json` changes only B03's planning representation:

- preserve the observable closed/open physical constraint;
- preserve evidence and truth boundaries;
- remove/delay the pre-resolved 'security versus visibility paradox';
- leave Writer contract unchanged.

The prediction is explicit: `EXPLANATION_BEFORE_NEED` should reduce without harming truth, artifact clarity or continuity.

## MVP boundary

This repository session has no live agent-execution adapter. Therefore Phase 3 must not fabricate a rerun or claim improvement.

The white-box trace and bounded intervention are executable now; the next live Writer run must consume the intervention under the same evidence ceiling, then return to the Phase 1 owner/Product measurement surface.

## Exit condition for this slice

This slice succeeds when:

1. failed output span maps backward to one Writer beat and one Plan node;
2. Writer alignment/deviation is mechanically visible;
3. Plan-vs-realization classification follows explicit observations rather than agent self-assertion;
4. one smallest-change intervention is generated for the diagnosed region;
5. no benchmark, production router or unrelated agent framework is expanded.
