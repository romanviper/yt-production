from __future__ import annotations

import base64
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.context_packet import compile_packet
from scripts.historical_substrate_adoption import section_adopts_historical_substrate
from scripts.historical_substrate_contract import FORBIDDEN_NARRATIVE_FIELDS
from scripts.materialize_sections import materialize
from scripts.substrate_preflight import verify_canonical_section_state


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PRODUCT = REPO_ROOT / "products" / "sumer-writing"
EXPECTED_IDS = ["HS-P01-0001", "HS-P01-0003", "HS-P01-0004", "HS-P01-0007"]


def _b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def _forbidden_keys(value: object, prefix: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            here = f"{prefix}.{key}"
            if key in FORBIDDEN_NARRATIVE_FIELDS:
                found.append(here)
            found.extend(_forbidden_keys(child, here))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_forbidden_keys(child, f"{prefix}[{index}]"))
    return found


class P01FrozenProbeGate(unittest.TestCase):
    def test_current_p01_is_ready_for_clean_historical_substrate_probe(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "sumer-writing"
            shutil.copytree(SOURCE_PRODUCT, product)

            # Gate 1: execute the normal bounded materialization path.  The
            # checked-in derived state must be exactly reproducible from
            # outline + approved overlay + product Historical Substrate.
            created = materialize(product, section="P01")
            self.assertTrue(created)
            self.assertTrue(section_adopts_historical_substrate(product, "P01"))

            source_state = json.loads(
                (SOURCE_PRODUCT / "03_sections" / "P01" / "section.json").read_text(encoding="utf-8")
            )
            source_projection = json.loads(
                (SOURCE_PRODUCT / "03_sections" / "P01" / "historical-substrate.json").read_text(encoding="utf-8")
            )
            state = json.loads((product / "03_sections" / "P01" / "section.json").read_text(encoding="utf-8"))
            projection = json.loads(
                (product / "03_sections" / "P01" / "historical-substrate.json").read_text(encoding="utf-8")
            )
            self.assertEqual(source_state, state)
            self.assertEqual(source_projection, projection)

            # Gate 2: critical P01 preflight only.
            self.assertEqual([], verify_canonical_section_state(product, "P01"))
            self.assertEqual(1, state["historical_substrate_contract_version"])
            self.assertEqual(EXPECTED_IDS, state["historical_substrate_ids"])
            self.assertEqual(EXPECTED_IDS, [item["id"] for item in projection["primitives"]])
            self.assertTrue(projection["boundaries"])
            self.assertFalse(_forbidden_keys(projection))
            for primitive in projection["primitives"]:
                self.assertIsInstance(primitive.get("world"), dict)
                self.assertTrue(primitive["world"])

            # Gate 3: compile the canonical Writer packet that the adopted P01
            # path produces, then add only a task-local noncanonical output
            # bound for this experiment.  No story method is supplied here.
            canonical_packet, canonical_context = compile_packet(
                product,
                "draft_section",
                "T9900-draft-section-P01",
                section="P01",
            )
            input_paths = [item["path"] for item in canonical_packet["inputs"]]
            self.assertIn("03_sections/P01/historical-substrate.json", input_paths)
            self.assertNotIn("03_sections/P01/evidence-pack.json", input_paths)
            self.assertNotIn("03_sections/P01/materials.json", input_paths)
            self.assertNotIn("01_research/claim-ledger.json", input_paths)
            self.assertNotIn("01_research/source-index.json", input_paths)
            self.assertIn("Historical Substrate is the primary history model", canonical_context)
            self.assertIn("Evidence access is secondary verification only", canonical_context)
            self.assertNotIn("COMPACT EVIDENCE SUBSET", canonical_context)

            forbidden_path_fragments = (
                "probe-1", "probe-2", "probe-3", "probe-4", "feedback",
                "competitor's scripts", "outcome-evaluation.md", "review.md",
            )
            all_packet_paths = list(canonical_packet.get("instruction_files", [])) + input_paths
            for fragment in forbidden_path_fragments:
                self.assertFalse(any(fragment in path for path in all_packet_paths), fragment)

            probe_contract = {
                "schema_version": 1,
                "experiment": "P01-HSUB-CLEAN-PROBE-01",
                "canonical_output": False,
                "section": "P01",
                "output_language": "vi",
                "target_words": {"min": 450, "max": 650},
                "output_scope": (
                    "Write one contiguous passage from the larger unfinished P01. "
                    "Do not compress, summarize, or complete the whole section."
                ),
                "completion_rule": "P01 must remain unfinished after this passage.",
                "context_rule": (
                    "Use only this task-local bound plus the canonical Writer context below. "
                    "Do not inspect the repository or previous probes, feedback, reviews, or competitor prose."
                ),
            }
            effective_context = (
                "# TASK-LOCAL EXPERIMENT BOUND\n\n"
                + json.dumps(probe_contract, ensure_ascii=False, indent=2)
                + "\n\n# CANONICAL P01 WRITER CONTEXT\n\n"
                + canonical_context
            )
            effective_sha = hashlib.sha256(effective_context.encode("utf-8")).hexdigest()
            probe_packet = {
                "schema_version": 1,
                "operation": "p01_historical_substrate_clean_probe",
                "canonical_output": False,
                "section": "P01",
                "target_words": probe_contract["target_words"],
                "canonical_packet_context_sha256": canonical_packet["context_sha256"],
                "canonical_section_projection_sha256": canonical_packet["historical_substrate"]["section_projection_sha256"],
                "effective_context_sha256": effective_sha,
                "canonical_packet": canonical_packet,
                "probe_contract": probe_contract,
            }

            summary = {
                "status": "AUTHORIZED_TO_RUN_FRESH_P01_PROBE",
                "selected_substrate_ids": EXPECTED_IDS,
                "preflight_errors": [],
                "writer_inputs": input_paths,
                "instruction_files": canonical_packet.get("instruction_files", []),
                "evidence_mode": "secondary_verification_only",
                "effective_context_sha256": effective_sha,
            }
            print("P01_PROBE_GATE_SUMMARY=" + json.dumps(summary, ensure_ascii=False, sort_keys=True))
            print("P01_PROBE_PACKET_B64=" + _b64(json.dumps(probe_packet, ensure_ascii=False, indent=2) + "\n"))
            print("P01_PROBE_CONTEXT_B64=" + _b64(effective_context))


if __name__ == "__main__":
    unittest.main()
