#!/usr/bin/env python3
"""Historical-Substrate-aware product validation with legacy compatibility."""

from __future__ import annotations

from pathlib import Path

try:
    import scripts.validate_legacy as _legacy
    from scripts.validate_legacy import *  # noqa: F401,F403
    from scripts.historical_substrate_contract import (
        validate_historical_substrate,
        validate_section_binding,
    )
    from scripts.section_overlay_contract import validate_section_overlay, resolve_section_spec
    from scripts.substrate_preflight import verify_canonical_section_state
except ModuleNotFoundError:  # pragma: no cover
    import validate_legacy as _legacy
    from validate_legacy import *  # type: ignore # noqa: F401,F403
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
    if not substrate_path.is_file():
        return issues

    claims_path = product_dir / "01_research" / "claim-ledger.json"
    sources_path = product_dir / "01_research" / "source-index.json"
    outline_path = product_dir / "02_outline" / "outline.json"
    if not claims_path.is_file() or not sources_path.is_file() or not outline_path.is_file():
        return issues

    substrate = read_json(substrate_path)
    claims = read_json(claims_path)
    sources = read_json(sources_path)
    outline = read_json(outline_path)
    _append(
        issues,
        substrate_path,
        validate_historical_substrate(substrate, claims, sources),
    )

    overlays_dir = product_dir / "02_outline" / "section-overlays"
    if overlays_dir.is_dir():
        for overlay_path in sorted(overlays_dir.glob("P??.json")):
            overlay = read_json(overlay_path)
            _append(
                issues,
                overlay_path,
                validate_section_overlay(overlay, outline, outline_path),
            )
            section = overlay.get("section")
            if isinstance(section, str):
                try:
                    resolved, _authority = resolve_section_spec(
                        product_dir,
                        section,
                        outline=outline,
                        outline_path=outline_path,
                    )
                except ValueError as exc:
                    issues.append(Issue("ERROR", str(overlay_path), str(exc)))
                else:
                    _append(
                        issues,
                        overlay_path,
                        validate_section_binding(resolved, substrate),
                    )

    architecture = outline.get("script_architecture", {}) if isinstance(outline, dict) else {}
    if isinstance(architecture, dict) and architecture.get("historical_substrate_contract_version") == 1:
        _append(
            issues,
            substrate_path,
            validate_historical_substrate(
                substrate,
                claims,
                sources,
                require_product_complete=True,
            ),
        )
        for section_spec in outline.get("sections", []):
            if isinstance(section_spec, dict):
                _append(
                    issues,
                    outline_path,
                    validate_section_binding(section_spec, substrate),
                )

    section_root = product_dir / "03_sections"
    if section_root.is_dir():
        for root in sorted(path for path in section_root.iterdir() if path.is_dir() and path.name.startswith("P")):
            state_path = root / "section.json"
            if not state_path.is_file():
                continue
            state = read_json(state_path)
            contract_version = int(state.get("historical_substrate_contract_version") or 0)
            if contract_version < 1:
                continue
            if contract_version != 1:
                issues.append(
                    Issue(
                        "ERROR",
                        str(state_path),
                        "historical_substrate_contract_version must be 1",
                    )
                )
            _append(
                issues,
                root,
                verify_canonical_section_state(product_dir, root.name),
            )
    return issues


def main() -> int:
    _legacy.validate_product = validate_product
    return _legacy.main()


if __name__ == "__main__":
    raise SystemExit(main())
