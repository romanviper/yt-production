from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.assemble import assemble_product
from scripts.approval import approve_plan, approve_section, request_changes
from scripts.context_packet import compile_packet
from scripts.consolidate_research import consolidate, verify_consolidation
from scripts.governance import classify_paths, commit_scope_errors, product_task_violations
from scripts.impact import calculate_impact
from scripts.materialize_research import materialize as materialize_research
from scripts.materialize_sections import materialize as materialize_sections
from scripts.new_product import DEFAULT_TEMPLATE_ROOT, create_product
from scripts.operator_brief import MAX_RENDERED_WORDS, render_brief, validate_brief
from scripts.packet_contract import PACKET_COMPILER, PACKET_SCHEMA_VERSION
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
        sections.append(
            {
                "id": section_id,
                "order": number,
                "title": f"Part {number}",
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
                "target_words": {"min": 700, "max": 1200},
            }
        )
    write_json(
        product / "02_outline" / "outline.json",
        {"schema_version": 2, "product": product.name, "status": "approved", "section_count": section_count, "sections": sections},
    )


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
            packet, context = compile_packet(product, "draft_section", "T0001", section="P06")
            self.assertIn("03_sections/P06/brief.md", context)
            self.assertIn("03_sections/P06/evidence-pack.json", context)
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

    def test_draft_packet_adds_only_approved_dependency_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
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
            self.assertEqual(2, len(result["manifest"]["sections"]))
            self.assertTrue((product / "03_sections" / "P01" / "draft.md").is_file())


if __name__ == "__main__":
    unittest.main()
