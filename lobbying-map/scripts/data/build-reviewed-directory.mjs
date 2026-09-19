import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { gunzipSync, gzipSync } from 'node:zlib';
import { createHash } from 'node:crypto';
import {applyVerifiedMerges} from './verified-merges.mjs';
import {applyVerifiedSplits} from './verified-splits.mjs';
import {readReviewedProfiles} from './reviewed-profiles.mjs';
const base = JSON.parse(gunzipSync(readFileSync('research/directory-base.json.gz')));
const shards = new Map();
const reportsForMember = id => {
  const prefix = id.slice(0, 2);
  if (!shards.has(prefix)) shards.set(prefix, JSON.parse(gunzipSync(readFileSync(`public/data/reports/${prefix}.json.gz`))));
  const reports = shards.get(prefix)[id];
  if (!reports) throw new Error(`Missing filings for member ${id}`);
  return reports;
};
const splits = JSON.parse(readFileSync('research/verified-entity-splits.json'));
const splitIncrease = splits.filter(d => d.mode !== 'filings').reduce((n, d) => n + d.children.length - 1, 0);
base.companies = applyVerifiedSplits(base.companies, splits, reportsForMember);
base.merged_name_variants -= splitIncrease;
const profiles = {...JSON.parse(readFileSync('research/profiles.json')), ...readReviewedProfiles({sync: true})};
const known = new Set(base.companies.map(c => c.id));
for (const id of Object.keys(profiles)) if (!known.has(id)) throw new Error(`Missing directory ID: ${id}`);
const counts = {};
for (const c of base.companies) {
  if (profiles[c.id]) { c.profile = profiles[c.id]; c.name = c.profile.name; }
  const status = c.profile?.status || 'pending';
  counts[status] = (counts[status] || 0) + 1;
}
const metadata = JSON.parse(readFileSync('research/publication-metadata.json'));
for (const key of new Set([...Object.keys(counts), ...Object.keys(metadata.counts)])) {
  if ((counts[key] || 0) !== (metadata.counts[key] || 0)) throw new Error(`Research count differs: ${key}`);
}
base.research = {...metadata, source_name_groups: base.companies.length};
const decisions = JSON.parse(readFileSync('research/verified-entity-merges.json'));
base.companies = applyVerifiedMerges(base.companies, decisions, reportsForMember);
base.research.displayed_organizations = base.companies.length;
const data = gzipSync(Buffer.from(JSON.stringify(base)), {level: 9});
mkdirSync('public/data', {recursive: true});
writeFileSync('public/data/directory-v3.json.gz', data);
console.log(`Built ${Object.keys(profiles).length} annotation overlays; SHA256 ${createHash('sha256').update(data).digest('hex')}`);
