import json
from pathlib import Path

r = Path('work/research-2026')
p = json.load(open(r / 'reviewed.json'))
changes = {}

def review(i, note, sources, **fields):
    changes[i] = dict(fields, review_outcome='confirmed', checked_at='2026-09-14', notes=note, identity_evidence=note)
    changes[i]['new_sources'] = [{'url': u, 'label': label, 'claim': claim} for u, label, claim in sources]

review('27ca17b2866103ed', 'The official careviso site identifies its seeQer healthcare-administration software and former CMT Solutions name. A May 21, 2025 SEC Form D independently names Careviso, Inc. as the stock-investment target, corroborating the exact company name. The investment vehicle is a separate entity; its offering amount and ownership are not assigned to careviso. Current ownership remains unknown.', [
 ('https://www.careviso.com/about', 'Official company description, retrieved September 14, 2026', 'careviso identifies its former CMT Solutions brand and software for patient cost information and prior authorizations.'),
 ('https://www.sec.gov/Archives/edgar/data/2069667/000206966725000001/xslFormDX08/primary_doc.xml', 'Investor SEC Form D, May 21, 2025', 'The separate issuer states it was formed to acquire stock in Careviso, Inc.; corroborates the exact name without establishing a controlling owner.')], legal_form='Corporation')

review('ad1394aa2fc041b3', 'Operating identity confirmed from the official Cascade Space site: spacecraft-communications engineering in San Francisco matches the original 2026 registration, which names Cascade Space Corp. at 730 Clementina Street and describes a private deep-space communications network. Website branding omits the suffix; no conflicting legal entity was identified. Ownership remains unknown, and planned 2027 capacity is not represented as operational.', [
 ('https://cascade.space/about/', 'Official company body, retrieved September 14, 2026', 'The San Francisco team designs, builds, tests and operates spacecraft communication systems.'),
 ('https://disclosurespreview.house.gov/data/LD/2026_Registrations_XML.zip', 'Original registration 301870756.xml', 'Client name, San Francisco address and deep-space communications activity corroborate the operating identity. Legal name retained as reported.')])

review('2af6b35d4cf4fa4e', 'Confirmed as the Carlyle investment-management operating business. The original client record 101289 places the unsuffixed name in Washington, DC and reports private-equity activity; Carlyle publishes an adviser brochure for Carlyle Investment Management LLC. This supports the operating identity, but does not establish that every unsuffixed or Inc. filing is the LLC. No legal-entity merge, parent ticker or exact ownership is assigned.', [
 ('https://lda.gov/api/v1/filings/efc3c179-cd3b-4f55-bf96-17cd09870c26/?format=json', 'Original filing retrieved September 14, 2026', 'Unsuffixed client name, Washington DC and private-equity activity.'),
 ('https://www.carlyle.com/sites/default/files/2025-08/Carlyle_Investment_Management_LLC_CIM_ADV_2A_Brochure_March_31_2025.pdf', 'Official adviser brochure, March 31, 2025', 'Previously read primary brochure identifies the related Carlyle Investment Management LLC adviser; operating corroboration only for this unsuffixed record.')])

review('92ff5e9db00aaf44', 'Coalition identity is independently documented in Felipe Vicini’s April 23, 1986 congressional testimony on behalf of the Caribbean Basin Initiative Sugar Group. The exact coalition label appears in current lobbying records. Historical participant countries are not asserted as current members; current governance, legal incorporation and a standalone website remain unknown.', [
 ('https://www.jec.senate.gov/reports/99th%20Congress/European%20Community%20Agricultural%20Trade%20Practices%20%281405%29.pdf', 'Congressional hearing, April 23, 1986; downloaded and read', 'Printed page 15 names the coalition and describes Caribbean Basin sugar producers advocating on sugar-trade policy.')])

review('c05c3567e2a566a8', 'Confirmed as the McAlester, Oklahoma community health-center operation. Original registration 301473442 names Caring Hands Health Center, Inc. at 3101 Elk Drive, McAlester. The official clinic privacy notice identifies Caring Hands Healthcare Centers at 3101 Elks Road in the same city, while the Oklahoma health department links its McAlester and Hartshorne clinics to chhcok.com. The reported name and address variants are retained; current legal ownership is unknown.', [
 ('https://disclosurespreview.house.gov/data/LD/2023_Registrations_XML.zip', 'Original registration 301473442.xml', 'Exact filed name, McAlester address and health-center activity.'),
 ('https://chhcok.com/wp-content/uploads/2023/10/CHHC-Notice-of-Privacy-Practices.pdf', 'Official clinic privacy notice, indexed body inspected', 'The first page names Caring Hands Healthcare Centers at 3101 Elks Road, McAlester.'),
 ('https://oklahoma.gov/content/dam/ok/en/health/health2/documents/oklahoma-fqhcs-january-2018.pdf', 'Oklahoma health department, January 2018; downloaded and read', 'Lists McAlester and Hartshorne sites under Caring Hands Healthcare Center and links chhcok.com.')], description='Community health-center organization serving McAlester and Hartshorne, Oklahoma.')

batch = {q['id']: q for q in json.load(open(r/'identity304-batch.json'))['records']}
notes = {
 'd52260625be7e51d': 'Official privacy policy effective May 2025 explicitly identifies CelLink Corporation as the operator of cellinktechnologies.com and lists its San Carlos address. This resolves the Corporation/Technologies branding question. It is the flexible-circuit business, distinct from CELLINK bioprinting. Current ownership remains unknown.',
 '6140b35b7ca505cf': 'Marvell’s February 2, 2026 completion release confirms its acquisition of Celestial AI and incorporation of the technology and teams into its Data Center Group. This is a completed acquisition, not an announcement of intent. Celestial AI remains a separate historical lobbying record; Marvell’s stock ticker is not assigned to it.',
 '0a255d6c114270b8': 'The official privacy policy was read in the rendered browser on September 14, 2026. It is revised August 13, 2025, names Celligence LLC as provider of celligence.com and AngelAi, and explains its AI-assisted mortgage workflow. This supersedes the older January revision reported in the research batch. Current ownership remains unknown.',
 '1a8ce383217d1fa7': 'The official user agreement, last updated September 29, 2021, explicitly identifies Auth9, Inc. d/b/a Certree and certree.com. It describes employer-issued employment and income documents and individual-controlled sharing with verifiers. The indexed official body was read; direct retrieval was blocked. Ownership remains unknown. Its 2026 termination filing remains preserved.',
 '0ebfd4fe8828882d': 'The downloaded official manufacturing-services PDF names Cerion, LLC, gives its Rochester address, and describes custom inorganic-nanomaterial design, scale-up and manufacturing. Its footer is dated 2023 despite the 2022 filename. Exact identity is confirmed; current ownership remains unknown.'}
for i, note in notes.items():
    q=batch[i]
    src=[(s['url'], 'Official identity evidence reviewed September 14, 2026', note) for s in q['sources'] if 'lda.gov/' not in s['url']][:1]
    fields={}
    if i != '6140b35b7ca505cf': fields['website_status']='verified'
    if i in ['d52260625be7e51d','1a8ce383217d1fa7']: fields['legal_form']='Corporation'
    if i in ['0a255d6c114270b8','0ebfd4fe8828882d']: fields['legal_form']='LLC'
    if i=='6140b35b7ca505cf': fields.update(ownership='Subsidiary', description='Developed optical connections that move data between AI computing systems. Marvell completed its acquisition of Celestial AI in February 2026.')
    review(i,note,src,**fields)

review('306d2566a0bcc98b', 'Confirmed as Center for Employment Opportunities (CEO), the nonprofit using ceoworks.org. Its official leadership biography explicitly identifies the New York-based employment nonprofit, and the published Form 990 names Center for Employment Opportunities, Inc., EIN 13-3843322. The filed CEO Works label and reentry-employment activity align. Its lobbying registrant is an intermediary, not an owner.', [
 ('https://www.ceoworks.org/leadership/sam-schaeffer', 'Official leadership biography, indexed body inspected', 'Explicitly identifies the Center for Employment Opportunities as a New York-based nonprofit providing employment services to people with criminal convictions.'),
 ('https://ceoworks.org/assets/downloads/financial-reports/CEO-2017-Form-990-PD-Version_6.30.18.pdf', 'Organization-published 2017 Form 990', 'Names the corporation and EIN and describes transitional work and job placement.')], website_status='verified', legal_form='Nonprofit corporation')

review('e7709c506bde5ffb', 'Confirmed as an office within Center for Inquiry, rather than a separately owned company. The organization’s 2016 progress report explicitly attributes lobbying and lawmaker meetings to its Office of Public Policy, independently corroborating the office named in the original 2021 registrations. Website is the parent organization’s official site; separate office incorporation is not asserted.', [
 ('https://progress2016.centerforinquiry.org/', 'Official 2016 progress report, body retrieved September 14, 2026', 'Explicitly identifies lobbying by CFI’s Office of Public Policy and its secular-government and science advocacy.')], website_status='verified')

for i in ['1197d31c5892037f','b3e24f293c67aa0a']:
    review(i, 'Confirmed as the CentraCare health-system operating identity in St. Cloud, Minnesota. Original registrations use CentraCare Health System and CentraCare Health, with 1900 CentraCare Circle appearing across the records. The current official careers site describes the Minnesota system formed in 1995 and its hospitals. Individual hospital corporations remain distinct; these two filing-name records are not yet legally merged.', [
      ('https://jobs.centracare.com/us/en/life-at-centracare', 'Official current system description, retrieved September 14, 2026', 'Describes CentraCare’s Minnesota hospital system, St. Cloud roots and 1995 formation.')], website_status='verified')

before=r/'featured303-before.json'
assert not before.exists()
before.write_text(json.dumps({i:p[i] for i in changes},ensure_ascii=False,indent=2)+'\n')
for i,fields in changes.items():
    src=fields.pop('new_sources')
    p[i].update(fields)
    p[i]['sources'].extend(src)
logos=json.load(open(r/'evidence304/logo-followup.json'))['logos']
for q in logos:
    if q['asset_url'] and q['id'] in changes:
        p[q['id']].update(logo_url=q['asset_url'],logo_kind='logo',logo_status='official_site_asset',logo_source_url=q['source_page'])
(r/'featured303-decisions.json').write_text(json.dumps({i:p[i] for i in changes},ensure_ascii=False,indent=2)+'\n')
(r/'reviewed.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')))
Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
print(f'Saved {len(changes)} reviewed identities and verified logo updates.')
