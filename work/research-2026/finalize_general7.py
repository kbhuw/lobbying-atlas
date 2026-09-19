import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round7-90-draft.json'))
ev=json.load(open(r/'general7-ownership-evidence.json'))
for k,e in ev.items():
 v=p[k];v['sources'].append(dict(url=e['sourceurl'],label='Primary ownership evidence',claim=e['quoted_evidence']));v['notes']+=' '+e['reasoning']
for k in ['6ecfc0ce623a9639','010e841fa23be197']:p[k]['ownership']='Private company'
p['2079ca3d9dfbff35'].update(ownership='Subsidiary of public company',description='Insurance operating company within The Allstate Corporation, providing property and casualty insurance including auto and home coverage.')
p['855ee349b74b3e2f'].update(ownership='Unknown',review_outcome='partial');p['855ee349b74b3e2f']['notes']+=' The listed issuer is Allison Transmission Holdings Inc.; the filing’s shortened operating name does not establish that it names the holding company.'
p['d9940f9d7bd6ea65']['ownership']='Publicly traded';p['d9940f9d7bd6ea65']['sources'][-1]['claim']='Allianz SE registered shares trade on German exchanges, including Frankfurt and Xetra: ALV; ISIN DE0008404005.'
p['f5cb13ced71c58f0']['ownership']='Nonprofit / tax-exempt';p['f5cb13ced71c58f0']['sources'][-1]['claim']+=' The manifesto identifies the organization as a 501(c)(4).'
v=p['f3219ea81a0b59e8'];v.update(website='https://www.allianthealth.org/',ownership='Nonprofit / tax-exempt',review_outcome='partial');v['sources']=[s for s in v['sources'] if 'allianthealthsolutions.org' not in s['url']];v['sources'].append(dict(url=v['website'],label='Alliant Health Solutions official site',claim='Official site identifies nonprofit Alliant Health Solutions and its quality improvement, program integrity and care-management services.'))
p['78a58f16dff73e7d']['website']='https://www.alliesforcherrypoint.com/'
v=p['f82d5856e6d0feac'];v.update(website='',review_outcome='partial');v['notes']+=' The previously cited Wix address now redirects to Wix itself and is not presented as a current official website.'
for k in ['d9940f9d7bd6ea65','2079ca3d9dfbff35','e9905a95e1b8e317']:p[k]['featured']=True
for k,v in p.items():
 if v['name']=='Allliance Of Marine Mammal Parks And Aquariums':v['name']='Alliance of Marine Mammal Parks and Aquariums'
 if v['name']=='Alliant University F/k/a Alliant International University':v['name']='Alliant University'
 if v['name'].startswith('American Lightweight Materials'):v['name']='LIFT (American Lightweight Materials Manufacturing Innovation Institute)'
(r/'general-round7-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
s=(r/'build_general6.py').read_text().replace('general-round6','general-round7');a=s.index('hold=');b=s.index('\nfor k,v',a);s=s[:a]+"hold={'405b80eaef25fecd','f82d5856e6d0feac','e416e68aa7028661','4d3574b2aeef177c','8f2a84d9187690c0','7711126e69ef191e'}"+s[b:];(r/'build_general7.py').write_text(s)
f=pathlib.Path('lobbying-map/scripts/data/export_profiles.py');s=f.read_text().replace("'BUDAPEST:', 'EURONEXT:')","'BUDAPEST:', 'EURONEXT:', 'XETRA:')");f.write_text(s)
s=(r/'fix_general6icons.py').read_text().split('for k,index in')[0];s+="for k,index in [('8a5e68bdbd770cef',1),('8b4c57936d0c09a0',1),('feefb45d1e4506fa',1),('e6e9a1089268c4b2',2),('a2e1ead593a8ef2d',1),('997963fd1f79dfed',1)]:\n c=json.load(open(cache/(k+'.json')));a=c['asset_candidates'][index]\n try:\n  dest,mime,b=get(a['url'],1000000)\n  assert mime.startswith('image/') and len(b)>80\n  c.update(logo_url=a['url'],logo_kind=a['kind'],logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime)\n except Exception:\n  c.pop('logo_url',None)\n (cache/(k+'.json')).write_text(json.dumps(c,indent=2));print(k,'checked')\n";(r/'fix_general7icons.py').write_text(s)
s=(r/'check_general7.py').read_text().replace('if v.get("website")','if v.get("website") and k in ["f3219ea81a0b59e8","78a58f16dff73e7d"]');(r/'check_general7changes.py').write_text(s)
