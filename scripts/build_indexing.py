#!/usr/bin/env python3
"""Only update robots metadata and crawl files; preserve every other HTML byte."""
import argparse
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'shinox-v2-site'
ORIGIN = 'https://www.shinox-wash.com'
UPDATED = '2026-10-29'
EXCLUDED = {'404.html', 'admin.html', 'privacy.html', 'terms.html'}
ROBOTS_META = re.compile(r'<meta\b(?=[^>]*\bname\s*=\s*[\'\"]robots[\'\"])[^>]*>', re.I)
CONTENT = re.compile(r'(\bcontent\s*=\s*)([\'\"])(.*?)\2', re.I | re.S)
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XHTML_NS = 'http://www.w3.org/1999/xhtml'


def source_pages():
    return sorted(p.name for p in SITE.glob('*.html') if p.name not in EXCLUDED) + sorted(p.relative_to(SITE).as_posix() for p in (SITE/'products').glob('*.html'))


def public_pages():
    return [prefix+source for source in source_pages() for prefix in ['', 'en/']]


def indexable_html(text):
    matches = list(ROBOTS_META.finditer(text))
    if not matches:
        # Newly added formal pages may omit robots (indexable by default).
        # Add the explicit policy without serializing or changing their contents.
        head = re.search(r'<head\b[^>]*>', text, re.I)
        if not head:
            raise ValueError('Expected a head element')
        return text[:head.end()]+'<meta name="robots" content="index,follow,max-image-preview:large">'+text[head.end():]
    if len(matches) != 1:
        raise ValueError('Expected exactly one robots meta element')
    tag = matches[0].group()
    replacement, count = CONTENT.subn(lambda m: m[1]+m[2]+'index,follow,max-image-preview:large'+m[2], tag)
    if count != 1:
        raise ValueError('Expected one robots content attribute')
    return text[:matches[0].start()]+replacement+text[matches[0].end():]


def outputs():
    result = {}
    ET.register_namespace('', SITEMAP_NS);ET.register_namespace('xhtml', XHTML_NS)
    root = ET.Element('{'+SITEMAP_NS+'}urlset')
    for source in source_pages():
        for prefix in ['', 'en/']:
            path = prefix+source
            file = SITE/path
            if not file.is_file():
                raise ValueError('Missing corresponding page: '+path)
            result[file] = indexable_html(file.read_text())
            entry = ET.SubElement(root, '{'+SITEMAP_NS+'}url')
            ET.SubElement(entry, '{'+SITEMAP_NS+'}loc').text = ORIGIN+'/'+path
            ET.SubElement(entry, '{'+SITEMAP_NS+'}lastmod').text = UPDATED
            for language, target in [('zh-Hant', source), ('en', 'en/'+source), ('x-default', source)]:
                ET.SubElement(entry, '{'+XHTML_NS+'}link', {'rel':'alternate', 'hreflang':language, 'href':ORIGIN+'/'+target})
    ET.indent(root, space='  ')
    result[SITE/'sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root, encoding='unicode')+'\n'
    result[SITE/'robots.txt'] = 'User-agent: *\nAllow: /\nDisallow: /404.html\nDisallow: /en/404.html\nDisallow: /admin.html\nDisallow: /api/\n\nSitemap: '+ORIGIN+'/sitemap.xml\n'
    return result


def main():
    parser = argparse.ArgumentParser();parser.add_argument('--check', action='store_true');args = parser.parse_args()
    changed = []
    for path, text in outputs().items():
        if path.read_text() != text:
            changed.append(path.relative_to(ROOT).as_posix())
            if not args.check:path.write_text(text)
    if args.check and changed:raise SystemExit('Regenerate indexing: '+', '.join(changed))
    print(('Checked' if args.check else 'Updated'), len(public_pages()), 'formal bilingual pages;', len(changed), 'files differ' if args.check else 'files changed')


if __name__ == '__main__':main()
