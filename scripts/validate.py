#!/usr/bin/env python3
"""Historical-Substrate-aware product validation with legacy compatibility."""

from __future__ import annotations

from pathlib import Path

try:
    import scripts.validate_legacy as _legacy
    from scripts.validate_legacy import *  # noqa: F401,F403
    from scripts.historical_substrate_adoption import (
        outline_adopts_historical_substrate,
        section_adopts_historical_substrate,
    )
    from scripts.historical_substrate_contract import validate_historical_substrate, validate_section_binding
    from scripts.section_overlay_contract import validate_section_overlay, resolve_section_spec
    from scripts.substrate_preflight import verify_canonical_section_state
except ModuleNotFoundError:  # pragma: no cover
    import validate_legacy as _legacy
    from validate_legacy import *  # type: ignore # noqa: F401,F403
    from historical_substrate_adoption import outline_adopts_historical_substrate, section_adopts_historical_substrate
    from historical_substrate_contract import validate_historical_substrate, validate_section_binding
    from section_overlay_contract import validate_section_overlay, resolve_section_spec
    from substrate_preflight import verify_canonical_section_state


def _append(issues: list[Issue], location: Path | str, messages: list[str]) -> None:
    for message in messages:
        issues.append(Issue("ERROR", str(location), message))


def validate_product(product_dir: Path) -> list[Issue]:
    product_dir = product_dir.resolve()
    issues = list(_legacy.validate_product(product_dir))

    substrate_path = product_dir / "01_research" / "historical-substrate.json"
    claims_path = product_dir / "01_research" / "claim-ledger.json"
    sources_path = product_dir / "01_research" / "source-index.json"
    outline_path = product_dir / "02_outline" / "outline.json"
    product_path = product_dir / "product.json"
    if not outline_path.is_file() or not product_path.is_file():
        return issues

    outline = read_json(outline_path)
    product = read_json(product_path)
    product_adopted = outline_adopts_historical_substrate(
        product_dir, product=product, outline=outline
    )

    # A substrate artifact may exist before adoption; validate its intrinsic
    # authority if present, but do not infer lifecycle adoption from presence.
    substrate = None
    claims = None
    sources = None
    if substrate_path.is_file() and claims_path.is_file() and sources_path.is_file():
        substrate = read_json(substrate_path)
        claims = read_json(claims_path)
        sources = read_json(sources_path)
        _append(issues, substrate_path, validate_historical_substrate(substrate, claims, sources))
    elif product_adopted:
        issues.append(Issue("ERROR", str(substrate_path), "Adopted product is missing Historical Substrate authority."))

    overlays_dir = product_dir / "02_outline" / "section-overlays"
    if overlays_dir.is_dir():
        for overlay_path in sorted(overlays_dir.glob("P??.json")):
            overlay = read_json(overlay_path)
            _append(issues, overlay_path, validate_section_overlay(overlay, outline, outline_path))
            section = overlay.get("section")
            if not isinstance(section, str):
                continue
            adopted = section_adopts_historical_substrate(
                product_dir, section, product=product, outline=outline
            )
            if not adopted:
                continue
            if substrate is None:
                issues.append(Issue("ERROR", str(overlay_path), "Adopted section is missing product Historical Substrate authority."))
                continue
            try:
                resolved, _authority = resolve_section_spec(
                    product_dir, section, outline=outline, outline_path=outline_path
                )
            except ValueError as exc:
                issues.append(Issue("ERROR", str(overlay_path), str(exc)))
            else:
                _append(issues, overlay_path, validate_section_binding(resolved, substrate))

    if product_adopted and substrate is not None and claims is not None and sources is not None:
        _append(
            issues,
            substrate_path,
            validate_historical_substrate(substrate, claims, sources, require_product_complete=True),
        )
        for section_spec in outline.get("sections", []):
            if isinstance(section_spec, dict):
                _append(issues, outline_path, validate_section_binding(section_spec, substrate))

    section_root = product_dir / "03_sections"
    if section_root.is_dir():
        for root in sorted(path for path in section_root.iterdir() if path.is_dir() and path.name.startswith("P")):
            if not section_adopts_historical_substrate(
                product_dir, root.name, product=product, outline=outline
            ):
                continue
            state_path = root / "section.json"
            if not state_path.is_file():
                issues.append(Issue("ERROR", str(state_path), "Adopted section is not materialized."))
                continue
            state = read_json(state_path)
            if int(state.get("historical_substrate_contract_version") or 0) != 1:
                issues.append(Issue("ERROR", str(state_path), "historical_substrate_contract_version must be 1"))
            _append(issues, root, verify_canonical_section_state(product_dir, root.name))
    return issues


def main() -> int:
    _legacy.validate_product = validate_product
    return _legacy.main()


if __name__ == "__main__":
    raise SystemExit(main())
