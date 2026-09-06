import json
import tempfile
import unittest
from pathlib import Path

from learning_runtime.phase3 import run_phase3, verify_run_bundle
from learning_runtime.whitebox import EvidenceError, diagnose_failure

ROOT = Path(__file__).resolve().parents[1]


class Phase3WhiteboxTests(unittest.TestCase):
    def _round1(self):
        plan = json.loads((ROOT / "experiments/p01-writer-trace-v2/runs/round-01/writing-plan.json").read_text(encoding="utf-8"))
        writer = json.loads((ROOT / "experiments/p01-writer-trace-v2/runs/round-01/writer-report.json").read_text(encoding="utf-8"))
        failure = json.loads((ROOT / "learning_runtime/scenarios/p01-rootcause-01.failure.json").read_text(encoding="utf-8"))
        candidate = (ROOT / "experiments/p01-writer-trace-v2/runs/round-01/candidate.md").read_text(encoding="utf-8")
        return candidate, plan, writer, failure

    def test_round1_failure_maps_to_b03_with_bounded_plan_suspect(self):
        candidate, plan, writer, failure = self._round1()
        result = diagnose_failure(candidate_text=candidate, plan=plan, writer_report=writer, failure=failure)
        self.assertEqual(result.beat_id, "B03")
        self.assertEqual(result.mapping_status, "VALIDATED_EXACT")
        self.assertEqual(result.mapping_confidence, "HIGH")
        self.assertEqual(result.classification, "PLAN_REGION_SUSPECT")
        self.assertEqual(result.confidence, "MEDIUM")
        self.assertIn("Writer contribution is not excluded", " ".join(result.limitations))

    def test_relevant_writer_deviation_can_nominate_write_without_boolean_rule(self):
        plan = {"beats": [{"id": "B1", "function": "x", "listener_after": "x"}]}
        writer = {
            "beat_execution": [{"beat_id": "B1", "status": "REALIZED", "candidate_quote": "bad"}],
            "deviations": [{"beat_id": "B1", "type": "SEMANTIC", "symptom_relevance": "RELEVANT", "evidence": "inserted same symptom"}],
        }
        failure = {"failure_id": "F", "symptom": "X", "candidate_quote": "bad", "plan_observation": {"fields": ["listener_after"], "observation": "plan may also contribute", "symptom_present": False}}
        result = diagnose_failure(candidate_text="bad", plan=plan, writer_report=writer, failure=failure)
        self.assertEqual(result.classification, "MULTIPLE_REGIONS_SUSPECT")

    def test_missing_mapping_is_typed_invalid_evidence(self):
        with self.assertRaises(EvidenceError) as ctx:
            diagnose_failure(candidate_text="actual", plan={"beats": []}, writer_report={"beat_execution": []}, failure={"failure_id": "F", "symptom": "X", "candidate_quote": "absent"})
        self.assertEqual(ctx.exception.code, "SPAN_NOT_FOUND")
        self.assertEqual(ctx.exception.artifact, "failure")

    def test_phase3_run_materializes_snapshots_traces_and_valid_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            manifest = run_phase3("p01-rootcause-01", out)
            self.assertEqual(manifest["status"], "WHITEBOX_TRACE_COMPLETE")
            self.assertEqual(manifest["attribution"], "PLAN_REGION_SUSPECT")
            self.assertTrue((out / "input-snapshot/candidate.md").exists())
            self.assertTrue((out / "plan/trace.jsonl").exists())
            self.assertTrue((out / "write/trace.jsonl").exists())
            diagnosis = json.loads((out / "diagnosis.json").read_text(encoding="utf-8"))
            self.assertEqual(diagnosis["root_cause_status"], "BOUNDED_HYPOTHESIS_NOT_CAUSAL_PROOF")
            self.assertEqual(diagnosis["mapping_confidence"], "HIGH")
            self.assertEqual(diagnosis["attribution_confidence"], "MEDIUM")
            plan_manifest = json.loads((out / "plan/manifest.json").read_text(encoding="utf-8"))
            write_manifest = json.loads((out / "write/manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(plan_manifest["trace_available"])
            self.assertTrue(write_manifest["trace_available"])
            self.assertEqual(verify_run_bundle(out)["status"], "VALID")

    def test_bundle_detects_post_freeze_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            run_phase3("p01-rootcause-01", out)
            failure_snapshot = out / "input-snapshot/failure.json"
            failure_snapshot.write_text(failure_snapshot.read_text(encoding="utf-8") + " ", encoding="utf-8")
            result = verify_run_bundle(out)
            self.assertEqual(result["status"], "INVALID")
            self.assertTrue(any(e["code"] == "BUNDLE_ARTIFACT_CHANGED" for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
