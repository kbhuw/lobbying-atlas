import json,pathlib,collections,datetime,csv,re
r=pathlib.Path('outputs/2026-directory'); rows=json.load(open(r/'organizations.json'))
p=json.load(open('work/research-2026/reviewed.json')); published=json.load(open('work/research-2026/publication.json'))
merges=json.load(open('lobbying-map/research/verified-entity-merges.json'))
canonical={id:m['canonical_id'] for m in merges for id in m['source_ids']}
split_names={c['id']:c['aliases'] for d in json.load(open('lobbying-map/research/verified-entity-splits.json')) for c in d['children']}
ownership_categories=json.load(open('lobbying-map/lib/ownership-categories.json'))
for row in rows:
 row['canonical_organization_id']=canonical.get(row['id'],row['id'])
 if row['id'] in split_names:row['filing_names']=' | '.join(split_names[row['id']])
 if row['id'] not in p:continue
 v=p[row['id']]
 for a,b in [('name','name'),('description','description'),('organization_type','kind'),('ownership','ownership'),('website','website'),('website_status','website_status'),('logo_url','logo_url'),('logo_kind','logo_kind'),('logo_background','logo_background'),('source_tier','status'),('individual_review','review_outcome'),('checked_at','checked_at'),('notes','notes')]:row[a]=v.get(b,'')
 row['legal_form']=v.get('legal_form','')
 row['sources']=' | '.join(s['url'] for s in v['sources'])
 row['ownership_category']='Government body' if v.get('ownership')=='Not applicable' and v.get('kind')=='Government' else ownership_categories.get(v.get('ownership','Unknown'),'Other ownership')
assert len(rows)==18036 and sum(x['individual_review']!='not_individually_reviewed' for x in rows)==len(p)
(r/'organizations.json').write_text(json.dumps(rows,indent=2)+'\n')
with (r/'organizations.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
publication=f"Last recorded deployment: {published.get('status', 'unknown')} at {published.get('verified_at', 'unknown time')}; live data comparison: {'verified' if published.get('live_bytes_verified') else 'not performed'}."
if published.get("local_changes_pending"):
 publication = "Current exports are local and await publication. " + publication
 failure = published.get('pending_publication_attempt', {}).get('last_failed_upload', {}).get('failure')
 if failure:
  publication += " Last source upload failed; current corrections are not confirmed live."
s={'year':2026,'total_directory_entries':len(rows),'displayed_organizations':len({x['canonical_organization_id'] for x in rows}),'individually_reviewed':len(p),'not_yet_individually_reviewed':len(rows)-len(p),'review_outcomes':dict(collections.Counter(x['individual_review'] for x in rows)),'exported_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publication':publication,'complete':False}
s['profiles_with_research_record'] = len(p)
s['identity_confirmed'] = s['review_outcomes'].get('confirmed', 0)
s['identity_incomplete'] = len(rows) - s['identity_confirmed']
s['review_count_definition'] = 'individually_reviewed counts profiles with a saved research record, including partial and unresolved; it does not mean completed or verified.'
s['verified_websites'] = sum(v.get('website_status') == 'verified' for v in p.values())
s['official_logo_assets'] = sum(v.get('logo_status') == 'official_site_asset' and v.get('logo_kind') == 'logo' for v in p.values())
(r/'progress.json').write_text(json.dumps(s,indent=2)+'\n')
f=r/'README.md';f.write_text(re.sub(r'the \d+ entries reviewed',f'the {len(p)} entries reviewed',f.read_text()))
out=pathlib.Path('outputs/2026-research-trial');fields=['id','name','description','kind','ownership','legal_form','website','logo_url','logo_kind','logo_background','review_outcome','checked_at','sources']
with (out/'profiles.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for k,v in p.items():w.writerow({**{field:v.get(field,'') for field in fields},'id':k,'sources':' | '.join(s['url'] for s in v['sources'])})
(out/'current-progress.json').write_text(json.dumps({**s,'websites':sum(bool(v.get('website')) for v in p.values()),'branding':dict(collections.Counter(v.get('logo_kind') or 'missing' for v in p.values()))},indent=2)+'\n')

import subprocess
subprocess.run(["python3", "lobbying-map/scripts/export-resolved-2026.py"], check=True)

# Use the resolved entity count consistently in both progress outputs.
resolved_progress=json.loads((r/"progress.json").read_text())
trial_progress=json.loads((out/"current-progress.json").read_text())
trial_progress["displayed_organizations"]=resolved_progress["displayed_organizations"]
trial_progress["resolved_export_scope"]=resolved_progress["resolved_export_scope"]
(out/"current-progress.json").write_text(json.dumps(trial_progress,indent=2)+"\n")
print(resolved_progress)
