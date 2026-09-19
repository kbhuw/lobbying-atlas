import json
from pathlib import Path
r=Path('work/research-2026');p=json.load(open(r/'reviewed.json'))
rows={
'968148990198f5c1':('https://www.smartlablearning.com/about/','The official SmartLab About page explicitly identifies Creative Learning Systems as the developer of its project-based STEM learning systems. The official privacy policy gives the same company name and Longmont, Colorado address. Operating identity confirmed; current equity ownership remains unknown.'),
'b4a2a2c9b952dc39':('https://www.sugaright.com/case-studies','The official Sugaright value-proposition page explicitly names CSC Sugar, LLC and its sugar-trading group. The About page identifies Sugaright as a wholly owned subsidiary of CSC Sugar. The linked CSC Sugar website independently identifies its trading/refining business and Westport, Connecticut office. Current ownership of CSC Sugar itself remains unknown; historical AMERRA-fund evidence is not promoted to current ownership.'),
'e9c12d8f5573cd36':('https://www.csiaviation.com/about/','The official About page names CSI Aviation, Inc., describes its earlier Charter Services, Inc. name and air charter/transportation business serving passenger, cargo and medical missions. Exact company identity confirmed. The company’s acquisition of another airline does not establish the ownership of CSI itself, which remains unknown.')
}
b=r/'featured326-before.json';assert not b.exists();b.write_text(json.dumps({i:p[i] for i in rows},indent=2,ensure_ascii=False)+'\n')
for i,(u,n) in rows.items():
 n+=' Direct official website bodies retrieved and reviewed September 14, 2026.'
 p[i].update(review_outcome='confirmed',checked_at='2026-09-14',notes=n,identity_evidence=n)
 p[i]['sources'].append({'url':u,'label':'Official company evidence reviewed September 14, 2026','claim':n})
p['b4a2a2c9b952dc39']['website']='https://www.cscsugar.com/'
p['b4a2a2c9b952dc39']['sources'].append({'url':'https://www.cscsugar.com/','label':'Official CSC Sugar website, directly retrieved September 14, 2026','claim':'CSC Sugar trading/refining identity and Westport Connecticut contact, linked by its Sugaright subsidiary.'})
p['e9c12d8f5573cd36']['legal_form']='Corporation'
(r/'reviewed.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')));Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n');(r/'featured326-decisions.json').write_text(json.dumps({i:p[i] for i in rows},indent=2,ensure_ascii=False)+'\n')
print('Three company identities confirmed; CSC Sugar website corrected.')
