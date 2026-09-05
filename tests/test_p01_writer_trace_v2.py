import importlib.util, unittest
from pathlib import Path
S=importlib.util.spec_from_file_location('m',Path(__file__).resolve().parents[1]/'scripts/experiments/p01_writer_trace_v2.py'); m=importlib.util.module_from_spec(S); S.loader.exec_module(m)
def plan():
 return {'schema':1,'segment_goal':'x','listener_start_state':{'knows':['a'],'does_not_yet_know':['b']},'beats':[{'id':f'B0{i}','function':'payoff' if i==4 else 'observation','evidence':[{'source':'s','locator':'l','source_quote':'clay'}],'listener_before':str(i),'listener_after':str(i+1),'new_information':'n','withheld_or_delayed':'w','forward_pressure':'f','truth_boundary':'t'} for i in range(1,5)],'local_payoff':'p','essay_failure_risks':['r'],'realization_constraints':['c']}
class T(unittest.TestCase):
 def test_plan_requires_state_change(self):
  p=plan(); p['beats'][0]['listener_after']=p['beats'][0]['listener_before']; old=m.bundle; m.bundle=lambda _: {'s':'clay'}
  with self.assertRaises(ValueError): m.validate_plan(p,{'plan_beat_count':[4,8],'authority':['s']})
  m.bundle=old
 def test_plan_accepts_evidence(self):
  old=m.bundle; m.bundle=lambda _: {'s':'clay'}; m.validate_plan(plan(),{'plan_beat_count':[4,8],'authority':['s']}); m.bundle=old
 def test_writer_report_covers_all_beats(self):
  p=plan(); cand='one two three four'; r={'schema':1,'plan_sha256':'h','beat_execution':[{'beat_id':f'B0{i}','status':'REALIZED','candidate_quote':q,'note':'n'} for i,q in enumerate(['one','two','three','four'],1)]}; m.validate_report(r,p,cand,'h')
 def test_writer_report_missing_beat_fails(self):
  with self.assertRaises(ValueError): m.validate_report({'schema':1,'plan_sha256':'h','beat_execution':[]},plan(),'x','h')
 def test_process_requires_writer_role(self): self.assertFalse(m.process_valid(Path('.'),{'roles':{}}))
if __name__=='__main__': unittest.main()