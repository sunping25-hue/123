"""Public crawl coverage and noindex exceptions, without rewriting page content."""
from html.parser import HTMLParser
from pathlib import Path
import http.client
import sys
import tempfile
import threading
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_indexing import SITE, ORIGIN, source_pages, public_pages, outputs, indexable_html, ROBOTS_META
from server import PreviewServer, RequestStore


class Meta(HTMLParser):
    def __init__(self):super().__init__();self.robots=[]
    def handle_starttag(self, tag, attrs):
        values=dict(attrs)
        if tag=='meta' and values.get('name')=='robots':self.robots.append(values.get('content',''))


class IndexingTests(unittest.TestCase):
    def test_formal_language_pairs_are_indexable_and_exceptions_stay_noindex(self):
        self.assertGreaterEqual(len(source_pages()), 22)
        self.assertEqual(len(public_pages()), 2*len(source_pages()))
        for path in public_pages():
            with self.subTest(path=path):
                document=Meta();document.feed((SITE/path).read_text())
                self.assertEqual(document.robots, ['index,follow,max-image-preview:large'])
        for prefix in ['', 'en/']:
            for path in ['404.html','privacy.html','terms.html','privacy/index.html','terms/index.html']:
                document=Meta();document.feed((SITE/(prefix+path)).read_text());self.assertIn('noindex', document.robots[0])
        document=Meta();document.feed((SITE/'admin.html').read_text());self.assertIn('noindex',document.robots[0])

    def test_sitemap_exact_coverage_reciprocal_languages_and_existing_canonical_paths(self):
        ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
        urls=ET.parse(SITE/'sitemap.xml').getroot().findall('s:url',ns)
        self.assertEqual({n.find('s:loc',ns).text for n in urls}, {ORIGIN+'/'+path for path in public_pages()})
        self.assertEqual(len(urls),len(public_pages()))
        for node in urls:
            self.assertEqual(node.find('s:lastmod',ns).text,'2026-10-29')
            self.assertEqual(len(node.findall('x:link',ns)),3)
            for link in node.findall('x:link',ns):self.assertIn(link.get('href'),{ORIGIN+'/'+path for path in public_pages()})

    def test_build_is_idempotent_and_metadata_edit_preserves_all_other_bytes(self):
        for path, expected in outputs().items():self.assertEqual(path.read_text(),expected,path)
        source='<html><head><meta content="noindex,nofollow" name="robots"><title>原標題</title></head><body>原文<img src="original.webp"></body></html>'
        actual=indexable_html(source)
        self.assertEqual(ROBOTS_META.sub('',source),ROBOTS_META.sub('',actual))
        self.assertEqual(indexable_html(actual),actual)
        without_robots=ROBOTS_META.sub('',source)
        self.assertEqual(ROBOTS_META.sub('',indexable_html(without_robots)),without_robots)

    def test_robots_advertises_sitemap_without_blocking_public_content(self):
        text=(SITE/'robots.txt').read_text()
        self.assertEqual(text.count('Sitemap: '+ORIGIN+'/sitemap.xml'),1)
        self.assertIn('Allow: /',text)
        self.assertNotIn('Disallow: /\n',text)
        self.assertIn('Disallow: /api/',text)

    def test_http_public_pages_and_crawl_files_have_no_noindex_header(self):
        with tempfile.TemporaryDirectory() as directory:
            store=RequestStore(Path(directory)/'requests.sqlite3')
            server=PreviewServer(('127.0.0.1',0),store,SITE)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                for path in public_pages()+['robots.txt','sitemap.xml']:
                    connection=http.client.HTTPConnection('127.0.0.1',server.server_port)
                    connection.request('HEAD','/'+path);response=connection.getresponse();response.read()
                    self.assertEqual(response.status,200,path)
                    self.assertNotIn('noindex',response.getheader('X-Robots-Tag',''),path)
                    connection.close()
            finally:server.shutdown();server.server_close()


if __name__=='__main__':unittest.main()
