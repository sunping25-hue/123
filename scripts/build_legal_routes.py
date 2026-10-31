#!/usr/bin/env python3
"""Generate clean legal routes while retaining the original .html entry points."""
import argparse,posixpath,re
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
from bs4 import BeautifulSoup
parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
root=Path(__file__).resolve().parents[1]/'shinox-v2-site';changed=[]
for lang in ['', 'en/']:
 for slug in ['privacy','terms']:
  source=lang+slug+'.html';target=lang+slug+'/index.html';soup=BeautifulSoup((root/source).read_text(),'html.parser')
  def route(value):
   u=urlsplit(value)
   if u.scheme or u.netloc or value.startswith(('#','data:','/')) or not u.path:return value
   resolved=posixpath.normpath(posixpath.join(posixpath.dirname(source),u.path));path=posixpath.relpath(resolved,posixpath.dirname(target))
   return urlunsplit(('','',path,u.query,u.fragment))
  for tag in soup.find_all(True):
   for attr in ['href','src','poster']:
    if tag.has_attr(attr):tag[attr]=route(tag[attr])
   if tag.has_attr('style'):tag['style']=re.sub(r"url\((['\"]?)(.*?)\1\)",lambda m:"url('"+route(m[2])+"')",tag['style'])
  content=str(soup).rstrip()+'\n';p=root/target
  if not p.exists() or p.read_text()!=content:
   changed.append(target)
   if not args.check:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
if args.check and changed:raise SystemExit('Regenerate legal routes: '+', '.join(changed))
print('Legal routes checked.' if args.check else 'Legal routes generated.')
