import json,pathlib
r=pathlib.Path('work/research-2026');p=json.load(open(r/'irs-round2-a-cleaned.json'));p={v['id']:v for v in p} if isinstance(p,list) else p
# Plain-language rewrites of the individually inspected mission and official-page evidence.
texts={
'8d5449780c93062a':'Association representing fish and wildlife agencies and coordinating conservation policy and professional work.',
'ebf849f0888db834':'Association of food and drug regulatory officials coordinating public-health standards, training, and policy on food and medical-product safety.',
'9dae9fe600583681':'Trade association representing home-appliance manufacturers in industry standards and public policy.',
'd3c5ddf1c01c2370':'Trade association representing advertisers and providing marketing education, industry programs, and policy advocacy.',
'b6b104d0c1709302':'Business association representing employers and advocating on trade, commerce, and economic policy in Washington state.',
'80d515b32693231c':'Association supporting Women’s Business Centers and the organizations that train and advise women entrepreneurs.',
'dfd8dbbd5d7b1edd':'College athletics conference organizing competition and coordinating athletic programs among its member institutions.',
'7c6237fed2c93eed':'Trade association representing businesses that supply aftermarket vehicle parts, products, and repair services.',
'a76f9838fd309592':'Business and technology organization helping companies adopt manufacturing automation, software, and artificial intelligence.',
'b556bb7285a495ad':'Industry association advocating for policies that permit deployment of autonomous vehicles.',
'd8216d6c0cd30382':'Business association bringing San Francisco Bay Area employers together on regional economic and public-policy issues.',
'd6ed3825452b6046':'Youth-services nonprofit arranging and supporting one-to-one mentoring relationships in the Philadelphia region.',
'a866434ff5cb0882':'Membership organization advocating for public lands, waters, wildlife habitat, and access for hunting and fishing.',
'acbc212f5ab92c3d':'Banking-industry association conducting research and advocating on banking regulation and public policy.',
'b874d988f445aa53':'Community hospital providing medical care to patients in the Springville, New York area.',
'c53e28da0a36fa9c':'Advocacy organization promoting policy proposals developed by the affiliated Bipartisan Policy Center.',
'd57d9d30b6767e4a':'Veterans organization providing support and advocacy for veterans who are blind or have impaired vision.',
'7c2845d4d577141d':'Cryptocurrency-industry association advocating on U.S. blockchain and digital-asset policy.',
'b7a9a1990166d1e3':'Conservation and hunting organization supporting wildlife preservation, research, and hunting records.',
'e6c8b06a13df5d4e':'Business-policy coalition advocating for cross-border trade and economic development among the United States, Mexico, and Canada.',
'a26bc27927f8a329':'Trade association representing clay-brick manufacturers and promoting the brick industry.',
'cadacfaf30aa5452':'Fundraising foundation supporting Brooklyn College through alumni engagement and charitable contributions.',
'd2545ab169cad69d':'Trade association representing commercial-building owners and managers through advocacy, education, and industry research.',
'd5e04ab791aa0e01':'Arts and culture nonprofit supporting Burning Man events, community projects, education, and civic participation.',
'bf58e39f233a934f':'Community-development nonprofit supporting neighborhood revitalization and residents in underserved Cleveland communities.',
'e2df598434767eb1':'University auxiliary organization providing services and facilities that support California Polytechnic State University in San Luis Obispo.',
'cb3bc386338c826c':'Industry association representing controlled-environment agriculture businesses, including indoor growing operations.',
'd4c5f8019f81a021':'Association supporting California food banks and advocating for policies and resources to reduce hunger.',
'6c668b9cce0c8d90':'Association representing California public hospitals and health systems in health-policy advocacy.',
'b0c0204d0f63e145':'Association representing California sanitation agencies on wastewater, clean-water, and beneficial-reuse policy.',
'f21942b9ef21a628':'Trade association representing California winegrape growers through advocacy, information exchange, and industry programs.',
'766c721d4ffc20f1':'Grower association providing citrus-industry information and advocating for California citrus producers.',
'e8e4e4998090cf59':'Industry association serving local telephone carriers and broadband companies through networking and industry coordination.',
'ae8306b673699806':'Trade association representing California credit unions through policy advocacy, education, and member services.',
'ddb2547bae21c6d3':'Public-health advocacy organization promoting policies to reduce tobacco use, particularly among children.',
'cb8ccd220891e148':'Legal advocacy nonprofit working on voting rights, campaign finance, government ethics, and participation in democracy.',
'aa97b1c00df37f8b':'Higher-education association supporting civic engagement and partnerships between colleges and their communities.',
'd2785b0e70d08c3f':'Workforce-development nonprofit arranging youth apprenticeships and partnerships between employers and education providers in Colorado.',
'b94a8ac9b02b80b0':'Climate-policy advocacy organization educating policymakers and lobbying on measures to address climate change.',
'cc7649f758a80d3b':'Social-services nonprofit providing food, shelter, and related support to people in need in Southern Nevada.',
'7989bbe9535b992d':'Climate advocacy organization helping communities and governments pursue accountability from fossil-fuel companies for climate-related harms.',
'8e69b689baa86334':'Environmental-justice nonprofit conducting education, research, and advocacy on climate, energy, and environmental policy.',
'a557ef8a64e5d83f':'Employment-services nonprofit helping people recently released from incarceration find and retain work.',
'6e99324f91fd1f0e':'Rural-development nonprofit supporting rural communities through economic-development, environmental, and public-policy work.',
'7453081cc27fdc77':'Policy research organization analyzing government budgets and their effects on people with low and moderate incomes.',
'b0622e400d784efb':'Regional climate advocacy nonprofit organizing campaigns in Maryland, Virginia, and Washington, D.C.',
'960141538d4fa56e':'Social-services nonprofit supporting Chicago children, families, and older adults through community programs.',
'f0bdcf873c3de957':'Professional society supporting pediatric neurologists through education, research, professional training, and advocacy.'}
for k,t in texts.items():p[k]['description']=t
for k,v in json.load(open(r/'irs-round2-a-specific-facts.json')).items():
 p[k]['description']=v['description'];p[k]['name']=v.get('name',p[k]['name']);p[k]['sources']+=v.get('sources',[])
assert len(p)==75
for v in p.values():
 assert len(v['description'])>30
 assert not v['description'].lower().startswith(('we ','our ','to ','the trusted','nonprofit organization supporting its stated'))
 assert 'schedule o' not in v['description'].lower()
(r/'irs-round2-a-root-rewrite.json').write_text(json.dumps(p,indent=2)+'\n');print('75 descriptions rewritten and checked')
