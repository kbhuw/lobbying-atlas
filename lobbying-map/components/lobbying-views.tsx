'use client';
import {useEffect,useMemo,useState} from 'react';
import {Button} from '@/components/ui/button';
import {LobbyIndex,IssueBoard,TopicBoard,FirmDetail,OrgLobby,FilingDetail,Notable,loadIndex,loadIssue,loadTopic,loadFirm,loadOrgLobby,loadOrgFilings,loadNotable,dollars} from '@/lib/lobbying';
import {readable,Company} from '@/lib/directory';

function Pager({page,count,onChange}:{page:number;count:number;onChange:(n:number)=>void}){
  return <div className="pager"><span>{count?(page*40+1).toLocaleString()+'–'+Math.min((page+1)*40,count).toLocaleString():'0'} of {count.toLocaleString()}</span><Button variant="outline" disabled={!page} onClick={()=>onChange(page-1)}>Previous</Button><Button variant="outline" disabled={(page+1)*40>=count} onClick={()=>onChange(page+1)}>Next</Button></div>;
}

function Mark({name,profile}:{name:string;profile?:Company['profile']}){
  const [failed,setFailed]=useState(false);
  const src=profile?.logo_url;
  return src&&!failed?<img className={"organization-mark"+(profile?.logo_background==='dark'?' dark-mark':'')} src={src} alt="" loading="lazy" referrerPolicy="no-referrer" onError={()=>setFailed(true)}/>:<span className="organization-mark empty-mark" aria-hidden="true">{name.replace(/[^A-Za-z0-9]/g,'').slice(0,2).toUpperCase()}</span>;
}

export function IssuesExplorer({year:initialYear,onOpenOrg,companies}:{year:number;onOpenOrg:(orgKey:string)=>void;companies?:Map<string,Company>}){
  const [index,setIndex]=useState<LobbyIndex|null>(null);
  const [mode,setMode]=useState<'topics'|'codes'>('topics');
  const [code,setCode]=useState<string|null>(null);
  const [year,setYear]=useState(initialYear);
  useEffect(()=>setYear(initialYear),[initialYear]);
  const [board,setBoard]=useState<IssueBoard|TopicBoard|null>(null);
  const [boardName,setBoardName]=useState('');
  const [q,setQ]=useState('');const [page,setPage]=useState(0);
  const [err,setErr]=useState('');
  useEffect(()=>{loadIndex().then(setIndex).catch(()=>setErr('Could not load lobbying data.'))},[]);
  useEffect(()=>{setBoard(null);if(!code)return;
    const load=mode==='topics'?loadTopic(code,year):loadIssue(code,year);
    load.then(b=>{setBoard(b);setBoardName(b.name)}).catch(()=>setErr('Could not load this issue.'))},[code,year,mode]);
  useEffect(()=>setPage(0),[q,code,year]);
  if(err)return <p>{err}</p>;
  if(!index)return <p className="count">Loading…</p>;
  const hasTopics=!!Object.keys(index.topic_index||{}).length;

  if(code&&board){
    const s=q.trim().toLowerCase();
    const orgs=board.organizations.filter(o=>o.name.toLowerCase().includes(s));
    return <>
      <button className="back" onClick={()=>{setCode(null);setQ('')}}>← {mode==='topics'?'All topics':'All issue areas'}</button>
      <h1>{boardName||index.issue_codes[code]||code}</h1>
      <p className="secondary">Who reported lobbying on this in {year}, ranked by spending. Each filing's full amount counts toward every topic it lists.</p>
      <YearPicker index={index} year={year} onChange={setYear}/>
      <div className="controls"><label className="search"><span>Search organizations</span><input type="search" value={q} placeholder="Organization name" onChange={e=>setQ(e.target.value)}/></label></div>
      <p className="count">{orgs.length.toLocaleString()} organizations</p>
      <div className="org-list">{orgs.slice(page*40,(page+1)*40).map((o,i)=>{const c=companies?.get(o.id);const display=c?.name||readable(o.name);return <button key={o.id} className="org-row" onClick={()=>onOpenOrg(o.id)}>
        <span className="rank">{page*40+i+1}</span>
        <Mark name={display} profile={c?.profile}/>
        <span className="org-main"><span className="org-name">{display}</span><span className="org-sub">{o.filings} report{o.filings===1?'':'s'} filed in {year}</span></span>
        <span className="org-amt">{dollars(o.amount)}</span>
      </button>})}</div>
      <Pager page={page} count={orgs.length} onChange={setPage}/>
    </>;
  }
  if(code)return <><button className="back" onClick={()=>setCode(null)}>← Back</button><p className="count">Loading…</p></>;

  const source=mode==='topics'?index.topic_names||{}:index.issue_codes;
  const iidx=mode==='topics'?index.topic_index||{}:index.issue_index;
  const rows=Object.entries(source)
    .map(([c,name])=>({c,name,...(iidx[c]?.[String(year)]||{organizations:0,amount:0})}))
    .filter(r=>r.name.toLowerCase().includes(q.trim().toLowerCase()))
    .sort((a,b)=>b.amount-a.amount||b.organizations-a.organizations);
  const maxAmount=rows[0]?.amount||1;
  return <>
    <div className="hero">
      <h1>Who lobbied for what?</h1>
      <p>Pick a topic to see who paid to lobby on it — and how much they reported spending.{hasTopics?' Topics are grouped by AI from what filers actually wrote on their forms; issue areas are the government\u2019s own categories.':''}</p>
    </div>
    <div className="hero-controls">
      <label className="search big-search"><input type="search" value={q} placeholder={mode==='topics'?'Search topics — e.g. AI, defense, pharma':'Search issue areas — e.g. Defense, Taxation'} onChange={e=>setQ(e.target.value)} aria-label={mode==='topics'?'Search topics':'Search issue areas'}/></label>
      {hasTopics&&<div className="featured-links" role="group" aria-label="View">
        <button className={mode==='topics'?'year-active':''} onClick={()=>{setMode('topics');setCode(null)}}>Topics</button>
        <button className={mode==='codes'?'year-active':''} onClick={()=>{setMode('codes');setCode(null)}}>Issue areas</button></div>}
      <YearPicker index={index} year={year} onChange={setYear}/>
    </div>
    <p className="count" aria-live="polite">{rows.length.toLocaleString()} {mode==='topics'?'topics':'issue areas'} lobbied in {year}</p>
    <div className="card-grid">
      {rows.map(r=><button key={r.c} className="topic-card" onClick={()=>setCode(r.c)}>
        <span className="topic-name">{r.name}</span>
        <span className="topic-meta"><span>{r.organizations.toLocaleString()} organizations</span><strong>{dollars(r.amount)}</strong></span>
        <span className="topic-bar"><span style={{width:Math.max(2,Math.round(r.amount/maxAmount*100))+'%'}}/></span>
      </button>)}
    </div>
    {!rows.length&&<p>No matches. Try a different search.</p>}
  </>;
}

function YearPicker({index,year,onChange}:{index:LobbyIndex;year:number;onChange:(y:number)=>void}){
  return <div className="featured-links" role="group" aria-label="Reporting year">{[...index.years].sort((a,b)=>b-a).map(y=>
    <button key={y} className={y===year?'year-active':''} onClick={()=>onChange(y)}>{y}</button>)}</div>;
}

export function FirmsExplorer({onOpenOrg,companies}:{onOpenOrg:(orgKey:string)=>void;companies?:Map<string,Company>}){
  const [index,setIndex]=useState<LobbyIndex|null>(null);
  const [firm,setFirm]=useState<FirmDetail|null>(null);
  const [q,setQ]=useState('');const [page,setPage]=useState(0);const [err,setErr]=useState('');
  useEffect(()=>{loadIndex().then(setIndex).catch(()=>setErr('Could not load lobbying data.'))},[]);
  useEffect(()=>setPage(0),[q,firm]);
  if(err)return <p>{err}</p>;
  if(!index)return <p className="count">Loading…</p>;

  if(firm){
    const s=q.trim().toLowerCase();
    const clients=firm.clients.filter(c=>c.name.toLowerCase().includes(s));
    return <>
      <button className="back" onClick={()=>{setFirm(null);setQ('')}}>← All lobbying firms</button>
      <h1>{readable(firm.name||'')}</h1>
      <p className="secondary">{firm.filings.toLocaleString()} filings · {dollars(firm.total)} reported income · {firm.clients.length.toLocaleString()} clients (2024–2026, latest filing per period)</p>
      {firm.topics&&Object.keys(firm.topics).length>0&&<p className="secondary">Top topics: {Object.keys(firm.topics).slice(0,8).map(t=>index.topic_names?.[t]||t).join(' · ')}</p>}
      {Object.keys(firm.issues).length>0&&<p className="secondary">Top issues: {Object.keys(firm.issues).slice(0,8).map(c=>index.issue_codes[c]||c).join(' · ')}</p>}
      <div className="controls"><label className="search"><span>Search clients</span><input type="search" value={q} placeholder="Client name" onChange={e=>setQ(e.target.value)}/></label></div>
      <p className="count">{clients.length.toLocaleString()} clients</p>
      <div className="org-list">{clients.slice(page*40,(page+1)*40).map((c,i)=>{const co=companies?.get(c.key);const display=co?.name||readable(c.name);return <button key={String(c.key)} className="org-row" onClick={()=>onOpenOrg(c.key)}>
        <span className="rank">{page*40+i+1}</span>
        <Mark name={display} profile={co?.profile}/>
        <span className="org-main"><span className="org-name">{display}</span><span className="org-sub">{c.issues.slice(0,4).map(x=>index.issue_codes[x]||x).join(' · ')}</span></span>
        <span className="org-amt">{dollars(c.amount)}</span>
      </button>})}</div>
      <Pager page={page} count={clients.length} onChange={setPage}/>
    </>;
  }

  const s=q.trim().toLowerCase();
  const firms=index.top_firms.filter(f=>(f.name||'').toLowerCase().includes(s));
  const maxFirmTotal=firms[0]?.total||1;
  const PAGE=40;
  return <>
    <div className="hero">
      <h1>Lobbying firms</h1>
      <p>Which firms get hired to lobby, ranked by reported income, 2024–2026. In-house teams appear when they file for their own organization.</p>
    </div>
    <div className="controls"><label className="search big-search"><input type="search" value={q} placeholder="Search firms — e.g. Akin Gump, Brownstein" onChange={e=>setQ(e.target.value)} aria-label="Search firms"/></label></div>
    <p className="count">{firms.length.toLocaleString()} lobbying firms</p>
    <div className="card-grid">
      {firms.slice(page*PAGE,(page+1)*PAGE).map(f=><button key={f.id} className="topic-card" onClick={()=>loadFirm(f.id).then(setFirm).catch(()=>setErr('Could not load this firm.'))}>
        <span className="topic-name">{readable(f.name||'')}</span>
        <span className="topic-meta"><span>{f.clients.toLocaleString()} clients</span><strong>{dollars(f.total)}</strong></span>
        <span className="topic-bar"><span style={{width:Math.max(2,Math.round(f.total/maxFirmTotal*100))+'%'}}/></span>
      </button>)}
    </div>
    <Pager page={page} count={firms.length} onChange={setPage}/>
    {!firms.length&&<p>No matches. Try a different search.</p>}
  </>;
}

const BUCKET_LABEL:Record<string,string>={
  member_of_congress:'Former member of Congress',
  congressional_leadership:'Top congressional aide',
  executive_branch:'White House / executive branch',
  agency:'Federal agency staff',
  congressional_staff:'Congressional staffer',
  military:'Military / defense',
  other_gov:'Other government job',
  unclear:'Government job',
};

const COUNTRY:Record<string,string>={CAN:'Canada',GBR:'United Kingdom',AUS:'Australia',SUI:'Switzerland',MEX:'Mexico',KOR:'South Korea',ISR:'Israel',UAE:'United Arab Emirates',BRA:'Brazil',NED:'Netherlands',PUR:'Puerto Rico',GER:'Germany',CAY:'Cayman Islands',JPN:'Japan',IRL:'Ireland',LUX:'Luxembourg',CHN:'China',FRA:'France',SWE:'Sweden',NOR:'Norway',BEL:'Belgium',DEN:'Denmark',ITA:'Italy',ESP:'Spain',IND:'India',SGP:'Singapore',HKG:'Hong Kong',TWN:'Taiwan',SAU:'Saudi Arabia',QAT:'Qatar',BHR:'Bahrain',KWT:'Kuwait',BER:'Bermuda',BVI:'British Virgin Islands',VGB:'British Virgin Islands',JEY:'Jersey',GGY:'Guernsey',IMN:'Isle of Man',LIE:'Liechtenstein',MCO:'Monaco',PAN:'Panama',BHS:'Bahamas',BRB:'Barbados',TTO:'Trinidad & Tobago',ARG:'Argentina',CHL:'Chile',COL:'Colombia',PER:'Peru',POL:'Poland',AUT:'Austria',PRT:'Portugal',FIN:'Finland',ISL:'Iceland',EST:'Estonia',LVA:'Latvia',LTU:'Lithuania',CZE:'Czech Republic',SVK:'Slovakia',HUN:'Hungary',ROU:'Romania',BGR:'Bulgaria',GRC:'Greece',TUR:'Turkey',UKR:'Ukraine',RUS:'Russia',GEO:'Georgia',ARM:'Armenia',AZE:'Azerbaijan',KAZ:'Kazakhstan',NGA:'Nigeria',GHA:'Ghana',ZAF:'South Africa',EGY:'Egypt',MAR:'Morocco',TUN:'Tunisia',LBY:'Libya',IRQ:'Iraq',AFG:'Afghanistan',PAK:'Pakistan',BGD:'Bangladesh',LKA:'Sri Lanka',THA:'Thailand',VNM:'Vietnam',MYS:'Malaysia',IDN:'Indonesia',PHL:'Philippines',NZL:'New Zealand',BUL:'Bulgaria',NGR:'Nigeria',GUA:'Guatemala',MKD:'North Macedonia',BGRX:'Bulgaria'};

export function NotableExplorer(){
  const [data,setData]=useState<Notable|null>(null);
  const [mode,setMode]=useState<'spend'|'door'|'foreign'>('spend');
  const [q,setQ]=useState('');const [page,setPage]=useState(0);const [err,setErr]=useState('');
  useEffect(()=>{loadNotable().then(setData).catch(()=>setErr('Could not load this data.'))},[]);
  useEffect(()=>setPage(0),[q,mode]);
  if(err)return <p>{err}</p>;
  if(!data)return <p className="count">Loading…</p>;
  const s=q.trim().toLowerCase();
  const spenders=data.spenders.filter(r=>r.client.toLowerCase().includes(s)||r.topics.some(t=>t.toLowerCase().includes(s)));
  const door=data.revolving_door.filter(r=>r.name.toLowerCase().includes(s)||r.clients.some(c=>c.toLowerCase().includes(s))||(r.former||'').toLowerCase().includes(s));
  const foreign=data.foreign.filter(r=>r.client.toLowerCase().includes(s)||(COUNTRY[r.country]||r.country).toLowerCase().includes(s));
  const rows=mode==='spend'?spenders:mode==='door'?door:foreign;
  return <>
    <div className="hero">
      <h1>Worth a look</h1>
      <p>Who's paying the most, who's lobbying after working in government, and who's headquartered abroad. Federal filings, 2024–2026.</p>
      <p className="secondary">{data.stats.lobbyists_former_gov.toLocaleString()} registered lobbyists disclosed a former government job — including {data.stats.former_members.toLocaleString()} former members of Congress.</p>
    </div>
    <div className="hero-controls">
      <label className="search big-search"><input type="search" value={q} placeholder={mode==='spend'?'Search companies or topics — e.g. Amazon, drug pricing':mode==='door'?'Search people or their clients — e.g. Collins, Eli Lilly':'Search companies or countries — e.g. ByteDance, China'} onChange={e=>setQ(e.target.value)} aria-label="Search"/></label>
      <div className="featured-links" role="group" aria-label="View">
        <button className={mode==='spend'?'year-active':''} onClick={()=>setMode('spend')}>Biggest spenders</button>
        <button className={mode==='door'?'year-active':''} onClick={()=>setMode('door')}>Revolving door</button>
        <button className={mode==='foreign'?'year-active':''} onClick={()=>setMode('foreign')}>Foreign-based clients</button>
      </div>
    </div>
    <p className="count">{rows.length.toLocaleString()} {mode==='spend'?'companies and groups':mode==='door'?'former government insiders':'companies based abroad'}</p>
    {mode==='door'&&<p className="secondary">Ranked by the total reported on filings each person is listed on — a filing's full amount counts toward every lobbyist it names.</p>}
    <div className="org-list">{mode==='spend'?spenders.slice(page*40,(page+1)*40).map((r,i)=>(
      <div key={'s'+i} className="org-row static-row">
        <span className="rank">{page*40+i+1}</span>
        <span className="org-main"><span className="org-name">{r.client}</span>
        <span className="org-sub"><strong>Lobbies on:</strong> {r.topics.join(', ')||'not disclosed'}</span>
        {r.bills.length>0&&<span className="org-sub"><strong>Bills:</strong> {r.bills.slice(0,4).join(' · ')}</span>}
        {r.says.length>0&&<details className="row-details"><summary>What their filings say</summary>{r.says.map((t,j)=><p key={j}>“{t}”</p>)}</details>}</span>
        <span className="org-amt">{dollars(r.total)}<span className="org-sub">{r.filings} filings</span></span>
      </div>)):mode==='door'?door.slice(page*40,(page+1)*40).map((r,i)=>(
      <div key={'d'+i} className="org-row static-row">
        <span className="rank">{page*40+i+1}</span>
        <span className="org-main"><span className="org-name">{r.name} <span className="insider-badge">{BUCKET_LABEL[r.bucket]||'Government job'}</span></span>
        <span className="org-sub">Before: {r.former||'government job'}</span>
        <span className="org-sub">Now lobbying for: {r.clients.join(', ')||'undisclosed'}</span>
        {r.topics.length>0&&<span className="org-sub">On: {r.topics.join(', ')}</span>}</span>
        <span className="org-amt">{dollars(r.total)}<span className="org-sub">{r.filings} filings</span></span>
      </div>)):foreign.slice(page*40,(page+1)*40).map((r,i)=>(
      <div key={'f'+i} className="org-row static-row">
        <span className="rank">{page*40+i+1}</span>
        <span className="org-main"><span className="org-name">{r.client}</span>
        <span className="org-sub"><strong>Lobbies on:</strong> {r.topics.join(', ')||'not disclosed'}</span>
        {r.bills.length>0&&<span className="org-sub"><strong>Bills:</strong> {r.bills.slice(0,4).join(' · ')}</span>}
        {r.says.length>0&&<details className="row-details"><summary>What their filings say</summary>{r.says.map((t,j)=><p key={j}>“{t}”</p>)}</details>}
        <span className="org-sub">{COUNTRY[r.country]||r.country} · {r.filings} filing{r.filings===1?'':'s'}</span></span>
        <span className="org-amt">{dollars(r.total)}</span>
      </div>))}
    </div>
    <Pager page={page} count={rows.length} onChange={setPage}/>
    {!rows.length&&<p>No matches. Try a different search.</p>}
  </>;
}

export function OrgLobbyPanel({orgKey,index}:{orgKey:string;index:LobbyIndex}){
  const [org,setOrg]=useState<OrgLobby|null>(null);
  const [filings,setFilings]=useState<FilingDetail[]|null>(null);
  const [open,setOpen]=useState(false);
  const [err,setErr]=useState('');
  useEffect(()=>{setOrg(null);setFilings(null);setOpen(false);setErr('');
    loadOrgLobby(orgKey).then(o=>{setOrg(o);loadOrgFilings(o.filing_ids).then(setFilings).catch(()=>{})}).catch(()=>setErr('No lobbying detail for this organization.'))},[orgKey]);
  if(err)return null;
  if(!org)return <p className="secondary">Loading lobbying detail…</p>;
  const latest=(filings||[]).filter(f=>f.latest).sort((a,b)=>b.posted.localeCompare(a.posted));
  const issueNames=Object.entries(org.issues);
  return <section className="profile" aria-label="Lobbying activity">
    <h2 style={{fontSize:20,marginTop:0}}>Lobbying activity · 2024–2026</h2>
    <p>{org.name} reported <strong>{dollars(org.total)}</strong> in lobbying across {org.filings} filing{org.filings===1?'':'s'}{org.firms.length?<> via {org.firms.length===1?'firm ':'firms '}<strong>{org.firms.slice(0,4).map(f=>readable(f.name||'')).join(', ')}{org.firms.length>4?' and more':''}</strong></>:null}.</p>
    {!!org.lobbyists.length&&<p className="secondary">Named lobbyists: {org.lobbyists.slice(0,12).join(', ')}{org.lobbyists.length>12?` +${org.lobbyists.length-12} more`:''}</p>}
    {org.topics&&Object.keys(org.topics).length>0&&<p className="secondary"><strong>Top topics:</strong> {Object.keys(org.topics).slice(0,8).map(t=>index.topic_names?.[t]||t).join(' · ')}</p>}
    {issueNames.length>0&&<dl>{issueNames.map(([code,amt])=><div key={code}><dt>{index.issue_codes[code]||code}</dt><dd className="amount">{dollars(amt)}</dd></div>)}</dl>}
    {!!org.sample_texts.length&&<details><summary>What the filings say ({org.sample_texts.length})</summary><ul>{org.sample_texts.map((t,i)=><li key={i}>{t}</li>)}</ul></details>}
    {latest.length>0&&<details open={open} onToggle={e=>setOpen((e.target as HTMLDetailsElement).open)}>
      <summary>Filing detail ({latest.length} latest)</summary>
      <ul>{latest.slice(0,30).map(f=><li key={f.id}>
        <strong>{f.kind} · {f.year} · {dollars(f.amount)}</strong>{f.firm?` — ${readable(f.firm||'')}`:''}
        {f.activities.map((a,i)=><div key={i} className="secondary">
          {a.issue||a.code}{a.topic?` · ${index.topic_names?.[a.topic]||a.topic}`:''}{a.text?` — ${a.text}`:''}
          {a.lobbyists.length>0&&<span><br/>Lobbyists: {a.lobbyists.map(l=>l.name).join(', ')}</span>}
          {a.agencies.length>0&&<span><br/>Contacted: {a.agencies.join('; ')}</span>}
        </div>)}
      </li>)}</ul>
      {latest.length>30&&<p className="secondary">Showing 30 of {latest.length}.</p>}
    </details>}
  </section>;
}
