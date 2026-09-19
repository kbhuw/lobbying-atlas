import pathlib,zipfile,json,unicodedata,collections,sqlite3
from lxml import etree
import os
project=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(os.environ.get('LOBBYING_DATA_DIR',str(project/'work'/'data')))
root.mkdir(parents=True,exist_ok=True)
def norm(t):return ' '.join(unicodedata.normalize('NFKC',t or '').split()).upper()
db=sqlite3.connect(root/'issues.sqlite')
db.executescript('CREATE TABLE IF NOT EXISTS issues(client TEXT,year INTEGER,code TEXT,source_zip TEXT,source_member TEXT,PRIMARY KEY(client,year,code));CREATE TABLE IF NOT EXISTS processed(archive TEXT PRIMARY KEY,members INTEGER,errors INTEGER);CREATE TABLE IF NOT EXISTS errors(archive TEXT,member TEXT,error TEXT);')
for p in sorted((root/'raw').glob('*.zip')):
 if db.execute('select 1 from processed where archive=?',(p.name,)).fetchone():continue
 rows=[];errors=[];count=0
 with zipfile.ZipFile(p) as z:
  for member in z.namelist():
   if not member.lower().endswith('.xml'):continue
   count+=1
   try:
    x=etree.fromstring(z.read(member),etree.XMLParser(resolve_entities=False,no_network=True))
    if x.tag!='LOBBYINGDISCLOSURE2' or x.findtext('noLobbying','').strip()=='Y':continue
    client=norm(x.findtext('clientName'));year=x.findtext('reportYear','').strip()
    if not client or not year.isdigit():continue
    for a in x.findall('.//ali_info'):
     code=a.findtext('issueAreaCode','').strip()
     if code:rows.append((client,int(year),code,p.name,member))
   except Exception as e:errors.append((p.name,member,str(e)))
 db.executemany('INSERT OR IGNORE INTO issues VALUES(?,?,?,?,?)',rows)
 db.executemany('INSERT INTO errors VALUES(?,?,?)',errors)
 db.execute('INSERT INTO processed VALUES(?,?,?)',(p.name,count,len(errors)));db.commit()
 print(p.name,'members',count,'issue_rows',len(rows),'errors',len(errors),flush=True)
print('DONE',flush=True)
