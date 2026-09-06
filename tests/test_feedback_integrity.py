import inspect
import tempfile
import unittest
from pathlib import Path

from learning_runtime import artifacts
from learning_runtime.whitebox import EvidenceError, diagnose_failure


class FeedbackIntegrityTests(unittest.TestCase):
    def _plan(self):
        return {"beats": [{"id": "B1", "function": "x", "listener_after": "resolved lesson"}]}

    def _writer(self, quote="bad", deviations=None):
        return {"beat_execution": [{"beat_id": "B1", "status": "REALIZED", "candidate_quote": quote}], "deviations": deviations or []}

    def _failure(self, *, symptom_present=True, fields=None, observation="resolved lesson is predeclared"):
        return {
            "failure_id": "F",
            "symptom": "X",
            "candidate_quote": "bad",
            "plan_observation": {
                "symptom_present": symptom_present,
                "fields": fields or ["listener_after"],
                "observation": observation,
            },
        }

    def test_diagnosis_requires_actual_candidate_text(self):
        self.assertIn("candidate_text", inspect.signature(diagnose_failure).parameters)

    def test_empty_writer_quote_is_rejected(self):
        with self.assertRaises(EvidenceError) as ctx:
            diagnose_failure(candidate_text="bad", plan=self._plan(), writer_report=self._writer(""), failure=self._failure())
        self.assertEqual(ctx.exception.code, "EMPTY_WRITER_QUOTE")

    def test_duplicate_writer_quote_is_ambiguous_without_locator(self):
        plan = {"beats": [{"id": "B1", "listener_after": "x"}, {"id": "B2", "listener_after": "x"}]}
        writer = {
            "beat_execution": [
                {"beat_id": "B1", "status": "REALIZED", "candidate_quote": "bad"},
                {"beat_id": "B2", "status": "REALIZED", "candidate_quote": "bad"},
            ],
            "deviations": [],
        }
        failure = self._failure(fields=["listener_after"], observation="x")
        with self.assertRaises(EvidenceError) as ctx:
            diagnose_failure(candidate_text="bad and bad", plan=plan, writer_report=writer, failure=failure)
        self.assertEqual(ctx.exception.code, "AMBIGUOUS_SPAN")

    def test_failure_quote_missing_from_actual_output_is_rejected(self):
        with self.assertRaises(EvidenceError) as ctx:
            diagnose_failure(candidate_text="different text", plan=self._plan(), writer_report=self._writer(), failure=self._failure())
        self.assertEqual(ctx.exception.artifact, "failure")
        self.assertEqual(ctx.exception.code, "SPAN_NOT_FOUND")

    def test_writer_report_from_different_candidate_is_rejected(self):
        writer = self._writer("different writer text")
        with self.assertRaises(EvidenceError) as ctx:
            diagnose_failure(candidate_text="bad", plan=self._plan(), writer_report=writer, failure=self._failure())
        self.assertEqual(ctx.exception.artifact, "writer_report")
        self.assertEqual(ctx.exception.code, "SPAN_NOT_FOUND")

    def test_boolean_only_change_does_not_flip_attribution(self):
        a = diagnose_failure(candidate_text="bad", plan=self._plan(), writer_report=self._writer(), failure=self._failure(symptom_present=True))
        b = diagnose_failure(candidate_text="bad", plan=self._plan(), writer_report=self._writer(), failure=self._failure(symptom_present=False))
        self.assertEqual(a.classification, b.classification)
        self.assertEqual(a.classification, "PLAN_REGION_SUSPECT")
        self.assertEqual(a.confidence, "MEDIUM")

    def test_irrelevant_deviation_does_not_force_writer_fault(self):
        writer = self._writer(deviations=[{"beat_id": "B1", "type": "PUNCTUATION", "symptom_relevance": "IRRELEVANT", "evidence": "comma only"}])
        result = diagnose_failure(candidate_text="bad", plan=self._plan(), writer_report=writer, failure=self._failure())
        self.assertEqual(result.classification, "PLAN_REGION_SUSPECT")
        self.assertEqual(result.suspected_regions, ["PLAN"])

    def test_relevant_writer_deviation_keeps_multiple_suspects(self):
        writer = self._writer(deviations=[{"beat_id": "B1", "type": "SEMANTIC", "symptom_relevance": "RELEVANT", "evidence": "Writer inserted a resolved lesson inside the mapped span."}])
        result = diagnose_failure(candidate_text="bad", plan=self._plan(), writer_report=writer, failure=self._failure())
        self.assertEqual(result.classification, "MULTIPLE_REGIONS_SUSPECT")
        self.assertEqual(result.suspected_regions, ["PLAN", "WRITE"])

    def test_missing_referenced_plan_field_is_stale_evidence(self):
        with self.assertRaises(EvidenceError) as ctx:
            diagnose_failure(candidate_text="bad", plan=self._plan(), writer_report=self._writer(), failure=self._failure(fields=["missing_field"]))
        self.assertEqual(ctx.exception.code, "PLAN_EVIDENCE_STALE")

    def test_raw_hash_diff_but_crlf_normalization_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lf = root / "lf.txt"
            crlf = root / "crlf.txt"
            lf.write_bytes(b"a\nb\n")
            crlf.write_bytes(b"a\r\nb\r\n")
            expected = artifacts.artifact_identity(lf)
            result = artifacts.verify_artifact_identity(crlf, expected)
            self.assertEqual(result["status"], "TEXT_MATCH_RAW_DIFF_ALLOWED_NORMALIZATION")
            self.assertNotEqual(expected["raw_sha256"], result["observed"]["raw_sha256"])

    def test_one_word_change_fails_normalized_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = root / "a.txt"
            b = root / "b.txt"
            a.write_text("one two\n", encoding="utf-8")
            b.write_text("one three\n", encoding="utf-8")
            result = artifacts.verify_artifact_identity(b, artifacts.artifact_identity(a))
            self.assertEqual(result["status"], "CONTENT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
