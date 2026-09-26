"""Parse House bulk XML zips (LOBBYINGDISCLOSURE1/2) into a filings-detail sqlite.

Source: https://disclosurespreview.house.gov/data/LD/{Year}_{Period}_XML.zip
Each zip member is one filed document. senateID on LD-2 docs is
'<registrant_senate_id>-<client_senate_id>' — the canonical numeric IDs the
LDA API exposes as registrant.id / client.id. On LD-1 registrations it is the
registrant id alone (new clients do not yet have a senate id on the doc).

Usage: python3 parse_house_xml.py <raw_zip_dir> <out.sqlite>
"""
import pathlib, zipfile, sqlite3, sys, datetime, re
import xml.etree.ElementTree as ET

SCHEMA = """
CREATE TABLE IF NOT EXISTS filings(
  doc_id TEXT PRIMARY KEY,           -- zipname/member
  senate_id TEXT,
  form TEXT,                          -- LD-1 | LD-2
  filing_type TEXT,                   -- reportType / regType
  filing_year INTEGER,
  income REAL, expenses REAL, expenses_method TEXT,
  dt_posted TEXT,                     -- ISO from signedDate
  termination_date TEXT, effective_date TEXT,
  no_lobbying INTEGER,
  client_id INTEGER, client_name TEXT, client_state TEXT, client_country TEXT,
  client_description TEXT, client_self_select TEXT,
  registrant_id INTEGER, registrant_name TEXT, registrant_description TEXT,
  source_zip TEXT);
CREATE TABLE IF NOT EXISTS activities(
  doc_id TEXT, idx INTEGER, issue_code TEXT, description TEXT,
  agencies TEXT, foreign_entity_issues TEXT,
  PRIMARY KEY(doc_id,idx));
CREATE TABLE IF NOT EXISTS lobbyists(
  doc_id TEXT, activity_idx INTEGER, first_name TEXT, last_name TEXT,
  suffix TEXT, covered_position TEXT, new TEXT);
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT);
CREATE INDEX IF NOT EXISTS ix_f_client ON filings(client_id);
CREATE INDEX IF NOT EXISTS ix_f_reg ON filings(registrant_id);
CREATE INDEX IF NOT EXISTS ix_act_code ON activities(issue_code);
"""

def txt(x, tag):
    v = x.findtext(tag)
    return ' '.join((v or '').split()) or None

def txt_ci(x, tag):  # LD-1 uses clientZipExt; LD-2 clientZipext etc.
    for t in (tag, tag.lower(), tag.upper()):
        v = x.findtext(t)
        if v and v.strip():
            return ' '.join(v.split())
    # last resort: case-insensitive scan
    for el in x.iter():
        if el.tag.lower() == tag.lower() and el.text and el.text.strip():
            return ' '.join(el.text.split())
    return None

def iso_date(s):
    if not s:
        return None
    s = s.strip()
    for fmt in ('%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.datetime.strptime(s, fmt).isoformat()
        except ValueError:
            pass
    m = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', s)
    return f'{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}' if m else s

def parse_money(s):
    try:
        return float(s.replace(',', '')) if s and s.strip() else None
    except ValueError:
        return None

def reg_name(x):
    return txt(x, 'organizationName') or ' '.join(
        p for p in (txt(x, 'prefix'), txt(x, 'firstName'), txt(x, 'lastName')) if p) or None


def parse_ld2(x, doc_id, zipname):
    sid = txt(x, 'senate_id'.upper()) or txt(x, 'senateID')
    reg_id, client_id = None, None
    if sid and '-' in sid:
        a, b = sid.split('-', 1)
        reg_id, client_id = int(a) if a.isdigit() else None, int(b) if b.isdigit() else None
    f = (doc_id, sid, 'LD-2', txt(x, 'reportType'),
         int(txt(x, 'reportYear') or 0) or None,
         parse_money(txt(x, 'income')), parse_money(txt(x, 'expenses')),
         txt(x, 'expensesMethod'), iso_date(txt(x, 'signedDate')),
         txt(x, 'terminationDate'), None,
         1 if (txt(x, 'noLobbying') or '').upper() == 'Y' else 0,
         client_id, txt(x, 'clientName'), txt_ci(x, 'clientState'),
         txt_ci(x, 'clientCountry'), txt(x, 'generalDescription'), txt(x, 'selfSelect'),
         reg_id, reg_name(x), None, zipname)
    acts, lobs = [], []
    for i, a in enumerate(x.findall('.//ali_info')):
        code = txt(a, 'issueAreaCode')
        descs = [d.text.strip() for d in a.findall('.//specific_issues/description') if d.text and d.text.strip()]
        acts.append((doc_id, i, code, '\n'.join(descs) or None, txt(a, 'federal_agencies'),
                     txt(a, 'foreign_entity_issues')))
        for l in a.findall('.//lobbyists/lobbyist'):
            fn, ln = txt(l, 'lobbyistFirstName'), txt(l, 'lobbyistLastName')
            if not (fn or ln):
                continue
            lobs.append((doc_id, i, fn, ln, txt(l, 'lobbyistSuffix'),
                         txt(l, 'coveredPosition'), txt(l, 'lobbyistNew')))
    return f, acts, lobs

def parse_ld1(x, doc_id, zipname):
    sid = txt(x, 'senateID')
    reg_id = int(sid) if sid and sid.isdigit() else None
    f = (doc_id, sid, 'LD-1', txt(x, 'regType'), None, None, None, None,
         iso_date(txt(x, 'signedDate')), None, iso_date(txt(x, 'effectiveDate')), 0,
         None, txt(x, 'clientName'), txt_ci(x, 'clientState'), txt_ci(x, 'clientCountry'),
         txt(x, 'clientGeneralDescription'), txt(x, 'selfSelect'),
         reg_id, reg_name(x), txt(x, 'registrantGeneralDescription'), zipname)
    acts, lobs = [], []
    codes = [c.text.strip() for c in x.findall('.//alis/ali_Code') if c.text and c.text.strip()]
    for i, code in enumerate(codes):
        acts.append((doc_id, i, code, None, None, None))
        for l in x.findall('.//lobbyists/lobbyist'):
            fn, ln = txt(l, 'lobbyistFirstName'), txt(l, 'lobbyistLastName')
            if fn or ln:
                lobs.append((doc_id, i, fn, ln, txt(l, 'lobbyistSuffix'),
                             txt(l, 'coveredPosition'), txt(l, 'lobbyistNew')))
    return f, acts, lobs

def main(raw_dir, out):
    db = sqlite3.connect(out)
    db.executescript(SCHEMA)
    done = {r[0] for r in db.execute('select value from meta where key like ?', ('zip:%',))}
    for zp in sorted(pathlib.Path(raw_dir).glob('*.zip')):
        if zp.name in done:
            continue
        nf = na = nl = err = 0
        with zipfile.ZipFile(zp) as z:
            for member in z.namelist():
                if not member.lower().endswith('.xml'):
                    continue
                doc_id = f'{zp.name}/{member}'
                try:
                    x = ET.fromstring(z.read(member))
                    if x.tag == 'LOBBYINGDISCLOSURE2':
                        f, acts, lobs = parse_ld2(x, doc_id, zp.name)
                    elif x.tag == 'LOBBYINGDISCLOSURE1':
                        f, acts, lobs = parse_ld1(x, doc_id, zp.name)
                    else:
                        continue
                    db.execute('INSERT OR REPLACE INTO filings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', f)
                    db.executemany('INSERT OR REPLACE INTO activities VALUES(?,?,?,?,?,?)', acts)
                    db.executemany('INSERT OR REPLACE INTO lobbyists VALUES(?,?,?,?,?,?,?)', lobs)
                    nf += 1; na += len(acts); nl += len(lobs)
                except Exception as e:
                    err += 1
                    if err < 5:
                        print('ERR', doc_id, e, flush=True)
        db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)', (f'zip:{zp.name}', f'{nf} filings'))
        db.commit()
        print(zp.name, 'filings', nf, 'activities', na, 'lobbyists', nl, 'errors', err, flush=True)
    print('DONE', flush=True)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
