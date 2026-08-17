from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.new_product import DEFAULT_TEMPLATE_ROOT, create_product
from scripts.task import create_task, set_task_state, submit_task
from scripts.validate import validate_product


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_direction_approved_product(root: Path) -> Path:
    product = create_product(root / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
    state_path = product / "product.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["stages"]["direction"] = "approved"
    write_json(state_path, state)
    return product


class TaskEnforcementTests(unittest.TestCase):
    def test_invalid_packet_cannot_be_activated(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direction_approved_product(Path(temp))
            work = create_task(product, "research_plan", None, None, False)
            packet_path = product / work["packet_manifest"]
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            packet["compiler"] = "connector/manual-equivalent"
            write_json(packet_path, packet)

            errors = set_task_state(product, work["id"], "in_progress")

            self.assertTrue(any("packet.compiler" in item for item in errors))
            persisted = json.loads((product / "tasks" / work["id"] / "work-order.json").read_text(encoding="utf-8"))
            self.assertEqual("ready", persisted["state"])

    def test_submitted_packet_remains_validated_after_active_pointer_moves(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direction_approved_product(Path(temp))
            work = create_task(product, "research_plan", None, None, False)
            task_root = product / "tasks" / work["id"]

            persisted = json.loads((task_root / "work-order.json").read_text(encoding="utf-8"))
            persisted["state"] = "ready_for_review"
            write_json(task_root / "work-order.json", persisted)
            packet = json.loads((task_root / "packet.json").read_text(encoding="utf-8"))
            packet["compiler"] = "connector/manual-equivalent"
            write_json(task_root / "packet.json", packet)
            (product / "tasks" / "ACTIVE.json").unlink()

            issues = validate_product(product)

            self.assertTrue(any("packet.compiler" in issue.message for issue in issues))

    def test_replaced_task_cannot_be_submitted_after_active_pointer_moves(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direction_approved_product(Path(temp))
            first = create_task(product, "research_plan", None, None, False)
            create_task(product, "research_plan", None, None, True)

            errors = submit_task(product, first["id"])

            self.assertTrue(any("not the active task" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
