"""Writer-observability experiment v2. No model calls; only packet/provenance gates."""
import argparse, hashlib, json, re, secrets, sys
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; DOC=ROOT/'docs/experiments/p01-writer-trace-v2'; RUNS=ROOT/'experiments/p01-writer-trace-v2/runs'
DIMS=('continue','movement','specificity','connections','listenability','payoff')
def req(x,m):
    if not x: raise ValueError(m)
def rd(p): return p.read_text(encoding='utf-8-sig').replace('\r\n','\n')
def js(p): return json.loads(rd(p))
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def wr(p,v): req(not p.exists(),f'refuse overwrite: {p}'); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def cfg(): return js(DOC/'round-01.json')
def run(n): req(re.fullmatch(r'round-01',n),'v2 authorizes round-01 only'); return RUNS/n
def bundle(paths): return {p:rd(ROOT/p) for p in paths}
def baseline(c):
    ps=[x.strip() for x in rd(ROOT/c['baseline']).split('\n\n') if x.strip() and not x.lstrip().startswith('#')]; a,b=c['baseline_paragraphs']; return '\n\n'.join(ps[a-1:b])
def refs(c):
    out=[]
    for r in c['references']:
        t=rd(ROOT/r['path']).strip()
        if r['start']: req(t.count(r['start'])==1,'bad ref start'); t=t[t.index(r['start']):]
        if r['end']: req(t.count(r['end'])==1,'bad ref end'); t=t[:t.index(r['end'])]
        out.append({'id':r['id'],'function':r['function'],'text':t.strip(),'role':'CRAFT_ONLY_NOT_TRUTH'})
    return out
def check(): req(js(DOC/'inputs.lock.json')['source_commit']==cfg()['source_commit'],'lock/config mismatch')
def exact(q,t,m): req(isinstance(q,str) and q.strip() and q in t,f'bad exact quote: {m}')
def planner_packet(c): return {'role':'PLANNER','scope':c['scope'],'instruction':c['planner_instruction'],'baseline':baseline(c),'authority':bundle(c['authority']),'product_context':bundle(c['product_context']),'craft_references':refs(c),'output_schema':{'schema':1,'segment_goal':'...','listener_start_state':{'knows':['...'],'does_not_yet_know':['...']},'beats':[{'id':'B01','function':'observation|question|contrast|reveal|reframe|payoff','evidence':[{'source':'approved path','locator':'...','source_quote':'exact quote'}],'listener_before':'...','listener_after':'...','new_information':'...','withheld_or_delayed':'...','forward_pressure':'...','truth_boundary':'...'}],'local_payoff':'...','essay_failure_risks':['...'],'realization_constraints':['...']}}
def plan(name): check(); r=run(name); req(not r.exists(),'run exists'); wr(r/'planner-packet.json',planner_packet(cfg())); wr(r/'frozen-inputs.json',js(DOC/'inputs.lock.json')); return {'status':'PLANNER_PACKET_READY'}
def validate_plan(p,c):
    req(p.get('schema')==1,'bad plan schema'); beats=p.get('beats'); lo,hi=c['plan_beat_count']; req(isinstance(beats,list) and lo<=len(beats)<=hi,'bad beat count'); ids=[]; payoff=False; auth=bundle(c['authority']); fields={'id','function','evidence','listener_before','listener_after','new_information','withheld_or_delayed','forward_pressure','truth_boundary'}
    for b in beats:
        req(set(b)==fields,'bad beat fields'); req(re.fullmatch(r'B\d\d',b['id']),'bad beat id'); ids.append(b['id']); req(b['listener_before'].strip()!=b['listener_after'].strip(),'beat must change listener state'); payoff|=b['function']=='payoff'; req(b['evidence'],'beat needs evidence')
        for e in b['evidence']: req(e['source'] in auth,'outside authority'); exact(e['source_quote'],auth[e['source']],b['id'])
    req(len(ids)==len(set(ids)),'duplicate beats'); req(payoff,'missing payoff'); req(p.get('local_payoff'),'missing local payoff'); req(p.get('essay_failure_risks'),'missing essay risks'); req(p.get('realization_constraints'),'missing realization constraints')
def lock_plan(name):
    check(); c=cfg(); r=run(name); p=js(r/'writing-plan.json'); validate_plan(p,c); h=sha(rd(r/'writing-plan.json')); wr(r/'plan.lock.json',{'writing_plan_sha256':h}); wr(r/'writer-packet.json',{'role':'WRITER','scope':c['scope'],'instruction':c['writer_instruction'],'frozen_plan_sha256':h,'frozen_writing_plan':p,'authority':bundle(c['authority']),'product_context':bundle(c['product_context']),'context_exclusions':['old baseline','FoC transcripts','review labels','previous verdicts','planner conversation'],'outputs':{'candidate.md':'Vietnamese narration only','writer-report.json':{'schema':1,'plan_sha256':h,'beat_execution':[{'beat_id':'B01','status':'REALIZED|PARTIAL|OMITTED','candidate_quote':'exact span or empty if omitted','note':'observable execution note'}],'deviations':[],'exposition_risks':[],'truth_risks':[],'strongest_realization':'...','weakest_realization':'...'}},'report_boundary':'Observable decisions/deviations only; no private chain-of-thought.'}); return {'status':'WRITER_PACKET_READY','writing_plan_sha256':h}
def validate_report(x,p,cand,h):
    req(x.get('schema')==1 and x.get('plan_sha256')==h,'writer report mismatch'); ids={b['id'] for b in p['beats']}; rows=x.get('beat_execution',[]); req(len(rows)==len(ids) and {z.get('beat_id') for z in rows}==ids,'writer report must cover every beat exactly once')
    for z in rows:
        req(z['status'] in {'REALIZED','PARTIAL','OMITTED'},'bad beat status'); q=z.get('candidate_quote',''); req(bool(z.get('note','').strip()),'missing beat note'); (req(q=='','omitted beat needs empty quote') if z['status']=='OMITTED' else exact(q,cand,z['beat_id']))
def product_packet(c,samples): return {'role':'PRODUCT_REVIEWER','samples':samples,'craft_references':refs(c),'instruction':'Judge prose only; blind to plan/trace/newness. TIE/UNCERTAIN allowed.','output_schema':{'packet_sha256':'...','winner':'A|B|TIE|UNCERTAIN','dimensions':{d:{'winner':'A|B|TIE|UNCERTAIN'} for d in DIMS}}}
def sentences(t): return [{'id':f'S{i:03d}','text':s.strip()} for i,s in enumerate(re.split(r'(?<=[.!?])\s+|\n+',t.strip()),1) if s.strip()]
def prepare(name):
    check(); c=cfg(); r=run(name); p=js(r/'writing-plan.json'); lock=js(r/'plan.lock.json'); req(sha(rd(r/'writing-plan.json'))==lock['writing_plan_sha256'],'plan changed'); cand=rd(r/'candidate.md').strip(); lo,hi=c['candidate_whitespace_units']; req(lo<=len(cand.split())<=hi,'bad candidate length'); rep=js(r/'writer-report.json'); validate_report(rep,p,cand,lock['writing_plan_sha256']); old=baseline(c); order=secrets.choice([True,False]); samples={'A':cand if order else old,'B':old if order else cand}; packets={'product-1':product_packet(c,samples),'product-2':product_packet(c,{'A':samples['B'],'B':samples['A']}),'truth':{'role':'TRUTH_REVIEWER','candidate':sentences(cand),'authority':bundle(c['authority']),'instruction':'Audit every factual clause using only authority.'},'trace-auditor':{'role':'TRACE_AUDITOR','writing_plan':p,'candidate':cand,'writer_report':rep,'instruction':'Audit observable plan-to-prose alignment; do not infer private reasoning.','output_schema':{'packet_sha256':'...','plan_quality':'COHERENT|WEAK|UNCERTAIN','realization_quality':'ALIGNED|PARTIAL|MISALIGNED|UNCERTAIN','failure_mode':'NONE|PLAN_FAILURE|REALIZATION_FAILURE|MIXED|TRACE_UNRELIABLE','diagnostic_summary':'...'}}}; hs={}
    for role,pkt in packets.items(): wr(r/f'{role}-packet.json',pkt); hs[role]=sha(rd(r/f'{role}-packet.json'))
    labels={'product-1':'A' if order else 'B','product-2':'B' if order else 'A'}; wr(r/'dispatch.json',{'candidate_sha256':sha(cand),'candidate_labels':labels,'review_packet_hashes':hs}); role_packets={'planner':'planner-packet.json','writer':'writer-packet.json','trace-auditor':'trace-auditor-packet.json','truth':'truth-packet.json','product-1':'product-1-packet.json','product-2':'product-2-packet.json'}; wr(r/'execution.template.json',{'roles':{role:{'run_id':'','model_config':'','started_at':'','finished_at':'','operator_verified_input_isolation':False,'input_packet':fn,'input_packet_sha256':sha(rd(r/fn)),'platform_export':'','platform_export_sha256':''} for role,fn in role_packets.items()}}); return {'status':'AUDIT_PACKETS_READY_NOT_DISPATCHED'}
def process_valid(r,e):
    roles=e.get('roles',{}); expected={'planner','writer','trace-auditor','truth','product-1','product-2'}
    if set(roles)!=expected:return False
    for x in roles.values():
        if not all(str(x.get(k,'')).strip() for k in ('run_id','model_config','started_at','finished_at','input_packet','input_packet_sha256')) or x.get('operator_verified_input_isolation') is not True:return False
    return True
def decide(name):
    check(); r=run(name); d=js(r/'dispatch.json'); req(sha(rd(r/'candidate.md').strip())==d['candidate_sha256'],'candidate changed'); truth=js(r/'truth.json'); truth_ok=not truth.get('unresolved') and not any(c.get('status')=='UNSUPPORTED' for c in truth.get('claims',[])); ok=process_valid(r,js(r/'execution.json') if (r/'execution.json').exists() else {}); status='REJECT_TRUTH' if not truth_ok else ('INCONCLUSIVE_PROCESS' if not ok else 'NO_DEMONSTRATED_GAIN'); tr=js(r/'trace-auditor.json'); out={'status':status,'diagnosis':tr.get('failure_mode','TRACE_UNRELIABLE'),'plan_quality':tr.get('plan_quality','UNCERTAIN'),'realization_quality':tr.get('realization_quality','UNCERTAIN')}; wr(r/'decision.json',out); return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('command',choices=['check','plan','lock-plan','prepare','decide']); ap.add_argument('--run',default='round-01'); a=ap.parse_args()
    try:
        if a.command=='check': check(); res={'status':'READY_FOR_PLANNING'}
        else: res=globals()[a.command.replace('-','_')](a.run)
        print(json.dumps(res,ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as e: print('BLOCKED:',e,file=sys.stderr); return 1
    return 0
if __name__=='__main__': sys.exit(main())