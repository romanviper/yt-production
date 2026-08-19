from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.context_packet import compile_packet
from scripts.draft_evidence import DraftEvidenceBroker, EvidenceAccessError
from scripts.materialize_sections import materialize
from scripts.new_product import DEFAULT_TEMPLATE_ROOT, create_product
from scripts.story_plan_contract import verify_narration_pack
from scripts.task import create_task, validate_output_contract


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PRODUCT = REPO_ROOT / "products" / "sumer-writing"


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_direct_authorship_fixture(root: Path) -> Path:
    product = create_product(root / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
    product_state = json.loads((product / "product.json").read_text(encoding="utf-8"))
    product_state["target"] = {"duration_minutes": {"min": 15, "max": 24}, "narration_wpm": 100}
    product_state["stages"]["research"] = "complete"
    write_json(product / "product.json", product_state)

    sources = [
        {
            "id": "SRC-0001",
            "title": "Primary Source One",
            "type": "primary",
            "authority": "primary",
            "status": "reviewed",
            "url": "https://example.com/one",
            "locators": ["p. 10"],
            "limitations": ["Bounded fixture source."],
            "notes": ["Contains a measured object description."],
            "provenance": [{"workstream": "WS01", "local_id": "WS01-SRC-001"}],
        },
        {
            "id": "SRC-0002",
            "title": "Unrelated Source Two",
            "type": "primary",
            "authority": "primary",
            "status": "reviewed",
            "url": "https://example.com/two",
            "locators": ["p. 20"],
            "limitations": ["Belongs to another section."],
            "notes": ["UNRELATED_NEEDLE"],
            "provenance": [{"workstream": "WS02", "local_id": "WS02-SRC-001"}],
        },
    ]
    claims = [
        {
            "id": "CLM-0001",
            "statement": "Approved fact for P01.",
            "type": "fact",
            "confidence": "high",
            "status": "supported",
            "sources": ["SRC-0001"],
            "counterevidence": "None in fixture.",
            "provenance": [{"workstream": "WS01", "local_id": "WS01-CLM-001"}],
        },
        {
            "id": "CLM-0002",
            "statement": "Approved fact for P02 only.",
            "type": "fact",
            "confidence": "high",
            "status": "supported",
            "sources": ["SRC-0002"],
            "counterevidence": "None in fixture.",
            "provenance": [{"workstream": "WS02", "local_id": "WS02-CLM-001"}],
        },
    ]
    write_json(product / "01_research" / "source-index.json", {"schema_version": 1, "product": "demo", "status": "complete", "sources": sources})
    write_json(product / "01_research" / "claim-ledger.json", {"schema_version": 1, "product": "demo", "status": "complete", "claims": claims})
    write_json(
        product / "01_research" / "material-ledger.json",
        {
            "schema_version": 2,
            "product": "demo",
            "status": "complete",
            "purpose": "optional_evidence_preservation",
            "materials": [
                {
                    "id": "MAT-0001",
                    "kind": "object",
                    "label": "Optional preserved object detail",
                    "details": {"measurement": "12 cm"},
                    "claim_ids": ["CLM-0001"],
                    "source_refs": [{"source_id": "SRC-0001", "locators": ["p. 10"]}],
                    "limitations": ["Measurement only; no story route implied."],
                    "provenance": [{"workstream": "WS01", "local_id": "WS01-MAT-001"}],
                }
            ],
        },
    )

    cycle = product_state["production_cycle"]["id"]
    sections = []
    for number, claim_id in [(1, "CLM-0001"), (2, "CLM-0002"), (3, "CLM-0002")]:
        sections.append(
            {
                "id": f"P{number:02d}",
                "order": number,
                "title": f"Part {number}",
                "movement_ids": [f"M{number:02d}"],
                "narrative_job": f"Change listener state from {number - 1} to {number} without prescribing how.",
                "entry_state": f"State {number - 1}",
                "exit_state": f"State {number}",
                "transition": "The new state makes the next question necessary." if number < 3 else "Close the central question.",
                "claim_ids": [claim_id],
                "dependencies": [f"P{number - 1:02d}"] if number > 1 else [],
                "non_goal": "Do not invent unsupported evidence.",
                "target_words": {"min": 500, "max": 800},
            }
        )
    outline = {
        "schema_version": 4,
        "product": "demo",
        "cycle_id": cycle,
        "status": "approved",
        "section_count": 3,
        "script_architecture": {
            "writer_authorship_contract_version": 1,
            "central_question": "How does the system change?",
            "audience_promise": "Follow one bounded transformation.",
            "design_rationale": "Architecture defines destination and evidence territory, not narrative route.",
            "total_word_envelope": {"min": 1500, "max": 2400},
            "acts": [
                {"id": "A01", "order": 1, "role": "opening", "title": "Opening", "narrative_job": "Open the question.", "entry_state": "Unknown.", "exit_state": "Question defined.", "movement_ids": ["M01"]},
                {"id": "A02", "order": 2, "role": "body", "title": "Body", "narrative_job": "Develop the mechanism.", "entry_state": "Question defined.", "exit_state": "Mechanism understood.", "movement_ids": ["M02"]},
                {"id": "A03", "order": 3, "role": "ending", "title": "Ending", "narrative_job": "Close the question.", "entry_state": "Mechanism understood.", "exit_state": "Question resolved.", "movement_ids": ["M03"]},
            ],
            "movements": [
                {"id": "M01", "order": 1, "act_id": "A01", "title": "Question", "narrative_job": "Define the problem.", "entry_state": "Unknown.", "exit_state": "Question defined.", "section_ids": ["P01"]},
                {"id": "M02", "order": 2, "act_id": "A02", "title": "Mechanism", "narrative_job": "Develop the mechanism.", "entry_state": "Question defined.", "exit_state": "Mechanism understood.", "section_ids": ["P02"]},
                {"id": "M03", "order": 3, "act_id": "A03", "title": "Resolution", "narrative_job": "Resolve the problem.", "entry_state": "Mechanism understood.", "exit_state": "Question resolved.", "section_ids": ["P03"]},
            ],
        },
        "sections": sections,
    }
    write_json(product / "02_outline" / "outline.json", outline)
    return product


class AuthorshipBoundaryRegression(unittest.TestCase):
    def test_creative_route_freedom_is_not_a_schema_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            root = product / "03_sections" / "P01"

            self.assertEqual("ready_for_draft", json.loads((root / "section.json").read_text(encoding="utf-8"))["status"])
            self.assertFalse((root / "story-plan.json").exists())
            self.assertFalse((root / "material-pack.json").exists())

            packet, context = compile_packet(product, "draft_section", "T9999-draft-section-P01", section="P01")
            self.assertIn("evidence_access", packet)
            self.assertNotIn("material-pack.json", context)
            self.assertNotIn("story-plan.json", context)
            self.assertNotIn("material_ids", context)
            self.assertNotIn("what_audience_follows", context)

            # A deliberately non-carrier-specific route is system-valid. Quality remains a review concern.
            (root / "draft.md").write_text(
                "# P01\n\nThe section develops the approved question through a comparative conceptual route using only the permitted fact.\n",
                encoding="utf-8",
            )
            (root / "handoff.md").write_text("Listener reaches State 1.\n", encoding="utf-8")
            work = {"operation": "draft_section", "target": {"section": "P01"}}
            self.assertEqual([], validate_output_contract(product, work))

    def test_retrieval_increases_resolution_but_cannot_escape_claim_source_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            work = create_task(product, "draft_section", "P01", None, False)
            broker = DraftEvidenceBroker(product, work["id"])

            scope = broker.call("scope")
            self.assertEqual(["CLM-0001"], scope["claim_ids"])
            self.assertEqual(["SRC-0001"], scope["source_ids"])

            allowed = broker.call("source", {"id": "SRC-0001"})
            self.assertEqual("SRC-0001", allowed["source"]["id"])
            self.assertEqual("12 cm", allowed["preserved_details"][0]["details"]["measurement"])
            with self.assertRaises(EvidenceAccessError):
                broker.call("source", {"id": "SRC-0002"})
            with self.assertRaises(EvidenceAccessError):
                broker.call("claims", {"ids": ["CLM-0002"]})

            searched = broker.call("search", {"query": "UNRELATED_NEEDLE", "limit": 10})
            self.assertEqual([], searched["results"])
            recorded = broker.call(
                "record",
                {"source_id": "SRC-0001", "parent_locator": "p. 10", "locator": "p. 10, table 2", "detail": "Measured dimension is 12 cm."},
            )
            self.assertTrue(recorded["truth_ceiling_unchanged"])

            trace = [json.loads(line) for line in (product / "tasks" / work["id"] / "evidence-trace.jsonl").read_text(encoding="utf-8").splitlines()]
            source_entry = next(item for item in trace if item["capability"] == "source" and item["response"])
            self.assertEqual("SRC-0001", source_entry["response"]["source"]["id"])
            record_entry = next(item for item in trace if item["capability"] == "record")
            self.assertEqual("Measured dimension is 12 cm.", record_entry["response"]["detail"])

    def test_c003_compatibility_path_no_longer_requires_material_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "products" / "sumer-writing"
            shutil.copytree(SOURCE_PRODUCT, product)
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

            materialize(product)
            root = product / "03_sections" / "P01"
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertEqual("ready_for_draft", state["status"])
            self.assertFalse((root / "material-pack.json").exists())
            self.assertFalse((root / "story-plan.json").exists())
            self.assertEqual([], verify_narration_pack(product, "P01"))

            packet, context = compile_packet(product, "draft_section", "T9998-draft-section-P01", section="P01")
            self.assertNotIn("material-pack.json", [item["path"] for item in packet["inputs"]])
            self.assertIn("evidence_access", packet)
            # Legacy C003 outline still contains route-heavy narrative_job content.
            # The system correction must not rewrite product content to hide that migration blocker.
            self.assertIn("MAT-0001", context)


if __name__ == "__main__":
    unittest.main()
