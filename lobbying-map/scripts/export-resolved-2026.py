"""Export current built 2026 entities, preserving split and merge provenance."""
import csv, gzip, json, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
out=root.parent/'outputs/2026-directory'
data=json.load(gzip.open(root/'public/data/directory-v3.json.gz'))
rows=[]
for c in data['companies']:
 if not c['years'].get('2026'):continue
 p=c.get('profile') or {}
 rows.append({'id':c['id'],'name':c['name'],'reports_2026':c['years']['2026'],'source_member_ids':c['members'],'filing_names':c['aliases'],'assigned_filing_ids':c.get('filing_ids'), 'identity_split':c.get('identity_split'), 'source_records':c.get('source_records'), 'profile':p})
assert len({r['id'] for r in rows})==len(rows)
(out/'resolved-organizations.json').write_text(json.dumps(rows,indent=2)+'\n')
fields=['id','name','reports_2026','source_member_ids','filing_names','description','organization_type','ownership','website','logo_url','review_outcome','sources','assigned_filing_ids']
with (out/'resolved-organizations.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in rows:
  p=r['profile'];w.writerow(dict(id=r['id'],name=r['name'],reports_2026=r['reports_2026'],source_member_ids=' | '.join(r['source_member_ids']),filing_names=' | '.join(r['filing_names']),description=p.get('description',''),organization_type=p.get('kind',''),ownership=p.get('ownership',''),website=p.get('website',''),logo_url=p.get('logo_url',''),review_outcome=p.get('review_outcome',''),sources=' | '.join(s['url'] for s in p.get('sources',[])),assigned_filing_ids=' | '.join(r['assigned_filing_ids'] or [])))
progress=json.loads((out/'progress.json').read_text());progress['displayed_organizations']=len(rows);progress['resolved_export_scope']='Built local directory, including verified splits and merges; publication status is tracked separately.';(out/'progress.json').write_text(json.dumps(progress,indent=2)+'\n')
print(f'Exported {len(rows)} 2026 entities after splits and merges.')
