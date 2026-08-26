from __future__ import annotations

import unittest
from pathlib import Path

from scripts.excerpt_packet import compile_excerpt_packet
from scripts.materialize_sections import materialize
from test_material_aware_handoff import SOURCE_PRODUCT, make_direct_authorship_fixture


LOCAL_JOB = (
    "Make the audience feel why information must outlast the people and action that first produced it."
)
STOP_RULE = (
    "Stop when a durable external trace first becomes valuable; leave its later forms unexplained."
)


class WriterExcerptPacketTests(unittest.TestCase):
    def test_excerpt_is_a_slice_not_a_miniature_section(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            packet, context = compile_excerpt_packet(
                product,
                "P01",
                position="opening",
                target_words={"min": 300, "max": 400},
                local_job=LOCAL_JOB,
                completion_rule=STOP_RULE,
                claim_ids=["CLM-0001"],
            )

            self.assertEqual("draft_excerpt", packet["operation"])
            self.assertFalse(packet["canonical_output"])
            self.assertEqual({"min": 300, "max": 400}, packet["target_words"])
            self.assertEqual(["CLM-0001"], packet["selected_claim_ids"])
            self.assertIn('"whole_section_target_words": {\n    "min": 500,\n    "max": 800', context)
            self.assertIn('"excerpt_target_words": {\n    "min": 300,\n    "max": 400', context)
            self.assertIn("one contiguous slice of the longer section", context)
            self.assertIn("not a compressed target for the whole section", context)
            self.assertIn("continuity and presence of a historical novel", context)
            self.assertIn("Approved fact for P01.", context)
            self.assertNotIn("CLM-0001", context)
            self.assertNotIn('"whole_section_mission"', context)
            self.assertNotIn('"whole_section_exit_state"', context)
            self.assertNotIn("State 1", context)
            self.assertNotIn("Make the approved mission answerable", context)

    def test_current_p01_opening_probe_exposes_only_one_local_claim(self) -> None:
        packet, context = compile_excerpt_packet(
            SOURCE_PRODUCT,
            "P01",
            position="opening",
            target_words={"min": 300, "max": 400},
            local_job=(
                "Make finite human memory and growing administrative load create a need for a durable external trace."
            ),
            completion_rule=(
                "Stop when durable recording becomes desirable; do not introduce the later token-seal-tablet ecology."
            ),
            claim_ids=["CLM-0014"],
        )

        self.assertEqual(["CLM-0014"], packet["selected_claim_ids"])
        self.assertIn("Administrative scale is a major formation pressure", context)
        self.assertNotIn("Numerical systems provide", context)
        self.assertNotIn("Neolithic clay objects", context)
        self.assertNotIn("direct token→tablet→writing", context)
        self.assertNotIn("feedback model", context)
        self.assertNotIn("CLM-0014", context)
        self.assertNotIn("formation là một ecology", context)
        self.assertNotIn('"whole_section_exit_state"', context)
        self.assertLess(packet["target_words"]["max"], 1550)

    def test_excerpt_rejects_out_of_scope_claim_and_full_section_sized_probe(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            with self.assertRaisesRegex(ValueError, "outside approved section scope"):
                compile_excerpt_packet(
                    product,
                    "P01",
                    position="opening",
                    target_words={"min": 300, "max": 400},
                    local_job=LOCAL_JOB,
                    completion_rule=STOP_RULE,
                    claim_ids=["CLM-0002"],
                )
            with self.assertRaisesRegex(ValueError, "smaller than the full section target"):
                compile_excerpt_packet(
                    product,
                    "P01",
                    position="opening",
                    target_words={"min": 500, "max": 800},
                    local_job=LOCAL_JOB,
                    completion_rule=STOP_RULE,
                    claim_ids=["CLM-0001"],
                )


if __name__ == "__main__":
    unittest.main()
