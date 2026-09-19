import json,pathlib,gzip
r=pathlib.Path('work/research-2026');f=r/'general-round24-root-draft.json';p=json.load(open(f))
for k,u,c in [('b5608e7236336c94','https://investors.boeing.com/investors/news/default.aspx','The current Boeing investor news site identifies the issuer as NYSE: BA.'),('47e612d9eac837a4','https://www.elanco.com/us/newsroom/press-releases/elanco-animal-health-reports-second-quarter-2026-results','The August 2026 results release identifies Elanco Animal Health Incorporated as NYSE: ELAN.')]:p[k]['sources'].append(dict(url=u,label='Current issuer evidence',claim=c))
p['47e612d9eac837a4'].update(name='Elanco Animal Health (via Bockorny Group)',description='Develops and markets medicines, vaccines, and other animal-health products for pets and farm animals.')
p['788143f001397c9f'].update(name='South Dakota State University (via Bockorny Group)',description='Public land-grant university in Brookings, South Dakota, providing education, research, and extension services.')
p['f01393daff8b320b']['name']='Transhumance Holding Company (via Bockorny Group)'
for k,v in p.items():
 v.setdefault('notes','');v.setdefault('featured',False)
 if not v.get('sources'):
  row=json.load(gzip.open(f'lobbying-map/public/data/reports/{k[:2]}.json.gz','rt'))[k][0]
  v['sources']=[dict(url=f"https://lda.gov/filings/public/filing/{row['id']}/print/",label='Lobbying disclosure',claim='Disclosed client label; exact standalone organizational identity remains unresolved.')];v['review_outcome']='unresolved'
f.write_text(json.dumps(p,indent=2)+'\n')
hold={'0257c6d2080bf7c4','e94643dd58155f56','d0b0b91706dbf8e6','d8a1dd0d78d8fb72','0466846622189eb1','82425b4b6da0b383','c99a636b9b8301ec','f7ca3490b44dfdfa','878c1369a88599f5','0b48abe64e1c6e36','230dde79c3e4d8fe','92056be6f3c2546a','59bf28014972933f'}
s=(r/'build_general23.py').read_text().replace('round23','round24');a=s.index('hold=');b=s.index('\nfor k,v',a);s=s[:a]+'hold='+repr(hold)+s[b:];(r/'build_general24.py').write_text(s)
