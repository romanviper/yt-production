import unittest

from scripts.common import REPO_ROOT, read_json
from scripts.historical_substrate_contract import (
    validate_historical_substrate,
    validate_section_binding,
    verify_writer_section_substrate,
)
from scripts.section_overlay_contract import resolve_section_spec


class P01SubstrateSelectionTest(unittest.TestCase):
    def setUp(self):
        self.product = REPO_ROOT / "products" / "sumer-writing"
        self.resolved, _ = resolve_section_spec(self.product, "P01")
        self.substrate = read_json(self.product / "01_research" / "historical-substrate.json")

    def test_selected_material_stays_within_evidence_authority(self):
        claims = read_json(self.product / "01_research" / "claim-ledger.json")
        sources = read_json(self.product / "01_research" / "source-index.json")
        evidence = read_json(self.product / "03_sections" / "P01" / "evidence-pack.json")
        self.assertEqual(validate_historical_substrate(self.substrate, claims, sources), [])
        self.assertEqual(validate_section_binding(self.resolved, self.substrate), [])
        selected = self.resolved["historical_substrate_ids"]
        records = {r["id"]: r for r in self.substrate["records"]}
        self.assertTrue(selected)
        self.assertEqual(len(selected), len(set(selected)))
        self.assertTrue(set(selected) < set(records))
        used_claims = {c for key in selected for c in records[key]["claim_ids"]}
        self.assertTrue(used_claims <= set(evidence["claim_ids"]))
        self.assertEqual(set(evidence["claim_ids"]), set(self.resolved["claim_ids"]))

    def test_writer_projection_is_current(self):
        self.assertEqual(verify_writer_section_substrate(self.product, "P01"), [])

    def test_section_narrative_contract_is_synchronized(self):
        state = read_json(self.product / "03_sections" / "P01" / "section.json")
        for key in ("narrative_job", "entry_state", "exit_state", "transition", "audience_discovery"):
            with self.subTest(field=key):
                self.assertEqual(state[key], self.resolved[key])


if __name__ == "__main__":
    unittest.main()
