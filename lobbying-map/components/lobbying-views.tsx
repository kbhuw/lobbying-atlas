'use client';
import {useEffect,useMemo,useState} from 'react';
import {Table,TableHeader,TableBody,TableRow,TableHead,TableCell} from '@/components/ui/table';
import {Button} from '@/components/ui/button';
import {LobbyIndex,IssueBoard,TopicBoard,FirmDetail,OrgLobby,FilingDetail,loadIndex,loadIssue,loadTopic,loadFirm,loadOrgLobby,loadOrgFilings,dollars} from '@/lib/lobbying';
import {readable} from '@/lib/directory';

function Pager({page,count,onChange}:{page:number;count:number;onChange:(n:number)=>void}){
  return <div className="pager"><span>{count?(page*40+1).toLocaleString()+'–'+Math.min((page+1)*40,count).toLocaleString():'0'} of {count.toLocaleString()}</span><Button variant="outline" disabled={!page} onClick={()=>onChange(page-1)}>Previous</Button><Button variant="outline" disabled={(page+1)*40>=count} onClick={()=>onChange(page+1)}>Next</Button></div>;
}

export function IssuesExplorer({year:initialYear,onOpenOrg}:{year:number;onOpenOrg:(orgKey:string)=>void}){
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
      <p className="secondary">Who lobbied on this in {year}. Amounts attribute each filing's full reported amount to every issue it lists.</p>
      <YearPicker index={index} year={year} onChange={setYear}/>
      <div className="controls"><label className="search"><span>Search organizations</span><input type="search" value={q} placeholder="Organization name" onChange={e=>setQ(e.target.value)}/></label></div>
      <p className="count">{orgs.length.toLocaleString()} organizations</p>
      <Table><TableHeader><TableRow><TableHead>Organization</TableHead><TableHead>Reported spend</TableHead><TableHead>Filings</TableHead></TableRow></TableHeader>
      <TableBody>{orgs.slice(page*40,(page+1)*40).map(o=><TableRow key={o.id}>
        <TableCell><button className="name" onClick={()=>onOpenOrg(o.id)}>{o.name}</button></TableCell>
        <TableCell className="amount">{dollars(o.amount)}</TableCell>
        <TableCell>{o.filings}</TableCell></TableRow>)}</TableBody></Table>
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
  return <>
    <h1>Who lobbied for what</h1>
    <p className="secondary">Pick a topic to see which organizations reported lobbying on it, ranked by reported spend.{hasTopics?' Topics are AI-normalized from the free-text descriptions on each filing; issue areas are the official LDA categories.':''}</p>
    {hasTopics&&<div className="featured-links" role="group" aria-label="View">
      <button className={mode==='topics'?'year-active':''} onClick={()=>{setMode('topics');setCode(null)}}>Topics</button>
      <button className={mode==='codes'?'year-active':''} onClick={()=>{setMode('codes');setCode(null)}}>Issue areas</button></div>}
    <YearPicker index={index} year={year} onChange={setYear}/>
    <div className="controls"><label className="search"><span>Search</span><input type="search" value={q} placeholder={mode==='topics'?'Topic':'Issue area'} onChange={e=>setQ(e.target.value)}/></label></div>
    <Table><TableHeader><TableRow><TableHead>{mode==='topics'?'Topic':'Issue area'}</TableHead><TableHead>Organizations</TableHead><TableHead>Reported spend</TableHead></TableRow></TableHeader>
    <TableBody>{rows.map(r=><TableRow key={r.c}>
      <TableCell><button className="name" onClick={()=>setCode(r.c)}>{r.name}</button></TableCell>
      <TableCell>{r.organizations.toLocaleString()}</TableCell>
      <TableCell className="amount">{dollars(r.amount)}</TableCell></TableRow>)}</TableBody></Table>
  </>;
}

function YearPicker({index,year,onChange}:{index:LobbyIndex;year:number;onChange:(y:number)=>void}){
  return <div className="featured-links" role="group" aria-label="Reporting year">{[...index.years].sort((a,b)=>b-a).map(y=>
    <button key={y} className={y===year?'year-active':''} onClick={()=>onChange(y)}>{y}</button>)}</div>;
}

export function FirmsExplorer({onOpenOrg}:{onOpenOrg:(orgKey:string)=>void}){
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
      <Table><TableHeader><TableRow><TableHead>Client</TableHead><TableHead>Issues</TableHead><TableHead>Reported income</TableHead></TableRow></TableHeader>
      <TableBody>{clients.slice(page*40,(page+1)*40).map(c=><TableRow key={String(c.key)}>
        <TableCell><button className="name" onClick={()=>onOpenOrg(c.key)}>{c.name}</button></TableCell>
        <TableCell><span className="secondary">{c.issues.slice(0,4).map(i=>index.issue_codes[i]||i).join(' · ')}</span></TableCell>
        <TableCell className="amount">{dollars(c.amount)}</TableCell></TableRow>)}</TableBody></Table>
      <Pager page={page} count={clients.length} onChange={setPage}/>
    </>;
  }

  const s=q.trim().toLowerCase();
  const firms=index.top_firms.filter(f=>(f.name||'').toLowerCase().includes(s));
  return <>
    <h1>Lobbying firms</h1>
    <p className="secondary">Firms ranked by reported lobbying income, 2024–2026. In-house teams appear when they file for their own organization.</p>
    <div className="controls"><label className="search"><span>Search firms</span><input type="search" value={q} placeholder="Firm name" onChange={e=>setQ(e.target.value)}/></label></div>
    <p className="count">{firms.length.toLocaleString()} registrants</p>
    <Table><TableHeader><TableRow><TableHead>Firm</TableHead><TableHead>Clients</TableHead><TableHead>Reported income</TableHead></TableRow></TableHeader>
    <TableBody>{firms.slice(page*40,(page+1)*40).map(f=><TableRow key={f.id}>
      <TableCell><button className="name" onClick={()=>loadFirm(f.id).then(setFirm).catch(()=>setErr('Could not load this firm.'))}>{readable(f.name||'')}</button></TableCell>
      <TableCell>{f.clients.toLocaleString()}</TableCell>
      <TableCell className="amount">{dollars(f.total)}</TableCell></TableRow>)}</TableBody></Table>
    <Pager page={page} count={firms.length} onChange={setPage}/>
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
