import unicodedata,hashlib,datetime

def norm(s):return ' '.join(unicodedata.normalize('NFKC',s or '').split()).upper()
def key(s):return hashlib.sha256(norm(s).encode()).hexdigest()[:16]
def date(s):
 try:return datetime.datetime.strptime(s,'%m/%d/%Y @ %I:%M %p').isoformat()
 except ValueError:return ''
def period(s):
 for p in ['1st Quarter','2nd Quarter','3rd Quarter','4th Quarter','Mid-Year','Year-End']:
  if s.startswith(p):return p
 return None

def latest_groups(records):
 groups={}
 for r in records:
  p=period(r['kind'])
  if not p:continue
  g=(key(r['client']),norm(r['registrant']),r['year'],p);prev=groups.get(g);stamp=date(r['posted'])
  if not prev or stamp>prev[0]:groups[g]=(stamp,[r])
  elif stamp==prev[0]:prev[1].append(r)
 return groups
