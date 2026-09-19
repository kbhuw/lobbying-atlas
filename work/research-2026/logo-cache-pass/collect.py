import json,pathlib,concurrent.futures,subprocess,sys,re
root=pathlib.Path('work/research-2026');profiles=json.loads((root/'reviewed.json').read_text());folder=root/'logo-cache-pass'/sys.argv[1];folder.mkdir(exist_ok=True)
exclude={'09972fc29d90f84f','04d0999d14efc462','05408f3dbd828326'}
for review in (root/'logo-cache-pass').glob('**/review.json'):
 exclude.update(json.loads(review.read_text()).get('deferred',{}))
jobs=[]
prior_holds={}
for k,p in profiles.items():
 if p.get('logo_url') or not p.get('website') or k in exclude:continue
 evidence=str(p.get('identity_evidence',''))+' '+str(p.get('notes',''))
 if re.search(r'(?:logo|branding|brand asset).{0,35}(?:held|not assigned)|(?:held|not assigned).{0,35}(?:logo|branding)',evidence,re.I):
  prior_holds[k]={'name':p['name'],'reason':evidence}
  continue
 f=root/'website-cache'/f'{k}.json'
 if not f.exists():continue
 c=json.loads(f.read_text())
 if c.get('logo_kind')!='logo' or not c.get('logo_url'):continue
 jobs.append(dict(id=k,name=p['name'],url=c['logo_url'],source=c['logo_source_url'],description=p['description']))
 if len(jobs)==(int(sys.argv[2]) if len(sys.argv)>2 else 24):break
def fetch(j):
 o=folder/(j['id']+'.asset');r=subprocess.run(['curl','-fLsS','--max-time','20',j['url'],'-o',str(o)],capture_output=True);j['download_ok']=r.returncode==0
 if j['download_ok']:
  preview=folder/(j['id']+'.png');r=subprocess.run(['magick','-background','#d6dbe0',str(o),'-alpha','remove','-resize','360x130','-gravity','center','-extent','380x150',str(preview)],capture_output=True);j['preview_ok']=r.returncode==0
 return j
results=list(concurrent.futures.ThreadPoolExecutor(6).map(fetch,jobs));(folder/'candidates.json').write_text(json.dumps(results,indent=2)+'\n')
for i,j in enumerate(results):print(i,j['id'],j['name'],j['download_ok'],j.get('preview_ok'))

(folder/'prior-identity-holds.json').write_text(json.dumps(prior_holds,indent=2)+'\n')
print('Skipped',len(prior_holds),'previously documented identity holds without downloading again')
