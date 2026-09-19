import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));before={};dec=[];assert not (r/'featured99-before.json').exists()
rows=json.load(open(r/'featured99-first10.json'));names=['Wray Community District Hospital','WeightWatchers (WW International, Inc.)','Wynn Resorts','X-Bow Launch Systems, Inc.','Xcel Energy','Zipline','Zocdoc','Zurich American Insurance Company']
def src(u,c):return dict(url=u,label='Primary organization evidence',claim=c)
for idx,d in enumerate(rows):
 i=d['id'];before[i]=json.loads(json.dumps(p[i]));f=dict(name=names[idx],description=d['description'],kind=d['kind'],ownership=d['ownership'],review_outcome='confirmed',notes=d['evidence'],website=d['website'],website_status='verified',status='sourced',checked_at='2026-09-13',as_of='2026-09-13');s=[src(d['official_url'],d['evidence'])]
 if idx==0:
  f['website']='https://wrayhealth.com/';f['notes']='Current Wray Health contact page explicitly retains Wray Community District Hospital and Clinic name and address. Former wrayhospital.org URL failed direct retrieval; current domain used. District-wide brand includes other facilities, which are not merged into hospital identity.';s=[src('https://wrayhealth.com/contact/','Current official contact page explicitly identifies Wray Community District Hospital and Clinic at 1017 W 7th St in Wray.'),src('https://wrayhealth.com/','Current district site describes hospital, emergency, outpatient and clinic services.')]
 if idx==1:
  f['ownership']='Public company';f['notes']='August 5 2026 official earnings release identifies WW International Inc. as Nasdaq WW and documents emergence from financial reorganization June24 2025. Current listing checked rather than inferred from predecessor stock.';s=[src('https://corporate.ww.com/news/news-details/2026/Weight-Watchers-Announces-Second-Quarter-2026-Results/',f['notes'])]
 if idx==2:f['notes']='2025 Form 10-K confirms Wynn Resorts Limited, its resort business and Nasdaq-listed WYNN common stock.';s=[src(d['official_url'],f['notes'])]
 if idx==3:
  f['notes']='Official terms explicitly identify X-Bow Launch Systems Inc. as operator of xbowsystems.com; exact corporate name bridge established.';s=[src('https://www.xbowsystems.com/terms-and-conditions/',f['notes']),src('https://www.xbowsystems.com/','Official website describes solid rocket motors and defense and space technology; header uses the downloaded, visually verified X-Bow wordmark.')];f.update(logo_url='https://www.xbowsystems.com/wp-content/uploads/2021/06/XBow.png',logo_source_url='https://www.xbowsystems.com/terms-and-conditions/',logo_kind='logo',logo_status='official_site_asset',logo_background='light')
 if idx==4:
  f['description']='Xcel Energy is the publicly traded parent of regulated electricity and natural-gas utilities operating across multiple U.S. states.';f['kind']='Utility holding company';f['notes']='2025 SEC Form10-K identifies Xcel Energy Inc. and Nasdaq XEL common stock; operating subsidiaries remain distinct.';s=[src(d['official_url'],f['notes'])]
 if idx==7:
  f['ownership']='Subsidiary';f['description']='Zurich American Insurance Company is a U.S. insurance underwriting subsidiary within Zurich Insurance Group.';f['notes']='2025 audited group financial statements table27.1 explicitly lists exact Zurich American Insurance Company, New York, at100percent ownership and voting rights; distinct from Zurich American Life Insurance Company.';s.append(src('https://www.zurich.com/-/media-assets/project/zurich/dotcom/investor-relations/docs/results/2025/q4/consolidated-financial-statements-annual-results-2025.pdf',f['notes']))
 f['identity_evidence']=f['notes'];p[i].update(f);bad={d['official_url']}-{x['url'] for x in s};byurl={x['url']:x for x in p[i].get('sources',[]) if x['url'] not in bad}
 for x in s:byurl[x['url']]=x
 p[i]['sources']=list(byurl.values());dec.append(dict(id=i,decision=f['review_outcome'],notes=f['notes'],sources=s))
(r/'featured99-before.json').write_text(json.dumps(before,indent=2)+'\n');(r/'featured99-decisions.json').write_text(json.dumps(dec,indent=2)+'\n')
for path in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
print('New confirmed',sum(p[i]['review_outcome']=='confirmed' and b['review_outcome']!='confirmed' for i,b in before.items()));print('Status changes',[(i,b.get('status'),p[i]['status']) for i,b in before.items() if b.get('status')!=p[i]['status']])
