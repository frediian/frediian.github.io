#!/usr/bin/env python3
"""Build static service-card fragments and social input from one editable catalog.

The fragments can be inserted into the primary and operations service grids.
This command does not change index.html or contact settings.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICON_IDS = {
    'desarrollo': 'i-code', 'consultoria': 'i-grid', 'datos': 'i-chart',
    'infraestructura': 'i-server', 'seguridad': 'i-shield',
    'automatizacion': 'i-automation', 'monitoreo': 'i-pulse', 'ecommerce': 'i-grid',
}
SOCIAL_FIELDS = ('key','title','hook','benefit','bullets','cta','icon','note')


def read_services(root=ROOT):
    records = json.loads((root/'content/services.json').read_text())
    if not isinstance(records, list) or not records:
        raise ValueError('The service catalog must be a nonempty array')
    seen=set()
    for item in records:
        key=item['key']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',key) or key in seen:
            raise ValueError('Every service needs a unique safe key')
        seen.add(key)
        if item['group'] not in ('primary','operations') or item['icon'] not in ICON_IDS:
            raise ValueError(f'{key}: unsupported group or icon')
        if not 1 <= len(item['tags']) <= 3 or len(item['bullets']) != 3 or not item['details']:
            raise ValueError(f'{key}: check tags, benefit bullets and details')
        for field in ('title','summary','hook','benefit','cta','note'):
            if not isinstance(item[field],str) or not item[field].strip():
                raise ValueError(f'{key}: missing {field}')
        for field in ('tags','bullets','details'):
            if any(not isinstance(text,str) or not text.strip() for text in item[field]):
                raise ValueError(f'{key}: empty {field} item')
    return records


def card_markup(item, ordinal, root=ROOT):
    escape=lambda text: html.escape(text,quote=True)
    key=item['key']
    image='assets/social/'+key+'.png'
    path=root/image
    if path.is_file():image+='?v='+hashlib.sha256(path.read_bytes()).hexdigest()[:10]
    tags=''.join('<span>'+escape(tag)+'</span>' for tag in item['tags'])
    details=''.join('<li>'+escape(text)+'</li>' for text in item['details'])
    return (
        f'<article class="service-card" id="servicio-{key}" data-service-group="{item["group"]}">'
        f'<div class="card-top"><svg class="service-icon" aria-hidden="true"><use href="#{ICON_IDS[item["icon"]]}"/></svg><span>{ordinal:02}</span></div>'
        f'<h3>{escape(item["title"])}</h3><p>{escape(item["summary"])}</p>'
        f'<div class="service-tags">{tags}</div>'
        f'<details class="service-details"><summary>Qué incluye <span aria-hidden="true">+</span></summary><ul>{details}</ul></details>'
        f'<a class="service-share" href="{image}" download="frediian-{key}.png" data-share="{key}" aria-label="Compartir imagen de {escape(item["title"])}"><svg class="icon" aria-hidden="true"><use href="#i-share"/></svg>Compartir</a></article>'
    )


def build_services(root=ROOT):
    records=read_services(root)
    for group in ('primary','operations'):
        cards=[card_markup(item,index+1,root) for index,item in enumerate(record for record in records if record['group']==group)]
        (root/'content'/('generated-'+group+'.html')).write_text('\n'.join(cards)+'\n')
    social=[{field:record[field] for field in SOCIAL_FIELDS} for record in records]
    (root/'social/services.json').write_text(json.dumps(social,ensure_ascii=False,indent=2)+'\n')
    return records


if __name__=='__main__':
    records=build_services()
    print(f'Built {len(records)} service cards in two fragments and derived social/services.json')
