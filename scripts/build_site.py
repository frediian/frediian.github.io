#!/usr/bin/env python3
"""Compose the static service and architecture sections from their editable sources."""
from pathlib import Path
import re

from build_services import build_services
from update_asset_versions import refresh_asset_versions

ROOT = Path(__file__).resolve().parents[1]


def build_site(root=ROOT):
    build_services(root)
    page = root / 'index.html'
    markup = page.read_text()
    for marker, fragment in [
        ('PRIMARY_SERVICES', 'content/generated-primary.html'),
        ('OPERATIONS_SERVICES', 'content/generated-operations.html'),
        ('ARCHITECTURE', 'content/architecture.html'),
    ]:
        pattern = r'(<!-- ' + marker + r'_START -->).*?(<!-- ' + marker + r'_END -->)'
        replacement = (root / fragment).read_text().strip()
        markup, count = re.subn(pattern, lambda match: match.group(1) + '\n' + replacement + '\n' + match.group(2), markup, flags=re.S)
        if count != 1:
            raise ValueError(f'Missing or duplicate {marker} build markers')
    page.write_text(markup)
    refresh_asset_versions(root)


if __name__ == '__main__':
    build_site()
    print('Built 12 specialties and architecture module; static asset versions refreshed')
