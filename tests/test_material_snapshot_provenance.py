"""Tests for immutable material snapshot and provenance binding."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.common import sha256
from scripts.draft_evidence import DraftEvidenceBroker, EvidenceAccessError
from scripts.draft_lifecycle_contract import validate_evidence_trace
from scripts.materialize_sections import materialize
from scripts.task import create_task, verify_task
from scripts.validate import validate_product
from test_material_aware_handoff import make_direct_authorship_fixture, write_json


class MaterialSnapshotProvenanceTests(unittest.TestCase):
    def test_task_creation_binds_material_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)

            # Add section materials.json
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

            task = create_task(product, "draft_section", "P01", None, False)
            snapshot_path = product / "03_sections" / "P01" / "material-snapshot.json"
            self.assertTrue(snapshot_path.is_file())

            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            self.assertEqual(1, snapshot["schema_version"])
            self.assertEqual("P01", snapshot["section"])
            self.assertEqual(sha256(sec_mat), snapshot["materials_sha256"])

            # Verify work-order and packet bind the snapshot sha256
            self.assertEqual(sha256(snapshot_path), task["material_snapshot_sha256"])
            packet = json.loads((product / "tasks" / task["id"] / "packet.json").read_text(encoding="utf-8"))
            self.assertEqual(sha256(snapshot_path), packet["evidence_access"]["material_snapshot_sha256"])

            # Verify task is currently valid
            errors = verify_task(product, task["id"])
            self.assertEqual([], errors)

            # Broker can call capabilities
            broker = DraftEvidenceBroker(product, task["id"])
            attestation = broker.call("attest_scope")
            self.assertIn("scope_attestation", attestation)

            # Trace has material_snapshot_sha256
            trace_errors = validate_evidence_trace(product, task["id"])
            self.assertEqual([], trace_errors)

            # Post-creation mutation of material-snapshot.json invalidates task
            write_json(
                snapshot_path,
                {
                    "schema_version": 1,
                    "section": "P01",
                    "created_at": "2026-09-03T00:00:00Z",
                    "materials_sha256": "tampered",
                    "materials": [],
                },
            )

            # verify_task must detect mutation
            errors_after = verify_task(product, task["id"])
            self.assertTrue(any("material snapshot is stale / mutated" in err for err in errors_after))

            # broker.call must reject with EvidenceAccessError
            with self.assertRaises(EvidenceAccessError) as ctx:
                broker.call("attest_scope")
            self.assertIn("material snapshot has mutated since task creation", str(ctx.exception))

            # validate_product must report hash mismatch
            issues = validate_product(product)
            self.assertTrue(any("material snapshot hash mismatch" in issue.message for issue in issues))


if __name__ == "__main__":
    unittest.main()
