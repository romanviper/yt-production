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
EXPECTED_CANONICAL_CONTEXT_SHA256 = "65992acd578be4c3c72ae31de43cc4ff1231b6c63946fa33d8d3a5f30c7e3084"
EXPECTED_EFFECTIVE_CONTEXT_SHA256 = "338b3b14c425c0907f9920fc8a7240dfbe427f890750fba4ed4c97e83b57140a"


def main() -> int:
    gate = json.loads((PROBE_ROOT / "gate-manifest.json").read_text(encoding="utf-8"))
    contract = json.loads((PROBE_ROOT / "probe-contract.json").read_text(encoding="utf-8"))
    if gate.get("status") != "AUTHORIZED_TO_RUN_FRESH_P01_PROBE":
        raise SystemExit("probe gate is not authorized")

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
        canonical_sha = hashlib.sha256(canonical_context.encode("utf-8")).hexdigest()
        if canonical_sha != EXPECTED_CANONICAL_CONTEXT_SHA256:
            raise SystemExit(
                f"canonical Writer context changed: {canonical_sha} != {EXPECTED_CANONICAL_CONTEXT_SHA256}"
            )

        effective_context = (
            "# TASK-LOCAL EXPERIMENT BOUND\n\n"
            + json.dumps(contract, ensure_ascii=False, indent=2)
            + "\n\n# CANONICAL P01 WRITER CONTEXT\n\n"
            + canonical_context
        )
        effective_sha = hashlib.sha256(effective_context.encode("utf-8")).hexdigest()
        if effective_sha != EXPECTED_EFFECTIVE_CONTEXT_SHA256:
            raise SystemExit(
                f"effective probe context changed: {effective_sha} != {EXPECTED_EFFECTIVE_CONTEXT_SHA256}"
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

    print("AUTHORIZED_TO_RUN_FRESH_P01_PROBE")
    print(f"writer-context.md sha256={EXPECTED_EFFECTIVE_CONTEXT_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
