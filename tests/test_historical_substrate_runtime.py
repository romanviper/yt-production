from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.common import REPO_ROOT, read_json, write_json
from scripts.context_packet import compile_packet
from scripts.historical_substrate_contract import (
    validate_historical_substrate,
    validate_section_binding,
)
from scripts.materialize_sections import materialize
from scripts.section_overlay_contract import resolve_section_spec
from scripts.substrate_preflight import verify_canonical_section_state
from scripts.validate import validate_product


class HistoricalSubstrateRuntimeIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.product = Path(self.temp.name) / "sumer-writing"
        source = REPO_ROOT / "products" / "sumer-writing"
        required = [
            "product.json",
            "00_brief/product-brief.md",
            "00_brief/benchmark.md",
            "01_research/plan.json",
            "01_research/source-index.json",
            "01_research/claim-ledger.json",
            "01_research/historical-substrate.json",
            "02_outline/outline.json",
            "02_outline/story-bible.md",
            "02_outline/voice-profile.md",
            "02_outline/section-overlays/P01.json",
        ]
        for relative in required:
            src = source / relative
            dst = self.product / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

        product = read_json(self.product / "product.json")
        product["status"] = "outline_approved"
        product.setdefault("stages", {})["sections"] = "not_started"
        product.setdefault("production_cycle", {})["status"] = "outline_approved"
        write_json(self.product / "product.json", product)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _materialize_p01(self) -> None:
        materialize(self.product, section="P01")

    def test_section_migration_materializes_only_declared_section(self) -> None:
        paths = materialize(self.product, section="P01")
        self.assertTrue((self.product / "03_sections/P01/historical-substrate.json").is_file())
        self.assertTrue(any(path.name == "section.json" for path in paths))
        self.assertEqual(verify_canonical_section_state(self.product, "P01"), [])
        with self.assertRaisesRegex(ValueError, "explicit Historical Substrate adoption"):
            materialize(self.product, section="P02")
        with self.assertRaisesRegex(ValueError, "product-complete"):
            materialize(self.product)

    def test_whole_outline_task_requires_product_complete_substrate(self) -> None:
        product = read_json(self.product / "product.json")
        product.setdefault("production_cycle", {})["historical_substrate_contract_version"] = 1
        write_json(self.product / "product.json", product)
        with self.assertRaisesRegex(ValueError, "product-complete"):
            compile_packet(self.product, "outline", "T9000-outline")

    def test_writer_packet_uses_world_substrate_and_secondary_evidence_only(self) -> None:
        self._materialize_p01()
        packet, text = compile_packet(
            self.product,
            "draft_section",
            "T9001-draft-section-P01",
            section="P01",
        )
        self.assertIn("# BEGIN INPUT: 03_sections/P01/historical-substrate.json", text)
        self.assertIn("Evidence access is secondary verification only", text)
        self.assertNotIn("discover story material as well as verify facts", text)
        self.assertEqual(
            packet["historical_substrate"]["section_projection_path"],
            "03_sections/P01/historical-substrate.json",
        )
        projection = read_json(self.product / "03_sections/P01/historical-substrate.json")
        self.assertIn("world", projection["primitives"][0])
        self.assertNotIn("statement", projection["primitives"][0])

    def test_reviewer_packet_contains_same_historical_substrate(self) -> None:
        self._materialize_p01()
        root = self.product / "03_sections/P01"
        state = read_json(root / "section.json")
        state["status"] = "ready_for_review"
        write_json(root / "section.json", state)
        (root / "draft.md").write_text("Draft fixture.\n", encoding="utf-8")
        (root / "handoff.md").write_text("Handoff fixture.\n", encoding="utf-8")
        _packet, text = compile_packet(
            self.product,
            "review_section",
            "T9002-review-section-P01",
            section="P01",
        )
        self.assertIn("# BEGIN INPUT: 03_sections/P01/historical-substrate.json", text)

    def test_stale_section_projection_blocks_task_and_validator_sees_it(self) -> None:
        self._materialize_p01()
        path = self.product / "03_sections/P01/historical-substrate.json"
        value = read_json(path)
        value["primitives"][0]["world"]["operation"] += " edited"
        write_json(path, value)
        with self.assertRaisesRegex(ValueError, "stale or edited"):
            compile_packet(
                self.product,
                "draft_section",
                "T9003-draft-section-P01",
                section="P01",
            )
        issues = validate_product(self.product)
        self.assertTrue(any("stale or edited" in issue.message for issue in issues))

    def test_evidence_state_change_and_narrative_authority_are_rejected(self) -> None:
        substrate = read_json(self.product / "01_research/historical-substrate.json")
        claims = read_json(self.product / "01_research/claim-ledger.json")
        sources = read_json(self.product / "01_research/source-index.json")
        mutated = json.loads(json.dumps(substrate))
        mutated["records"][0]["hook"] = "open here"
        errors = validate_historical_substrate(mutated, claims, sources)
        self.assertTrue(any("narrative-authority fields" in error for error in errors))

        resolved, _authority = resolve_section_spec(self.product, "P01")
        resolved["historical_change"] = {
            "from": "Evidence shows one class of object.",
            "to": "The corpus shows another class of object.",
        }
        errors = validate_section_binding(resolved, substrate)
        self.assertTrue(any("evidence-state" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
