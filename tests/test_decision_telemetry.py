import json
import tempfile
import unittest
from pathlib import Path

from learning_runtime.telemetry import (
    TelemetryError,
    read_telemetry,
    seal_execution,
    verify_execution_seal,
)
from learning_runtime.workspace import RoleWorkspaceBroker, create_workspace_run

ROOT = Path(__file__).resolve().parents[1]


class DecisionTelemetryTests(unittest.TestCase):
    def _brief(self):
        return json.loads((ROOT / "learning_runtime/briefs/p01-rootcause-01.json").read_text(encoding="utf-8"))

    def _run(self, tmp: str):
        return create_workspace_run(
            Path(tmp),
            "RUN-TEL-001",
            {"plan": "P1", "writer": "W1", "truth": "T1", "audit": "A1", "review": "R1"},
            self._brief(),
        )

    def _writer_decision(self, output_refs=None):
        return {
            "event_id": "W-D01",
            "event_type": "DECISION",
            "subject_refs": ["plan:B03", "evidence:E17"],
            "decision_type": "REALIZATION_STRATEGY",
            "chosen_action": "SHOW_CONDITION_BEFORE_INTERPRETATION",
            "rationale_summary": "Keep the listener on the material constraint before naming its broader interpretation.",
            "evidence_refs": ["plan:B03", "evidence:E17"],
            "alternatives_considered": ["STATE_PARADOX_EXPLICITLY"],
            "expected_effect": "The physical consequence earns the later interpretation.",
            "risks": ["The unit could become too implicit without a later interpretive beat."],
            "output_refs": output_refs or ["output/candidate.md"],
        }

    def test_record_event_adds_role_execution_and_monotonic_sequence(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            first = writer.record_event(self._writer_decision())
            second = writer.record_event(
                {
                    "event_id": "W-C02",
                    "event_type": "CHECKPOINT",
                    "subject_refs": ["output/candidate.md"],
                    "checkpoint": "B03_REALIZATION_COMPLETE",
                    "status": "READY_TO_FREEZE",
                    "artifact_refs": ["output/candidate.md"],
                }
            )
            self.assertEqual(first["sequence"], 1)
            self.assertEqual(second["sequence"], 2)
            self.assertEqual(first["role"], "writer")
            self.assertEqual(first["execution_id"], "W1")
            events = read_telemetry(run / "agents/writer/W1/output/telemetry.jsonl", expected_role="writer", expected_execution_id="W1")
            self.assertEqual([event["event_id"] for event in events], ["W-D01", "W-C02"])

    def test_private_chain_of_thought_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            event = self._writer_decision()
            event["chain_of_thought"] = "hidden internal reasoning"
            with self.assertRaises(TelemetryError) as ctx:
                writer.record_event(event)
            self.assertEqual(ctx.exception.code, "PRIVATE_REASONING_FIELD_FORBIDDEN")

    def test_writer_seal_requires_at_least_one_decision_even_if_filesystem_was_bypassed(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            # Deliberately bypass the broker to exercise seal-level fail-closed behavior.
            candidate = run / "agents/writer/W1/output/candidate.md"
            candidate.write_text("candidate", encoding="utf-8")
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            writer.record_event(
                {
                    "event_id": "W-C01",
                    "event_type": "CHECKPOINT",
                    "subject_refs": ["output/candidate.md"],
                    "checkpoint": "OUTPUT_WRITTEN",
                    "status": "READY",
                    "artifact_refs": ["output/candidate.md"],
                }
            )
            with self.assertRaises(TelemetryError) as ctx:
                seal_execution(run, role="writer", execution_id="W1", required_output_refs=["candidate.md"])
            self.assertEqual(ctx.exception.code, "DECISION_EVENT_REQUIRED_BEFORE_SEAL")

    def test_seal_rejects_primary_output_not_bound_to_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            writer.record_event(self._writer_decision(["output/candidate.md"]))
            writer.write_text("output/candidate.md", "candidate")
            # Directly materialize an unbound output to ensure the seal catches broker bypass.
            report = run / "agents/writer/W1/output/report.json"
            report.write_text("{}", encoding="utf-8")
            with self.assertRaises(TelemetryError) as ctx:
                seal_execution(run, role="writer", execution_id="W1", required_output_refs=["candidate.md", "report.json"])
            self.assertEqual(ctx.exception.code, "PRIMARY_OUTPUT_NOT_BOUND_TO_DECISION")

    def test_seal_hashes_telemetry_and_output_and_detects_direct_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            writer.record_event(self._writer_decision())
            candidate = writer.write_text("output/candidate.md", "candidate v1")
            seal = seal_execution(run, role="writer", execution_id="W1", required_output_refs=["candidate.md"])
            self.assertEqual(seal["status"], "SEALED_BEFORE_DOWNSTREAM_FEEDBACK")
            self.assertEqual(seal["decision_count"], 1)
            self.assertIn("prior DECISION", seal["output_binding_rule"])
            self.assertEqual(verify_execution_seal(run, role="writer", execution_id="W1")["status"], "VALID")
            candidate.write_text("candidate v2", encoding="utf-8")
            with self.assertRaises(TelemetryError) as ctx:
                verify_execution_seal(run, role="writer", execution_id="W1")
            self.assertEqual(ctx.exception.code, "SEALED_OUTPUT_CHANGED")

    def test_role_specific_decision_type_is_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            event = self._writer_decision()
            event["decision_type"] = "EVIDENCE_SELECTION"
            with self.assertRaises(TelemetryError) as ctx:
                writer.record_event(event)
            self.assertEqual(ctx.exception.code, "DECISION_TYPE_NOT_ALLOWED_FOR_ROLE")

    def test_decision_output_refs_must_be_bounded_final_output_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            event = self._writer_decision(["scratch/candidate.md"])
            with self.assertRaises(TelemetryError) as ctx:
                writer.record_event(event)
            self.assertEqual(ctx.exception.code, "INVALID_DECISION_OUTPUT_REF")

    def test_planner_can_record_information_order_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            planner = RoleWorkspaceBroker(run, "plan", "P1")
            event = planner.record_event(
                {
                    "event_id": "P-D01",
                    "event_type": "DECISION",
                    "subject_refs": ["beat:B03"],
                    "decision_type": "INFORMATION_ORDER",
                    "chosen_action": "DEFER_RESOLVED_INTERPRETATION",
                    "rationale_summary": "Let the physical visibility constraint appear before its abstract consequence is named.",
                    "evidence_refs": ["evidence:E17"],
                    "alternatives_considered": ["ENCODE_PARADOX_IN_LISTENER_AFTER"],
                    "expected_effect": "Preserve discovery-led information release across B03.",
                    "risks": ["The next beat must carry enough interpretation to avoid ambiguity."],
                    "output_refs": ["output/plan.json"],
                }
            )
            self.assertEqual(event["decision_type"], "INFORMATION_ORDER")
            planner.write_text("output/plan.json", "{}")

    def test_truth_and_audit_have_decision_contracts_but_review_is_not_forced_to_rationalize_prevote(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            review = RoleWorkspaceBroker(run, "review", "R1")
            review.write_text("output/preference.json", "{}")
            review.record_event(
                {
                    "event_id": "R-C01",
                    "event_type": "CHECKPOINT",
                    "subject_refs": ["output/preference.json"],
                    "checkpoint": "FIRST_PASS_VOTE_FROZEN",
                    "status": "FROZEN",
                    "artifact_refs": ["output/preference.json"],
                }
            )
            seal = seal_execution(
                run,
                role="review",
                execution_id="R1",
                required_output_refs=["preference.json"],
                require_decision=False,
            )
            self.assertEqual(seal["decision_count"], 0)


if __name__ == "__main__":
    unittest.main()
