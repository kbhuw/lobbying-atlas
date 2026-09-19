import pathlib,json
r=pathlib.Path('work/research-2026');exec((r/'merge33a_first.py').read_text());a=json.load(open(r/'round33a-last10-evidence.json'))
for k,v in a.items():
 i=index[k];own='Government body' if i in [26,27,28] else 'Unknown' if i==25 else 'Nonprofit / tax-exempt';name=v['name'];notes=v['notes']
 if i==21:name='U.S. Chamber of Commerce'
 if i==22:name='The Digital Chamber (Chamber of Digital Commerce)'
 if i==23:name='Chamber of Industry of Guatemala'
 if i==24:name='Chamber of Marine Commerce'
 if i==25:name='Chamber of Shipping of America'
 if i==27:name='Cedar Port Navigation and Improvement District';notes+=' Original Chambers County Improvement District No. 1 filing name preserved; linked site concerns district navigation project.'
 if i==28:name='Champaign-Urbana Mass Transit District'
 add(i,name,v['description'],v['website'],kind=v['kind'],own=own,sources=[(s['url'],s['claim']) for s in v['sources']],notes=notes,outcome='partial' if i in [20,27] else None,featured=i in [21,22])
assert len(p)==30
(r/'general-round33a-root-draft.json').write_text(json.dumps(p,indent=2)+'\n');print('30 drafts assembled')
