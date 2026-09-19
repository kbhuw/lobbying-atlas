import assert from 'node:assert/strict';
import {groupReports} from '../../lib/directory.ts';

// Undo a reviewed name normalization without deleting any original filing group.
export function applyVerifiedSplits(companies, decisions, reportsForMember) {
  const byId = new Map(companies.map(c => [c.id, c]));
  const replacements = new Map();
  const allocated = new Set(companies.map(c => c.id));
  for (const d of decisions) {
    const original = byId.get(d.source_id);
    assert(original && !replacements.has(d.source_id), 'Unknown or repeated split');
    assert(d.rationale && d.sources?.length && d.children.length > 1);
    const filingSplit = d.mode === 'filings';
    if (filingSplit) {
      assert(d.children.every(c => c.filing_ids?.length), 'Every child needs explicit filings');
      assert.deepEqual([...new Set(d.children.flatMap(c => c.members))].sort(), [...original.members].sort());
      assert.deepEqual([...new Set(d.children.flatMap(c => c.aliases))].sort(), [...original.aliases].sort());
      assert.deepEqual(d.children.flatMap(c => c.filing_ids).sort(), original.members.flatMap(reportsForMember).map(r => r.id).sort(), 'Filing split must preserve every filing exactly once');
    } else {
      assert.deepEqual(d.children.flatMap(c => c.members).sort(), [...original.members].sort(), 'Split must preserve every member exactly once');
      assert.deepEqual(d.children.flatMap(c => c.aliases).sort(), [...original.aliases].sort(), 'Split must preserve every original name');
    }
    replacements.set(d.source_id, d.children.map(child => {
      assert(filingSplit || child.members.includes(child.id));
      assert(child.id === d.source_id || !allocated.has(child.id), 'Split ID collision');
      allocated.add(child.id);
      const years = {};
      const allowed = filingSplit ? new Set(child.filing_ids) : null;
      for (const g of groupReports(child.members.flatMap(reportsForMember).filter(r => !allowed || allowed.has(r.id))))
        if (g.active) years[g.year] = (years[g.year] || 0) + 1;
      return {...child, years, identity_split: {source_id: d.source_id, rationale: d.rationale, sources: d.sources}};
    }));
  }
  return companies.flatMap(c => replacements.get(c.id) || [c]);
}
