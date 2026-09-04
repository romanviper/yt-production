#!/usr/bin/env python3
"""Build three immutable, isolated P01 Writer contexts for the diagnostic run."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
P01 = ROOT.parents[1]
REPO = ROOT.parents[5]
BASELINE = P01 / "probes" / "hsub-clean-01" / "writer-context.md"
MATERIALS = P01 / "materials.json"

TARGET = {"min": 450, "max": 650}
COMMON = {
    "section": "P01",
    "language": "vi",
    "target_words": TARGET,
    "form": "one contiguous passage from a larger unfinished section",
    "completion_rule": "Do not summarize or complete the whole P01 movement.",
    "creative_authority": "The Writer owns the telling, composition, exposition, reconstruction and language.",
    "forbidden_prescriptions": [
        "required scene", "required protagonist", "required hook", "fixed beats",
        "required reveal order", "required climax", "sensory quota", "stylistic imitation",
    ],
    "truth_rule": "Stay inside the supplied historical authority. Do not invent named actors, attributed quotations, chronology, measurements, institutions, motives, dialogue, private thoughts or causal conclusions.",
    "metadata_rule": "Evidence and boundary metadata constrain the prose; they do not need to be narrated.",
}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_variant(name: str, payload: dict) -> dict:
    text = "# ISOLATED WRITER TASK\n\n" + json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path = ROOT / f"writer-{name}-context.md"
    path.write_text(text, encoding="utf-8")
    return {"variant": name.upper(), "context_path": str(path.relative_to(REPO)), "context_sha256": sha(text)}


def rich_payload() -> dict:
    source = json.loads(MATERIALS.read_text(encoding="utf-8"))
    keep = {
        "id", "kind", "label", "actor", "time", "place", "physical_description",
        "measurement", "object_or_trace", "source_relation", "source_refs",
        "limitations", "representativeness", "epistemic_layers",
    }
    return {
        "role": "primary rich historical material; choose freely and do not cover exhaustively",
        "records": [
            {key: value for key, value in item.items() if key in keep}
            for item in source.get("materials", [])
            if isinstance(item, dict)
        ],
    }


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    rich = rich_payload()
    baseline_text = BASELINE.read_text(encoding="utf-8")
    marker = "# CANONICAL P01 WRITER CONTEXT\n\n"
    if marker not in baseline_text:
        raise SystemExit("canonical baseline context marker is missing")
    canonical = baseline_text.split(marker, 1)[1]

    a = {
        **COMMON,
        "experiment": "P01-THREE-WRITER-A",
        "variant": "rich historical material, direct draft",
        "instruction": "Draft directly from the material below. Choose what to use; do not first produce a plan or composition artifact.",
        "historical_material": rich,
    }
    b = {
        **COMMON,
        "experiment": "P01-THREE-WRITER-B",
        "variant": "canonical Historical Substrate control",
        "instruction": "Draft directly from the canonical Writer context below.",
        "canonical_writer_context": canonical,
    }
    c = {
        **COMMON,
        "experiment": "P01-THREE-WRITER-C",
        "variant": "rich historical material plus Writer-owned composition",
        "instruction": (
            "Before drafting, privately choose one bounded local historical thread and decide where this passage begins and deliberately stops. "
            "Save only a brief high-level composition decision record containing chosen_thread, begins_at, stops_before, intended_material_ids, and intentionally_unused_material_ids. "
            "Do not save detailed reasoning. Then draft from your own decision."
        ),
        "historical_material": rich,
    }

    variants = [write_variant("a", a), write_variant("b", b), write_variant("c", c)]
    manifest = {
        "schema_version": 1,
        "experiment": "P01-THREE-CLEAN-WRITER-DIAGNOSTIC",
        "architecture_frozen": True,
        "model_configuration": "gpt-5.6-sol / high",
        "shared_target_words": TARGET,
        "a_c_rich_material_sha256": sha(json.dumps(rich, ensure_ascii=False, sort_keys=True)),
        "variants": variants,
        "outputs": {
            "A": "writer-a-rich-material.md",
            "B": "writer-b-substrate.md",
            "C": "writer-c-composition.md",
            "C_composition_record": "writer-c-composition-decision.json",
        },
    }
    (ROOT / "execution-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
