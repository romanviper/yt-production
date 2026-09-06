import json
import tempfile
import unittest
from pathlib import Path

from learning_runtime.phase3 import run_phase3
from learning_runtime.whitebox import diagnose_failure

ROOT = Path(__file__).resolve().parents[1]


class Phase3WhiteboxTests(unittest.TestCase):
    def test_round1_failure_traces_to_plan(self):
        plan = json.loads((ROOT / "experiments/p01-writer-trace-v2/runs/round-01/writing-plan.json").read_text())
        writer = json.loads((ROOT / "experiments/p01-writer-trace-v2/runs/round-01/writer-report.json").read_text())
        failure = json.loads((ROOT / "learning_runtime/scenarios/p01-rootcause-01.failure.json").read_text())
        result = diagnose_failure(plan=plan, writer_report=writer, failure=failure)
        self.assertEqual(result.beat_id, "B03")
        self.assertEqual(result.classification, "PLAN_FAILURE")
        self.assertEqual(result.confidence, "HIGH")

    def test_writer_deviation_routes_to_realization(self):
        plan = {"beats": [{"id": "B1", "function": "x", "listener_after": "x"}]}
        writer = {"beat_execution": [{"beat_id": "B1", "status": "REALIZED", "candidate_quote": "bad"}], "deviations": [{"beat_id": "B1", "type": "MODIFIED"}]}
        failure = {"failure_id": "F", "symptom": "X", "candidate_quote": "bad", "plan_observation": {"symptom_present": True, "fields": ["listener_after"]}}
        result = diagnose_failure(plan=plan, writer_report=writer, failure=failure)
        self.assertEqual(result.classification, "REALIZATION_FAILURE")

    def test_missing_mapping_is_inconclusive(self):
        result = diagnose_failure(plan={"beats": []}, writer_report={"beat_execution": []}, failure={"failure_id": "F", "symptom": "X", "candidate_quote": "absent"})
        self.assertEqual(result.classification, "INCONCLUSIVE_TRACE")

    def test_phase3_run_materializes_plan_write_traces(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            manifest = run_phase3("p01-rootcause-01", out)
            self.assertEqual(manifest["diagnosis"], "PLAN_FAILURE")
            self.assertTrue((out / "plan/trace.jsonl").exists())
            self.assertTrue((out / "write/trace.jsonl").exists())
            diagnosis = json.loads((out / "diagnosis.json").read_text())
            self.assertEqual(diagnosis["root_cause_status"], "BOUNDED_REGION_NOT_FINAL_CAUSAL_PROOF")
            self.assertEqual(manifest["live_rerun_status"], "NOT_EXECUTED_NO_LIVE_AGENT_ADAPTER")


if __name__ == "__main__":
    unittest.main()
