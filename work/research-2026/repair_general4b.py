import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round4-90-draft.json'));a=json.load(open(r/'general-round4-b-audit.json'))['profiles']
for k,v in a.items():
 p[k]['sources']=[s for s in p[k]['sources'] if not s['claim'].startswith('Official site reviewed')]+[dict(s,label='Primary source audit') for s in v['source_claims']]
 for c in v['corrections']:
  if c['field'] in ['description','ownership','website']:p[k][c['field']]=c['value']
 if v['decision']=='hold':p[k]['review_outcome']='partial' if p[k].get('website') else p[k]['review_outcome']
# Exact operating entities are distinguished from the listed issuer.
for k in ['0777610248c84880','66c89f4b9c993764']:p[k].update(ownership='Unknown',review_outcome='partial');p[k]['notes']='Official group website supports the business; the exact disclosed legal entity relationship to the listed issuer remains unverified.'
p['6b54662afba94dc0']['ownership']='Subsidiary of public company'
p['3e879cb44ebd4a76']['ownership']='Subsidiary of public company'
p['c233123841a34c66']['description']='Develops foam-based engine cleaning systems for commercial and military aircraft.'
p['5437fdae0990a738']['description']='Develops stratospheric balloons, radar systems and protective wear for aerospace and defense applications.'
def fix(k,u,desc):
 p[k].update(website=u,description=desc,status='sourced',review_outcome='partial',identity_evidence='Official organization page identifies the distinctive disclosed name and matching business activities; ownership is not independently established.')
 p[k]['sources'].append(dict(url=u,label='Official organization website',claim=desc))
fix('f791a5f2205cc084','https://aeryaviation.com/about/','Engineers, modifies, maintains and operates aircraft for government, defense, medical-transport and commercial customers.')
fix('c2e61b7c073e462b','https://www.aepartners.com/','Provides financing and tax-credit syndication services for developers and investors building or preserving affordable multifamily housing.')
fix('2278d48683bdf49c','https://www.aesirtec.com/','Develops nickel-zinc batteries for critical infrastructure, defense and aerospace applications, with facilities in Joplin, Missouri and Bozeman, Montana.')
p['2278d48683bdf49c']['sources']=[s for s in p['2278d48683bdf49c']['sources'] if 'aesirtech.com' not in s['url']]
for k,domain in [('3e64b5dc3b0fdce7','affordgroup.com'),('2b1925f86a572531','ahdc.org'),('f8102d7f947fe805','aerospaceaz.org')]:
 p[k].update(website='',website_status='unresolved',review_outcome='partial');p[k]['sources']=[s for s in p[k]['sources'] if domain not in s['url']];p[k]['identity_evidence']='Disclosure identifies the organization and reported activities. The proposed website was parked or could not be corroborated and was excluded.'
 p[k]['notes']='Current official website remains unverified.'
p['4ceb3d4f117c77df']['sources'].append(dict(url='https://aerospacecolorado.org/',label='Official association website',claim='Aerospace Colorado describes a member-driven association promoting the Colorado aerospace and defense industry, with a Westminster address.'))
(r/'general-round4-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
