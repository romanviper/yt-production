"""Tests for deterministic section material preflight and evidence resolution routing."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.draft_evidence import preflight_section_materials
from scripts.materialize_sections import materialize
from scripts.task import create_task
from test_material_aware_handoff import make_direct_authorship_fixture, write_json


class MaterialPreflightRoutingTests(unittest.TestCase):
    def test_claims_only_section_cannot_create_draft_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)

            # Remove global and section materials to leave only claims
            global_mat = product / "01_research" / "material-ledger.json"
            if global_mat.is_file():
                global_mat.unlink()

            sec_mat = product / "03_sections" / "P01" / "materials.json"
            if sec_mat.is_file():
                sec_mat.unlink()

            preflight = preflight_section_materials(product, "P01")
            self.assertEqual("needs_evidence_resolution", preflight["status"])
            self.assertEqual(0, preflight["material_count"])

            with self.assertRaisesRegex(ValueError, "needs_evidence_resolution"):
                create_task(product, "draft_section", "P01", None, False)

    def test_evidence_resolution_resolves_preflight_allowing_draft_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)

            # Remove global ledger to simulate claims-only research
            global_mat = product / "01_research" / "material-ledger.json"
            if global_mat.is_file():
                global_mat.unlink()

            # Verify it cannot draft yet
            preflight = preflight_section_materials(product, "P01")
            self.assertEqual("needs_evidence_resolution", preflight["status"])

            # Create evidence_resolution task
            res_task = create_task(product, "evidence_resolution", "P01", None, False)
            self.assertIn("evidence_resolution", res_task["operation"])

            # Simulate evidence_resolution outputting materials.json
            sec_mat = product / "03_sections" / "P01" / "materials.json"
            write_json(
                sec_mat,
                {
                    "schema_version": 1,
                    "materials": [
                        {
                            "id": "P01-MAT-001",
                            "kind": "object",
                            "label": "Clay token",
                            "claim_ids": ["CLM-0001"],
                            "source_refs": [{"source_id": "SRC-0001", "locators": ["p. 10"]}],
                            "source_relation": "contemporary_material",
                            "actor": "Administrator",
                            "object_or_trace": "Geometric token",
                            "documented_action": "Sealing in clay envelope",
                        }
                    ],
                },
            )

            # Material preflight now passes
            preflight_after = preflight_section_materials(product, "P01")
            self.assertEqual("material_ready", preflight_after["status"])
            self.assertEqual(1, preflight_after["material_count"])

            # Close evidence_resolution task
            work_order_path = product / "tasks" / res_task["id"] / "work-order.json"
            wo = json.loads(work_order_path.read_text(encoding="utf-8"))
            wo["state"] = "closed"
            write_json(work_order_path, wo)

            # Now draft_section task can be created
            draft_task = create_task(product, "draft_section", "P01", None, False)
            self.assertEqual("draft_section", draft_task["operation"])


if __name__ == "__main__":
    unittest.main()
