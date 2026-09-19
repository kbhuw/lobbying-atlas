"""Rank official-page asset candidates; visual review is still required."""
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit

GENERIC = {'national', 'american', 'international', 'association', 'council',
           'company', 'corporation', 'foundation', 'organization', 'group',
           'www', 'com', 'org', 'net', 'the', 'for', 'and', 'inc'}


class Page(HTMLParser):
    def __init__(self, name, url=''):
        super().__init__()
        tokens = re.findall('[a-z0-9]+', name.lower())
        host = (urlsplit(url).hostname or '').split('.')
        self.name_tokens = {t for t in tokens + host if len(t) > 2 and t not in GENERIC}
        self.full_name = ' '.join(tokens)
        self.candidates, self.text, self.ld = [], [], []
        self.skip, self.jsonld = 0, False
        self.stack = []
        self.order = 0

    def handle_starttag(self, tag, attrs):
        a = {k: v or '' for k, v in attrs}
        if tag in ('script', 'style'):
            self.skip += 1
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.jsonld = True
        ancestry = ' '.join(self.stack).lower()
        if tag == 'img':
            asset = a.get('data-src') or a.get('src', '')
            desc = ' '.join(a.get(k, '') for k in ('alt', 'class', 'id', 'src', 'data-src')).lower()
            alt = ' '.join(re.findall('[a-z0-9]+', a.get('alt', '').lower()))
            social = re.search(r'\b(facebook|instagram|tiktok|twitter|bluesky|vimeo|flickr|youtube|linkedin)\b', alt)
            named_brand = alt == self.full_name and bool(alt)
            if asset and not asset.startswith('data:') and not social and ('logo' in desc or named_brand):
                self.order += 1
                score = 100
                if named_brand:
                    score -= 40
                identity = (a.get('alt', '') + ' ' + urlsplit(asset).path.rsplit('/', 1)[-1]).lower()
                if any(t in identity for t in self.name_tokens):
                    score -= 40
                if any(t in ancestry for t in ('header', 'navbar', 'site-brand', 'site-logo')):
                    score -= 30
                if any(t in desc for t in ('logo-main', 'main-logo', 'logofooter', 'logoimage', 'logo-white')):
                    score -= 10
                if any(t in ancestry + ' ' + desc for t in ('sponsor', 'partner-logo', '/members/', 'charity-navigator', 'award', 'equal-housing')):
                    score += 100
                # Preserve page order for ties instead of alphabetizing asset URLs.
                self.candidates.append((score + self.order / 10000, asset.strip(), 'logo'))
        if tag == 'link' and 'icon' in a.get('rel', '').lower() and a.get('href'):
            self.order += 1
            self.candidates.append((300 + self.order / 10000, a['href'].strip(), 'site_icon'))
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.stack.append(tag + ' ' + a.get('class', '') + ' ' + a.get('id', ''))

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
        if tag == 'script':
            self.jsonld = False
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].split(' ', 1)[0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.jsonld:
            self.ld.append(data)
        if not self.skip and data.strip():
            self.text.append(data.strip())
