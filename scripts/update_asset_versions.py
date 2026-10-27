#!/usr/bin/env python3
"""Refresh first-party asset versions and no-JS social-image download links."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def refresh_asset_versions(root=ROOT):
    page = root / 'index.html'
    source = page.read_text()
    for asset in ['assets/styles.css', 'assets/app.js', 'assets/share.js', 'assets/architecture.js', 'assets/architecture.css', 'assets/brand/tokens.css', 'assets/favicon.svg', 'assets/social/services.json']:
        path = root / asset
        if not path.exists():
            continue
        version = hashlib.sha256(path.read_bytes()).hexdigest()[:10]
        source = re.sub(re.escape(asset) + r'(?:\?v=[a-f0-9]+)?', asset + '?v=' + version, source)
    manifest = root / 'assets/social/services.json'
    if manifest.exists():
        for item in json.loads(manifest.read_text()):
            asset = 'assets/social/' + item['key'] + '.png'
            source = re.sub(re.escape(asset) + r'(?:\?v=[a-f0-9]+)?', item['image'], source)
    page.write_text(source)


if __name__ == '__main__':
    refresh_asset_versions()
