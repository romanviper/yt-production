import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "p01_loop", Path(__file__).resolve().parents[1] / "scripts/experiments/p01_foc_loop.py")
loop = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(loop)


def product(winner="A"):
    return {"packet_sha256": "hash", "winner": winner,
            "dimensions": {d: {"winner": winner, "a_quote": "Old text", "b_quote": "New text",
                               "reference_id": "ref", "reference_quote": "Reference",
                               "reason": "Effect", "remaining_gap": "Gap"} for d in loop.DIMS},
            "strongest_counterargument": "A competing explanation"}


class Gates(unittest.TestCase):
    def setUp(self):
        self.packet = {"samples": {"A": "Old text.", "B": "New text."},
                       "craft_references": [{"id": "ref", "text": "Reference text."}]}
        self.truth_packet = {"candidate": [{"id": "S001", "text": "A clay object."}],
                             "authority": {"source": "Catalogue: clay object."}}
        self.truth = {"packet_sha256": "hash", "unresolved": [], "claims": [
            {"sentence_id": "S001", "claim_quote": "clay object", "status": "SUPPORTED",
             "source": "source", "locator": "Catalogue", "source_quote": "clay object",
             "reason": "Entity and material recorded"}]}

    def test_valid_product(self):
        loop.validate_product(product(), self.packet, "hash")

    def test_fabricated_quote(self):
        r = product()
        r["dimensions"]["movement"]["a_quote"] = "invented"
        with self.assertRaises(ValueError):
            loop.validate_product(r, self.packet, "hash")

    def test_empty_quote(self):
        with self.assertRaises(ValueError):
            loop.exact("", "anything", "empty")

    def test_missing_dimension(self):
        r = product()
        del r["dimensions"]["payoff"]
        with self.assertRaises(ValueError):
            loop.validate_product(r, self.packet, "hash")

    def test_stale_review(self):
        with self.assertRaises(ValueError):
            loop.validate_product(product(), self.packet, "changed")

    def test_missing_gap(self):
        r = product()
        r["dimensions"]["payoff"]["remaining_gap"] = ""
        with self.assertRaises(ValueError):
            loop.validate_product(r, self.packet, "hash")

    def test_truth_supported(self):
        self.assertTrue(loop.validate_truth(self.truth, self.truth_packet, "hash"))

    def test_truth_unknown_source(self):
        self.truth["claims"][0]["source"] = "FoC"
        with self.assertRaises(ValueError):
            loop.validate_truth(self.truth, self.truth_packet, "hash")

    def test_truth_missing_sentence(self):
        self.truth_packet["candidate"].append({"id": "S002", "text": "Other claim."})
        with self.assertRaises(ValueError):
            loop.validate_truth(self.truth, self.truth_packet, "hash")

    def test_truth_unsupported(self):
        self.truth["claims"][0]["status"] = "UNSUPPORTED"
        self.assertFalse(loop.validate_truth(self.truth, self.truth_packet, "hash"))

    def test_truth_unresolved(self):
        self.truth["unresolved"] = ["Missing motive authority"]
        self.assertFalse(loop.validate_truth(self.truth, self.truth_packet, "hash"))

    def test_exact_quote_does_not_prove_entailment(self):
        # Explicit limit: code accepts a wrong interpretation of a real quote.
        # The semantic audit MUST catch this; no semantic certification claimed.
        self.truth["claims"][0]["reason"] = "This proves taxation (it does not)."
        self.assertTrue(loop.validate_truth(self.truth, self.truth_packet, "hash"))

    def test_decision_matrix(self):
        r = {"product-1": product("A"), "product-2": product("B")}
        labels = {"product-1": "A", "product-2": "B"}
        self.assertEqual(loop.outcome(True, True, r, labels), "PROVISIONAL_SCRIPT_IMPROVEMENT")
        self.assertEqual(loop.outcome(False, True, r, labels), "REJECT_TRUTH")
        self.assertEqual(loop.outcome(True, False, r, labels), "INCONCLUSIVE_PROCESS")
        for value in ("A", "TIE", "UNCERTAIN"):
            r["product-2"]["winner"] = value
            self.assertEqual(loop.outcome(True, True, r, labels), "NO_DEMONSTRATED_GAIN")

    def test_position_bias_rejected(self):
        r = {"product-1": product("A"), "product-2": product("A")}
        self.assertEqual(loop.outcome(True, True, r, {"product-1": "A", "product-2": "B"}),
                         "NO_DEMONSTRATED_GAIN")

    def test_regression_rejected(self):
        r = {"product-1": product("A"), "product-2": product("B")}
        r["product-1"]["dimensions"]["listenability"]["winner"] = "B"
        self.assertEqual(loop.outcome(True, True, r, {"product-1": "A", "product-2": "B"}),
                         "NO_DEMONSTRATED_GAIN")

    def test_movement_tie_rejected(self):
        r = {"product-1": product("A"), "product-2": product("B")}
        r["product-1"]["dimensions"]["movement"]["winner"] = "TIE"
        self.assertEqual(loop.outcome(True, True, r, {"product-1": "A", "product-2": "B"}),
                         "NO_DEMONSTRATED_GAIN")

    def test_missing_execution_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(loop.process_valid(Path(tmp), {}))

    def test_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(loop.evidence_file(Path(tmp), "../outside", "hash"))
            with self.assertRaises(ValueError):
                loop.runpath(Path(tmp), "../../elsewhere")

    def test_no_automatic_round_two(self):
        with self.assertRaises(ValueError):
            loop.runpath(Path("."), "round-02")

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "a.json"
            loop.write_json(p, {})
            with self.assertRaises(ValueError):
                loop.write_json(p, {"changed": True})

    def test_real_inputs_and_public_packet_no_answer_labels(self):
        c = loop.config()
        packet = loop.product_packet(loop.ROOT, c, {"A": "Text one", "B": "Text two"})
        text = json.dumps(packet)
        for forbidden in ("EXPLANATORY_ESSAY", "GENUINE_NARRATIVE_MOVEMENT", "hypothesis", "candidate_labels"):
            self.assertNotIn(forbidden, text)
        self.assertEqual(len(packet["craft_references"]), 3)
        self.assertTrue(all(r["audio_status"] == "NOT_VERIFIED" for r in packet["craft_references"]))

    def test_sentence_coverage_preserves_tail(self):
        self.assertEqual(len(loop.sentences("First. Second!\nLast fragment")), 3)


class Workflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in loop.tracked_inputs(loop.config()):
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(loop.ROOT / name, dest)
        loop.write_json(self.root / loop.DOC / "inputs.lock.json", loop.snapshot(self.root))

    def prepared(self):
        loop.writer(self.root, "round-01")
        run = loop.runpath(self.root, "round-01")
        # Deliberately meaningless synthetic text: exercise plumbing, not quality.
        (run / "candidate.md").write_text("Synthetic fixture " * 350 + ".", encoding="utf-8")
        loop.prepare(self.root, "round-01")
        dispatch = loop.load(run / "dispatch.json")
        for role, sha in dispatch["packet_hashes"].items():
            packet = loop.load(run / f"{role}-packet.json")
            if role == "truth":
                review = {"packet_sha256": sha, "unresolved": [], "claims": [
                    {"sentence_id": s["id"], "claim_quote": s["text"], "status": "NONFACTUAL",
                     "source": "", "source_quote": "", "locator": "", "reason": "Synthetic test"}
                    for s in packet["candidate"]]}
            else:
                review = product(dispatch["candidate_labels"][role])
                review["packet_sha256"] = sha
                for f in review["dimensions"].values():
                    f["a_quote"] = packet["samples"]["A"][:30]
                    f["b_quote"] = packet["samples"]["B"][:30]
                    f["reference_id"] = packet["craft_references"][0]["id"]
                    f["reference_quote"] = packet["craft_references"][0]["text"][:30]
            loop.write_json(run / f"{role}.json", review)
        return run

    def test_full_flow_does_not_certify_missing_execution(self):
        self.prepared()
        result = loop.decide(self.root, "round-01")
        self.assertEqual(result["status"], "INCONCLUSIVE_PROCESS")
        self.assertEqual(result["audio_status"], "NOT_EVALUATED")

    def test_full_flow_only_provisional_with_synthetic_execution(self):
        run = self.prepared()
        execution = loop.load(run / "execution.template.json")
        for index, (role, record) in enumerate(execution["roles"].items()):
            filename = f"test-only-export-{index}.txt"
            text = "SYNTHETIC TEST EXPORT, NOT AN AGENT RUN"
            (run / filename).write_text(text, encoding="utf-8")
            record.update(run_id=str(index), model_config="TEST ONLY",
                          started_at="2026-09-05T00:00:00Z", finished_at="2026-09-05T00:01:00Z",
                          input_only_enforced=True, platform_export=filename,
                          platform_export_sha256=loop.digest(text))
        (run / "audit.txt").write_text("SYNTHETIC TEST AUDIT", encoding="utf-8")
        execution["commander_semantic_audit"] = {
            "complete": True, "evidence_file": "audit.txt", "sha256": loop.digest("SYNTHETIC TEST AUDIT")}
        loop.write_json(run / "execution.json", execution)
        result = loop.decide(self.root, "round-01")
        self.assertEqual(result["status"], "PROVISIONAL_SCRIPT_IMPROVEMENT")
        self.assertEqual(result["human_listener_status"], "NOT_EVALUATED")
        # This also documents the boundary: code cannot authenticate platform exports.
        execution["roles"]["truth"]["finished_at"] = "yesterday"
        self.assertFalse(loop.process_valid(run, execution))

    def test_candidate_mutation_blocked(self):
        run = self.prepared()
        (run / "candidate.md").write_text("Changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Candidate changed"):
            loop.decide(self.root, "round-01")

    def test_packet_mutation_blocked(self):
        run = self.prepared()
        (run / "product-1-packet.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Packet changed"):
            loop.decide(self.root, "round-01")

    def test_input_mutation_blocked(self):
        path = self.root / loop.DOC / "protocol.md"
        path.write_text(loop.read(path) + "\nChanged criterion", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Frozen input drift"):
            loop.check(self.root)

    def test_duplicate_writer_blocked(self):
        loop.writer(self.root, "round-01")
        with self.assertRaises(ValueError):
            loop.writer(self.root, "round-01")

    def test_short_candidate_blocked(self):
        loop.writer(self.root, "round-01")
        run = loop.runpath(self.root, "round-01")
        (run / "candidate.md").write_text("Too short", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "whitespace units"):
            loop.prepare(self.root, "round-01")


if __name__ == "__main__":
    unittest.main()
