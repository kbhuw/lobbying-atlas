import re,unicodedata
SUFFIXES={'INC':'corporation','INCORPORATED':'corporation','CORP':'corporation','CORPORATION':'corporation','LLC':'llc','LLP':'llp','LP':'lp','LTD':'limited','LIMITED':'limited','PBC':'pbc','PLC':'plc'}
def normalized(s):
 s=unicodedata.normalize('NFKC',s).upper().replace('&',' AND ')
 s=re.sub(r"[.\u2019']",'',s)
 return ' '.join(re.sub(r'[^\w ]',' ',s).split())
def parts(s):
 n=normalized(s);w=n.split();family=SUFFIXES.get(w[-1]) if w else None
 return (' '.join(w[:-1]) if family and len(w)>1 else n),family
ACRONYMS={'LLC','LLP','LP','PBC','PLC','IBM','AT&T','US','USA','UK','EU','DC','AI','AARP','AFL','CIO','NASA','NRA','NAACP','GM','GE','HP','3M','UPS','USPS','AT','T'}
def display(s):
 return ' '.join(w if w in ACRONYMS or (len(w)<=3 and w.isupper() and w not in {'THE','AND','FOR','OF','INC','CO'}) else w.capitalize() for w in s.split())
