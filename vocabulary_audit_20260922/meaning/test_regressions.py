"""Business-rule regressions for the saved, fully rerun 20,000-card audit."""
from pathlib import Path
from tempfile import TemporaryDirectory
import contextlib,io,json,sys,unittest
B=Path(__file__).resolve().parent;P=B.parent
sys.path.insert(0,str(P))
from conditional_audit import main

class MeaningAuditTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.findings=json.loads((P/'final_findings.json').read_text())
  cls.bykey={(x['pack'],x['overall'],x['word']):x for x in cls.findings}
  cls.reviews=json.loads((B/'sense_reviews.json').read_text())
  cls.resolutions=json.loads((P/'semantic_decisions.json').read_text())
 def test_homonyms_do_not_block_known_inflections(self):
  for p,n,w in [('english_russian',134,'saw'),('english_russian',307,'fell'),('english_russian',191,'left'),('russian_english',13,'mine')]:
   self.assertNotIn((p,n,w),self.bykey)
   self.assertTrue(any(x['pack']==p and x['overall']==n and x['word']==w and x['allowed'] for x in self.resolutions))
 def test_same_meaning_later_forms_stay_blocked(self):
  f=self.bykey[('russian_english',2140,'forbidden')]
  self.assertEqual(f['earliest']['overall'],6169)
  self.assertTrue(any(x['word']=='bought' and x['earliest']['overall']==8106 for x in self.findings))
 def test_find_does_not_borrow_the_establish_entry(self):
  for n in [181,1540,1833,1851,1865,1922]:
   self.assertEqual(self.bykey[('english_russian',n,'found')]['earliest']['overall'],1650)
  self.assertNotIn(('english_russian',2022,'found'),self.bykey)
 def test_unknown_inflections_still_allowed(self):
  self.assertFalse(any(x['word']=='worked' for x in self.findings))
 def test_current_target_does_not_need_prior_base(self):
  self.assertNotIn(('english_russian',530,'managed'),self.bykey)
  self.assertNotIn(('russian_english',259,'managed'),self.bykey)
 def test_all_approved_exemptions_active(self):
  ex=set(json.loads((P/'exempt_forms.json').read_text()))
  self.assertEqual(len(ex),16)
  self.assertFalse(any(x['word'] in ex for x in self.findings))
 def test_totals_and_update_inventory_agree(self):
  plan=json.loads((B/'update_plan.json').read_text());summary=json.loads((P/'final_summary.json').read_text())
  self.assertEqual({(x['pack'],x['overall']) for x in plan},{(x['pack'],x['overall']) for x in self.findings})
  self.assertEqual(len(plan),sum(x['flagged_cards'] for x in summary.values()))
  self.assertTrue(all(x['cardId'] and x['current_english_example'] and x['current_russian_example'] for x in plan))
 def test_changed_context_cannot_reuse_old_semantic_review(self):
  lookup={(x['pack'],x['overall'],x['word']):dict(x) for x in self.reviews}
  lookup[('english_russian',134,'saw')]['example']='A different sentence.'
  with TemporaryDirectory() as temp,contextlib.redirect_stdout(io.StringIO()):
   with self.assertRaisesRegex(AssertionError,'Stale semantic review'):
    main(sense_reviews=lookup,output_base=Path(temp))

if __name__=='__main__':unittest.main()
