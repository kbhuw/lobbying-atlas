import json,pathlib,copy
r=pathlib.Path('work/research-2026');p=json.load(open(r/'reviewed.json'));assert not (r/'featured218-before.json').exists();before={};dec=[]
updates={
'0727872fc471ff78':dict(name='PNI Sensor (via SBIR Advisors)',notes='PNI’s August 2025 sales terms identify its contracting business as Protonex LLC doing business as PNI Sensor, explaining the SBIR name/domain match. The original lobbying label says PNI Sensor Corporation; that reported label is preserved, and corporate succession between that label and Protonex has not been established. SBIR Advisors is the reported intermediary, not an inferred owner.',url='https://www.pnisensor.com/terms/',confirmed=False),
'01e060b95b89fe96':dict(name='Enexor BioEnergy (via the Bennett Group DC)',notes='Enexor’s own DOE award announcement identifies Enexor BioEnergy, the same operating name reported as the represented client in the lobbying filing. It describes biomass preprocessing and renewable energy systems at 1 Enterprise Court, Franklin, Tennessee. The SBIR awardee is Enexor Energy LLC; a formal rename or ownership relationship between those legal names is not established. Identity is confirmed at the represented operating-business level; original legal labels remain intact.',url='https://www.enexor.com/newsroom/pr-doe-biomass-preprocessing',confirmed=True),
'1f30b4f1d25f1996':dict(name='WhiteFox Defense Technologies (via Next Global Capital)',notes='The original 2026 report explicitly names Next Global Capital, Inc. on behalf of WhiteFox Defense Technologies, Inc. and reports drone airspace-security issues. The official WhiteFox identity and activity match the represented business. This establishes the relationship as reported in the lobbying disclosure; it does not establish ownership by Next Global Capital.',url='https://lda.gov/filings/public/filing/156a1bb7-b668-47f3-b2db-39adf61792b1/print/',confirmed=True)}
for i,x in updates.items():
 v=p[i];before[i]=copy.deepcopy(v);v.update(name=x['name'],notes=x['notes'],identity_evidence=x['notes'],checked_at='2026-09-13')
 if x['confirmed']:v['review_outcome']='confirmed'
 v['sources'].append(dict(url=x['url'],label='Primary identity clarification',claim=x['notes']))
 dec.append(dict(id=i,**x))
for k,v in [('before',before),('decisions',dec)]: (r/f'featured218-{k}.json').write_text(json.dumps(v,indent=2)+'\n')
for f in [r/'reviewed.json',pathlib.Path('outputs/2026-research-trial/profiles.json')]:f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(p,ensure_ascii=False))
print('2 represented identities confirmed, 1 legal discrepancy documented; 3 names made readable')
