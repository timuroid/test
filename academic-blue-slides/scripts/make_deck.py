#!/usr/bin/env python3
"""Create a self-contained HTML starter for the academic blue slide system."""
from __future__ import annotations

import argparse
import base64
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assets = Path(__file__).resolve().parents[1] / 'assets'
    html = (assets / 'starter.html').read_text(encoding='utf-8')
    resources = {
        'FONT_REGULAR': 'fonts/Inter-Regular.ttf',
        'FONT_BOLD': 'fonts/Inter-Bold.ttf',
        'CREST_WHITE': 'crest-white-watermark.png',
    }
    for token, name in resources.items():
        marker = '{{' + token + '}}'
        if marker not in html:
            raise SystemExit(f'Missing resource marker: {marker}')
        html = html.replace(marker, base64.b64encode((assets / name).read_bytes()).decode('ascii'))
    license_text = (assets / 'fonts/OFL.txt').read_text(encoding='utf-8')
    html = html.replace('{{FONT_LICENSE}}', license_text.replace('--', '—'))
    output = args.output.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output.open('x', encoding='utf-8') as handle:
            handle.write(html)
    except FileExistsError:
        raise SystemExit(f'File already exists; choose a new output path: {output}')
    print(output.resolve())


if __name__ == '__main__':
    main()
