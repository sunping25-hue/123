"""GoatCounter scope, failure handling and footer integration checks.

Run: python -m unittest discover -s tests -p test_goatcounter.py -v
Browser checks mock third-party requests; they do not send real statistics.
"""
import asyncio
import functools
import http.server
import json
import re
import subprocess
import threading
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "shinox-v2-site"
BASE = "84c2890364405673468d2f28f2d3f2b8f781daad"
TOTAL = "https://shinox.goatcounter.com/counter/TOTAL.json"
TRACKER = '<script data-goatcounter="https://shinox.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
WRAPPER = re.compile(r'<small id="visit-count-wrap"[^>]*>.*?<span id="visit-count"></span></small>')
SHARED = re.compile(r'<script defer src="(?:\.\./)*assets/js/visit-count\.js"></script>')


class MarkupTests(unittest.TestCase):
    def test_every_site_page_and_original_content(self):
        pages = list(SITE.rglob("*.html"))
        self.assertEqual(len(pages), 59)
        for page in pages:
            with self.subTest(page=page.relative_to(SITE)):
                text = page.read_text()
                self.assertEqual(text.count(TRACKER), 1)
                self.assertEqual(text.count('id="visit-count-wrap"'), 1)
                self.assertEqual(text.count('id="visit-count"'), 1)
                wrapper = WRAPPER.search(text)
                self.assertIsNotNone(wrapper)
                self.assertIn(" hidden ", wrapper.group())
                self.assertIn("display:none", wrapper.group())
                self.assertTrue(text.index(wrapper.group()) < text.index("</footer>"))
                self.assertTrue(text.index(TRACKER) < text.lower().index("</body>"))
                script = SHARED.search(text)
                self.assertIsNotNone(script)
                src = re.search(r'src="([^"]+)"', script.group())[1]
                self.assertEqual((page.parent / src).resolve(), SITE / "assets/js/visit-count.js")
                original = subprocess.check_output(["git", "show", f"{BASE}:{page.relative_to(ROOT)}"], cwd=ROOT).decode()
                restored = WRAPPER.sub("", SHARED.sub("", text.replace(TRACKER, "")))
                self.assertEqual(restored, original)

    def test_legacy_site_and_redirect_untouched(self):
        for name in ("index.html", "counters_with_icons_horizontal.html"):
            original = subprocess.check_output(["git", "show", f"{BASE}:{name}"], cwd=ROOT)
            self.assertEqual((ROOT / name).read_bytes(), original)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class BrowserTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        from playwright.async_api import async_playwright
        handler = functools.partial(QuietHandler, directory=str(SITE))
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.origin = f"http://127.0.0.1:{self.server.server_port}"
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])

    async def asyncTearDown(self):
        await self.browser.close()
        await self.playwright.stop()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    async def page_with_counter(self, payload=None, status=200, body=None, network_failure=False):
        page = await self.browser.new_page()
        hits = []
        async def handle(route):
            if route.request.url == TOTAL:
                hits.append(route.request.url)
                if network_failure:
                    await route.abort()
                else:
                    await route.fulfill(status=status, content_type="application/json", body=body if body is not None else json.dumps(payload))
            elif route.request.url.startswith(self.origin):
                await route.continue_()
            else:
                # Never contact GoatCounter tracking or other third parties in QA.
                await route.abort()
        await page.route("**/*", handle)
        return page, hits

    async def test_bilingual_and_nested_footer_success(self):
        for route, english in [("index.html", False), ("en/index.html", True), ("products/self-3.html", False), ("en/products/wash-2.html", True), ("privacy/index.html", False), ("en/terms/index.html", True), ("404.html", False), ("admin.html", False)]:
            with self.subTest(route=route):
                page, hits = await self.page_with_counter({"count": "1,234"})
                await page.goto(self.origin + "/" + route, wait_until="domcontentloaded")
                await page.locator("#visit-count-wrap").wait_for(state="visible")
                self.assertEqual(await page.locator("#visit-count").text_content(), "1,234")
                self.assertEqual(await page.locator("#visit-count-wrap").text_content(), ("Total visits: " if english else "累計瀏覽人次：") + "1,234")
                self.assertEqual(await page.locator("footer #visit-count-wrap").count(), 1)
                self.assertEqual(hits, [TOTAL])
                await page.close()

    async def test_failures_hide_entire_counter(self):
        cases = [dict(payload={"count": "4,567"}, status=500), dict(body="invalid JSON"), dict(payload={}), dict(payload={"count": None}), dict(payload={"count": -1}), dict(payload={"count": "NaN"}), dict(payload={"count": "<img>"}), dict(network_failure=True)]
        for case in cases:
            with self.subTest(case=case):
                page, hits = await self.page_with_counter(**case)
                await page.goto(self.origin + "/en/products/self-1.html", wait_until="networkidle")
                self.assertEqual(hits, [TOTAL])
                self.assertFalse(await page.locator("#visit-count-wrap").is_visible())
                self.assertEqual(await page.locator("#visit-count").text_content(), "")
                self.assertNotIn("0", await page.locator("#visit-count-wrap").text_content())
                await page.close()

    async def test_late_footer_replacement_and_duplicate_script(self):
        page, hits = await self.page_with_counter({"count": 9876})
        await page.goto(self.origin + "/en/404.html", wait_until="networkidle")
        await page.evaluate("document.querySelector('footer').remove()")
        await page.evaluate("const f=document.createElement('footer');f.innerHTML='<p>© ShinoX Car Wash Systems</p>';document.body.append(f)")
        await page.locator("footer #visit-count-wrap").wait_for(state="visible")
        await page.add_script_tag(url=self.origin + "/assets/js/visit-count.js")
        await page.evaluate("const f=document.querySelector('footer');const next=document.createElement('footer');next.innerHTML='<p>© ShinoX Car Wash Systems</p>';f.replaceWith(next)")
        await page.locator("footer #visit-count-wrap").wait_for(state="visible")
        self.assertEqual(await page.locator("#visit-count-wrap").count(), 1)
        self.assertEqual(await page.locator("#visit-count-wrap").text_content(), "Total visits: 9876")
        self.assertEqual(hits, [TOTAL])
        await page.close()


if __name__ == "__main__":
    unittest.main()
