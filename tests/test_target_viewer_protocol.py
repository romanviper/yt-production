from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROFILE = REPO_ROOT / "system" / "audiences" / "foc-public-v1.md"
RUNTIME_PROFILE = REPO_ROOT / "system" / "audiences" / "longform-history-runtime-v1.md"
PROTOCOL = REPO_ROOT / "system" / "workflows" / "target-viewer-protocol.md"
HARNESS = REPO_ROOT / "system" / "workflows" / "section-production-harness.md"


class TargetViewerProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE_PROFILE.read_text(encoding="utf-8")
        cls.runtime = RUNTIME_PROFILE.read_text(encoding="utf-8")
        cls.protocol = PROTOCOL.read_text(encoding="utf-8")
        cls.harness = HARNESS.read_text(encoding="utf-8")

    def test_runtime_projection_is_anonymous(self) -> None:
        banned_literals = [
            "Fall of Civilizations",
            "vidIQ",
            "UCT6Y5JJPKe_JDMivpKgVXew",
            "d2lJUOv0hLA",
            "1.5 million",
            "219,697,090",
            "40,183,162",
            "Sumerians",
            "Majapahit",
            "Assyrians",
            "competitor",
            "benchmark",
        ]
        for token in banned_literals:
            with self.subTest(token=token):
                self.assertNotIn(token.casefold(), self.runtime.casefold())
        self.assertIsNone(re.search(r"\bFoC\b", self.runtime, flags=re.IGNORECASE))

    def test_named_source_stays_separate_from_runtime_projection(self) -> None:
        for required in [
            "2026-08-25",
            "## Observed",
            "## Inferred",
            "## Unknown",
            "UCT6Y5JJPKe_JDMivpKgVXew",
            "1.5M subscribers",
            "219,697,090",
            "220 relevance-sorted public comment threads",
            "96 recent channel-level public threads",
            "nonrandom, self-selected",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, self.source)
        self.assertIn("must never be passed to a target viewer", self.protocol)
        self.assertIn("longform-history-runtime-v1.md", self.protocol)
        self.assertIn("named audience source profile", self.harness)

    def test_protocol_and_harness_put_cold_read_before_formal_review(self) -> None:
        self.assertIn("fresh fork with no inherited conversation", self.protocol)
        self.assertIn("Give it no filesystem, repository, web, shell", self.protocol)
        self.assertIn("Send exactly one new chunk per turn", self.protocol)
        self.assertIn("## Mode: `route_probe`", self.protocol)
        self.assertIn("## Mode: `draft_cold_read`", self.protocol)
        self.assertIn("does not replace or pre-author the writer's narrative choices", self.protocol)
        writer_index = self.harness.index("Writer receives")
        cold_read_index = self.harness.index("Run a clean `draft_cold_read`")
        formal_review_index = self.harness.index("Route `review_section`")
        self.assertLess(writer_index, cold_read_index)
        self.assertLess(cold_read_index, formal_review_index)
        self.assertIn("continuation is `no` or `uncertain`", self.harness)
        self.assertIn("Do not auto-loop a writer", self.harness)

    def test_runtime_contract_and_writer_authorship_invariant_remain_explicit(self) -> None:
        for required in [
            '"strongest_next_question"',
            '"mental_scene"',
            '"experienced_change"',
            '"focal_orientation"',
            '"narration_mode"',
            '"listening_state"',
            '"retained_image"',
            '"historical_change_retold"',
            '"first_lecture_break_chunk"',
            '"spoken_naturalness"',
            '"curiosity_chain"',
            "no score alone determines the verdict",
            "not from a fixed numeric threshold",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, self.runtime)
        self.assertIn(
            "The broker never asks for, records or validates a creative route.",
            self.harness,
        )
        self.assertIn("tell a compelling historical story that earns continued voluntary attention", self.harness)
        self.assertIn("discover the mission's meaning through what unfolds", self.harness)
        self.assertIn("keep proposed visual grammar outside the Writer packet", self.harness)
        self.assertIn("Only observation and desired outcome enter a normal Writer packet", self.harness)
        self.assertIn("owner_locked_for_single_task", self.harness)


if __name__ == "__main__":
    unittest.main()
