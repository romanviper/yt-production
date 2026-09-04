#!/usr/bin/env python3
"""Historical-Substrate-aware packet runtime with legacy compatibility.

The previous compiler is retained in ``context_packet_legacy``. This module
keeps its packet/provenance machinery but changes canonical Historical
Substrate routing at the runtime boundary: whole-outline creation requires
product-complete substrate, Reviewer receives the same compact historical
model as Writer, bounded evidence access is secondary verification, and stale
section/substrate projections cannot spawn tasks.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

try:
    import scripts.context_packet_legacy as _legacy
    from scripts.context_packet_legacy import *  # noqa: F401,F403 - compatibility surface
    from scripts.historical_substrate_contract import validate_historical_substrate
    from scripts.substrate_preflight import require_canonical_section_state
except ModuleNotFoundError:  # pragma: no cover
    import context_packet_legacy as _legacy
    from context_packet_legacy import *  # type: ignore # noqa: F401,F403
    from historical_substrate_contract import validate_historical_substrate
    from substrate_preflight import require_canonical_section_state


CANONICAL_REVIEW_REQUIRED_INPUTS = [
    "02_outline/outline.json",
    "03_sections/{section}/section.json",
    "03_sections/{section}/historical-substrate.json",
    "03_sections/{section}/narration-pack.json",
    "03_sections/{section}/draft.md",
    "03_sections/{section}/handoff.md",
]
_legacy.CANONICAL_REVIEW_REQUIRED_INPUTS = CANONICAL_REVIEW_REQUIRED_INPUTS

_LEGACY_DISCOVERY_TEXT = (
    "Use it inside the approved claim/source scope to discover story material as well as verify facts: "
    "who or what acts, what happens, where, what object or trace is present, what remains unexplained, "
    "and what later evidence changes the current understanding.\n"
    "These are optional retrieval questions, not required story ingredients or a narrative order; "
    "evidence records prescribe no creative route."
)
_CANONICAL_SECONDARY_TEXT = (
    "Evidence access is secondary verification only. Choose the telling from the Historical Substrate "
    "already present in this packet; use the adapter only to verify, sharpen, or qualify specific details "
    "required by that chosen telling.\n"
    "Do not survey evidence to discover the story route or to decide what historical reality exists to tell."
)


def _historical_substrate_runtime(product_dir: Path, operation: str, section: str | None) -> bool:
    if operation not in {"draft_section", "review_section", "revise_section"} or not section:
        return False
    state_path = product_dir.resolve() / "03_sections" / section / "section.json"
    substrate_path = product_dir.resolve() / "03_sections" / section / "historical-substrate.json"
    if not state_path.is_file() or not substrate_path.is_file():
        return False
    state = _legacy.read_json_local(state_path)
    return int(state.get("historical_substrate_contract_version") or 0) >= 1


def _require_product_complete_outline_substrate(product_dir: Path) -> None:
    product_dir = product_dir.resolve()
    substrate_path = product_dir / "01_research" / "historical-substrate.json"
    claims_path = product_dir / "01_research" / "claim-ledger.json"
    sources_path = product_dir / "01_research" / "source-index.json"
    if not substrate_path.is_file():
        raise ValueError("Outline creation requires 01_research/historical-substrate.json")
    errors = validate_historical_substrate(
        _legacy.read_json_local(substrate_path),
        _legacy.read_json_local(claims_path),
        _legacy.read_json_local(sources_path),
        require_product_complete=True,
    )
    if errors:
        raise ValueError("Outline Historical Substrate preflight failed: " + "; ".join(errors))


def compile_packet(
    product_dir: Path,
    operation: str,
    task_id: str,
    section: str | None = None,
    unit: str | None = None,
    execution_runtime: str | None = None,
) -> tuple[dict[str, Any], str]:
    if operation == "outline":
        _require_product_complete_outline_substrate(product_dir)

    canonical_substrate = _historical_substrate_runtime(product_dir, operation, section)
    if canonical_substrate and section:
        require_canonical_section_state(product_dir, section)

    packet, text = _legacy.compile_packet(
        product_dir,
        operation,
        task_id,
        section=section,
        unit=unit,
        execution_runtime=execution_runtime,
    )
    if not canonical_substrate or not section:
        return packet, text

    if _LEGACY_DISCOVERY_TEXT not in text:
        raise ValueError(
            "Canonical Historical Substrate packet could not replace legacy evidence-discovery routing; "
            "runtime header drifted."
        )
    text = text.replace(_LEGACY_DISCOVERY_TEXT, _CANONICAL_SECONDARY_TEXT)

    section_substrate = product_dir.resolve() / "03_sections" / section / "historical-substrate.json"
    state = _legacy.read_json_local(product_dir.resolve() / "03_sections" / section / "section.json")
    packet["historical_substrate"] = {
        "contract_version": state.get("historical_substrate_contract_version"),
        "section_projection_path": f"03_sections/{section}/historical-substrate.json",
        "section_projection_sha256": _legacy.sha256(section_substrate),
        "architecture_authority": state.get("architecture_authority"),
    }
    packet["context_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    packet["estimated_context_tokens"] = _legacy.estimate_tokens(text)
    return packet, text


def main() -> int:
    _legacy.compile_packet = compile_packet
    return _legacy.main()


if __name__ == "__main__":
    raise SystemExit(main())
