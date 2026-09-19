"""Flag source-copy placeholders and cross-record evidence mistakes before publication."""
import json,pathlib,re,sys,urllib.parse
r=pathlib.Path('work/research-2026');result={}
for n in range(2):
 f=r/f'tax-large-reviewed-{n}.json'
 if not f.exists():continue
 original={v['id']:v for v in json.load(open(r/f'tax-large-{n}.json'))}
 for k,v in json.load(open(f)).items():
  flags=[];desc=v.get('description','');raw=original.get(k,{}).get('tax_evidence',{})
  if re.search(r'Organization focused on|stated organizational purpose|mission is detailed|see schedule|continued on schedule|…|\.\.\.',desc,re.I):flags.append('placeholder_or_truncation')
  if len(desc)<35:flags.append('description_too_short_to_explain_entity')
  if raw.get('ein','').replace('-','') not in str(v.get('identity_evidence','')).replace('-',''):flags.append('missing_exact_EIN_evidence')
  if not any(s.get('url')==raw.get('source_url') for s in v.get('sources',[])):flags.append('missing_original_tax_source')
  if not v.get('website_status'):flags.append('missing_website_status')
  if k not in original:flags.append('unexpected_id')
  result[k]={'name':v.get('name'),'flags':flags}
(r/'large-quality-audit.json').write_text(json.dumps(result,indent=2));print({'entries':len(result),'flagged':sum(bool(x['flags']) for x in result.values())})
