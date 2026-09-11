import json
import tempfile
import unittest
from pathlib import Path

from scripts import learning
from scripts.export_writer_assignment import export_assignment


class DynamicOwnerFirstTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.overlay = self.root / "P01.json"
        self.substrate = self.root / "historical-substrate.json"
        self.overlay.write_text(json.dumps({
            "section": "P01",
            "historical_territory": "territory",
            "historical_change": {"from": "a", "to": "b"},
            "historical_substrate_ids": ["HS-P01-0001"],
        }), encoding="utf-8")
        self.substrate.write_text(json.dumps({
            "section": "P01",
            "historical_territory": "territory",
            "historical_change": {"from": "a", "to": "b"},
            "primitives": [{"id": "HS-P01-0001"}],
            "boundaries": [],
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def prepare(self, name="run"):
        run = self.root / name
        learning.prepare_run(run, owner_request="TEST_ONLY P01", overlay_path=self.overlay,
                             substrate_path=self.substrate, test_only=True, code_ref="test")
        learning.propose_budget(run, budget_id=f"B-{name}", sol_seconds=1200,
                                scope="Sol repo only", code_ref="test")
        learning.record_budget_decision(run, request_id=f"B-{name}:initial",
                                        decision="APPROVED", owner_text="Owner approves 20 min Sol repo.",
                                        source_ref="chat:test")
        plan = self.root / f"{name}-plan.json"
        plan.write_text(json.dumps({
            "section": "P01", "telling_scope": "show material constraint",
            "source_refs": ["overlay:P01", "HS-P01-0001"],
            "stop_condition": "stop once legible",
        }), encoding="utf-8")
        learning.freeze_plan(run, session_id="sol-repo-001", source_file=plan,
                             declared_reason="bounded", uncertainty="wording open",
                             duration_seconds=30, timestamp_source="TEST")
        return run

    def submission(self, run, sid, model, *, binding="PREBOUND", duration=99999):
        draft = self.root / f"{sid}.md"
        draft.write_text(f"TEST_ONLY draft from {model}\n", encoding="utf-8")
        state = learning._load_state(run)
        if binding == "PREBOUND":
            assignment_sha = state["writer_assignment_sha256"]
            inputs = [{"ref": "control/writer-assignment.json", "sha256": assignment_sha}]
        else:
            assignment_sha = None
            inputs = [
                {"ref": "owner-instruction:test", "sha256": "owner-directive-sha256"},
                {"ref": "products/test/P01-overlay.json", "sha256": "overlay-sha256"},
                {"ref": "products/test/P01-historical-substrate.json", "sha256": "substrate-sha256"},
            ]
        report = {
            "schema_version": learning.WRITER_REPORT_SCHEMA,
            "submission_id": sid,
            "provider": "test",
            "actual_model": model,
            "actual_config": None,
            "provider_session_id": f"host-{sid}",
            "assignment_binding": binding,
            "assignment_sha256": assignment_sha,
            "inputs_used": inputs,
            "attempt": 1,
            "status": "COMPLETED",
            "timing": {"source": "WRITER_SELF_REPORTED_DURATION", "duration_seconds": duration},
            "draft_sha256": learning.sha256_file(draft),
            "issues_encountered": [],
            "uncertainty": "owner judges",
        }
        rp = self.root / f"{sid}.json"
        rp.write_text(json.dumps(report), encoding="utf-8")
        return learning.accept_writer_submission(run, report_file=rp, draft_file=draft)

    def test_sol_repo_only_is_budgeted(self):
        run = self.prepare("budget")
        summary = learning.budget_summary(run)
        self.assertEqual(summary["writer_budget_policy"], "NOT_APPLICABLE")
        self.assertEqual(set(summary) >= {"sol_repo", "writer_budget_policy"}, True)
        with self.assertRaises(learning.LearningError) as ctx:
            learning.request_budget_extension(run, actor="writer_gpt6", requested_seconds=10,
                                              scope="write", reason="x", evidence="x")
        self.assertEqual(ctx.exception.code, "WRITER_BUDGET_NOT_APPLICABLE")

    def test_dynamic_models_need_no_registration(self):
        run = self.prepare("dynamic")
        self.submission(run, "gemini-001", "Gemini 3.8 Flash")
        self.submission(run, "gpt6-001", "GPT-6")
        self.submission(run, "claude-001", "Claude X")
        view = learning.status(run)
        self.assertEqual([x["submission_id"] for x in view["submissions"]],
                         ["gemini-001", "gpt6-001", "claude-001"])

    def test_writer_duration_does_not_block_or_request_extension(self):
        run = self.prepare("timing")
        state = self.submission(run, "slow-writer", "GPT-6", duration=100000)
        self.assertEqual(state["state"], "AWAITING_WRITER_SUBMISSIONS")
        self.assertEqual(learning.status(run)["budget"]["pending_extension_requests"], [])

    def test_prebound_and_owner_directed_not_prebound_are_distinguished(self):
        run = self.prepare("binding")
        self.submission(run, "pre", "GPT-6", binding="PREBOUND")
        self.submission(run, "owner-direct", "GPT-5.6 Sol", binding="NOT_PREBOUND")
        rows = {x["submission_id"]: x for x in learning.status(run)["submissions"]}
        self.assertTrue(rows["pre"]["controlled_comparison_eligible"])
        self.assertFalse(rows["owner-direct"]["controlled_comparison_eligible"])
        self.assertIsNone(rows["owner-direct"]["assignment_sha256"])
        report = json.loads((run / rows["owner-direct"]["report_ref"]).read_text(encoding="utf-8"))
        self.assertEqual(report["assignment_binding"], "NOT_PREBOUND")
        self.assertIsNone(report["assignment_sha256"])
        self.assertNotIn("control/writer-assignment.json", {x["ref"] for x in report["inputs_used"]})

    def test_wrong_prebound_hash_is_rejected(self):
        run = self.prepare("hash")
        draft = self.root / "x.md"
        draft.write_text("x", encoding="utf-8")
        report = {
            "schema_version": learning.WRITER_REPORT_SCHEMA,
            "submission_id": "x",
            "actual_model": "GPT-6",
            "assignment_binding": "PREBOUND",
            "assignment_sha256": "wrong",
            "inputs_used": [{"ref": "x", "sha256": "y"}],
            "attempt": 1,
            "status": "COMPLETED",
            "timing": {"source": "UNKNOWN", "duration_seconds": None},
            "draft_sha256": learning.sha256_file(draft),
        }
        rp = self.root / "x.json"
        rp.write_text(json.dumps(report), encoding="utf-8")
        with self.assertRaises(learning.LearningError) as ctx:
            learning.accept_writer_submission(run, report_file=rp, draft_file=draft)
        self.assertEqual(ctx.exception.code, "ASSIGNMENT_HASH_MISMATCH")

    def test_submission_id_is_write_once_no_reroll(self):
        run = self.prepare("write-once")
        self.submission(run, "gpt6", "GPT-6")
        with self.assertRaises(learning.LearningError) as ctx:
            self.submission(run, "gpt6", "GPT-6")
        self.assertEqual(ctx.exception.code, "SUBMISSION_ALREADY_EXISTS")

    def test_close_pool_then_feedback_and_stop(self):
        run = self.prepare("owner")
        self.submission(run, "gpt6", "GPT-6")
        self.submission(run, "gemini", "Gemini")
        learning.close_submissions(run)
        self.assertEqual(learning.status(run)["state"], "AWAITING_OWNER_FEEDBACK")
        learning.record_owner_feedback(run, feedback_text="GPT-6 better", selection="gpt6", primary_writer="gpt6")
        view = learning.status(run)
        self.assertEqual(view["state"], "OWNER_FEEDBACK_RECORDED")
        with self.assertRaises(learning.LearningError):
            self.submission(run, "late", "Sol")

    def test_export_is_generic_not_actor_specific(self):
        run = self.prepare("export")
        out = self.root / "bundle"
        manifest = export_assignment(run, out)
        self.assertFalse(manifest["writer_registration_required"])
        self.assertEqual(manifest["writer_time_budget"], "NOT_APPLICABLE")
        self.assertTrue((out / "assignment.json").is_file())
        self.assertTrue((out / "execution-report-template.json").is_file())


if __name__ == "__main__":
    unittest.main()
