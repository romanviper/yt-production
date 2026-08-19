from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.context_packet import compile_packet
from scripts.materialize_sections import materialize
from scripts.story_plan_contract import verify_narration_pack


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PRODUCT = REPO_ROOT / "products" / "sumer-writing"


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class MaterialAwareHandoffRegression(unittest.TestCase):
    def _copy_c003_as_approved_fixture(self, root: Path) -> Path:
        product = root / "products" / "sumer-writing"
        shutil.copytree(SOURCE_PRODUCT, product)

        # Regression must not alter the real product or inherit C002 section artifacts.
        section_root = product / "03_sections"
        if section_root.exists():
            shutil.rmtree(section_root)
        section_root.mkdir(parents=True)

        outline_path = product / "02_outline" / "outline.json"
        outline = json.loads(outline_path.read_text(encoding="utf-8"))
        self.assertEqual("C003", outline["cycle_id"])
        self.assertEqual(1, outline["script_architecture"]["story_material_contract_version"])
        outline["status"] = "approved"
        write_json(outline_path, outline)
        return product

    def test_c003_p01_materializes_directly_to_draft_packet(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = self._copy_c003_as_approved_fixture(Path(temp))
            materialize(product)

            root = product / "03_sections" / "P01"
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            material_pack = json.loads((root / "material-pack.json").read_text(encoding="utf-8"))
            narration_pack = json.loads((root / "narration-pack.json").read_text(encoding="utf-8"))

            self.assertEqual("C003", state["cycle_id"])
            self.assertEqual("ready_for_draft", state["status"])
            self.assertEqual(["MAT-0004", "MAT-0001"], state["material_ids"])
            self.assertFalse((root / "story-plan.json").exists())

            self.assertEqual(["MAT-0004", "MAT-0001"], material_pack["material_ids"])
            chogha = next(item for item in material_pack["materials"] if item["id"] == "MAT-0001")
            sequence = " ".join(chogha["recountable"]["sequence"])
            self.assertIn("clay envelope contains accounting tokens", sequence)
            self.assertIn("five numeral signs directly on a clay surface", sequence)

            self.assertEqual(3, narration_pack["schema_version"])
            self.assertEqual("C003", narration_pack["cycle_id"])
            self.assertEqual([], verify_narration_pack(product, "P01"))

            packet, context = compile_packet(product, "draft_section", "T9999-draft-section-P01", section="P01")
            input_paths = [item["path"] for item in packet["inputs"]]
            self.assertIn("03_sections/P01/material-pack.json", input_paths)
            self.assertIn("03_sections/P01/narration-pack.json", input_paths)
            self.assertNotIn("03_sections/P01/story-plan.json", input_paths)
            self.assertIn("clay envelope contains accounting tokens", context)
            self.assertIn("five numeral signs directly on a clay surface", context)

    def test_cycle_mismatch_blocks_material_aware_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = self._copy_c003_as_approved_fixture(Path(temp))
            materialize(product)
            state_path = product / "03_sections" / "P01" / "section.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["cycle_id"] = "C002"
            write_json(state_path, state)

            errors = verify_narration_pack(product, "P01")
            self.assertTrue(any("does not match outline cycle" in item for item in errors))
            with self.assertRaisesRegex(ValueError, "Narration pack is not ready"):
                compile_packet(product, "draft_section", "T9998-draft-section-P01", section="P01")


if __name__ == "__main__":
    unittest.main()
