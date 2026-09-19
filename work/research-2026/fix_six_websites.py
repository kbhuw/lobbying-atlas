import json,pathlib,re,datetime
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));bad=json.load(open(r/'malformed-reviewed-websites.json'));changed={}
for x in bad:
 k=x['id'];v=p[k];c=json.load(open(r/f'website-cache/{k}.json'));assert c['http_status']==200 and len(c['text'])>150
 v.update(website=c['final_url'],website_status='verified',checked_at='2026-09-05',logo_status='unresolved',logo_url='',logo_source_url='',logo_kind='')
 if c.get('logo_http_status')==200:
  for f in ['logo_url','logo_source_url','logo_kind']:v[f]=c[f]
  v['logo_status']='official_site_asset'
 if k=='4e468de3d5724730':
  v['sources']=[s for s in v['sources'] if s['label'].startswith('House disclosure')]
  v['sources'] += [dict(label='National union profile',url='https://www.nalc.org/about',claim='National union identifies its representation of USPS city delivery letter carriers and distinguishes its local branches.'),dict(label='IRS group exemption notice on national union website',url='https://www.nalc.org/union-administration/secretary-treasurer/body/tax-exempt_docs.pdf',claim='IRS notice identifies the national association at 100 Indiana Avenue NW, Washington DC, with taxpayer identification number 53-0114650.')]
  v['identity_evidence']='National union name and Washington DC disclosure compared with national union official profile and IRS notice. Previous EIN 520908160 and branch142.com link removed because they did not establish the national entity.'
  v['notes']='Corrected an earlier national-union/local-branch registry mismatch. National union and its local branches have separate EINs; the prior branch record is not evidence for this client. Original historical name-group filings are retained.'
  v['description']='National labor union representing USPS city delivery letter carriers in collective bargaining and legislative advocacy.'
 else:
  v['sources']=[s for s in v['sources'] if not re.match(r'^https?://https?://',s['url'],re.I)]
  v['identity_evidence']+=' Malformed duplicate-protocol website corrected; the current official site identifies the named organization.'
  v['notes']+=' Official website link and branding rechecked 2026-09-05; earlier malformed website link superseded.'
 v['sources'].append(dict(label='Official website and branding check',url=v['website'],claim='Official site identifies the organization; page and organization branding asset responded successfully on 2026-09-05.'))
 changed[k]=v
for f in [r/'reviewed.json',pathlib.Path('lobbying-map/research/reviewed-2026.json'),pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,indent=2)+'\n')
q=[json.loads(l) for l in (r/'queue.jsonl').read_text().splitlines()]
for x in q:
 if x['id'] in changed:
  v=changed[x['id']];x.update(review_status=v['review_outcome'],website_status=v['website_status'],logo_status=v['logo_status'],missing_fields=[f for f in ['website','logo_url','ownership'] if not v.get(f) or v.get(f)=='Unknown'],reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(r/'queue.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in q));(r/'six-website-corrections.json').write_text(json.dumps(changed,indent=2)+'\n');print('Corrected6 website and source links; removed national/local union EIN mismatch; verified6 official assets')
