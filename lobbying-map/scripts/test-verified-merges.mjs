import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {gunzipSync} from 'node:zlib';
import {applyVerifiedMerges} from './data/verified-merges.mjs';
import {applyVerifiedSplits} from './data/verified-splits.mjs';
import {readReviewedProfiles} from './data/reviewed-profiles.mjs';
const read=p=>JSON.parse(gunzipSync(readFileSync(p)));
const before=read('research/directory-base.json.gz');
before.companies=applyVerifiedSplits(before.companies,JSON.parse(readFileSync('research/verified-entity-splits.json')),id=>read(`public/data/reports/${id.slice(0,2)}.json.gz`)[id]);
const after=read('public/data/directory-v3.json.gz');
const decisions=JSON.parse(readFileSync('research/verified-entity-merges.json'));
const original=new Map(before.companies.map(c=>[c.id,c]));
const reviewed={...JSON.parse(readFileSync('research/profiles.json')),...readReviewedProfiles()};
const mergedIds=new Set(decisions.flatMap(d=>d.source_ids));
assert.equal(after.companies.length,before.companies.length-decisions.reduce((n,d)=>n+d.source_ids.length-1,0));
assert.deepEqual(after.companies.flatMap(c=>c.members).sort(),before.companies.flatMap(c=>c.members).sort());
for(const c of after.companies){
 if(!c.identity_merge){assert(!mergedIds.has(c.id));continue;}
 const d=decisions.find(d=>d.canonical_id===c.id);assert.deepEqual(c.identity_merge,d);
 assert.deepEqual(c.source_records.map(x=>x.id),d.source_ids);
 for(const source of c.source_records){
  const base=original.get(source.id),profile=reviewed[source.id]||base.profile;
  assert.deepEqual(source,{...base,...(profile?{profile,name:profile.name}:{})});
  assert(after.companies.find(x=>x.id===source.id||x.members.includes(source.id))===c,'Old links resolve to merged card');
 }
 assert.deepEqual(c.aliases,[...new Set(c.source_records.flatMap(x=>x.aliases))]);
 for(const s of c.source_records.flatMap(x=>x.profile.sources))assert(c.profile.sources.some(v=>v.url===s.url&&v.claim===s.claim));
}
// A shared firm's newer no-activity filing supersedes older activity even when
// it appeared under another alias. A second firm still contributes one row.
const card=id=>({id,name:id,members:[id],aliases:[id],issues:[],years:{2026:1},profile:{status:'sourced',sources:[]}});
const report=(id,firm,posted,kind)=>({id,registrant:firm,year:2026,posted_iso:posted,kind});
const shared=report('active','Firm','2026-04-01','1st Quarter - Report');
const reports={a:[shared],b:[shared,report('inactive','FIRM','2026-04-02','1st Quarter - No Activity'),report('other','Other Firm','2026-04-01','1st Quarter - Report')]};
const decision={canonical_id:'a',source_ids:['a','b'],rationale:'Verified aliases',sources:[{url:'https://example.com',claim:'Fixture'}]};
const result=applyVerifiedMerges([card('a'),card('b')],[decision],id=>reports[id]);
assert.deepEqual(result[0].years,{'2026':1});
assert.throws(()=>applyVerifiedMerges([card('a'),card('b')],[decision,decision],id=>reports[id]),/overlapping/);
console.log(`Verified ${decisions.length} identity merges; original cards, sources, links and filings preserved.`);
