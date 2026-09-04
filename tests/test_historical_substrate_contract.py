from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.historical_substrate_contract import (
    build_writer_section_substrate,
    validate_historical_substrate,
    validate_section_binding,
)


class HistoricalSubstrateContractTest(unittest.TestCase):
    def _claims(self) -> dict:
        return {
            "claims": [
                {"id": "CLM-0001", "status": "supported", "sources": ["SRC-0001"]}
            ]
        }

    def _sources(self) -> dict:
        return {"sources": [{"id": "SRC-0001", "status": "reviewed"}]}

    def _substrate(self) -> dict:
        return {
            "schema_version": 2,
            "coverage": {"mode": "section_migration", "covered_sections": ["P01"]},
            "records": [
                {
                    "id": "HS-P01-0001",
                    "kind": "practice",
                    "world": {
                        "participants": [],
                        "operation": "record quantities through several clay practices",
                        "object_or_medium": ["clay counters", "clay surfaces"],
                        "information_or_relation_handled": ["quantities"],
                        "context": "Late-Uruk administration",
                    },
                    "statement": "Quantities were recorded through several coexisting clay practices.",
                    "epistemic_status": "documented",
                    "claim_ids": ["CLM-0001"],
                    "source_refs": [{"source_id": "SRC-0001", "locator": "pp. 1–2"}],
                    "time_scope": "Late Uruk",
                    "place_scope": "Southern Mesopotamia",
                    "boundaries": ["Do not infer a single replacement sequence."],
                }
            ],
            "constraints": [
                {
                    "id": "HSC-P01-0001",
                    "rule": "Do not infer a single replacement sequence.",
                    "applies_to": ["HS-P01-0001"],
                    "claim_ids": ["CLM-0001"],
                    "source_refs": [{"source_id": "SRC-0001", "locator": "pp. 1–2"}],
                }
            ],
        }

    def _section(self) -> dict:
        return {
            "id": "P01",
            "historical_territory": "Late-Uruk clay recording practices.",
            "historical_change": {
                "from": "Quantities were handled across several coexisting devices.",
                "to": "Quantities increasingly appeared directly on durable clay surfaces.",
            },
            "historical_substrate_ids": ["HS-P01-0001"],
            "claim_ids": ["CLM-0001"],
        }

    def test_valid_world_shaped_substrate_is_source_bound(self) -> None:
        self.assertEqual(
            validate_historical_substrate(self._substrate(), self._claims(), self._sources()),
            [],
        )

    def test_substrate_rejects_narrative_authority(self) -> None:
        value = self._substrate()
        value["records"][0]["hook"] = "Open on the object"
        errors = validate_historical_substrate(value, self._claims(), self._sources())
        self.assertTrue(any("narrative-authority fields" in error for error in errors))

    def test_world_rejects_evidence_state_language(self) -> None:
        value = self._substrate()
        value["records"][0]["world"]["operation"] = "the corpus shows quantities"
        errors = validate_historical_substrate(value, self._claims(), self._sources())
        self.assertTrue(any("evidence-state language" in error for error in errors))

    def test_section_binding_rejects_question_and_evidence_state_change(self) -> None:
        section = self._section()
        section["historical_territory"] = "What did the evidence show?"
        section["historical_change"] = {
            "from": "Evidence shows counters.",
            "to": "The corpus shows tablets.",
        }
        errors = validate_section_binding(section, self._substrate())
        self.assertTrue(any("answer-shaped question" in error for error in errors))
        self.assertTrue(any("evidence-state" in error for error in errors))

    def test_writer_projection_is_world_shaped_and_hides_research_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            substrate_path = root / "historical-substrate.json"
            outline_path = root / "outline.json"
            substrate_path.write_text(json.dumps(self._substrate()), encoding="utf-8")
            outline_path.write_text(json.dumps({"status": "approved"}), encoding="utf-8")
            writer_view = build_writer_section_substrate(substrate_path, self._section(), outline_path)
        primitive = writer_view["primitives"][0]
        self.assertIn("world", primitive)
        self.assertNotIn("statement", primitive)
        self.assertNotIn("claim_ids", primitive)
        self.assertNotIn("source_refs", primitive)
        self.assertEqual(primitive["world"]["operation"], "record quantities through several clay practices")
        self.assertTrue(any(item.get("source") == "HSC-P01-0001" for item in writer_view["boundaries"]))

    def test_statement_is_not_native_semantic_authority(self) -> None:
        value = self._substrate()
        del value["records"][0]["statement"]
        self.assertEqual(validate_historical_substrate(value, self._claims(), self._sources()), [])
        self.assertEqual(value["records"][0]["world"]["object_or_medium"], ["clay counters", "clay surfaces"])


if __name__ == "__main__":
    unittest.main()
