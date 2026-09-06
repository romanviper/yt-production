from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifacts import normalize_text


class EvidenceError(ValueError):
    def __init__(self, code: str, *, artifact: str, field: str, expected: Any = None, observed: Any = None):
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        super().__init__(f"{code}: {artifact}.{field}: expected={expected!r} observed={observed!r}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "artifact": self.artifact,
            "field": self.field,
            "expected": self.expected,
            "observed": self.observed,
        }


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    quote: str


@dataclass(frozen=True)
class Diagnosis:
    failure_id: str
    beat_id: str | None
    classification: str
    confidence: str
    mapping_status: str
    mapping_confidence: str
    attribution_status: str
    suspected_regions: list[str]
    observations: list[dict[str, Any]]
    limitations: list[str]


def _find_all(text: str, quote: str) -> list[int]:
    starts: list[int] = []
    pos = 0
    while True:
        found = text.find(quote, pos)
        if found < 0:
            return starts
        starts.append(found)
        pos = found + 1


def resolve_exact_span(
    text: str,
    quote: str,
    *,
    artifact: str,
    field: str,
    locator: dict[str, int] | None = None,
) -> Span:
    normalized_text = normalize_text(text)
    normalized_quote = normalize_text(quote)
    if not normalized_quote:
        raise EvidenceError("EMPTY_QUOTE", artifact=artifact, field=field, expected="non-empty exact quote", observed=quote)

    if locator is not None:
        start = locator.get("start")
        end = locator.get("end")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end < start:
            raise EvidenceError("MALFORMED_LOCATOR", artifact=artifact, field=field, expected="integer start/end", observed=locator)
        observed = normalized_text[start:end]
        if observed != normalized_quote:
            raise EvidenceError("LOCATOR_QUOTE_MISMATCH", artifact=artifact, field=field, expected=normalized_quote, observed=observed)
        return Span(start, end, normalized_quote)

    starts = _find_all(normalized_text, normalized_quote)
    if not starts:
        raise EvidenceError("SPAN_NOT_FOUND", artifact=artifact, field=field, expected=normalized_quote, observed=None)
    if len(starts) > 1:
        raise EvidenceError("AMBIGUOUS_SPAN", artifact=artifact, field=field, expected="unique quote or locator", observed=starts)
    start = starts[0]
    return Span(start, start + len(normalized_quote), normalized_quote)


def _validate_writer_report_against_candidate(candidate_text: str, writer_report: dict[str, Any]) -> dict[str, Span]:
    spans: dict[str, Span] = {}
    previous_start = -1
    for index, beat in enumerate(writer_report.get("beat_execution", [])):
        if beat.get("status") != "REALIZED":
            continue
        beat_id = beat.get("beat_id")
        if not beat_id:
            raise EvidenceError("MALFORMED_WRITER_REPORT", artifact="writer_report", field=f"beat_execution[{index}].beat_id", expected="non-empty beat_id", observed=beat_id)
        quote = beat.get("candidate_quote")
        if not isinstance(quote, str) or not quote:
            raise EvidenceError("EMPTY_WRITER_QUOTE", artifact="writer_report", field=f"beat_execution[{index}].candidate_quote", expected="non-empty exact quote", observed=quote)
        locator = beat.get("candidate_locator")
        span = resolve_exact_span(candidate_text, quote, artifact="writer_report", field=f"beat_execution[{index}].candidate_quote", locator=locator)
        if span.start < previous_start:
            raise EvidenceError("WRITER_REPORT_OUTPUT_ORDER_MISMATCH", artifact="writer_report", field="beat_execution", expected="candidate spans in report order", observed=[previous_start, span.start])
        previous_start = span.start
        spans[beat_id] = span
    if not spans:
        raise EvidenceError("WRITER_REPORT_HAS_NO_REALIZED_SPANS", artifact="writer_report", field="beat_execution", expected="at least one realized exact span", observed=[])
    return spans


def diagnose_failure(
    *,
    candidate_text: str,
    plan: dict[str, Any],
    writer_report: dict[str, Any],
    failure: dict[str, Any],
) -> Diagnosis:
    observations: list[dict[str, Any]] = []
    limitations: list[str] = []

    failure_quote = failure.get("candidate_quote")
    if not isinstance(failure_quote, str) or not failure_quote:
        raise EvidenceError("EMPTY_FAILURE_QUOTE", artifact="failure", field="candidate_quote", expected="non-empty exact quote", observed=failure_quote)
    failure_span = resolve_exact_span(
        candidate_text,
        failure_quote,
        artifact="failure",
        field="candidate_quote",
        locator=failure.get("candidate_locator"),
    )
    observations.append(
        {
            "kind": "OUTPUT_IDENTITY_AND_SPAN",
            "authority": "RUNTIME_OBSERVED",
            "failure_id": failure.get("failure_id"),
            "symptom": failure.get("symptom"),
            "span": {"start": failure_span.start, "end": failure_span.end, "quote": failure_span.quote},
        }
    )

    writer_spans = _validate_writer_report_against_candidate(candidate_text, writer_report)
    covering: list[tuple[dict[str, Any], Span]] = []
    for beat in writer_report.get("beat_execution", []):
        beat_id = beat.get("beat_id")
        span = writer_spans.get(beat_id)
        if span and span.start <= failure_span.start and span.end >= failure_span.end:
            covering.append((beat, span))
    if not covering:
        raise EvidenceError("WRITER_MAPPING_NOT_FOUND", artifact="writer_report", field="beat_execution", expected="one realized writer span covering failure span", observed=[])
    if len(covering) > 1:
        raise EvidenceError("AMBIGUOUS_WRITER_MAPPING", artifact="writer_report", field="beat_execution", expected="one writer span covering failure span", observed=[b.get("beat_id") for b, _ in covering])

    writer_beat, writer_span = covering[0]
    beat_id = writer_beat["beat_id"]
    observations.append(
        {
            "kind": "WRITER_MAPPING",
            "authority": "RUNTIME_OBSERVED",
            "beat_id": beat_id,
            "writer_span": {"start": writer_span.start, "end": writer_span.end, "quote": writer_span.quote},
            "covers_failure_span": True,
        }
    )
    observations.append(
        {
            "kind": "WRITER_DECLARATION",
            "authority": "AGENT_DECLARED",
            "beat_id": beat_id,
            "status": writer_beat.get("status"),
            "note": "REALIZED is retained as a declaration; it is not independent proof of semantic adherence.",
        }
    )

    plan_beat = next((b for b in plan.get("beats", []) if b.get("id") == beat_id), None)
    if plan_beat is None:
        raise EvidenceError("PLAN_BEAT_NOT_FOUND", artifact="plan", field="beats", expected=beat_id, observed=None)

    plan_observation = failure.get("plan_observation") or {}
    fields = plan_observation.get("fields") or []
    if not fields:
        raise EvidenceError("PLAN_EVIDENCE_MISSING", artifact="failure", field="plan_observation.fields", expected="one or more referenced Plan fields", observed=fields)
    field_evidence: list[dict[str, Any]] = []
    for field in fields:
        if field not in plan_beat:
            raise EvidenceError("PLAN_EVIDENCE_STALE", artifact="plan", field=f"{beat_id}.{field}", expected="referenced field exists", observed=None)
        value = plan_beat[field]
        if value is None or value == "":
            raise EvidenceError("PLAN_EVIDENCE_EMPTY", artifact="plan", field=f"{beat_id}.{field}", expected="non-empty field", observed=value)
        field_evidence.append({"field": field, "exact_value": value})
    observations.append(
        {
            "kind": "PLAN_MAPPING",
            "authority": "RUNTIME_OBSERVED",
            "beat_id": beat_id,
            "function": plan_beat.get("function"),
            "field_evidence": field_evidence,
        }
    )

    reviewer_interpretation = plan_observation.get("observation")
    if reviewer_interpretation:
        observations.append(
            {
                "kind": "PLAN_REVIEWER_INTERPRETATION",
                "authority": "REVIEWER_INTERPRETATION",
                "beat_id": beat_id,
                "interpretation": reviewer_interpretation,
                "legacy_symptom_flag": plan_observation.get("symptom_present"),
                "note": "The boolean flag is recorded for provenance but does not drive attribution.",
            }
        )
    else:
        limitations.append("No reviewer interpretation binds the referenced Plan fields to the output symptom.")

    beat_deviations = [d for d in writer_report.get("deviations", []) if d.get("beat_id") == beat_id]
    relevant_deviations = [
        d for d in beat_deviations
        if d.get("symptom_relevance") == "RELEVANT" and isinstance(d.get("evidence"), str) and d.get("evidence").strip()
    ]
    observations.append(
        {
            "kind": "WRITER_DEVIATIONS",
            "authority": "AGENT_DECLARED_WITH_RUNTIME_FILTER",
            "beat_id": beat_id,
            "all_declared": beat_deviations,
            "symptom_relevant_with_evidence": relevant_deviations,
            "note": "Unrelated or ungrounded deviations do not affect attribution.",
        }
    )

    plan_support = bool(reviewer_interpretation and field_evidence)
    writer_support = bool(relevant_deviations)
    if plan_support and writer_support:
        classification = "MULTIPLE_REGIONS_SUSPECT"
        suspected_regions = ["PLAN", "WRITE"]
        attribution_confidence = "MEDIUM"
        limitations.append("Both Plan interpretation evidence and symptom-relevant Writer deviation evidence are present; contribution cannot be isolated further from this bundle.")
    elif plan_support:
        classification = "PLAN_REGION_SUSPECT"
        suspected_regions = ["PLAN"]
        attribution_confidence = "MEDIUM"
        limitations.append("Plan evidence supports inspecting the Plan region, but Writer contribution is not excluded merely because the report says REALIZED/no deviation.")
    elif writer_support:
        classification = "WRITE_REGION_SUSPECT"
        suspected_regions = ["WRITE"]
        attribution_confidence = "MEDIUM"
        limitations.append("A symptom-relevant Writer deviation is declared with evidence; Plan contribution is not independently disproved.")
    else:
        classification = "INCONCLUSIVE_ATTRIBUTION"
        suspected_regions = []
        attribution_confidence = "LOW"
        limitations.append("Exact mapping is valid, but semantic attribution lacks enough evidence to nominate a bounded region.")

    observations.append(
        {
            "kind": "BOUNDED_ATTRIBUTION",
            "authority": "INTERVENTION_SUPPORTED_HYPOTHESIS",
            "classification": classification,
            "suspected_regions": suspected_regions,
            "mapping_confidence": "HIGH",
            "attribution_confidence": attribution_confidence,
            "rule": "Exact identity/mapping is necessary but not causal proof. Reviewer interpretation may nominate Plan; only symptom-relevant grounded deviations may nominate Write; boolean flags and REALIZED/no-deviation declarations never decide attribution alone.",
        }
    )

    return Diagnosis(
        failure_id=failure["failure_id"],
        beat_id=beat_id,
        classification=classification,
        confidence=attribution_confidence,
        mapping_status="VALIDATED_EXACT",
        mapping_confidence="HIGH",
        attribution_status="BOUNDED_HYPOTHESIS" if suspected_regions else "INCONCLUSIVE",
        suspected_regions=suspected_regions,
        observations=observations,
        limitations=limitations,
    )


def write_trace(path: Path, events: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for event in events:
            fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
