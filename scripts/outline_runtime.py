#!/usr/bin/env python3
"""Bounded DeepSeek Harness runtime adapter for outline tasks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
    from scripts.context_packet import DSH_OUTLINE_CAPABILITIES
    from scripts.operator_brief import validate_brief_file
    from scripts.task import submit_task, validate_output_contract, verify_task
    from scripts.validate import validate_product
except ModuleNotFoundError:  # Direct execution: python scripts/outline_runtime.py
    from common import read_json, sha256, write_json
    from context_packet import DSH_OUTLINE_CAPABILITIES
    from operator_brief import validate_brief_file
    from task import submit_task, validate_output_contract, verify_task
    from validate import validate_product


INTERFACE_VERSION = 1
SERVER_NAME = "yt_outline"
TESTED_DSH_VERSION = "0.1.0-rc.5"
MAX_QUERY_CHARS = 200
MAX_WRITE_BYTES = {
    "02_outline/outline.json": 250_000,
    "02_outline/story-bible.md": 120_000,
    "02_outline/voice-profile.md": 40_000,
}

# The shipped DSH headless profile otherwise exposes broad filesystem, shell,
# web, code, subagent and workflow surfaces. The POC fails closed by disabling
# every such model-facing row and then inserting exactly one scoped MCP broker.
DISABLED_DSH_ROWS = [
    "session-title-llm",
    "tool-bash",
    "tool-pwsh",
    "tool-jobs",
    "tool-fs",
    "tool-fs-search",
    "agent-instructions",
    "skill-filesystem",
    "tool-skill",
    "plan-mode",
    "goal",
    "goal-round-driver",
    "command-goal",
    "subagent",
    "subagent-spawn-in-process",
    "subagent-fork-in-process",
    "tool-subagent-control",
    "tool-subagent-list-agents",
    "tool-subagent",
    "tool-subagent-fork",
    "tool-subagent-report",
    "workflow-worker-thread",
    "tool-workflow",
    "tool-todo",
    "tool-goal",
    "tool-ralph",
    "tool-str-replace-editor",
    "web",
    "web-search-deepseek",
    "tool-web",
    "code-runtime",
]


class OutlineRuntimeError(ValueError):
    """Fail-closed runtime boundary error."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def json_digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _bounded_int(value: Any, *, default: int, minimum: int, maximum: int, field: str) -> int:
    if value is None:
        return default
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        raise OutlineRuntimeError(f"{field} must be an integer between {minimum} and {maximum}")
    return value


class OutlineContextBroker:
    """Expose only task-declared outline context and writes, with a reconstructable trace."""

    def __init__(self, product_dir: Path, task_id: str):
        self.product_dir = product_dir.resolve()
        self.task_id = task_id
        self.task_dir = self.product_dir / "tasks" / task_id
        self.work_path = self.task_dir / "work-order.json"
        self.packet_path = self.task_dir / "packet.json"
        self.context_path = self.task_dir / "context.md"
        self.work = read_json(self.work_path)
        self.packet = read_json(self.packet_path)

        runtime = self.packet.get("execution_runtime", {})
        if self.work.get("operation") != "outline" or self.packet.get("operation") != "outline":
            raise OutlineRuntimeError("DeepSeek Harness broker accepts outline tasks only")
        if runtime.get("kind") != "dsh" or runtime.get("interface_version") != INTERFACE_VERSION:
            raise OutlineRuntimeError("Task is not compiled for the supported DeepSeek Harness interface")
        if runtime.get("capabilities") != DSH_OUTLINE_CAPABILITIES:
            raise OutlineRuntimeError("Task capability manifest differs from the supported outline interface")
        verification = verify_task(self.product_dir, self.task_id)
        if verification:
            raise OutlineRuntimeError("Task verification failed: " + "; ".join(verification))

        self.input_records = {item["path"]: item for item in self.packet.get("inputs", [])}
        self.output_baselines = {item["path"]: item for item in self.packet.get("output_baselines", [])}
        self.agent_write_paths = set(self.packet.get("operation_outputs", [])) | {
            self.packet["report_path"],
            self.packet["operator_brief_path"],
        }
        self.runtime_owned_paths = set(self.packet.get("runtime_owned_paths", []))
        if self.agent_write_paths.intersection(self.runtime_owned_paths):
            raise OutlineRuntimeError("Runtime-owned paths must be disjoint from model-writable outputs")
        self.trace_path = self.product_dir / f"tasks/{task_id}/runtime-trace.jsonl"
        expected_trace = f"tasks/{task_id}/runtime-trace.jsonl"
        expected_owned = {expected_trace, f"tasks/{task_id}/runtime-run.json"}
        if self.runtime_owned_paths != expected_owned:
            raise OutlineRuntimeError("Task runtime-owned scope differs from the exact trace/run contract")
        self._sources: list[dict[str, Any]] = []

    def _safe_product_path(self, relative: str) -> Path:
        if not isinstance(relative, str) or not relative:
            raise OutlineRuntimeError("Path must be a non-empty product-relative string")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            raise OutlineRuntimeError(f"Path escapes product scope: {relative}")
        target = (self.product_dir / relative).resolve()
        if not target.is_relative_to(self.product_dir):
            raise OutlineRuntimeError(f"Resolved path escapes product scope: {relative}")
        return target

    def _record_source(self, relative: str, path: Path) -> None:
        record = {"path": relative, "sha256": sha256(path), "bytes": path.stat().st_size}
        if record not in self._sources:
            self._sources.append(record)

    def _read_input_text(self, relative: str) -> str:
        record = self.input_records.get(relative)
        if record is None:
            raise OutlineRuntimeError(f"Capability attempted undeclared input read: {relative}")
        path = self._safe_product_path(relative)
        if not path.is_file():
            raise OutlineRuntimeError(f"Declared input is missing: {relative}")
        current = sha256(path)
        if current != record.get("sha256"):
            raise OutlineRuntimeError(f"Declared input is stale: {relative}")
        self._record_source(relative, path)
        return path.read_text(encoding="utf-8")

    def _read_control_json(self, path: Path) -> dict[str, Any]:
        if path not in {self.work_path, self.packet_path}:
            raise OutlineRuntimeError("Control read is outside the task envelope")
        relative = str(path.relative_to(self.product_dir))
        self._record_source(relative, path)
        return read_json(path)

    def _read_current_output(self, relative: str) -> str | None:
        if relative not in self.agent_write_paths and relative not in self.output_baselines:
            raise OutlineRuntimeError(f"Capability attempted undeclared output read: {relative}")
        path = self._safe_product_path(relative)
        if not path.is_file():
            return None
        self._record_source(relative, path)
        return path.read_text(encoding="utf-8")

    def _append_trace(
        self,
        capability: str,
        arguments: dict[str, Any],
        response: Any | None,
        error: str | None,
    ) -> None:
        safe_arguments = arguments
        if capability == "write_outputs":
            raw_files = arguments.get("files", [])
            if not isinstance(raw_files, list):
                raw_files = []
            safe_arguments = {
                "files": [
                    {
                        "path": item.get("path"),
                        "bytes": len(item.get("content", "").encode("utf-8")) if isinstance(item.get("content"), str) else None,
                        "sha256": hashlib.sha256(item.get("content", "").encode("utf-8")).hexdigest()
                        if isinstance(item.get("content"), str)
                        else None,
                    }
                    for item in raw_files
                    if isinstance(item, dict)
                ]
            }
        entry = {
            "schema_version": 1,
            "timestamp": utc_now(),
            "task_id": self.task_id,
            "capability": capability,
            "arguments": safe_arguments,
            "sources": self._sources,
            "response": response,
            "response_sha256": json_digest(response) if response is not None else None,
            "error": error,
        }
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        with self.trace_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")

    def call(self, capability: str, arguments: dict[str, Any] | None = None) -> Any:
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, dict):
            raise OutlineRuntimeError("Capability arguments must be an object")
        self._sources = []
        handlers = {
            "get_task_state": self.get_task_state,
            "get_product_direction": self.get_product_direction,
            "get_research_summary": self.get_research_summary,
            "search_evidence": self.search_evidence,
            "get_claims": self.get_claims,
            "get_benchmark": self.get_benchmark,
            "get_current_outline": self.get_current_outline,
            "write_outputs": self.write_outputs,
            "validate": self.validate,
            "submit": self.submit,
        }
        handler = handlers.get(capability)
        if handler is None:
            error = f"Unknown outline capability: {capability}"
            self._append_trace(capability, arguments, None, error)
            raise OutlineRuntimeError(error)
        try:
            response = handler(arguments)
        except Exception as exc:
            error = str(exc)
            self._append_trace(capability, arguments, None, error)
            raise
        self._append_trace(capability, arguments, response, None)
        return response

    def get_task_state(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise OutlineRuntimeError("get_task_state takes no arguments")
        work = self._read_control_json(self.work_path)
        packet = self._read_control_json(self.packet_path)
        brief_text = self._read_current_output(packet["operator_brief_path"])
        brief_template = json.loads(brief_text) if brief_text else None
        return {
            "task": {
                "id": work["id"],
                "product": work["product"],
                "operation": work["operation"],
                "state": work["state"],
                "authority": work["authority"],
                "target": work.get("target"),
            },
            "execution_runtime": packet.get("execution_runtime"),
            "declared_inputs": [item["path"] for item in packet.get("inputs", [])],
            "operation_outputs": packet.get("operation_outputs", []),
            "model_writable_paths": sorted(self.agent_write_paths),
            "runtime_owned_paths": sorted(self.runtime_owned_paths),
            "validation": packet.get("validation", []),
            "operator_brief_template": brief_template,
            "approval_boundary": "Outputs must remain draft; only the user may approve the outline.",
        }

    def get_product_direction(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise OutlineRuntimeError("get_product_direction takes no arguments")
        product_text = self._read_input_text("product.json")
        brief = self._read_input_text("00_brief/product-brief.md")
        return {"product": json.loads(product_text), "product_brief": brief}

    def get_research_summary(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise OutlineRuntimeError("get_research_summary takes no arguments")
        return {"research_summary": self._read_input_text("01_research/research-synthesis.md")}

    def get_benchmark(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise OutlineRuntimeError("get_benchmark takes no arguments")
        return {"benchmark": self._read_input_text("00_brief/benchmark.md")}

    def _evidence_pack(self) -> dict[str, Any]:
        return json.loads(self._read_input_text("01_research/outline-evidence-pack.json"))

    def get_claims(self, arguments: dict[str, Any]) -> dict[str, Any]:
        ids = arguments.get("ids")
        if ids is not None and (
            not isinstance(ids, list)
            or len(ids) > 50
            or not all(isinstance(item, str) and re.fullmatch(r"CLM-\d{4}", item) for item in ids)
        ):
            raise OutlineRuntimeError("ids must be a list of at most 50 CLM-#### values")
        limit = _bounded_int(arguments.get("limit"), default=20, minimum=1, maximum=50, field="limit")
        unknown = set(arguments).difference({"ids", "limit"})
        if unknown:
            raise OutlineRuntimeError("Unknown get_claims arguments: " + ", ".join(sorted(unknown)))
        pack = self._evidence_pack()
        claims = pack.get("claims", [])
        if ids is not None:
            requested = set(ids)
            selected = [item for item in claims if item.get("id") in requested]
            missing = sorted(requested.difference({item.get("id") for item in selected}))
        else:
            selected = claims[:limit]
            missing = []
        return {
            "claims": selected[:limit],
            "returned": min(len(selected), limit),
            "total_available": len(claims),
            "missing_ids": missing,
            "scope_note": pack.get("scope_note"),
        }

    def search_evidence(self, arguments: dict[str, Any]) -> dict[str, Any]:
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip() or len(query) > MAX_QUERY_CHARS:
            raise OutlineRuntimeError(f"query must be 1-{MAX_QUERY_CHARS} characters")
        limit = _bounded_int(arguments.get("limit"), default=10, minimum=1, maximum=20, field="limit")
        unknown = set(arguments).difference({"query", "limit"})
        if unknown:
            raise OutlineRuntimeError("Unknown search_evidence arguments: " + ", ".join(sorted(unknown)))
        terms = re.findall(r"[\wÀ-ỹ]+", query.casefold(), flags=re.UNICODE)
        if not terms:
            raise OutlineRuntimeError("query must contain searchable text")
        pack = self._evidence_pack()
        ranked: list[tuple[int, str, dict[str, Any]]] = []
        for claim in pack.get("claims", []):
            haystack = json.dumps(claim, ensure_ascii=False, sort_keys=True).casefold()
            score = sum(haystack.count(term) for term in terms)
            if claim.get("id", "").casefold() == query.strip().casefold():
                score += 100
            if score:
                ranked.append((score, claim.get("id", ""), claim))
        ranked.sort(key=lambda item: (-item[0], item[1]))

        contradiction_matches = []
        register = pack.get("contradiction_register", [])
        entries = register if isinstance(register, list) else [register]
        for entry in entries:
            haystack = json.dumps(entry, ensure_ascii=False, sort_keys=True).casefold()
            if any(term in haystack for term in terms):
                contradiction_matches.append(entry)
            if len(contradiction_matches) >= limit:
                break
        return {
            "query": query,
            "claims": [item[2] for item in ranked[:limit]],
            "contradictions": contradiction_matches,
            "scope_note": pack.get("scope_note"),
        }

    def get_current_outline(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise OutlineRuntimeError("get_current_outline takes no arguments")
        files: dict[str, Any] = {}
        for relative in self.packet.get("operation_outputs", []):
            content = self._read_current_output(relative)
            files[relative] = json.loads(content) if content is not None and relative.endswith(".json") else content
        change_request = "02_outline/outline-change-request.md"
        if change_request in self.input_records:
            files[change_request] = self._read_input_text(change_request)
        return {"files": files}

    def _write_limit(self, relative: str) -> int:
        if relative == self.packet["report_path"]:
            return 300_000
        if relative == self.packet["operator_brief_path"]:
            return 30_000
        return MAX_WRITE_BYTES.get(relative, 120_000)

    def write_outputs(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if set(arguments) != {"files"}:
            raise OutlineRuntimeError("write_outputs requires exactly one field: files")
        files = arguments.get("files")
        if not isinstance(files, list) or not 1 <= len(files) <= len(self.agent_write_paths):
            raise OutlineRuntimeError("files must contain one entry per bounded write, without duplicates")
        paths = [item.get("path") for item in files if isinstance(item, dict)]
        if len(paths) != len(files) or len(paths) != len(set(paths)):
            raise OutlineRuntimeError("write_outputs paths must be unique strings")

        prepared: list[tuple[str, Path, str]] = []
        for item in files:
            if set(item) != {"path", "content"}:
                raise OutlineRuntimeError("Each write entry requires exactly path and content")
            relative = item["path"]
            content = item["content"]
            if relative not in self.agent_write_paths:
                raise OutlineRuntimeError(f"Write is outside model scope: {relative}")
            if not isinstance(content, str):
                raise OutlineRuntimeError(f"Content for {relative} must be text")
            encoded = content.encode("utf-8")
            if len(encoded) > self._write_limit(relative):
                raise OutlineRuntimeError(f"Content for {relative} exceeds its bounded write limit")
            if relative.endswith(".json"):
                parsed = json.loads(content)
                if not isinstance(parsed, dict):
                    raise OutlineRuntimeError(f"JSON output must be an object: {relative}")
            prepared.append((relative, self._safe_product_path(relative), content))

        written = []
        for relative, path, content in prepared:
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
                handle.write(content)
                temp_path = Path(handle.name)
            try:
                os.replace(temp_path, path)
            finally:
                if temp_path.exists():
                    temp_path.unlink()
            written.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
        return {"written": written}

    def validate(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise OutlineRuntimeError("validate takes no arguments")
        errors = list(verify_task(self.product_dir, self.task_id))
        errors.extend(
            f"{issue.location}: {issue.message}"
            for issue in validate_product(self.product_dir)
            if issue.level == "ERROR"
        )
        current_work = read_json(self.work_path)
        errors.extend(validate_output_contract(self.product_dir, current_work))
        errors.extend(validate_brief_file(self.product_dir / self.packet["operator_brief_path"]))
        return {"ok": not errors, "errors": list(dict.fromkeys(errors))}

    def submit(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if arguments:
            raise OutlineRuntimeError("submit takes no arguments")
        errors = submit_task(self.product_dir, self.task_id)
        work = read_json(self.work_path)
        return {
            "ok": not errors,
            "errors": errors,
            "task_state": work.get("state"),
            "human_approval_required": True,
        }


TOOL_DEFINITIONS = [
    {
        "name": "get_task_state",
        "description": "Read the current work order, scope, validation commands, and operator-brief template.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "get_product_direction",
        "description": "Read the task-declared product state and product brief.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "get_research_summary",
        "description": "Read the task-declared research synthesis.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "search_evidence",
        "description": "Search only the deterministic outline evidence pack; never scans repository files.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "minLength": 1, "maxLength": MAX_QUERY_CHARS},
                "limit": {"type": "integer", "minimum": 1, "maximum": 20},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_claims",
        "description": "Read bounded claims by ID or page from the deterministic outline evidence pack.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ids": {"type": "array", "maxItems": 50, "items": {"type": "string", "pattern": "^CLM-\\d{4}$"}},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "get_benchmark",
        "description": "Read the task-declared benchmark brief.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "get_current_outline",
        "description": "Read current declared outline outputs and the task-declared outline change request, if present.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "write_outputs",
        "description": "Atomically write only declared outline artifacts, task report, or operator brief.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                        "required": ["path", "content"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["files"],
            "additionalProperties": False,
        },
    },
    {
        "name": "validate",
        "description": "Run existing deterministic task, product, output, and operator-brief validators.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "submit",
        "description": "Submit through the existing task lifecycle after validation; never grants human approval.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


def mcp_result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def handle_mcp_message(broker: OutlineContextBroker, message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if method in {"notifications/initialized", "notifications/cancelled"}:
        return None
    if method == "initialize":
        requested = message.get("params", {}).get("protocolVersion", "2025-06-18")
        return mcp_result(
            request_id,
            {
                "protocolVersion": requested,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "yt-production-outline-runtime", "version": str(INTERFACE_VERSION)},
                "instructions": "Use repository-backed outline capabilities only; all calls are audit-logged.",
            },
        )
    if method == "ping":
        return mcp_result(request_id, {})
    if method == "tools/list":
        return mcp_result(request_id, {"tools": TOOL_DEFINITIONS})
    if method == "tools/call":
        params = message.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})
        try:
            value = broker.call(name, arguments)
            return mcp_result(
                request_id,
                {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}]},
            )
        except Exception as exc:
            return mcp_result(
                request_id,
                {"content": [{"type": "text", "text": str(exc)}], "isError": True},
            )
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def serve_mcp(product_dir: Path, task_id: str) -> int:
    broker = OutlineContextBroker(product_dir, task_id)
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = handle_mcp_message(broker, message)
        except Exception as exc:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(exc)},
            }
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    return 0


def build_dsh_patch(product_dir: Path, task_id: str, runtime_dir: Path) -> str:
    product_dir = product_dir.resolve()
    adapter = Path(__file__).resolve()
    persona = (
        "You are an outline architecture execution agent. Use only the yt_outline MCP capabilities. "
        "Do not inspect the filesystem, run shell or code tools, browse, delegate, or treat session memory as factual authority. "
        "Repository artifacts returned by the broker are the sole factual authority. Human approval remains external."
    )
    lines = [
        "- id: system-prompt",
        "  config:",
        "    persona: " + json.dumps(persona, ensure_ascii=False),
    ]
    for row_id in DISABLED_DSH_ROWS:
        lines.extend([f"- id: {row_id}", "  disabled: true"])
    lines.extend(
        [
            "- insert:",
            "    - id: yt-outline-runtime-mcp",
            "      name: '@deepseek-ai/dsh-mcp-client'",
            "      config:",
            "        transport: stdio",
            f"        serverName: {SERVER_NAME}",
            "        command: " + json.dumps(sys.executable),
            "        args:",
            "          - " + json.dumps(str(adapter)),
            "          - mcp",
            "          - --product",
            "          - " + json.dumps(str(product_dir)),
            "          - --task-id",
            "          - " + json.dumps(task_id),
            "        env: {}",
            "        cwd: " + json.dumps(str(runtime_dir.resolve())),
            "        toolCallTimeoutMs: 60000",
            "        failOnStartupError: true",
        ]
    )
    return "\n".join(lines) + "\n"


def resolve_executable(value: str) -> str:
    if not value:
        raise OutlineRuntimeError("DSH executable must be non-empty")
    if os.sep in value:
        path = Path(value).resolve()
        if not path.is_file() or not os.access(path, os.X_OK):
            raise OutlineRuntimeError(f"DSH executable is unavailable: {path}")
        return str(path)
    resolved = shutil.which(value)
    if not resolved:
        raise OutlineRuntimeError(
            "DeepSeek Harness executable was not found. Install @deepseek-ai/dsh and expose the `dsh` binary, "
            "or pass --executable with an explicit path."
        )
    return resolved


def verify_composed_dsh_config(config_text: str) -> list[str]:
    """Fail closed if the tested DSH patch did not disable every broad tool row."""

    errors = []

    def row_block(row_id: str) -> str | None:
        match = re.search(
            rf"(?ms)^\s*-\s+id:\s*{re.escape(row_id)}\s*$\n(.*?)(?=^\s*-\s+id:|\Z)",
            config_text,
        )
        return match.group(1) if match else None

    for row_id in DISABLED_DSH_ROWS:
        block = row_block(row_id)
        if block is None:
            errors.append(f"composed DSH config is missing guarded row: {row_id}")
        elif not re.search(r"(?m)^\s+disabled:\s+true\s*$", block):
            errors.append(f"composed DSH config did not disable guarded row: {row_id}")
    broker = row_block("yt-outline-runtime-mcp")
    if broker is None:
        errors.append("composed DSH config is missing the outline MCP broker")
    else:
        if "@deepseek-ai/dsh-mcp-client" not in broker:
            errors.append("outline MCP broker resolved to an unexpected plugin")
        if not re.search(rf"(?m)^\s+serverName:\s*{SERVER_NAME}\s*$", broker):
            errors.append("outline MCP broker has an unexpected server namespace")
    return errors


def run_dsh(product_dir: Path, task_id: str, executable: str = "dsh", timeout_seconds: int = 1800) -> int:
    broker = OutlineContextBroker(product_dir, task_id)
    packet = broker.packet
    run_relative = f"tasks/{task_id}/runtime-run.json"
    if run_relative not in broker.runtime_owned_paths:
        raise OutlineRuntimeError("Task does not declare the runtime run record")
    run_path = broker.product_dir / run_relative
    dsh = resolve_executable(executable)
    seed = broker.context_path.read_text(encoding="utf-8")
    started = utc_now()

    with tempfile.TemporaryDirectory(prefix=f"yt-outline-{task_id}-") as temp:
        runtime_dir = Path(temp)
        patch_text = build_dsh_patch(broker.product_dir, task_id, runtime_dir)
        patch_path = runtime_dir / "outline-runtime.cordis.yml"
        patch_path.write_text(patch_text, encoding="utf-8")
        env = os.environ.copy()
        env["DSH_HOME"] = str(runtime_dir / "dsh-home")
        env["DSH_TELEMETRY_DISABLED"] = "1"
        env["DSH_PERMISSION_MODE"] = "read-only"
        env.pop("DSH_TOOLS_MODE", None)

        try:
            version_result = subprocess.run(
                [dsh, "--version"],
                cwd=runtime_dir,
                env=env,
                text=True,
                capture_output=True,
                timeout=15,
                check=False,
            )
            version_stdout = version_result.stdout.strip()
            version_stderr = version_result.stderr.strip()
        except subprocess.TimeoutExpired:
            version_stdout = ""
            version_stderr = "dsh --version timed out after 15 seconds"
        version_text = f"{version_stdout}\n{version_stderr}"
        if TESTED_DSH_VERSION not in version_text:
            raise OutlineRuntimeError(
                f"DSH version is outside the audited POC boundary; expected {TESTED_DSH_VERSION!r}, "
                f"got {version_text.strip() or 'no version output'!r}"
            )

        dump_result = subprocess.run(
            [dsh, "--profile", "headless", "--patch", str(patch_path), "--dump-config"],
            cwd=runtime_dir,
            env=env,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        if dump_result.returncode != 0:
            raise OutlineRuntimeError(
                "DSH config preflight failed: " + (dump_result.stderr.strip() or f"exit {dump_result.returncode}")
            )
        config_errors = verify_composed_dsh_config(dump_result.stdout)
        if config_errors:
            raise OutlineRuntimeError("DSH config boundary failed: " + "; ".join(config_errors))
        command = [dsh, "--profile", "headless", "--patch", str(patch_path), seed]
        timed_out = False
        try:
            result = subprocess.run(
                command,
                cwd=runtime_dir,
                env=env,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
            return_code = result.returncode
            stdout = result.stdout
            stderr = result.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            return_code = 124
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
            stderr = (stderr + f"\nDSH outline runtime timed out after {timeout_seconds} seconds.").strip()

        work = read_json(broker.work_path)
        if return_code == 0 and work.get("state") != "ready_for_review":
            return_code = 2
            stderr = (stderr + "\nDSH completed without submitting the task through the control plane.").strip()

        record = {
            "schema_version": 1,
            "task_id": task_id,
            "runtime": "dsh",
            "interface_version": INTERFACE_VERSION,
            "started_at": started,
            "finished_at": utc_now(),
            "executable": dsh,
            "version_stdout": version_stdout,
            "version_stderr": version_stderr,
            "tested_dsh_version": TESTED_DSH_VERSION,
            "composed_config_sha256": hashlib.sha256(dump_result.stdout.encode("utf-8")).hexdigest(),
            "composed_config": dump_result.stdout,
            "seed_sha256": hashlib.sha256(seed.encode("utf-8")).hexdigest(),
            "patch_sha256": hashlib.sha256(patch_text.encode("utf-8")).hexdigest(),
            "patch": patch_text,
            "telemetry_disabled": True,
            "workspace_mode": "isolated-empty-directory",
            "return_code": return_code,
            "timed_out": timed_out,
            "stdout": stdout[-100_000:],
            "stderr": stderr[-100_000:],
            "task_state": work.get("state"),
            "fallback": "Create a replacement outline task with --runtime legacy; product artifacts are runtime-neutral.",
            "packet_context_sha256": packet.get("context_sha256"),
        }
        write_json(run_path, record)
        if stdout:
            print(stdout, end="" if stdout.endswith("\n") else "\n")
        if stderr:
            print(stderr, file=sys.stderr)
        return return_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    mcp = sub.add_parser("mcp", help="Serve the scoped outline capability interface over MCP stdio")
    mcp.add_argument("--product", required=True, type=Path)
    mcp.add_argument("--task-id", required=True)
    run = sub.add_parser("run", help="Run one DSH headless outline task")
    run.add_argument("product", type=Path)
    run.add_argument("task_id")
    run.add_argument("--executable", default="dsh")
    run.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()
    try:
        if args.command == "mcp":
            return serve_mcp(args.product, args.task_id)
        if args.timeout_seconds < 1:
            raise OutlineRuntimeError("--timeout-seconds must be positive")
        return run_dsh(args.product, args.task_id, args.executable, args.timeout_seconds)
    except (OutlineRuntimeError, OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
