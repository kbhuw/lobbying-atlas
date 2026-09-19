import {groupReports} from '../../lib/directory.ts';

// Only evidence-reviewed identity decisions belong here. Similar names never
// trigger a merge automatically; the original cards remain losslessly embedded.
export function applyVerifiedMerges(companies, decisions, reportsForMember) {
  const byId = new Map(companies.map(c => [c.id, c]));
  const used = new Set();
  const replacements = new Map();
  for (const decision of decisions) {
    const {canonical_id, source_ids, rationale, sources} = decision;
    if (source_ids.length < 2 || !source_ids.includes(canonical_id) || !rationale || !sources?.length)
      throw new Error('Incomplete verified merge decision');
    const records = source_ids.map(id => {
      if (used.has(id) || !byId.has(id)) throw new Error(`Invalid or overlapping merge ID: ${id}`);
      used.add(id);
      const c = byId.get(id);
      if (!c.profile || c.profile.status !== 'sourced' || c.identity_merge || c.filing_ids)
        throw new Error(`Merge requires individually sourced original records: ${id}`);
      return c;
    });
    const canonical = byId.get(canonical_id);
    const members = [...new Set(records.flatMap(c => c.members))];
    const reports = members.flatMap(id => reportsForMember(id));
    const years = {};
    for (const group of groupReports(reports)) if (group.active)
      years[group.year] = (years[group.year] || 0) + 1;
    const unique = new Map(records.flatMap(c => c.profile.sources).map(s => [JSON.stringify([s.url, s.claim]), s]));
    replacements.set(canonical_id, {
      ...canonical,
      aliases: [...new Set(records.flatMap(c => c.aliases))],
      members,
      issues: [...new Set(records.flatMap(c => c.issues))].sort(),
      years,
      profile: {...canonical.profile, sources: [...unique.values()], notes: rationale,
        identity_evidence: rationale, featured: records.some(c => c.profile.featured)},
      identity_merge: decision,
      source_records: records,
    });
  }
  return companies.flatMap(c => replacements.has(c.id) ? [replacements.get(c.id)] : used.has(c.id) ? [] : [c]);
}
