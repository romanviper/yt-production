from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.rework import _resolve_research_unit, rework


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ResearchSemanticReworkTests(unittest.TestCase):
    def make_product(self, root: Path) -> Path:
        product = root / "products" / "demo"
        write_json(
            product / "01_research" / "plan.json",
            {"status": "approved", "workstreams": [{"id": "WS01"}, {"id": "WS02"}]},
        )
        return product

    def test_omitting_unit_means_rework_whole_workstream_layer(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = self.make_product(Path(temp))
            unit, all_workstreams = _resolve_research_unit(product, None)
            self.assertEqual("WS01", unit)
            self.assertTrue(all_workstreams)

    def test_explicit_unit_keeps_rework_local(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = self.make_product(Path(temp))
            unit, all_workstreams = _resolve_research_unit(product, "WS02")
            self.assertEqual("WS02", unit)
            self.assertFalse(all_workstreams)

    def test_rework_routes_first_unit_after_stage_level_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = self.make_product(Path(temp))
            fake_registry = {"research_workstream": {"target_kind": "unit"}}
            fake_work = {"id": "T9999-research-workstream-WS01"}

            with (
                patch("scripts.rework.load_registry", return_value=fake_registry),
                patch("scripts.rework.cancel_active_task", return_value="T9998-draft-section-P01"),
                patch("scripts.rework._ensure_outline_invalidated_for_research"),
                patch("scripts.rework.prepare_research_rework", return_value="WS01") as prepare,
                patch("scripts.rework.create_task", return_value=fake_work) as create,
                patch("scripts.rework._record_rework"),
            ):
                work = rework(
                    product,
                    "research_workstream",
                    section=None,
                    unit=None,
                    request="Rework the whole research workstream layer.",
                )

            self.assertEqual(fake_work, work)
            prepare.assert_called_once_with(
                product.resolve(),
                "research_workstream",
                "Rework the whole research workstream layer.",
                unit="WS01",
                all_units=True,
            )
            create.assert_called_once_with(product.resolve(), "research_workstream", None, "WS01", False, None)


if __name__ == "__main__":
    unittest.main()
