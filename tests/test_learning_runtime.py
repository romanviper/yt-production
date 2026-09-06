from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from learning_runtime.run import load_scenario, run_scenario
from learning_runtime.stages import STAGE_ORDER, validate_scenario


class LearningRuntimeTests(unittest.TestCase):
    def test_frozen_scenario_has_minimal_stage_order(self):
        scenario = load_scenario("p01-mvp")
        self.assertEqual(tuple(scenario["stage_order"]), STAGE_ORDER)
        self.assertEqual(set(scenario["stages"]), set(STAGE_ORDER))

    def test_rejects_topology_drift(self):
        scenario = load_scenario("p01-mvp")
        mutated = dict(scenario)
        mutated["stage_order"] = ["plan", "truth", "write", "product"]
        with self.assertRaises(ValueError):
            validate_scenario(mutated)

    def test_smoke_run_materializes_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            manifest = run_scenario("p01-mvp", root)
            self.assertEqual(manifest["status"], "SMOKE_REPLAY_COMPLETE")
            self.assertEqual([node["stage"] for node in manifest["nodes"]], list(STAGE_ORDER))

            parent = None
            for stage in STAGE_ORDER:
                stage_dir = root / stage
                self.assertTrue((stage_dir / "input.json").is_file())
                self.assertTrue((stage_dir / "manifest.json").is_file())
                node = json.loads((stage_dir / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(node["parent_node_id"], parent)
                self.assertFalse(node["trace_available"])
                parent = node["node_id"]

            truth = json.loads((root / "truth" / "output.json").read_text(encoding="utf-8"))
            self.assertEqual(truth["status"], "REFERENCE_ONLY_NOT_REEVALUATED")
            self.assertIn("LEGACY_UNTRUSTED", truth["fixture_trust"])

    def test_existing_run_requires_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            run_scenario("p01-mvp", root)
            with self.assertRaises(FileExistsError):
                run_scenario("p01-mvp", root)


if __name__ == "__main__":
    unittest.main()
