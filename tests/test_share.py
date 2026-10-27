"""Browser checks for the social-card workflow; all OS sharing is mocked."""
from __future__ import annotations

import functools
import hashlib
import json
import os
import struct
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'assets/social/services.json').read_text())
KEYS = [entry['key'] for entry in MANIFEST]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class SharingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/'
        cls.playwright = sync_playwright().start()
        executable = os.environ.get('CHROMIUM_EXECUTABLE')
        bundled = Path('/workspace/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome')
        if not executable and bundled.exists():
            executable = str(bundled)
        cls.browser = cls.playwright.chromium.launch(**({'executable_path': executable} if executable else {}))

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [])

    def configure(self, mode='none', clipboard=True):
        self.page.add_init_script('''(options => {
          window.testShares = []; window.testClipboard = '';
          Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:async text=>{
            if (!options.clipboard) throw new DOMException('Denied','NotAllowedError');
            window.testClipboard=text;
          }}});
          Object.defineProperty(navigator,'canShare',{configurable:true,value:()=>options.mode==='files'});
          Object.defineProperty(navigator,'share',{configurable:true,value:options.mode==='none'?undefined:async data=>{
            if (window.testFailure) throw new DOMException('Share cancelled',window.testFailure);
            const files=[];
            for (const file of data.files||[]) {
              const digest=await crypto.subtle.digest('SHA-256',await file.arrayBuffer());
              files.push({name:file.name,type:file.type,hash:[...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,'0')).join('')});
            }
            window.testShares.push({title:data.title,text:data.text,url:data.url,files});
          }});
        })(''' + json.dumps({'mode': mode, 'clipboard': clipboard}) + ');')
        self.page.goto(self.url, wait_until='networkidle')

    def open_card(self, key, ready=True):
        trigger = self.page.locator(f'[data-share="{key}"]')
        if not trigger.is_visible():
            self.page.locator('#servicios > summary').click()
        trigger.click()
        self.assertTrue(self.page.locator('#share-dialog').is_visible())
        if ready:
            self.page.wait_for_function('!document.querySelector("#share-preview").hidden')

    def test_all_images_download_exact_files_and_copy_service_links(self):
        self.configure()
        self.assertEqual(self.page.locator('[data-share]').count(), len(MANIFEST))
        for item in MANIFEST:
            with self.subTest(service=item['key']):
                image_path = ROOT / urlsplit(item['image']).path
                raw = image_path.read_bytes()
                self.assertEqual(raw[:8], b'\x89PNG\r\n\x1a\n')
                self.assertEqual(struct.unpack('>II', raw[16:24]), (1080, 1920))
                self.open_card(item['key'])
                self.assertIn(item['title'], self.page.locator('#share-title').inner_text())
                self.assertEqual(self.page.locator('#share-url').input_value(), item['url'])
                self.assertEqual(self.page.locator('#share-preview').evaluate('(e)=>[e.naturalWidth,e.naturalHeight]'), [1080, 1920])
                self.assertFalse(self.page.locator('#share-native').is_visible())
                with self.page.expect_download() as event:
                    self.page.locator('#share-download').click()
                download = event.value
                self.assertEqual(download.suggested_filename, item['filename'])
                self.assertEqual(Path(download.path()).read_bytes(), raw)
                self.page.locator('#share-copy').click()
                self.page.wait_for_function('window.testClipboard.length>0')
                self.assertEqual(self.page.evaluate('window.testClipboard'), item['url'])
                self.page.keyboard.press('Escape')
                self.assertFalse(self.page.locator('#share-dialog').is_visible())
                self.assertTrue(self.page.locator(f'[data-share="{item["key"]}"]').evaluate('(e)=>e===document.activeElement'))
                self.page.evaluate('window.testClipboard=""')

    def test_native_file_sharing_receives_the_actual_png_and_caption(self):
        self.configure(mode='files')
        item = MANIFEST[2]
        self.open_card(item['key'])
        self.assertEqual(self.page.locator('#share-native').inner_text(), 'Compartir imagen')
        self.page.locator('#share-native').click()
        self.page.wait_for_function('window.testShares.length===1')
        shared = self.page.evaluate('window.testShares[0]')
        self.assertEqual(shared['title'], item['title'])
        self.assertEqual(shared['text'], item['text'])
        self.assertIn(item['url'], shared['text'])
        self.assertEqual(shared['files'], [{'name': item['filename'], 'type': 'image/png', 'hash': hashlib.sha256((ROOT / urlsplit(item['image']).path).read_bytes()).hexdigest()}])

    def test_link_only_sharing_and_cancellation_are_honest(self):
        self.configure(mode='link')
        self.open_card(KEYS[0])
        self.assertEqual(self.page.locator('#share-native').inner_text(), 'Compartir enlace')
        self.page.locator('#share-native').click()
        self.page.wait_for_function('window.testShares.length===1')
        shared = self.page.evaluate('window.testShares[0]')
        self.assertEqual(shared['url'], MANIFEST[0]['url'])
        self.assertEqual(shared['files'], [])
        self.page.evaluate('window.testFailure="AbortError"')
        self.page.locator('#share-native').click()
        self.page.wait_for_function('!document.querySelector("#share-native").disabled')
        self.assertEqual(self.page.locator('#share-feedback').inner_text(), '')
        self.page.evaluate('window.testFailure="NotAllowedError"')
        self.page.locator('#share-native').click()
        self.page.wait_for_function('document.querySelector("#share-feedback").textContent.includes("descargar")')
        self.assertTrue(self.page.locator('#share-download').is_visible())

    def test_failed_manifest_can_retry_and_clipboard_failure_keeps_selectable_link(self):
        self.configure(clipboard=False)
        self.page.route('**/assets/social/services.json*', lambda route: route.abort())
        self.open_card(KEYS[1], ready=False)
        self.page.locator('#share-retry').wait_for(state='visible')
        self.page.locator('#share-copy').click()
        self.assertIn('Selecciona y copia', self.page.locator('#share-feedback').inner_text())
        self.assertEqual(self.page.locator('#share-url').evaluate('(e)=>e.selectionEnd-e.selectionStart'), len(MANIFEST[1]['url']))
        self.page.unroute('**/assets/social/services.json*')
        self.page.locator('#share-retry').click()
        self.page.wait_for_function('!document.querySelector("#share-preview").hidden')
        self.assertEqual(self.page.locator('#share-url').input_value(), MANIFEST[1]['url'])

    def test_invalid_image_retries_without_a_broken_file_in_cache(self):
        self.configure(mode='files')
        route_pattern = '**/assets/social/web-ventas.png*'
        self.page.route(route_pattern, lambda route: route.fulfill(status=200, content_type='image/png', body=b'invalid png'))
        self.open_card('web-ventas', ready=False)
        self.page.locator('#share-retry').wait_for(state='visible')
        self.assertFalse(self.page.locator('#share-native').is_visible())
        self.page.unroute(route_pattern)
        self.page.locator('#share-retry').click()
        self.page.wait_for_function('!document.querySelector("#share-preview").hidden')
        self.assertTrue(self.page.locator('#share-native').is_visible())

    def test_brief_specialties_exact_slogan_and_architecture_tabs(self):
        self.configure()
        slogan = 'Tecnología que resuelve. Tú avanzas.'
        self.assertEqual(' '.join(self.page.locator('h1').inner_text().split()), slogan)
        self.assertEqual(self.page.locator('.footer-message>p').inner_text(), slogan)
        self.assertEqual(self.page.title(), 'Frediian | Desarrollo de Software, Arquitectura e IA')
        self.assertEqual(self.page.locator('[data-service-group="primary"]').count(), 6)
        self.assertEqual(self.page.locator('[data-service-group="operations"]').count(), 6)
        self.assertIsNone(self.page.locator('#servicios').get_attribute('open'))
        self.assertEqual(self.page.locator('[data-service-group="primary"]:visible').count(), 6)
        self.assertEqual(self.page.locator('[data-service-group="operations"]:visible').count(), 0)
        self.assertEqual(self.page.locator('.method-steps>li').count(), 4)
        for key in ['software-medida', 'arquitectura-c4', 'ia-mcp', 'agentes-control', 'desarrollo-seguro', 'datos-infraestructura']:
            self.assertEqual(self.page.locator('#servicio-' + key).count(), 1)
        schemas = json.loads(self.page.locator('script[type="application/ld+json"]').text_content())
        self.assertIn('WebSite', [node['@type'] for node in schemas['@graph']])
        self.assertEqual(self.page.locator('link[rel="canonical"]').get_attribute('href'), 'https://frediian.dev/')
        self.page.locator('.architecture-disclosure').first.locator('summary').click()
        self.assertEqual(self.page.locator('[role="tab"]').count(), 3)
        self.page.locator('#c4-tab-context').focus()
        self.page.keyboard.press('End')
        self.assertEqual(self.page.locator('#c4-tab-components').get_attribute('aria-selected'), 'true')
        self.assertTrue(self.page.locator('#c4-panel-components').is_visible())
        self.assertFalse(self.page.locator('#c4-panel-context').is_visible())
        self.page.keyboard.press('ArrowRight')
        self.assertEqual(self.page.locator('#c4-tab-context').get_attribute('aria-selected'), 'true')
        self.page.locator('#c4-tab-containers').click()
        self.assertTrue(self.page.locator('#c4-panel-containers').is_visible())
        self.assertIn('Límite del sistema', self.page.locator('#c4-panel-containers').inner_text())
        self.page.set_viewport_size({'width': 320, 'height': 844})
        self.page.locator('#c4-tab-context').focus()
        self.page.keyboard.press('End')
        tab = self.page.locator('#c4-tab-components').bounding_box()
        bar = self.page.locator('.c4-tabs').bounding_box()
        self.assertLessEqual(tab['x'] + tab['width'], bar['x'] + bar['width'])

    def test_legacy_qr_targets_reveal_their_collapsed_cards(self):
        self.configure()
        self.page.set_viewport_size({'width': 390, 'height': 844})
        for key in ['web-ventas', 'compras-asesoria', 'datos-reportes', 'servidores-redes', 'control-seguridad', 'monitoreo-ti']:
            with self.subTest(service=key):
                self.page.goto(self.url + '#servicio-' + key, wait_until='networkidle')
                self.assertTrue(self.page.locator('#servicios').evaluate('(e)=>e.open'))
                target = self.page.locator('#servicio-' + key)
                self.assertTrue(target.is_visible())
                top = target.bounding_box()['y']
                self.assertGreaterEqual(top, 72)
                self.assertLess(top, 160)
        self.page.goto(self.url, wait_until='networkidle')
        self.page.evaluate('location.hash="servicio-web-ventas"')
        self.page.wait_for_function('document.querySelector("#servicios").open')
        self.assertTrue(self.page.locator('#servicio-web-ventas').is_visible())

    def test_mobile_dialog_keyboard_and_no_javascript_download(self):
        self.configure()
        for width in [320, 390, 650, 768, 1024, 1440]:
            with self.subTest(width=width):
                self.page.set_viewport_size({'width': width, 'height': 844})
                self.open_card(KEYS[4])
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                self.assertLessEqual(self.page.locator('#share-dialog').bounding_box()['width'], width)
                self.page.locator('.share-close').focus()
                self.page.keyboard.press('Shift+Tab')
                self.assertTrue(self.page.evaluate('document.querySelector("#share-dialog").contains(document.activeElement)'))
                self.page.keyboard.press('Escape')
        nojs = self.browser.new_context(java_script_enabled=False, viewport={'width': 320, 'height': 844})
        page = nojs.new_page()
        page.goto(self.url, wait_until='networkidle')
        self.assertFalse(page.locator('#share-dialog').is_visible())
        for item in MANIFEST:
            link = page.locator(f'[data-share="{item["key"]}"]')
            self.assertEqual(link.get_attribute('download'), item['filename'])
            self.assertTrue(link.get_attribute('href').startswith('assets/social/' + item['key'] + '.png'))
        nojs.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
