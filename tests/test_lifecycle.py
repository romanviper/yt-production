from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lifecycle import (
    apply_research_submission,
    apply_section_submission,
    prepare_research_rework,
    prepare_section_rework,
    research_rework_blocker,
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


def make_research_fixture(root: Path) -> Path:
    product = root / "products" / "demo"
    write_json(
        product / "product.json",
        {
            "slug": "demo",
            "status": "outline_approved",
            "stages": {
                "direction": "approved",
                "research_plan": "approved",
                "research": "approved",
                "outline": "approved",
                "sections": "in_progress",
                "integration": "not_started",
                "delivery": "not_started",
            },
            "production_cycle": {"id": "C002", "status": "outline_approved"},
        },
    )
    write_json(
        product / "01_research" / "plan.json",
        {
            "status": "approved",
            "workstreams": [{"id": "WS01"}, {"id": "WS02"}],
        },
    )
    for unit in ["WS01", "WS02"]:
        root_ws = product / "01_research" / "workstreams" / unit
        write_json(root_ws / "sources.json", {"status": "complete", "sources": []})
        write_json(root_ws / "claims.json", {"status": "complete", "claims": []})
        write_json(root_ws / "materials.json", {"status": "complete", "materials": []})
        (root_ws / "synthesis.md").write_text("Status: complete\n\n# Synthesis\n", encoding="utf-8")
    (product / "01_research" / "research-synthesis.md").write_text(
        "Status: complete\n\n# Research synthesis\n", encoding="utf-8"
    )
    write_json(product / "01_research" / "story-material-map.json", {"status": "complete"})
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

    def test_stage_level_workstream_rework_invalidates_all_units_and_downstream(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_research_fixture(Path(temp))

            selected = prepare_research_rework(
                product,
                "research_workstream",
                "Rebuild research handoff before a full outline redesign.",
                all_units=True,
            )

            self.assertEqual("WS01", selected)
            state = json.loads((product / "01_research" / "rework-state.json").read_text(encoding="utf-8"))
            product_state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            self.assertEqual(["WS01", "WS02"], state["pending_units"])
            self.assertEqual("in_progress", product_state["stages"]["research"])
            self.assertEqual("changes_requested", product_state["stages"]["outline"])
            self.assertEqual("paused", product_state["stages"]["sections"])
            self.assertIn("WS01", str(research_rework_blocker(product)))
            for unit in ["WS01", "WS02"]:
                sources = json.loads((product / "01_research" / "workstreams" / unit / "sources.json").read_text(encoding="utf-8"))
                claims = json.loads((product / "01_research" / "workstreams" / unit / "claims.json").read_text(encoding="utf-8"))
                self.assertEqual("rework_pending", sources["status"])
                self.assertEqual("rework_pending", claims["status"])
                self.assertIn(
                    "Status: rework_pending",
                    (product / "01_research" / "workstreams" / unit / "synthesis.md").read_text(encoding="utf-8"),
                )
            self.assertIn(
                "Status: rework_pending",
                (product / "01_research" / "research-synthesis.md").read_text(encoding="utf-8"),
            )

    def test_workstream_submissions_drain_rework_queue(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_research_fixture(Path(temp))
            prepare_research_rework(product, "research_workstream", "Rework all workstreams.", all_units=True)

            apply_research_submission(product, "research_workstream", "WS01")
            state = json.loads((product / "01_research" / "rework-state.json").read_text(encoding="utf-8"))
            self.assertEqual(["WS02"], state["pending_units"])
            self.assertEqual(["WS01"], state["completed_units"])

            apply_research_submission(product, "research_workstream", "WS02")
            state = json.loads((product / "01_research" / "rework-state.json").read_text(encoding="utf-8"))
            self.assertEqual([], state["pending_units"])
            self.assertEqual("workstreams_complete", state["status"])
            self.assertIsNone(research_rework_blocker(product))

    def test_research_synthesis_submission_closes_transient_rework_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_research_fixture(Path(temp))
            prepare_research_rework(product, "research_synthesis", "Rebuild material-aware synthesis.")
            self.assertTrue((product / "01_research" / "rework-state.json").is_file())

            apply_research_submission(product, "research_synthesis", None)

            product_state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            self.assertEqual("complete", product_state["stages"]["research"])
            self.assertFalse((product / "01_research" / "rework-state.json").exists())
            self.assertFalse((product / "01_research" / "rework-request.md").exists())

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
