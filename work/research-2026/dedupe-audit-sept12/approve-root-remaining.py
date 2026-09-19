import json,gzip,pathlib
r=pathlib.Path('work/research-2026/dedupe-audit-sept12');a=json.load(open('work/research-2026/duplicate-name-candidates-sept12.json'));p=json.load(open('work/research-2026/reviewed.json'));b={x['id']:x for x in json.load(gzip.open('lobbying-map/research/directory-base.json.gz','rt'))['companies']}
reasons={
26:'Both original labels explicitly identify GRAIL, Inc.; one retains a formerly LLC qualifier. Both confirmed profiles reference SEC issuer CIK 1699031.',
29:'MGM Resorts is the shortened disclosed name of MGM Resorts International; both saved identity records identify SEC issuer CIK 789570.',
30:'Both full disclosed names identify American Biomass Energy Association; one retains a former-name qualifier. The saved IRS and original registration match identifies EIN 770508798.',
31:'The labels identify American Cancer Society Cancer Action Network with a shortened Action Network spelling or ACSCAN acronym. The source profiles identify the advocacy organization and its own 501(c)(4) return, not the separate American Cancer Society.',
32:'Both full disclosed names identify American Cleaning Institute; one preserves the former Soap & Detergent Association qualifier. The reviewed organization records identify the same cleaning-products trade association.',
38:'Both full labels identify Center for Sportfishing Policy. Its official FAQ documents the former Center for Coastal Conservation name and its 501(c)(4) status.',
39:'The on-behalf-of label explicitly names Coalition for App Fairness as beneficiary and Forbes Tate as intermediary. Both beneficiary profiles identify the same coalition, EIN 852605965.',
40:'The Eudcation spelling is a filing typo for DeFi Education Fund; the saved identity match identifies EIN 871014079 and the same Washington organization.',
41:'Both profiles identify the South Carolina federally qualified health center at genesisfqhc.org; the original names differ only in Health Care spacing. The saved IRS identity is EIN 010932846, not the similarly named nursing-home business.',
43:'Healthcare versus Health Care spacing distinguishes the labels; the saved IRS and original registration match identifies Healthcare Supply Chain Association, EIN 521699732.',
45:'Both original labels identify National Council of Nonprofits; one has a truncated former-name qualifier. The official organization page and saved IRS match identify EIN 521689643.',
46:'NMDP is the acronym of the disclosed National Marrow Donor Program. The reviewed official pages establish the donor-registry organization and its current NMDP identity.',
47:'Healthplan versus Health Plan spacing distinguishes the labels. Both identify National MLTSS Health Plan Association, EIN 813841361.',
49:'Both full labels identify NCTA-The Internet & Television Association; one retains the former-name qualifier. The saved IRS and registration identity identifies EIN 530222396.',
50:'Sixteenthirty versus Sixteen Thirty spacing distinguishes the labels; the reviewed official About page identifies the same 501(c)(4) organization.',
52:'The full National Center for Infants Toddlers and Families qualifier and the shorter ZERO TO THREE label identify the same organization in the reviewed IRS, filing and official website records.',
53:'The on-behalf-of filing explicitly names D-Wave Government Inc. as beneficiary. Both profiles concern that subsidiary, which the SEC exhibit identifies separately from D-Wave Quantum Inc.',
54:'The on-behalf-of label explicitly names Technology Service Corporation as beneficiary and 535 Group as intermediary. Both profiles identify the employee-owned engineering company at tsc.com.',
55:'The full A. O. Smith Corporation labels differ only in initial punctuation. The reviewed issuer evidence identifies the same AOS company.',
57:'Both labels explicitly name Academy of Nutrition and Dietetics, differing in ampersand and a retained former-name qualifier. The reviewed official organization identity is the same academy.',
58:'Both full labels identify Air-Conditioning, Heating, and Refrigeration Institute, with punctuation and AHRI/former-name qualifiers. The reviewed official site identifies that institute.',
61:'Both full original labels identify Alliance for Physical Therapy Quality and Innovation. The second retains historical qualifiers; the reviewed APTQI website identifies the same current alliance.',
63:'The full Americas Health Insurance Plans labels differ in apostrophe and Inc. punctuation and both include AHIP. The reviewed official association evidence identifies the same organization.',
64:'Two labels explicitly name the American Bankers Association Card Policy Council. The third original filing is specifically corroborated as that council by the cited LDA record and ABA publication; the council is not merged with its parent association.',
67:'Assoc. versus Association and the AMGA acronym distinguish the full names. The reviewed official About page identifies the same American Medical Group Association.',
68:'Both full labels explicitly name American Psychological Association Services, Inc. The reviewed APA sources distinguish this advocacy entity from the American Psychological Association; this merge does not include the parent association.',
69:'Both full disclosed names identify Americans for Responsible Innovation; one adds ARI. The official ari.us source corroborates that organization.',
70:'The second name has an extra t in Attendants and different punctuation; both profiles identify Association of Flight Attendants-CWA and cite its official union About page. No CWA parent or local union is included.',
72:'BCBSM Inc. and Blue Cross Blue Shield Michigan identify the same Michigan mutual insurer in the saved state, financial and official company sources. Other Blue Cross licensees are not included.',
73:'Both full disclosed names identify BeOne Medicines USA, Inc. and retain the same former BeiGene USA name; only punctuation differs. The cited company filing identifies this exact US subsidiary, not its parent.',
74:'The on-behalf-of label explicitly identifies Bosma Enterprises as beneficiary and G2 Strategies as intermediary. Both profiles identify Bosma Enterprises, not a separate Bosma foundation.',
75:'Children\'s Hospital Boston and Boston Children\'s Hospital are the same hospital brand in the saved official legal-identity evidence, which identifies Children\'s Hospital Corporation, EIN 042774441. The separate trust is not included.',
76:'Both labels identify Bracewell representing FBI Agents Association, using the full name or FBIAA acronym. The official association evidence corroborates the same represented organization.',
77:'The on-behalf-of label explicitly identifies Cabot Corporation as beneficiary and Kerbey Harrington Pinkard as intermediary. The other label and reviewed issuer materials identify that same Cabot Corporation.',
78:'The original California Head Start Association label explicitly supplies Head Start California as its alternate name; the other label uses that same name and the official site corroborates the organization.'}
deferred={25:'Fuellcell spelling likely a typo, but the saved second profile lacks a specific filing-location or legal-identifier match; retain pending verification.',27:'Gaurdant spelling likely a typo, but the saved second profile lacks a specific filing-location or legal-identifier match; retain pending verification.',37:'America versus American likely a typo, but current evidence summary lacks specific second-record identifier or location proof.',42:'The IHRSA relationship needs explicit legal-name continuity evidence beyond the current brand and generic activity statement.',56:'Shared a16z brand does not alone establish continuity among capital-management legal entities and former names.',60:'Truncated former transportation-agency label could refer to a predecessor; verify legal continuity before merging.',65:'Civil War Trust qualifier may involve a renamed division or predecessor; generic shared mission is insufficient legal continuity evidence.',66:'Current names match but saved source claims do not document Portland Cement Association legal continuity; verify official rename evidence.',71:'Original labels name different coalitions under the Azura brand; shared brand does not establish that these are one represented legal entity.',79:'Cambia and former Regence Group relationship needs explicit legal continuity evidence; shared healthcare activity is insufficient.'}
out=[];audit=[]
for n,why in reasons.items():
 x=a[n];ids=x['ids'];assert all(p[i]['review_outcome']=='confirmed' and p[i]['status']=='sourced' for i in ids)
 canonical=max(ids,key=lambda i:(p[i].get('logo_status')=='official_site_asset' and p[i].get('logo_kind')=='logo',p[i].get('website_status')=='verified',p[i].get('featured',False)))
 sources=[];seen=set()
 for i in ids:
  for s in p[i]['sources']:
   k=(s['url'],s.get('claim',''))
   if k not in seen:seen.add(k);sources.append(s)
 out.append({'canonical_id':canonical,'source_ids':ids,'rationale':why+' All original names, individual research and filings are retained.','sources':sources,'reviewed_at':'2026-09-12'})
 audit.append({'index':n,'ids':ids,'decision':'approved','rationale':why,'original_labels':{i:b[i]['aliases'] for i in ids}})
for n,why in deferred.items():audit.append({'index':n,'ids':a[n]['ids'],'decision':'deferred','rationale':why})
(r/'root-remaining-approved.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');(r/'root-remaining-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n');print('Approved',len(out),'deferred',len(deferred))
