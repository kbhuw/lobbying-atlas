import unittest
from cleaning import norm,key,date,period,latest_groups
class CleaningTests(unittest.TestCase):
 def r(self,id,kind,posted,year=2025):return dict(id=id,client='Acme LLC',registrant='Firm A',year=year,kind=kind,posted=posted)
 def test_no_activity_correction_replaces_activity(self):
  g=latest_groups([self.r('a','1st Quarter - Report','04/10/2025 @ 10:00 AM'),self.r('b','1st Quarter - Amendment (No Activity)','05/10/2025 @ 10:00 AM')]);rs=next(iter(g.values()))[1];self.assertEqual([r['id'] for r in rs],['b']);self.assertFalse(all('No Activity' not in r['kind'] for r in rs))
 def test_registration_does_not_establish_activity(self):self.assertEqual(latest_groups([self.r('a','Registration','04/10/2025 @ 10:00 AM')]),{})
 def test_reporting_year_not_posting_year(self):
  g=latest_groups([self.r('a','4th Quarter - Report','01/10/2026 @ 10:00 AM')]);self.assertEqual(next(iter(g))[2],2025)
 def test_same_minute_versions_are_preserved(self):
  g=latest_groups([self.r('a','1st Quarter - Report','04/10/2025 @ 10:00 AM'),self.r('b','1st Quarter - Amendment','04/10/2025 @ 10:00 AM')]);self.assertEqual(len(next(iter(g.values()))[1]),2)
 def test_exact_names_without_fuzzy_merges(self):
  self.assertEqual(key(' ACME\u00a0LLC '),key('acme llc'));self.assertNotEqual(key('Acme LLC'),key('Acme Inc.'));self.assertNotEqual(key('A&B'),key('A and B'))
 def test_legacy_semesters_separate(self):self.assertNotEqual(period('Mid-Year Amendment'),period('Year-End Report'))
 def test_sort_dates_chronologically(self):self.assertGreater(date('01/10/2026 @ 12:00 AM'),date('12/31/2025 @ 11:59 PM'))
if __name__=='__main__':unittest.main()
