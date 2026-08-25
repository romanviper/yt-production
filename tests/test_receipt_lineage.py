from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.common import sha256
from scripts.context_packet import compile_packet
from scripts.draft_evidence import (
    REVIEW_RECORD_PROJECTION_END,
    REVIEW_RECORD_PROJECTION_START,
    DraftEvidenceBroker,
    EvidenceAccessError,
    MAX_REVIEW_RECORD_PARENT_LOCATOR_CHARS,
    MAX_REVIEW_RECORD_RECEIPTS,
)
from scripts.materialize_sections import materialize
from scripts.packet_contract import validate_packet_contract
from scripts.task import create_task, submit_task
from test_material_aware_handoff import make_direct_authorship_fixture, write_json
from test_writer_baseline import submit_fixture_prose


def _brief(path: Path, headline: str) -> None:
    write_json(
        path,
        {
            "schema_version": 1,
            "status": "ready_for_review",
            "headline": headline,
            "material_points": ["The task stayed inside the routed section scope."],
            "decision": {
                "required": True,
                "question": "Run independent review?",
                "recommendation": "Route the fresh review task.",
                "options": [{"label": "Review", "effect": "Evaluate the submitted prose."}],
            },
            "next_step": "",
        },
    )


def _route_revision(product: Path, direct_details: list[str] | None = None) -> tuple[str, str]:
    root = product / "03_sections" / "P01"
    state_path = root / "section.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    draft_task_id = str(state["prose_provenance"]["task_id"])
    state["status"] = "changes_requested"
    write_json(state_path, state)
    (root / "review.md").write_text(
        "# Outcome Evaluation — P01\n\nVerdict: changes_requested\n\n"
        "## Issues\n\nOne sentence needs a bounded evidence qualification.\n\n"
        "## Routing\n\nRoute that sentence only to prose_execution.\n",
        encoding="utf-8",
    )
    (root / "change-request.md").write_text(
        "# Change Request — P01\n\n## Approved revision scope\n\nQualify one sentence.\n",
        encoding="utf-8",
    )
    work = create_task(product, "revise_section", "P01", None, False)
    task_id = work["id"]
    if direct_details:
        broker = DraftEvidenceBroker(product, task_id)
        for index, detail in enumerate(direct_details):
            broker.call(
                "record",
                {
                    "source_id": "SRC-0001",
                    "parent_locator": "p. 10",
                    "locator": f"p. 10, revision detail {index}",
                    "detail": detail,
                },
            )
    (root / "draft.md").write_text("# P01\n\nA qualified, supported historical progression.\n", encoding="utf-8")
    (root / "handoff.md").write_text("The listener still reaches the assigned exit state.\n", encoding="utf-8")
    (root / "revision-log.md").write_text("Qualified one bounded sentence.\n", encoding="utf-8")
    task_root = product / "tasks" / task_id
    (task_root / "report.md").write_text("One diagnosed revision completed.\n", encoding="utf-8")
    _brief(task_root / "operator-brief.json", "P01 revision is ready for fresh review.")
    errors = submit_task(product, task_id)
    if errors:
        raise AssertionError("fixture revision submission failed: " + "; ".join(errors))
    return draft_task_id, task_id


def _revised_fixture(temp: str, inherited: list[str], direct: list[str] | None = None) -> tuple[Path, str, str]:
    product = make_direct_authorship_fixture(Path(temp))
    materialize(product)
    submit_fixture_prose(product, inherited)
    draft_id, revision_id = _route_revision(product, direct)
    return product, draft_id, revision_id


def _json_digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _canonical_projection_tokens(projection: dict[str, object]) -> int:
    canonical = copy.deepcopy(projection)
    telemetry = canonical["telemetry"]
    assert isinstance(telemetry, dict)
    telemetry["estimated_projection_tokens"] = 0
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return (len(encoded) + 3) // 4 + int(telemetry["serialization_margin_tokens"])


def _rewrite_projection_context(task_root: Path, packet: dict[str, object]) -> Path:
    projection = packet["recorded_evidence_projection"]
    assert isinstance(projection, dict)
    telemetry = projection["telemetry"]
    assert isinstance(telemetry, dict)
    telemetry["estimated_projection_tokens"] = _canonical_projection_tokens(projection)
    context_path = task_root / "context.md"
    context = context_path.read_text(encoding="utf-8")
    start = context.index(REVIEW_RECORD_PROJECTION_START) + len(REVIEW_RECORD_PROJECTION_START)
    end = context.index(REVIEW_RECORD_PROJECTION_END)
    context = context[:start] + "\n" + json.dumps(projection, ensure_ascii=False, indent=2) + "\n" + context[end:]
    context_path.write_text(context, encoding="utf-8")
    packet["context_sha256"] = sha256(context_path)
    return context_path


class ReceiptLineageTests(unittest.TestCase):
    def test_draft_receipts_survive_one_revision_without_a_new_trace(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product, draft_id, revision_id = _revised_fixture(temp, ["Inherited measured detail."])
            self.assertFalse((product / "tasks" / revision_id / "evidence-trace.jsonl").exists())

            work = create_task(product, "review_section", "P01", None, False)
            task_root = product / "tasks" / work["id"]
            packet = json.loads((task_root / "packet.json").read_text(encoding="utf-8"))
            projection = packet["recorded_evidence_projection"]

            self.assertEqual(5, packet["schema_version"])
            self.assertEqual("projected", projection["recorded_evidence_state"])
            self.assertEqual(1, projection["depth"])
            self.assertEqual(revision_id, projection["current_prose_task"]["task_id"])
            self.assertEqual([draft_id], [item["task_id"] for item in projection["receipt_origins"]])
            self.assertEqual(draft_id, projection["records"][0]["origin_task_id"])
            self.assertEqual([], validate_packet_contract(packet, task_root / "context.md"))

    def test_revision_receipts_union_with_inherited_receipts_in_declared_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product, draft_id, revision_id = _revised_fixture(
                temp,
                ["Inherited detail."],
                ["New revision detail."],
            )
            packet, context = compile_packet(product, "review_section", "T9999-review-section-P01", section="P01")
            projection = packet["recorded_evidence_projection"]

            self.assertEqual([draft_id, revision_id], [item["task_id"] for item in projection["receipt_origins"]])
            self.assertEqual(
                [(draft_id, "Inherited detail."), (revision_id, "New revision detail.")],
                [(item["origin_task_id"], item["detail"]) for item in projection["records"]],
            )
            self.assertIn("New revision detail.", context)

    def test_explicit_none_and_legacy_v4_are_never_inferred(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            submit_fixture_prose(product, [])
            draft_id, revision_id = _route_revision(product)
            revision_packet_path = product / "tasks" / revision_id / "packet.json"
            revision_packet = json.loads(revision_packet_path.read_text(encoding="utf-8"))
            self.assertEqual("none", revision_packet["receipt_lineage_anchor"]["state"])
            self.assertIsNone(revision_packet["receipt_lineage_anchor"]["receipt_origin"])
            packet, _ = compile_packet(product, "review_section", "T9998-review-section-P01", section="P01")
            self.assertEqual("none", packet["recorded_evidence_projection"]["recorded_evidence_state"])
            self.assertEqual([], packet["recorded_evidence_projection"]["records"])

            broker = DraftEvidenceBroker(product, draft_id)
            broker.call(
                "record",
                {
                    "source_id": "SRC-0001",
                    "parent_locator": "p. 10",
                    "locator": "p. 10, late valid detail",
                    "detail": "A valid receipt added after the immutable none anchor.",
                },
            )
            trace_path = product / "tasks" / draft_id / "evidence-trace.jsonl"
            traces = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
            draft_work = json.loads((product / "tasks" / draft_id / "work-order.json").read_text(encoding="utf-8"))
            next(item for item in traces if item.get("capability") == "record")["at"] = draft_work["submitted_at"]
            trace_path.write_text(
                "\n".join(json.dumps(item, ensure_ascii=False) for item in traces) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(EvidenceAccessError, "trace attestation"):
                compile_packet(product, "review_section", "T9988-review-section-P01", section="P01")

        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            draft_id = submit_fixture_prose(product, ["Old receipt must not be inferred."])
            old_packet_path = product / "tasks" / draft_id / "packet.json"
            old_packet = json.loads(old_packet_path.read_text(encoding="utf-8"))
            old_packet["schema_version"] = 4
            write_json(old_packet_path, old_packet)
            self.assertEqual([], validate_packet_contract(old_packet, product / "tasks" / draft_id / "context.md"))
            with self.assertRaisesRegex(EvidenceAccessError, "packet schema or hash has changed"):
                compile_packet(product, "review_section", "T9997-downgraded-review-P01", section="P01")

            root = product / "03_sections" / "P01"
            state_path = root / "section.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["prose_provenance"].pop("schema_version")
            state["prose_provenance"].pop("packet_schema_version")
            state["prose_provenance"].pop("task_packet_sha256")
            write_json(state_path, state)
            packet, context = compile_packet(product, "review_section", "T9997-review-section-P01", section="P01")
            projection = packet["recorded_evidence_projection"]
            self.assertEqual("legacy_unverifiable", projection["recorded_evidence_state"])
            self.assertEqual([], projection["records"])
            self.assertNotIn("Old receipt must not be inferred.", context)

            frozen_review = copy.deepcopy(packet)
            frozen_review["schema_version"] = 4
            frozen_review.pop("recorded_evidence_projection")
            self.assertEqual([], validate_packet_contract(frozen_review))

            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            state["status"] = "changes_requested"
            write_json(root / "section.json", state)
            (root / "review.md").write_text(
                "# Outcome Evaluation — P01\n\nVerdict: changes_requested\n\n"
                "## Issues\n\nOne sentence needs a bounded evidence qualification.\n\n"
                "## Routing\n\nRoute that sentence only to prose_execution.\n",
                encoding="utf-8",
            )
            (root / "change-request.md").write_text(
                "# Change Request — P01\n\n## Approved revision scope\n\nQualify one sentence.\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(EvidenceAccessError, "schema-v5 draft predecessor"):
                create_task(product, "revise_section", "P01", None, False)

    def test_v5_prose_provenance_binds_packet_schema_hash_and_submission_timestamp(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            draft_id = submit_fixture_prose(product, ["Timestamp-bound draft detail."])
            root = product / "03_sections" / "P01"
            state = json.loads((root / "section.json").read_text(encoding="utf-8"))
            provenance = state["prose_provenance"]
            self.assertEqual(2, provenance["schema_version"])
            self.assertEqual(5, provenance["packet_schema_version"])

            work_path = product / "tasks" / draft_id / "work-order.json"
            work = json.loads(work_path.read_text(encoding="utf-8"))
            work["submitted_at"] = "2001-01-01T00:00:00+00:00"
            write_json(work_path, work)
            with self.assertRaisesRegex(EvidenceAccessError, "timestamp differs"):
                compile_packet(product, "review_section", "T9987-review-section-P01", section="P01")

        with tempfile.TemporaryDirectory() as temp:
            product, _, revision_id = _revised_fixture(
                temp,
                ["Inherited timestamp-bound detail."],
                ["Direct timestamp-bound detail."],
            )
            work_path = product / "tasks" / revision_id / "work-order.json"
            work = json.loads(work_path.read_text(encoding="utf-8"))
            work["submitted_at"] = "2001-01-01T00:00:00.000001+00:00"
            write_json(work_path, work)
            with self.assertRaisesRegex(EvidenceAccessError, "timestamp differs"):
                compile_packet(product, "review_section", "T9986-review-section-P01", section="P01")

        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            draft_id = submit_fixture_prose(product, ["Schema-bound draft detail."])
            packet_path = product / "tasks" / draft_id / "packet.json"
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            packet["schema_version"] = 4
            write_json(packet_path, packet)
            with self.assertRaisesRegex(EvidenceAccessError, "packet schema or hash has changed"):
                compile_packet(product, "review_section", "T9985-review-section-P01", section="P01")

    def test_predecessor_trace_attestation_binds_nonrecord_content_and_absence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            draft_id = submit_fixture_prose(product, [])
            trace_path = product / "tasks" / draft_id / "evidence-trace.jsonl"
            self.assertTrue(trace_path.is_file())
            _, revision_id = _route_revision(product)
            revision_root = product / "tasks" / revision_id
            revision_packet = json.loads((revision_root / "packet.json").read_text(encoding="utf-8"))
            self.assertEqual("present", revision_packet["receipt_lineage_anchor"]["predecessor_trace"]["state"])
            review_work = create_task(product, "review_section", "P01", None, False)
            review_root = product / "tasks" / review_work["id"]
            review_packet = json.loads((review_root / "packet.json").read_text(encoding="utf-8"))

            trace_path.write_text('{"schema_version":1,"capability":"scope","forged":true}\n', encoding="utf-8")
            revision_errors = validate_packet_contract(revision_packet, revision_root / "context.md")
            self.assertTrue(any("predecessor trace" in error for error in revision_errors), revision_errors)
            review_errors = validate_packet_contract(review_packet, review_root / "context.md")
            self.assertTrue(any("cannot reconstruct its declared prose lineage" in error for error in review_errors))

        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            draft_id = submit_fixture_prose(product, [])
            trace_path = product / "tasks" / draft_id / "evidence-trace.jsonl"
            trace_path.unlink()
            _, revision_id = _route_revision(product)
            revision_root = product / "tasks" / revision_id
            revision_packet = json.loads((revision_root / "packet.json").read_text(encoding="utf-8"))
            self.assertEqual("absent", revision_packet["receipt_lineage_anchor"]["predecessor_trace"]["state"])
            review_work = create_task(product, "review_section", "P01", None, False)
            review_root = product / "tasks" / review_work["id"]
            review_packet = json.loads((review_root / "packet.json").read_text(encoding="utf-8"))

            trace_path.write_text('{"schema_version":1,"capability":"scope"}\n', encoding="utf-8")
            revision_errors = validate_packet_contract(revision_packet, revision_root / "context.md")
            self.assertTrue(any("absent predecessor trace" in error for error in revision_errors), revision_errors)
            review_errors = validate_packet_contract(review_packet, review_root / "context.md")
            self.assertTrue(any("cannot reconstruct its declared prose lineage" in error for error in review_errors))

        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            draft_id = submit_fixture_prose(product, [])
            trace_path = product / "tasks" / draft_id / "evidence-trace.jsonl"
            _, revision_id = _route_revision(product)
            revision_root = product / "tasks" / revision_id
            revision_packet = json.loads((revision_root / "packet.json").read_text(encoding="utf-8"))
            review_work = create_task(product, "review_section", "P01", None, False)
            review_root = product / "tasks" / review_work["id"]
            review_packet = json.loads((review_root / "packet.json").read_text(encoding="utf-8"))

            trace_path.unlink()
            revision_errors = validate_packet_contract(revision_packet, revision_root / "context.md")
            self.assertTrue(any("predecessor trace" in error for error in revision_errors), revision_errors)
            review_errors = validate_packet_contract(review_packet, review_root / "context.md")
            self.assertTrue(any("cannot reconstruct its declared prose lineage" in error for error in review_errors))

    def test_frozen_v4_review_with_v1_receipts_still_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = make_direct_authorship_fixture(Path(temp))
            materialize(product)
            submit_fixture_prose(product, ["Frozen v1 detail."])
            packet, _ = compile_packet(product, "review_section", "T9991-review-section-P01", section="P01")
            projection = packet["recorded_evidence_projection"]
            origin = projection["receipt_origins"][0]
            records = [{key: value for key, value in item.items() if key != "origin_task_id"} for item in projection["records"]]
            records[0]["parent_locator"] = "p" * (MAX_REVIEW_RECORD_PARENT_LOCATOR_CHARS + 1)
            telemetry = dict(projection["telemetry"])
            telemetry.pop("origin_count")
            frozen = copy.deepcopy(packet)
            frozen["schema_version"] = 4
            frozen["recorded_evidence_projection"] = {
                "schema_version": 1,
                "projection_kind": "submitted_prose_record_receipts",
                "source_task_id": origin["task_id"],
                "source_operation": origin["operation"],
                "source_trace_path": origin["trace_path"],
                "source_trace_sha256": origin["trace_sha256"],
                "source_task_packet_sha256": origin["task_packet_sha256"],
                "narration_pack_sha256": projection["narration_pack_sha256"],
                "evidence_pack_sha256": projection["evidence_pack_sha256"],
                "records": records,
                "records_sha256": _json_digest(records),
                "truth_ceiling_unchanged": True,
                "telemetry": telemetry,
            }
            telemetry["estimated_projection_tokens"] = _canonical_projection_tokens(
                frozen["recorded_evidence_projection"]
            )
            self.assertEqual([], validate_packet_contract(frozen))

    def test_lineage_tamper_matrix_hard_fails_without_scanning_for_a_replacement(self) -> None:
        cases = {
            "missing anchor": lambda packet, product, draft_id: packet.pop("receipt_lineage_anchor"),
            "predecessor trace hash": lambda packet, product, draft_id: packet["receipt_lineage_anchor"]["predecessor_trace"].__setitem__("sha256", "0" * 64),
            "trace hash": lambda packet, product, draft_id: packet["receipt_lineage_anchor"]["receipt_origin"].__setitem__("trace_sha256", "0" * 64),
            "trace path": lambda packet, product, draft_id: packet["receipt_lineage_anchor"]["receipt_origin"].__setitem__("trace_path", "tasks/T9999-wrong/evidence-trace.jsonl"),
            "section": lambda packet, product, draft_id: packet["receipt_lineage_anchor"].__setitem__("section", "P02"),
            "cycle": lambda packet, product, draft_id: packet["receipt_lineage_anchor"].__setitem__("cycle_id", "C999"),
            "timestamp": lambda packet, product, draft_id: packet["receipt_lineage_anchor"]["predecessor"].__setitem__("submitted_at", "2026-01-01T00:00:00+07:00"),
            "predecessor": lambda packet, product, draft_id: packet["receipt_lineage_anchor"]["predecessor"].__setitem__("operation", "revise_section"),
            "depth": lambda packet, product, draft_id: packet["receipt_lineage_anchor"].__setitem__("depth", 2),
            "revision input": lambda packet, product, draft_id: next(item for item in packet["inputs"] if item["path"].endswith("/draft.md")).__setitem__("sha256", "0" * 64),
        }
        for label, mutate in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                product, draft_id, revision_id = _revised_fixture(temp, ["Immutable inherited detail."])
                packet_path = product / "tasks" / revision_id / "packet.json"
                packet = json.loads(packet_path.read_text(encoding="utf-8"))
                mutate(packet, product, draft_id)
                write_json(packet_path, packet)
                with self.assertRaises(EvidenceAccessError, msg=label):
                    compile_packet(product, "review_section", "T9996-review-section-P01", section="P01")

        with tempfile.TemporaryDirectory() as temp:
            product, draft_id, _ = _revised_fixture(temp, ["Immutable inherited detail."])
            (product / "tasks" / draft_id / "evidence-trace.jsonl").unlink()
            with self.assertRaises(EvidenceAccessError):
                compile_packet(product, "review_section", "T9995-review-section-P01", section="P01")

        with tempfile.TemporaryDirectory() as temp:
            product, draft_id, _ = _revised_fixture(temp, ["Immutable inherited detail."])
            predecessor_packet = product / "tasks" / draft_id / "packet.json"
            value = json.loads(predecessor_packet.read_text(encoding="utf-8"))
            value["created_at"] = "2026-01-01T00:00:00+00:00"
            write_json(predecessor_packet, value)
            with self.assertRaises(EvidenceAccessError):
                compile_packet(product, "review_section", "T9994-review-section-P01", section="P01")

        with tempfile.TemporaryDirectory() as temp:
            product, _, _ = _revised_fixture(temp, ["Immutable inherited detail."])
            draft = product / "03_sections" / "P01" / "draft.md"
            draft.write_text("# P01\n\nTampered after revision submission.\n", encoding="utf-8")
            with self.assertRaises(EvidenceAccessError):
                compile_packet(product, "review_section", "T9993-review-section-P01", section="P01")

        for label, replacement in [("missing", None), ("malformed", "{bad packet\n")]:
            with self.subTest(current_packet=label), tempfile.TemporaryDirectory() as temp:
                product, _, revision_id = _revised_fixture(temp, ["Immutable inherited detail."])
                current_packet = product / "tasks" / revision_id / "packet.json"
                if replacement is None:
                    current_packet.unlink()
                else:
                    current_packet.write_text(replacement, encoding="utf-8")
                with self.assertRaises(EvidenceAccessError):
                    compile_packet(product, "review_section", "T9990-review-section-P01", section="P01")

    def test_union_caps_fail_closed_and_context_must_equal_manifest(self) -> None:
        inherited_count = MAX_REVIEW_RECORD_RECEIPTS // 2 + 1
        direct_count = MAX_REVIEW_RECORD_RECEIPTS - inherited_count + 1
        with tempfile.TemporaryDirectory() as temp:
            product, _, _ = _revised_fixture(
                temp,
                [f"Inherited detail {index}." for index in range(inherited_count)],
                [f"Revision detail {index}." for index in range(direct_count)],
            )
            with self.assertRaisesRegex(EvidenceAccessError, "submitted prose lineage has"):
                compile_packet(product, "review_section", "T9992-review-section-P01", section="P01")

        with tempfile.TemporaryDirectory() as temp:
            product, _, revision_id = _revised_fixture(temp, ["Context-bound inherited detail."])
            work = create_task(product, "review_section", "P01", None, False)
            task_root = product / "tasks" / work["id"]
            packet_path = task_root / "packet.json"
            context_path = task_root / "context.md"
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            self.assertEqual([], validate_packet_contract(packet, context_path))
            packet["recorded_evidence_projection"]["records"][0]["detail"] = "Manifest-only tamper."
            self.assertTrue(
                any(
                    "differs from compiled context" in error
                    for error in validate_packet_contract(packet, context_path)
                )
            )

            capped = json.loads(packet_path.read_text(encoding="utf-8"))
            capped_projection = capped["recorded_evidence_projection"]
            capped_record = capped_projection["records"][0]
            capped_record["parent_locator"] = "p" * (MAX_REVIEW_RECORD_PARENT_LOCATOR_CHARS + 1)
            capped_origin = capped_projection["receipt_origins"][0]
            capped_origin_records = [
                {key: value for key, value in record.items() if key != "origin_task_id"}
                for record in capped_projection["records"]
                if record["origin_task_id"] == capped_origin["task_id"]
            ]
            capped_origin["records_sha256"] = _json_digest(capped_origin_records)
            capped_projection["records_sha256"] = _json_digest(capped_projection["records"])
            capped_projection["telemetry"]["estimated_projection_tokens"] = _canonical_projection_tokens(
                capped_projection
            )
            capped_errors = validate_packet_contract(capped)
            self.assertTrue(any("invalid parent_locator" in error for error in capped_errors), capped_errors)

            noncanonical = json.loads(packet_path.read_text(encoding="utf-8"))
            noncanonical["recorded_evidence_projection"]["telemetry"]["estimated_projection_tokens"] = 0
            noncanonical_errors = validate_packet_contract(noncanonical)
            self.assertTrue(any("token estimate is not canonical" in error for error in noncanonical_errors))

            broker = DraftEvidenceBroker(product, revision_id)
            oversized_parent = "p" * (MAX_REVIEW_RECORD_PARENT_LOCATOR_CHARS + 1)
            broker.sources_by_id["SRC-0001"]["locators"] = [oversized_parent]
            with self.assertRaisesRegex(EvidenceAccessError, "parent_locator must be non-empty text up to"):
                broker.record(
                    {
                        "source_id": "SRC-0001",
                        "parent_locator": oversized_parent,
                        "locator": "bounded locator",
                        "detail": "This call must fail before a successful receipt can be written.",
                    }
                )

    def test_frozen_review_reconstructs_union_direct_trace_and_timestamp_edge(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product, _, revision_id = _revised_fixture(temp, ["Anchored inherited detail."])
            work = create_task(product, "review_section", "P01", None, False)
            task_root = product / "tasks" / work["id"]
            packet = json.loads((task_root / "packet.json").read_text(encoding="utf-8"))
            context_path = task_root / "context.md"
            context = context_path.read_text(encoding="utf-8")

            projection = packet["recorded_evidence_projection"]
            projection["recorded_evidence_state"] = "none"
            projection["receipt_origins"] = []
            projection["records"] = []
            projection["records_sha256"] = hashlib.sha256(b"[]").hexdigest()
            projection["telemetry"]["eligible_receipts"] = 0
            projection["telemetry"]["included_receipts"] = 0
            projection["telemetry"]["origin_count"] = 0
            context_path = _rewrite_projection_context(task_root, packet)
            errors = validate_packet_contract(packet, context_path)
            self.assertTrue(any("differs from reconstructed prose lineage" in error for error in errors), errors)

        with tempfile.TemporaryDirectory() as temp:
            product, _, revision_id = _revised_fixture(
                temp,
                ["Anchored inherited detail."],
                ["Direct bound detail."],
            )
            work = create_task(product, "review_section", "P01", None, False)
            task_root = product / "tasks" / work["id"]
            packet = json.loads((task_root / "packet.json").read_text(encoding="utf-8"))
            projection = packet["recorded_evidence_projection"]
            direct_record = next(
                record for record in projection["records"] if record["origin_task_id"] == revision_id
            )
            direct_record["detail"] = direct_record["detail"].replace("Direct", "Forged")
            direct_record["response_sha256"] = "f" * 64
            direct_origin = next(
                origin for origin in projection["receipt_origins"] if origin["task_id"] == revision_id
            )
            direct_origin_records = [
                {key: value for key, value in record.items() if key != "origin_task_id"}
                for record in projection["records"]
                if record["origin_task_id"] == revision_id
            ]
            direct_origin["records_sha256"] = _json_digest(direct_origin_records)
            projection["records_sha256"] = _json_digest(projection["records"])
            context_path = _rewrite_projection_context(task_root, packet)
            errors = validate_packet_contract(packet, context_path)
            self.assertTrue(any("differs from reconstructed prose lineage" in error for error in errors), errors)

        with tempfile.TemporaryDirectory() as temp:
            product, _, revision_id = _revised_fixture(temp, ["Anchored inherited detail."])
            work = create_task(product, "review_section", "P01", None, False)
            task_root = product / "tasks" / work["id"]
            packet = json.loads((task_root / "packet.json").read_text(encoding="utf-8"))
            source_work_path = product / "tasks" / revision_id / "work-order.json"
            source_work = json.loads(source_work_path.read_text(encoding="utf-8"))
            source_work["submitted_at"] = "2001-01-01T00:00:00+00:00"
            write_json(source_work_path, source_work)
            packet["recorded_evidence_projection"]["current_prose_task"]["submitted_at"] = source_work["submitted_at"]
            context_path = _rewrite_projection_context(task_root, packet)
            errors = validate_packet_contract(packet, context_path)
            self.assertTrue(any("cannot reconstruct its declared prose lineage" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
