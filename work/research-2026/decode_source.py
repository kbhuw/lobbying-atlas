"""Decode source HTML using its declared charset before UTF-8 fallback."""
import re

def decode_html(raw, headers=None):
    declared = headers.get_content_charset() if headers is not None else None
    match = re.search(br"charset\s*=\s*[\"\']?([a-zA-Z0-9._-]+)", raw[:8192], re.I)
    candidates = [declared, match.group(1).decode("ascii") if match else None, "utf-8"]
    for charset in candidates:
        if not charset:
            continue
        try:
            return raw.decode(charset)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("utf-8", errors="replace")
