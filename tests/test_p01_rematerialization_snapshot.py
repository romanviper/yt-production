from __future__ import annotations

import base64
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.materialize_sections import materialize


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PRODUCT = REPO_ROOT / "products" / "sumer-writing"
OUTPUTS = [
    "03_sections/P01/section.json",
    "03_sections/P01/brief.md",
    "03_sections/P01/evidence-pack.json",
    "03_sections/P01/historical-substrate.json",
    "03_sections/P01/narration-pack.json",
    "03_sections/P01/continuity-in.md",
]


class P01CanonicalRematerializationSnapshot(unittest.TestCase):
    def test_rematerialize_p01_and_report_exact_diff(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            product = Path(temp) / "sumer-writing"
            shutil.copytree(SOURCE_PRODUCT, product)
            created = materialize(product, section="P01")
            self.assertEqual(6, len(created))

            changed: list[str] = []
            for rel in OUTPUTS:
                source_path = SOURCE_PRODUCT / rel
                materialized_path = product / rel
                self.assertTrue(materialized_path.is_file(), rel)
                source_bytes = source_path.read_bytes() if source_path.is_file() else b""
                output_bytes = materialized_path.read_bytes()
                if source_bytes != output_bytes:
                    changed.append(rel)
                    print(
                        "P01_REMATERIALIZED_FILE="
                        + json.dumps(
                            {
                                "path": rel,
                                "content_b64": base64.b64encode(output_bytes).decode("ascii"),
                            },
                            ensure_ascii=False,
                            sort_keys=True,
                        )
                    )

            print(
                "P01_REMATERIALIZE_SUMMARY="
                + json.dumps(
                    {
                        "status": "REMATERIALIZED",
                        "section": "P01",
                        "artifact_count": len(OUTPUTS),
                        "changed": changed,
                        "byte_identical_to_branch": not changed,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )


if __name__ == "__main__":
    unittest.main()
