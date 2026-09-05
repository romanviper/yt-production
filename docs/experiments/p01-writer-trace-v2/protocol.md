# Frozen writer-observability contract v2

## Objective

Diagnose why repeated harness revisions fail to converge on the desired history-podcast prose by separating planning quality from prose realization.

## Core causal split

1. `writing-plan.json`: inspectable pre-prose listener-experience plan.
2. `candidate.md`: Writer realization of that frozen plan.
3. `writer-report.json`: structured observable execution/deviation report, not chain-of-thought.
4. Blind Product reviews: prose only, no plan/trace.
5. Trace Auditor: plan + prose + Writer report, no Product verdicts.

## Planner contract

Planner may inspect frozen baseline, approved historical authority, product context and FoC craft references. It outputs structure, not polished prose. Each of 4–8 beats must bind exact evidence and record `listener_before`, `listener_after`, delayed information, forward pressure and truth boundary. Renaming a topical outline as beats is a planning failure.

## Writer contract

Writer receives frozen plan, approved authority and product context, but not old baseline, FoC transcripts, comparison labels, hypothesis, prior verdicts or Planner conversation. It writes candidate prose plus a structured report covering every beat and observable deviations. It must not reveal private chain-of-thought.

## Trace Auditor contract

Audit observable plan-to-prose alignment and classify `PLAN_FAILURE`, `REALIZATION_FAILURE`, `MIXED`, `NONE`, or `TRACE_UNRELIABLE`. Stated intention alone is not evidence that prose achieved it.

## Independence

Truth and Product reviewers never receive the plan or Writer report. Product reviewers compare reversed A/B samples. Truth uses approved authority only; FoC remains craft-only.

## Execution provenance

Planner, Writer, Trace Auditor, Truth and both Product reviewers are first-class executions. Each records input packet hash, model/config, timestamps, run/context ID and preserved platform export. Missing Writer provenance makes the process inconclusive.

## Decision boundary

Trace diagnosis explains failure location but never votes on product quality. `PROVISIONAL_SCRIPT_IMPROVEMENT` still requires truth clearance, valid execution evidence and both blind Product reviewers preferring the candidate overall and on `movement`, with no dimension preferring baseline or uncertain for candidate.