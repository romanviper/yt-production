from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Diagnosis:
    failure_id: str
    beat_id: str | None
    classification: str
    confidence: str
    observations: list[dict[str, Any]]


def diagnose_failure(*, plan: dict[str, Any], writer_report: dict[str, Any], failure: dict[str, Any]) -> Diagnosis:
    needle = failure["candidate_quote"]
    writer_beat = None
    for beat in writer_report.get("beat_execution", []):
        quote = beat.get("candidate_quote", "")
        if needle in quote or quote in needle:
            writer_beat = beat
            break

    observations: list[dict[str, Any]] = [
        {
            "kind": "OUTPUT_FAILURE",
            "failure_id": failure["failure_id"],
            "symptom": failure["symptom"],
            "candidate_quote": needle,
            "authority": failure.get("authority", "DIAGNOSTIC_HYPOTHESIS"),
        }
    ]

    if writer_beat is None:
        observations.append({"kind": "WRITER_MAPPING", "status": "NOT_FOUND"})
        return Diagnosis(failure["failure_id"], None, "INCONCLUSIVE_TRACE", "LOW", observations)

    beat_id = writer_beat["beat_id"]
    deviations = [d for d in writer_report.get("deviations", []) if d.get("beat_id") == beat_id]
    observations.append(
        {
            "kind": "WRITER_MAPPING",
            "status": writer_beat.get("status"),
            "beat_id": beat_id,
            "deviations": deviations,
        }
    )

    plan_beat = next((b for b in plan.get("beats", []) if b.get("id") == beat_id), None)
    if plan_beat is None:
        observations.append({"kind": "PLAN_MAPPING", "status": "NOT_FOUND", "beat_id": beat_id})
        return Diagnosis(failure["failure_id"], beat_id, "INCONCLUSIVE_TRACE", "LOW", observations)

    plan_observation = failure.get("plan_observation", {})
    fields = plan_observation.get("fields", [])
    observations.append(
        {
            "kind": "PLAN_MAPPING",
            "status": "FOUND",
            "beat_id": beat_id,
            "function": plan_beat.get("function"),
            "inspected_fields": {field: plan_beat.get(field) for field in fields},
        }
    )
    symptom_present = plan_observation.get("symptom_present")
    observations.append(
        {
            "kind": "PLAN_SYMPTOM_OBSERVATION",
            "symptom_present": symptom_present,
            "observation": plan_observation.get("observation"),
            "authority": "DECLARED_DIAGNOSTIC_OBSERVATION_NOT_PRIVATE_REASONING",
        }
    )

    aligned = writer_beat.get("status") == "REALIZED" and not deviations
    observations.append({"kind": "REALIZATION_ALIGNMENT", "aligned": aligned})

    if not aligned:
        classification = "REALIZATION_FAILURE"
        confidence = "MEDIUM"
    elif symptom_present is True:
        classification = "PLAN_FAILURE"
        confidence = "HIGH"
    elif symptom_present is False:
        classification = "REALIZATION_FAILURE"
        confidence = "MEDIUM"
    else:
        classification = "INCONCLUSIVE_TRACE"
        confidence = "LOW"

    observations.append(
        {
            "kind": "DERIVED_DIAGNOSIS",
            "classification": classification,
            "confidence": confidence,
            "rule": "aligned writer + symptom already observable in mapped plan node => PLAN_FAILURE; deviation or symptom introduced only in prose => REALIZATION_FAILURE",
        }
    )
    return Diagnosis(failure["failure_id"], beat_id, classification, confidence, observations)


def write_trace(path: Path, events: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
