#!/usr/bin/env python3
"""Reject source-only releases and stale HTML/PDF pairs.

After building and exporting the PDF, use --record to record their hashes.
Normal verification never changes artifacts. The source hash covers all source
files, including renderers, content, browser scripts and styles.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ('index.html', 'BLUEPRINT.md', 'completion-manifest.json',
             'System-Design-Atlas-Complete.pdf')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hash():
    digest = hashlib.sha256()
    for path in sorted((ROOT / 'src').rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            digest.update(path.relative_to(ROOT).as_posix().encode() + b'\0')
            digest.update(path.read_bytes() + b'\0')
    return digest.hexdigest()


def check_pdf(manifest):
    """Read the actual export, independently of HTML/manifest counts."""
    pdf = ROOT / ARTIFACTS[-1]
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
    assert re.search(r'Tagged:\s+yes', info), 'PDF must be tagged'
    pages = int(re.search(r'Pages:\s+(\d+)', info)[1])
    extracted = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
    normalized = ' '.join(extracted.split())
    assert 'Source edition: ' + source_hash() in normalized, (
        'PDF source edition is stale. Rebuild HTML and export the PDF before recording a release.')
    missing = []
    for unit in manifest['units']:
        for chapter in unit['chapters']:
            title = ' '.join(chapter['title'].split())
            if title not in normalized:
                missing.append(chapter['id'])
            for i, section in enumerate(chapter.get('sections', []), 1):
                heading = chapter['number'] + '.' + str(i) + ' · ' + section
                if ' '.join(heading.split()) not in normalized:
                    missing.append(f'{chapter["id"]}-section-{i}')
    for figure in manifest['figures']:
        if not re.search(r'FIG\.\s*' + re.escape(figure['number']) + r'(?![\d.])', normalized):
            missing.append(figure['id'])
    assert not missing, f'PDF is missing chapter/figure labels: {missing}'
    return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'completion-manifest.json').read_text())
    assert 'Source edition: ' + source_hash() in (ROOT / 'index.html').read_text(), (
        'HTML source edition is stale. Run build.py before recording a release.')
    current = dict(schema=1, source_sha256=source_hash(),
                   artifacts={name: sha(ROOT / name) for name in ARTIFACTS},
                   pdf_pages=check_pdf(manifest))
    record = ROOT / 'release.json'
    if args.record:
        record.write_text(json.dumps(current, indent=2) + '\n')
        print(f'Recorded HTML/PDF release: {current["pdf_pages"]} tagged pages.')
    else:
        assert record.exists(), 'No release record. Build, export PDF, then run --record.'
        expected = json.loads(record.read_text())
        assert current == expected, ('Release artifacts are stale. Build the HTML, export the PDF, '
                                     'then run verify_release.py --record and commit all artifacts.')
        print(f'Release hashes and PDF contents match: {current["pdf_pages"]} tagged pages.')


if __name__ == '__main__':
    main()
