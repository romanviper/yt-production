from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.common import sha256
from scripts.context_packet import compile_packet
from scripts.materialize_sections import materialize
from test_material_aware_handoff import SOURCE_PRODUCT, make_direct_authorship_fixture, write_json


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
            input_paths = [item["path"] for item in packet["inputs"]]
            self.assertEqual(
                [
                    "03_sections/P01/section.json",
                    "03_sections/P01/narration-pack.json",
                    "03_sections/P01/continuity-in.md",
                ],
                input_paths[:3],
            )
            self.assertTrue(set(input_paths[3:]).issubset({"03_sections/P01/draft-rework-request.md"}))
            self.assertIn("evidence_access", packet)
            self.assertEqual(["resolve_claims"], packet["evidence_access"]["required_before_submit"])
            self.assertIn("answer the section mission in their own words", context)
            self.assertIn("retell the historical path", context)

            # The writer sees a plain mission projection plus control states, not upstream architecture prose.
            self.assertIn('"mission"', context)
            self.assertIn('"entry_state"', context)
            self.assertIn('"exit_state"', context)
            self.assertNotIn('"narrative_job"', context)
            self.assertNotIn('"macro_movements"', context)

            # Truth ceiling is visible as IDs; claim/source prose stays behind bounded retrieval.
            self.assertIn("CLM-0001", context)
            for value in [
                "permitted_claims",
                "qualifications",
                "source_refs",
                "writer_contract",
                "counterevidence",
                "narrative_implication",
                "Approved fact for P01.",
                "Primary Source One",
            ]:
                self.assertNotIn(value, context)

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
                "system/standards/section-quality-gate.md",
                "supported_human_work_orientation",
                "production-gate:start",
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

    def test_review_gets_hash_bound_current_next_projection_and_bounded_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))
            outline["projection_forbidden_sentinel"] = "FULL_OUTLINE_REVIEW_SENTINEL"
            write_json(outline_path, outline)

            root = product / "03_sections" / "P01"
            section_path = root / "section.json"
            section_state = json.loads(section_path.read_text(encoding="utf-8"))
            section_state["outline_sha256"] = sha256(outline_path)
            section_state["status"] = "ready_for_review"
            write_json(section_path, section_state)

            evidence_path = root / "evidence-pack.json"
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            evidence["outline_sha256"] = sha256(outline_path)
            write_json(evidence_path, evidence)
            narration_path = root / "narration-pack.json"
            narration = json.loads(narration_path.read_text(encoding="utf-8"))
            narration["outline_sha256"] = sha256(outline_path)
            narration["evidence_pack_sha256"] = sha256(evidence_path)
            write_json(narration_path, narration)
            (root / "draft.md").write_text("# P01\n\nA supported historical progression for review.\n", encoding="utf-8")

            packet, context = compile_packet(
                product,
                "review_section",
                "T9999-review-section-P01",
                section="P01",
            )

            self.assertIn("system/standards/section-quality-gate.md", packet["instruction_files"])
            self.assertEqual(2, packet["review_contract_version"])
            self.assertIn("evidence_access", packet)
            self.assertEqual(["resolve_claims"], packet["evidence_access"]["required_before_submit"])
            self.assertIn('"projection_kind": "review_current_next_boundary"', context)
            self.assertIn(f'"outline_sha256": "{sha256(outline_path)}"', context)
            self.assertIn('"id": "P01"', context)
            ordered = sorted(outline["sections"], key=lambda item: item["order"])
            current_index = next(index for index, item in enumerate(ordered) if item["id"] == "P01")
            if current_index + 1 < len(ordered):
                self.assertIn(f'"id": "{ordered[current_index + 1]["id"]}"', context)
            else:
                self.assertIn('"next": null', context)
            self.assertNotIn("FULL_OUTLINE_REVIEW_SENTINEL", context)
            outline_record = next(item for item in packet["inputs"] if item["path"] == "02_outline/outline.json")
            self.assertEqual(sha256(outline_path), outline_record["sha256"])

    def test_current_sumer_c003_p01_smoke_compiles_to_minimal_writer_packet(self) -> None:
        """Use current Sumer artifacts while refreshing only stale derived hashes in a temporary copy."""

        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "sumer-writing"
            shutil.copytree(SOURCE_PRODUCT, product)

            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))
            self.assertEqual("C003", outline["cycle_id"])
            self.assertEqual(1, outline["script_architecture"]["writer_authorship_contract_version"])
            p01 = next(item for item in outline["sections"] if item["id"] == "P01")

            root = product / "03_sections" / "P01"
            section_path = root / "section.json"
            section_state = json.loads(section_path.read_text(encoding="utf-8"))
            section_state["cycle_id"] = outline["cycle_id"]
            section_state["outline_sha256"] = sha256(outline_path)
            section_state["status"] = "ready_for_draft"
            write_json(section_path, section_state)

            evidence_path = root / "evidence-pack.json"
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            evidence_claim_ids = [item["id"] for item in evidence.get("claims", [])]
            self.assertEqual(p01["claim_ids"], evidence_claim_ids)
            evidence["cycle_id"] = outline["cycle_id"]
            evidence["outline_sha256"] = sha256(outline_path)
            write_json(evidence_path, evidence)

            narration_path = root / "narration-pack.json"
            narration = json.loads(narration_path.read_text(encoding="utf-8"))
            narration["cycle_id"] = outline["cycle_id"]
            narration["outline_sha256"] = sha256(outline_path)
            narration["brief_sha256"] = sha256(root / "brief.md")
            narration["evidence_pack_sha256"] = sha256(evidence_path)
            write_json(narration_path, narration)

            packet, context = compile_packet(
                product,
                "draft_section",
                "T9998-draft-section-P01",
                section="P01",
            )

            self.assertEqual(
                [
                    "system/core/creative-boundaries.md",
                    "system/operations/draft-section.md",
                ],
                packet["instruction_files"],
            )
            input_paths = [item["path"] for item in packet["inputs"]]
            self.assertEqual(
                [
                    "03_sections/P01/section.json",
                    "03_sections/P01/narration-pack.json",
                    "03_sections/P01/continuity-in.md",
                ],
                input_paths[:3],
            )
            self.assertTrue(set(input_paths[3:]).issubset({"03_sections/P01/draft-rework-request.md"}))
            self.assertIn("evidence_access", packet)
            self.assertIn('"mission"', context)
            self.assertIn("CLM-0011", context)
            self.assertNotIn('"narrative_job"', context)
            self.assertNotIn("permitted_claims", context)
            self.assertNotIn("source_refs", context)

            forbidden = [
                "02_outline/voice-profile.md",
                "02_outline/story-bible.md",
                "03_sections/P01/brief.md",
                "02_outline/outline.json",
                "claim-ledger.json",
                "source-index.json",
                "story-plan.json",
                "outcome-evaluation.md",
                "Fall Of Civilization writing style- example.md",
                "competitor's scripts",
                "material-ledger.json",
                "story-material-map.json",
            ]
            for value in forbidden:
                self.assertNotIn(value, context)


if __name__ == "__main__":
    unittest.main()
