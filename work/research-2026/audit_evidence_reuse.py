"""Flag copied research across dissimilar names; candidates need human review."""
import json, pathlib, re, sys
r=pathlib.Path(__file__).parent
reviewed=json.load(open(r/'reviewed.json'))
def words(s):
 return set(re.findall(r'[a-z0-9]+',s.lower()))-{'inc','llc','ltd','company','corporation','the','of','and','usa','group','corp'}
index={}
for k,v in reviewed.items():
 description=v.get('description','').strip().lower()
 if len(description)>30:index.setdefault(description,[]).append((k,v))
flags=[]
for filename in sys.argv[1:]:
 for k,v in json.load(open(filename)).items():
  for oldk,old in index.get(v.get('description','').strip().lower(),[]):
   if oldk!=k and not words(v.get('name','')) & words(old.get('name','')):
    flags.append({'id':k,'name':v.get('name'),'copied_from_id':oldk,'copied_from_name':old.get('name'),'reason':'Identical description under dissimilar names','file':filename})
print(json.dumps(flags,indent=2))
