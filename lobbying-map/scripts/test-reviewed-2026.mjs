import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {gunzipSync} from 'node:zlib';
import {createHash} from 'node:crypto';
import {readReviewedProfiles} from './data/reviewed-profiles.mjs';
const p=readReviewedProfiles();
const data=JSON.parse(gunzipSync(readFileSync('public/data/directory-v3.json.gz')));
const manifest=JSON.parse(readFileSync('research/reviewed-2026-manifest.json','utf8'));
assert.equal(manifest.reviewed_ids.length,18036);
assert.deepEqual(Object.keys(p).sort(),manifest.reviewed_ids);
assert.deepEqual([...new Set(manifest.batches.flatMap(b=>b.ids))].sort(),manifest.reviewed_ids);
const originalCards=new Map(data.companies.flatMap(c=>c.source_records||[c]).map(c=>[c.id,c]));
for(const [id,v] of Object.entries(p)){
 const c=originalCards.get(id);assert(c?.years['2026']);assert.deepEqual(c.profile,v);
 assert(v.sources.length&&v.identity_evidence&&v.description.length>20);
 assert(!v.description.startsWith('IRS activity classification:'));
 assert(!v.sources.some(s=>s.url.includes('undefined')));
 if(id !== 'b1c76d600f96d3ab') assert(!v.sources.some(s=>new URL(s.url).hostname === 'atzmanufacturing.com'), `${id}: unrelated ATZ citation leaked from a batch script`);
 for(const url of [v.website,v.logo_url,...v.sources.map(s=>s.url)].filter(Boolean)){
  assert(!/^https?:\/\/https?:\/\//i.test(url),`${id}: duplicated URL protocol`);
  const ldaRecord = url.match(/^https:\/\/lda\.gov\/api\/v1\/(?:clients|registrants)\/([^/?]+)/i);
  if(ldaRecord) assert(/^\d+$/.test(ldaRecord[1]),`${id}: LDA API record IDs must be numeric`);
 }
 if(v.logo_url){
  assert(!v.logo_url.includes('static.parastorage.com/client/pfavico.ico'));
  const localLogo=v.logo_url.match(/^\/assets\/organization-logos\/([a-f0-9]{64})\.(svg|png|webp)$/);
  assert(v.logo_url.startsWith('https://')||localLogo);
  if(localLogo){
   const asset=readFileSync(`public${v.logo_url}`);
   assert.equal(createHash('sha256').update(asset).digest('hex'),localLogo[1]);
   assert.deepEqual(readFileSync(`dist/client${v.logo_url}`),asset,'Local logo must be included unchanged in the build');
  }
  assert(v.logo_source_url?.startsWith('https://'));assert(['logo','site_icon'].includes(v.logo_kind));assert.equal(v.logo_status,'official_site_asset');
 }
 if(v.status==='unresolved'){assert.equal(v.website,'');assert.equal(v.review_outcome,'unresolved')}
}
assert.equal(p['0abe5b7cf46d3470'].ownership,'Subsidiary of public company');
assert.equal(p['65a085bed4d3b491'].ownership,'Unknown');
assert(p['7595bb424fff28dc'].website.includes('activate.org'));
assert(!p['7595bb424fff28dc'].sources.some(s=>s.url.includes('activateglobally')));
assert(!p['0667298c4d614051'].sources.some(s=>s.url.includes('modernstates')));
assert.equal(p['4e468de3d5724730'].website,'https://www.nalc.org/');
assert.equal(p['4e13272ab4ed3540'].name,'Electronic Frontier Foundation');
assert.equal(p['ba4ab3c6bd789b8d'].name,'Addus HomeCare');
assert(!JSON.stringify(p['ba4ab3c6bd789b8d'].sources).includes('accendrahealth.com'));
assert.equal(p['67ac8fd8a092c612'].website,'https://www.elementdefense.com/');
assert(!JSON.stringify(p['67ac8fd8a092c612'].sources).includes('elementlpower.io'));
assert.equal(p['4e13272ab4ed3540'].website,'https://www.eff.org/');
assert(!p['4e13272ab4ed3540'].sources.some(s=>s.url.includes('elementbiosciences')));
assert(!data.companies.some(c=>c.source_records?.some(s=>s.id==='4e13272ab4ed3540') && c.source_records?.some(s=>s.id==='4f39ee6592e77d57')));
assert(!p['4e468de3d5724730'].sources.some(s=>/520908160|branch142/i.test(JSON.stringify(s))));
console.log('2026 review invariants passed; 18036 exact IDs, unresolved identities and corrected parent relationships preserved.');
