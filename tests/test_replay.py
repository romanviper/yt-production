from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.replay import continue_replay, start_replay


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ReplayTests(unittest.TestCase):
    def test_start_replay_routes_only_first_semantic_step(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "products" / "demo"
            product.mkdir(parents=True)
            write_json(product / "02_outline" / "outline.json", {"status": "approved"})

            with patch("scripts.replay.rework", return_value={"id": "T0100-outline-outline"}) as routed:
                state = start_replay(
                    product,
                    start="outline",
                    through="draft_section",
                    section="P01",
                    request="Replay current harness through P01 draft.",
                )

            self.assertEqual(["outline", "design_section", "draft_section"], state["steps"])
            self.assertEqual("outline", state["current_step"])
            self.assertEqual("T0100-outline-outline", state["current_task"])
            routed.assert_called_once()

    def test_start_outline_replay_rejects_unapproved_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "products" / "demo"
            write_json(product / "02_outline" / "outline.json", {"status": "draft"})

            with self.assertRaisesRegex(ValueError, "approved baseline"):
                start_replay(
                    product,
                    start="outline",
                    through="draft_section",
                    section="P01",
                    request="Replay",
                )

    def test_continue_waits_for_human_outline_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "products" / "demo"
            write_json(
                product / "replay-state.json",
                {
                    "schema_version": 1,
                    "id": "RP-1",
                    "status": "active",
                    "request": "Replay",
                    "section": "P01",
                    "steps": ["outline", "design_section", "draft_section"],
                    "current_index": 0,
                    "current_step": "outline",
                    "current_task": "T0100-outline-outline",
                    "history": [],
                },
            )
            write_json(product / "tasks" / "T0100-outline-outline" / "work-order.json", {"state": "ready_for_review"})
            write_json(product / "02_outline" / "outline.json", {"status": "draft"})

            state = continue_replay(product)

            self.assertEqual("outline_approval", state["blocked_on"])
            self.assertEqual("outline", state["current_step"])

    def test_continue_after_outline_approval_materializes_then_routes_design(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "products" / "demo"
            write_json(
                product / "replay-state.json",
                {
                    "schema_version": 1,
                    "id": "RP-1",
                    "status": "active",
                    "request": "Replay",
                    "section": "P01",
                    "steps": ["outline", "design_section", "draft_section"],
                    "current_index": 0,
                    "current_step": "outline",
                    "current_task": "T0100-outline-outline",
                    "history": [],
                },
            )
            write_json(product / "tasks" / "T0100-outline-outline" / "work-order.json", {"state": "ready_for_review"})
            write_json(product / "02_outline" / "outline.json", {"status": "approved"})

            with (
                patch("scripts.replay._archive_if_needed", return_value=[]),
                patch("scripts.replay.materialize", return_value=[]),
                patch("scripts.replay.create_task", return_value={"id": "T0101-design-section-P01"}) as create,
            ):
                state = continue_replay(product)

            self.assertEqual("design_section", state["current_step"])
            self.assertEqual("T0101-design-section-P01", state["current_task"])
            create.assert_called_once_with(product.resolve(), "design_section", "P01", None, False, None)

    def test_continue_after_story_plan_approval_routes_draft_without_state_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "products" / "demo"
            write_json(
                product / "replay-state.json",
                {
                    "schema_version": 1,
                    "id": "RP-1",
                    "status": "active",
                    "request": "Replay",
                    "section": "P01",
                    "steps": ["outline", "design_section", "draft_section"],
                    "current_index": 1,
                    "current_step": "design_section",
                    "current_task": "T0101-design-section-P01",
                    "history": [],
                },
            )
            write_json(product / "tasks" / "T0101-design-section-P01" / "work-order.json", {"state": "ready_for_review"})
            write_json(product / "03_sections" / "P01" / "story-plan.json", {"status": "approved"})
            write_json(product / "03_sections" / "P01" / "section.json", {"status": "ready_for_draft"})

            with patch("scripts.replay.create_task", return_value={"id": "T0102-draft-section-P01"}) as create:
                state = continue_replay(product)

            self.assertEqual("draft_section", state["current_step"])
            self.assertEqual("T0102-draft-section-P01", state["current_task"])
            create.assert_called_once_with(product.resolve(), "draft_section", "P01", None, False, None)


if __name__ == "__main__":
    unittest.main()
