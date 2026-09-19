"""Regression fixtures from actual sponsor/member mistakes, no network required."""
import pathlib,urllib.parse
from logo_candidates import Page
r=pathlib.Path(__file__).parent/'logo-ranker-fixtures'
cases=[('ncpdp','National Council for Prescription Drug Programs','https://www.ncpdp.org/','NCPDPLogoImage.png'),('ndrn','National Disability Rights Network','https://www.ndrn.org/','logo-white.png'),('core','National Community Renaissance','https://nationalcore.org/','CORE-Logo-'),('nfff','National Fallen Firefighters Foundation','https://www.firehero.org/','NFFF-Logo-'),('cdcf','CDC Foundation','https://www.cdcfoundation.org/','logo2.svg'),('ncssma','National Council of Social Security Management Associations','https://www.ncssma.com/','ncssma_logo_transparent.png')]
for key,name,url,expected in cases:
 p=Page(name,url);p.feed((r/(key+'.html')).read_text(errors='replace'));top=sorted(p.candidates)[0][1];assert expected in top,(key,top)
 assert p.text,'Text extraction lost'
print('6 actual-page logo regressions passed; candidates still require visual review.')
