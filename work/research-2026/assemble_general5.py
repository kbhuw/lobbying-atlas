import json,pathlib
r=pathlib.Path('work/research-2026')
def read(f):return json.load(open(r/f))
p={}
for l in 'abc':
 d=read(f'general-round5-{l}-researched.json');d={v['id']:v for v in d} if isinstance(d,list) else d
 assert set(d)=={v['id'] for v in read(f'general-round5-{l}-input.json')};p.update(d)
for k,a in read('general-round5-a-audit.json').items():
 # Agent transcribed AIM's ID onto Aimpoint correction. Keep each identity separate.
 if k=='2a2aaa9bebeb01f7':k='b290f27e4fbd525d'
 if a.get('correction'):
  p[k].update(a['correction']);p[k]['identity_evidence']=a['identity_notes']
  if a.get('source_url') and a['source_url']!='https://lda.gov/api/v1/clients/':p[k]['sources'].append(dict(url=a['source_url'],label='Primary identity correction',claim=a['source_excerpt']))
for k,a in read('general-round5-b-audit.json')['profiles'].items():
 for c in a['corrections']:
  if c['field'] in ['name','description','ownership','website']:p[k][c['field']]=c['value']
  if c.get('source'):p[k]['sources'].append(dict(c['source'],label='Primary identity correction'))
for a in read('general-round5-c-audit.json')['records']:
 k=a['id']
 # Retain a represented client's own site, identified explicitly in notes; exclude intermediary sites.
 if a.get('website_correction') is not None and not ('on behalf of' in p[k]['name'] and p[k].get('website') and 'akingump.com' not in p[k]['website']):p[k]['website']=a['website_correction']
 if a.get('ownership_correction') is not None:p[k]['ownership']=a['ownership_correction']
 p[k]['sources']+=a.get('sources',[])
 if a['identity_decision'] in ['partial','unresolved']:p[k]['review_outcome']=a['identity_decision']
 if 'on behalf of' in p[k]['name']:
  p[k]['notes']='The disclosed entry names Akin Gump as an intermediary acting on behalf of the represented client. Description and website describe the represented client; this entry has not been merged with either party.'
  p[k]['review_outcome']='partial'
def fix(k,u,desc,claim=None):
 p[k].update(website=u,description=desc,status='sourced',review_outcome='partial',identity_evidence=claim or desc)
 p[k]['sources'].append(dict(url=u,label='Official organization source',claim=claim or desc))
fix('6a7034c8f96749f1','https://www.agrippaindustries.com/','Maritime logistics company serving commercial and other partners.','Official website identifies Agrippa Industries Inc. and describes maritime logistics services.')
fix('7f0e3a84eff8259a','https://akoya.com/','Financial technology company operating a network for permissioned sharing of financial account data between financial institutions and financial applications.')
p['7f0e3a84eff8259a']['notes']='This profile describes the financial-technology client active in 2026. Older same-name filings from 2005–2007 have not been established as belonging to that company; the directory currently groups names rather than proving historical legal identity.'
p['36b3142c687d2342'].update(description='Manufactures air-distribution and ventilation products used in heating, ventilation and air-conditioning systems.',review_outcome='partial',status='sourced',identity_evidence='Official Air Distribution Technologies website identifies the company and HVAC product businesses; exact ownership is unverified.')
p['2b9adca9ed52d3ea'].update(ownership='Unknown',legal_form='Colorado public benefit corporation')
p['60d53c98bf5c7962'].update(description='California limited liability company identified in Santa Nella project records. Its lobbying registration describes real-estate development; current ownership and a standalone website remain unverified.',review_outcome='partial',status='sourced',legal_form='California limited liability company',identity_evidence='Merced County project agreement and LEI 549300G48XK5U1YY2V36 identify the exact legal name, with a Sacramento address care of AKT Investments.')
for k in ['1ce2145aa67a0638','f9d16dd67d276a91']:
 p[k]['sources']=[s for s in p[k]['sources'] if 'akingump.com' not in s['url']]
p['5b76d480a15fb3b6']['ownership']='Subsidiary of public company'
p['6b315e882527cd6b']['ownership']='Unknown'
p['cf931b0087558406'].update(website='',review_outcome='partial',identity_evidence='The disclosure identifies Airdex doing business as ATA Aviation. Similar-name websites could not establish the exact legal entity and have been withheld.')
p['cf931b0087558406']['sources']=[s for s in p['cf931b0087558406']['sources'] if 'ataaviation.com' not in s['url']]
for l in 'abc':
 for v in read(f'general-round5-{l}-input.json'):p[v['id']]['sources']+=v.get('profile',{}).get('sources',[])
for k in ['7cdf5e68c9e5d28d','c5da7c809a65b7f6','414462c5d5d58148','8682afb14bfecaac']:p[k]['featured']=True
(r/'general-round5-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
