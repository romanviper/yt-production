from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.context_packet import compile_packet
from scripts.materialize_sections import materialize
from test_material_aware_handoff import make_direct_authorship_fixture


class WriterBaselineTests(unittest.TestCase):
    def test_clean_direct_authorship_packet_contains_only_mission_boundary_and_continuity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))

            # These files may remain useful elsewhere, but canonical draft_section must not ingest them.
            (product / "02_outline" / "story-bible.md").write_text(
                "FULL_STORY_BIBLE_SENTINEL\n",
                encoding="utf-8",
            )
            (product / "02_outline" / "voice-profile.md").write_text(
                "CREATIVE_HEURISTIC_SENTINEL causality over chronology concrete focus\n",
                encoding="utf-8",
            )

            materialize(product)
            root = product / "03_sections" / "P01"
            (root / "story-plan.json").write_text(
                json.dumps({"legacy": "LEGACY_STORY_PLAN_SENTINEL"}) + "\n",
                encoding="utf-8",
            )
            (root / "draft.md").write_text("OLD_DRAFT_SENTINEL\n", encoding="utf-8")
            (root / "handoff.md").write_text("OLD_HANDOFF_SENTINEL\n", encoding="utf-8")
            (root / "benchmark-example.md").write_text(
                "BENCHMARK_IMITATION_SENTINEL Fall of Civilizations\n",
                encoding="utf-8",
            )

            packet, context = compile_packet(
                product,
                "draft_section",
                "T9997-draft-section-P01",
                section="P01",
            )

            self.assertEqual(
                [
                    "system/core/creative-boundaries.md",
                    "system/operations/draft-section.md",
                ],
                packet["instruction_files"],
            )
            self.assertEqual(
                [
                    "03_sections/P01/section.json",
                    "03_sections/P01/narration-pack.json",
                    "03_sections/P01/continuity-in.md",
                ],
                [item["path"] for item in packet["inputs"]],
            )
            self.assertIn("evidence_access", packet)

            # Mission and truth boundary remain visible.
            self.assertIn("Change listener state from 0 to 1 without prescribing how.", context)
            self.assertIn("CLM-0001", context)

            # Creative guidance/evaluator/legacy artifacts and old prose do not enter model context.
            excluded = [
                "FULL_STORY_BIBLE_SENTINEL",
                "CREATIVE_HEURISTIC_SENTINEL",
                "LEGACY_STORY_PLAN_SENTINEL",
                "OLD_DRAFT_SENTINEL",
                "OLD_HANDOFF_SENTINEL",
                "BENCHMARK_IMITATION_SENTINEL",
                "system/standards/channel-constitution.md",
                "system/standards/outcome-evaluation.md",
                "02_outline/voice-profile.md",
                "02_outline/story-bible.md",
                "03_sections/P01/brief.md",
                "material-ledger.json",
                "story-material-map.json",
                "claim-ledger.json",
                "source-index.json",
                "02_outline/outline.json",
                "crafted narration intended to be spoken aloud",
                "recount-before-interpret",
                "delayed explanation",
                "scale shift",
            ]
            for value in excluded:
                self.assertNotIn(value, context)


if __name__ == "__main__":
    unittest.main()
