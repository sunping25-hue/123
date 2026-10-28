#!/usr/bin/env python3
"""Generate English pages from the current Traditional Chinese design master.
Edit Chinese templates + locales/en.json, then run this script. --check detects drift.
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import argparse,json,posixpath,re,sys
from urllib.parse import urlsplit,urlunsplit
ROOT=Path(__file__).resolve().parents[1]/'shinox-v2-site'
DICT=json.loads((ROOT/'locales/en.json').read_text())
CJK=re.compile('[\u3400-\u9fff]');missing=set()
def tr(value):
 if not isinstance(value,str) or not CJK.search(value):return value
 key=value.strip()
 if key not in DICT:missing.add(key);return value
 return value[:len(value)-len(value.lstrip())]+DICT[key]+value[len(value.rstrip()):]
def relative(path,parent):return posixpath.relpath(path,parent or '.')
def route(value,source,target,asset=False):
 u=urlsplit(value)
 if u.scheme or u.netloc or value.startswith(('#','data:','javascript:')):return value
 if not u.path:return value
 normalized=posixpath.normpath(posixpath.join(posixpath.dirname(source),u.path)) if not u.path.startswith('/') else u.path.lstrip('/')
 if normalized.startswith('../'):raise ValueError('Path leaves site root: '+source+' '+value)
 if not asset:
  if normalized.startswith('en/'):normalized=source
  elif normalized.endswith('.html'):normalized='en/'+normalized
 path=relative(normalized,posixpath.dirname(target))
 return urlunsplit(('','',path,u.query,u.fragment))
def json_translate(v):
 if isinstance(v,str):return tr(v)
 if isinstance(v,list):return [json_translate(x) for x in v]
 if isinstance(v,dict):return {k:json_translate(x) for k,x in v.items()}
 return v
sources=sorted(ROOT.glob('*.html'))+sorted((ROOT/'products').glob('*.html'))
outputs={};manifest=[]
for path in sources:
 source=path.relative_to(ROOT).as_posix();target='en/'+source;soup=BeautifulSoup(path.read_text(),'html.parser');soup.html['lang']='en'
 # Keep source form option values stable while translating the visible choices.
 for option in soup.select('option'):
  if not option.has_attr('value'):option['value']=option.get_text()
 for tag in soup.find_all(True):
  if tag.name=='script' and tag.get('type')=='application/ld+json':
   try:tag.string=json.dumps(json_translate(json.loads(tag.string)),ensure_ascii=False,separators=(',',':'))
   except json.JSONDecodeError:pass
  for attr in ['alt','title','aria-label','placeholder','data-calculator-title','content']:
   if isinstance(tag.get(attr),str):tag[attr]=tr(tag[attr])
  if tag.name=='input' and isinstance(tag.get('value'),str):tag['value']=tr(tag['value'])
  for attr in ['src','poster','data-element-src','data-contact-src']:
   if tag.has_attr(attr):tag[attr]=route(tag[attr],source,target,asset=True)
  if tag.has_attr('href'):
   is_asset=tag.name=='link' and tag.get('rel')!=['alternate']
   tag['href']=route(tag['href'],source,target,asset=is_asset)
  if tag.has_attr('style'):
   tag['style']=re.sub(r"url\((['\"]?)(.*?)\1\)",lambda m:"url('"+route(m[2],source,target,asset=True)+"')",tag['style'])
 for text in list(soup.find_all(string=True)):
  if text.parent.name in ['script','style']:continue
  translated=tr(str(text))
  if translated!=str(text):text.replace_with(NavigableString(translated))
 # Corresponding-page language links, not a link back to the other homepage.
 for group in soup.select('.language-switch'):
  for a in group.select('a[lang]'):
   if a['lang'].startswith('zh'):
    a['href']=relative(source,posixpath.dirname(target));a.attrs.pop('aria-current',None);a['aria-label']='View this page in Traditional Chinese';a['data-locale-link']='zh-Hant';a.string='繁中'
   else:
    a['href']=relative(target,posixpath.dirname(target));a['aria-current']='page';a['aria-label']='English, current language';a.string='EN'
 for a in soup.select('a[lang="en"]'):
  if a.find_parent(class_='language-switch'):continue
  a['href']=relative(source,posixpath.dirname(target));a['lang']='zh-Hant';a['hreflang']='zh-Hant';a['aria-label']='View this page in Traditional Chinese';a['data-locale-link']='zh-Hant';a.string='繁中'
 for meta in soup.select('meta[property="og:locale"]'):meta['content']='en_US'
 for alternate in soup.select('link[rel="alternate"][hreflang]'):alternate.decompose()
 for locale,dest in [('zh-Hant',source),('en',target),('x-default',source)]:soup.head.append(soup.new_tag('link',rel='alternate',hreflang=locale,href=relative(dest,posixpath.dirname(target))))
 memory=soup.new_tag('script',src=relative('locales/en.js',posixpath.dirname(target)));memory['defer']='';soup.head.insert(0,memory)
 outputs[ROOT/target]=str(soup)+'\n';manifest.append({'zh':source,'en':target})
outputs[ROOT/'locales/en.js']='/* Generated from en.json by scripts/build_english.py. */\nwindow.SHINOX_EN='+json.dumps(DICT,ensure_ascii=False,separators=(',',':'))+';\n'
outputs[ROOT/'locales/pages.json']=json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'
if missing:print('Missing English translations:\n'+json.dumps(sorted(missing),ensure_ascii=False,indent=2));sys.exit(1)
parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();changed=[]
for dest,content in outputs.items():
 if not dest.exists() or dest.read_text()!=content:
  changed.append(str(dest.relative_to(ROOT)))
  if not args.check:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(content)
if args.check and changed:print('Regenerate English pages: python scripts/build_english.py\n'+json.dumps(changed,indent=2));sys.exit(1)
print(('Checked' if args.check else 'Generated')+' '+str(len(manifest))+' English pages from the Chinese master; '+str(len(changed))+' files '+('differ' if args.check else 'updated')+'.')
