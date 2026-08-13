from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.assemble import assemble_product
from scripts.approval import approve_plan, approve_section, approve_story_plan, request_changes, request_story_plan_changes
from scripts.context_packet import compile_packet
from scripts.consolidate_research import consolidate, verify_consolidation
from scripts.governance import classify_paths, commit_scope_errors, product_task_violations
from scripts.impact import calculate_impact
from scripts.materialize_research import materialize as materialize_research
from scripts.materialize_sections import materialize as materialize_sections
from scripts.new_product import DEFAULT_TEMPLATE_ROOT, create_product
from scripts.operator_brief import MAX_RENDERED_WORDS, render_brief, validate_brief
from scripts.outline_contract import validate_outline_contract
from scripts.packet_contract import PACKET_COMPILER, PACKET_SCHEMA_VERSION
from scripts.story_plan_contract import build_narration_pack, verify_narration_pack
from scripts.task import create_task, submit_task, verify_task
from scripts.validate import validate_product
from scripts.common import word_count


REPO_ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_approved_outline(product: Path, section_count: int = 10) -> None:
    source = {
        "id": "SRC-0001",
        "title": "Source",
        "status": "reviewed",
        "locators": ["p. 1"],
        "limitations": "Fixture only",
    }
    claim = {
        "id": "CLM-0001",
        "statement": "Supported fixture claim.",
        "type": "fact",
        "confidence": "high",
        "status": "supported",
        "sources": ["SRC-0001"],
        "counterevidence": "None in fixture",
    }
    write_json(product / "01_research" / "source-index.json", {"schema_version": 1, "product": product.name, "status": "complete", "sources": [source]})
    write_json(product / "01_research" / "claim-ledger.json", {"schema_version": 1, "product": product.name, "status": "complete", "claims": [claim]})
    sections = []
    for number in range(1, section_count + 1):
        section_id = f"P{number:02d}"
        minimum = 500 + number * 50
        maximum = minimum + 200 + (number % 3) * 100
        sections.append(
            {
                "id": section_id,
                "order": number,
                "title": f"Part {number}",
                "movement_id": "M01",
                "structural_role": f"Distinct state transition {number}.",
                "narrative_job": f"Move story state {number - 1} to {number}.",
                "entry_state": f"State {number - 1}",
                "exit_state": f"State {number}",
                "question": f"What changes in part {number}?",
                "payoff": f"Resolve turn {number}.",
                "claim_ids": ["CLM-0001"],
                "dependencies": [f"P{number - 1:02d}"] if number > 1 else [],
                "anchor_requirements": "Evidence-backed object.",
                "bridge_in": "Prior state.",
                "bridge_out": "Next state.",
                "boundary": "Do not explain the next part.",
                "risk": "Overclaim.",
                "target_words": {"min": minimum, "max": maximum},
                "budget_rationale": f"Part {number} receives only the space required for its distinct state change.",
                "planned_moves": ["Open the local question.", "Produce the state change."],
            }
        )
    total_min = sum(item["target_words"]["min"] for item in sections)
    total_max = sum(item["target_words"]["max"] for item in sections)
    product_state = json.loads((product / "product.json").read_text(encoding="utf-8"))
    product_state["target"] = {
        "duration_minutes": {"min": total_min / 100, "max": total_max / 100},
        "narration_wpm": 100,
    }
    write_json(product / "product.json", product_state)
    write_json(
        product / "02_outline" / "outline.json",
        {
            "schema_version": 3,
            "product": product.name,
            "status": "approved",
            "section_count": section_count,
            "script_architecture": {
                "audience_promise": "Follow one complete causal transformation.",
                "design_rationale": "The whole arc is designed before bounded production work units are cut.",
                "total_word_envelope": {"min": total_min, "max": total_max},
                "movements": [
                    {
                        "id": "M01",
                        "order": 1,
                        "title": "Complete movement",
                        "narrative_job": "Carry the audience through the complete test arc.",
                        "entry_state": "The causal problem is unresolved.",
                        "exit_state": "The causal problem is resolved.",
                        "section_ids": [item["id"] for item in sections],
                    }
                ],
            },
            "sections": sections,
        },
    )


def make_approved_story_plan(product: Path, section: str) -> None:
    root = product / "03_sections" / section
    evidence = json.loads((root / "evidence-pack.json").read_text(encoding="utf-8"))
    state = json.loads((root / "section.json").read_text(encoding="utf-8"))
    claim_ids = [item["id"] for item in evidence["claims"]]
    write_json(
        root / "story-plan.json",
        {
            "schema_version": 2,
            "section": section,
            "status": "draft",
            "governing_idea": "A record changes what an institution can remember and enforce.",
            "audience_question": "Why does this small record matter?",
            "audience_payoff": "The object matters because it changes what can persist beyond one encounter.",
            "structure_shape": "A compact object mystery turns once into a bounded institutional consequence.",
            "word_budget": {
                "recommended": state["target_words"],
                "rationale": "The range matches one object, one explanatory turn and one concrete payoff without padding.",
            },
            "evidence_roles": {
                "narrated": claim_ids[:1],
                "support": [],
                "guardrail": [],
                "omit": claim_ids[1:],
            },
            "claim_use": {claim_ids[0]: "It proves the durable capacity revealed in the payoff."},
            "beats": [
                {"id": "B01", "function": "hook", "purpose": "Begin with the bounded object and one unresolved problem.", "audience_change": "The object becomes a problem rather than an exhibit.", "claim_ids": claim_ids[:1]},
                {"id": "B02", "function": "tension", "purpose": "Show why memory alone cannot settle the problem.", "audience_change": "The audience sees the limit that demands a record.", "claim_ids": []},
                {"id": "B03", "function": "payoff", "purpose": "Reveal the new capacity created by the record.", "audience_change": "The audience can name the capacity gained.", "claim_ids": []},
                {"id": "B04", "function": "bridge", "purpose": "Carry that capacity into the next institutional change.", "audience_change": "The solution now creates the next historical question.", "claim_ids": []},
            ],
            "terminology": [],
            "opening_move": "Put one object in front of the audience and make its unresolved job visible.",
            "ending_move": "Name the concrete capacity gained and point to the next pressure it creates.",
            "comprehension_test": "The audience can explain the change in one ordinary sentence.",
        },
    )
    approve_story_plan(product, section)


def valid_operator_brief() -> dict:
    return {
        "schema_version": 1,
        "status": "ready_for_review",
        "headline": "Research plan đã sẵn sàng để bạn kiểm duyệt.",
        "material_points": [
            "Plan giữ đúng subject và chia trách nhiệm research rõ ràng.",
            "Một boundary nhỏ cần được theo dõi khi synthesis.",
        ],
        "decision": {
            "required": True,
            "question": "Bạn muốn duyệt plan hay yêu cầu chỉnh boundary trước?",
            "recommendation": "Chỉnh boundary nhỏ rồi duyệt plan.",
            "options": [
                {"label": "Chỉnh trước", "effect": "Plan được patch; research chưa chạy."},
                {"label": "Duyệt", "effect": "Mở research workstreams theo plan hiện tại."},
            ],
        },
        "next_step": "",
    }


def add_research_contract(plan: dict) -> dict:
    plan["shared_research_protocol"] = {
        "chronology": ["Use qualified date ranges."],
        "terminology": ["Define contested terms."],
        "case_selection": ["Choose cases for evidence, not spectacle."],
        "cross_cutting_ownership": {"memory": "WS01 establishes the bounded fixture handoff."},
        "handoff_contract": ["Return chronology, claims, unknowns and dependencies."],
    }
    for item in plan.get("workstreams", []):
        item.setdefault("ownership", f"Own only the question of {item.get('id', 'this unit')}.")
        item.setdefault("synthesis_handoff", ["Bounded findings and unresolved questions."])
    return plan
    (product / "02_outline" / "story-bible.md").write_text(
        "# Story Bible\n\nPremise, causal spine, terminology and global exclusions.\n",
        encoding="utf-8",
    )


class ModularProductionTests(unittest.TestCase):
    def test_pilot_validates_before_research(self) -> None:
        issues = validate_product(REPO_ROOT / "products" / "sumer-writing")
        errors = [issue for issue in issues if issue.level == "ERROR"]
        self.assertEqual([], errors, "\n".join(str(issue) for issue in errors))

    def test_new_product_has_operation_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo-history", "Demo History", DEFAULT_TEMPLATE_ROOT)
            expected = [
                "00_brief/product-brief.md",
                "01_research/plan.json",
                "01_research/research-synthesis.md",
                "02_outline/outline.json",
                "02_outline/story-bible.md",
                "02_outline/voice-profile.md",
                "03_sections/README.md",
                "04_integration/README.md",
                "05_delivery/README.md",
            ]
            for relative in expected:
                self.assertTrue((product / relative).is_file(), relative)
            self.assertFalse((product / "work-order.json").exists())

    def test_product_task_cannot_modify_protected_system_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            # Governance resolves real repo-relative product paths, so use the pilot path for a synthetic work order.
            pilot = REPO_ROOT / "products" / "sumer-writing"
            work = {
                "id": "T0001-research-plan",
                "authority": "product_agent",
                "target": {"section": None, "unit": None},
                "allowed_write_paths": [
                    "01_research/plan.json",
                    "tasks/T0001-research-plan/report.md",
                    "tasks/T0001-research-plan/operator-brief.json",
                ],
            }
            allowed = ["products/sumer-writing/01_research/plan.json"]
            self.assertEqual([], product_task_violations(pilot, work, allowed))
            violations = product_task_violations(
                pilot,
                work,
                allowed + ["system/core/invariants.md", "scripts/materialize_research.py"],
            )
            self.assertEqual(2, len(violations))
            self.assertTrue(all("protected system path" in item for item in violations))

    def test_system_and_product_changes_must_use_separate_commits(self) -> None:
        self.assertEqual([], commit_scope_errors(["system/core/invariants.md", "scripts/task.py"]))
        self.assertEqual([], commit_scope_errors(["products/sumer-writing/01_research/plan.json"]))
        errors = commit_scope_errors(["system/core/invariants.md", "products/sumer-writing/01_research/plan.json"])
        self.assertEqual(1, len(errors))
        classified = classify_paths(["AGENTS.md", "products/sumer-writing/product.json"])
        self.assertEqual(["AGENTS.md"], classified["system"])
        self.assertEqual(["products/sumer-writing/product.json"], classified["product"])

    def test_new_tasks_are_product_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            state["stages"]["direction"] = "approved"
            write_json(product / "product.json", state)
            work = create_task(product, "research_plan", None, None, False)
            packet = json.loads((product / work["packet_manifest"]).read_text(encoding="utf-8"))
            self.assertEqual("product_agent", work["authority"])
            self.assertEqual("product_agent", packet["authority"])
            self.assertEqual(PACKET_SCHEMA_VERSION, packet["schema_version"])
            self.assertEqual(PACKET_COMPILER, packet["compiler"])

    def test_research_workstreams_are_isolated(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            plan = json.loads((REPO_ROOT / "products" / "sumer-writing" / "01_research" / "plan.json").read_text(encoding="utf-8"))
            add_research_contract(plan)
            plan["status"] = "approved"
            write_json(product / "01_research" / "plan.json", plan)
            materialize_research(product)
            packet, context = compile_packet(product, "research_workstream", "T0001", unit="WS02")
            self.assertIn("01_research/workstreams/WS02/brief.md", context)
            self.assertNotIn("01_research/workstreams/WS01/brief.md", context)
            self.assertNotIn("01_research/workstreams/WS03/brief.md", context)
            self.assertEqual(3, len(packet["operation_outputs"]))
            self.assertIn("system/standards/operator-interface.md", packet["instruction_files"])
            brief = (product / "01_research" / "workstreams" / "WS02" / "brief.md").read_text(encoding="utf-8")
            self.assertIn("## Ownership", brief)
            self.assertIn("## Required synthesis handoff", brief)
            self.assertIn("## Shared research protocol", brief)
            self.assertIn("### Chronology", brief)
            self.assertIn("### Cross-cutting ownership", brief)

    def test_plan_cannot_be_approved_without_executable_handoff_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            plan = json.loads((REPO_ROOT / "products" / "sumer-writing" / "01_research" / "plan.json").read_text(encoding="utf-8"))
            # Keep this test independent from the current Sumer product state.
            plan.pop("shared_research_protocol", None)
            write_json(product / "01_research" / "plan.json", plan)
            with self.assertRaisesRegex(ValueError, "shared_research_protocol"):
                approve_plan(product)
            add_research_contract(plan)
            write_json(product / "01_research" / "plan.json", plan)
            approve_plan(product)
            approved = json.loads((product / "01_research" / "plan.json").read_text(encoding="utf-8"))
            self.assertEqual("approved", approved["status"])

    def test_research_synthesis_requires_every_declared_workstream(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            plan = {
                "schema_version": 1,
                "status": "approved",
                "central_research_question": "How did it change?",
                "hypotheses_to_test": [],
                "workstreams": [
                    {
                        "id": unit,
                        "title": unit,
                        "question": f"Question {unit}",
                        "in_scope": "One responsibility.",
                        "out_of_scope": "The other responsibility.",
                        "required_evidence": ["Primary source"],
                        "completion_criteria": ["Answer the question"],
                    }
                    for unit in ["WS01", "WS02"]
                ],
                "coverage_matrix": {},
                "synthesis_questions": [],
            }
            add_research_contract(plan)
            write_json(product / "01_research" / "plan.json", plan)
            materialize_research(product)
            for unit in ["WS01"]:
                root = product / "01_research" / "workstreams" / unit
                write_json(root / "sources.json", {"schema_version": 1, "workstream": unit, "status": "complete", "sources": []})
                write_json(root / "claims.json", {"schema_version": 1, "workstream": unit, "status": "complete", "claims": []})
                (root / "synthesis.md").write_text(f"# {unit}\n\nStatus: complete\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Incomplete workstream ledgers: WS02"):
                compile_packet(product, "research_synthesis", "T0001")

            root = product / "01_research" / "workstreams" / "WS02"
            write_json(root / "sources.json", {"schema_version": 1, "workstream": "WS02", "status": "complete", "sources": []})
            write_json(root / "claims.json", {"schema_version": 1, "workstream": "WS02", "status": "complete", "claims": []})
            (root / "synthesis.md").write_text("# WS02\n\nStatus: complete\n", encoding="utf-8")
            consolidate(product)
            packet, context = compile_packet(product, "research_synthesis", "T0002")
            self.assertTrue(packet["inputs"])
            self.assertTrue(all(set(record) == {"path", "sha256", "bytes"} for record in packet["inputs"]))
            input_paths = [record["path"] for record in packet["inputs"]]
            self.assertIn("01_research/workstreams/WS01/synthesis.md", context)
            self.assertIn("01_research/workstreams/WS02/synthesis.md", context)
            self.assertNotIn("01_research/workstreams/WS01/claims.json", input_paths)
            self.assertNotIn("01_research/workstreams/WS02/sources.json", input_paths)
            self.assertEqual(["01_research/research-synthesis.md"], packet["operation_outputs"])
            self.assertLess(packet["estimated_context_tokens"], packet["max_context_tokens"])

    def test_research_consolidation_deduplicates_sources_and_preserves_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            plan = {
                "schema_version": 1,
                "status": "approved",
                "workstreams": [{"id": unit} for unit in ["WS01", "WS02"]],
            }
            write_json(product / "01_research" / "plan.json", plan)
            for number, unit in enumerate(["WS01", "WS02"], start=1):
                root = product / "01_research" / "workstreams" / unit
                write_json(
                    root / "sources.json",
                    {
                        "schema_version": 1,
                        "workstream": unit,
                        "status": "complete",
                        "sources": [
                            {
                                "id": f"{unit}-SRC-001",
                                "title": "Shared source",
                                "author": "Historian",
                                "url": "https://example.com/shared",
                                "locators": [f"p. {number}"],
                                "limitations": [f"Limit {number}"],
                            }
                        ],
                    },
                )
                write_json(
                    root / "claims.json",
                    {
                        "schema_version": 1,
                        "workstream": unit,
                        "status": "complete",
                        "claims": [
                            {
                                "id": f"{unit}-CLM-001",
                                "statement": f"Distinct claim {number}.",
                                "sources": [f"{unit}-SRC-001"],
                            }
                        ],
                    },
                )
                (root / "synthesis.md").write_text(f"# {unit}\n\nStatus: complete\n", encoding="utf-8")
            consolidate(product)
            self.assertEqual([], verify_consolidation(product))
            sources = json.loads((product / "01_research" / "source-index.json").read_text(encoding="utf-8"))["sources"]
            claims = json.loads((product / "01_research" / "claim-ledger.json").read_text(encoding="utf-8"))["claims"]
            self.assertEqual(1, len(sources))
            self.assertEqual(2, len(sources[0]["provenance"]))
            self.assertEqual(["SRC-0001"], claims[0]["sources"])
            self.assertEqual(["SRC-0001"], claims[1]["sources"])

    def test_ten_part_draft_packet_contains_only_selected_part(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 10)
            materialize_sections(product)
            make_approved_story_plan(product, "P06")
            packet, context = compile_packet(product, "draft_section", "T0001", section="P06")
            self.assertIn("03_sections/P06/brief.md", context)
            self.assertIn("03_sections/P06/story-plan.json", context)
            self.assertIn("03_sections/P06/narration-pack.json", context)
            self.assertNotIn("# BEGIN INPUT: 03_sections/P06/evidence-pack.json", context)
            self.assertNotIn("03_sections/P05/brief.md", context)
            self.assertNotIn("03_sections/P07/brief.md", context)
            self.assertEqual(
                [
                    "03_sections/P06/draft.md",
                    "03_sections/P06/handoff.md",
                    "tasks/T0001/report.md",
                    "tasks/T0001/operator-brief.json",
                ],
                packet["allowed_write_paths"],
            )
            self.assertIn("Operator Interface Standard", context)
            self.assertLess(packet["estimated_context_tokens"], packet["max_context_tokens"])

    def test_outline_contract_materializes_split_question_and_payoff(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 1)
            outline = json.loads((product / "02_outline" / "outline.json").read_text(encoding="utf-8"))
            outline["sections"][0]["anchor_requirements"] = ["Object one.", "Object two."]
            write_json(product / "02_outline" / "outline.json", outline)
            materialize_sections(product)
            brief = (product / "03_sections" / "P01" / "brief.md").read_text(encoding="utf-8")
            self.assertIn("## Question\n\nWhat changes in part 1?", brief)
            self.assertIn("## Payoff\n\nResolve turn 1.", brief)
            self.assertIn("- Object one.\n- Object two.", brief)
            state = json.loads((product / "03_sections" / "P01" / "section.json").read_text(encoding="utf-8"))
            self.assertEqual("needs_story_plan", state["status"])
            self.assertTrue((product / "03_sections" / "P01" / "story-plan.json").is_file())

    def test_outline_architecture_allows_unequal_work_units_but_requires_whole_arc_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 4)
            outline = json.loads((product / "02_outline" / "outline.json").read_text(encoding="utf-8"))
            target = json.loads((product / "product.json").read_text(encoding="utf-8"))["target"]
            self.assertEqual([], validate_outline_contract(outline, {"CLM-0001"}, target))
            self.assertGreater(len({tuple(item["target_words"].values()) for item in outline["sections"]}), 1)
            outline["script_architecture"]["movements"][0]["section_ids"] = ["P01", "P03", "P02", "P04"]
            errors = validate_outline_contract(outline, {"CLM-0001"}, target)
            self.assertTrue(any("contiguously" in item for item in errors))

    def test_legacy_approved_artifacts_remain_readable_but_cannot_be_new_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 1)
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))
            outline["schema_version"] = 2
            outline.pop("script_architecture")
            for item in outline["sections"]:
                for field in ["movement_id", "structural_role", "planned_moves", "budget_rationale"]:
                    item.pop(field)
            write_json(outline_path, outline)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            root = product / "03_sections" / "P01"
            plan = json.loads((root / "story-plan.json").read_text(encoding="utf-8"))
            plan["schema_version"] = 1
            plan.pop("structure_shape")
            plan.pop("word_budget")
            write_json(root / "story-plan.json", plan)
            build_narration_pack(product, "P01")
            target = json.loads((product / "product.json").read_text(encoding="utf-8"))["target"]
            self.assertEqual([], validate_outline_contract(outline, {"CLM-0001"}, target))
            self.assertEqual([], verify_narration_pack(product, "P01"))
            errors = validate_outline_contract(outline, {"CLM-0001"}, target, require_current=True)
            self.assertTrue(any("new or revised output" in item for item in errors))

    def test_story_design_can_choose_two_beats_and_resize_without_padding(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 1)
            product_state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            product_state["target"] = {"duration_minutes": {"min": 3, "max": 10}, "narration_wpm": 100}
            write_json(product / "product.json", product_state)
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))
            outline["script_architecture"]["total_word_envelope"] = {"min": 300, "max": 1000}
            write_json(outline_path, outline)
            materialize_sections(product)
            root = product / "03_sections" / "P01"
            evidence = json.loads((root / "evidence-pack.json").read_text(encoding="utf-8"))
            claim_id = evidence["claims"][0]["id"]
            write_json(
                root / "story-plan.json",
                {
                    "schema_version": 2,
                    "section": "P01",
                    "status": "draft",
                    "governing_idea": "One bounded object can change what survives.",
                    "audience_question": "What survives here?",
                    "audience_payoff": "The selected relation survives without a full scene.",
                    "structure_shape": "A two-step miniature: inspect the object, then reverse what survival means.",
                    "word_budget": {
                        "recommended": {"min": 350, "max": 600},
                        "rationale": "One object and one reversal need less space than the outline first estimated.",
                    },
                    "evidence_roles": {"narrated": [claim_id], "support": [], "guardrail": [], "omit": []},
                    "claim_use": {claim_id: "The object carries the only factual turn required for the payoff."},
                    "beats": [
                        {
                            "id": "B01",
                            "function": "inspection",
                            "purpose": "Make the object's limited content visible.",
                            "audience_change": "The object becomes a bounded question.",
                            "claim_ids": [claim_id],
                        },
                        {
                            "id": "B02",
                            "function": "payoff",
                            "purpose": "Name exactly what can persist.",
                            "audience_change": "The audience can state the limited capacity.",
                            "claim_ids": [],
                        },
                    ],
                    "terminology": [],
                    "opening_move": "Inspect only the information the object actually preserves.",
                    "ending_move": "Resolve the limited capacity without adding a generic bridge.",
                    "comprehension_test": "The audience can name what survives and what does not.",
                },
            )
            approve_story_plan(product, "P01")
            section_state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            revised_outline = json.loads(outline_path.read_text(encoding="utf-8"))
            self.assertEqual({"min": 350, "max": 600}, section_state["target_words"])
            self.assertEqual({"min": 350, "max": 600}, revised_outline["sections"][0]["target_words"])
            self.assertEqual(1, len(revised_outline["script_architecture"]["budget_revisions"]))

    def test_story_design_is_required_before_drafting(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 1)
            materialize_sections(product)
            with self.assertRaisesRegex(ValueError, "does not allow draft_section"):
                compile_packet(product, "draft_section", "T0001", section="P01")
            packet, context = compile_packet(product, "design_section", "T0002", section="P01")
            self.assertIn("03_sections/P01/evidence-pack.json", context)
            self.assertIn("system/standards/voice.md", packet["instruction_files"])
            self.assertEqual(["03_sections/P01/story-plan.json"], packet["operation_outputs"])
            make_approved_story_plan(product, "P01")
            draft_packet, draft_context = compile_packet(product, "draft_section", "T0003", section="P01")
            self.assertIn("03_sections/P01/narration-pack.json", draft_context)
            self.assertNotIn("# BEGIN INPUT: 03_sections/P01/evidence-pack.json", draft_context)
            self.assertEqual("draft_section", draft_packet["operation"])

    def test_story_plan_feedback_creates_a_fresh_design_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 1)
            materialize_sections(product)
            root = product / "03_sections" / "P01"
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            state["status"] = "story_plan_review"
            write_json(root / "section.json", state)
            with self.assertRaisesRegex(ValueError, "does not allow design_section"):
                compile_packet(product, "design_section", "T0001", section="P01")
            request = "Merge the definition beats and remove unsupported participants."
            request_story_plan_changes(product, "P01", request)
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertEqual("story_plan_changes_requested", state["status"])
            packet, context = compile_packet(product, "design_section", "T0002", section="P01")
            self.assertIn(request, context)
            self.assertIn("03_sections/P01/story-plan-change-request.md", [item["path"] for item in packet["inputs"]])

    def test_failed_prose_can_reopen_story_design_without_editing_the_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 1)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            root = product / "03_sections" / "P01"
            (root / "draft.md").write_text("DIAGNOSTIC_DRAFT_THAT_MUST_NOT_BE_EDITED", encoding="utf-8")
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            state["status"] = "ready_for_review"
            write_json(root / "section.json", state)
            request_story_plan_changes(
                product,
                "P01",
                "The prose exposed a padded structure; redesign the shape and reduce its budget.",
            )
            plan = json.loads((root / "story-plan.json").read_text(encoding="utf-8"))
            self.assertEqual("draft", plan["status"])
            packet, context = compile_packet(product, "design_section", "T0001", section="P01")
            self.assertIn("DIAGNOSTIC_DRAFT_THAT_MUST_NOT_BE_EDITED", context)
            self.assertEqual(["03_sections/P01/story-plan.json"], packet["operation_outputs"])

    def test_draft_packet_adds_only_approved_dependency_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            make_approved_story_plan(product, "P02")
            prior = product / "03_sections" / "P01"
            (prior / "handoff.md").write_text("P01_APPROVED_HANDOFF", encoding="utf-8")
            prior_state = json.loads((prior / "section.json").read_text(encoding="utf-8"))
            prior_state.update({"status": "approved", "human_approved": True})
            write_json(prior / "section.json", prior_state)
            future = product / "03_sections" / "P03"
            (future / "handoff.md").write_text("P03_UNAPPROVED_HANDOFF", encoding="utf-8")
            _, context = compile_packet(product, "draft_section", "T0001", section="P02")
            self.assertIn("P01_APPROVED_HANDOFF", context)
            self.assertNotIn("P03_UNAPPROVED_HANDOFF", context)

    def test_integration_review_requires_all_sections_human_approved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 2)
            materialize_sections(product)
            with self.assertRaisesRegex(ValueError, "human-approved section: P01"):
                compile_packet(product, "integration_review", "T0001")
            for section_id in ["P01", "P02"]:
                root = product / "03_sections" / section_id
                (root / "handoff.md").write_text(f"Handoff {section_id}.", encoding="utf-8")
                state = json.loads((root / "section.json").read_text(encoding="utf-8"))
                state.update({"status": "approved", "human_approved": True})
                write_json(root / "section.json", state)
            packet, context = compile_packet(product, "integration_review", "T0002")
            self.assertIn("03_sections/P01/handoff.md", context)
            self.assertIn("03_sections/P02/handoff.md", context)
            self.assertEqual(
                [
                    "04_integration/review.md",
                    "04_integration/change-map.json",
                    "tasks/T0002/report.md",
                    "tasks/T0002/operator-brief.json",
                ],
                packet["allowed_write_paths"],
            )

    def test_task_detects_stale_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            state["stages"]["direction"] = "approved"
            write_json(product / "product.json", state)
            work = create_task(product, "research_plan", None, None, False)
            self.assertEqual([], verify_task(product, work["id"]))
            with (product / "00_brief" / "product-brief.md").open("a", encoding="utf-8") as handle:
                handle.write("\nChanged after packet creation.\n")
            self.assertTrue(any("stale input" in item for item in verify_task(product, work["id"])))

    def test_malformed_packet_is_rejected_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            state["stages"]["direction"] = "approved"
            write_json(product / "product.json", state)
            work = create_task(product, "research_plan", None, None, False)
            packet_path = product / work["packet_manifest"]
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            packet["inputs"] = ["00_brief/product-brief.md"]
            write_json(packet_path, packet)
            errors = verify_task(product, work["id"])
            self.assertTrue(any("compiled record" in item for item in errors))
            issues = validate_product(product)
            self.assertTrue(any("compiled record" in issue.message for issue in issues))

    def test_compiled_context_cannot_be_replaced_after_task_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            state["stages"]["direction"] = "approved"
            write_json(product / "product.json", state)
            work = create_task(product, "research_plan", None, None, False)
            context_path = product / work["context_packet"]
            context_path.write_text("Hand-written replacement.\n", encoding="utf-8")
            self.assertTrue(any("context packet is stale" in item for item in verify_task(product, work["id"])))

    def test_task_submission_requires_changed_artifact_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            state["stages"]["direction"] = "approved"
            write_json(product / "product.json", state)
            work = create_task(product, "research_plan", None, None, False)
            first_errors = submit_task(product, work["id"])
            self.assertTrue(any("missing output" in item or "no declared" in item for item in first_errors))
            self.assertTrue(any("operator brief" in item for item in first_errors))
            plan_path = product / "01_research" / "plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["central_research_question"] = "A real changed question"
            plan["workstreams"] = [
                {
                    "id": "WS01",
                    "title": "Formation",
                    "question": "How did the system form?",
                    "in_scope": "Formation mechanisms.",
                    "out_of_scope": "Later legacy.",
                    "required_evidence": ["Primary evidence", "Scholarly synthesis"],
                    "completion_criteria": ["Sources and claims are explicitly scoped."],
                }
            ]
            add_research_contract(plan)
            write_json(plan_path, plan)
            report = product / "tasks" / work["id"] / "report.md"
            report.write_text(("Detailed evidence and validation record. " * 500) + "\n", encoding="utf-8")
            write_json(product / "tasks" / work["id"] / "operator-brief.json", valid_operator_brief())
            self.assertEqual([], submit_task(product, work["id"]))
            submitted = json.loads((product / "tasks" / work["id"] / "work-order.json").read_text(encoding="utf-8"))
            self.assertEqual("ready_for_review", submitted["state"])

    def test_submitted_task_allows_router_owned_state_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 1)
            materialize_sections(product)
            work = create_task(product, "design_section", "P01", None, False)
            root = product / "03_sections" / "P01"
            evidence = json.loads((root / "evidence-pack.json").read_text(encoding="utf-8"))
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            claim_id = evidence["claims"][0]["id"]
            write_json(
                root / "story-plan.json",
                {
                    "schema_version": 2,
                    "section": "P01",
                    "status": "draft",
                    "governing_idea": "A durable mark preserves selected information without recording complete speech.",
                    "audience_question": "What can the mark preserve?",
                    "audience_payoff": "Selected information can persist on a durable object.",
                    "structure_shape": "A short object puzzle turns directly into one bounded capacity.",
                    "word_budget": {
                        "recommended": state["target_words"],
                        "rationale": "The range supports one puzzle, one turn and one payoff without repetition.",
                    },
                    "evidence_roles": {"narrated": [claim_id], "support": [], "guardrail": [], "omit": []},
                    "claim_use": {claim_id: "It proves the limited capacity revealed by the section."},
                    "beats": [
                        {"id": "B01", "function": "hook", "purpose": "Open on the object as an unresolved problem.", "audience_change": "The object becomes a question.", "claim_ids": [claim_id]},
                        {"id": "B02", "function": "tension", "purpose": "Ask what survives without complete speech.", "audience_change": "The audience sees the information gap.", "claim_ids": []},
                        {"id": "B03", "function": "payoff", "purpose": "Reveal the selected information that persists.", "audience_change": "The audience names the limited capacity.", "claim_ids": []},
                        {"id": "B04", "function": "bridge", "purpose": "Open the question of how that capacity formed.", "audience_change": "The answer creates the next question.", "claim_ids": []},
                    ],
                    "terminology": [],
                    "opening_move": "Begin close to one object and make its limitation visible.",
                    "ending_move": "Name the limited capacity and open its formation question.",
                    "comprehension_test": "The audience can explain the capacity in one sentence.",
                },
            )
            (product / "tasks" / work["id"] / "report.md").write_text("Diagnostic task report with completed contract details.\n", encoding="utf-8")
            write_json(product / "tasks" / work["id"] / "operator-brief.json", valid_operator_brief())
            self.assertEqual([], submit_task(product, work["id"]))
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertEqual("story_plan_review", state["status"])
            self.assertEqual([], verify_task(product, work["id"]))
            issues = validate_product(product)
            self.assertFalse(any("stale input" in issue.message for issue in issues))

    def test_operator_brief_is_short_while_report_can_remain_deep(self) -> None:
        document = valid_operator_brief()
        rendered = render_brief(document)
        self.assertEqual([], validate_brief(document))
        self.assertLessEqual(word_count(rendered), MAX_RENDERED_WORDS)
        self.assertIn("Cần bạn quyết định", rendered)
        self.assertNotIn("file", rendered.lower())

    def test_operator_brief_rejects_overload_and_ambiguous_review_state(self) -> None:
        overloaded = valid_operator_brief()
        overloaded["material_points"] = ["Điểm một.", "Điểm hai.", "Điểm ba.", "Điểm bốn."]
        self.assertTrue(any("more than 3" in item for item in validate_brief(overloaded)))
        ambiguous = valid_operator_brief()
        ambiguous["decision"] = {"required": False, "question": "", "recommendation": "", "options": []}
        ambiguous["next_step"] = "Tiếp tục khi phù hợp."
        self.assertTrue(any("explicit user decision" in item for item in validate_brief(ambiguous)))

        too_long = valid_operator_brief()
        dense = "Một nhận định quan trọng cần được cân nhắc kỹ trước khi người dùng đưa ra quyết định cuối cùng cho giai đoạn hiện tại."
        too_long["headline"] = dense
        too_long["material_points"] = [dense, dense, dense]
        too_long["decision"]["question"] = dense
        too_long["decision"]["recommendation"] = dense
        too_long["decision"]["options"] = [
            {"label": "Phương án", "effect": dense},
            {"label": "Phương án", "effect": dense},
        ]
        self.assertTrue(any("rendered operator brief exceeds" in item for item in validate_brief(too_long)))

    def test_operator_interface_supports_adaptive_depth(self) -> None:
        standard = (REPO_ROOT / "system" / "standards" / "operator-interface.md").read_text(encoding="utf-8")
        for mode in ["Brief mode", "Guided explanation mode", "Deep review mode", "Deliverable mode"]:
            self.assertIn(mode, standard)
        self.assertIn("không phải luôn nói ngắn", standard)

    def test_review_change_request_and_revision_stay_in_one_section(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 10)
            materialize_sections(product)
            make_approved_story_plan(product, "P06")
            root = product / "03_sections" / "P06"
            (root / "draft.md").write_text("Draft P06.", encoding="utf-8")
            (root / "handoff.md").write_text("Exit state P06.", encoding="utf-8")
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            state["status"] = "ready_for_review"
            write_json(root / "section.json", state)
            review_packet, review_context = compile_packet(product, "review_section", "T0001", section="P06")
            self.assertEqual(
                ["03_sections/P06/review.md", "tasks/T0001/report.md", "tasks/T0001/operator-brief.json"],
                review_packet["allowed_write_paths"],
            )
            self.assertNotIn("03_sections/P05/draft.md", review_context)
            request_changes(product, "P06", "Fix ISSUE-01 only; preserve the entry scene.")
            (root / "review.md").write_text("ISSUE-01: causal link is unsupported.", encoding="utf-8")
            revision_packet, revision_context = compile_packet(product, "revise_section", "T0002", section="P06")
            self.assertIn("Fix ISSUE-01 only", revision_context)
            self.assertNotIn("03_sections/P07", revision_context)
            self.assertIn("03_sections/P06/revision-log.md", revision_packet["allowed_write_paths"])
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            state["status"] = "ready_for_review"
            write_json(root / "section.json", state)
            approve_section(product, "P06")
            approved = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertTrue(approved["human_approved"])

    def test_context_budget_blocks_oversized_packet(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 1)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            (product / "02_outline" / "story-bible.md").write_text("x" * 70000, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exceeds budget"):
                compile_packet(product, "draft_section", "T0001", section="P01")

    def test_impact_traverses_section_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 10)
            result = calculate_impact(product, "CLM-0001", None)
            self.assertEqual(10, len(result["direct_sections"]))
            result = calculate_impact(product, None, "P06")
            self.assertEqual(["P06", "P07", "P08", "P09", "P10"], result["review_sections"])

    def test_assembly_requires_human_approval_and_keeps_sources_modular(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 2)
            materialize_sections(product)
            for section_id in ["P01", "P02"]:
                root = product / "03_sections" / section_id
                (root / "draft.md").write_text(f"Narration for {section_id}.", encoding="utf-8")
                state = json.loads((root / "section.json").read_text(encoding="utf-8"))
                state.update({"status": "approved", "human_approved": True})
                write_json(root / "section.json", state)
            result = assemble_product(product)
            self.assertIn("Narration for P01", result["script"])
            self.assertIn("Narration for P02", result["script"])
            self.assertIn("## Complete movement", result["script"])
            self.assertIn("<!-- production-unit: P01", result["script"])
            self.assertNotIn("## P01", result["script"])
            self.assertEqual(2, len(result["manifest"]["sections"]))
            self.assertTrue((product / "03_sections" / "P01" / "draft.md").is_file())


if __name__ == "__main__":
    unittest.main()
