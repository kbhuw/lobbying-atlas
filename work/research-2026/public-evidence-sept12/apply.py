import json,pathlib
w=pathlib.Path('work/research-2026');p=w/'reviewed.json';d=json.loads(p.read_text());b=w/'public-evidence-sept12'
items=[
('5e3c36f67d1eb334','ACN','NYSE','https://investor.accenture.com/investor-resources/investor-faqs'),
('5580001dfb3b98b1','AVNT','NYSE','https://www.avient.com/investors'),
('d735907400e00afa','BAC','NYSE','https://newsroom.bankofamerica.com/content/newsroom/press-releases/2026/04/bank-of-america-reports-first-quarter-2026-financial-results.html'),
('47b81cb9ef8b1897','ARAY','NASDAQ','https://investors.accuray.com/news-releases/news-release-details/accuray-advances-strategic-priorities-through-key-executive'),
('cc593421619332e5','AVY','NYSE','https://investors.averydennison.com/news/news-details/2026/Avery-Dennison-Announces-Second-Quarter-2026-Results/default.aspx'),
('0de88654e0c367a3','CE','NYSE','https://investors.celanese.com/news/celanese-corporation-reports-second-quarter-earnings/4f485280-d86f-43f3-8068-de01ca04a02c'),
('24f7f748dfef8f16','COR','NYSE','https://investor.cencora.com/news/news-details/2026/Cencora-Announces-Updated-Fiscal-Year-2026-Financial-Outlook/default.aspx'),
('15558ff382174f2c','COR','NYSE','https://investor.cencora.com/news/news-details/2026/Cencora-Announces-Updated-Fiscal-Year-2026-Financial-Outlook/default.aspx'),
('920780110bdb2808','CIEN','NYSE','https://investor.ciena.com/news/news-details/2026/Ciena-Reports-Fiscal-Third-Quarter-2026-Financial-Results/default.aspx'),
('07e0fc14d6da7a3a','CIEN','NYSE','https://investor.ciena.com/news/news-details/2026/Ciena-Reports-Fiscal-Third-Quarter-2026-Financial-Results/default.aspx')]
for k,t,e,u in items:
 v=d[k];assert v['review_outcome']=='partial';v.update(review_outcome='confirmed',ownership=f'Publicly traded company ({e}: {t})',checked_at='2026-09-12',as_of='2026-09-12');v['sources'].append(dict(url=u,label='Issuer listing evidence rechecked September 2026',claim=f'Official issuer material identifies {e}: {t}; corroborates the existing exact issuer and business match.'))
 v['notes']=v.get('notes','').replace('Official page reviewed individually; ownership is Unknown where no explicit primary ownership evidence was found.','').strip()+' Identity and exchange listing rechecked against official issuer material on September 12, 2026. Historical filing names retained; no automatic entity merge.'
 v['identity_evidence']=str(v.get('identity_evidence',''))+f' Official issuer source independently corroborates {e}: {t}.'
(b/'approved.json').write_text(json.dumps({k:d[k] for k,*_ in items},indent=2)+'\n');p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');pathlib.Path('lobbying-map/research/reviewed-2026.json').write_text(json.dumps(d,ensure_ascii=False)+'\n');pathlib.Path('outputs/2026-research-trial/profiles.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=w/'publication.json';v=json.loads(p.read_text());v['local_changes_pending']=True;v['pending_change_summary']='SAIC variants and UNFI issuer profiles, plus ten public-company records revalidated against issuer evidence September 12, await publication.';p.write_text(json.dumps(v,indent=2)+'\n')
print('Applied',len(items),'individually selected issuer matches; 12 other candidates retained for follow-up')
