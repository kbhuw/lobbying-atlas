"""Convert saved public HTML to readable text for Jev; keep originals intact."""
from html.parser import HTMLParser
from pathlib import Path
import sys

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        source = Path(filename)
        parser = TextParser()
        parser.feed(source.read_text(errors='replace'))
        output = source.with_suffix('.txt')
        output.write_text('\n'.join(parser.parts) + '\n')
        print(output)
