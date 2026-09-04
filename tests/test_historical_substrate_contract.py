from __future__ import annotations

import json
from pathlib import Path

from scripts.historical_substrate_contract import (
    build_writer_section_substrate,
    validate_historical_substrate,
    validate_section_binding,
)


def _claims() -> dict:
    return {
        "claims": [
            {
                "id": "CLM-0001",
                "status": "supported",
                "sources": ["SRC-0001"],
            }
        ]
    }


def _sources() -> dict:
    return {
        "sources": [
            {
                "id": "SRC-0001",
                "status": "reviewed",
            }
        ]
    }


def _substrate() -> dict:
    return {
        "schema_version": 1,
        "coverage": {"mode": "product", "covered_sections": ["P01"]},
        "records": [
            {
                "id": "HS-P01-0001",
                "kind": "practice",
                "statement": "Quantities were recorded through several coexisting clay practices.",
                "epistemic_status": "documented",
                "claim_ids": ["CLM-0001"],
                "source_refs": [{"source_id": "SRC-0001", "locator": "pp. 1-2"}],
                "time_scope": "Late Uruk",
                "place_scope": "Southern Mesopotamia",
                "limitations": ["Do not infer a single replacement sequence."],
            }
        ],
    }


def test_valid_substrate_is_source_bound() -> None:
    assert validate_historical_substrate(_substrate(), _claims(), _sources()) == []


def test_substrate_rejects_narrative_authority() -> None:
    value = _substrate()
    value["records"][0]["hook"] = "Open on the object"
    errors = validate_historical_substrate(value, _claims(), _sources())
    assert any("narrative-authority fields" in error for error in errors)


def test_substrate_rejects_source_outside_claim_authority() -> None:
    value = _substrate()
    value["records"][0]["source_refs"] = [{"source_id": "SRC-9999"}]
    errors = validate_historical_substrate(
        value,
        _claims(),
        {"sources": [{"id": "SRC-9999", "status": "reviewed"}]},
    )
    assert any("exceed referenced claim authority" in error for error in errors)


def test_section_binding_rejects_question_mission_and_evidence_state_change() -> None:
    section = {
        "id": "P01",
        "historical_territory": "What did the evidence show?",
        "historical_change": {
            "from": "Bằng chứng còn lại cho thấy counters.",
            "to": "Evidence shows tablets.",
        },
        "historical_substrate_ids": ["HS-P01-0001"],
        "claim_ids": ["CLM-0001"],
    }
    errors = validate_section_binding(section, _substrate())
    assert any("must not be an answer-shaped question" in error for error in errors)
    assert any("evidence-state rather than historical-world state" in error for error in errors)


def test_writer_projection_hides_research_ledger_payload(tmp_path: Path) -> None:
    substrate_path = tmp_path / "historical-substrate.json"
    outline_path = tmp_path / "outline.json"
    substrate_path.write_text(json.dumps(_substrate()), encoding="utf-8")
    outline_path.write_text(json.dumps({"status": "approved"}), encoding="utf-8")
    section = {
        "id": "P01",
        "historical_territory": "Late-Uruk clay recording practices.",
        "historical_change": {
            "from": "Quantities were handled across several coexisting devices.",
            "to": "Quantities increasingly appeared directly on durable clay surfaces.",
        },
        "historical_substrate_ids": ["HS-P01-0001"],
        "claim_ids": ["CLM-0001"],
    }
    writer_view = build_writer_section_substrate(substrate_path, section, outline_path)
    primitive = writer_view["primitives"][0]
    assert primitive["statement"]
    assert "claim_ids" not in primitive
    assert "source_refs" not in primitive
    assert writer_view["boundaries"][0]["limitations"]
