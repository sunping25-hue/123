from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import posixpath,json
root=Path(__file__).resolve().parents[1]/'shinox-v2-site';pairs=json.loads((root/'locales/pages.json').read_text());errors=[]
for pair in pairs:
 z=BeautifulSoup((root/pair['zh']).read_text(),'html.parser');e=BeautifulSoup((root/pair['en']).read_text(),'html.parser')
 def structure(s):return [(n.name,n.get('class'),n.get('id')) for n in s.body.find_all(True)]
 assert structure(z)==structure(e),pair
 for file,soup in [(pair['zh'],z),(pair['en'],e)]:
  for tag in soup.select('[src],[poster],[href],[data-element-src],[data-contact-src]'):
   for attr in ['src','poster','href','data-element-src','data-contact-src']:
    v=tag.get(attr)
    if not v:continue
    u=urlsplit(v)
    if u.scheme or u.netloc:continue
    if not u.path:target=file
    else:target=unquote(u.path).lstrip('/') if u.path.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(file),unquote(u.path)))
    dest=root/target
    if not dest.exists():errors.append([file,v,'not found']);continue
    if u.fragment and target.endswith('.html') and not BeautifulSoup(dest.read_text(),'html.parser').find(id=u.fragment):errors.append([file,v,'missing anchor'])
for pair in pairs:
 for file in [pair['zh'],pair['en']]:
  soup=BeautifulSoup((root/file).read_text(),'html.parser')
  for tag in soup.select('[srcset]'):
   for candidate in tag['srcset'].split(','):
    value=candidate.strip().split()[0];u=urlsplit(value)
    if u.scheme or u.netloc:continue
    target=u.path.lstrip('/') if u.path.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(file),u.path))
    if not (root/target).is_file():errors.append([file,value,'srcset not found'])
print('Pairs with identical body structure:',len(pairs));print(json.dumps(errors,ensure_ascii=False,indent=2))
(root.parent/'docs/review/bilingual-ui/static-qa.json').write_text(json.dumps({'pairs':len(pairs),'identicalStructure':True,'errors':errors},ensure_ascii=False,indent=2))
assert not errors
