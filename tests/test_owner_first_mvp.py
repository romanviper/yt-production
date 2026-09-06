import json
import tempfile
import unittest
from pathlib import Path

from scripts.learning import (
    LearningError,
    WorkspaceBroker,
    freeze_draft,
    freeze_plan,
    prepare_run,
    record_owner_feedback,
    status,
)


class OwnerFirstMVPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.overlay = self.root / "P01.json"
        self.substrate = self.root / "historical-substrate.json"
        overlay = {
            "section": "P01",
            "historical_territory": "territory",
            "historical_change": {"from": "a", "to": "b"},
            "historical_substrate_ids": ["HS-P01-0001", "HS-P01-0003"],
        }
        substrate = {
            "section": "P01",
            "historical_territory": "territory",
            "historical_change": {"from": "a", "to": "b"},
            "primitives": [{"id": "HS-P01-0001"}, {"id": "HS-P01-0003"}],
            "boundaries": [],
        }
        self.overlay.write_text(json.dumps(overlay), encoding="utf-8")
        self.substrate.write_text(json.dumps(substrate), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _prepare(self, name="run"):
        run = self.root / name
        prepare_run(
            run,
            owner_request="TEST_ONLY: prepare one readable P01 excerpt",
            overlay_path=self.overlay,
            substrate_path=self.substrate,
            test_only=True,
        )
        return run

    def _plan_file(self):
        path = self.root / "plan.json"
        path.write_text(
            json.dumps(
                {
                    "section": "P01",
                    "telling_scope": "Show overlapping clay recording practices without forcing a linear genealogy.",
                    "source_refs": ["overlay:P01", "HS-P01-0001", "HS-P01-0003"],
                    "stop_condition": "Stop after the material constraint becomes legible.",
                }
            ),
            encoding="utf-8",
        )
        return path

    def _freeze_plan(self, run):
        freeze_plan(
            run,
            session_id="plan-001",
            source_file=self._plan_file(),
            declared_reason="Bound the excerpt to approved P01 territory.",
            uncertainty="Exact narrative phrasing remains Writer-owned.",
        )

    def _draft_file(self):
        path = self.root / "draft.md"
        path.write_text("Đây là bản nháp TEST_ONLY để kiểm tra đường bàn giao.\n", encoding="utf-8")
        return path

    def test_m1_status_has_single_waiting_role_and_artifact(self):
        run = self._prepare("m1")
        view = status(run)
        self.assertEqual(view["state"], "AWAITING_PLANNER")
        self.assertEqual(view["waiting_for"], "Planner")
        self.assertTrue(view["artifact_to_open"].endswith("agents/plan/plan-001/input/packet.json"))
        self.assertIn("freeze-plan", view["next_action"])

    def test_m2_tampered_packet_wrong_session_and_overwrite_are_rejected(self):
        run = self._prepare("m2")
        packet = run / "agents/plan/plan-001/input/packet.json"
        packet.chmod(0o666)
        packet.write_text(packet.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaises(LearningError) as ctx:
            freeze_plan(run, session_id="plan-001", source_file=self._plan_file(), declared_reason="x", uncertainty="y")
        self.assertEqual(ctx.exception.code, "FROZEN_ARTIFACT_CHANGED")

        run2 = self._prepare("m2-session")
        with self.assertRaises(LearningError) as ctx:
            freeze_plan(run2, session_id="wrong-session", source_file=self._plan_file(), declared_reason="x", uncertainty="y")
        self.assertEqual(ctx.exception.code, "SESSION_MISMATCH")

        self._freeze_plan(run2)
        with self.assertRaises(LearningError) as ctx:
            freeze_plan(run2, session_id="plan-001", source_file=self._plan_file(), declared_reason="x", uncertainty="y")
        self.assertEqual(ctx.exception.code, "STATE_TRANSITION_DENIED")

    def test_plan_cannot_expand_authority(self):
        run = self._prepare("authority")
        bad = self.root / "bad-plan.json"
        bad.write_text(
            json.dumps(
                {
                    "section": "P01",
                    "telling_scope": "x",
                    "source_refs": ["external:internet"],
                    "stop_condition": "y",
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(LearningError) as ctx:
            freeze_plan(run, session_id="plan-001", source_file=bad, declared_reason="x", uncertainty="y")
        self.assertEqual(ctx.exception.code, "PLAN_AUTHORITY_EXPANSION")

    def test_m3_workspace_broker_blocks_cross_role_and_resolved_symlink_escape(self):
        run = self._prepare("m3")
        broker = WorkspaceBroker(run, "plan", "plan-001")
        self.assertIn("TEST_ONLY", broker.read_text("input/packet.json"))
        with self.assertRaises(LearningError) as ctx:
            broker.read_text("../../writer/writer-001/input/packet.json")
        self.assertEqual(ctx.exception.code, "PATH_ESCAPE_DENIED")
        with self.assertRaises(LearningError) as ctx:
            broker.write_text("input/tamper.json", "x")
        self.assertEqual(ctx.exception.code, "ROLE_PATH_DENIED")

        outside = self.root / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        link = run / "agents/plan/plan-001/scratch/link.txt"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            return
        with self.assertRaises(LearningError) as ctx:
            broker.read_text("scratch/link.txt")
        self.assertEqual(ctx.exception.code, "ROLE_PATH_DENIED")

    def test_m4_test_only_fixture_reaches_owner_reading_copy(self):
        run = self._prepare("m4")
        self._freeze_plan(run)
        self.assertEqual(status(run)["waiting_for"], "Writer")
        freeze_draft(
            run,
            session_id="writer-001",
            source_file=self._draft_file(),
            declared_reason="Realized the frozen Plan only.",
            uncertainty="Literary quality is for Owner judgment.",
        )
        view = status(run)
        self.assertEqual(view["state"], "AWAITING_OWNER_FEEDBACK")
        self.assertEqual(view["waiting_for"], "Owner")
        owner_draft = run / "owner/draft.md"
        writer_draft = run / "agents/writer/writer-001/output/draft.md"
        self.assertEqual(owner_draft.read_bytes(), writer_draft.read_bytes())
        state = json.loads((run / "control/state.json").read_text(encoding="utf-8"))
        self.assertTrue(state["test_only"])

    def test_m5_feedback_stops_without_new_candidate(self):
        run = self._prepare("m5")
        self._freeze_plan(run)
        freeze_draft(run, session_id="writer-001", source_file=self._draft_file(), declared_reason="x", uncertainty="y")
        draft_before = (run / "owner/draft.md").read_bytes()
        record_owner_feedback(run, feedback_text="Tôi muốn đoạn này bớt giống thuyết trình.")
        view = status(run)
        self.assertEqual(view["state"], "OWNER_FEEDBACK_RECORDED")
        self.assertEqual(view["waiting_for"], "Owner")
        feedback = json.loads((run / "control/owner-feedback.json").read_text(encoding="utf-8"))
        self.assertEqual(feedback["verbatim_feedback"], "Tôi muốn đoạn này bớt giống thuyết trình.")
        self.assertEqual(feedback["interpretation"], "NOT_PERFORMED")
        self.assertEqual((run / "owner/draft.md").read_bytes(), draft_before)
        self.assertFalse((run / "agents/writer/writer-002").exists())
        with self.assertRaises(LearningError):
            freeze_draft(run, session_id="writer-001", source_file=self._draft_file(), declared_reason="reroll", uncertainty="none")

    def test_feedback_is_bound_to_unchanged_draft(self):
        run = self._prepare("feedback-hash")
        self._freeze_plan(run)
        freeze_draft(run, session_id="writer-001", source_file=self._draft_file(), declared_reason="x", uncertainty="y")
        draft = run / "owner/draft.md"
        draft.chmod(0o666)
        draft.write_text("tampered", encoding="utf-8")
        with self.assertRaises(LearningError) as ctx:
            record_owner_feedback(run, feedback_text="feedback")
        self.assertEqual(ctx.exception.code, "FROZEN_ARTIFACT_CHANGED")


if __name__ == "__main__":
    unittest.main()
