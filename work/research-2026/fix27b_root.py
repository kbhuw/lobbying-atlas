import pathlib,json
r=pathlib.Path('work/research-2026');p=json.load(open(r/'general-round27-b-root-draft.json'))
for k,v in p.items():
 old=v['ownership'];v['ownership']='Government body' if old=='Public entity' else 'Private company' if old=='100% employee-owned' else 'Publicly traded' if old.startswith('Publicly traded') else 'Unknown'
 v['notes']=v.get('notes','')+(' '+old if old not in ['Unknown','Public entity'] else '')
 v['review_outcome']='partial' if v['ownership']=='Unknown' else 'confirmed'
 v['sources']=[s for s in v['sources'] if 'buildingsandskilledtrades.org' not in s['url']]
 v.setdefault('identity_evidence','Original disclosure and primary organization pages checked; remaining uncertainties are noted.')
 if v.get('website'):v['sources'].append(dict(url=v['website'],label='Organization website',claim='Official organization page provides business and identity information; exact ownership is separately assessed.'))
def fix(k,desc,kind='Business',own=None,url=None,claim=None,source=None,name=None):
 v=p[k];v.update(description=desc,kind=kind)
 if own:v['ownership']=own;v['review_outcome']='partial' if own=='Unknown' else 'confirmed'
 if url:v['website']=url
 if name:v['name']=name
 if claim:v['identity_evidence']=claim;v['sources'].append(dict(url=source or url or v['website'],label='Primary research evidence',claim=claim))
fix('9a884f8a55ad3642','Public library district providing books, digital resources, and community programs in Buena Park, California.','Government')
fix('d63474a368ca7cb9','Insures municipal and infrastructure bonds, guaranteeing scheduled debt payments to investors.','Business',claim='BAM’s official site describes its municipal-bond insurance business.')
fix('62381954e0d6f8b9','Coalition advocating for federal investment in public-school buildings and infrastructure.','Industry coalition',claim='Official coalition site describes advocacy for public-school facilities.')
fix('4cd2b59300941883','Federation of construction unions representing skilled building-trades workers and supporting training, safety, and labor-policy advocacy.','Labor union','Not applicable',claim='NABTU identifies itself as North America’s Building Trades Unions, the AFL-CIO building-trades department.',name='North America’s Building Trades Unions (NABTU)')
fix('36e5f121769b569c','Membership association supporting construction businesses and building-industry professionals in northern Kentucky.','Trade association')
fix('df4ce5c2f9ac0601','Represents New York construction contractors and their employer associations on industry policy and business issues.','Trade association')
fix('e10caa0c77e1db8d','Advocates for disaster mitigation, stronger building codes, and public investment in resilient infrastructure.','Advocacy organization',url='https://buildstrongamerica.com/',claim='Official BuildStrong site describes disaster-mitigation and resilience policy advocacy.')
fix('c7b6fc2e7dde1350','Provides reusable dumpster bags and debris-removal services for construction, cleanup, and disaster recovery.')
fix('83decdbfe2c78ca9','Digital-asset business associated with the Bullish exchange platform. The exact relationship of this Global filing label to the current listed issuer remains unverified.',url='https://bullish.com/',claim='Bullish group site describes digital-asset exchange services; Global legal-entity ownership is held unresolved.')
fix('f0811271644c7ad2','Develops moving-target systems for military and other live-fire training.',claim='Official Bullseye Target Systems site describes its moving-target training system.')
fix('9e310fef8e347b9c','Produces and markets canned and packaged tuna and other seafood products.')
fix('661459544299ef25','Legal entity named in Bumble’s terms for its online dating and social-connection services.',claim='Bumble terms identify Bumble Trading LLC; its ownership is not inferred from the public parent.')
fix('da21f8f4d0dc0d79','North American Bunge agribusiness operations involving grain, oilseeds, food ingredients, and agricultural supply chains.',claim='Bunge’s regional site describes North American operations; exact legal-entity ownership remains unverified.')
fix('567f1c830c3d3f94','Provides testing, inspection, and certification services for products, industrial facilities, buildings, and supply chains.',claim='Bureau Veritas identifies its Euronext Paris listing, EURONEXT: BVI.',source='https://group.bureauveritas.com/fr/node/28')
fix('a1f577c55708338b','Finances commercial litigation and arbitration and helps businesses and law firms manage the cost and risk of legal disputes.',claim='Company homepage identifies public listings on the NYSE: and London Stock Exchange.')
fix('d66bf2837dc58bac','Explores and develops copper and gold mineral properties, particularly in Nevada.',own='Publicly traded',claim='Fairchild Gold’s official site identifies TSX Venture: FAIR and OTC: FCHDF listings.',name='Fairchild Gold (via Burkhan World Investments)')
fix('cea51e1d5c6795b6','Municipal government providing public services in Burlington, North Carolina.','Government')
fix('7b81033e39daf58d','Develops, leases, and manages commercial real estate in the Washington, D.C. region.',claim='Akridge official site describes development, construction, leasing, and property management.',name='Akridge (via Burnham Developer)')
for k in ['fbfbdf9781114148','5549cd0f2ddf170e']:fix(k,'Provides engineering, architecture, construction, and consulting services for infrastructure and industrial projects.',own='Private company',claim='Official Burns & McDonnell homepage describes the business and states 100% employee ownership.')
for k,n in [('60a221be15ffa527','AMO Pharma'),('f6b63da4b38fa917','Cogwear'),('ced715c8caa88779','Sentry View Systems'),('96aba871d2ec839e','Shionogi Inc.')]:p[k]['name']=n+' (via Burrell International Group)'
for k in ['9e310fef8e347b9c','661459544299ef25','da21f8f4d0dc0d79','567f1c830c3d3f94','a1f577c55708338b','9bb393f0e6e3db8d']:p[k]['featured']=True
(r/'general-round27-b-root-draft.json').write_text(json.dumps(p,indent=2)+'\n')
