import json
import os
import tempfile
import unittest
from pathlib import Path

from learning_runtime.artifacts import artifact_identity
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

    def test_review_brief_hides_diagnostic_hypothesis(self):
        review = role_safe_brief(self._brief(), "review")
        plan = role_safe_brief(self._brief(), "plan")
        self.assertNotIn("diagnostic_hypothesis", review)
        self.assertIn("diagnostic_hypothesis", plan)
        self.assertIn("product_standard", review)

    def test_role_can_read_input_and_write_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            broker = RoleWorkspaceBroker(run, "writer", "W1")
            brief = broker.read_text("input/common-brief.json")
            self.assertIn("OWNER_PRODUCT_FIT", brief)
            output = broker.write_text("output/draft.md", "draft")
            self.assertEqual(output.read_text(encoding="utf-8"), "draft")

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

    def test_handoff_copies_exact_hash_to_read_only_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            writer = RoleWorkspaceBroker(run, "writer", "W1")
            source = writer.write_text("output/candidate.md", "candidate text")
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
            self.assertEqual(record["result"], "COPIED_READ_ONLY_HASH_MATCH")
            truth = RoleWorkspaceBroker(run, "truth", "T1")
            with self.assertRaises(WorkspaceError):
                truth.write_text("input/candidate.md", "changed")

    def test_manifest_states_broker_only_limitations(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self._run(tmp)
            manifest = workspace_manifest(run)
            self.assertEqual(manifest["policy"]["host_process_isolation"], "NOT_PROVEN")
            self.assertIn("sole filesystem surface", " ".join(manifest["limitations"]))


if __name__ == "__main__":
    unittest.main()
