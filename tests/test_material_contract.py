"""Tests for the authoritative material contract and validation rules."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.draft_evidence import DraftEvidenceBroker, EvidenceAccessError
from scripts.material_contract import (
    FORBIDDEN_CREATIVE_FIELDS,
    VALID_MATERIAL_KINDS,
    VALID_SOURCE_RELATIONS,
    validate_material_record,
    validate_materials_collection,
    validate_materials_file,
)
from test_material_aware_handoff import SOURCE_PRODUCT, make_direct_authorship_fixture, write_json
from scripts.materialize_sections import materialize
from scripts.task import create_task


class MaterialContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_record = {
            "id": "MAT-0001",
            "kind": "object",
            "label": "Clay accounting token",
            "claim_ids": ["CLM-0001"],
            "source_refs": [
                {
                    "source_id": "SRC-0001",
                    "locators": ["p. 42"],
                }
            ],
            "source_relation": "contemporary_material",
            "object_or_trace": "Geometric clay token",
            "documented_action": "Impression on clay surface",
            "explicit_sequence": ["model sphere", "incise mark", "bake"],
            "time": "Late Uruk period",
            "place": "Eanna precinct",
            "physical_description": "Conical clay token measuring 2cm",
            "measurement": "2cm height",
            "limitations": ["Attested in administrative contexts only"],
            "representativeness": "standard administrative token",
        }

    def test_valid_record_passes_contract(self) -> None:
        errors = validate_material_record(
            self.valid_record,
            allowed_claim_ids={"CLM-0001"},
            allowed_source_ids={"SRC-0001"},
            require_source_relation=True,
        )
        self.assertEqual([], errors)

    def test_forbidden_creative_authority_fields_fail(self) -> None:
        for field in FORBIDDEN_CREATIVE_FIELDS:
            with self.subTest(forbidden_field=field):
                bad = dict(self.valid_record)
                bad[field] = "some creative assignment"
                errors = validate_material_record(bad)
                self.assertTrue(any(field in err and "forbidden creative-authority field" in err for err in errors))

    def test_out_of_scope_claim_and_source_fail(self) -> None:
        errors = validate_material_record(
            self.valid_record,
            allowed_claim_ids={"CLM-9999"},
            allowed_source_ids={"SRC-9999"},
        )
        self.assertTrue(any("unknown claim: CLM-0001" in err for err in errors))
        self.assertTrue(any("unknown source: SRC-0001" in err for err in errors))

    def test_invalid_kind_and_source_relation_fail(self) -> None:
        bad = dict(self.valid_record)
        bad["kind"] = "unsupported_fiction_kind"
        bad["source_relation"] = "hearsay_rumor"
        errors = validate_material_record(bad)
        self.assertTrue(any("invalid kind: unsupported_fiction_kind" in err for err in errors))
        self.assertTrue(any("invalid source_relation: hearsay_rumor" in err for err in errors))

    def test_explicit_sequence_and_limitations_must_be_strings(self) -> None:
        bad = dict(self.valid_record)
        bad["explicit_sequence"] = [123, True]
        bad["limitations"] = [None]
        errors = validate_material_record(bad)
        self.assertTrue(any("explicit_sequence must be a list of strings" in err for err in errors))
        self.assertTrue(any("limitations must be a list of strings" in err for err in errors))

    def test_validate_materials_collection_detects_duplicates(self) -> None:
        collection = [self.valid_record, self.valid_record]
        errors = validate_materials_collection(collection)
        self.assertTrue(any("duplicate material ID: MAT-0001" in err for err in errors))

    def test_validate_materials_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            file_path = Path(temp) / "materials.json"
            write_json(file_path, {"schema_version": 1, "materials": [self.valid_record]})
            errors = validate_materials_file(
                file_path,
                allowed_claim_ids={"CLM-0001"},
                allowed_source_ids={"SRC-0001"},
            )
            self.assertEqual([], errors)

            bad_record = dict(self.valid_record)
            bad_record["focal_carrier"] = "Must not enter"
            write_json(file_path, {"schema_version": 1, "materials": [bad_record]})
            errors = validate_materials_file(file_path)
            self.assertTrue(any("forbidden creative-authority field: focal_carrier" in err for err in errors))

    def test_broker_rejects_material_with_forbidden_creative_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            task_work = create_task(product, "draft_section", "P01", None, False)
            task_id = task_work["id"]

            sec_mat_path = product / "03_sections" / "P01" / "materials.json"
            bad_mat = dict(self.valid_record)
            bad_mat["story_role"] = "opening_revelation"
            write_json(sec_mat_path, {"schema_version": 1, "materials": [bad_mat]})

            broker = DraftEvidenceBroker(product, task_id)
            with self.assertRaises(EvidenceAccessError) as ctx:
                broker.call("source", {"id": "SRC-0001"})
            self.assertIn("forbidden creative-authority field: story_role", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
