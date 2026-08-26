from __future__ import annotations

import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts.assemble import assemble_product
from scripts.approval import (
    approve_plan,
    approve_section,
    approve_story_plan,
    human_amend_outline,
    human_amend_section,
    request_changes,
    request_story_plan_changes,
    start_new_cycle,
)
from scripts.context_packet import compile_packet
from scripts.draft_evidence import DraftEvidenceBroker
from scripts.consolidate_research import consolidate, verify_consolidation
from scripts.governance import classify_paths, commit_scope_errors, product_task_violations
from scripts.impact import calculate_impact
from scripts.materialize_research import materialize as materialize_research
from scripts.materialize_sections import archive_previous_cycle, materialize as materialize_sections
from scripts.new_product import DEFAULT_TEMPLATE_ROOT, create_product
from scripts.operator_brief import MAX_RENDERED_WORDS, render_brief, validate_brief
from scripts.outline_runtime import (
    DISABLED_DSH_ROWS,
    TESTED_DSH_VERSION,
    TOOL_DEFINITIONS,
    OutlineContextBroker,
    OutlineRuntimeError,
    build_dsh_patch,
    handle_mcp_message,
    run_dsh,
    verify_composed_dsh_config,
)
from scripts.outcome_eval_contract import GATE_END, GATE_START, HARD_GATES, STORY_DIMENSIONS, validate_outcome_review
from scripts.outline_contract import validate_outline_contract
from scripts.outline_evidence_pack import verify_outline_evidence_pack
from scripts.packet_contract import PACKET_COMPILER, PACKET_SCHEMA_VERSION, validate_packet_contract
from scripts.story_plan_contract import build_narration_pack, verify_narration_pack
from scripts.task import create_task, submit_task, validate_output_contract, verify_task
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
    section_ids = [f"P{number:02d}" for number in range(1, section_count + 1)]
    if section_count == 1:
        movement_sections = [section_ids, section_ids, section_ids]
    elif section_count == 2:
        movement_sections = [[section_ids[0]], section_ids, [section_ids[1]]]
    else:
        first_cut = max(1, section_count // 3)
        second_cut = max(first_cut + 1, (section_count * 2) // 3)
        second_cut = min(second_cut, section_count - 1)
        movement_sections = [section_ids[:first_cut], section_ids[first_cut:second_cut], section_ids[second_cut:]]

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
                "movement_ids": [f"M{index + 1:02d}" for index, members in enumerate(movement_sections) if section_id in members],
                "narrative_job": f"Move story state {number - 1} to {number}.",
                "entry_state": f"State {number - 1}",
                "exit_state": f"State {number}",
                "claim_ids": ["CLM-0001"],
                "dependencies": [f"P{number - 1:02d}"] if number > 1 else [],
                "anchor_options": ["Evidence-backed object."],
                "continuity_in": "Prior state.",
                "continuity_out": "Next state.",
                "non_goal": "Do not resolve work assigned to a later unit.",
                "target_words": {"min": minimum, "max": maximum},
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
            "schema_version": 4,
            "product": product.name,
            "cycle_id": json.loads((product / "product.json").read_text(encoding="utf-8"))["production_cycle"]["id"],
            "status": "approved",
            "section_count": section_count,
            "script_architecture": {
                "central_question": "How does the fixture system change from pressure to legacy?",
                "audience_promise": "Follow one complete causal transformation.",
                "design_rationale": "The whole arc is designed before bounded production work units are cut.",
                "total_word_envelope": {"min": total_min, "max": total_max},
                "acts": [
                    {
                        "id": "A01",
                        "order": 1,
                        "role": "opening",
                        "title": "Opening",
                        "narrative_job": "Establish the concrete tension and promise.",
                        "entry_state": "The causal problem is unresolved.",
                        "exit_state": "The audience knows what must be explained.",
                        "movement_ids": ["M01"],
                    },
                    {
                        "id": "A02",
                        "order": 2,
                        "role": "body",
                        "title": "Body",
                        "narrative_job": "Trace mechanism, expansion, conflict and adaptation.",
                        "entry_state": "The causal problem is defined.",
                        "exit_state": "The mechanism and consequences are understood.",
                        "movement_ids": ["M02"],
                    },
                    {
                        "id": "A03",
                        "order": 3,
                        "role": "ending",
                        "title": "Ending",
                        "narrative_job": "Answer the question and return to the opening tension.",
                        "entry_state": "The causal chain is visible.",
                        "exit_state": "The central question is resolved through legacy.",
                        "movement_ids": ["M03"],
                    },
                ],
                "movements": [
                    {
                        "id": f"M{index + 1:02d}",
                        "order": index + 1,
                        "act_id": f"A{index + 1:02d}",
                        "title": ["Concrete tension", "Causal development", "Resolution and legacy"][index],
                        "narrative_job": ["Open the causal problem.", "Explain the transformation.", "Resolve the question."][index],
                        "entry_state": ["Unresolved object.", "Defined problem.", "Visible consequence."][index],
                        "exit_state": ["Promised investigation.", "Visible consequence.", "Resolved legacy."][index],
                        "section_ids": members,
                    }
                    for index, members in enumerate(movement_sections)
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
            "schema_version": 3,
            "section": section,
            "status": "draft",
            "audience_shift": "The audience understands how a small record changes what can persist beyond one encounter.",
            "story_strategy": "Use the evidence-backed object as an anchor, then choose the clearest route from its immediate function to the section's assigned state change.",
            "word_budget": {
                "recommended": state["target_words"],
                "rationale": "The range matches one object, one explanatory turn and one concrete payoff without padding.",
            },
            "evidence_roles": {
                "core": claim_ids[:1],
                "optional": [],
                "guardrail": [],
                "exclude": claim_ids[1:],
            },
            "design_risks": [],
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


def valid_outcome_review(verdict: str = "pass") -> str:
    hard = {
        name: {
            "status": "pass",
            "basis": "The submitted draft provides a concrete observable basis for this gate judgment.",
        }
        for name in HARD_GATES
    }
    dimensions = {
        name: {
            "score": 8,
            "evidence_scope": "limited" if name == "supported_human_work_orientation" else "full",
            "basis": "The draft uses the available evidence effectively without inventing unsupported narrative detail.",
        }
        for name in STORY_DIMENSIONS
    }
    if verdict == "changes_requested":
        dimensions["causal_clarity"]["score"] = 7
    elif verdict == "blocked":
        hard["evidence_integrity"]["status"] = "blocked"
    gate = json.dumps(
        {"schema_version": 1, "hard_gates": hard, "dimensions": dimensions},
        ensure_ascii=False,
        indent=2,
    )
    return (
        "# Outcome Evaluation — P01\n\n"
        f"Verdict: {verdict}\n\n"
        "## Outcome judgment\n\n"
        "The section advances its assigned act, creates a visible change in understanding and remains clear when spoken aloud. "
        "Its causal relation is understandable without forcing the listener through the source order.\n\n"
        "## Mission answerability\n\n"
        "Yes. A listener can answer the assigned mission in their own words after one attentive hearing.\n\n"
        "## Historical progression\n\n"
        "Yes. A listener can retell the historical progression that leads to the section answer.\n\n"
        "## Production gate\n\n"
        f"{GATE_START}\n{gate}\n{GATE_END}\n\n"
        "## Issues\n\n"
        "No material issue remains. The evidence ceiling, semantic economy and product voice are intact in the current draft.\n\n"
        "## Routing\n\n"
        "Pass to human review. No prose, local design, product architecture or evidence intervention is required.\n"
    )


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


def make_dsh_outline_task(root: Path) -> tuple[Path, dict]:
    product = create_product(root / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
    make_approved_outline(product, 3)
    start_new_cycle(product, "Rebuild the complete outline through the bounded runtime POC.")
    (product / "01_research" / "research-synthesis.md").write_text(
        "# Research Synthesis\n\nStatus: complete\n\nA bounded causal synthesis for the fixture.\n",
        encoding="utf-8",
    )
    work = create_task(product, "outline", None, None, False, "dsh")
    return product, work


def valid_dsh_composed_config() -> str:
    rows = []
    for row_id in DISABLED_DSH_ROWS:
        rows.extend([f"- id: {row_id}", "  disabled: true"])
    rows.extend(
        [
            "- id: yt-outline-runtime-mcp",
            "  name: '@deepseek-ai/dsh-mcp-client'",
            "  config:",
            "    serverName: yt_outline",
        ]
    )
    return "\n".join(rows) + "\n"


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
                allowed + ["system/harness.json", "scripts/materialize_research.py"],
            )
            self.assertEqual(2, len(violations))
            self.assertTrue(all("protected system path" in item for item in violations))

    def test_system_and_product_changes_must_use_separate_commits(self) -> None:
        self.assertEqual([], commit_scope_errors(["system/harness.json", "scripts/task.py"]))
        self.assertEqual([], commit_scope_errors(["products/sumer-writing/01_research/plan.json"]))
        errors = commit_scope_errors(["system/harness.json", "products/sumer-writing/01_research/plan.json"])
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
            self.assertNotIn("acceptance_criteria", packet)
            self.assertNotIn("acceptance_criteria", work)
            context_path = product / work["context_packet"]
            context = context_path.read_text(encoding="utf-8")
            self.assertNotIn("## Acceptance criteria", context)
            self.assertNotIn("## Local autonomy", context)
            legacy = dict(packet)
            legacy["schema_version"] = 3
            legacy["acceptance_criteria"] = ["Legacy generated criterion."]
            self.assertEqual([], validate_packet_contract(legacy, context_path))

    def test_dsh_outline_uses_minimal_seed_and_preserves_legacy_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product, work = make_dsh_outline_task(Path(temp))
            packet = json.loads((product / work["packet_manifest"]).read_text(encoding="utf-8"))
            seed = (product / work["context_packet"]).read_text(encoding="utf-8")
            self.assertEqual("dsh", packet["execution_runtime"]["kind"])
            self.assertEqual(0, packet["input_tokens"])
            self.assertIn("get_task_state", seed)
            self.assertIn("search_evidence", seed)
            self.assertNotIn("Supported fixture claim.", seed)
            self.assertNotIn("# BEGIN INPUT:", seed)
            self.assertEqual(
                ["02_outline/outline.json", "02_outline/story-bible.md", "02_outline/voice-profile.md"],
                packet["operation_outputs"],
            )
            self.assertTrue(set(packet["runtime_owned_paths"]).isdisjoint(packet["allowed_write_paths"]))
            self.assertEqual([], validate_packet_contract(packet, product / work["context_packet"]))

            default_packet, default_context = compile_packet(product, "outline", "T9998-outline-outline")
            legacy_packet, legacy_context = compile_packet(product, "outline", "T9998-outline-outline", execution_runtime="legacy")
            self.assertEqual(default_context, legacy_context)
            self.assertNotIn("execution_runtime", default_packet)
            self.assertIn("Supported fixture claim.", legacy_context)
            with self.assertRaisesRegex(ValueError, "does not support execution runtime"):
                compile_packet(product, "research_plan", "T9999-research-plan", execution_runtime="dsh")

    def test_dsh_outline_broker_enforces_read_write_scope_and_audits_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product, work = make_dsh_outline_task(Path(temp))
            broker = OutlineContextBroker(product, work["id"])
            claims = broker.call("get_claims", {"limit": 1})
            self.assertEqual(["CLM-0001"], [item["id"] for item in claims["claims"]])
            search = broker.call("search_evidence", {"query": "fixture", "limit": 5})
            self.assertEqual("CLM-0001", search["claims"][0]["id"])

            escaped = product / "system" / "harness.json"
            with self.assertRaisesRegex(OutlineRuntimeError, "outside model scope"):
                broker.call("write_outputs", {"files": [{"path": "system/harness.json", "content": "{}\n"}]})
            self.assertFalse(escaped.exists())
            with self.assertRaisesRegex(OutlineRuntimeError, "outside model scope"):
                broker.call(
                    "write_outputs",
                    {
                        "files": [
                            {
                                "path": f"tasks/{work['id']}/runtime-trace.jsonl",
                                "content": "model-owned trace replacement\n",
                            }
                        ]
                    },
                )

            trace_path = product / "tasks" / work["id"] / "runtime-trace.jsonl"
            entries = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
            claim_entry = next(item for item in entries if item["capability"] == "get_claims")
            self.assertEqual("01_research/outline-evidence-pack.json", claim_entry["sources"][0]["path"])
            self.assertEqual(claims, claim_entry["response"])
            self.assertTrue(claim_entry["response_sha256"])
            self.assertTrue(any(item["error"] for item in entries if item["capability"] == "write_outputs"))

            synthesis = product / "01_research" / "research-synthesis.md"
            synthesis.write_text(synthesis.read_text(encoding="utf-8") + "Changed after task creation.\n", encoding="utf-8")
            with self.assertRaisesRegex(OutlineRuntimeError, "stale"):
                broker.call("get_research_summary", {})

    def test_dsh_patch_removes_general_tools_and_exposes_exact_capability_interface(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product, work = make_dsh_outline_task(Path(temp))
            runtime_dir = Path(temp) / "empty-runtime"
            runtime_dir.mkdir()
            patch_text = build_dsh_patch(product, work["id"], runtime_dir)
            for row_id in DISABLED_DSH_ROWS:
                self.assertIn(f"- id: {row_id}\n  disabled: true", patch_text)
            self.assertEqual(1, patch_text.count("@deepseek-ai/dsh-mcp-client"))
            self.assertIn("serverName: yt_outline", patch_text)
            composed = valid_dsh_composed_config()
            self.assertEqual([], verify_composed_dsh_config(composed))
            unsafe = composed.replace("- id: tool-fs\n  disabled: true", "- id: tool-fs")
            self.assertTrue(any("tool-fs" in item for item in verify_composed_dsh_config(unsafe)))
            tool_names = [item["name"] for item in TOOL_DEFINITIONS]
            packet = json.loads((product / work["packet_manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(packet["execution_runtime"]["capabilities"], tool_names)
            self.assertEqual(len(tool_names), len(set(tool_names)))

            broker = OutlineContextBroker(product, work["id"])
            initialized = handle_mcp_message(
                broker,
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
            )
            self.assertEqual("2025-06-18", initialized["result"]["protocolVersion"])
            listed = handle_mcp_message(broker, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
            self.assertEqual(tool_names, [item["name"] for item in listed["result"]["tools"]])
            called = handle_mcp_message(
                broker,
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_task_state", "arguments": {}}},
            )
            state = json.loads(called["result"]["content"][0]["text"])
            self.assertEqual(work["id"], state["task"]["id"])

            tampered = dict(packet)
            tampered["runtime_owned_paths"] = ["../outside.json"]
            errors = validate_packet_contract(tampered, product / work["context_packet"])
            self.assertTrue(any("runtime_owned_paths" in item for item in errors))

    def test_dsh_runner_uses_isolated_workspace_and_fails_closed_without_submit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product, work = make_dsh_outline_task(Path(temp))
            calls = [
                subprocess.CompletedProcess(
                    ["/mock/dsh", "--version"], 0, stdout=f"dsh {TESTED_DSH_VERSION}\n", stderr=""
                ),
                subprocess.CompletedProcess(
                    ["/mock/dsh", "--dump-config"], 0, stdout=valid_dsh_composed_config(), stderr=""
                ),
                subprocess.CompletedProcess(["/mock/dsh"], 0, stdout="Finished without submit.\n", stderr=""),
            ]
            with patch("scripts.outline_runtime.resolve_executable", return_value="/mock/dsh"), patch(
                "scripts.outline_runtime.subprocess.run", side_effect=calls
            ) as mocked_run:
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    code = run_dsh(product, work["id"], executable="dsh", timeout_seconds=30)
            self.assertEqual(2, code)
            run_call = mocked_run.call_args_list[2]
            command = run_call.args[0]
            self.assertEqual(["/mock/dsh", "--profile", "headless", "--patch"], command[:4])
            self.assertNotEqual(product.resolve(), Path(run_call.kwargs["cwd"]).resolve())
            self.assertEqual("1", run_call.kwargs["env"]["DSH_TELEMETRY_DISABLED"])
            self.assertEqual("read-only", run_call.kwargs["env"]["DSH_PERMISSION_MODE"])
            record = json.loads(
                (product / "tasks" / work["id"] / "runtime-run.json").read_text(encoding="utf-8")
            )
            self.assertEqual(2, record["return_code"])
            self.assertEqual("ready", record["task_state"])
            self.assertEqual("isolated-empty-directory", record["workspace_mode"])
            self.assertIn("yt-outline-runtime-mcp", record["patch"])

    def test_policy_has_one_authoritative_home(self) -> None:
        registry = json.loads((REPO_ROOT / "system" / "operations" / "registry.json").read_text(encoding="utf-8"))
        for name, spec in registry["operations"].items():
            self.assertNotIn("acceptance", spec, name)
            for required in ["target_kind", "max_context_tokens", "instruction_files", "required_inputs", "outputs", "context_profile"]:
                self.assertIn(required, spec, f"{name}.{required}")
        harness = json.loads((REPO_ROOT / "system" / "harness.json").read_text(encoding="utf-8"))
        self.assertTrue(all("autonomy" not in profile for profile in harness["profiles"].values()))
        self.assertFalse((REPO_ROOT / "system" / "core" / "invariants.md").exists())
        self.assertFalse((REPO_ROOT / "system" / "standards" / "review.md").exists())

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
            self.assertNotIn("system/standards/operator-interface.md", packet["instruction_files"])
            self.assertEqual("research", packet["context_profile"])
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
            self.assertNotIn("Operator Interface Standard", context)
            self.assertEqual("creative_draft", packet["context_profile"])
            self.assertLessEqual(packet["prompt_instruction_tokens"], 1500)
            self.assertLess(packet["estimated_context_tokens"], packet["max_context_tokens"])

    def test_outline_contract_materializes_global_acts_without_section_formula(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            outline = json.loads((product / "02_outline" / "outline.json").read_text(encoding="utf-8"))
            outline["sections"][0]["anchor_options"] = ["Object one.", "Object two."]
            write_json(product / "02_outline" / "outline.json", outline)
            materialize_sections(product)
            brief = (product / "03_sections" / "P01" / "brief.md").read_text(encoding="utf-8")
            body_brief = (product / "03_sections" / "P02" / "brief.md").read_text(encoding="utf-8")
            ending_brief = (product / "03_sections" / "P03" / "brief.md").read_text(encoding="utf-8")
            self.assertIn("## Whole-script acts", brief)
            self.assertIn("opening — Opening", brief)
            self.assertIn("body — Body", body_brief)
            self.assertIn("ending — Ending", ending_brief)
            self.assertNotIn("## Question", brief)
            self.assertNotIn("## Planned shape", brief)
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
            self.assertTrue(any("contiguous" in item for item in errors))

    def test_legacy_approved_artifacts_remain_readable_but_cannot_be_new_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))
            outline["schema_version"] = 3
            outline["script_architecture"].pop("acts")
            outline["script_architecture"].pop("central_question")
            outline["script_architecture"]["movements"] = [
                {
                    "id": "M01",
                    "order": 1,
                    "title": "Legacy movement",
                    "narrative_job": "Carry the legacy section.",
                    "entry_state": "Legacy entry.",
                    "exit_state": "Legacy exit.",
                    "section_ids": [item["id"] for item in outline["sections"]],
                }
            ]
            for item in outline["sections"]:
                item.pop("movement_ids")
                item.update(
                    {
                        "movement_id": "M01",
                        "structural_role": "Legacy transition.",
                        "question": "What changes?",
                        "payoff": "The state changes.",
                        "budget_rationale": "Legacy allocation.",
                        "planned_moves": ["Legacy move."],
                        "boundary": "Legacy boundary.",
                    }
                )
            write_json(outline_path, outline)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            root = product / "03_sections" / "P01"
            plan = json.loads((root / "story-plan.json").read_text(encoding="utf-8"))
            plan = {
                "schema_version": 2,
                "section": "P01",
                "status": "approved",
                "governing_idea": "A legacy record changes what persists.",
                "audience_question": "What persists?",
                "audience_payoff": "Selected information persists.",
                "structure_shape": "Legacy approved object turn.",
                "word_budget": {"recommended": {"min": 550, "max": 850}, "rationale": "Legacy range."},
                "evidence_roles": {"narrated": ["CLM-0001"], "support": [], "guardrail": [], "omit": []},
                "claim_use": {"CLM-0001": "Legacy use."},
                "beats": [],
                "terminology": [],
                "opening_move": "Legacy opening.",
                "ending_move": "Legacy ending.",
                "comprehension_test": "Legacy test.",
            }
            write_json(root / "story-plan.json", plan)
            build_narration_pack(product, "P01")
            target = json.loads((product / "product.json").read_text(encoding="utf-8"))["target"]
            self.assertEqual([], validate_outline_contract(outline, {"CLM-0001"}, target))
            self.assertEqual([], verify_narration_pack(product, "P01"))
            errors = validate_outline_contract(outline, {"CLM-0001"}, target, require_current=True)
            self.assertTrue(any("new or revised output" in item for item in errors))

    def test_story_design_resizes_without_prescribing_beats(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            product_state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            product_state["target"] = {"duration_minutes": {"min": 15, "max": 25}, "narration_wpm": 100}
            write_json(product / "product.json", product_state)
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))
            outline["script_architecture"]["total_word_envelope"] = {"min": 1500, "max": 2500}
            write_json(outline_path, outline)
            materialize_sections(product)
            root = product / "03_sections" / "P01"
            evidence = json.loads((root / "evidence-pack.json").read_text(encoding="utf-8"))
            claim_id = evidence["claims"][0]["id"]
            write_json(
                root / "story-plan.json",
                {
                    "schema_version": 3,
                    "section": "P01",
                    "status": "draft",
                    "audience_shift": "The audience sees that one bounded object changes what can survive.",
                    "story_strategy": "Stay close to the object until its limited capacity becomes clear; leave ordering and cadence to the writer.",
                    "word_budget": {
                        "recommended": {"min": 350, "max": 600},
                        "rationale": "One object and one reversal need less space than the outline first estimated.",
                    },
                    "evidence_roles": {"core": [claim_id], "optional": [], "guardrail": [], "exclude": []},
                    "design_risks": [],
                },
            )
            approve_story_plan(product, "P01")
            section_state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            revised_outline = json.loads(outline_path.read_text(encoding="utf-8"))
            self.assertEqual({"min": 350, "max": 600}, section_state["target_words"])
            self.assertEqual({"min": 350, "max": 600}, revised_outline["sections"][0]["target_words"])
            self.assertEqual(1, len(revised_outline["script_architecture"]["budget_revisions"]))
            self.assertNotIn("beats", json.loads((root / "story-plan.json").read_text(encoding="utf-8")))

    def test_story_design_is_required_before_drafting(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            with self.assertRaisesRegex(ValueError, "does not allow draft_section"):
                compile_packet(product, "draft_section", "T0001", section="P01")
            packet, context = compile_packet(product, "design_section", "T0002", section="P01")
            self.assertIn("03_sections/P01/evidence-pack.json", context)
            self.assertIn("system/standards/channel-constitution.md", packet["instruction_files"])
            self.assertNotIn("system/standards/voice.md", packet["instruction_files"])
            self.assertEqual(["03_sections/P01/story-plan.json"], packet["operation_outputs"])
            make_approved_story_plan(product, "P01")
            draft_packet, draft_context = compile_packet(product, "draft_section", "T0003", section="P01")
            self.assertIn("03_sections/P01/narration-pack.json", draft_context)
            self.assertNotIn("# BEGIN INPUT: 03_sections/P01/evidence-pack.json", draft_context)
            self.assertEqual("draft_section", draft_packet["operation"])

    def test_creative_packet_separates_hard_soft_and_evaluation_layers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            packet, context = compile_packet(product, "draft_section", "T0001", section="P01")
            self.assertEqual("creative_draft", packet["context_profile"])
            self.assertEqual("review_section_or_human_amendment", packet["evaluation_gate"])
            self.assertIn("system/core/creative-boundaries.md", packet["instruction_files"])
            self.assertIn("system/standards/channel-constitution.md", packet["instruction_files"])
            for excluded in [
                "system/standards/operator-interface.md",
                "system/standards/outcome-evaluation.md",
            ]:
                self.assertNotIn(excluded, packet["instruction_files"])
            self.assertNotIn("Operator Interface Standard", context)
            self.assertLessEqual(packet["prompt_instruction_tokens"], 1500)
            self.assertLess(packet["estimated_context_tokens"], 9000)
            narration_pack = json.loads(
                (product / "03_sections" / "P01" / "narration-pack.json").read_text(encoding="utf-8")
            )
            self.assertEqual(2, narration_pack["schema_version"])
            self.assertNotIn("claim_use", narration_pack)
            self.assertNotIn("narrated_claims", narration_pack)
            self.assertTrue(all("authority" not in item and "limitations" not in item for item in narration_pack["source_refs"]))

    def test_length_estimate_does_not_force_padding(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            work = create_task(product, "draft_section", "P01", None, False)
            root = product / "03_sections" / "P01"
            (root / "draft.md").write_text("# P01\n\nA concise factual turn.\n", encoding="utf-8")
            (root / "handoff.md").write_text("The intended state change is complete.\n", encoding="utf-8")
            (product / "tasks" / work["id"] / "report.md").write_text(
                "The material reached its intended shift below the planning estimate without repetition.\n",
                encoding="utf-8",
            )
            write_json(product / "tasks" / work["id"] / "operator-brief.json", valid_operator_brief())
            DraftEvidenceBroker(product, work["id"]).call("resolve_claims")
            self.assertEqual([], submit_task(product, work["id"]))

    def test_production_unit_hard_cap_remains_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            work = create_task(product, "draft_section", "P01", None, False)
            root = product / "03_sections" / "P01"
            (root / "draft.md").write_text(("word " * 3001).strip() + "\n", encoding="utf-8")
            (root / "handoff.md").write_text("State.\n", encoding="utf-8")
            errors = validate_output_contract(product, work)
            self.assertTrue(any("hard cap" in item for item in errors))

    def test_outcome_evaluation_is_required_before_section_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            root = product / "03_sections" / "P01"
            (root / "draft.md").write_text("A draft with an evidenced state change.\n", encoding="utf-8")
            (root / "handoff.md").write_text("State changed.\n", encoding="utf-8")
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            state["status"] = "ready_for_review"
            write_json(root / "section.json", state)
            with self.assertRaisesRegex(ValueError, "completed outcome review"):
                approve_section(product, "P01")
            (root / "review.md").write_text(valid_outcome_review("changes_requested"), encoding="utf-8")
            state["status"] = "review_complete"
            write_json(root / "section.json", state)
            with self.assertRaisesRegex(ValueError, "has not passed"):
                approve_section(product, "P01")
            review = valid_outcome_review("pass")
            self.assertEqual([], validate_outcome_review(review))
            (root / "review.md").write_text(review, encoding="utf-8")
            approve_section(product, "P01")
            approved = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertTrue(approved["human_approved"])

    def test_new_cycle_reopens_whole_product_architecture(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            cycle_id = start_new_cycle(
                product,
                "Rebuild the complete three-act arc under the lean hard-boundary/soft-logic harness.",
            )
            self.assertEqual("C002", cycle_id)
            state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            outline = json.loads((product / "02_outline" / "outline.json").read_text(encoding="utf-8"))
            self.assertEqual("outline_design", state["production_cycle"]["status"])
            self.assertEqual("changes_requested", state["stages"]["outline"])
            self.assertEqual("paused", state["stages"]["sections"])
            self.assertEqual("draft", outline["status"])
            self.assertEqual("C002", outline["cycle_id"])
            request = (product / "02_outline" / "outline-change-request.md").read_text(encoding="utf-8")
            self.assertIn("hard-boundary/soft-logic", request)
            (product / "01_research" / "research-synthesis.md").write_text(
                "# Research Synthesis\n\nStatus: complete\n",
                encoding="utf-8",
            )
            work = create_task(product, "outline", None, None, False)
            context = (product / work["context_packet"]).read_text(encoding="utf-8")
            self.assertIn("Outline Change Request — C002", context)
            self.assertIn('"id": "C002"', context)
            with self.assertRaisesRegex(ValueError, "approved outline"):
                start_new_cycle(product, "Do it again.")

    def test_outline_packet_compacts_legacy_approved_research(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            state["stages"]["research"] = "approved"
            write_json(product / "product.json", state)
            (product / "01_research" / "research-synthesis.md").write_text(
                "# Research Synthesis\n\nStatus: ready_for_review\n\nA previously approved causal synthesis.\n",
                encoding="utf-8",
            )
            ledger_path = product / "01_research" / "claim-ledger.json"
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            base = ledger["claims"][0]
            ledger["claims"] = []
            for number in range(1, 72):
                claim = dict(base)
                claim["id"] = f"CLM-{number:04d}"
                claim["statement"] = f"Claim {number} gives the architecture a bounded, evidence-backed causal option."
                claim["provenance"] = [
                    {"workstream": "WS01", "local_id": f"WS01-CLM-{number:03d}", "notes": "x" * 240}
                ]
                claim["counterevidence"] = (
                    "A detailed research caveat that remains authoritative outside the creative prompt. " + "y" * 180
                )
                ledger["claims"].append(claim)
            write_json(ledger_path, ledger)

            packet, context = compile_packet(product, "outline", "T0001-outline-outline")
            input_paths = [item["path"] for item in packet["inputs"]]
            self.assertIn("01_research/outline-evidence-pack.json", input_paths)
            self.assertNotIn("01_research/claim-ledger.json", input_paths)
            self.assertIn("claim_ledger_sha256", context)
            self.assertNotIn('"provenance"', context)
            self.assertEqual([], verify_outline_evidence_pack(product))
            self.assertLess(packet["estimated_context_tokens"], packet["max_context_tokens"])

    def test_new_cycle_archives_old_sections_before_rematerialization(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            self.assertTrue((product / "03_sections" / "P01").is_dir())
            start_new_cycle(product, "Rebuild the full arc.")
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))
            outline["status"] = "approved"
            write_json(outline_path, outline)
            archived = archive_previous_cycle(product)
            self.assertEqual(3, len(archived))
            self.assertTrue((product / "03_sections" / "_history" / "C001" / "P01").is_dir())
            created = materialize_sections(product)
            self.assertTrue(created)
            current = json.loads((product / "03_sections" / "P01" / "section.json").read_text(encoding="utf-8"))
            self.assertEqual("C002", current["cycle_id"])

    def test_story_plan_feedback_creates_a_fresh_design_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
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
            make_approved_outline(product, 3)
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
            self.assertNotIn("DIAGNOSTIC_DRAFT_THAT_MUST_NOT_BE_EDITED", context)
            self.assertIn("The prose exposed a padded structure", context)
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
            make_approved_outline(product, 3)
            materialize_sections(product)
            with self.assertRaisesRegex(ValueError, "human-approved section: P01"):
                compile_packet(product, "integration_review", "T0001")
            for section_id in ["P01", "P02", "P03"]:
                root = product / "03_sections" / section_id
                (root / "handoff.md").write_text(f"Handoff {section_id}.", encoding="utf-8")
                state = json.loads((root / "section.json").read_text(encoding="utf-8"))
                state.update({"status": "approved", "human_approved": True})
                write_json(root / "section.json", state)
            packet, context = compile_packet(product, "integration_review", "T0002")
            self.assertIn("03_sections/P01/handoff.md", context)
            self.assertIn("03_sections/P02/handoff.md", context)
            self.assertIn("03_sections/P03/handoff.md", context)
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
            make_approved_outline(product, 3)
            materialize_sections(product)
            work = create_task(product, "design_section", "P01", None, False)
            root = product / "03_sections" / "P01"
            evidence = json.loads((root / "evidence-pack.json").read_text(encoding="utf-8"))
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            claim_id = evidence["claims"][0]["id"]
            write_json(
                root / "story-plan.json",
                {
                    "schema_version": 3,
                    "section": "P01",
                    "status": "draft",
                    "audience_shift": "The audience understands that selected information can persist on a durable object.",
                    "story_strategy": "Use the object as the factual anchor and let the writer choose the clearest route to its limited capacity.",
                    "word_budget": {
                        "recommended": state["target_words"],
                        "rationale": "The range supports one puzzle, one turn and one payoff without repetition.",
                    },
                    "evidence_roles": {"core": [claim_id], "optional": [], "guardrail": [], "exclude": []},
                    "design_risks": [],
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
            draft_work = create_task(product, "draft_section", "P06", None, False)
            DraftEvidenceBroker(product, draft_work["id"]).call("resolve_claims")
            (root / "draft.md").write_text("Draft P06.", encoding="utf-8")
            (root / "handoff.md").write_text("Exit state P06.", encoding="utf-8")
            (product / "tasks" / draft_work["id"] / "report.md").write_text("Draft ready.\n", encoding="utf-8")
            write_json(product / "tasks" / draft_work["id"] / "operator-brief.json", valid_operator_brief())
            self.assertEqual([], submit_task(product, draft_work["id"]))
            review_packet, review_context = compile_packet(product, "review_section", "T0001", section="P06")
            self.assertEqual(
                ["03_sections/P06/review.md", "tasks/T0001/report.md", "tasks/T0001/operator-brief.json"],
                review_packet["allowed_write_paths"],
            )
            self.assertNotIn("03_sections/P05/draft.md", review_context)
            self.assertEqual("none", review_packet["recorded_evidence_projection"]["recorded_evidence_state"])
            request_changes(product, "P06", "Fix ISSUE-01 only; preserve the entry scene.")
            (root / "review.md").write_text("ISSUE-01: causal link is unsupported.", encoding="utf-8")
            revision_packet, revision_context = compile_packet(product, "revise_section", "T0002", section="P06")
            self.assertIn("Fix ISSUE-01 only", revision_context)
            self.assertNotIn("03_sections/P07", revision_context)
            self.assertIn("03_sections/P06/revision-log.md", revision_packet["allowed_write_paths"])
            legacy_revision_inputs = [item["path"] for item in revision_packet["inputs"]]
            for preserved_path in [
                "02_outline/story-bible.md",
                "02_outline/voice-profile.md",
                "03_sections/P06/brief.md",
                "03_sections/P06/narration-pack.json",
                "03_sections/P06/draft.md",
                "03_sections/P06/handoff.md",
                "03_sections/P06/review.md",
                "03_sections/P06/change-request.md",
                "03_sections/P06/story-plan.json",
            ]:
                self.assertIn(preserved_path, legacy_revision_inputs)
            (root / "review.md").write_text(valid_outcome_review("pass"), encoding="utf-8")
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            state["status"] = "review_complete"
            write_json(root / "section.json", state)
            approve_section(product, "P06")
            approved = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertTrue(approved["human_approved"])

    def test_human_outline_amendment_bypasses_task_lifecycle_and_marks_downstream_sync(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            voice_body = (
                "Evidence leads the narration while uncertainty stays visible and causal language remains bounded. " * 4
            )
            (product / "02_outline" / "voice-profile.md").write_text(
                "Status: approved\n\n"
                + "\n\n".join(
                    f"{heading}\n\n{voice_body}"
                    for heading in [
                        "## Product voice",
                        "## Borrowed functions",
                        "## Original expression",
                        "## Prohibited imitation",
                        "## Draft tests",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            work = create_task(product, "design_section", "P01", None, False)
            outline_path = product / "02_outline" / "outline.json"
            outline = json.loads(outline_path.read_text(encoding="utf-8"))
            outline["sections"][0]["narrative_job"] = "Human-approved direct architecture correction."
            write_json(outline_path, outline)

            record = human_amend_outline(
                product,
                "Apply the user's architecture correction directly; do not create another outline task.",
                ["outline.json"],
            )

            active = json.loads((product / "tasks" / "ACTIVE.json").read_text(encoding="utf-8"))
            work_state = json.loads((product / "tasks" / work["id"] / "work-order.json").read_text(encoding="utf-8"))
            section_state = json.loads((product / "03_sections" / "P01" / "section.json").read_text(encoding="utf-8"))
            product_state = json.loads((product / "product.json").read_text(encoding="utf-8"))
            self.assertIsNone(active["task_id"])
            self.assertEqual("cancelled", work_state["state"])
            self.assertEqual(record["id"], work_state["superseded_by"])
            self.assertEqual("outline_amended", section_state["status"])
            self.assertEqual("human_sync_required", product_state["stages"]["sections"])
            self.assertEqual([], [issue for issue in validate_product(product) if issue.level == "ERROR"])
            log = (product / "human-amendments.jsonl").read_text(encoding="utf-8")
            self.assertIn(record["id"], log)
            self.assertIn("02_outline/outline.json", log)

    def test_human_story_plan_edit_builds_evidence_handoff_without_design_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            root = product / "03_sections" / "P01"
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            evidence = json.loads((root / "evidence-pack.json").read_text(encoding="utf-8"))
            claim_ids = [item["id"] for item in evidence["claims"]]
            write_json(
                root / "story-plan.json",
                {
                    "schema_version": 3,
                    "section": "P01",
                    "status": "draft",
                    "audience_shift": "The audience understands the human-approved state change.",
                    "story_strategy": "Use the selected evidence directly and keep the causal turn compact.",
                    "word_budget": {
                        "recommended": state["target_words"],
                        "rationale": "The existing range fits the bounded narrative load.",
                    },
                    "evidence_roles": {"core": claim_ids, "optional": [], "guardrail": [], "exclude": []},
                    "design_risks": [],
                },
            )

            human_amend_section(
                product,
                "P01",
                "Accept the user's direct story-plan edit.",
                ["story-plan.json"],
            )

            plan = json.loads((root / "story-plan.json").read_text(encoding="utf-8"))
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertEqual("approved", plan["status"])
            self.assertEqual("ready_for_draft", state["status"])
            self.assertTrue((root / "narration-pack.json").is_file())
            self.assertFalse((product / "tasks" / "ACTIVE.json").is_file())

    def test_human_prose_edit_can_be_approved_without_review_task_but_keeps_hard_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            root = product / "03_sections" / "P01"
            work = create_task(product, "draft_section", "P01", None, False)
            (root / "draft.md").write_text("# P01\n\nHuman-edited narration with a bounded factual turn.\n", encoding="utf-8")
            (root / "handoff.md").write_text("The approved state change is complete.\n", encoding="utf-8")
            before_tasks = sorted((product / "tasks").glob("T*")) if (product / "tasks").is_dir() else []

            record = human_amend_section(
                product,
                "P01",
                "Accept the user's direct prose correction as the reviewed output.",
                ["draft.md"],
            )

            after_tasks = sorted((product / "tasks").glob("T*")) if (product / "tasks").is_dir() else []
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertEqual(before_tasks, after_tasks)
            self.assertEqual("approved", state["status"])
            self.assertTrue(state["human_approved"])
            self.assertEqual("human_direct_edit", state["approval_basis"])
            self.assertEqual(record["id"], state["last_human_amendment"])
            active = json.loads((product / "tasks" / "ACTIVE.json").read_text(encoding="utf-8"))
            work_state = json.loads((product / "tasks" / work["id"] / "work-order.json").read_text(encoding="utf-8"))
            self.assertIsNone(active["task_id"])
            self.assertEqual("cancelled", work_state["state"])
            self.assertEqual(record["id"], work_state["superseded_by"])
            with self.assertRaisesRegex(ValueError, "outside the allowed output scope"):
                human_amend_section(product, "P01", "Do not widen scope.", ["review.md"])

            (root / "draft.md").write_text(("word " * 3001).strip() + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hard cap"):
                human_amend_section(product, "P01", "This must still fail validation.", ["draft.md"])

    def test_context_budget_blocks_oversized_packet(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
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
            make_approved_outline(product, 3)
            materialize_sections(product)
            for section_id in ["P01", "P02", "P03"]:
                root = product / "03_sections" / section_id
                (root / "draft.md").write_text(f"Narration for {section_id}.", encoding="utf-8")
                state = json.loads((root / "section.json").read_text(encoding="utf-8"))
                state.update({"status": "approved", "human_approved": True})
                write_json(root / "section.json", state)
            result = assemble_product(product)
            self.assertIn("Narration for P01", result["script"])
            self.assertIn("Narration for P02", result["script"])
            self.assertIn("Narration for P03", result["script"])
            self.assertIn("## Opening", result["script"])
            self.assertIn("## Body", result["script"])
            self.assertIn("## Ending", result["script"])
            self.assertIn("<!-- production-unit: P01", result["script"])
            self.assertNotIn("## P01", result["script"])
            self.assertEqual(3, len(result["manifest"]["sections"]))
            self.assertTrue((product / "03_sections" / "P01" / "draft.md").is_file())

    def test_human_approval_closes_design_task_and_routes_draft_immediately(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            design = create_task(product, "design_section", "P01", None, False)

            make_approved_story_plan(product, "P01")

            persisted = json.loads(
                (product / "tasks" / design["id"] / "work-order.json").read_text(encoding="utf-8")
            )
            active = json.loads((product / "tasks" / "ACTIVE.json").read_text(encoding="utf-8"))
            self.assertEqual("closed", persisted["state"])
            self.assertIsNone(active["task_id"])
            draft = create_task(product, "draft_section", "P01", None, False)
            self.assertEqual("ready", draft["state"])

    def test_submitted_task_left_in_active_is_self_healed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            state_path = product / "product.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["stages"]["direction"] = "approved"
            write_json(state_path, state)
            first = create_task(product, "research_plan", None, None, False)
            work_path = product / "tasks" / first["id"] / "work-order.json"
            work = json.loads(work_path.read_text(encoding="utf-8"))
            work["state"] = "ready_for_review"
            write_json(work_path, work)

            second = create_task(product, "research_plan", None, None, False)

            active = json.loads((product / "tasks" / "ACTIVE.json").read_text(encoding="utf-8"))
            self.assertEqual(second["id"], active["task_id"])

    def test_terminal_task_left_in_active_does_not_block(self) -> None:
        for terminal_state in ["closed", "cancelled"]:
            with self.subTest(terminal_state=terminal_state), tempfile.TemporaryDirectory() as temp:
                product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
                state_path = product / "product.json"
                state = json.loads(state_path.read_text(encoding="utf-8"))
                state["stages"]["direction"] = "approved"
                write_json(state_path, state)
                first = create_task(product, "research_plan", None, None, False)
                work_path = product / "tasks" / first["id"] / "work-order.json"
                work = json.loads(work_path.read_text(encoding="utf-8"))
                work["state"] = terminal_state
                write_json(work_path, work)

                second = create_task(product, "research_plan", None, None, False)

                self.assertNotEqual(first["id"], second["id"])

    def test_human_story_plan_amendment_supersedes_live_draft_and_allows_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            make_approved_outline(product, 3)
            materialize_sections(product)
            make_approved_story_plan(product, "P01")
            first = create_task(product, "draft_section", "P01", None, False)

            human_amend_section(
                product,
                "P01",
                "Accept the human story-plan adjustment and replace the routed draft task.",
                ["story-plan.json"],
            )

            persisted = json.loads(
                (product / "tasks" / first["id"] / "work-order.json").read_text(encoding="utf-8")
            )
            self.assertEqual("cancelled", persisted["state"])
            replacement = create_task(product, "draft_section", "P01", None, False)
            self.assertNotEqual(first["id"], replacement["id"])

    def test_genuine_live_scope_conflict_still_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = create_product(Path(temp) / "products", "demo", "Demo", DEFAULT_TEMPLATE_ROOT)
            state_path = product / "product.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["stages"]["direction"] = "approved"
            write_json(state_path, state)
            first = create_task(product, "research_plan", None, None, False)

            with self.assertRaisesRegex(ValueError, first["id"]):
                create_task(product, "research_plan", None, None, False)


if __name__ == "__main__":
    unittest.main()
