import json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parents[2];master=ROOT/'work/research-2026/reviewed.json';p=json.load(open(master));shutil.copyfile(master,R/'first20-before.json');q=json.load(open(R/'matches.json'))[:20];skip={'caa1579c5c5c0dc5','c8db79d10e008f3d'};audit=[]
for item in q:
 i=item['id'];x=p[i];m=item['matches'][0];e=m['registration']
 if i in skip:audit.append({'id':i,'decision':'partial','reason':'Group/brand website and common address do not yet prove exact operating legal entity.'});continue
 assert x['review_outcome']=='partial'
 proof=f"Official organization page matches the filed name or documented operating name and its address: {e['address']}, {e['city']}, {e['state']}. Matched source: {e['archive']} / {e['member']}."
 if i=='f5412a36b84e7087':proof='Arcfield’s official AFLCMC/XA contract page explicitly names Analex Corporation as contract holder (CAGE 05BD6) and lists 14295 Park Meadow Drive, Chantilly, matching the Analex dba Arcfield registration.'
 if i=='329e8184b8586ed1':proof='The official page names Angel Adoption, Inc. at 820 E. Terra Cotta Avenue, Suite 149, Crystal Lake, matching the client address. Separately listed affiliated agencies and LifeLong Adoptions at Suite 145 are not substituted.'
 if i=='106e00cc6c0f64a9':proof='Official contact page explicitly labels the mailing address Arcadia Solutions, LLC, 100 Summit Drive, Burlington, MA, matching the client registration. The website footer also names Arcadia Solutions, LLC.'
 x.update(review_outcome='confirmed',website_status='verified',checked_at='2026-09-12',as_of='2026-09-12',identity_evidence=proof)
 x['sources'] += [{'url':m['page_url'],'label':'Official identity and address checked September 12, 2026','claim':proof},{'url':e['source_url'],'label':'Original House registration '+e['member'],'claim':f"Reports {e['client_name']} at {e['address']}, {e['city']}, {e['state']}; activity: {e['description']}."}]
 if i=='15ff0ecb9a8054ec':x['legal_form']='Public-benefit corporation';x['notes']='Official press material identifies ApiJect Systems Corp. as a public-benefit medical technology company. Public-benefit status does not mean publicly traded; ownership remains unverified.'
 if i=='106e00cc6c0f64a9':x['legal_form']='Limited liability company (LLC)'
 if i=='e6ceebf83e8da7f7':x['legal_form']='Corporation'
 if i=='fb10f4a685798fbb':x['legal_form']='Limited partnership (LP)'
 audit.append({'id':i,'decision':'identity_confirmed','proof':proof,'source':m,'ownership_changed':False})
for target,indent in [(master,2),(ROOT/'lobbying-map/research/reviewed-2026.json',None),(ROOT/'outputs/2026-research-trial/profiles.json',2)]:target.write_text(json.dumps(p,indent=indent,ensure_ascii=False)+'\n')
(R/'first20-decisions.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print('18 identity confirmations;2 retained partial. Ownership qualifications preserved.')
