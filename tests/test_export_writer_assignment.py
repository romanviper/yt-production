import json
import tempfile
import unittest
from pathlib import Path

from scripts import learning
from scripts.export_writer_assignment import EXPORT_SCHEMA, export_assignment


class PortableWriterAssignmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.overlay = self.root / "P01.json"
        self.substrate = self.root / "historical-substrate.json"
        self.overlay.write_text(json.dumps({
            "section": "P01",
            "historical_territory": "territory",
            "historical_change": {"from": "a", "to": "b"},
            "historical_substrate_ids": ["HS-P01-0001"],
        }), encoding="utf-8")
        self.substrate.write_text(json.dumps({
            "section": "P01",
            "historical_territory": "territory",
            "historical_change": {"from": "a", "to": "b"},
            "primitives": [{"id": "HS-P01-0001"}],
            "boundaries": [],
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self):
        run = self.root / "run"
        learning.prepare_run(
            run,
            owner_request="TEST_ONLY portable writer handoff",
            overlay_path=self.overlay,
            substrate_path=self.substrate,
            test_only=True,
            code_ref="test-export",
        )
        learning.propose_budget(
            run,
            budget_id="B-export",
            initial_cap_seconds=2400,
            allocations={"sol_repo": 1200, "writer_gemini": 600, "writer_sol": 600},
            scope="TEST_ONLY export",
            code_ref="test-export",
        )
        learning.record_budget_decision(
            run,
            request_id="B-export:initial",
            decision="APPROVED",
            owner_text="Owner approves TEST_ONLY budget.",
            source_ref="chat:test",
        )
        plan = self.root / "plan.json"
        plan.write_text(json.dumps({
            "section": "P01",
            "telling_scope": "Show the material constraint.",
            "source_refs": ["overlay:P01", "HS-P01-0001"],
            "stop_condition": "Stop after the constraint is legible.",
        }), encoding="utf-8")
        learning.freeze_plan(
            run,
            session_id="sol-repo-001",
            source_file=plan,
            declared_reason="TEST_ONLY plan",
            uncertainty="Writer wording remains open.",
            duration_seconds=10,
            timestamp_source="TEST_CONTROLLER_DURATION",
        )
        return run

    def test_export_contains_only_selected_writer_assignment_and_hashes(self):
        run = self._run()
        out = self.root / "portable-sol"
        manifest = export_assignment(run, actor="writer_sol", out_dir=out)
        self.assertEqual(manifest["schema_version"], EXPORT_SCHEMA)
        self.assertEqual(manifest["actor"], "writer_sol")
        self.assertEqual(manifest["approved_budget_seconds"], 600)
        self.assertFalse(manifest["other_writer_assignment_exported"])
        self.assertTrue((out / "packet.json").is_file())
        self.assertTrue((out / "self-report-contract.json").is_file())
        self.assertTrue((out / "assignment-manifest.json").is_file())
        self.assertTrue((out / "START-HERE.md").is_file())
        self.assertEqual(manifest["packet_sha256"], learning.sha256_file(out / "packet.json"))
        self.assertEqual(manifest["self_report_contract_sha256"], learning.sha256_file(out / "self-report-contract.json"))
        packet = learning.read_json(out / "packet.json")
        self.assertEqual(packet["role"], "writer_sol")
        self.assertNotIn("writer_gemini", json.dumps(packet))
        self.assertIn("Do not scan the repository", (out / "START-HERE.md").read_text(encoding="utf-8"))

    def test_export_refuses_nonempty_destination(self):
        run = self._run()
        out = self.root / "portable-sol"
        out.mkdir()
        (out / "old.txt").write_text("stale", encoding="utf-8")
        with self.assertRaises(learning.LearningError) as ctx:
            export_assignment(run, actor="writer_sol", out_dir=out)
        self.assertEqual(ctx.exception.code, "EXPORT_DIR_NOT_EMPTY")


if __name__ == "__main__":
    unittest.main()
