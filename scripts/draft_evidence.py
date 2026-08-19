#!/usr/bin/env python3
"""Bounded, audit-logged evidence access for draft/revision tasks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256
except ModuleNotFoundError:  # Direct execution from scripts/
    from common import read_json, sha256


MAX_QUERY_CHARS = 300
MAX_RESULTS = 30
MAX_RECORDED_DETAIL_CHARS = 6000
ALLOWED_OPERATIONS = {"draft_section", "revise_section"}


class EvidenceAccessError(ValueError):
    pass


def _json_hash(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _bounded_int(value: Any, *, default: int, minimum: int, maximum: int, field: str) -> int:
    if value is None:
        return default
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        raise EvidenceAccessError(f"{field} must be an integer from {minimum} to {maximum}")
    return value


class DraftEvidenceBroker:
    """Expose only evidence reachable from the task's approved claim/source scope."""

    def __init__(self, product_dir: Path, task_id: str):
        self.product_dir = product_dir.resolve()
        self.task_id = task_id
        self.task_dir = self.product_dir / "tasks" / task_id
        self.work_path = self.task_dir / "work-order.json"
        self.packet_path = self.task_dir / "packet.json"
        self.work = read_json(self.work_path)
        self.packet = read_json(self.packet_path)
        self._validate_task()

        target = self.work.get("target", {})
        self.section = str(target.get("section") or "")
        self.root = self.product_dir / "03_sections" / self.section
        self.narration_path = self.root / "narration-pack.json"
        self.narration = read_json(self.narration_path)
        self.claim_ledger_path = self.product_dir / "01_research" / "claim-ledger.json"
        self.source_index_path = self.product_dir / "01_research" / "source-index.json"
        self.material_ledger_path = self.product_dir / "01_research" / "material-ledger.json"
        self.claim_ledger = read_json(self.claim_ledger_path)
        self.source_index = read_json(self.source_index_path)
        self.material_ledger = read_json(self.material_ledger_path) if self.material_ledger_path.is_file() else None

        self.allowed_claim_ids, self.allowed_source_ids = self._scope_from_narration()
        self.claims_by_id = {
            item.get("id"): item
            for item in self.claim_ledger.get("claims", [])
            if isinstance(item, dict) and item.get("id")
        }
        self.sources_by_id = {
            item.get("id"): item
            for item in self.source_index.get("sources", [])
            if isinstance(item, dict) and item.get("id")
        }
        self._validate_scope()
        self.trace_path = self.task_dir / "evidence-trace.jsonl"

    def _validate_task(self) -> None:
        if self.work.get("id") != self.task_id or self.packet.get("task_id") != self.task_id:
            raise EvidenceAccessError("task id does not match work-order/packet")
        if self.work.get("operation") != self.packet.get("operation"):
            raise EvidenceAccessError("work-order and packet operation differ")
        if self.work.get("operation") not in ALLOWED_OPERATIONS:
            raise EvidenceAccessError("bounded writer evidence access is limited to draft_section/revise_section")
        if self.work.get("target") != self.packet.get("target"):
            raise EvidenceAccessError("work-order and packet target differ")
        access = self.packet.get("evidence_access")
        if not isinstance(access, dict):
            raise EvidenceAccessError("task packet does not expose bounded evidence access")
        if access.get("kind") != "bounded_claim_sources" or access.get("adapter") != "scripts/draft_evidence.py":
            raise EvidenceAccessError("task packet evidence access contract is invalid")
        expected_trace = f"tasks/{self.task_id}/evidence-trace.jsonl"
        if access.get("trace_path") != expected_trace:
            raise EvidenceAccessError("task packet evidence trace path is invalid")

        records = {
            item.get("path"): item
            for item in self.packet.get("inputs", [])
            if isinstance(item, dict) and item.get("path")
        }
        narration_rel = f"03_sections/{self.work.get('target', {}).get('section')}/narration-pack.json"
        record = records.get(narration_rel)
        narration_path = self.product_dir / narration_rel
        if record is None or not narration_path.is_file() or sha256(narration_path) != record.get("sha256"):
            raise EvidenceAccessError("narration pack is missing or stale relative to task creation")

    def _scope_from_narration(self) -> tuple[list[str], list[str]]:
        if self.narration.get("schema_version") == 4:
            scope = self.narration.get("retrieval_scope")
            if not isinstance(scope, dict):
                raise EvidenceAccessError("direct narration pack is missing retrieval_scope")
            claims = scope.get("claim_ids")
            sources = scope.get("source_ids")
        else:
            claims = [
                item.get("id")
                for field in ["core_claims", "optional_claims"]
                for item in self.narration.get(field, [])
                if isinstance(item, dict) and item.get("id")
            ]
            sources = [
                source_id
                for item in self.narration.get("source_refs", [])
                if isinstance(item, dict)
                for source_id in [item.get("id")]
                if isinstance(source_id, str)
            ]
        if not isinstance(claims, list) or not all(isinstance(item, str) and re.fullmatch(r"CLM-\d{4}", item) for item in claims):
            raise EvidenceAccessError("retrieval claim scope is invalid")
        if not isinstance(sources, list) or not all(isinstance(item, str) and re.fullmatch(r"SRC-\d{4}", item) for item in sources):
            raise EvidenceAccessError("retrieval source scope is invalid")
        return list(dict.fromkeys(claims)), list(dict.fromkeys(sources))

    def _validate_scope(self) -> None:
        missing_claims = [claim_id for claim_id in self.allowed_claim_ids if claim_id not in self.claims_by_id]
        missing_sources = [source_id for source_id in self.allowed_source_ids if source_id not in self.sources_by_id]
        if missing_claims:
            raise EvidenceAccessError("retrieval scope references missing claims: " + ", ".join(missing_claims))
        if missing_sources:
            raise EvidenceAccessError("retrieval scope references missing sources: " + ", ".join(missing_sources))
        reachable_sources = {
            source_id
            for claim_id in self.allowed_claim_ids
            for source_id in self.claims_by_id[claim_id].get("sources", [])
            if isinstance(source_id, str)
        }
        extra = [source_id for source_id in self.allowed_source_ids if source_id not in reachable_sources]
        if extra:
            raise EvidenceAccessError("retrieval source scope exceeds approved claim graph: " + ", ".join(extra))

    def _preserved_details(self, source_id: str) -> list[dict[str, Any]]:
        if not isinstance(self.material_ledger, dict):
            return []
        results = []
        allowed_claims = set(self.allowed_claim_ids)
        for material in self.material_ledger.get("materials", []):
            if not isinstance(material, dict):
                continue
            linked_claims = {item for item in material.get("claim_ids", []) if isinstance(item, str)}
            if linked_claims and not linked_claims.intersection(allowed_claims):
                continue
            matching_refs = [
                ref
                for ref in material.get("source_refs", [])
                if isinstance(ref, dict) and ref.get("source_id") == source_id
            ]
            if not matching_refs:
                continue
            factual = {
                key: value
                for key, value in material.items()
                if key
                not in {
                    "id",
                    "claim_ids",
                    "source_refs",
                    "provenance",
                    "narratability",
                    "what_audience_follows",
                    "representativeness",
                }
                and value not in (None, "", [])
            }
            results.append(
                {
                    "material_id": material.get("id"),
                    "locators": [loc for ref in matching_refs for loc in ref.get("locators", [])],
                    "preserved_detail": factual,
                    "limitations": material.get("limitations", []),
                    "authority": "optional_evidence_preservation_only",
                }
            )
        return results

    def _append_trace(self, capability: str, arguments: dict[str, Any], response: Any, error: str | None = None) -> None:
        record = {
            "schema_version": 1,
            "at": datetime.now(timezone.utc).isoformat(),
            "task_id": self.task_id,
            "section": self.section,
            "capability": capability,
            "arguments": arguments,
            "response_sha256": _json_hash(response) if response is not None else None,
            "error": error,
            "truth_ceiling_unchanged": True,
        }
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        with self.trace_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    def call(self, capability: str, arguments: dict[str, Any] | None = None) -> Any:
        arguments = arguments or {}
        handlers = {
            "scope": self.scope,
            "claims": self.claims,
            "sources": self.sources,
            "source": self.source,
            "search": self.search,
            "record": self.record,
        }
        handler = handlers.get(capability)
        if handler is None:
            raise EvidenceAccessError(f"unknown evidence capability: {capability}")
        try:
            response = handler(arguments)
        except Exception as exc:
            self._append_trace(capability, arguments, None, str(exc))
            raise
        self._append_trace(capability, arguments, response, None)
        return response

    def scope(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise EvidenceAccessError("scope takes no arguments")
        return {
            "section": self.section,
            "claim_ids": self.allowed_claim_ids,
            "source_ids": self.allowed_source_ids,
            "rule": (
                "You may increase source-level factual resolution inside this graph. "
                "A new claim, causal conclusion, thesis, contradiction or generalization requires research/evidence authority."
            ),
        }

    def claims(self, arguments: dict[str, Any]) -> dict[str, Any]:
        ids = arguments.get("ids", self.allowed_claim_ids)
        if set(arguments) - {"ids"}:
            raise EvidenceAccessError("claims accepts only ids")
        if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids):
            raise EvidenceAccessError("ids must be a list")
        outside = [item for item in ids if item not in self.allowed_claim_ids]
        if outside:
            raise EvidenceAccessError("claim is outside approved section scope: " + ", ".join(outside))
        return {"claims": [self.claims_by_id[item] for item in ids]}

    def sources(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise EvidenceAccessError("sources takes no arguments")
        return {
            "sources": [self.sources_by_id[item] for item in self.allowed_source_ids],
            "rule": "Only these reviewed sources may be opened for this task without expanding evidence territory.",
        }

    def source(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if set(arguments) != {"id"}:
            raise EvidenceAccessError("source requires exactly id")
        source_id = arguments.get("id")
        if source_id not in self.allowed_source_ids:
            raise EvidenceAccessError(f"source {source_id!r} is outside approved section scope")
        return {
            "source": self.sources_by_id[source_id],
            "preserved_details": self._preserved_details(str(source_id)),
            "retrieval_instruction": (
                "Read only the approved source URL/locators returned here. If external reading adds factual detail used in drafting, "
                "call record with this source id and one approved parent locator so the evidence access remains auditable."
            ),
        }

    def search(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if set(arguments) - {"query", "limit"}:
            raise EvidenceAccessError("search accepts only query and limit")
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip() or len(query) > MAX_QUERY_CHARS:
            raise EvidenceAccessError(f"query must be 1-{MAX_QUERY_CHARS} characters")
        limit = _bounded_int(arguments.get("limit"), default=10, minimum=1, maximum=MAX_RESULTS, field="limit")
        terms = re.findall(r"[\wÀ-ỹ]+", query.casefold(), flags=re.UNICODE)
        ranked: list[tuple[int, str, dict[str, Any]]] = []
        for claim_id in self.allowed_claim_ids:
            item = self.claims_by_id[claim_id]
            haystack = json.dumps(item, ensure_ascii=False, sort_keys=True).casefold()
            score = sum(haystack.count(term) for term in terms)
            if score:
                ranked.append((score, f"claim:{claim_id}", {"kind": "claim", "record": item}))
        for source_id in self.allowed_source_ids:
            item = self.sources_by_id[source_id]
            source_payload = {
                "source": item,
                "preserved_details": self._preserved_details(source_id),
            }
            haystack = json.dumps(source_payload, ensure_ascii=False, sort_keys=True).casefold()
            score = sum(haystack.count(term) for term in terms)
            if score:
                ranked.append((score, f"source:{source_id}", {"kind": "source", "record": source_payload}))
        ranked.sort(key=lambda row: (-row[0], row[1]))
        return {"query": query, "results": [row[2] for row in ranked[:limit]]}

    def record(self, arguments: dict[str, Any]) -> dict[str, Any]:
        required = {"source_id", "parent_locator", "locator", "detail"}
        if set(arguments) != required:
            raise EvidenceAccessError("record requires exactly source_id, parent_locator, locator and detail")
        source_id = arguments.get("source_id")
        if source_id not in self.allowed_source_ids:
            raise EvidenceAccessError(f"source {source_id!r} is outside approved section scope")
        source = self.sources_by_id[str(source_id)]
        parent_locator = arguments.get("parent_locator")
        approved_locators = source.get("locators", [])
        if parent_locator not in approved_locators:
            raise EvidenceAccessError("parent_locator must exactly match a reviewed locator on the approved source")
        locator = arguments.get("locator")
        detail = arguments.get("detail")
        if not isinstance(locator, str) or not locator.strip() or len(locator) > 1000:
            raise EvidenceAccessError("locator must be non-empty text up to 1000 characters")
        if not isinstance(detail, str) or not detail.strip() or len(detail) > MAX_RECORDED_DETAIL_CHARS:
            raise EvidenceAccessError(f"detail must be non-empty text up to {MAX_RECORDED_DETAIL_CHARS} characters")
        return {
            "status": "recorded_source_detail",
            "source_id": source_id,
            "parent_locator": parent_locator,
            "locator": locator.strip(),
            "detail": detail.strip(),
            "authority": "source_level_detail_not_new_claim",
            "truth_ceiling_unchanged": True,
            "rule": "If this detail changes interpretation/generalization rather than merely increasing factual resolution, route it to research authority.",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("task_id")
    sub = parser.add_subparsers(dest="capability", required=True)
    sub.add_parser("scope")

    claims = sub.add_parser("claims")
    claims.add_argument("--id", dest="ids", action="append")

    sub.add_parser("sources")
    source = sub.add_parser("source")
    source.add_argument("--id", required=True)

    search = sub.add_parser("search")
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=10)

    record = sub.add_parser("record")
    record.add_argument("--source-id", required=True)
    record.add_argument("--parent-locator", required=True)
    record.add_argument("--locator", required=True)
    record.add_argument("--detail", required=True)

    args = parser.parse_args()
    broker = DraftEvidenceBroker(args.product, args.task_id)
    arguments: dict[str, Any]
    if args.capability == "claims":
        arguments = {} if args.ids is None else {"ids": args.ids}
    elif args.capability == "source":
        arguments = {"id": args.id}
    elif args.capability == "search":
        arguments = {"query": args.query, "limit": args.limit}
    elif args.capability == "record":
        arguments = {
            "source_id": args.source_id,
            "parent_locator": args.parent_locator,
            "locator": args.locator,
            "detail": args.detail,
        }
    else:
        arguments = {}
    try:
        result = broker.call(args.capability, arguments)
    except (EvidenceAccessError, FileNotFoundError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
