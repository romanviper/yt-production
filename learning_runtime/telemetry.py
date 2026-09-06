from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .artifacts import artifact_identity, write_json

TELEMETRY_VERSION = "PHASE3-DECISION-TELEMETRY-1"
TELEMETRY_FILE = "output/telemetry.jsonl"
REQUIRED_DECISION_ROLES = {"plan", "writer", "truth", "audit"}
EVENT_TYPES = {"DECISION", "CHECKPOINT", "RISK", "DEVIATION"}
FORBIDDEN_KEYS = {
    "chain_of_thought",
    "raw_chain_of_thought",
    "private_reasoning",
    "internal_monologue",
    "hidden_reasoning",
    "scratchpad_reasoning",
}

DECISION_TYPES_BY_ROLE = {
    "plan": {
        "EVIDENCE_SELECTION",
        "INFORMATION_ORDER",
        "BEAT_FUNCTION",
        "DEFER_OR_REVEAL",
        "SCOPE_BOUNDARY",
        "OTHER_BOUNDED_DECISION",
    },
    "writer": {
        "REALIZATION_STRATEGY",
        "PLAN_DEVIATION",
        "EXPLICITNESS",
        "UNIT_BOUNDARY",
        "CLAIM_PHRASING",
        "OTHER_BOUNDED_DECISION",
    },
    "truth": {
        "CLAIM_CLASSIFICATION",
        "EVIDENCE_JUDGMENT",
        "QUALIFICATION",
        "RELEASE_BLOCK",
        "OTHER_BOUNDED_DECISION",
    },
    "audit": {
        "ATTRIBUTION",
        "EVIDENCE_LIMITATION",
        "HYPOTHESIS_UPDATE",
        "OTHER_BOUNDED_DECISION",
    },
}


class TelemetryError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


def _require_string(event: dict[str, Any], key: str) -> str:
    value = event.get(key)
    if not isinstance(value, str) or not value.strip():
        raise TelemetryError("INVALID_TELEMETRY_FIELD", f"{key} must be a non-empty string")
    return value


def _require_list(event: dict[str, Any], key: str) -> list[Any]:
    value = event.get(key)
    if not isinstance(value, list):
        raise TelemetryError("INVALID_TELEMETRY_FIELD", f"{key} must be a list")
    return value


def _reject_private_reasoning_fields(value: Any, path: str = "event") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_KEYS:
                raise TelemetryError(
                    "PRIVATE_REASONING_FIELD_FORBIDDEN",
                    f"{path}.{key} is forbidden; record concise declared decisions and evidence instead",
                )
            _reject_private_reasoning_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_private_reasoning_fields(child, f"{path}[{index}]")


def validate_event(event: dict[str, Any], *, expected_role: str | None = None, expected_execution_id: str | None = None) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise TelemetryError("INVALID_TELEMETRY_EVENT", "event must be an object")
    _reject_private_reasoning_fields(event)

    if event.get("telemetry_version") != TELEMETRY_VERSION:
        raise TelemetryError("TELEMETRY_VERSION_MISMATCH", "unexpected telemetry_version")
    sequence = event.get("sequence")
    if not isinstance(sequence, int) or sequence < 1:
        raise TelemetryError("INVALID_TELEMETRY_SEQUENCE", "sequence must be a positive integer")
    role = _require_string(event, "role")
    execution_id = _require_string(event, "execution_id")
    if expected_role is not None and role != expected_role:
        raise TelemetryError("TELEMETRY_ROLE_MISMATCH", f"expected {expected_role}, observed {role}")
    if expected_execution_id is not None and execution_id != expected_execution_id:
        raise TelemetryError(
            "TELEMETRY_EXECUTION_MISMATCH",
            f"expected {expected_execution_id}, observed {execution_id}",
        )

    event_type = _require_string(event, "event_type")
    if event_type not in EVENT_TYPES:
        raise TelemetryError("UNKNOWN_TELEMETRY_EVENT_TYPE", event_type)
    _require_string(event, "event_id")
    _require_list(event, "subject_refs")

    if event_type == "DECISION":
        decision_type = _require_string(event, "decision_type")
        allowed = DECISION_TYPES_BY_ROLE.get(role, {"OTHER_BOUNDED_DECISION"})
        if decision_type not in allowed:
            raise TelemetryError(
                "DECISION_TYPE_NOT_ALLOWED_FOR_ROLE",
                f"role={role} decision_type={decision_type}",
            )
        _require_string(event, "chosen_action")
        rationale = _require_string(event, "rationale_summary")
        if len(rationale) > 600:
            raise TelemetryError(
                "RATIONALE_SUMMARY_TOO_LONG",
                "rationale_summary must stay concise and engineering-oriented",
            )
        _require_list(event, "evidence_refs")
        _require_list(event, "alternatives_considered")
        _require_string(event, "expected_effect")
        _require_list(event, "risks")
        output_refs = _require_list(event, "output_refs")
        if not all(isinstance(ref, str) and ref.startswith("output/") and ".." not in Path(ref).parts for ref in output_refs):
            raise TelemetryError(
                "INVALID_DECISION_OUTPUT_REF",
                "DECISION output_refs must use bounded output/<path> references",
            )
    elif event_type == "CHECKPOINT":
        _require_string(event, "checkpoint")
        _require_string(event, "status")
        _require_list(event, "artifact_refs")
    elif event_type == "RISK":
        _require_string(event, "risk")
        _require_string(event, "mitigation_or_acceptance")
        _require_list(event, "evidence_refs")
    elif event_type == "DEVIATION":
        _require_string(event, "declared_from")
        _require_string(event, "chosen_action")
        _require_string(event, "rationale_summary")
        _require_list(event, "evidence_refs")
        output_refs = _require_list(event, "output_refs")
        if not all(isinstance(ref, str) and ref.startswith("output/") and ".." not in Path(ref).parts for ref in output_refs):
            raise TelemetryError(
                "INVALID_DEVIATION_OUTPUT_REF",
                "DEVIATION output_refs must use bounded output/<path> references",
            )

    return event


def read_telemetry(path: Path, *, expected_role: str | None = None, expected_execution_id: str | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        raise TelemetryError("TELEMETRY_MISSING", str(path))
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TelemetryError("TELEMETRY_JSON_INVALID", f"line {line_number}: {exc}") from exc
        validate_event(event, expected_role=expected_role, expected_execution_id=expected_execution_id)
        events.append(event)
    if not events:
        raise TelemetryError("TELEMETRY_EMPTY", str(path))
    observed = [event["sequence"] for event in events]
    expected = list(range(1, len(events) + 1))
    if observed != expected:
        raise TelemetryError(
            "TELEMETRY_SEQUENCE_GAP",
            f"expected contiguous sequence {expected}, observed {observed}",
        )
    event_ids = [event["event_id"] for event in events]
    if len(event_ids) != len(set(event_ids)):
        raise TelemetryError("TELEMETRY_EVENT_ID_DUPLICATE", "event_id values must be unique within one execution")
    return events


def decision_binds_output(events: list[dict[str, Any]], output_ref: str) -> bool:
    return any(
        event.get("event_type") == "DECISION" and output_ref in event.get("output_refs", [])
        for event in events
    )


def seal_path(run_root: Path, role: str, execution_id: str) -> Path:
    return run_root / "control" / "seals" / f"{role}-{execution_id}.json"


def is_execution_sealed(run_root: Path, role: str, execution_id: str) -> bool:
    return seal_path(run_root, role, execution_id).exists()


def seal_execution(
    run_root: Path,
    *,
    role: str,
    execution_id: str,
    required_output_refs: list[str],
    require_decision: bool | None = None,
) -> dict[str, Any]:
    run_root = run_root.resolve()
    execution_root = (run_root / "agents" / role / execution_id).resolve()
    if not execution_root.exists():
        raise FileNotFoundError(execution_root)
    destination = seal_path(run_root, role, execution_id)
    if destination.exists():
        raise FileExistsError(destination)

    telemetry_path = execution_root / TELEMETRY_FILE
    events = read_telemetry(
        telemetry_path,
        expected_role=role,
        expected_execution_id=execution_id,
    )
    if require_decision is None:
        require_decision = role in REQUIRED_DECISION_ROLES
    if require_decision and not any(event["event_type"] == "DECISION" for event in events):
        raise TelemetryError(
            "DECISION_EVENT_REQUIRED_BEFORE_SEAL",
            f"role {role} must declare at least one bounded decision before seal",
        )

    outputs: dict[str, Any] = {}
    output_root = (execution_root / "output").resolve()
    for relative in required_output_refs:
        rel = Path(relative)
        if rel.is_absolute() or ".." in rel.parts:
            raise TelemetryError("INVALID_REQUIRED_OUTPUT_REF", relative)
        path = (output_root / rel).resolve(strict=True)
        if path == telemetry_path.resolve():
            raise TelemetryError("TELEMETRY_CANNOT_BE_PRIMARY_OUTPUT", relative)
        if output_root not in path.parents:
            raise TelemetryError("REQUIRED_OUTPUT_ESCAPE", relative)
        full_ref = f"output/{relative}"
        if require_decision and not decision_binds_output(events, full_ref):
            raise TelemetryError(
                "PRIMARY_OUTPUT_NOT_BOUND_TO_DECISION",
                f"{role}/{execution_id}:{full_ref}",
            )
        outputs[relative] = artifact_identity(path)

    seal = {
        "schema_version": "1.1.0",
        "telemetry_version": TELEMETRY_VERSION,
        "role": role,
        "execution_id": execution_id,
        "status": "SEALED_BEFORE_DOWNSTREAM_FEEDBACK",
        "telemetry_ref": TELEMETRY_FILE,
        "telemetry_identity": artifact_identity(telemetry_path),
        "event_count": len(events),
        "decision_count": sum(1 for event in events if event["event_type"] == "DECISION"),
        "output_identities": outputs,
        "output_binding_rule": "Each required primary output for Plan/Writer/Truth/Audit must be named by a prior DECISION output_refs entry before materialization.",
        "limitations": [
            "Telemetry records declared engineering/editorial decisions, checkpoints, risks and deviations; it is not raw private chain-of-thought.",
            "A declared rationale remains self-report evidence and can be contradicted by downstream artifact analysis.",
        ],
    }
    write_json(destination, seal)
    return seal


def verify_execution_seal(run_root: Path, *, role: str, execution_id: str) -> dict[str, Any]:
    run_root = run_root.resolve()
    path = seal_path(run_root, role, execution_id)
    if not path.exists():
        raise TelemetryError("EXECUTION_NOT_SEALED", f"{role}/{execution_id}")
    seal = json.loads(path.read_text(encoding="utf-8"))
    execution_root = (run_root / "agents" / role / execution_id).resolve()
    telemetry_path = execution_root / seal["telemetry_ref"]
    telemetry_observed = artifact_identity(telemetry_path)
    if telemetry_observed["raw_sha256"] != seal["telemetry_identity"]["raw_sha256"]:
        raise TelemetryError("SEALED_TELEMETRY_CHANGED", f"{role}/{execution_id}")
    for relative, expected in seal["output_identities"].items():
        observed = artifact_identity(execution_root / "output" / relative)
        if observed["raw_sha256"] != expected["raw_sha256"]:
            raise TelemetryError("SEALED_OUTPUT_CHANGED", f"{role}/{execution_id}:{relative}")
    read_telemetry(telemetry_path, expected_role=role, expected_execution_id=execution_id)
    return {"status": "VALID", "seal": seal}
