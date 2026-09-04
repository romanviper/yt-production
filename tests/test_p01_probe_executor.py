from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROBE_ROOT = REPO_ROOT / "products" / "sumer-writing" / "03_sections" / "P01" / "probes" / "hsub-clean-01"
EXPECTED_EFFECTIVE_SHA256 = "338b3b14c425c0907f9920fc8a7240dfbe427f890750fba4ed4c97e83b57140a"
EXPECTED_CANONICAL_SHA256 = "65992acd578be4c3c72ae31de43cc4ff1231b6c63946fa33d8d3a5f30c7e3084"


class P01ProbeExecutorTest(unittest.TestCase):
    def test_executor_reproduces_the_gated_writer_context(self) -> None:
        context_path = PROBE_ROOT / "writer-context.md"
        packet_path = PROBE_ROOT / "writer-packet.json"
        try:
            result = subprocess.run(
                [sys.executable, str(PROBE_ROOT / "build_probe_context.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("AUTHORIZED_TO_RUN_FRESH_P01_PROBE", result.stdout)
            context = context_path.read_text(encoding="utf-8")
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            self.assertEqual(
                EXPECTED_EFFECTIVE_SHA256,
                hashlib.sha256(context.encode("utf-8")).hexdigest(),
            )
            self.assertEqual(EXPECTED_EFFECTIVE_SHA256, packet["effective_context_sha256"])
            self.assertEqual(EXPECTED_CANONICAL_SHA256, packet["canonical_context_sha256"])
            self.assertEqual(False, packet["canonical_output"])
            self.assertEqual({"min": 450, "max": 650}, packet["probe_contract"]["target_words"])
        finally:
            context_path.unlink(missing_ok=True)
            packet_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
