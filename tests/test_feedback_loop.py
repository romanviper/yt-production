import json
import tempfile
import unittest
from pathlib import Path

from learning_runtime.feedback import (
    FeedbackError,
    _replace_only_beat,
    ingest_measurement,
    prepare_case,
    show_state,
    validate_guided_artifact,
    verify_case_bundle,
)

ROOT = Path(__file__).resolve().parents[1]


class FeedbackLoopTests(unittest.TestCase):
    def _prepare(self, tmp: str):
        case_dir = Path(tmp) / "case"
        result = prepare_case("p01-rootcause-01", case_dir)
        return case_dir, result

    def _measurement(
        self,
        case_dir: Path,
        *,
        measurement_id="M001",
        preference="YES",
        symptom=None,
        candidate_hash=None,
        regressions=None,
        invariants=None,
        scope=None,
        case_id=None,
        supersedes=None,
    ):
        case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
        payload = {
            "schema_version": "1.0.0",
            "measurement_id": measurement_id,
            "case_id": case_id or case["case_id"],
            "candidate_text_sha256": candidate_hash or case["candidate"]["identity"]["text_sha256"],
            "reviewer_id": "TEST-REVIEWER",
            "trust_mode": "TEST_ONLY",
            "scope": scope or case["measurement_scope"],
            "preference_result": preference,
        }
        if symptom is not None:
            payload["symptom_observation"] = symptom
        if invariants is not None:
            payload["invariants"] = invariants
        if regressions is not None:
            payload["regressions"] = regressions
        if supersedes is not None:
            payload["supersedes"] = supersedes
        path = case_dir.parent / f"measurement-{measurement_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def test_prepare_builds_frozen_b03_case_and_waits_for_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, result = self._prepare(tmp)
            self.assertEqual(result["status"], "AWAITING_MEASUREMENT")
            self.assertEqual(result["verification"]["status"], "VALID")
            case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
            self.assertEqual(case["plan_change"]["allowed_beat_ids"], ["B03"])
            self.assertEqual(case["candidate"]["independence"], "NONE")
            self.assertEqual(case["standard"]["product_review_blinding"], "DIAGNOSTIC_HYPOTHESIS_HIDDEN_PRE_VOTE")
            self.assertTrue((case_dir / "standard/p01-rootcause-01.json").exists())
            initial = json.loads((case_dir / "feedback/initial.json").read_text(encoding="utf-8"))
            self.assertEqual(initial["symptom_observation"], "AWAITING_MEASUREMENT")
            self.assertEqual(initial["improvement"], "NOT_ESTABLISHED")

    def test_plan_patch_outside_b03_is_rejected(self):
        baseline = {"beats": [{"id": "B03", "listener_after": "old"}, {"id": "B04", "listener_after": "other"}]}
        with self.assertRaises(FeedbackError) as ctx:
            _replace_only_beat(baseline, {"id": "B04", "listener_after": "changed"}, "B03")
        self.assertEqual(ctx.exception.code, "PLAN_SCOPE_VIOLATION")

    def test_static_phase3_comparison_is_actually_grounded(self):
        session = ROOT / "benchmarks/p01/review-sessions/phase3-p3-f01-rerun-guided.json"
        result = validate_guided_artifact(session, root=ROOT)
        self.assertEqual(result["format"], "COMPARISON")
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["owner_measurement_pending"])

    def test_empty_guided_session_fails_structure(self):
        source = json.loads((ROOT / "benchmarks/p01/review-sessions/owner-pilot-01-guided.json").read_text(encoding="utf-8"))
        source["micro_units"] = []
        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp) / "empty.json"
            session.write_text(json.dumps(source, ensure_ascii=False), encoding="utf-8")
            result = validate_guided_artifact(session, root=ROOT)
        self.assertTrue(any("minItems" in error for error in result["errors"]))

    def test_fake_guided_locator_and_quote_fail_grounding(self):
        single = json.loads((ROOT / "benchmarks/p01/review-sessions/owner-pilot-01-guided.json").read_text(encoding="utf-8"))
        single["micro_units"][0]["source_locator"] = "paragraph 999"
        comparison = json.loads((ROOT / "benchmarks/p01/review-sessions/phase3-p3-f01-rerun-guided.json").read_text(encoding="utf-8"))
        comparison["new"]["excerpt"] = "THIS QUOTE DOES NOT EXIST"
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.json"
            b = Path(tmp) / "b.json"
            a.write_text(json.dumps(single, ensure_ascii=False), encoding="utf-8")
            b.write_text(json.dumps(comparison, ensure_ascii=False), encoding="utf-8")
            self.assertTrue(any("LOCATOR_OUT_OF_RANGE" in e for e in validate_guided_artifact(a, root=ROOT)["errors"]))
            self.assertTrue(any("excerpt not grounded" in e for e in validate_guided_artifact(b, root=ROOT)["errors"]))

    def test_preference_yes_without_symptom_does_not_claim_symptom_reduction(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            feedback = ingest_measurement(case_dir, self._measurement(case_dir, preference="YES"))
            self.assertEqual(feedback["preference_result"], "YES")
            self.assertEqual(feedback["symptom_observation"], "NOT_MEASURED")
            self.assertEqual(feedback["next_action"], "COLLECT_SYMPTOM_OBSERVATION_KEEP_INTERVENTION")
            self.assertEqual(feedback["improvement"], "NOT_ESTABLISHED")

    def test_uncertain_preference_keeps_intervention_and_requests_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            feedback = ingest_measurement(case_dir, self._measurement(case_dir, preference="UNCERTAIN"))
            self.assertEqual(feedback["next_action"], "CLARIFY_OR_COLLECT_MORE_OBSERVATION_KEEP_INTERVENTION")
            self.assertEqual(feedback["symptom_observation"], "NOT_MEASURED")

    def test_wrong_target_revisits_target_without_rewriting_plan_or_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            feedback = ingest_measurement(case_dir, self._measurement(case_dir, preference="WRONG_TARGET"))
            self.assertEqual(feedback["next_action"], "REVISIT_TARGET_DEFINITION_KEEP_OUTPUT_FROZEN")

    def test_separate_symptom_observation_can_support_bounded_hypothesis(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            feedback = ingest_measurement(case_dir, self._measurement(case_dir, preference="YES", symptom="REDUCED"))
            self.assertEqual(feedback["symptom_observation"], "REDUCED")
            self.assertEqual(feedback["next_action"], "KEEP_BOUNDED_HYPOTHESIS_FOR_NEXT_INDEPENDENT_TEST")
            self.assertEqual(feedback["improvement"], "NOT_ESTABLISHED")

    def test_invariants_merge_with_case_defaults_when_measurement_is_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            feedback = ingest_measurement(case_dir, self._measurement(case_dir, invariants={"artifact_clarity": "PASS"}))
            self.assertEqual(feedback["invariant_state"]["artifact_clarity"], "PASS")
            self.assertEqual(feedback["invariant_state"]["truth"], "NOT_MEASURED")
            self.assertEqual(feedback["invariant_state"]["sequence_continuity"], "NOT_MEASURED")

    def test_stale_candidate_wrong_case_and_wrong_scope_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            bad = [
                (self._measurement(case_dir, measurement_id="STALE", candidate_hash="0" * 64), "STALE_MEASUREMENT_CANDIDATE"),
                (self._measurement(case_dir, measurement_id="CASE", case_id="OLD-CASE"), "MEASUREMENT_CASE_MISMATCH"),
                (self._measurement(case_dir, measurement_id="SCOPE", scope="WHOLE_SECTION"), "MEASUREMENT_SCOPE_MISMATCH"),
            ]
            for path, code in bad:
                with self.assertRaises(FeedbackError) as ctx:
                    ingest_measurement(case_dir, path)
                self.assertEqual(ctx.exception.code, code)

    def test_duplicate_measurement_id_is_rejected_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            first = self._measurement(case_dir, measurement_id="M001", preference="YES")
            ingest_measurement(case_dir, first)
            frozen = (case_dir / "measurements/M001.json").read_text(encoding="utf-8")
            second = self._measurement(case_dir, measurement_id="M001", preference="NO")
            with self.assertRaises(FeedbackError) as ctx:
                ingest_measurement(case_dir, second)
            self.assertEqual(ctx.exception.code, "MEASUREMENT_ID_ALREADY_EXISTS")
            self.assertEqual((case_dir / "measurements/M001.json").read_text(encoding="utf-8"), frozen)

    def test_superseding_measurement_preserves_history_and_becomes_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            ingest_measurement(case_dir, self._measurement(case_dir, measurement_id="M001", preference="UNCERTAIN"))
            ingest_measurement(case_dir, self._measurement(case_dir, measurement_id="M002", preference="YES", symptom="REDUCED", supersedes="M001"))
            current = json.loads((case_dir / "current.json").read_text(encoding="utf-8"))
            self.assertEqual(current["measurement_ids"], ["M001", "M002"])
            self.assertEqual(current["current_measurement_id"], "M002")
            self.assertTrue((case_dir / "measurements/M001.json").exists())
            self.assertTrue((case_dir / "feedback/M001.json").exists())
            self.assertEqual(show_state(case_dir)["current_feedback"]["measurement_id"], "M002")

    def test_parallel_measurements_are_preserved_and_leave_resolution_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            case_dir, _ = self._prepare(tmp)
            ingest_measurement(case_dir, self._measurement(case_dir, measurement_id="R1", preference="YES"))
            ingest_measurement(case_dir, self._measurement(case_dir, measurement_id="R2", preference="NO"))
            current = json.loads((case_dir / "current.json").read_text(encoding="utf-8"))
            self.assertEqual(current["resolution"], "MULTIPLE_MEASUREMENTS_UNRESOLVED")
            self.assertIsNone(current["current_measurement_id"])
            self.assertEqual(sorted(current["measurement_ids"]), ["R1", "R2"])
            self.assertEqual(verify_case_bundle(case_dir)["status"], "VALID")

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
