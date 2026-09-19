import json,pathlib,concurrent.futures
r=pathlib.Path('work/research-2026');p={}
for s in ['a-rootchecked','b-researched','c-researched']:p.update(json.load(open(r/f'general-round25-{s}.json')))
for k,v in json.load(open(r/'general-round25-b-corrections.json')).items():
 old=p[k];v['sources'] += [s for s in old['sources'] if 'lda.gov' in s['url'] or 'house.gov' in s['url']];p[k]=v
p['ff0f25c824238a47'].update(description='Egis designs, engineers, and operates buildings and transport infrastructure worldwide. This filing names Bose Public Affairs as its representative.',ownership='Private company',notes='Egis reports ownership by Tikehau Capital funds (43%), Caisse des Dépôts (34%), and partners, managers and employees (23%).')
p['6ca0895f14a88ca0'].update(description='Cauldron develops continuous precision-fermentation technology for manufacturing ingredients and other biological products. Boundary Stone Partners represents it in this filing.',ownership='Private company',legal_form='Australian proprietary limited company',notes='Official privacy notice identifies Cauldron Molecules Pty Ltd. Individual shareholders were not established.')
k='207660a3e944c480';p[k].update(ownership='Unknown',review_outcome='partial',description='A Boston Scientific lobbying record with Office-Based Facility Association and former USPA wording in the disclosed name. Its filing context concerns medical devices and Medicare payment policy.',notes='The label combines a manufacturer and association names. Their exact legal relationship remains unresolved; no standalone nonprofit classification is assigned.')
p[k]['sources']=[s for s in p[k]['sources'] if 'legilist' not in s['url']]+[dict(url='https://lda.gov/filings/public/filing/1de6dafd-78e4-4fad-a8e9-4b4d1b404a9d/print/',label='Original LDA filing',claim='Original filing for the disclosed Boston Scientific / OBFA / former USPA name; legal relationship is held unresolved.')]
p[k]['identity_evidence']='Original filing name and medical-device context associate the record with Boston Scientific; the OBFA/USPA relationship is not independently resolved.'
for k in ['d7df59cb91f2ed5a','337df6b48f225132','ba22822239449fd9','af2e6d2421a5d742']:
 p[k].update(ownership='Unknown',review_outcome='partial');p[k]['notes']+=' Current exact-entity ownership was not established by the cited sources.'
p['af2e6d2421a5d742']['description']='Real-estate investment record associated with Boyd Watterson and properties leased to the U.S. General Services Administration. The exact investment vehicle remains only partly identified.'
p['7e83b6809f21c4ae']['sources']=[dict(url='https://lda.gov/api/v1/clients/63289/?format=json',label='LDA client record',claim='Ohio client self-reports "Botanicals for better health"; exact organizational identity remains unconfirmed.')]
p['7e83b6809f21c4ae']['description']='Ohio lobbying client that describes its activity as botanicals for better health. An official organization website and exact legal identity have not been confirmed.'
for k in ['cbf2c9ad35f9d2ef','8d367a0899de5033','ca9be504a0f1e7a6']:
 p[k]['notes']+=' '+p[k]['ownership'];p[k]['ownership']='Subsidiary / affiliated entity'
p['1798fd4f167d67c7']['ownership']='Private company'
for v in p.values():
 o=v['ownership']
 if o=='Public entity':v['ownership']='Government body'
 elif o.startswith('Nonprofit'):v['ownership']='Nonprofit / tax-exempt'
 elif o.startswith('Publicly traded'):v['ownership']='Publicly traded'
for k in ['830c580ec5f673e9','207660a3e944c480']:
 for s in p[k]['sources']:
  if 'sec.gov' in s['url']:s['claim']='SEC filing identifies Boston Scientific Corporation common stock listed as NYSE: BSX.'
# Hold Boryung ownership until primary registry response can be validated.
p['008eb8b1d6980f47'].update(ownership='Unknown',review_outcome='partial',notes='FSS/DART listing evidence could not be fetched during root review; exchange classification held pending validation.')
p['008eb8b1d6980f47']['sources'][0]['claim']='FSS/DART company record supplied as a registry reference; current listing and ownership require validation.'
p['008eb8b1d6980f47']['identity_evidence']='Official Boryung website and LDA client record identify the pharmaceutical business. Current listing evidence is pending verification.'
(r/'general-round25-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
exec((r/'check_general15.py').read_text().split('profiles=json.load')[0])
keys=['ff0f25c824238a47','6ca0895f14a88ca0','207660a3e944c480','37fe331e7b41be4f','d6bdb5da7eb8eea4']
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for k,c in ex.map(one,[(k,p[k]) for k in keys]):print(k,c.get('http_status'),c.get('logo_url'),flush=True)
for k,i in {'1cfd78d11b729527':2,'3f001ed32d6b8443':1,'4b22dc989064e7bd':1,'9e5eb2afa6da5082':1,'4748396f92400271':1}.items():
 path=r/f'website-cache/{k}.json';c=json.load(open(path));a=c['asset_candidates'][i]
 try:
  dest,mime,b=get(a['url']);assert mime.startswith('image/') and len(b)>80
  c.update(logo_url=a['url'],logo_kind=a['kind'],logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime);path.write_text(json.dumps(c,indent=2));print(k,'asset corrected',flush=True)
 except Exception as e:
  c.pop('logo_url',None);path.write_text(json.dumps(c,indent=2));print(k,str(e),flush=True)
