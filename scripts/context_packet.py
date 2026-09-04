#!/usr/bin/env python3
"""Architecture-aware context packet compiler.

Compatibility and Historical Substrate routing are selected before the legacy
packet machinery assembles or budgets a prompt. The shared legacy compiler is
used as a packet/provenance engine, not as the authority for architecture mode.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any

try:
    import scripts.context_packet_legacy as _legacy
    from scripts.context_packet_legacy import *  # noqa: F401,F403
    from scripts.historical_substrate_adoption import (
        outline_adopts_historical_substrate,
        section_adopts_historical_substrate,
    )
    from scripts.historical_substrate_contract import validate_historical_substrate
    from scripts.substrate_preflight import require_canonical_section_state
except ModuleNotFoundError:  # pragma: no cover
    import context_packet_legacy as _legacy
    from context_packet_legacy import *  # type: ignore # noqa: F401,F403
    from historical_substrate_adoption import (
        outline_adopts_historical_substrate,
        section_adopts_historical_substrate,
    )
    from historical_substrate_contract import validate_historical_substrate
    from substrate_preflight import require_canonical_section_state


_ORIGINAL_LOAD_REGISTRY = _legacy.load_registry
_ORIGINAL_REVIEW_INPUTS = list(_legacy.CANONICAL_REVIEW_REQUIRED_INPUTS)

COMPAT_DIRECT_DRAFT_INPUTS = [
    "03_sections/{section}/section.json",
    "03_sections/{section}/narration-pack.json",
    "03_sections/{section}/continuity-in.md",
]
COMPAT_DIRECT_REVISE_INPUTS = [
    "02_outline/outline.json",
    "03_sections/{section}/section.json",
    "03_sections/{section}/narration-pack.json",
    "03_sections/{section}/draft.md",
    "03_sections/{section}/handoff.md",
    "03_sections/{section}/review.md",
    "03_sections/{section}/change-request.md",
]
ADOPTED_REVIEW_INPUTS = [
    "02_outline/outline.json",
    "03_sections/{section}/section.json",
    "03_sections/{section}/historical-substrate.json",
    "03_sections/{section}/narration-pack.json",
    "03_sections/{section}/draft.md",
    "03_sections/{section}/handoff.md",
]

CANONICAL_SECONDARY_GUIDANCE = (
    "Task context includes a bounded evidence capability. Historical Substrate is the primary history model.\n"
    "Use evidence only after choosing a telling from that model, to verify, sharpen, or qualify a specific detail.\n"
    "Do not survey evidence to discover the story route or to decide what historical reality exists to tell.\n"
    "Every capability call is audit-logged; new claims or causal generalizations remain evidence-authority work."
)


def _require_product_complete_outline_substrate(product_dir: Path) -> None:
    product_dir = product_dir.resolve()
    substrate_path = product_dir / "01_research" / "historical-substrate.json"
    claims_path = product_dir / "01_research" / "claim-ledger.json"
    sources_path = product_dir / "01_research" / "source-index.json"
    if not substrate_path.is_file():
        raise ValueError("Adopted outline creation requires 01_research/historical-substrate.json")
    errors = validate_historical_substrate(
        _legacy.read_json_local(substrate_path),
        _legacy.read_json_local(claims_path),
        _legacy.read_json_local(sources_path),
        require_product_complete=True,
    )
    if errors:
        raise ValueError("Outline Historical Substrate preflight failed: " + "; ".join(errors))


def _architecture_flags(
    product_dir: Path, operation: str, section: str | None
) -> tuple[bool, bool]:
    product_dir = product_dir.resolve()
    outline_path = product_dir / "02_outline" / "outline.json"
    product_path = product_dir / "product.json"
    outline = _legacy.read_json_local(outline_path) if outline_path.is_file() else {}
    product = _legacy.read_json_local(product_path) if product_path.is_file() else {}
    outline_adopted = outline_adopts_historical_substrate(
        product_dir, product=product, outline=outline
    )
    section_adopted = bool(
        section
        and operation in {"draft_section", "review_section", "revise_section"}
        and section_adopts_historical_substrate(
            product_dir, section, product=product, outline=outline
        )
    )
    return outline_adopted, section_adopted


def _adapt_registry(
    operation: str,
    *,
    outline_adopted: bool,
    section_adopted: bool,
) -> dict[str, Any]:
    registry = deepcopy(_ORIGINAL_LOAD_REGISTRY())
    spec = registry.get(operation)
    if not isinstance(spec, dict):
        return registry

    if operation == "outline" and not outline_adopted:
        spec["required_inputs"] = [
            item for item in spec.get("required_inputs", [])
            if item != "01_research/historical-substrate.json"
        ]

    if operation == "draft_section" and not section_adopted:
        spec["required_inputs"] = list(COMPAT_DIRECT_DRAFT_INPUTS)
    elif operation == "revise_section" and not section_adopted:
        spec["required_inputs"] = list(COMPAT_DIRECT_REVISE_INPUTS)

    if section_adopted and operation == "review_section":
        # Channel identity is upstream product context; the evaluation standard +
        # production gate + operation contract are sufficient here and keep the
        # canonical evaluator inside its existing prompt budget.
        spec["instruction_files"] = [
            "system/standards/outcome-evaluation.md",
            "system/standards/section-quality-gate.md",
            "system/operations/review-section.md",
        ]

    # Adopted evidence semantics are inserted by this architecture layer before
    # final context-budget validation. Removing evidence_access here prevents the
    # legacy compiler from emitting its evidence-as-story-discovery paragraph.
    if section_adopted and operation in {"draft_section", "review_section", "revise_section"}:
        spec.pop("evidence_access", None)
    return registry


def _evidence_packet(
    product_dir: Path,
    operation: str,
    task_id: str,
    section: str,
) -> dict[str, Any] | None:
    original_spec = _ORIGINAL_LOAD_REGISTRY().get(operation, {})
    evidence_access = original_spec.get("evidence_access")
    if not isinstance(evidence_access, dict):
        return None
    packet: dict[str, Any] = {
        "kind": evidence_access["kind"],
        "adapter": evidence_access["adapter"],
        "interface_version": evidence_access["interface_version"],
        "capabilities": list(evidence_access["capabilities"]),
        "trace_path": f"tasks/{task_id}/evidence-trace.jsonl",
    }
    if evidence_access.get("required_before_submit"):
        packet["required_before_submit"] = list(evidence_access["required_before_submit"])

    sec_dir = product_dir.resolve() / "03_sections" / section
    materials = sec_dir / "materials.json"
    snapshot = sec_dir / "material-snapshot.json"
    if materials.is_file():
        if not snapshot.is_file() or _legacy.sha256(materials) != _legacy.read_json_local(snapshot).get("materials_sha256"):
            value = _legacy.read_json_local(materials)
            _legacy.write_json(
                snapshot,
                {
                    "schema_version": 1,
                    "section": section,
                    "created_at": _legacy.datetime.now(_legacy.timezone.utc).isoformat(),
                    "materials_sha256": _legacy.sha256(materials),
                    "materials": value.get("materials", []) if isinstance(value, dict) else value,
                },
            )
    if snapshot.is_file():
        packet["material_snapshot_sha256"] = _legacy.sha256(snapshot)
    return packet


def _insert_canonical_evidence_guidance(
    text: str, product_dir: Path, task_id: str, evidence: dict[str, Any]
) -> str:
    lines = [
        "# Canonical evidence routing",
        CANONICAL_SECONDARY_GUIDANCE,
        f"Evidence adapter: `python {evidence['adapter']} products/{product_dir.name} {task_id} <capability>`.",
        "Capabilities: " + ", ".join(f"`{item}`" for item in evidence["capabilities"]) + ".",
    ]
    if evidence.get("required_before_submit"):
        lines.append(
            "Submission requirement: call "
            + ", ".join(f"`{item}`" for item in evidence["required_before_submit"])
            + " successfully before submitting this task."
        )
    block = "\n".join(lines) + "\n\n"
    marker = "# BEGIN INSTRUCTION:"
    index = text.find(marker)
    if index < 0:
        return text.rstrip() + "\n\n" + block
    return text[:index] + block + text[index:]


def compile_packet(
    product_dir: Path,
    operation: str,
    task_id: str,
    section: str | None = None,
    unit: str | None = None,
    execution_runtime: str | None = None,
) -> tuple[dict[str, Any], str]:
    product_dir = product_dir.resolve()
    outline_adopted, section_adopted = _architecture_flags(
        product_dir, operation, section
    )

    if operation == "outline" and outline_adopted:
        _require_product_complete_outline_substrate(product_dir)
    if section_adopted and section:
        require_canonical_section_state(product_dir, section)

    adapted_registry = _adapt_registry(
        operation,
        outline_adopted=outline_adopted,
        section_adopted=section_adopted,
    )
    old_loader = _legacy.load_registry
    old_review_inputs = list(_legacy.CANONICAL_REVIEW_REQUIRED_INPUTS)
    _legacy.load_registry = lambda: adapted_registry
    _legacy.CANONICAL_REVIEW_REQUIRED_INPUTS = (
        list(ADOPTED_REVIEW_INPUTS) if section_adopted else list(_ORIGINAL_REVIEW_INPUTS)
    )
    try:
        packet, text = _legacy.compile_packet(
            product_dir,
            operation,
            task_id,
            section=section,
            unit=unit,
            execution_runtime=execution_runtime,
        )
    finally:
        _legacy.load_registry = old_loader
        _legacy.CANONICAL_REVIEW_REQUIRED_INPUTS = old_review_inputs

    if not section_adopted or not section:
        return packet, text

    evidence = _evidence_packet(product_dir, operation, task_id, section)
    if evidence is not None:
        text = _insert_canonical_evidence_guidance(text, product_dir, task_id, evidence)
        packet["evidence_access"] = evidence

    section_substrate = product_dir / "03_sections" / section / "historical-substrate.json"
    state = _legacy.read_json_local(product_dir / "03_sections" / section / "section.json")
    packet["historical_substrate"] = {
        "contract_version": state.get("historical_substrate_contract_version"),
        "section_projection_path": f"03_sections/{section}/historical-substrate.json",
        "section_projection_sha256": _legacy.sha256(section_substrate),
        "architecture_authority": state.get("architecture_authority"),
    }

    tokens = _legacy.estimate_tokens(text)
    budget = int(packet["max_context_tokens"])
    if tokens > budget:
        raise ValueError(
            f"Context packet estimate {tokens} exceeds budget {budget}; compact canonical upstream context."
        )
    packet["context_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    packet["estimated_context_tokens"] = tokens
    return packet, text


def main() -> int:
    _legacy.compile_packet = compile_packet
    return _legacy.main()


if __name__ == "__main__":
    raise SystemExit(main())
