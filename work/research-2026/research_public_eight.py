import json,pathlib,copy
r=pathlib.Path('work/research-2026');reg=json.load(open('work/organization-research/registry-profiles.json'));out={}
rows=[
('bd48b4c406f94175','Abbott Laboratories','Develops medical devices, diagnostic tests, medicines, and nutrition products.','https://www.abbott.com/','https://www.abbott.com/en-us/about-abbott'),
('0dcac80f2cc8c608','AbbVie','Biopharmaceutical company developing and commercializing medicines.','https://www.abbvie.com/','https://www.abbvie.com/who-we-are.html?sf279148156=1'),
('ee610f39842879b0','Adobe','Software company providing tools for creative work, digital documents, and digital experiences.','https://www.adobe.com/','https://www.adobe.com/about-adobe.html'),
('db5c9689b9083624','AT&T','Provides wireless communications, broadband internet, and business connectivity services.','https://about.att.com/','https://about.att.com/pages/corporate-profile'),
('87cd4e316ffb09c7','Autodesk','Develops design and engineering software for architecture, construction, manufacturing, and media.','https://www.autodesk.com/','https://www.autodesk.com/company/newsroom/corporate-info'),
('74c7732f67cdd9b3','Amgen','Biotechnology company researching, developing, and manufacturing medicines.','https://www.amgen.com/','https://www.amgen.com/about'),
('7b16082d50ca9c1a','Aflac','Insurance group offering supplemental coverage for accidents, illnesses, and related financial needs.','https://www.aflac.com/','https://www.aflac.com/about-aflac/our-company/'),
('f1f1d3ff6a0c4bda','American International Group (AIG)','Insurance group providing commercial and personal insurance and risk-management services.','https://www.aig.com/','https://www.aig.com/home/about')]
for k,name,desc,url,source in rows:
 base=reg[k];sec=json.load(open('work/organization-research/sec-submissions/'+base['registry']['id']+'.json'))['data'];assert sec.get('tickers') and sec.get('exchanges')
 v={'name':name,'description':desc,'kind':'Business','ownership':'Publicly traded','website':url,'website_status':'verified','status':'sourced','review_outcome':'confirmed','featured':True,'legal_form':'','as_of':'2026-09-05','checked_at':'2026-09-05','logo_url':'','logo_kind':'','logo_source_url':'','logo_status':'unresolved','sources':copy.deepcopy(base['sources']),'notes':'The listed corporation is identified by its SEC CIK and corroborated by the official corporate website. Highlighting is an editorial aid for recognizable organizations, not a lobbying-impact score.','identity_evidence':'SEC CIK '+base['registry']['id']+'; SEC legal name '+sec['name']+'. The source match also corroborates the lobbying client name and city/state.'}
 v['sources'][0]['claim']+=' Listing: '+', '.join(e.upper()+': '+t for e,t in zip(sec['exchanges'],sec['tickers']))+'.'
 v['sources'].append({'label':'Official company overview','url':source,'claim':desc})
 if k=='0dcac80f2cc8c608':v['notes']+=' AbbVie became separate from Abbott in 2013; the two directory identities remain separate.'
 out[k]=v
(r/'public-eight.json').write_text(json.dumps(out,indent=2)+'\n')
