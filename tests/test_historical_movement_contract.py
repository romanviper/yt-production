"""Tests for historical movement outline contract and writer projection."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.context_packet import compile_packet
from scripts.materialize_sections import materialize
from scripts.outline_contract import validate_outline_contract
from test_material_aware_handoff import make_direct_authorship_fixture, write_json


class HistoricalMovementContractTests(unittest.TestCase):
    def test_valid_historical_change_passes_outline_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))

            # Add historical_change and earned_meaning to P01
            p01 = next(sec for sec in outline["sections"] if sec["id"] == "P01")
            p01["historical_change"] = {
                "from": "Kế toán bằng token đất sét rời rạc không thể theo kịp quy mô đô thị hóa",
                "to": "Tập hợp các ký hiệu số và dấu ấn hình thành hệ thống lưu trữ ngoại thân đầu tiên",
            }
            p01["earned_meaning"] = "Chữ viết xuất hiện từ áp lực quản trị vật chất chứ không phải phát minh ngôn ngữ thuần túy"
            write_json(outline_path, outline)

            errors = validate_outline_contract(outline, require_current=True)
            self.assertEqual([], errors)

    def test_malformed_historical_change_fails_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))

            p01 = next(sec for sec in outline["sections"] if sec["id"] == "P01")
            p01["historical_change"] = {"from": "", "to": "some state"}
            write_json(outline_path, outline)

            errors = validate_outline_contract(outline, require_current=True)
            self.assertTrue(any("historical_change must be an object with non-empty 'from' and 'to'" in err for err in errors))

    def test_materialization_and_writer_projection_preserve_historical_movement(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))

            p01 = next(sec for sec in outline["sections"] if sec["id"] == "P01")
            p01["historical_change"] = {
                "from": "Ký ức sinh học đơn lẻ",
                "to": "Trí nhớ ngoại thân ổn định",
            }
            p01["earned_meaning"] = "Dấu vết vật chất định hình trật tự xã hội"
            write_json(outline_path, outline)

            materialize(product)

            sec_path = product / "03_sections" / "P01" / "section.json"
            sec_state = json.loads(sec_path.read_text(encoding="utf-8"))
            self.assertEqual("Ký ức sinh học đơn lẻ", sec_state["historical_change"]["from"])
            self.assertEqual("Trí nhớ ngoại thân ổn định", sec_state["historical_change"]["to"])
            self.assertEqual("Dấu vết vật chất định hình trật tự xã hội", sec_state["earned_meaning"])

            packet, context = compile_packet(
                product,
                "draft_section",
                "T0001-draft-section-P01",
                section="P01",
            )

            # Writer context must include historical_change and earned_meaning
            self.assertIn('"historical_change"', context)
            self.assertIn("Ký ức sinh học đơn lẻ", context)
            self.assertIn("Trí nhớ ngoại thân ổn định", context)
            self.assertIn("Dấu vết vật chất định hình trật tự xã hội", context)

            # Writer context must NOT expose legacy choreography fields or claim lists
            self.assertNotIn('"entry_state"', context)
            self.assertNotIn('"exit_state"', context)
            self.assertNotIn('"story_strategy"', context)
            self.assertNotIn('"story_plan"', context)
            self.assertNotIn("permitted_claims", context)


if __name__ == "__main__":
    unittest.main()
