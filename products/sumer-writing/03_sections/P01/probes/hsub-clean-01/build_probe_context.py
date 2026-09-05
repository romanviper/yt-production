#!/usr/bin/env python3
"""Build the frozen P01 Historical-Substrate probe context without mutating product state."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[6]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.context_packet import compile_packet
from scripts.materialize_sections import materialize
from scripts.substrate_preflight import verify_canonical_section_state


SOURCE_PRODUCT = REPO_ROOT / "products" / "sumer-writing"
PROBE_ROOT = SOURCE_PRODUCT / "03_sections" / "P01" / "probes" / "hsub-clean-01"
TASK_ID = "T9900-draft-section-P01"
READY_STATUS = "READY_FOR_FRESH_WRITER_EXECUTION"


def _required_manifest_value(gate: dict, *path: str) -> str:
    value: object = gate
    for key in path:
        if not isinstance(value, dict) or key not in value:
            raise SystemExit("gate manifest is missing required field: " + ".".join(path))
        value = value[key]
    if not isinstance(value, str) or not value:
        raise SystemExit("gate manifest field is not a non-empty string: " + ".".join(path))
    return value


def main() -> int:
    gate = json.loads((PROBE_ROOT / "gate-manifest.json").read_text(encoding="utf-8"))
    contract = json.loads((PROBE_ROOT / "probe-contract.json").read_text(encoding="utf-8"))
    if gate.get("status") != READY_STATUS:
        raise SystemExit(
            f"probe gate is not ready: {gate.get('status')!r}; expected {READY_STATUS!r}"
        )
    rematerialization = gate.get("rematerialization", {})
    if not isinstance(rematerialization, dict) or not rematerialization.get("canonical_artifacts_applied"):
        raise SystemExit("probe gate does not attest that canonical rematerialized P01 artifacts were applied")

    expected_canonical_sha = _required_manifest_value(
        gate, "writer_packet", "canonical_context_sha256"
    )
    expected_effective_sha = _required_manifest_value(
        gate, "writer_packet", "effective_probe_context_sha256"
    )
    expected_projection_sha = _required_manifest_value(
        gate, "historical_substrate", "section_projection_sha256"
    )

    with tempfile.TemporaryDirectory() as temp:
        product = Path(temp) / "sumer-writing"
        shutil.copytree(SOURCE_PRODUCT, product)
        materialize(product, section="P01")
        errors = verify_canonical_section_state(product, "P01")
        if errors:
            raise SystemExit("P01 critical preflight failed: " + "; ".join(errors))

        packet, canonical_context = compile_packet(
            product,
            "draft_section",
            TASK_ID,
            section="P01",
        )
        projection_sha = packet.get("historical_substrate", {}).get("section_projection_sha256")
        if projection_sha != expected_projection_sha:
            raise SystemExit(
                f"Writer substrate projection changed: {projection_sha} != {expected_projection_sha}"
            )

        canonical_sha = hashlib.sha256(canonical_context.encode("utf-8")).hexdigest()
        if canonical_sha != expected_canonical_sha:
            raise SystemExit(
                f"canonical Writer context changed: {canonical_sha} != {expected_canonical_sha}"
            )

        effective_context = (
            "# TASK-LOCAL EXPERIMENT BOUND\n\n"
            + json.dumps(contract, ensure_ascii=False, indent=2)
            + "\n\n# CANONICAL P01 WRITER CONTEXT\n\n"
            + canonical_context
        )
        effective_sha = hashlib.sha256(effective_context.encode("utf-8")).hexdigest()
        if effective_sha != expected_effective_sha:
            raise SystemExit(
                f"effective probe context changed: {effective_sha} != {expected_effective_sha}"
            )

        packet_out = {
            "schema_version": 1,
            "experiment": contract["experiment"],
            "canonical_output": False,
            "canonical_writer_packet": packet,
            "probe_contract": contract,
            "canonical_context_sha256": canonical_sha,
            "effective_context_sha256": effective_sha,
        }
        (PROBE_ROOT / "writer-packet.json").write_text(
            json.dumps(packet_out, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (PROBE_ROOT / "writer-context.md").write_text(effective_context, encoding="utf-8")

    print(READY_STATUS)
    print(f"writer-context.md sha256={expected_effective_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
