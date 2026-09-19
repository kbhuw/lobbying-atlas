import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {gunzipSync} from 'node:zlib';
import {applyVerifiedSplits} from './data/verified-splits.mjs';
const read=p=>JSON.parse(gunzipSync(readFileSync(p)));
const before=read('public/data/directory-v2.json.gz'),after=read('public/data/directory-v3.json.gz');
before.companies=applyVerifiedSplits(before.companies,JSON.parse(readFileSync('research/verified-entity-splits.json')),id=>read(`public/data/reports/${id.slice(0,2)}.json.gz`)[id]);
const originals=after.companies.flatMap(c=>c.source_records||[c]);
assert.equal(originals.length,before.companies.length);
assert.equal(new Set(originals.map(c=>c.id)).size,before.companies.length);
const old=new Map(before.companies.map(c=>[c.id,c]));
const counts={};
for(const c of originals){
 assert.deepEqual(c.members,old.get(c.id).members); assert.deepEqual(c.years,old.get(c.id).years);assert.deepEqual(c.aliases,old.get(c.id).aliases);
 const p=c.profile;const status=p?.status||'pending';counts[status]=(counts[status]||0)+1;
 if(p){assert(p.sources.length);for(const s of p.sources){const url=new URL(s.url);assert(url.protocol==='https:'||(url.protocol==='http:'&&p.website_status==='verified'&&p.website&&new URL(p.website).protocol==='http:'&&url.hostname===new URL(p.website).hostname),'Sources must use HTTPS, except verified official sites available only over HTTP');assert(s.claim);assert(!s.url.includes('undefined'));assert(!s.url.includes('google.com/search'))}
  assert(p.as_of);
  if(p.status==='registry_matched'){assert.equal(p.registry.match,'name_city_state');assert(p.sources.length>=2);assert.equal(p.featured,false)}
  if(p.status==='self_reported'){assert.equal(p.kind,'Unknown');assert.equal(p.ownership,'Unknown');assert.equal(p.featured,false)}
 }
}
assert.deepEqual(counts,after.research.counts);
const get=id=>after.companies.find(c=>c.id===id);
assert.equal(get('689fc334b6c0acb5').name,'1 Inc.');
assert.equal(get('8af369e769021e01').name,'1,000 Days');
assert.equal(get('b39442bdc274fb46').name,'#10 Enterprises LLC');
assert.equal(get('b39442bdc274fb46').profile.ownership,'Unknown');
assert.notEqual(get('458c30bd9c4bc0ba').profile.ownership,'Publicly traded');
assert.equal(get('aabb2501084cfbce').profile.ownership,'Subsidiary of public company');
console.log(JSON.stringify({tests:'passed',entries:after.companies.length,counts}));

assert.equal(get('04ce9d62458497d5').profile.status,'sourced');
assert.equal(get('0f6187133c1bd69e').profile.name,'Visa');
assert.equal(get('005a36a209d27215').profile.ownership,'Subsidiary of public company');
