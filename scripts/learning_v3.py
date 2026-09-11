#!/usr/bin/env python3
"""Owner-first MVP v3: budgeted Sol repo + dynamic, unmetered Writer submissions."""

from __future__ import annotations
import argparse, hashlib, json, os, shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OVERLAY = REPO_ROOT / "products/sumer-writing/02_outline/section-overlays/P01.json"
DEFAULT_SUBSTRATE = REPO_ROOT / "products/sumer-writing/03_sections/P01/historical-substrate.json"
DEFAULT_RUNS_ROOT = REPO_ROOT / "runs"
SCHEMA_VERSION = "OWNER_FIRST_MVP_3"
WRITER_REPORT_SCHEMA = "DYNAMIC_WRITER_SUBMISSION_1"
SOL_SESSION = "sol-repo-001"
BUDGET_UNIT = "CUMULATIVE_AGENT_SESSION_SECONDS"
FORBIDDEN_REASONING_KEYS = {"chain_of_thought","raw_chain_of_thought","private_reasoning","internal_monologue","hidden_reasoning","scratchpad_reasoning"}

class LearningError(RuntimeError):
    def __init__(self, code, message, *, path=None, repair=None):
        self.code, self.path, self.repair = code, path, repair
        super().__init__(f"{code}: {message}" + (f" [path={path}]" if path else "") + (f" [repair={repair}]" if repair else ""))

def utc_now(): return datetime.now(timezone.utc).isoformat()
def sha256_bytes(data): return hashlib.sha256(data).hexdigest()
def sha256_file(path): return sha256_bytes(Path(path).read_bytes())
def canonical_sha256(v): return sha256_bytes(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())
def make_read_only(path):
    try: Path(path).chmod(0o444)
    except OSError: pass
def read_json(path):
    path=Path(path)
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc: raise LearningError("FILE_MISSING","required file does not exist",path=path) from exc
    except json.JSONDecodeError as exc: raise LearningError("JSON_INVALID",str(exc),path=path) from exc
    if not isinstance(value,dict): raise LearningError("JSON_OBJECT_REQUIRED","expected JSON object",path=path)
    return value
def atomic_write_json(path,value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); os.replace(tmp,path)
def append_jsonl(path,value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8",newline="\n") as f: f.write(json.dumps(value,ensure_ascii=False,sort_keys=True)+"\n")
def read_jsonl(path):
    path=Path(path)
    if not path.is_file(): return []
    return [v for line in path.read_text(encoding="utf-8").splitlines() if line.strip() for v in [json.loads(line)] if isinstance(v,dict)]
def _parse_utc(v):
    try: d=datetime.fromisoformat(v.replace("Z","+00:00"))
    except ValueError as exc: raise LearningError("TIMESTAMP_INVALID",f"invalid ISO timestamp: {v}") from exc
    if d.tzinfo is None: raise LearningError("TIMESTAMP_TZ_REQUIRED",f"timestamp must include timezone: {v}")
    return d.astimezone(timezone.utc)
def _within(path,root): return path==root or root in path.parents
def _safe_relative(v):
    p=Path(v)
    if p.is_absolute() or not p.parts or ".." in p.parts: raise LearningError("PATH_ESCAPE_DENIED","path must stay inside role workspace")
    return p

class WorkspaceBroker:
    """Sol-repo-only path broker; Writer hosts do not receive repo workspaces in v3."""
    def __init__(self,run_root,role,session_id):
        if role!="sol_repo" or session_id!=SOL_SESSION: raise LearningError("ROLE_UNSUPPORTED","v3 broker is only for sol_repo")
        self.run_root=Path(run_root).resolve(); self.root=(self.run_root/"agents/sol_repo"/SOL_SESSION).resolve()
        if not self.root.exists(): raise LearningError("WORKSPACE_MISSING","role workspace missing",path=self.root)
        self.log=self.run_root/"control/access-events.jsonl"
    def _resolve(self,relative,write):
        action="WRITE" if write else "READ"
        try: rel=_safe_relative(relative)
        except LearningError as exc:
            append_jsonl(self.log,{"schema_version":SCHEMA_VERSION,"role":"sol_repo","session_id":SOL_SESSION,"action":action,"attempted_path":relative,"resolved_path":None,"result":"DENIED","code":exc.code,"observed_at":utc_now()}); raise
        resolved=(self.root/rel).resolve(strict=False)
        roots=[(self.root/"output").resolve(),(self.root/"scratch").resolve()] + ([] if write else [(self.root/"input").resolve()])
        if not any(_within(resolved,r) for r in roots):
            append_jsonl(self.log,{"schema_version":SCHEMA_VERSION,"role":"sol_repo","session_id":SOL_SESSION,"action":action,"attempted_path":relative,"resolved_path":str(resolved),"result":"DENIED","code":"ROLE_PATH_DENIED","observed_at":utc_now()})
            raise LearningError("ROLE_PATH_DENIED","resolved path outside role workspace",path=resolved)
        return resolved
    def read_text(self,relative):
        p=self._resolve(relative,False)
        if not p.is_file(): raise LearningError("FILE_MISSING","role input missing",path=p)
        return p.read_text(encoding="utf-8")
    def write_text(self,relative,text):
        p=self._resolve(relative,True)
        if p.exists() and relative.startswith("output/"): raise LearningError("OUTPUT_OVERWRITE_DENIED","role output is write-once",path=p)
        p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding="utf-8"); return p

def _run_paths(r):
    r=Path(r)
    return {"state":r/"control/state.json","authority":r/"control/authority.json","budget":r/"control/budget.json","budget_events":r/"control/budget-events.jsonl","work":r/"control/work-intervals.jsonl","cost":r/"control/cost-items.jsonl","handoffs":r/"control/handoffs.jsonl","feedback":r/"control/owner-feedback.json","assignment":r/"control/writer-assignment.json","brief":r/"agents/sol_repo"/SOL_SESSION/"input/brief.json","plan":r/"agents/sol_repo"/SOL_SESSION/"output/plan.json","submissions":r/"submissions","owner_submissions":r/"owner/submissions"}
def _load_state(r):
    s=read_json(_run_paths(r)["state"])
    if s.get("schema_version")!=SCHEMA_VERSION: raise LearningError("STATE_VERSION_MISMATCH","unsupported MVP state")
    return s
def _save_state(r,s): s["updated_at"]=utc_now(); atomic_write_json(_run_paths(r)["state"],s)
def _verify_frozen(path,sha,label):
    path=Path(path)
    if not path.is_file(): raise LearningError("FROZEN_ARTIFACT_MISSING",f"{label} missing",path=path)
    if sha256_file(path)!=sha: raise LearningError("FROZEN_ARTIFACT_CHANGED",f"{label} changed after freeze",path=path)

def validate_authority(o,s):
    if o.get("section")!="P01" or s.get("section")!="P01": raise LearningError("SECTION_MISMATCH","MVP bounded to P01")
    ids=o.get("historical_substrate_ids"); ps=s.get("primitives")
    if not isinstance(ids,list) or not isinstance(ps,list): raise LearningError("AUTHORITY_MALFORMED","P01 authority malformed")
    have={p.get("id") for p in ps if isinstance(p,dict)}
    if any(x not in have for x in ids): raise LearningError("AUTHORITY_LINK_BROKEN","overlay references missing substrate primitive")
    if o.get("historical_territory")!=s.get("historical_territory") or o.get("historical_change")!=s.get("historical_change"): raise LearningError("AUTHORITY_MISMATCH","overlay/substrate authority mismatch")
def _verify_authority(r,s):
    m=read_json(_run_paths(r)["authority"])
    for x in m["files"]: _verify_frozen(Path(r)/x["snapshot_ref"],x["sha256"],x["snapshot_ref"])
    _verify_frozen(_run_paths(r)["authority"],s["authority_manifest_sha256"],"authority manifest")

def prepare_run(run_root,*,owner_request,overlay_path=DEFAULT_OVERLAY,substrate_path=DEFAULT_SUBSTRATE,test_only=False,code_ref=None):
    r=Path(run_root).resolve()
    if r.exists() and any(r.iterdir()): raise LearningError("RUN_ALREADY_EXISTS","run must be new/empty",path=r)
    if not owner_request.strip(): raise LearningError("OWNER_REQUEST_REQUIRED","owner request required")
    o,s=read_json(overlay_path),read_json(substrate_path); validate_authority(o,s)
    for n in ("input","output","scratch"): (r/"agents/sol_repo"/SOL_SESSION/n).mkdir(parents=True,exist_ok=True)
    (r/"control/authority").mkdir(parents=True,exist_ok=True); (r/"submissions").mkdir(); (r/"owner/submissions").mkdir(parents=True)
    for n in ("access-events.jsonl","handoffs.jsonl","budget-events.jsonl","work-intervals.jsonl","cost-items.jsonl"): (r/"control"/n).touch()
    snaps=[]; root=REPO_ROOT.resolve()
    for src,name in ((Path(overlay_path),"P01-overlay.json"),(Path(substrate_path),"P01-historical-substrate.json")):
        dst=r/"control/authority"/name; shutil.copyfile(src,dst); make_read_only(dst); sr=src.resolve()
        snaps.append({"source_ref":sr.relative_to(root).as_posix() if _within(sr,root) else str(sr),"snapshot_ref":dst.relative_to(r).as_posix(),"sha256":sha256_file(dst)})
    manifest={"schema_version":SCHEMA_VERSION,"section":"P01","files":snaps,"validated_links":True,"captured_at":utc_now()}
    atomic_write_json(_run_paths(r)["authority"],manifest); make_read_only(_run_paths(r)["authority"])
    brief={"schema_version":SCHEMA_VERSION,"role":"sol_repo","session_id":SOL_SESSION,"owner_request":owner_request,"section":"P01","task":"Prepare one short Plan and freeze common Writer assignment; do not write production prose.","authority":{"overlay":o,"historical_substrate":s},"required_plan_fields":["section","telling_scope","source_refs","stop_condition"],"source_refs_allowed":["overlay:P01",*o["historical_substrate_ids"]],"boundaries":["No separate Planner/reviewer/coordinator.","No evidence expansion.","No Writer prose.","Writers are dynamic, not pre-registered."]}
    atomic_write_json(_run_paths(r)["brief"],brief); make_read_only(_run_paths(r)["brief"])
    state={"schema_version":SCHEMA_VERSION,"run_id":r.name,"test_only":test_only,"code_ref":code_ref,"state":"AWAITING_OWNER_BUDGET_APPROVAL","resume_state":"READY_FOR_SOL_PLAN","waiting_for":"Owner","artifact_to_open":str(_run_paths(r)["brief"]),"next_action":"Owner approves Sol repo budget. Writer execution has no time-budget gate.","sessions":{"sol_repo":SOL_SESSION},"authority_manifest_sha256":sha256_file(_run_paths(r)["authority"]),"sol_brief_sha256":sha256_file(_run_paths(r)["brief"]),"plan_sha256":None,"writer_assignment_sha256":None,"submissions":[],"submissions_closed":False,"owner_feedback_sha256":None,"owner_request":owner_request,"created_at":utc_now(),"updated_at":utc_now(),"limitations":["Writer metadata is self-declared unless independently host-attested.","Writer timing is telemetry only.","NOT_PREBOUND is readable but not controlled same-assignment evidence."]}
    atomic_write_json(_run_paths(r)["state"],state); return state

def propose_budget(run_root,*,budget_id,sol_seconds,scope,code_ref,initial_cap_seconds=None):
    r=Path(run_root).resolve(); s=_load_state(r); p=_run_paths(r)["budget"]
    if p.exists(): raise LearningError("BUDGET_ALREADY_PROPOSED","budget is write-once")
    if sol_seconds<=0 or not budget_id.strip() or not scope.strip() or not code_ref.strip(): raise LearningError("BUDGET_FIELDS_INVALID","valid Sol budget fields required")
    cap=float(initial_cap_seconds if initial_cap_seconds is not None else sol_seconds)
    if cap<float(sol_seconds): raise LearningError("BUDGET_ALLOCATIONS_EXCEED_CAP","Sol allocation exceeds cap")
    b={"schema_version":SCHEMA_VERSION,"budget_id":budget_id,"request_id":f"{budget_id}:initial","run_id":s["run_id"],"unit":BUDGET_UNIT,"scope":scope,"code_ref":code_ref,"initial_cap_seconds":cap,"allocations_seconds":{"sol_repo":float(sol_seconds)},"writer_budget_policy":"NOT_APPLICABLE","created_at":utc_now()}
    atomic_write_json(p,b); make_read_only(p); s["artifact_to_open"]=str(p); s["next_action"]=f"Owner decides {b['request_id']}"; _save_state(r,s); return b
def _initial(events,rid):
    xs=[x for x in events if x.get("type")=="INITIAL_BUDGET_DECISION" and x.get("request_id")==rid]; return xs[-1] if xs else None
def _reqs(events): return {x["request_id"]:x for x in events if x.get("type")=="EXTENSION_REQUEST"}
def _decs(events): return {x["request_id"]:x for x in events if x.get("type")=="EXTENSION_DECISION"}
def budget_summary(run_root,**_):
    r=Path(run_root); p=_run_paths(r)["budget"]
    if not p.is_file(): return {"status":"NOT_PROPOSED","approved":False,"writer_budget_policy":"NOT_APPLICABLE"}
    b=read_json(p); ev=read_jsonl(_run_paths(r)["budget_events"]); ini=_initial(ev,b["request_id"]); approved=bool(ini and ini.get("decision")=="APPROVED")
    ext=sum(float(x.get("approved_seconds") or 0) for rid,x in _decs(ev).items() if rid in _reqs(ev) and x.get("decision")=="APPROVED")
    ws=[x for x in read_jsonl(_run_paths(r)["work"]) if x.get("actor")=="sol_repo" and x.get("kind")=="WORK"]; known=[x for x in ws if isinstance(x.get("duration_seconds"),(int,float))]
    unknown=sum(1 for x in ws if x.get("duration_seconds") is None); used=sum(float(x["duration_seconds"]) for x in known); alloc=(float(b["allocations_seconds"]["sol_repo"]) if approved else 0)+ext; rem=None if unknown else alloc-used
    return {"status":"APPROVED" if approved else (ini.get("decision") if ini else "PENDING_OWNER_APPROVAL"),"approved":approved,"budget_id":b["budget_id"],"request_id":b["request_id"],"unit":b["unit"],"writer_budget_policy":"NOT_APPLICABLE","sol_repo":{"allocated_seconds":alloc,"used_seconds":used,"unknown_intervals":unknown,"remaining_seconds":rem,"overrun_seconds":None if rem is None else max(0,-rem),"extension_approved_seconds":ext},"pending_extension_requests":[x for rid,x in _reqs(ev).items() if rid not in _decs(ev)]}
def record_budget_decision(run_root,*,request_id,decision,owner_text,source_ref,actor=None,scope=None,approved_seconds=None):
    r=Path(run_root).resolve(); s=_load_state(r); b=read_json(_run_paths(r)["budget"]); ev=read_jsonl(_run_paths(r)["budget_events"]); decision=decision.upper()
    if not owner_text.strip() or not source_ref.strip(): raise LearningError("OWNER_APPROVAL_EVIDENCE_REQUIRED","Owner text/source required")
    if request_id==b["request_id"]:
        if _initial(ev,request_id): raise LearningError("BUDGET_DECISION_ALREADY_RECORDED","decision immutable")
        x={"schema_version":SCHEMA_VERSION,"type":"INITIAL_BUDGET_DECISION","run_id":s["run_id"],"request_id":request_id,"decision":decision,"owner_text":owner_text,"source_ref":source_ref,"recorded_at":utc_now()}; append_jsonl(_run_paths(r)["budget_events"],x)
        if decision=="APPROVED": s.update({"state":"READY_FOR_SOL_PLAN","resume_state":None,"waiting_for":"Sol repo","artifact_to_open":str(_run_paths(r)["brief"]),"next_action":"Sol repo prepares Plan within approved repo budget."})
        else: s.update({"state":"AWAITING_OWNER_BUDGET_APPROVAL","waiting_for":"Owner","next_action":"Budget rejected; Sol repo may not start."})
        _save_state(r,s); return x
    req=_reqs(ev)
    if request_id not in req: raise LearningError("EXTENSION_REQUEST_NOT_FOUND","extension request not found")
    if request_id in _decs(ev): raise LearningError("EXTENSION_DECISION_ALREADY_RECORDED","decision immutable")
    if actor!="sol_repo" or scope!=req[request_id]["scope"]: raise LearningError("EXTENSION_APPROVAL_SCOPE_MISMATCH","must match sol_repo request")
    if decision=="APPROVED" and (approved_seconds is None or approved_seconds<=0 or approved_seconds>req[request_id]["requested_seconds"]): raise LearningError("EXTENSION_AMOUNT_INVALID","invalid extension amount")
    x={"schema_version":SCHEMA_VERSION,"type":"EXTENSION_DECISION","run_id":s["run_id"],"request_id":request_id,"actor":"sol_repo","scope":scope,"decision":decision,"approved_seconds":float(approved_seconds or 0),"owner_text":owner_text,"source_ref":source_ref,"recorded_at":utc_now()}; append_jsonl(_run_paths(r)["budget_events"],x)
    if decision=="APPROVED": s["state"]=s.get("resume_state") or "READY_FOR_SOL_PLAN"; s["resume_state"]=None
    _save_state(r,s); return x
def request_budget_extension(run_root,*,actor,requested_seconds,scope,reason,evidence,request_id=None):
    if actor!="sol_repo": raise LearningError("WRITER_BUDGET_NOT_APPLICABLE","Writer timing is telemetry only; only sol_repo has time budget")
    r=Path(run_root).resolve(); s=_load_state(r); sm=budget_summary(r)
    if not sm.get("approved"): raise LearningError("BUDGET_NOT_APPROVED","initial Sol budget not approved")
    ev=read_jsonl(_run_paths(r)["budget_events"]); rid=request_id or f"{sm['budget_id']}:extension:{len(_reqs(ev))+1:03d}"
    x={"schema_version":SCHEMA_VERSION,"type":"EXTENSION_REQUEST","run_id":s["run_id"],"request_id":rid,"actor":"sol_repo","scope":scope,"requested_seconds":float(requested_seconds),"reason":reason,"evidence":evidence,"requested_at":utc_now()}; append_jsonl(_run_paths(r)["budget_events"],x)
    s["resume_state"]=s["state"] if s["state"]!="AWAITING_OWNER_BUDGET_APPROVAL" else s.get("resume_state"); s.update({"state":"AWAITING_OWNER_BUDGET_APPROVAL","waiting_for":"Owner","next_action":f"Owner decides {rid}"}); _save_state(r,s); return x

def _record_interval(r,*,actor,session_id,task,attempt,kind="WORK",start_utc=None,end_utc=None,duration_seconds=None,timestamp_source="UNKNOWN",status="COMPLETED",reason="",evidence_ref=None):
    if actor not in {"sol_repo","owner_wait","host_queue"}: raise LearningError("TIMING_ACTOR_INVALID","Writer timing belongs in submission metadata")
    sd=_parse_utc(start_utc) if start_utc else None; ed=_parse_utc(end_utc) if end_utc else None; comp=(ed-sd).total_seconds() if sd and ed else None
    if comp is not None and comp<0: raise LearningError("TIMING_CLOCK_REVERSED","end precedes start")
    if duration_seconds is not None:
        if duration_seconds<0: raise LearningError("TIMING_DURATION_INVALID","duration negative")
        if comp is not None and abs(comp-duration_seconds)>.01: raise LearningError("TIMING_DURATION_MISMATCH","duration mismatch")
        comp=float(duration_seconds)
    x={"schema_version":SCHEMA_VERSION,"interval_id":f"I{len(read_jsonl(_run_paths(r)['work']))+1:04d}","run_id":_load_state(r)["run_id"],"kind":kind,"actor":actor,"session_id":session_id,"task":task,"attempt":attempt,"start_utc":start_utc,"end_utc":end_utc,"duration_seconds":comp,"timestamp_source":timestamp_source,"status":"UNKNOWN" if comp is None else status,"reason":reason,"evidence_ref":evidence_ref,"recorded_at":utc_now()}; append_jsonl(_run_paths(r)["work"],x); return x
def record_wait_interval(run_root,**kwargs): kwargs["kind"]="WAIT"; return _record_interval(run_root,**kwargs)
def _require_sol_budget(r):
    sm=budget_summary(r)
    if not sm.get("approved"): raise LearningError("BUDGET_NOT_APPROVED","Owner-approved Sol budget required")
    row=sm["sol_repo"]
    if row["unknown_intervals"]: raise LearningError("BUDGET_ACCOUNTING_UNKNOWN","Sol timing UNKNOWN")
    if row["remaining_seconds"] is None or row["remaining_seconds"]<=0: raise LearningError("BUDGET_EXHAUSTED","Sol budget exhausted")
def _validate_plan(p,b):
    if p.get("section")!="P01": raise LearningError("PLAN_SECTION_INVALID","plan.section must be P01")
    if not all(isinstance(p.get(k),str) and p[k].strip() for k in ("telling_scope","stop_condition")): raise LearningError("PLAN_FIELD_REQUIRED","telling_scope/stop_condition required")
    refs=p.get("source_refs")
    if not isinstance(refs,list) or not refs: raise LearningError("PLAN_SOURCE_REFS_REQUIRED","source_refs required")
    extra=set(refs)-set(b["source_refs_allowed"])
    if extra: raise LearningError("PLAN_AUTHORITY_EXPANSION",f"unauthorized refs: {sorted(extra)}")

def freeze_plan(run_root,*,session_id,source_file,declared_reason,uncertainty,start_utc=None,end_utc=None,duration_seconds=None,timestamp_source="UNKNOWN",**_):
    r=Path(run_root).resolve(); s=_load_state(r)
    if s["state"]!="READY_FOR_SOL_PLAN": raise LearningError("STATE_TRANSITION_DENIED",f"cannot freeze Plan from {s['state']}")
    if session_id!=SOL_SESSION: raise LearningError("SESSION_MISMATCH",f"expected {SOL_SESSION}")
    _require_sol_budget(r); _verify_authority(r,s); _verify_frozen(_run_paths(r)["brief"],s["sol_brief_sha256"],"Sol brief")
    p=read_json(source_file); _validate_plan(p,read_json(_run_paths(r)["brief"])); target=_run_paths(r)["plan"]
    if target.exists(): raise LearningError("OUTPUT_OVERWRITE_DENIED","Plan already exists")
    target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source_file,target); make_read_only(target); ps=sha256_file(target)
    interval=_record_interval(r,actor="sol_repo",session_id=SOL_SESSION,task="prepare_plan",attempt=1,start_utc=start_utc,end_utc=end_utc,duration_seconds=duration_seconds,timestamp_source=timestamp_source,reason=declared_reason,evidence_ref=target.relative_to(r).as_posix())
    s["plan_sha256"]=ps; m=read_json(_run_paths(r)["authority"])
    assignment={"schema_version":SCHEMA_VERSION,"assignment_kind":"DYNAMIC_WRITER_ASSIGNMENT","run_id":s["run_id"],"owner_request":s["owner_request"],"section":"P01","task":"Write one standalone Vietnamese historical-podcast excerpt; one attempt, no self-review/reroll.","frozen_plan":p,"frozen_plan_sha256":ps,"authority":{"overlay":read_json(r/m["files"][0]["snapshot_ref"]),"historical_substrate":read_json(r/m["files"][1]["snapshot_ref"]),"source_hashes":{x["snapshot_ref"]:x["sha256"] for x in m["files"]}},"boundaries":["No Plan/evidence expansion while writing.","No other Writer/Owner feedback inspection.","One content attempt only.","Writer identity is declared after execution.","Writer timing is telemetry only; no Writer time-budget gate."],"required_submission":{"draft":"UTF-8 Markdown","metadata_schema":WRITER_REPORT_SCHEMA},"frozen_at":utc_now()}
    atomic_write_json(_run_paths(r)["assignment"],assignment); make_read_only(_run_paths(r)["assignment"]); s["writer_assignment_sha256"]=sha256_file(_run_paths(r)["assignment"])
    sm=budget_summary(r); row=sm["sol_repo"]
    if row["unknown_intervals"] or (row["remaining_seconds"] is not None and row["remaining_seconds"]<0):
        s["resume_state"]="AWAITING_WRITER_SUBMISSIONS"; _save_state(r,s); request_budget_extension(r,actor="sol_repo",requested_seconds=max(float(row["overrun_seconds"] or .001),.001),scope="prepare_plan",reason="Sol repo work exceeded/invalidated budget",evidence=target.relative_to(r).as_posix()); return _load_state(r)
    s.update({"state":"AWAITING_WRITER_SUBMISSIONS","resume_state":None,"waiting_for":"Writer submissions","artifact_to_open":str(_run_paths(r)["assignment"]),"next_action":"Owner may launch any Writer/model. Writer timing is telemetry only."})
    append_jsonl(_run_paths(r)["handoffs"],{"schema_version":SCHEMA_VERSION,"role":"sol_repo","session_id":SOL_SESSION,"output_sha256":ps,"writer_assignment_sha256":s["writer_assignment_sha256"],"declared_reason":declared_reason,"uncertainty":uncertainty,"timing_interval_id":interval["interval_id"],"validation":"ACCEPTED"}); _save_state(r,s); return s

def _contains_forbidden(v):
    if isinstance(v,dict): return any(str(k).casefold() in FORBIDDEN_REASONING_KEYS or _contains_forbidden(x) for k,x in v.items())
    if isinstance(v,list): return any(_contains_forbidden(x) for x in v)
    return False
def _submission_paths(r,sid):
    root=_run_paths(r)["submissions"]/sid; return root/"draft.md",root/"execution-report.json",_run_paths(r)["owner_submissions"]/f"{sid}.md"
def _validate_report(r,report,draft):
    if report.get("schema_version")!=WRITER_REPORT_SCHEMA: raise LearningError("WRITER_REPORT_SCHEMA_INVALID",f"expected {WRITER_REPORT_SCHEMA}")
    if _contains_forbidden(report): raise LearningError("PRIVATE_REASONING_FIELD_FORBIDDEN","private reasoning forbidden")
    sid=report.get("submission_id")
    if not isinstance(sid,str) or not sid.strip() or any(x in sid for x in ("/","\\","..")): raise LearningError("SUBMISSION_ID_INVALID","safe submission_id required")
    if not isinstance(report.get("actual_model"),str) or not report["actual_model"].strip(): raise LearningError("MODEL_IDENTITY_REQUIRED","declare actual_model or UNKNOWN")
    if report.get("attempt")!=1: raise LearningError("WRITER_REPORT_ATTEMPT_INVALID","one content attempt only")
    status=str(report.get("status") or "").upper()
    if status not in {"COMPLETED","FAILED","TIMEOUT"}: raise LearningError("WRITER_REPORT_STATUS_INVALID","invalid status")
    binding=report.get("assignment_binding")
    if binding not in {"PREBOUND","NOT_PREBOUND"}: raise LearningError("ASSIGNMENT_BINDING_INVALID","PREBOUND/NOT_PREBOUND required")
    state=_load_state(r)
    if binding=="PREBOUND" and report.get("assignment_sha256")!=state.get("writer_assignment_sha256"): raise LearningError("ASSIGNMENT_HASH_MISMATCH","PREBOUND must match frozen assignment")
    inputs=report.get("inputs_used")
    if not isinstance(inputs,list) or not inputs or any(not isinstance(x,dict) or not isinstance(x.get("ref"),str) or not isinstance(x.get("sha256"),str) for x in inputs): raise LearningError("WRITER_INPUT_PROVENANCE_REQUIRED","inputs_used ref+sha256 required")
    timing=report.get("timing")
    if not isinstance(timing,dict): raise LearningError("WRITER_REPORT_TIMING_REQUIRED","timing object required; UNKNOWN allowed")
    d=timing.get("duration_seconds")
    if d is not None and (not isinstance(d,(int,float)) or d<0): raise LearningError("TIMING_DURATION_INVALID","Writer duration invalid")
    if status=="COMPLETED":
        if draft is None or not Path(draft).is_file() or not Path(draft).read_text(encoding="utf-8").strip(): raise LearningError("DRAFT_MISSING","completed submission requires draft")
        if report.get("draft_sha256")!=sha256_file(draft): raise LearningError("WRITER_REPORT_DRAFT_HASH_MISMATCH","draft hash mismatch")
    return sid,status

def accept_writer_submission(run_root,*,report_file,draft_file=None):
    r=Path(run_root).resolve(); s=_load_state(r)
    if s["state"]!="AWAITING_WRITER_SUBMISSIONS" or s["submissions_closed"]: raise LearningError("STATE_TRANSITION_DENIED","Writer pool closed/not open")
    _verify_authority(r,s); _verify_frozen(_run_paths(r)["plan"],s["plan_sha256"],"Plan"); _verify_frozen(_run_paths(r)["assignment"],s["writer_assignment_sha256"],"Writer assignment")
    report=read_json(report_file); sid,status=_validate_report(r,report,draft_file); fd,fr,owner=_submission_paths(r,sid)
    if fr.exists() or any(x["submission_id"]==sid for x in s["submissions"]): raise LearningError("SUBMISSION_ALREADY_EXISTS","submission ID is write-once")
    fr.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(report_file,fr); make_read_only(fr); ds=None; owner_ref=None
    if status=="COMPLETED":
        shutil.copyfile(draft_file,fd); make_read_only(fd); ds=sha256_file(fd); shutil.copyfile(fd,owner); make_read_only(owner); owner_ref=owner.relative_to(r).as_posix()
    rec={"submission_id":sid,"status":status,"provider":report.get("provider"),"actual_model":report["actual_model"],"actual_config":report.get("actual_config"),"provider_session_id":report.get("provider_session_id"),"assignment_binding":report["assignment_binding"],"assignment_sha256":report.get("assignment_sha256"),"controlled_comparison_eligible":report["assignment_binding"]=="PREBOUND","report_ref":fr.relative_to(r).as_posix(),"report_sha256":sha256_file(fr),"draft_ref":fd.relative_to(r).as_posix() if ds else None,"draft_sha256":ds,"owner_ref":owner_ref,"timing":report["timing"],"issues_encountered":report.get("issues_encountered",[]),"uncertainty":report.get("uncertainty"),"accepted_at":utc_now()}
    s["submissions"].append(rec); s["artifact_to_open"]=[x["owner_ref"] for x in s["submissions"] if x.get("owner_ref")]; s["next_action"]="Owner may launch more Writers or close submissions."
    append_jsonl(_run_paths(r)["handoffs"],{"schema_version":SCHEMA_VERSION,"role":"dynamic_writer","submission_id":sid,"assignment_binding":report["assignment_binding"],"report_sha256":rec["report_sha256"],"output_sha256":ds,"validation":"ACCEPTED"}); _save_state(r,s); return s

def close_submissions(run_root):
    r=Path(run_root).resolve(); s=_load_state(r)
    if s["state"]!="AWAITING_WRITER_SUBMISSIONS" or s["submissions_closed"]: raise LearningError("STATE_TRANSITION_DENIED","pool not open")
    completed=[x for x in s["submissions"] if x["status"]=="COMPLETED"]
    if not completed: raise LearningError("NO_COMPLETED_SUBMISSIONS","need at least one completed submission")
    s.update({"state":"AWAITING_OWNER_FEEDBACK","submissions_closed":True,"waiting_for":"Owner","artifact_to_open":[x["owner_ref"] for x in completed],"next_action":"Owner reads frozen set and records feedback."}); _save_state(r,s); return s
def record_owner_feedback(run_root,*,feedback_text,selection="UNSELECTED",primary_writer=None):
    r=Path(run_root).resolve(); s=_load_state(r)
    if s["state"]!="AWAITING_OWNER_FEEDBACK": raise LearningError("STATE_TRANSITION_DENIED","Owner feedback gate not open")
    completed=[x for x in s["submissions"] if x["status"]=="COMPLETED"]; ids={x["submission_id"] for x in completed}
    if selection not in {"UNSELECTED","TIE"} and selection not in ids: raise LearningError("OWNER_SELECTION_INVALID","selection must be submission_id/TIE/UNSELECTED")
    if primary_writer is not None and primary_writer not in ids: raise LearningError("PRIMARY_WRITER_INVALID","primary_writer must be completed submission_id")
    samples={}
    for x in completed:
        _verify_frozen(r/x["draft_ref"],x["draft_sha256"],x["submission_id"]); _verify_frozen(r/x["owner_ref"],x["draft_sha256"],x["submission_id"])
        samples[x["submission_id"]]={"ref":x["owner_ref"],"sha256":x["draft_sha256"],"actual_model":x["actual_model"],"assignment_binding":x["assignment_binding"]}
    f={"schema_version":SCHEMA_VERSION,"authority":"OWNER","samples":samples,"verbatim_feedback":feedback_text,"selection":selection,"primary_writer_decision":primary_writer,"model_generalization":"NOT_PERFORMED","interpretation":"NOT_PERFORMED","recorded_at":utc_now()}
    atomic_write_json(_run_paths(r)["feedback"],f); make_read_only(_run_paths(r)["feedback"]); s.update({"state":"OWNER_FEEDBACK_RECORDED","waiting_for":"Owner","next_action":"STOP. No auto-rerun/default Writer.","artifact_to_open":str(_run_paths(r)["feedback"]),"owner_feedback_sha256":sha256_file(_run_paths(r)["feedback"])}); _save_state(r,s); return s
def record_cost_item(run_root,**kwargs):
    x={"schema_version":SCHEMA_VERSION,**kwargs,"recorded_at":utc_now()}; append_jsonl(_run_paths(run_root)["cost"],x); return x
def status(run_root,**_):
    r=Path(run_root).resolve(); s=_load_state(r); _verify_authority(r,s)
    if s.get("plan_sha256"): _verify_frozen(_run_paths(r)["plan"],s["plan_sha256"],"Plan")
    if s.get("writer_assignment_sha256"): _verify_frozen(_run_paths(r)["assignment"],s["writer_assignment_sha256"],"Writer assignment")
    for x in s["submissions"]:
        _verify_frozen(r/x["report_ref"],x["report_sha256"],x["submission_id"])
        if x.get("draft_sha256"): _verify_frozen(r/x["draft_ref"],x["draft_sha256"],x["submission_id"]); _verify_frozen(r/x["owner_ref"],x["draft_sha256"],x["submission_id"])
    return {"run_id":s["run_id"],"state":s["state"],"waiting_for":s["waiting_for"],"artifact_to_open":s["artifact_to_open"],"next_action":s["next_action"],"test_only":s["test_only"],"writer_assignment_sha256":s.get("writer_assignment_sha256"),"submissions_closed":s["submissions_closed"],"submissions":s["submissions"],"writer_budget_policy":"NOT_APPLICABLE","budget":budget_summary(r),"cost_items":read_jsonl(_run_paths(r)["cost"]),"limitations":s["limitations"]}
def submission_template(run_root,submission_id="writer-001"):
    s=_load_state(run_root); sha=s.get("writer_assignment_sha256")
    return {"schema_version":WRITER_REPORT_SCHEMA,"submission_id":submission_id,"provider":None,"actual_model":"UNKNOWN","actual_config":None,"provider_session_id":None,"assignment_binding":"PREBOUND" if sha else "NOT_PREBOUND","assignment_sha256":sha,"inputs_used":[{"ref":"control/writer-assignment.json","sha256":sha or "UNKNOWN"}],"attempt":1,"status":"COMPLETED","timing":{"source":"UNKNOWN","duration_seconds":None},"draft_sha256":"<sha256 of draft.md>","issues_encountered":[],"uncertainty":""}
def _resolve_run(v,root):
    p=Path(v); return p if p.is_absolute() or len(p.parts)>1 else Path(root)/p

def main():
    ap=argparse.ArgumentParser(description="Owner-first MVP v3"); ap.add_argument("--runs-root",type=Path,default=DEFAULT_RUNS_ROOT); sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("prepare"); p.add_argument("--run",required=True); g=p.add_mutually_exclusive_group(required=True); g.add_argument("--request"); g.add_argument("--request-file",type=Path); p.add_argument("--overlay",type=Path,default=DEFAULT_OVERLAY); p.add_argument("--substrate",type=Path,default=DEFAULT_SUBSTRATE); p.add_argument("--test-only",action="store_true"); p.add_argument("--code-ref")
    b=sp.add_parser("budget-propose"); b.add_argument("--run",required=True); b.add_argument("--budget-id",required=True); b.add_argument("--sol-seconds",type=float,required=True); b.add_argument("--cap-seconds",type=float); b.add_argument("--scope",required=True); b.add_argument("--code-ref",required=True)
    d=sp.add_parser("budget-decision"); d.add_argument("--run",required=True); d.add_argument("--request-id",required=True); d.add_argument("--decision",choices=["APPROVED","REJECTED"],required=True); d.add_argument("--owner-text",required=True); d.add_argument("--source-ref",required=True); d.add_argument("--actor"); d.add_argument("--scope"); d.add_argument("--approved-seconds",type=float)
    q=sp.add_parser("freeze-plan"); q.add_argument("--run",required=True); q.add_argument("--session",default=SOL_SESSION); q.add_argument("--file",type=Path,required=True); q.add_argument("--reason",required=True); q.add_argument("--uncertainty",required=True); q.add_argument("--start-utc"); q.add_argument("--end-utc"); q.add_argument("--duration-seconds",type=float); q.add_argument("--timestamp-source",default="UNKNOWN")
    c=sp.add_parser("close-submissions"); c.add_argument("--run",required=True)
    f=sp.add_parser("feedback"); f.add_argument("--run",required=True); gg=f.add_mutually_exclusive_group(required=True); gg.add_argument("--text"); gg.add_argument("--file",type=Path); f.add_argument("--selection",default="UNSELECTED"); f.add_argument("--primary-writer")
    st=sp.add_parser("status"); st.add_argument("--run",required=True)
    a=ap.parse_args(); r=_resolve_run(a.run,a.runs_root).resolve()
    try:
        if a.cmd=="prepare": out=prepare_run(r,owner_request=a.request if a.request is not None else a.request_file.read_text(encoding="utf-8"),overlay_path=a.overlay,substrate_path=a.substrate,test_only=a.test_only,code_ref=a.code_ref)
        elif a.cmd=="budget-propose": out=propose_budget(r,budget_id=a.budget_id,sol_seconds=a.sol_seconds,initial_cap_seconds=a.cap_seconds,scope=a.scope,code_ref=a.code_ref)
        elif a.cmd=="budget-decision": out=record_budget_decision(r,request_id=a.request_id,decision=a.decision,owner_text=a.owner_text,source_ref=a.source_ref,actor=a.actor,scope=a.scope,approved_seconds=a.approved_seconds)
        elif a.cmd=="freeze-plan": out=freeze_plan(r,session_id=a.session,source_file=a.file,declared_reason=a.reason,uncertainty=a.uncertainty,start_utc=a.start_utc,end_utc=a.end_utc,duration_seconds=a.duration_seconds,timestamp_source=a.timestamp_source)
        elif a.cmd=="close-submissions": out=close_submissions(r)
        elif a.cmd=="feedback": out=record_owner_feedback(r,feedback_text=a.text if a.text is not None else a.file.read_text(encoding="utf-8"),selection=a.selection,primary_writer=a.primary_writer)
        else: out=status(r)
        print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
    except LearningError as e:
        print(json.dumps({"status":"ERROR","code":e.code,"message":str(e)},ensure_ascii=False,indent=2)); return 2
if __name__=="__main__": raise SystemExit(main())
