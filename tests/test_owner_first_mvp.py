import json
import tempfile
import unittest
from pathlib import Path

from scripts.learning import (
    LearningError,
    WorkspaceBroker,
    budget_summary,
    freeze_draft,
    freeze_plan,
    prepare_run,
    propose_budget,
    record_budget_decision,
    record_cost_item,
    record_owner_feedback,
    record_wait_interval,
    record_writer_failure,
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

    def _prepare(self, name="run", approve=True, allocations=None):
        run = self.root / name
        prepare_run(
            run,
            owner_request="TEST_ONLY: prepare one readable P01 excerpt",
            overlay_path=self.overlay,
            substrate_path=self.substrate,
            test_only=True,
            code_ref="test-commit",
        )
        if approve:
            alloc = allocations or {"sol_repo": 30, "writer_gemini": 30, "writer_sol": 30}
            propose_budget(
                run,
                budget_id=f"B-{name}",
                initial_cap_seconds=sum(alloc.values()),
                allocations=alloc,
                scope="P01 two-writer TEST_ONLY round",
                code_ref="test-commit",
            )
            record_budget_decision(
                run,
                request_id=f"B-{name}:initial",
                decision="APPROVED",
                owner_text="Owner approves this TEST_ONLY time budget.",
                source_ref="chat:test",
            )
        return run

    def _plan_file(self):
        path = self.root / "plan.json"
        path.write_text(
            json.dumps({
                "section": "P01",
                "telling_scope": "Show overlapping clay recording practices without forcing a linear genealogy.",
                "source_refs": ["overlay:P01", "HS-P01-0001", "HS-P01-0003"],
                "stop_condition": "Stop after the material constraint becomes legible.",
            }),
            encoding="utf-8",
        )
        return path

    def _freeze_plan(self, run, start="2026-09-06T10:00:00+00:00", end="2026-09-06T10:00:10+00:00"):
        return freeze_plan(
            run,
            session_id="sol-repo-001",
            source_file=self._plan_file(),
            declared_reason="Bound the excerpt to approved P01 territory.",
            uncertainty="Exact narrative phrasing remains Writer-owned.",
            start_utc=start,
            end_utc=end,
            timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW",
        )

    def _draft_file(self, name="draft.md", text=None):
        path = self.root / name
        path.write_text(text or f"Đây là bản nháp TEST_ONLY {name} để kiểm tra đường bàn giao.\n", encoding="utf-8")
        return path

    def _freeze_writer(self, run, actor, start, end, name=None):
        if actor == "writer_gemini":
            session = "writer-gemini-001"
            model = "Gemini 3.8 Flash"
            name = name or "gemini.md"
        else:
            session = "writer-sol-001"
            model = "GPT-5.6 Sol"
            name = name or "sol.md"
        return freeze_draft(
            run,
            session_id=session,
            source_file=self._draft_file(name),
            declared_reason="Realized the same frozen Plan only.",
            uncertainty="Literary quality is for Owner judgment.",
            actual_model=model,
            actual_config="test-config",
            start_utc=start,
            end_utc=end,
            timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW",
        )

    def test_m1_status_has_single_waiting_role_and_artifact(self):
        run = self._prepare("m1", approve=False)
        view = status(run)
        self.assertEqual(view["state"], "AWAITING_OWNER_BUDGET_APPROVAL")
        self.assertEqual(view["waiting_for"], "Owner")
        parts = Path(view["artifact_to_open"]).parts
        self.assertEqual(parts[-5:], ("agents", "sol_repo", "sol-repo-001", "input", "brief.json"))
        self.assertIn("budget", view["next_action"].lower())

    def test_m2_tampered_packet_wrong_session_and_overwrite_are_rejected(self):
        run = self._prepare("m2")
        brief = run / "agents/sol_repo/sol-repo-001/input/brief.json"
        brief.chmod(0o666)
        brief.write_text(brief.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaises(LearningError) as ctx:
            self._freeze_plan(run)
        self.assertEqual(ctx.exception.code, "FROZEN_ARTIFACT_CHANGED")

        run2 = self._prepare("m2-session")
        with self.assertRaises(LearningError) as ctx:
            freeze_plan(run2, session_id="wrong-session", source_file=self._plan_file(), declared_reason="x", uncertainty="y")
        self.assertEqual(ctx.exception.code, "SESSION_MISMATCH")
        self._freeze_plan(run2)
        with self.assertRaises(LearningError) as ctx:
            self._freeze_plan(run2)
        self.assertEqual(ctx.exception.code, "STATE_TRANSITION_DENIED")

    def test_plan_cannot_expand_authority(self):
        run = self._prepare("authority")
        bad = self.root / "bad-plan.json"
        bad.write_text(json.dumps({"section": "P01", "telling_scope": "x", "source_refs": ["external:internet"], "stop_condition": "y"}), encoding="utf-8")
        with self.assertRaises(LearningError) as ctx:
            freeze_plan(
                run,
                session_id="sol-repo-001",
                source_file=bad,
                declared_reason="x",
                uncertainty="y",
                start_utc="2026-09-06T10:00:00+00:00",
                end_utc="2026-09-06T10:00:01+00:00",
                timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW",
            )
        self.assertEqual(ctx.exception.code, "PLAN_AUTHORITY_EXPANSION")

    def test_m3_workspace_broker_blocks_cross_role_and_resolved_symlink_escape(self):
        run = self._prepare("m3", approve=False)
        broker = WorkspaceBroker(run, "sol_repo", "sol-repo-001")
        self.assertIn("TEST_ONLY", broker.read_text("input/brief.json"))
        with self.assertRaises(LearningError) as ctx:
            broker.read_text("../../writer_sol/writer-sol-001/input/packet.json")
        self.assertEqual(ctx.exception.code, "PATH_ESCAPE_DENIED")
        with self.assertRaises(LearningError) as ctx:
            broker.write_text("input/tamper.json", "x")
        self.assertEqual(ctx.exception.code, "ROLE_PATH_DENIED")
        outside = self.root / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        link = run / "agents/sol_repo/sol-repo-001/scratch/link.txt"
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
        self._freeze_writer(run, "writer_gemini", "2026-09-06T10:01:00+00:00", "2026-09-06T10:01:05+00:00")
        self._freeze_writer(run, "writer_sol", "2026-09-06T10:01:00+00:00", "2026-09-06T10:01:06+00:00")
        view = status(run)
        self.assertEqual(view["state"], "AWAITING_OWNER_FEEDBACK")
        self.assertEqual(view["waiting_for"], "Owner")
        self.assertEqual((run / "owner/sample-A.md").read_bytes(), (run / "agents/writer_gemini/writer-gemini-001/output/draft.md").read_bytes())
        self.assertEqual((run / "owner/sample-B.md").read_bytes(), (run / "agents/writer_sol/writer-sol-001/output/draft.md").read_bytes())

    def test_m5_feedback_stops_without_new_candidate(self):
        run = self._prepare("m5")
        self._freeze_plan(run)
        self._freeze_writer(run, "writer_gemini", "2026-09-06T10:01:00+00:00", "2026-09-06T10:01:05+00:00")
        self._freeze_writer(run, "writer_sol", "2026-09-06T10:01:06+00:00", "2026-09-06T10:01:11+00:00")
        a_before = (run / "owner/sample-A.md").read_bytes()
        b_before = (run / "owner/sample-B.md").read_bytes()
        record_owner_feedback(run, feedback_text="Mẫu A tự nhiên hơn.", selection="A", primary_writer="writer_gemini")
        view = status(run)
        self.assertEqual(view["state"], "OWNER_FEEDBACK_RECORDED")
        feedback = json.loads((run / "control/owner-feedback.json").read_text(encoding="utf-8"))
        self.assertEqual(feedback["verbatim_feedback"], "Mẫu A tự nhiên hơn.")
        self.assertEqual(feedback["selection"], "A")
        self.assertEqual(feedback["primary_writer_decision"], "writer_gemini")
        self.assertEqual(feedback["model_generalization"], "NOT_PERFORMED")
        self.assertEqual((run / "owner/sample-A.md").read_bytes(), a_before)
        self.assertEqual((run / "owner/sample-B.md").read_bytes(), b_before)
        with self.assertRaises(LearningError):
            self._freeze_writer(run, "writer_gemini", "2026-09-06T10:02:00+00:00", "2026-09-06T10:02:05+00:00", "reroll.md")

    def test_feedback_is_bound_to_unchanged_draft(self):
        run = self._prepare("feedback-hash")
        self._freeze_plan(run)
        self._freeze_writer(run, "writer_gemini", "2026-09-06T10:01:00+00:00", "2026-09-06T10:01:05+00:00")
        self._freeze_writer(run, "writer_sol", "2026-09-06T10:01:06+00:00", "2026-09-06T10:01:11+00:00")
        draft = run / "owner/sample-A.md"
        draft.chmod(0o666)
        draft.write_text("tampered", encoding="utf-8")
        with self.assertRaises(LearningError) as ctx:
            record_owner_feedback(run, feedback_text="feedback")
        self.assertEqual(ctx.exception.code, "FROZEN_ARTIFACT_CHANGED")

    # RC1-RC6: exactly six amendment acceptance tests.
    def test_rc1_one_sol_plan_two_isolated_writers_same_common_hash(self):
        run = self._prepare("rc1")
        self._freeze_plan(run)
        state = json.loads((run / "control/state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["sessions"]["sol_repo"], "sol-repo-001")
        self.assertEqual(set(state["sessions"]), {"sol_repo", "writer_gemini", "writer_sol"})
        a = json.loads((run / "agents/writer_gemini/writer-gemini-001/input/packet.json").read_text(encoding="utf-8"))
        b = json.loads((run / "agents/writer_sol/writer-sol-001/input/packet.json").read_text(encoding="utf-8"))
        self.assertEqual(a["common_content_sha256"], b["common_content_sha256"])
        self.assertEqual(a["common"], b["common"])
        self.assertNotEqual(a["session_id"], b["session_id"])
        self.assertNotEqual(a["requested_model"], b["requested_model"])
        self.assertFalse((run / "agents/plan").exists())
        self.assertFalse((run / "agents/review").exists())

    def test_rc2_both_arrival_orders_failure_and_owner_selection_binding(self):
        for suffix, order in (("gs", ["writer_gemini", "writer_sol"]), ("sg", ["writer_sol", "writer_gemini"])):
            run = self._prepare(f"rc2-{suffix}")
            self._freeze_plan(run)
            for i, actor in enumerate(order):
                self._freeze_writer(run, actor, f"2026-09-06T10:01:0{i}+00:00", f"2026-09-06T10:01:0{i+1}+00:00", f"{suffix}-{actor}.md")
            self.assertEqual(status(run)["state"], "AWAITING_OWNER_FEEDBACK")
            record_owner_feedback(run, feedback_text="chọn theo owner", selection="B")
            feedback = json.loads((run / "control/owner-feedback.json").read_text(encoding="utf-8"))
            self.assertEqual(feedback["samples"]["A"]["sha256"], json.loads((run / "control/state.json").read_text(encoding="utf-8"))["draft_sha256"]["writer_gemini"])
            self.assertIsNone(feedback["primary_writer_decision"])

        run = self._prepare("rc2-fail")
        self._freeze_plan(run)
        self._freeze_writer(run, "writer_gemini", "2026-09-06T10:01:00+00:00", "2026-09-06T10:01:01+00:00")
        record_writer_failure(
            run,
            session_id="writer-sol-001",
            status="TIMEOUT",
            reason="host timeout",
            start_utc="2026-09-06T10:01:02+00:00",
            end_utc="2026-09-06T10:01:03+00:00",
            timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW",
        )
        self.assertNotEqual(status(run)["state"], "AWAITING_OWNER_FEEDBACK")
        self.assertFalse((run / "owner/sample-B.md").exists())

    def test_rc3_time_accounting_parallel_sequential_wait_retry_and_unknown(self):
        parallel = self._prepare("rc3-par", allocations={"sol_repo": 30, "writer_gemini": 200, "writer_sol": 200})
        self._freeze_plan(parallel, "2026-09-06T10:00:00+00:00", "2026-09-06T10:00:10+00:00")
        self._freeze_writer(parallel, "writer_gemini", "2026-09-06T10:01:00+00:00", "2026-09-06T10:03:00+00:00")
        self._freeze_writer(parallel, "writer_sol", "2026-09-06T10:01:00+00:00", "2026-09-06T10:03:00+00:00")
        record_wait_interval(
            parallel,
            actor="owner_wait",
            session_id="owner",
            task="owner_reading",
            attempt=0,
            start_utc="2026-09-06T10:03:00+00:00",
            end_utc="2026-09-06T10:13:00+00:00",
            timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW",
            status="COMPLETED",
            reason="Owner reading",
        )
        timing = budget_summary(parallel)["timing"]
        self.assertEqual(timing["total_work_seconds"], 250.0)
        self.assertEqual(timing["writer_pair_elapsed_seconds"], 120.0)
        self.assertEqual(timing["waiting_seconds"], 600.0)

        seq = self._prepare("rc3-seq")
        self._freeze_plan(seq)
        record_writer_failure(seq, session_id="writer-gemini-001", status="FAILED", reason="transport", start_utc="2026-09-06T10:01:00+00:00", end_utc="2026-09-06T10:01:02+00:00", timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW")
        self._freeze_writer(seq, "writer_gemini", "2026-09-06T10:01:03+00:00", "2026-09-06T10:01:05+00:00", "retry.md")
        self._freeze_writer(seq, "writer_sol", "2026-09-06T10:01:06+00:00", "2026-09-06T10:01:08+00:00")
        self.assertEqual(budget_summary(seq)["timing"]["total_work_seconds"], 16.0)

        unknown = self._prepare("rc3-unknown")
        freeze_plan(unknown, session_id="sol-repo-001", source_file=self._plan_file(), declared_reason="x", uncertainty="y")
        summary = budget_summary(unknown)
        self.assertEqual(summary["timing"]["unknown_work_intervals"], 1)
        self.assertIsNone(summary["total_remaining_seconds"])
        self.assertEqual(status(unknown)["state"], "AWAITING_OWNER_BUDGET_APPROVAL")

    def test_rc4_budget_required_overrun_blocks_and_preserves_pending_output(self):
        no_budget = self._prepare("rc4-none", approve=False)
        with self.assertRaises(LearningError) as ctx:
            freeze_plan(no_budget, session_id="sol-repo-001", source_file=self._plan_file(), declared_reason="x", uncertainty="y")
        self.assertEqual(ctx.exception.code, "STATE_TRANSITION_DENIED")

        run = self._prepare("rc4-over", allocations={"sol_repo": 20, "writer_gemini": 2, "writer_sol": 20})
        self._freeze_plan(run)
        freeze_draft(
            run,
            session_id="writer-gemini-001",
            source_file=self._draft_file("late.md"),
            declared_reason="one attempt",
            uncertainty="none",
            actual_model="Gemini 3.8 Flash",
            start_utc="2026-09-06T10:01:00+00:00",
            end_utc="2026-09-06T10:01:05+00:00",
            timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW",
        )
        view = status(run)
        self.assertEqual(view["state"], "AWAITING_OWNER_BUDGET_APPROVAL")
        self.assertTrue((run / "agents/writer_gemini/writer-gemini-001/output/draft.md").is_file())
        self.assertFalse((run / "owner/sample-A.md").exists())
        self.assertGreater(view["budget"]["actors"]["writer_gemini"]["overrun_seconds"], 0)
        self.assertTrue(view["budget"]["pending_extension_requests"])

    def test_rc5_extension_approval_exact_scope_no_reset_or_extra_attempt(self):
        run = self._prepare("rc5", allocations={"sol_repo": 20, "writer_gemini": 2, "writer_sol": 20})
        self._freeze_plan(run)
        freeze_draft(
            run,
            session_id="writer-gemini-001",
            source_file=self._draft_file("rc5-late.md"),
            declared_reason="one attempt",
            uncertainty="none",
            actual_model="Gemini 3.8 Flash",
            start_utc="2026-09-06T10:01:00+00:00",
            end_utc="2026-09-06T10:01:05+00:00",
            timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW",
        )
        request = budget_summary(run)["pending_extension_requests"][0]
        with self.assertRaises(LearningError) as ctx:
            record_budget_decision(run, request_id="wrong", decision="APPROVED", owner_text="yes", source_ref="chat", actor="writer_gemini", scope="write_draft", approved_seconds=3)
        self.assertEqual(ctx.exception.code, "EXTENSION_REQUEST_NOT_FOUND")
        with self.assertRaises(LearningError) as ctx:
            record_budget_decision(run, request_id=request["request_id"], decision="APPROVED", owner_text="yes", source_ref="chat", actor="writer_sol", scope="write_draft", approved_seconds=3)
        self.assertEqual(ctx.exception.code, "EXTENSION_APPROVAL_SCOPE_MISMATCH")
        record_budget_decision(run, request_id=request["request_id"], decision="APPROVED", owner_text="Owner approves exactly 3 seconds for Gemini overrun.", source_ref="chat:owner", actor="writer_gemini", scope="write_draft", approved_seconds=3)
        summary = budget_summary(run)
        self.assertEqual(summary["actors"]["writer_gemini"]["used_seconds"], 5.0)
        self.assertEqual(summary["actors"]["writer_gemini"]["extension_approved_seconds"], 3.0)
        self.assertTrue((run / "owner/sample-A.md").is_file())
        with self.assertRaises(LearningError):
            freeze_draft(run, session_id="writer-gemini-001", source_file=self._draft_file("second-attempt.md"), declared_reason="reroll", uncertainty="none", actual_model="Gemini 3.8 Flash", start_utc="2026-09-06T10:02:00+00:00", end_utc="2026-09-06T10:02:01+00:00", timestamp_source="OPERATOR_OBSERVED_SESSION_WINDOW")

    def test_rc6_cost_report_separates_estimate_observed_repair_round_and_paths(self):
        run = self._prepare("rc6")
        record_cost_item(run, work_item_id="ARCH-1", phase="ESTIMATE", kind="ARCHITECTURE_REPAIR", actor="sol_repo", task="fix path handling", code_scope="tests/test_owner_first_mvp.py", estimate_seconds=60, expected_runtime_impact="none expected", confidence="medium")
        record_cost_item(run, work_item_id="ARCH-1", phase="OBSERVED", kind="ARCHITECTURE_REPAIR", actor="sol_repo", task="fix path handling", code_scope="tests/test_owner_first_mvp.py", observed_seconds=45, commit_ref="abc123", evidence="CI Windows path test")
        record_cost_item(run, work_item_id="ROUND-1", phase="ESTIMATE", kind="ROUND_EXECUTION", actor="writer_sol", task="write draft", code_scope="P01", estimate_seconds=120, expected_runtime_impact="one writer invocation", confidence="low")
        view = status(run)
        kinds = {(x["work_item_id"], x["phase"], x["kind"]) for x in view["cost_items"]}
        self.assertIn(("ARCH-1", "ESTIMATE", "ARCHITECTURE_REPAIR"), kinds)
        self.assertIn(("ARCH-1", "OBSERVED", "ARCHITECTURE_REPAIR"), kinds)
        self.assertIn(("ROUND-1", "ESTIMATE", "ROUND_EXECUTION"), kinds)
        self.assertTrue(all("actor_task" in row for row in view["budget_table"]))
        parts = Path(view["artifact_to_open"]).parts
        self.assertNotIn("\\", parts[-1])


if __name__ == "__main__":
    unittest.main()
