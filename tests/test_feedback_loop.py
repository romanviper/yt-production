import json
import tempfile
import unittest
from pathlib import Path

from learning_runtime.feedback import FeedbackError, ingest_measurement, prepare_case, validate_guided_artifact, verify_case_bundle

ROOT = Path(__file__).resolve().parents[1]


class FeedbackLoopTests(unittest.TestCase):
    def _prepare(self, tmp: str):
        case_dir = Path(tmp) / "case"
        result = prepare_case("p01-rootcause-01", case_dir)
        return case_dir, result

    def _measurement(self, case_dir: Path, *, result="YES", candidate_hash=None, regressions=None, invariants=None):
        case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
        payload = {
            "schema_version": "1.0.0",
            "case_id": case["case_id"],
            "candidate_text_sha256": candidate_hash or case["candidate"]["identity"]["text_sha256"],
            "reviewer_id": "TEST-REVIEWER",
            "trust_mode": "TEST_ONLY",
            "scope": case["measurement_scope"],
            "result": result,
            "invariants": invariants or case["invariants"],
            "regressions": regressions or [],
        }
        path = case_dir.parent / f"measurement-{result}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def test_prepare_builds_frozen_b03_case_and_waits_for_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, result = self._prepare(tmp)
            self.assertEqual(result["status"], "AWAITING_MEASUREMENT")
            self.assertEqual(result["verification"]["status"], "VALID")
            case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
            self.assertEqual(case["plan_change"]["allowed_beat_ids"], ["B03"])
            self.assertEqual(case["plan_change"]["changed_beat_ids"], ["B03"])
            self.assertEqual(case["candidate"]["independence"], "NONE")
            feedback = json.loads((case_dir / "feedback.json").read_text(encoding="utf-8"))
            self.assertEqual(feedback["status"], "AWAITING_MEASUREMENT")
            self.assertEqual(feedback["improvement"], "NOT_ESTABLISHED")

    def test_static_phase3_comparison_is_actually_grounded(self):
        session = ROOT / "benchmarks/p01/review-sessions/phase3-p3-f01-rerun-guided.json"
        result = validate_guided_artifact(session, root=ROOT)
        self.assertEqual(result["format"], "COMPARISON")
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["owner_measurement_pending"])

    def test_positive_test_measurement_changes_symptom_delta_not_overall_gain(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            feedback = ingest_measurement(case_dir, self._measurement(case_dir, result="YES"))
            self.assertEqual(feedback["symptom_delta"], "DIRECTIONALLY_REDUCED_NOT_RESOLVED")
            self.assertEqual(feedback["measurement_authority"], "TEST_ONLY")
            self.assertEqual(feedback["improvement"], "NOT_ESTABLISHED")

    def test_negative_measurement_changes_feedback(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            feedback = ingest_measurement(case_dir, self._measurement(case_dir, result="NO"))
            self.assertEqual(feedback["symptom_delta"], "NOT_REDUCED")
            self.assertEqual(feedback["next_action"], "REJECT_OR_REVISE_BOUNDED_INTERVENTION")

    def test_stale_candidate_measurement_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            measurement = self._measurement(case_dir, result="YES", candidate_hash="0" * 64)
            with self.assertRaises(FeedbackError) as ctx:
                ingest_measurement(case_dir, measurement)
            self.assertEqual(ctx.exception.code, "STALE_MEASUREMENT_CANDIDATE")

    def test_regression_and_missing_truth_remain_visible_even_when_preferred(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            invariants = {
                "truth": "MISSING",
                "artifact_clarity": "PASS",
                "sequence_continuity": "NOT_MEASURED",
                "whole_section_quality": "OUT_OF_SCOPE",
            }
            measurement = self._measurement(case_dir, result="YES", regressions=["TRUTH_NOT_VERIFIED"], invariants=invariants)
            feedback = ingest_measurement(case_dir, measurement)
            self.assertEqual(feedback["symptom_delta"], "DIRECTIONALLY_REDUCED_NOT_RESOLVED")
            self.assertIn("TRUTH_NOT_VERIFIED", feedback["regressions"])
            self.assertEqual(feedback["invariant_state"]["truth"], "MISSING")
            self.assertEqual(feedback["improvement"], "NOT_ESTABLISHED")

    def test_case_bundle_detects_tampering_after_prepare(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            output = case_dir / "revised-output.md"
            output.write_text(output.read_text(encoding="utf-8") + " changed", encoding="utf-8")
            result = verify_case_bundle(case_dir)
            self.assertEqual(result["status"], "INVALID")
            self.assertTrue(any(e["code"] == "CASE_ARTIFACT_CHANGED" for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
