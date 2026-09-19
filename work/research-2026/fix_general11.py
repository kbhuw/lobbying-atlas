import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round11-90-draft.json'));rows={v['id']:v for b in ['a','b','c'] for v in json.load(open(r/f'general-round11-{b}-input.json'))}
def src(k,u,d):p[k]['sources'].append(dict(url=u,label='Primary organization evidence',claim=d))
for k in ['abb61594b355269a','be15ee16304d6817','584ac28bd6af70b8','3584a7996699e30d','ecd1e600468f8689']:
 p[k]['ownership']='Nonprofit / tax-exempt';src(k,p[k]['website'],'Official organization page identifies the organization as nonprofit.')
p['584ac28bd6af70b8']['legal_form']='501(c)(6)'
p['1e926be1648f5f99']['ownership']='Unknown';p['1269e27fef4598f4']['ownership']='Subsidiary';p['1269e27fef4598f4']['notes']+=' Parent private/public status not established.'
for k in ['84e9200f3e72f7c9','8537d02ba2368d07']:
 p[k].update(ownership='Nonprofit / tax-exempt',legal_form='501(c)(6)');src(k,'https://www.apa.org/events/apasi-cancel-policy','American Psychological Association Services Inc. is a Section 501(c)(6) organization.')
p['228c67e8c491c339']['ownership']='Nonprofit / tax-exempt';src('228c67e8c491c339','https://sites.aph.org/','APH identifies itself as a 501(c)(3) nonprofit organization.')
p['18d5f643748a2875']['ownership']='Not applicable'
for k,v in p.items():
 if v['review_outcome']=='unresolved':
  v['sources']=rows[k].get('profile',{}).get('sources',[]) or v.get('sources',[])
  v['description']='Lobbying client whose exact identity and current activities have not yet been independently established.';v['kind']='Unknown'
# Correct unrelated domains.
for k,u,d in [('043dc478592f4d6b','https://alanational.org/','Trade association supporting companies selling products and services through military commissaries, exchanges and related military retail channels.'),('8977b1a8fd83e143','https://www.americanlivestock.org/adt','Association representing livestock markets and dealers, including advocacy and guidance on animal-disease traceability requirements.')]:
 p[k].update(website=u,description=d,identity_evidence='Exact association name and sector identified on official site.',sources=[dict(url=u,label='Official association page',claim=d)],notes='Previously suggested unrelated domain rejected during root review.')
# Exact subsidiary pages and name-change evidence.
u='https://www.rheinmetall.com/en/company/subsidiaries/american-rheinmetall'
for k in ['47086cad36fe0b48','dccb1b1056e421ef']:
 p[k].update(website=u,description='U.S. defense business supplying tracked and wheeled vehicles, components and related military systems under the American Rheinmetall brand.',ownership='Subsidiary',review_outcome='partial');p[k]['sources']=[dict(url=u,label='Official subsidiary page',claim='American Rheinmetall Vehicles LLC does business as American Rheinmetall; the site describes military vehicle systems and components.')];p[k]['identity_evidence']='Official subsidiary page links the Vehicles name and American Rheinmetall brand.';p[k]['notes']='Filing names retained separately; source documents shared operating brand.'
p['2e8df3e4a6773d21'].update(website='https://www.rheinmetall.com/en/company/subsidiaries/american-rheinmetall-munitions',ownership='Subsidiary',review_outcome='confirmed');p['2e8df3e4a6773d21']['sources']=[dict(url=p['2e8df3e4a6773d21']['website'],label='Official subsidiary page',claim='American Rheinmetall Munitions Inc. is a registered DBA of American Rheinmetall Munition Inc. and part of the Weapon and Ammunition division.')]
p['d5287776e828eeee'].update(website=u,ownership='Subsidiary',review_outcome='partial');src('d5287776e828eeee','https://www.rheinmetall.com/en/media/news-watch/news/2025/07/2025-07-08-american-rheinmetall-systems-joins-american-rheinmetall-as-a-unified-business-entity','American Rheinmetall Systems announced it would operate under the American Rheinmetall name.');p['d5287776e828eeee']['notes']='Official announcement documents shared American Rheinmetall operating name; filing legal name retained.'
for k,n in {'0e685b6260c73670':'American Olive Oil Producers Association','c0f5745a21a1ef3b':'American Organization for Nursing Leadership','6d3814cd85089aff':'American Pet Products Association','4423580555620d28':'American Petroleum Institute','fe1a037525e3b8b5':'American Pistachio Growers','84e9200f3e72f7c9':'American Psychological Association Services, Inc.','de6352f91fc88e59':'American Property Casualty Insurance Association'}.items():p[k]['name']=n
for k in ['3709d774aa96f82b','49d44b3e2e6cd970','7b77a6ec0d852b72','abb61594b355269a']:p[k]['featured']=True
(r/'general-round11-90-draft.json').write_text(json.dumps(p,indent=2)+'\n')
exec((r/'check_general11.py').read_text().split('profiles=json.load')[0])
for k in ['043dc478592f4d6b','8977b1a8fd83e143','47086cad36fe0b48','dccb1b1056e421ef','2e8df3e4a6773d21','d5287776e828eeee']:
 _,c=one((k,p[k]));print(k,c.get('http_status'),c.get('error',''),flush=True)
