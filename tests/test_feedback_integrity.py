import inspect
import unittest

from learning_runtime import artifacts
from learning_runtime.whitebox import diagnose_failure


class FeedbackIntegrityRedTests(unittest.TestCase):
    def _plan(self):
        return {"beats": [{"id": "B1", "function": "x", "listener_after": "resolved lesson"}]}

    def test_diagnosis_requires_actual_candidate_text(self):
        self.assertIn("candidate_text", inspect.signature(diagnose_failure).parameters)

    def test_empty_writer_quote_does_not_map(self):
        writer = {"beat_execution": [{"beat_id": "B1", "status": "REALIZED", "candidate_quote": ""}], "deviations": []}
        failure = {"failure_id": "F", "symptom": "X", "candidate_quote": "bad", "plan_observation": {"symptom_present": True, "fields": ["listener_after"], "observation": "resolved lesson is predeclared"}}
        result = diagnose_failure(plan=self._plan(), writer_report=writer, failure=failure)
        self.assertNotEqual(result.classification, "PLAN_FAILURE")

    def test_duplicate_writer_quote_is_not_first_match_wins(self):
        plan = {"beats": [{"id": "B1", "listener_after": "x"}, {"id": "B2", "listener_after": "x"}]}
        writer = {"beat_execution": [
            {"beat_id": "B1", "status": "REALIZED", "candidate_quote": "bad"},
            {"beat_id": "B2", "status": "REALIZED", "candidate_quote": "bad"},
        ], "deviations": []}
        failure = {"failure_id": "F", "symptom": "X", "candidate_quote": "bad", "plan_observation": {"symptom_present": True, "fields": ["listener_after"], "observation": "x"}}
        result = diagnose_failure(plan=plan, writer_report=writer, failure=failure)
        self.assertEqual(result.classification, "INCONCLUSIVE_TRACE")

    def test_boolean_only_change_does_not_flip_attribution(self):
        writer = {"beat_execution": [{"beat_id": "B1", "status": "REALIZED", "candidate_quote": "bad"}], "deviations": []}
        base = {"failure_id": "F", "symptom": "X", "candidate_quote": "bad", "plan_observation": {"fields": ["listener_after"], "observation": "resolved lesson is predeclared"}}
        a = {**base, "plan_observation": {**base["plan_observation"], "symptom_present": True}}
        b = {**base, "plan_observation": {**base["plan_observation"], "symptom_present": False}}
        self.assertEqual(
            diagnose_failure(plan=self._plan(), writer_report=writer, failure=a).classification,
            diagnose_failure(plan=self._plan(), writer_report=writer, failure=b).classification,
        )

    def test_irrelevant_deviation_does_not_force_writer_fault(self):
        writer = {
            "beat_execution": [{"beat_id": "B1", "status": "REALIZED", "candidate_quote": "bad"}],
            "deviations": [{"beat_id": "B1", "type": "PUNCTUATION", "symptom_relevance": "IRRELEVANT", "evidence": "comma only"}],
        }
        failure = {"failure_id": "F", "symptom": "X", "candidate_quote": "bad", "plan_observation": {"symptom_present": True, "fields": ["listener_after"], "observation": "resolved lesson is predeclared"}}
        result = diagnose_failure(plan=self._plan(), writer_report=writer, failure=failure)
        self.assertNotEqual(result.classification, "REALIZATION_FAILURE")

    def test_missing_referenced_plan_field_cannot_produce_plan_high(self):
        writer = {"beat_execution": [{"beat_id": "B1", "status": "REALIZED", "candidate_quote": "bad"}], "deviations": []}
        failure = {"failure_id": "F", "symptom": "X", "candidate_quote": "bad", "plan_observation": {"symptom_present": True, "fields": ["missing_field"], "observation": "claims missing field supports symptom"}}
        result = diagnose_failure(plan=self._plan(), writer_report=writer, failure=failure)
        self.assertFalse(result.classification == "PLAN_FAILURE" and result.confidence == "HIGH")

    def test_artifact_identity_exposes_raw_and_normalized_text_hashes(self):
        self.assertTrue(hasattr(artifacts, "artifact_identity"))
        self.assertTrue(hasattr(artifacts, "verify_artifact_identity"))


if __name__ == "__main__":
    unittest.main()
