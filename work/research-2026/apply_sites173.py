import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));xs=json.load(open(r/'legal-sites169-review.json'));assert not (r/'featured173-before.json').exists();before={};dec=[]
for n in [3,26]:
 v=xs[n];i=v['id'];assert p[i]['review_outcome']!='confirmed';before[i]=copy.deepcopy(p[i])
 if n==3:
  e=json.load(open(r/'featured173-aem-evidence.json'));assert e['http_status']==200
  note='Union Park Capital explicitly names Advanced Environmental Monitoring Holdings, says it formed the group in 2018 and links aem.eco. Its portfolio page describes weather, hydrology, air and soil monitoring businesses. This bridges the filed holding-company name to the AEM brand; historical formation does not establish a current ownership percentage.'
  description='A group of environmental-monitoring businesses providing weather, water, air and soil measurement technology and related services.'
 else:
  e=json.load(open(r/'featured173-amg-web-evidence.json'))
  note='Official AMG Vanadium About page explicitly names AMG Vanadium LLC in Cambridge, Ohio, and identifies it as a subsidiary of AMG Critical Materials NV. It describes spent-refinery-catalyst recycling and ferroalloy production. The subsidiary website replaces the generic parent website. Primary page was read through web.open after local HTTP403; environmental superlatives and conversion rates are not independently verified.'
  description='Recycles spent oil-refinery catalysts and other vanadium-bearing materials to produce ferrovanadium and other alloys for steelmaking.'
  p[i]['website']='https://amg-v.com/';p[i]['ownership']='Subsidiary of AMG Critical Materials N.V.'
 p[i].update(description=description,review_outcome='confirmed',website_status='verified',notes=note,identity_evidence=note,checked_at='2026-09-13',as_of='2026-09-13')
 ss={s['url']:s for s in p[i]['sources']};ss[e['url']]={'url':e['url'],'label':'Primary organization identity evidence','claim':note};p[i]['sources']=list(ss.values());dec.append(dict(id=i,name=p[i]['name'],notes=note,evidence=e))
for name,value in [('before',before),('decisions',dec)]: (r/f'featured173-{name}.json').write_text(json.dumps(value,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False));print(len(dec),'confirmed')
