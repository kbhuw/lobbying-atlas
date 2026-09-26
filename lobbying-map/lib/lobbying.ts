import {readData} from './directory';

export type LobbyIndex={
  years:number[];filings:number;activities:number;clients:number;firms:number;
  top_firms:{id:number;name:string;total:number;filings:number;clients:number}[];
  issue_codes:Record<string,string>;
  issue_index:Record<string,Record<string,{organizations:number;amount:number}>>;
  topic_names?:Record<string,string>;
  topic_index?:Record<string,Record<string,{organizations:number;amount:number}>>;
};
export type Activity={code:string|null;issue:string|null;text:string|null;
  agencies:string[];topic?:string|null;
  lobbyists:{name:string;covered_position:string|null;new:boolean}[]};
export type FilingDetail={id:string;senate_id:string|null;form:string;
  group_id:string|null;client:string;
  firm_id:number|null;firm:string;kind:string;year:number;period:string;
  amount:number|null;income:number|null;expenses:number|null;posted:string;
  terminated:string|null;latest:boolean;activities:Activity[]};
export type IssueBoard={code:string;name:string;year:number;
  organizations:{id:string;name:string;amount:number|null;filings:number}[]};
export type TopicBoard={topic:string;name:string;year:number;
  organizations:{id:string;name:string;amount:number|null;filings:number}[]};
export type FirmDetail={id:number;name:string;total:number;filings:number;
  clients:{key:string;name:string;amount:number;filings:number;issues:string[]}[];
  issues:Record<string,number>;topics?:Record<string,number>};
export type OrgLobby={id:string;group_id:string|null;name:string;
  total:number;filings:number;years:number[];issues:Record<string,number>;
  topics?:Record<string,number>;
  firms:{firm_id:number;name:string;amount:number;filings:number}[];
  lobbyists:string[];filing_ids:string[];sample_texts:string[]};

const get=async<T>(path:string):Promise<T>=>{
  const r=await fetch(path);
  if(!r.ok)throw new Error(path);
  return readData<T>(r);
};

export const loadIndex=()=>get<LobbyIndex>('/data/lobbying/index.json.gz');
export const loadIssue=(code:string,year:number)=>get<IssueBoard>(`/data/lobbying/issues/${code}-${year}.json.gz`);
export const loadTopic=(topic:string,year:number)=>get<TopicBoard>(`/data/lobbying/topics/${topic}-${year}.json.gz`);
export const loadFirm=(id:number)=>get<FirmDetail>(`/data/lobbying/firms/${id}.json.gz`);
export const loadOrgLobby=(key:string)=>get<OrgLobby>(`/data/lobbying/orgs/${key}.json.gz`);

export type Insider={name:string;bucket:string;former:string;total:number;
  filings:number;clients:string[];topics:string[]};
export type ForeignClient={client:string;country:string;filings:number;
  total:number;topics:string[];bills:string[];says:string[]};
export type Spender={client:string;total:number;filings:number;topics:string[];
  bills:string[];says:string[]};
export type Notable={revolving_door:Insider[];foreign:ForeignClient[];
  spenders:Spender[];
  stats:{lobbyists_former_gov:number;former_members:number}};
export const loadNotable=()=>get<Notable>('/data/lobbying/notable.json.gz');

// Filing shards are keyed by sha256(doc_id)[:2] (WebCrypto has no MD5).
async function sha256hex(s:string){
  const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
}
export async function loadOrgFilings(filingIds:string[]):Promise<FilingDetail[]>{
  const prefixes=[...new Set(await Promise.all(filingIds.map(async id=>(await sha256hex(id)).slice(0,2))))];
  const shards=await Promise.all(prefixes.map(p=>get<FilingDetail[]>(`/data/lobbying/filings/${p}.json.gz`)));
  const want=new Set(filingIds);
  return shards.flat().filter(f=>want.has(f.id));
}

export const dollars=(n:number|null|undefined)=>n==null?'Not disclosed':
  n.toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});

export const periodOrder=(p:string)=>({Registration:0,Q1:1,Q2:2,Q3:3,Q4:4} as Record<string,number>)[p]??0;
