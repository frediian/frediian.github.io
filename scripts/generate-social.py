#!/usr/bin/env python3
"""Render the six local social cards as share-ready 1080 × 1920 PNGs.

Development only. Install social/requirements.txt outside the checkout, then run
with that installation on PYTHONPATH. The production site uses the generated
images and JSON and does not need Python, Playwright or a rendering service.
"""
from __future__ import annotations

import argparse
import base64
import functools
import hashlib
import html
import json
import re
import struct
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from xml.etree import ElementTree

import qrcode
from playwright.sync_api import sync_playwright

from update_asset_versions import refresh_asset_versions

ROOT = Path(__file__).resolve().parents[1]
KEYS = (
    "web-ventas", "compras-asesoria", "datos-reportes",
    "servidores-redes", "control-seguridad", "monitoreo-ti",
)
ORIGIN = "https://frediian.dev/"
WIDTH, HEIGHT = 1080, 1920
DEFAULT_CHROMIUM = "/workspace/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome"


class LocalAssets(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/__social-renderer":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<!doctype html><html><head><title>Local social renderer</title></head><body></body></html>")
        else:
            super().do_GET()

    def log_message(self, *_args):
        pass


def svg_contents(file: Path, *, logo: bool = False) -> str:
    source = file.read_text(encoding="utf-8")
    tree = ElementTree.fromstring(source)
    for node in tree.iter():
        if node.tag.split("}")[-1] in {"script", "foreignObject"}:
            raise ValueError(f"Unsupported SVG element in {file}")
        if any(key.lower().startswith("on") for key in node.attrib):
            raise ValueError(f"Unexpected SVG event attribute in {file}")
    if logo:
        # Preserve the master vector geometry; remove its tiny second-line slogan.
        source = re.sub(r'<text x="140".*?</text>', "", source, flags=re.S)
        source = re.sub(r'<title>.*?</title>', "", source, flags=re.S)
        source = re.sub(r'viewBox="[^"]*"', 'viewBox="0 0 430 120"', source, count=1)
    return source


def make_qr(url: str) -> tuple[str, int]:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    cells = len(matrix)
    # Integer-sized modules and a four-module white quiet zone avoid resampling.
    size = cells * 6
    modules = "".join(
        f"M{x} {y}h1v1h-1z"
        for y, row in enumerate(matrix) for x, filled in enumerate(row) if filled
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {cells} {cells}" shape-rendering="crispEdges">'
        f'<rect width="{cells}" height="{cells}" fill="white"/>'
        f'<path d="{modules}" fill="#102F46"/></svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode(), size


def render_markup(template: str, record: dict, logo: str, base_url: str) -> str:
    url = ORIGIN + "#servicio-" + record["key"]
    qr, qr_size = make_qr(url)
    parts = {
        "LOGO": logo,
        "ICON": svg_contents(ROOT / "assets/brand/iconos" / (record["icon"] + ".svg")),
        "TITLE": html.escape(record["title"]),
        "HOOK": html.escape(record["hook"]),
        "BENEFIT": html.escape(record["benefit"]),
        "BULLETS": "".join(
            '<li><span class="tick" aria-hidden="true">✓</span><span>'
            + html.escape(text) + "</span></li>" for text in record["bullets"]
        ),
        "NOTE": html.escape(record["note"]),
        "CTA": html.escape(record["cta"]),
        "QR": qr,
        "QR_SIZE": str(qr_size),
    }
    rendered = template.replace("<head>", '<head><base href="' + base_url + '">', 1)
    for token, value in parts.items():
        rendered = rendered.replace("{{" + token + "}}", value)
    if re.search(r"\{\{[A-Z_]+\}\}", rendered):
        raise ValueError("The social template contains an unresolved placeholder")
    return rendered


def caption(record: dict, url: str) -> str:
    return (
        record["hook"] + "\n\n" + record["benefit"] + "\n"
        + "\n".join("• " + point for point in record["bullets"])
        + "\n\n" + record["cta"] + ": " + url
        + "\n\nTecnología que resuelve, tú avanzas."
        + "\nLoja, Ecuador. Atención directa en Loja, Zamora y Yantzaza; "
        + "reuniones agendadas en todo Ecuador."
    )


def validate_page(page, key: str) -> None:
    state = page.evaluate("""() => {
      const bounds = (selector) => [...document.querySelectorAll(selector)].map(e => {
        const r=e.getBoundingClientRect();return {selector,top:r.top,bottom:r.bottom,left:r.left,right:r.right};
      });
      return {
        fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),
        safe:bounds('[data-safe="true"]'),
        story:document.querySelector('.story').getBoundingClientRect().bottom,
        cta:document.querySelector('.cta-panel').getBoundingClientRect().top,
        scrollWidth:document.documentElement.scrollWidth,
        scrollHeight:document.documentElement.scrollHeight,
        images:[...document.images].every(i=>i.complete && i.naturalWidth>0)
      };
    }""")
    if state["scrollWidth"] != WIDTH or state["scrollHeight"] != HEIGHT:
        raise RuntimeError(f"{key}: unexpected page dimensions: {state}")
    if not state["images"] or any(face["status"] != "loaded" for face in state["fonts"]):
        raise RuntimeError(f"{key}: missing fonts or image resources: {state}")
    for box in state["safe"]:
        if box["top"] < 120 or box["bottom"] > 1780 or box["left"] < 70 or box["right"] > 1010:
            raise RuntimeError(f"{key}: text lies outside the social safe area: {box}")
    if state["story"] + 24 > state["cta"]:
        raise RuntimeError(f"{key}: content overlaps the contact panel: {state}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chromium", help="Optional Chromium executable for rendering")
    args = parser.parse_args()
    records = json.loads((ROOT / "social/services.json").read_text())
    if [record["key"] for record in records] != list(KEYS):
        raise ValueError("The editable data must contain the six known service keys in order")
    for record in records:
        if len(record["bullets"]) != 3:
            raise ValueError(f'{record["key"]}: exactly three benefit bullets are required')
    template = (ROOT / "social/template.html").read_text()
    logo = svg_contents(ROOT / "assets/brand/logos/logo-inverso.svg", logo=True)
    out = ROOT / "assets/social"
    out.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(LocalAssets, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    manifest = []
    try:
        with sync_playwright() as playwright:
            executable = args.chromium or (DEFAULT_CHROMIUM if Path(DEFAULT_CHROMIUM).is_file() else None)
            browser = playwright.chromium.launch(**({"executable_path": executable} if executable else {}))
            page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1)
            page.goto(f"http://127.0.0.1:{server.server_port}/__social-renderer")
            errors, failed = [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed.append(request.url))
            for record in records:
                key = record["key"]
                markup = render_markup(template, record, logo, f"http://127.0.0.1:{server.server_port}/")
                page.set_content(markup, wait_until="networkidle")
                page.evaluate("""async () => {
                    await document.fonts.load('800 64px Manrope');
                    await document.fonts.load('650 30px "DM Sans"');
                    await document.fonts.ready;
                }""")
                validate_page(page, key)
                image = out / (key + ".png")
                page.screenshot(path=str(image), type="png", full_page=False, animations="disabled")
                raw = image.read_bytes()
                if struct.unpack(">II", raw[16:24]) != (WIDTH, HEIGHT):
                    raise RuntimeError(f"{key}: incorrect PNG dimensions")
                if errors or failed:
                    raise RuntimeError(f"{key}: browser resource errors: {errors}, {failed}")
                url = ORIGIN + "#servicio-" + key
                manifest.append({
                    "key": key,
                    "title": record["title"],
                    "image": "assets/social/" + key + ".png?v=" + hashlib.sha256(raw).hexdigest()[:10],
                    "filename": "frediian-" + key + ".png",
                    "url": url,
                    "text": caption(record, url),
                    "alt": (
                        "Tarjeta de " + record["title"].lower() + " de frediian. "
                        + record["hook"] + " " + record["benefit"]
                        + " " + "; ".join(record["bullets"]) + ". "
                        + record["note"] + " "
                        + record["cta"] + ". Visita " + url
                    ),
                })
                print(f"Generated {image.relative_to(ROOT)} — {WIDTH}×{HEIGHT}; safe areas and fonts verified", flush=True)
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
    (out / "services.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    refresh_asset_versions(ROOT)
    print(f"Manifest: {len(manifest)} services; image links and asset versions refreshed", flush=True)


if __name__ == "__main__":
    main()
