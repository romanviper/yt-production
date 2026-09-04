from pathlib import Path

from scripts.common import REPO_ROOT, read_json
from scripts.section_overlay_contract import resolve_section_spec


def test_p01_primary_substrate_is_intentionally_smaller_than_truth_ceiling() -> None:
    product = REPO_ROOT / "products" / "sumer-writing"
    resolved, _authority = resolve_section_spec(product, "P01")
    evidence = read_json(product / "03_sections" / "P01" / "evidence-pack.json")

    selected = resolved["historical_substrate_ids"]
    assert selected == [
        "HS-P01-0001",
        "HS-P01-0003",
        "HS-P01-0004",
        "HS-P01-0007",
    ]
    assert len(selected) < len(evidence["claim_ids"])
    assert set(evidence["claim_ids"]) == {
        "CLM-0011",
        "CLM-0012",
        "CLM-0013",
        "CLM-0014",
        "CLM-0015",
        "CLM-0016",
        "CLM-0017",
        "CLM-0018",
    }
