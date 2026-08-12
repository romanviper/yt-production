from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.assemble import assemble_product, check_freshness
from scripts.impact import calculate_impact
from scripts.new_product import DEFAULT_TEMPLATE_ROOT, create_product
from scripts.validate import validate_product


REPO_ROOT = Path(__file__).resolve().parents[1]


class ProductToolingTests(unittest.TestCase):
    def test_pilot_validates(self) -> None:
        issues = validate_product(REPO_ROOT / "products" / "sumer-writing")
        errors = [issue for issue in issues if issue.level == "ERROR"]
        self.assertEqual([], errors, "\n".join(str(issue) for issue in errors))

    def test_new_product_renders_template(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "products"
            product = create_product(root, "demo-history", "Demo History", DEFAULT_TEMPLATE_ROOT)
            data = json.loads((product / "product.json").read_text(encoding="utf-8"))
            self.assertEqual("demo-history", data["slug"])
            self.assertEqual("Demo History", data["working_title"])
            self.assertTrue((product / "03_outline" / "chapters" / "CH01-opening.md").is_file())

    def test_assembly_tracks_staleness(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "products" / "demo"
            chapter_dir = product / "04_script" / "chapters"
            outline_dir = product / "03_outline"
            chapter_dir.mkdir(parents=True)
            outline_dir.mkdir(parents=True)
            (product / "product.json").write_text(
                json.dumps(
                    {
                        "slug": "demo",
                        "working_title": "Demo",
                        "target": {"narration_wpm": 140},
                    }
                ),
                encoding="utf-8",
            )
            (outline_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "chapters": [
                            {
                                "id": "CH01",
                                "title": "Opening",
                                "status": "approved",
                                "draft": "04_script/chapters/CH01-opening.md",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            draft = chapter_dir / "CH01-opening.md"
            draft.write_text("Một chapter đã được duyệt.", encoding="utf-8")
            result = assemble_product(product)
            self.assertEqual(1, len(result["manifest"]["chapters"]))
            self.assertEqual([], check_freshness(product))
            draft.write_text("Chapter đã thay đổi sau lần lắp ráp.", encoding="utf-8")
            self.assertTrue(check_freshness(product))

    def test_claim_impact_is_transitive(self) -> None:
        result = calculate_impact(
            REPO_ROOT / "products" / "sumer-writing",
            claim_id="CLM-0003",
            chapter_id=None,
        )
        self.assertIn("CH05", result["direct_chapters"])
        self.assertIn("CH07", result["direct_chapters"])
        self.assertIn("CH10", result["affected_chapters"])


if __name__ == "__main__":
    unittest.main()

