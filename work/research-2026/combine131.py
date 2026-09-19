import json,pathlib,re
r=pathlib.Path('work/research-2026');e={};rows=json.load(open(r/'general-round131-input.json'))
for label,start,end in [('a',0,34),('b',34,67),('c',67,100)]:
 p=json.load(open(r/f'round131-{label}-evidence.json'));assert set(p)=={x['id'] for x in rows[start:end]};e.update(p)
for k,v in json.load(open(r/'round131-root-patches.json')).items():
 v=dict(v);extra=v.pop('extra_sources',[]);e[k].update(v);e[k]['sources']+=extra
for v in e.values():
 if v['ownership'].lower() in ['publicly traded issuer','publicly traded','public company']:v['ownership']='Public company'
 if v['ownership']=='Unknown' and v['review_outcome']=='confirmed':v['review_outcome']='partial'
 v['name']=v['name'].replace('NEW York','New York').replace('NO Limits','No Limits').replace('NO More','No More').replace('NO Surprise','No Surprise')
 v['sources']=[s for s in v['sources'] if s.get('url')]
 if not v['website'] and all('lda.gov/' in s['url'] or 'disclosurespreview.house.gov/' in s['url'] for s in v['sources']):
  v['review_outcome']='unresolved'
  if not v.get('description'):v['description']='Federal lobbying client whose exact current organization identity has not been independently verified.'
assert len(e)==100
(r/'round131-root-incremental-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
print('Combined100withrootpatches')
