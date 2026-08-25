from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.approval import approve_section
from scripts.draft_evidence import DraftEvidenceBroker
from scripts.draft_lifecycle_contract import (
    validate_canonical_draft_lifecycle,
    validate_evidence_trace,
    validate_required_evidence_resolution,
)
from scripts.materialize_sections import materialize
from scripts.outcome_eval_contract import (
    GATE_END,
    GATE_START,
    HARD_GATES,
    STORY_DIMENSIONS,
    outcome_review_template,
    validate_outcome_review,
)
from scripts.task import create_task, submit_task
from scripts.validate import validate_product
from test_material_aware_handoff import make_direct_authorship_fixture, write_json


def valid_v3_pass_review(section: str) -> str:
    gate = {
        "schema_version": 1,
        "hard_gates": {
            name: {
                "status": "pass",
                "basis": "The submitted draft provides a specific observable basis for this gate.",
            }
            for name in HARD_GATES
        },
        "dimensions": {
            name: {
                "score": 8,
                "evidence_scope": "limited" if name == "supported_human_work_orientation" else "full",
                "basis": "The draft uses available evidence effectively without inventing unsupported detail.",
            }
            for name in STORY_DIMENSIONS
        },
    }
    return (
        f"# Outcome Evaluation — {section}\n\n"
        "Verdict: pass\n\n"
        "## Outcome judgment\n\nThe listener reaches the assigned answer without evidence overreach.\n\n"
        "## Mission answerability\n\nYes. The listener can state the mission answer in their own words.\n\n"
        "## Historical progression\n\nYes. The listener can retell the historical path to that answer.\n\n"
        "## Production gate\n\n"
        f"{GATE_START}\n{json.dumps(gate, ensure_ascii=False, indent=2)}\n{GATE_END}\n\n"
        "## Issues\n\nNo material issue remains in this fixture.\n\n"
        "## Routing\n\nPass to human review; no intervention is required.\n"
    )


def write_ready_task_admin(task_root: Path, headline: str) -> None:
    (task_root / "report.md").write_text(headline + "\n", encoding="utf-8")
    write_json(
        task_root / "operator-brief.json",
        {
            "schema_version": 1,
            "status": "ready_for_review",
            "headline": headline,
            "material_points": ["The task stayed within its routed contract."],
            "decision": {
                "required": True,
                "question": "Continue with human review?",
                "recommendation": "Inspect the routed result before approval.",
                "options": [{"label": "Review", "effect": "Inspect the completed task output."}],
            },
            "next_step": "",
        },
    )


class WriterLifecycleRegression(unittest.TestCase):
    def test_canonical_draft_requires_official_task_and_binds_submission_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            root = product / "03_sections" / "P01"
            state_path = root / "section.json"

            # A prose file appearing in the workspace is not canonical by existence alone.
            (root / "draft.md").write_text("# P01\n\nUnrouted draft.\n", encoding="utf-8")
            (root / "handoff.md").write_text("Unrouted handoff.\n", encoding="utf-8")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            lifecycle_errors = validate_canonical_draft_lifecycle(product, "P01", state)
            self.assertTrue(any("missing submitted task provenance" in item for item in lifecycle_errors))
            product_errors = [issue.message for issue in validate_product(product)]
            self.assertTrue(any("missing submitted task provenance" in item for item in product_errors))

            (root / "draft.md").unlink()
            (root / "handoff.md").unlink()

            # The routed task owns the prose paths while writing is in progress.
            work = create_task(product, "draft_section", "P01", None, False)
            task_id = work["id"]
            (root / "draft.md").write_text("# P01\n\nEvidence-safe routed draft.\n", encoding="utf-8")
            (root / "handoff.md").write_text("Mission reached without expanding evidence.\n", encoding="utf-8")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual([], validate_canonical_draft_lifecycle(product, "P01", state))

            # Whole-scope claim resolution is mandatory and audit-bound; deeper retrieval remains optional.
            broker = DraftEvidenceBroker(product, task_id)
            broker.call("scope")
            self.assertTrue(validate_required_evidence_resolution(product, task_id))
            broker.call("resolve_claims")
            self.assertEqual([], validate_evidence_trace(product, task_id))
            self.assertEqual([], validate_required_evidence_resolution(product, task_id))
            resolved = broker.call("resolve_claims")
            self.assertEqual(len(resolved["sources"]), len({item["id"] for item in resolved["sources"]}))
            self.assertLessEqual(resolved["telemetry"]["estimated_response_tokens"], 6000)

            task_dir = product / "tasks" / task_id
            (task_dir / "report.md").write_text("Draft completed inside the routed task scope.\n", encoding="utf-8")
            write_json(
                task_dir / "operator-brief.json",
                {
                    "schema_version": 1,
                    "status": "ready_for_review",
                    "headline": "P01 draft is ready for review.",
                    "material_points": ["The draft stayed inside the approved mission and evidence boundary."],
                    "decision": {
                        "required": True,
                        "question": "Review P01 now?",
                        "recommendation": "Review the draft before approval.",
                        "options": [
                            {"label": "Review", "effect": "Inspect the draft and request changes or continue."}
                        ],
                    },
                    "next_step": "",
                },
            )
            self.assertEqual([], submit_task(product, task_id))

            submitted = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual("ready_for_review", submitted["status"])
            self.assertEqual(task_id, submitted["prose_provenance"]["task_id"])
            self.assertEqual([], validate_canonical_draft_lifecycle(product, "P01", submitted))

            # Tampering with an audit trace after submission invalidates canonical provenance.
            trace_path = task_dir / "evidence-trace.jsonl"
            records = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
            records[0]["response_sha256"] = "0" * 64
            trace_path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in records) + "\n", encoding="utf-8")
            tampered = validate_canonical_draft_lifecycle(product, "P01", submitted)
            self.assertTrue(any("response hash is invalid" in item for item in tampered))

    def test_canonical_evaluator_requires_mission_answer_and_retellable_progression(self) -> None:
        conclusion_list = (
            "# Outcome Evaluation — P01\n\n"
            "Verdict: pass\n\n"
            "## Outcome judgment\n\n"
            "Every factual conclusion is supported and the section contains the correct claims, but this judgment only checks correctness and lists the conclusions that appeared.\n\n"
            "## Issues\n\n"
            "No factual error is recorded, and no truth-ceiling expansion is visible in the submitted prose.\n\n"
            "## Routing\n\n"
            "Pass to human review because the facts are accurate and all expected conclusions are present.\n"
        )
        errors = validate_outcome_review(conclusion_list, require_mission_outcomes=True)
        self.assertTrue(any("Mission answerability" in item for item in errors))
        self.assertTrue(any("Historical progression" in item for item in errors))

        gate = {
            "schema_version": 1,
            "hard_gates": {
                name: {
                    "status": "pass",
                    "basis": "The submitted draft provides a specific observable basis for this hard gate.",
                }
                for name in HARD_GATES
            },
            "dimensions": {
                name: {
                    "score": 8,
                    "evidence_scope": "limited" if name == "supported_human_work_orientation" else "full",
                    "basis": "The draft uses the available supported material effectively without inventing narrative detail.",
                }
                for name in STORY_DIMENSIONS
            },
        }
        outcome_review = (
            "# Outcome Evaluation — P01\n\n"
            "Verdict: pass\n\n"
            "## Outcome judgment\n\n"
            "The listener reaches the assigned answer without evidence overreach, and the section preserves continuity with the approved boundary.\n\n"
            "## Mission answerability\n\n"
            "Yes. After hearing the section, the listener can state the answer to the section mission in their own words and distinguish it from adjacent questions.\n\n"
            "## Historical progression\n\n"
            "Yes. The listener can retell the historical path that produced the answer rather than recalling only a list of conclusions.\n\n"
            "## Production gate\n\n"
            f"{GATE_START}\n{json.dumps(gate, ensure_ascii=False, indent=2)}\n{GATE_END}\n\n"
            "## Issues\n\n"
            "No material outcome, continuity or evidence issue remains in this fixture.\n\n"
            "## Routing\n\n"
            "Pass to human review; no prose, architecture or evidence intervention is required.\n"
        )
        self.assertEqual(
            [],
            validate_outcome_review(
                outcome_review,
                require_mission_outcomes=True,
                require_production_gate=True,
            ),
        )

        gate["dimensions"]["causal_clarity"]["score"] = 7
        false_pass = outcome_review.replace(
            json.dumps(json.loads(outcome_review.split(GATE_START, 1)[1].split(GATE_END, 1)[0]), ensure_ascii=False, indent=2),
            json.dumps(gate, ensure_ascii=False, indent=2),
        )
        errors = validate_outcome_review(
            false_pass,
            require_mission_outcomes=True,
            require_production_gate=True,
        )
        self.assertTrue(any("derived verdict is 'changes_requested'" in item for item in errors))

    def test_review_contract_v3_enforces_exact_document_grammar_without_changing_v2(self) -> None:
        canonical = outcome_review_template("P01")
        strict = {
            "require_mission_outcomes": True,
            "require_production_gate": True,
        }
        self.assertEqual(
            [],
            validate_outcome_review(
                canonical,
                **strict,
                contract_version=3,
                section="P01",
            ),
        )

        wrong_title = canonical.replace("# Outcome Evaluation — P01", "# Review of P01", 1)
        wrong_order = canonical.replace("## Mission answerability", "## SWAP", 1).replace(
            "## Historical progression", "## Mission answerability", 1
        ).replace("## SWAP", "## Historical progression", 1)
        no_gate_heading = canonical.replace("## Production gate\n\n", "", 1)
        duplicate_verdict = canonical.replace(
            "Verdict: changes_requested",
            "Verdict: changes_requested\nVerdict: pass",
            1,
        )
        extra_gate_key = canonical.replace(
            '"schema_version": 1,',
            '"schema_version": 1,\n  "unexpected": true,',
            1,
        )
        for label, invalid, expected in [
            ("title", wrong_title, "title must be exactly"),
            ("order", wrong_order, "exact canonical sequence"),
            ("production heading", no_gate_heading, "exact canonical sequence"),
            ("verdict", duplicate_verdict, "exactly one literal Verdict line"),
            ("gate keys", extra_gate_key, "exactly schema_version"),
        ]:
            with self.subTest(label=label):
                errors = validate_outcome_review(
                    invalid,
                    **strict,
                    contract_version=3,
                    section="P01",
                )
                self.assertTrue(any(expected in error for error in errors), errors)

        v2_compatible = no_gate_heading.replace("# Outcome Evaluation — P01", "# Legacy Review", 1)
        self.assertEqual(
            [],
            validate_outcome_review(
                v2_compatible,
                **strict,
                contract_version=2,
                section="P01",
            ),
        )

    def test_v3_review_submission_is_exact_and_post_submit_tamper_blocks_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            root = product / "03_sections" / "P01"

            draft_work = create_task(product, "draft_section", "P01", None, False)
            draft_broker = DraftEvidenceBroker(product, draft_work["id"])
            draft_broker.call("resolve_claims")
            (root / "draft.md").write_text("# P01\n\nA supported routed draft.\n", encoding="utf-8")
            (root / "handoff.md").write_text("The listener reaches State 1.\n", encoding="utf-8")
            write_ready_task_admin(product / "tasks" / draft_work["id"], "P01 draft is ready for review.")
            self.assertEqual([], submit_task(product, draft_work["id"]))

            review_work = create_task(product, "review_section", "P01", None, False)
            self.assertEqual(3, review_work["review_contract_version"])
            review_broker = DraftEvidenceBroker(product, review_work["id"])
            review_broker.call("resolve_claims")
            review_text = valid_v3_pass_review("P01")
            review_path = root / "review.md"
            review_path.write_text(review_text, encoding="utf-8")
            write_ready_task_admin(product / "tasks" / review_work["id"], "P01 review passes contract v3.")
            self.assertEqual([], submit_task(product, review_work["id"]))

            review_path.write_text(review_text.replace("## Issues", "## Extra\n\nInjected.\n\n## Issues"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "differs from submitted review provenance"):
                approve_section(product, "P01")

            review_path.write_text(review_text, encoding="utf-8")
            approve_section(product, "P01")
            approved = json.loads((root / "section.json").read_text(encoding="utf-8"))
            self.assertTrue(approved["human_approved"])


if __name__ == "__main__":
    unittest.main()
