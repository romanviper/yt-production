"""Bounded experimental packet tooling; no LLM calls or semantic certification."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import secrets
import sys

ROOT = Path(__file__).resolve().parents[2]
DOC = "docs/experiments/p01-foc-loop/"
RUNS = "experiments/p01-foc-loop/runs/"
DIMS = ("continue", "movement", "specificity", "connections", "listenability", "payoff")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path, value):
    require(not path.exists(), f"Refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(path):
    return json.loads(read(path))


def config(root=ROOT):
    return load(root / DOC / "round-01.json")


def tracked_inputs(c):
    return sorted(set(["AGENTS.md", DOC + "START.md", DOC + "protocol.md",
                       DOC + "round-01.json", "scripts/experiments/p01_foc_loop.py",
                       "tests/test_p01_foc_loop.py", c["baseline"]]
                      + c["authority"] + c["product_context"]
                      + [r["path"] for r in c["references"]]))


def reference_text(root, r):
    text = read(root / r["path"]).strip()
    if r["start"]:
        require(text.count(r["start"]) == 1, "Ambiguous reference start")
        text = text[text.index(r["start"]):]
    if r["end"]:
        require(text.count(r["end"]) == 1, "Ambiguous reference end")
        text = text[:text.index(r["end"])]
    return text.strip()


def references(root, c):
    return [{"id": r["id"], "function": r["function"],
             "text": reference_text(root, r), "audio_status": r["audio_status"],
             "source": r["path"], "role": "CRAFT_ONLY_NOT_TRUTH"}
            for r in c["references"]]


def baseline(root, c):
    paragraphs = [p.strip() for p in read(root / c["baseline"]).split("\n\n")
                  if p.strip() and not p.lstrip().startswith("#")]
    first, last = c["baseline_paragraphs"]
    require(1 <= first <= last <= len(paragraphs), "Invalid baseline extent")
    return "\n\n".join(paragraphs[first - 1:last])


def snapshot(root):
    c = config(root)
    return {"schema": 1, "hash_normalization": "UTF-8, BOM removed, CRLF to LF",
            "files": {p: digest(read(root / p)) for p in tracked_inputs(c)},
            "baseline_excerpt_sha256": digest(baseline(root, c)),
            "reference_excerpt_sha256": {r["id"]: digest(r["text"])
                                         for r in references(root, c)}}


def check(root=ROOT):
    frozen = load(root / DOC / "inputs.lock.json")
    require(frozen == snapshot(root), "Frozen input drift: create a new protocol version, not a silent rerun")
    return frozen


def runpath(root, name):
    require(re.fullmatch(r"round-[0-9]{2}", name), "Run ID must be round-NN")
    require(name == "round-01", "This frozen contract authorizes round-01 only")
    return root / RUNS / name


def bundle(root, paths):
    return {p: read(root / p) for p in paths}


def writer(root, name):
    lock = check(root)
    c = config(root)
    run = runpath(root, name)
    require(not run.exists(), "Run already exists; preserve original attempts")
    packet = {"role": "WRITER", "scope": c["scope"],
              "hypothesis": c["hypothesis"], "failure_prediction": c["failure_prediction"],
              "instruction": c["writer_instruction"],
              "length_whitespace_units_not_duration": c["candidate_whitespace_units"],
              "baseline": baseline(root, c), "authority": bundle(root, c["authority"]),
              "product_context": bundle(root, c["product_context"]),
              "craft_references": references(root, c),
              "output": "Plain Vietnamese narration only; no headings or report."}
    write_json(run / "writer-packet.json", packet)
    write_json(run / "frozen-inputs.json", lock)
    return {"status": "WRITER_PACKET_READY", "packet": str(run / "writer-packet.json")}


def sentences(text):
    # IDs cover every nonempty sentence-like segment, including final fragments.
    return [{"id": f"S{i:03d}", "text": s.strip()}
            for i, s in enumerate(re.split(r"(?<=[.!?])\s+|\n+", text.strip()), 1)
            if s.strip()]


def product_packet(root, c, samples):
    return {"role": "PRODUCT_REVIEWER", "samples": samples,
            "craft_references": references(root, c),
            "instruction": (
                "Evaluate only these texts. You do not know which is newer. No truth verdicts. "
                "Do not add absent narrative bridges. Judge a material-investigation opening, "
                "not a whole episode. References are craft examples, not perfect gold answers. "
                "Compare same-function portions; discuss duration/language differences. "
                "Listenability is a text prediction, not an observed audio result. "
                "Return exactly the required JSON structure. Quotes must be exact nonempty spans. "
                "For each dimension explain consequences and the remaining FoC gap. "
                "TIE/UNCERTAIN are legitimate. No certification or unconditional PASS."),
            "dimensions": {
                "continue": "Reason to continue listening",
                "movement": "Change in understanding, situation or inquiry across beats",
                "specificity": "Details/actions that perform narrative work",
                "connections": "Actual transitions, without your invented links",
                "listenability": "Predicted one-pass comprehension, load and rhythm",
                "payoff": "Earned local understanding, not generic summary/teaser"},
            "output_schema": {
                "packet_sha256": "SHA256 of the exact packet file supplied by operator",
                "winner": "A|B|TIE|UNCERTAIN",
                "dimensions": {d: {"winner": "A|B|TIE|UNCERTAIN", "a_quote": "exact span",
                                   "b_quote": "exact span", "reference_id": "FOC reference ID",
                                   "reference_quote": "exact span", "reason": "observed effect",
                                   "remaining_gap": "specific remaining FoC difference"} for d in DIMS},
                "strongest_counterargument": "Why your preferred sample might not be better"}}


def prepare(root, name):
    lock = check(root)
    c = config(root)
    run = runpath(root, name)
    require(load(run / "frozen-inputs.json") == lock, "Run input drift")
    require(not (run / "dispatch.json").exists(), "Already prepared; no re-randomization")
    candidate = read(run / "candidate.md").strip()
    low, high = c["candidate_whitespace_units"]
    require(low <= len(candidate.split()) <= high, f"Candidate must have {low}–{high} whitespace units")
    require(not re.search(r"(?m)^\s*#", candidate), "Candidate must contain narration only")
    old = baseline(root, c)
    require(candidate != old, "Unchanged candidate")
    order = secrets.choice([True, False])
    samples = {"A": candidate if order else old, "B": old if order else candidate}
    packets = {"product-1": product_packet(root, c, samples),
               "product-2": product_packet(root, c, {"A": samples["B"], "B": samples["A"]}),
               "truth": {"role": "TRUTH_REVIEWER", "candidate": sentences(candidate),
                         "authority": bundle(root, c["authority"]),
                         "instruction": (
                             "Audit all factual clauses, not just familiar prohibited words. "
                             "Split each sentence into atomic claims. For every claim bind exact "
                             "source quote and locator to the relationship/function/motive/cause/"
                             "sequence/scope, not merely the entity. No external authority. "
                             "QUALIFIED requires wording that preserves qualification. "
                             "RECONSTRUCTION requires packet permission. NONFACTUAL must truly "
                             "assert no historical fact. Missing authority => UNSUPPORTED. "
                             "Cover all supplied sentence IDs; preserve every unresolved issue."),
                         "output_schema": {
                             "packet_sha256": "operator-supplied exact packet hash",
                             "claims": [{"sentence_id": "S001", "claim_quote": "exact clause",
                                         "status": "SUPPORTED|QUALIFIED|RECONSTRUCTION|UNSUPPORTED|NONFACTUAL",
                                         "source": "approved authority path, or empty",
                                         "locator": "record ID and field / notebook paragraph",
                                         "source_quote": "exact source span, or empty",
                                         "reason": "component-level entailment/limitation"}],
                             "unresolved": ["all unresolved defects, empty only if none"]}}}
    hashes = {}
    for role, packet in packets.items():
        path = run / f"{role}-packet.json"
        write_json(path, packet)
        hashes[role] = digest(read(path))
    write_json(run / "dispatch.json", {"candidate_sha256": digest(candidate),
                                       "candidate_labels": {"product-1": "A" if order else "B",
                                                            "product-2": "B" if order else "A"},
                                       "packet_hashes": hashes})
    write_json(run / "execution.template.json", {
        "roles": {role: {"run_id": "", "model_config": "", "started_at": "", "finished_at": "",
                         "input_only_enforced": False, "platform_export": "",
                         "platform_export_sha256": ""} for role in packets},
        "commander_semantic_audit": {"complete": False, "evidence_file": "", "sha256": ""}})
    return {"status": "REVIEW_PACKETS_READY_NOT_DISPATCHED", "packet_hashes": hashes}


def exact(quote, text, label):
    require(isinstance(quote, str) and bool(quote.strip()) and quote in text, f"Invalid exact quote: {label}")


def validate_product(review, packet, packet_hash):
    require(review["packet_sha256"] == packet_hash, "Product review packet mismatch")
    require(review["winner"] in {"A", "B", "TIE", "UNCERTAIN"}, "Invalid winner")
    require(set(review["dimensions"]) == set(DIMS), "Missing/extra craft dimension")
    require(bool(review["strongest_counterargument"].strip()), "Missing counterargument")
    refs = {r["id"]: r["text"] for r in packet["craft_references"]}
    for dim, finding in review["dimensions"].items():
        require(finding["winner"] in {"A", "B", "TIE", "UNCERTAIN"}, "Invalid dimension verdict")
        exact(finding["a_quote"], packet["samples"]["A"], dim + ":A")
        exact(finding["b_quote"], packet["samples"]["B"], dim + ":B")
        exact(finding["reference_quote"], refs[finding["reference_id"]], dim + ":FoC")
        require(bool(finding["reason"].strip()) and bool(finding["remaining_gap"].strip()), "Missing craft argument/gap")


def validate_truth(review, packet, packet_hash):
    require(review["packet_sha256"] == packet_hash, "Truth review packet mismatch")
    sentences_by_id = {s["id"]: s["text"] for s in packet["candidate"]}
    require({c["sentence_id"] for c in review["claims"]} == set(sentences_by_id), "Incomplete sentence coverage")
    require(isinstance(review["unresolved"], list), "Unresolved must be a list")
    blocked = bool(review["unresolved"])
    for claim in review["claims"]:
        exact(claim["claim_quote"], sentences_by_id[claim["sentence_id"]], "claim")
        status = claim["status"]
        require(status in {"SUPPORTED", "QUALIFIED", "RECONSTRUCTION", "UNSUPPORTED", "NONFACTUAL"}, "Invalid truth status")
        require(bool(claim["reason"].strip()), "Missing truth reasoning")
        if status in {"SUPPORTED", "QUALIFIED", "RECONSTRUCTION"}:
            require(claim["source"] in packet["authority"], "Source outside authority")
            exact(claim["source_quote"], packet["authority"][claim["source"]], "authority")
            require(bool(claim["locator"].strip()), "Missing locator")
        blocked |= status == "UNSUPPORTED"
    return not blocked


def evidence_file(run, name, sha):
    if not isinstance(name, str) or not name:
        return False
    path = (run / name).resolve()
    if not path.is_relative_to(run.resolve()) or not path.is_file():
        return False
    return bool(read(path).strip()) and digest(read(path)) == sha


def process_valid(run, execution):
    roles = execution.get("roles", {})
    if set(roles) != {"truth", "product-1", "product-2"}:
        return False
    ids = set()
    exports = set()
    for role in roles.values():
        if not all(isinstance(role.get(k), str) and role[k].strip()
                   for k in ("run_id", "model_config", "started_at", "finished_at")):
            return False
        ids.add(role["run_id"])
        try:
            start = datetime.fromisoformat(role["started_at"].replace("Z", "+00:00"))
            finish = datetime.fromisoformat(role["finished_at"].replace("Z", "+00:00"))
            if start.tzinfo is None or finish.tzinfo is None or finish < start:
                return False
        except ValueError:
            return False
        exports.add(role.get("platform_export"))
        if role.get("input_only_enforced") is not True or not evidence_file(
                run, role.get("platform_export"), role.get("platform_export_sha256")):
            return False
    audit = execution.get("commander_semantic_audit", {})
    return (len(ids) == 3 and len(exports) == 3 and audit.get("complete") is True and
            evidence_file(run, audit.get("evidence_file"), audit.get("sha256")))


def outcome(truth_ok, execution_ok, reviews, labels):
    if not truth_ok:
        return "REJECT_TRUTH"
    if not execution_ok:
        return "INCONCLUSIVE_PROCESS"
    for role, review in reviews.items():
        target = labels[role]
        if review["winner"] != target or review["dimensions"]["movement"]["winner"] != target:
            return "NO_DEMONSTRATED_GAIN"
        if any(f["winner"] not in {target, "TIE"} for f in review["dimensions"].values()):
            return "NO_DEMONSTRATED_GAIN"
    return "PROVISIONAL_SCRIPT_IMPROVEMENT"


def decide(root, name):
    lock = check(root)
    run = runpath(root, name)
    require(load(run / "frozen-inputs.json") == lock, "Run input drift")
    dispatch = load(run / "dispatch.json")
    require(digest(read(run / "candidate.md").strip()) == dispatch["candidate_sha256"], "Candidate changed after dispatch")
    packets, reviews = {}, {}
    for role, sha in dispatch["packet_hashes"].items():
        require(digest(read(run / f"{role}-packet.json")) == sha, "Packet changed after dispatch")
        packets[role] = load(run / f"{role}-packet.json")
        reviews[role] = load(run / f"{role}.json")
    truth_ok = validate_truth(reviews.pop("truth"), packets["truth"], dispatch["packet_hashes"]["truth"])
    for role, review in reviews.items():
        validate_product(review, packets[role], dispatch["packet_hashes"][role])
    execution = load(run / "execution.json") if (run / "execution.json").exists() else {}
    result = {"status": outcome(truth_ok, process_valid(run, execution), reviews, dispatch["candidate_labels"]),
              "audio_status": "NOT_EVALUATED", "human_listener_status": "NOT_EVALUATED",
              "limitations": "Schema/quote checks cannot prove entailment, genuine isolation or listener engagement. Commander must inspect real exports and semantic bindings; this is not certification.",
              "artifacts_sha256": {p.name: digest(read(p)) for p in run.iterdir() if p.is_file()}}
    write_json(run / "decision.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["freeze", "check", "writer", "prepare", "decide"])
    parser.add_argument("--run", default="round-01")
    args = parser.parse_args()
    try:
        if args.command == "freeze":
            write_json(ROOT / DOC / "inputs.lock.json", snapshot(ROOT))
            result = {"status": "INPUTS_FROZEN_NOT_EVALUATED"}
        elif args.command == "check":
            check()
            result = {"status": "READY_FOR_ROUND_1_PREPARATION", "writer_executed": False,
                      "audio_verified": False, "isolation_verified": False}
        else:
            result = globals()[args.command](ROOT, args.run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
