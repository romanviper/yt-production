from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lifecycle import (
    apply_section_submission,
    prepare_section_rework,
    section_operation_state_error,
    task_transition_errors,
)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_section_fixture(root: Path) -> Path:
    product = root / "products" / "demo"
    write_json(
        product / "product.json",
        {
            "slug": "demo",
            "stages": {"sections": "approved", "integration": "approved", "delivery": "approved"},
        },
    )
    write_json(product / "02_outline" / "outline.json", {"status": "approved"})
    write_json(
        product / "03_sections" / "P01" / "section.json",
        {
            "id": "P01",
            "status": "approved",
            "human_approved": True,
            "approved_by": "user",
            "approved_at": "2026-08-17T00:00:00+00:00",
            "approval_basis": "review",
        },
    )
    write_json(
        product / "03_sections" / "P01" / "story-plan.json",
        {
            "status": "approved",
            "approved_by": "user",
            "approved_at": "2026-08-17T00:00:00+00:00",
        },
    )
    return product


class LifecycleTests(unittest.TestCase):
    def test_section_operation_entry_states_have_one_canonical_mapping(self) -> None:
        self.assertIsNone(section_operation_state_error("draft_section", "ready_for_draft", "P01"))
        error = section_operation_state_error("draft_section", "approved", "P01")
        self.assertIn("ready_for_draft", str(error))
        self.assertIsNone(section_operation_state_error("outline", "anything", None))

    def test_terminal_task_is_not_reopened_by_low_level_state_mutation(self) -> None:
        errors = task_transition_errors("cancelled", "in_progress")
        self.assertTrue(any("fresh task" in item or "semantic rework" in item for item in errors))

    def test_design_rework_reopens_approved_section_without_review_state_ceremony(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_section_fixture(Path(temp))

            prepare_section_rework(product, "design_section", "P01", "Redesign this section from the approved evidence.")

            state = json.loads((product / "03_sections" / "P01" / "section.json").read_text(encoding="utf-8"))
            plan = json.loads((product / "03_sections" / "P01" / "story-plan.json").read_text(encoding="utf-8"))
            product_state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            self.assertEqual("story_plan_changes_requested", state["status"])
            self.assertFalse(state["human_approved"])
            self.assertNotIn("approved_by", state)
            self.assertEqual("draft", plan["status"])
            self.assertEqual("in_progress", product_state["stages"]["sections"])
            self.assertEqual("not_started", product_state["stages"]["integration"])
            request = (product / "03_sections" / "P01" / "story-plan-change-request.md").read_text(encoding="utf-8")
            self.assertIn("Redesign this section", request)

    def test_draft_rework_preserves_approved_plan_and_uses_one_shot_human_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_section_fixture(Path(temp))
            root = product / "03_sections" / "P01"

            with patch("scripts.lifecycle.verify_narration_pack", return_value=[]):
                prepare_section_rework(product, "draft_section", "P01", "Rewrite from the same approved story plan.")

            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            plan = json.loads((root / "story-plan.json").read_text(encoding="utf-8"))
            self.assertEqual("ready_for_draft", state["status"])
            self.assertEqual("approved", plan["status"])
            request_path = root / "draft-rework-request.md"
            self.assertTrue(request_path.is_file())
            self.assertIn("Rewrite from the same approved story plan", request_path.read_text(encoding="utf-8"))

            apply_section_submission(product, "draft_section", "P01")
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertEqual("ready_for_review", state["status"])
            self.assertFalse(request_path.exists())


if __name__ == "__main__":
    unittest.main()
