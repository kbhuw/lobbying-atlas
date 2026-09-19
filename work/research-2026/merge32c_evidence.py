import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'append32c_root.py').read_text());index={x['id']:i for i,x in enumerate(rows)}
a=json.load(open(r/'round32c-first10-evidence.json'))
for k,v in a.items():
 i=index[k];own='Government body' if i in [0,1,3,4,5,6] else 'Nonprofit / tax-exempt' if i in [2,9] else 'Not applicable' if i==8 else 'Unknown'
 name='Sound Transit (Central Puget Sound Regional Transit Authority)' if i in [5,6] else v['name'];desc=v['description'];notes=v['notes'];outcome=None
 if i==1:desc='Public transit authority serving Greater Columbus and Central Ohio with bus, on-demand and paratransit services.'
 if i==7:notes='Official business identity established; current ownership not established. Corporate form alone does not prove private ownership.'
 if i==8:notes+=' Pension-fund sources do not independently establish every health and welfare entity encompassed by the broad filing label.';outcome='partial'
 add(i,name,desc,v['website'],kind=v['kind'],own=own,sources=[(s['url'],s['claim']) for s in v['sources']],notes=notes,outcome=outcome)
(r/'general-round32c-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print(len(p),'drafts assembled')
s=(r/'check_general32b.py').read_text().replace('32b','32c');(r/'check_general32c.py').write_text(s)
