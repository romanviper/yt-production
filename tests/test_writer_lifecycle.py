from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.draft_evidence import DraftEvidenceBroker
from scripts.draft_lifecycle_contract import validate_canonical_draft_lifecycle, validate_evidence_trace
from scripts.materialize_sections import materialize
from scripts.outcome_eval_contract import validate_outcome_review
from scripts.task import create_task, submit_task
from scripts.validate import validate_product
from test_material_aware_handoff import make_direct_authorship_fixture, write_json


class WriterLifecycleRegression(unittest.TestCase):
    def test_canonical_draft_requires_official_task_and_binds_submission_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            root = product / "03_sections" / "P01"
            state_path = root / "section.json"

            # A prose file appearing in the workspace is not canonical by existence alone.
            (root / "draft.md").write_text("# P01\n\nUnrouted draft.\n", encoding="utf-8")
            (root / "handoff.md").write_text("Unrouted handoff.\n", encoding="utf-8")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            lifecycle_errors = validate_canonical_draft_lifecycle(product, "P01", state)
            self.assertTrue(any("missing submitted task provenance" in item for item in lifecycle_errors))
            product_errors = [issue.message for issue in validate_product(product)]
            self.assertTrue(any("missing submitted task provenance" in item for item in product_errors))

            (root / "draft.md").unlink()
            (root / "handoff.md").unlink()

            # The routed task owns the prose paths while writing is in progress.
            work = create_task(product, "draft_section", "P01", None, False)
            task_id = work["id"]
            (root / "draft.md").write_text("# P01\n\nEvidence-safe routed draft.\n", encoding="utf-8")
            (root / "handoff.md").write_text("Mission reached without expanding evidence.\n", encoding="utf-8")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual([], validate_canonical_draft_lifecycle(product, "P01", state))

            task_dir = product / "tasks" / task_id
            (task_dir / "report.md").write_text("Draft completed inside the routed task scope.\n", encoding="utf-8")
            write_json(
                task_dir / "operator-brief.json",
                {
                    "schema_version": 1,
                    "status": "ready_for_review",
                    "headline": "P01 draft is ready for review.",
                    "material_points": ["The draft stayed inside the approved mission and evidence boundary."],
                    "decision": {
                        "required": True,
                        "question": "Review P01 now?",
                        "recommendation": "Review the draft before approval.",
                        "options": [
                            {"label": "Review", "effect": "Inspect the draft and request changes or continue."}
                        ],
                    },
                    "next_step": "",
                },
            )

            # Direct-authorship drafts cannot submit by reading claim prose out of band.
            missing_trace = submit_task(product, task_id)
            self.assertTrue(any("must resolve approved claims" in item for item in missing_trace))

            broker = DraftEvidenceBroker(product, task_id)
            broker.call("scope")
            scope_only = submit_task(product, task_id)
            self.assertTrue(any("must inspect approved claims" in item for item in scope_only))

            broker.call("claims", {"ids": ["CLM-0001"]})
            self.assertEqual([], validate_evidence_trace(product, task_id))
            self.assertEqual([], submit_task(product, task_id))

            submitted = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual("ready_for_review", submitted["status"])
            self.assertEqual(task_id, submitted["prose_provenance"]["task_id"])
            self.assertEqual([], validate_canonical_draft_lifecycle(product, "P01", submitted))

            # Tampering with an audit trace after submission invalidates canonical provenance.
            trace_path = task_dir / "evidence-trace.jsonl"
            records = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
            records[0]["response_sha256"] = "0" * 64
            trace_path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in records) + "\n", encoding="utf-8")
            tampered = validate_canonical_draft_lifecycle(product, "P01", submitted)
            self.assertTrue(any("response hash is invalid" in item for item in tampered))

    def test_canonical_evaluator_requires_mission_answer_and_retellable_progression(self) -> None:
        conclusion_list = (
            "# Outcome Evaluation — P01\n\n"
            "Verdict: pass\n\n"
            "## Outcome judgment\n\n"
            "Every factual conclusion is supported and the section contains the correct claims, but this judgment only checks correctness and lists the conclusions that appeared.\n\n"
            "## Issues\n\n"
            "No factual error is recorded, and no truth-ceiling expansion is visible in the submitted prose.\n\n"
            "## Routing\n\n"
            "Pass to human review because the facts are accurate and all expected conclusions are present.\n"
        )
        errors = validate_outcome_review(conclusion_list, require_mission_outcomes=True)
        self.assertTrue(any("Mission answerability" in item for item in errors))
        self.assertTrue(any("Historical progression" in item for item in errors))

        outcome_review = (
            "# Outcome Evaluation — P01\n\n"
            "Verdict: pass\n\n"
            "## Outcome judgment\n\n"
            "The listener reaches the assigned answer without evidence overreach, and the section preserves continuity with the approved boundary.\n\n"
            "## Mission answerability\n\n"
            "Yes. After hearing the section, the listener can state the answer to the section mission in their own words and distinguish it from adjacent questions.\n\n"
            "## Historical progression\n\n"
            "Yes. The listener can retell the historical path that produced the answer rather than recalling only a list of conclusions.\n\n"
            "## Issues\n\n"
            "No material outcome, continuity or evidence issue remains in this fixture.\n\n"
            "## Routing\n\n"
            "Pass to human review; no prose, architecture or evidence intervention is required.\n"
        )
        self.assertEqual([], validate_outcome_review(outcome_review, require_mission_outcomes=True))


if __name__ == "__main__":
    unittest.main()
