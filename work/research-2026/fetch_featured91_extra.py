import requests,bs4,json,concurrent.futures,io,pathlib
from pypdf import PdfReader
urls=['https://lda.gov/filings/public/filing/eae4f114-691e-4a0c-ba03-6bf6a376cee9/print/','https://lda.gov/filings/public/filing/77480d3e-342f-419c-8463-75b70bf0e8a1/print/','https://www.titosvodka.com/distillery-tcs','https://toshiba.com/tai/about-us/','https://www.totalwine.com/site/binaries/content/assets/pdfs/weddings/0326_twm_weddings_booklet_web.pdf','https://www.torchtechnologies.com/','https://totegroup.com/about/','https://hscrc.maryland.gov/Documents/Strong%20als%20Folder/Audited%20Financials%20-%20ar-rev/FY%202024/TidalHealth%2C%20Inc.%20%20FY2024%20AFS.pdf']
def f(u):
 try:
  r=requests.get(u,timeout=25);t=' '.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(r.content)).pages) if r.content.startswith(b'%PDF') else bs4.BeautifulSoup(r.text,'html.parser').get_text(' ',strip=True);return dict(url=u,status=r.status_code,text=t)
 except Exception as e:return dict(url=u,error=str(e))
x=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(f,urls));pathlib.Path('work/research-2026/featured91-extra-fetch.json').write_text(json.dumps(x,indent=2)+'\n')
for i,d in enumerate(x):
 t=d.get('text','');words=['Client Name','501(c)','Fifth Generation','subsidiary','family-owned','employee-owned','TOTE, LLC'];print(i,d.get('status'),[(w,t[max(0,t.find(w)-60):t.find(w)+250]) for w in words if w in t])
