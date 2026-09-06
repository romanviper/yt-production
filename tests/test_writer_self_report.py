import json
import tempfile
import unittest
from pathlib import Path

from scripts import learning
from scripts.writer_submission import (
    REPORT_SCHEMA,
    accept_writer_submission,
    prepare_report_contracts,
)


class WriterSelfReportTests(unittest.TestCase):
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

    def _run(self, name="run", gemini_seconds=600, sol_seconds=600):
        run = self.root / name
        learning.prepare_run(
            run,
            owner_request="TEST_ONLY: produce two Writer samples",
            overlay_path=self.overlay,
            substrate_path=self.substrate,
            test_only=True,
            code_ref="test-self-report",
        )
        learning.propose_budget(
            run,
            budget_id=f"B-{name}",
            initial_cap_seconds=1200 + gemini_seconds + sol_seconds,
            allocations={"sol_repo": 1200, "writer_gemini": gemini_seconds, "writer_sol": sol_seconds},
            scope="TEST_ONLY writer self-report",
            code_ref="test-self-report",
        )
        learning.record_budget_decision(
            run,
            request_id=f"B-{name}:initial",
            decision="APPROVED",
            owner_text="Owner approves TEST_ONLY budget.",
            source_ref="chat:test",
        )
        plan = self.root / f"{name}-plan.json"
        plan.write_text(json.dumps({
            "section": "P01",
            "telling_scope": "Show the material constraint.",
            "source_refs": ["overlay:P01", "HS-P01-0001"],
            "stop_condition": "Stop after the constraint is legible.",
        }), encoding="utf-8")
        learning.freeze_plan(
            run,
            session_id="sol-repo-001",
            source_file=plan,
            declared_reason="TEST_ONLY plan",
            uncertainty="Writer wording remains open.",
            duration_seconds=10,
            timestamp_source="TEST_CONTROLLER_DURATION",
        )
        prepare_report_contracts(run)
        return run

    def _submission(self, run, actor="writer_gemini", duration=20, extension=None, forbidden=False):
        packet_path, _, _ = learning._writer_paths(run, actor)
        packet = learning.read_json(packet_path)
        draft = self.root / f"{run.name}-{actor}.md"
        draft.write_text(f"Bản nháp TEST_ONLY từ {actor}.\n", encoding="utf-8")
        report = {
            "schema_version": REPORT_SCHEMA,
            "actor": actor,
            "session_id": learning.WRITERS[actor]["session_id"],
            "provider_session_id": f"host-{actor}-001",
            "packet_sha256": learning.sha256_file(packet_path),
            "common_content_sha256": packet["common_content_sha256"],
            "actual_model": learning.WRITERS[actor]["requested_model"],
            "actual_config": "test-config",
            "attempt": 1,
            "status": "COMPLETED",
            "work_summary": "Produced one draft from the frozen packet.",
            "issues_encountered": [],
            "uncertainty": "Owner judges literary quality.",
            "timing": {
                "timestamp_source": "WRITER_SELF_REPORTED_DURATION",
                "start_utc": None,
                "end_utc": None,
                "duration_seconds": duration,
            },
            "draft_sha256": learning.sha256_file(draft),
            "budget_extension": extension,
        }
        if forbidden:
            report["private_reasoning"] = "must never be accepted"
        report_path = self.root / f"{run.name}-{actor}-execution-report.json"
        report_path.write_text(json.dumps(report), encoding="utf-8")
        return draft, report_path

    def test_writer_contracts_bind_same_packet_content_and_budget(self):
        run = self._run("contract")
        for actor in learning.WRITERS:
            contract = learning.read_json(run / "agents" / actor / learning.WRITERS[actor]["session_id"] / "input" / "self-report-contract.json")
            packet_path, _, _ = learning._writer_paths(run, actor)
            self.assertEqual(contract["packet_sha256"], learning.sha256_file(packet_path))
            self.assertEqual(contract["common_content_sha256"], learning.read_json(packet_path)["common_content_sha256"])
            self.assertIn("execution-report.json", contract["required_outputs"][1])
            self.assertGreater(contract["approved_budget_seconds"], 0)

    def test_completed_writer_metadata_and_timing_come_from_writer_report(self):
        run = self._run("complete")
        draft, report = self._submission(run, duration=25)
        state = accept_writer_submission(run, report_file=report, draft_file=draft)
        self.assertEqual(state["writer_status"]["writer_gemini"], "ACCEPTED")
        identity = state["writer_identity"]["writer_gemini"]
        self.assertEqual(identity["actual_model"], "Gemini 3.8 Flash")
        self.assertEqual(identity["actual_config"], "test-config")
        self.assertIn("self_report_sha256", identity)
        intervals = learning.read_jsonl(run / "control/work-intervals.jsonl")
        writer_interval = [x for x in intervals if x["actor"] == "writer_gemini"][-1]
        self.assertEqual(writer_interval["duration_seconds"], 25.0)
        self.assertEqual(writer_interval["timestamp_source"], "WRITER_SELF_REPORTED_DURATION")

    def test_overrun_requires_writer_reason_and_owner_extension_request(self):
        run = self._run("overrun", gemini_seconds=10)
        draft, report = self._submission(run, duration=15, extension=None)
        with self.assertRaises(learning.LearningError) as ctx:
            accept_writer_submission(run, report_file=report, draft_file=draft)
        self.assertEqual(ctx.exception.code, "WRITER_OVERRUN_EXPLANATION_REQUIRED")

        extension = {
            "requested_seconds": 8,
            "reason": "Host response exceeded the approved Writer window while completing the single draft.",
            "remaining_work_if_approved": "Cover the observed overrun and allow repo acceptance of the already-produced draft only.",
        }
        draft, report = self._submission(run, duration=15, extension=extension)
        state = accept_writer_submission(run, report_file=report, draft_file=draft)
        self.assertEqual(state["state"], "AWAITING_OWNER_BUDGET_APPROVAL")
        pending = learning.budget_summary(run)["pending_extension_requests"]
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["actor"], "writer_gemini")
        self.assertEqual(pending[0]["requested_seconds"], 8.0)
        self.assertIn("Host response exceeded", pending[0]["reason"])
        self.assertFalse((run / "owner/sample-A.md").exists())

    def test_private_reasoning_fields_are_rejected(self):
        run = self._run("reasoning")
        draft, report = self._submission(run, duration=5, forbidden=True)
        with self.assertRaises(learning.LearningError) as ctx:
            accept_writer_submission(run, report_file=report, draft_file=draft)
        self.assertEqual(ctx.exception.code, "PRIVATE_REASONING_FIELD_FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
