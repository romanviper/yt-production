import json
import os
import tempfile
import unittest
from pathlib import Path

from learning_runtime.artifacts import artifact_identity
from learning_runtime.telemetry import TelemetryError, seal_execution, verify_execution_seal
from learning_runtime.workspace import (
    RoleWorkspaceBroker,
    WorkspaceError,
    create_workspace_run,
    handoff_copy,
    role_safe_brief,
    workspace_manifest,
)

ROOT = Path(__file__).resolve().parents[1]


class WorkspaceTests(unittest.TestCase):
    def _brief(self):
        return json.loads((ROOT / "learning_runtime/briefs/p01-rootcause-01.json").read_text(encoding="utf-8"))

    def _run(self, tmp: str):
        return create_workspace_run(
            Path(tmp),
            "RUN-001",
            {"plan": "P1", "writer": "W1", "truth": "T1", "review": "R1", "audit": "A1"},
            self._brief(),
        )

    def _record_writer_decision(self, writer: RoleWorkspaceBroker, output_ref: str = "output/candidate.md", event_id: str = "W-D01"):
        return writer.record_event(
            {
                "event_id": event_id,
                "event_type": "DECISION",
                "subject_refs": ["plan:B03"],
                "decision_type": "REALIZATION_STRATEGY",
                "chosen_action": "SHOW_CONDITION_BEFORE_INTERPRETATION",
                "rationale_summary": "Keep the prose on the material condition before stating the broader meaning.",
                "evidence_refs": ["input/common-brief.json"],
                "alternatives_considered": ["STATE_PARADOX_EXPLICITLY"],
                "expected_effect": "Delay resolved interpretation until the physical constraint is legible.",
                "risks": ["The unit may feel under-explained if the next beat does not carry the interpretation."],
                "output_refs": [output_ref],
            }
        )

    def test_review_brief_hides_diagnostic_hypothesis(self):
        review = role_safe_brief(self._brief(), "review")
        plan = role_safe_brief(self._brief(), "plan")
        self.assertNotIn("diagnostic_hypothesis", review)
        self.assertIn("diagnostic_hypothesis", plan)
        self.assertIn("product_standard", review)
        self.assertIn("process_telemetry_contract", review)
        self.assertIn("before the first final output write", plan["process_telemetry_contract"]["temporal_rule"])

    def test_role_can_read_input_and_write_output_after_bound_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            broker = RoleWorkspaceBroker(run, "writer", "W1")
            brief = broker.read_text("input/common-brief.json")
            self.assertIn("OWNER_PRODUCT_FIT", brief)
            self._record_writer_decision(broker, "output/draft.md")
            output = broker.write_text("output/draft.md", "draft")
            self.assertEqual(output.read_text(encoding="utf-8"), "draft")

    def test_writer_final_output_requires_prior_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            with self.assertRaises(WorkspaceError) as ctx:
                writer.write_text("output/candidate.md", "candidate")
            self.assertEqual(ctx.exception.code, "DECISION_REQUIRED_BEFORE_FINAL_OUTPUT")
            self.assertFalse((run / "agents/writer/W1/output/candidate.md").exists())

    def test_final_output_is_write_once_before_seal_and_scratch_remains_iterable(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            self._record_writer_decision(writer)
            writer.write_text("scratch/draft.md", "draft 1")
            writer.write_text("scratch/draft.md", "draft 2")
            self.assertEqual(writer.read_text("scratch/draft.md"), "draft 2")
            writer.write_text("output/candidate.md", "candidate v1")
            with self.assertRaises(WorkspaceError) as ctx:
                writer.write_text("output/candidate.md", "candidate v2")
            self.assertEqual(ctx.exception.code, "OUTPUT_OVERWRITE_DENIED_USE_SCRATCH")
            self.assertEqual(writer.read_text("output/candidate.md"), "candidate v1")

    def test_writer_cannot_read_review_workspace_or_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            broker = RoleWorkspaceBroker(run, "writer", "W1")
            for path in ("../../review/R1/input/common-brief.json", "../../../control/role-policy.json"):
                with self.assertRaises(WorkspaceError):
                    broker.read_text(path)
            events = (run / "control/access-events.jsonl").read_text(encoding="utf-8")
            self.assertIn("DENIED", events)

    def test_writer_cannot_modify_input_and_hash_stays_same(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            input_path = run / "agents/writer/W1/input/common-brief.json"
            before = artifact_identity(input_path)["raw_sha256"]
            broker = RoleWorkspaceBroker(run, "writer", "W1")
            with self.assertRaises(WorkspaceError):
                broker.write_text("input/common-brief.json", "tamper")
            after = artifact_identity(input_path)["raw_sha256"]
            self.assertEqual(before, after)

    def test_reviewer_cannot_read_plan_via_absolute_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            plan_path = run / "agents/plan/P1/input/common-brief.json"
            broker = RoleWorkspaceBroker(run, "review", "R1")
            with self.assertRaises(WorkspaceError):
                broker.read_text(str(plan_path.resolve()))

    def test_symlink_escape_is_denied_when_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            link = run / "agents/writer/W1/scratch/review-link"
            target = run / "agents/review/R1/input"
            try:
                os.symlink(target, link, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation unavailable")
            broker = RoleWorkspaceBroker(run, "writer", "W1")
            with self.assertRaises(WorkspaceError):
                broker.read_text("scratch/review-link/common-brief.json")

    def test_handoff_requires_sealed_source_and_exact_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            self._record_writer_decision(writer)
            source = writer.write_text("output/candidate.md", "candidate text")
            with self.assertRaises(TelemetryError) as ctx:
                handoff_copy(
                    run,
                    source_role="writer",
                    source_execution="W1",
                    source_rel="candidate.md",
                    dest_role="truth",
                    dest_execution="T1",
                    dest_name="candidate.md",
                )
            self.assertEqual(ctx.exception.code, "EXECUTION_NOT_SEALED")

            seal_execution(run, role="writer", execution_id="W1", required_output_refs=["candidate.md"])
            self.assertEqual(verify_execution_seal(run, role="writer", execution_id="W1")["status"], "VALID")
            record = handoff_copy(
                run,
                source_role="writer",
                source_execution="W1",
                source_rel="candidate.md",
                dest_role="truth",
                dest_execution="T1",
                dest_name="candidate.md",
            )
            destination = run / "agents/truth/T1/input/candidate.md"
            self.assertEqual(artifact_identity(source)["raw_sha256"], artifact_identity(destination)["raw_sha256"])
            self.assertEqual(record["result"], "COPIED_FROM_SEALED_EXECUTION_READ_ONLY_HASH_MATCH")
            truth = RoleWorkspaceBroker(run, "truth", "T1")
            with self.assertRaises(WorkspaceError):
                truth.write_text("input/candidate.md", "changed")

    def test_writer_cannot_write_after_execution_seal(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            self._record_writer_decision(writer)
            writer.write_text("output/candidate.md", "candidate text")
            seal_execution(run, role="writer", execution_id="W1", required_output_refs=["candidate.md"])
            with self.assertRaises(WorkspaceError) as ctx:
                writer.write_text("scratch/retroactive.md", "retroactive rewrite")
            self.assertEqual(ctx.exception.code, "EXECUTION_SEALED")
            with self.assertRaises(WorkspaceError) as telemetry_ctx:
                writer.record_event(
                    {
                        "event_id": "W-R02",
                        "event_type": "RISK",
                        "subject_refs": ["candidate.md"],
                        "risk": "post-hoc rationalization",
                        "mitigation_or_acceptance": "should be impossible after seal",
                        "evidence_refs": [],
                    }
                )
            self.assertEqual(telemetry_ctx.exception.code, "EXECUTION_SEALED")

    def test_manifest_states_temporal_gate_limitations_and_seals(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            manifest = workspace_manifest(run)
            self.assertEqual(manifest["policy"]["host_process_isolation"], "NOT_PROVEN")
            limitations = " ".join(manifest["limitations"])
            self.assertIn("sole filesystem surface", limitations)
            self.assertIn("decision-before-final-output", limitations)
            self.assertEqual(manifest["execution_seal_count"], 0)
            self.assertEqual(manifest["policy"]["telemetry_version"], "PHASE3-DECISION-TELEMETRY-1")
            self.assertTrue(manifest["policy"]["roles"]["writer"]["decision_before_final_output"])
            self.assertTrue(manifest["policy"]["roles"]["writer"]["final_output_write_once"])


if __name__ == "__main__":
    unittest.main()
