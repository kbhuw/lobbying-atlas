import pathlib,json
r=pathlib.Path('work/research-2026');s=(r/'check_general32b.py').read_text();exec(s[:s.index('p=json.load(open(root/')])
fix={
'd2816102c7afc898':'https://cdn.prod.website-files.com/6787937dc91142157fba2748/6787937dc91142157fba2bbd_CTE%20Logo_Dropshadow_Nav%20Bar_3-01.avif',
'caa16875405c0f19':'https://centerphaseenergy.com/wp-content/uploads/2026/03/Center-Phase-Energy-New-Logo.webp',
'df56d9e1fdd78431':'https://irp.cdn-website.com/18ae6f39/dms3rep/multi/opt/Untitled-design--2819-29-234w.png'}
for k,u in fix.items():
 dest,mime,b=get(u);assert mime.startswith('image/') and len(b)>80
 f=r/f'website-cache/{k}.json';c=json.load(open(f));c.update(logo_url=u,logo_kind='logo',logo_source_url=c['final_url'],logo_http_status=200,logo_content_type=mime)
 if k=='df56d9e1fdd78431':c['logo_rejection_reason']='Earlier filename-only rejection was inconclusive; selected alternate official logo explicitly identified as CASS in site alt text.'
 f.write_text(json.dumps(c,indent=2)+'\n');print(k,mime)
s=(r/'build_general32a.py').read_text().replace('32a','32b');start=s.index('hold=');end=s.index('\n',start);s=s[:start]+"hold={'90d02823316d6083','43b94ca6d6a0a277'}"+s[end:];(r/'build_general32b.py').write_text(s)
