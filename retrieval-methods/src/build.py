#!/usr/bin/env python3
"""Build one network-independent HTML file, using only Python's standard library."""
import json
from pathlib import Path
from content import DATA
from teaching import attach

attach(DATA)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'index.html'
template = (HERE / 'template.html').read_text()
payload = json.dumps(DATA, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = template.replace('/*__CSS__*/', (HERE / 'style.css').read_text())
html = html.replace('__DATA__', payload).replace('/*__JS__*/', (HERE / 'app.js').read_text())
assert all(token not in html for token in ('/*__CSS__*/', '__DATA__', '/*__JS__*/'))
OUT.write_text(html)
print(f'Built {OUT}: {len(DATA["categories"])} method families + evaluation, '
      f'{sum(len(c["methods"]) for c in DATA["categories"])} notes, '
      f'{len(DATA["sources"])} references, {len(html):,} characters')
