import asyncio,json,argparse,os,io
from pathlib import Path
from PIL import Image,ImageDraw
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/review/bilingual-ui';OUT.mkdir(parents=True,exist_ok=True)
pairs=json.loads((ROOT/'shinox-v2-site/locales/pages.json').read_text());results=[]
parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://127.0.0.1:3027/');parser.add_argument('--products-only',action='store_true');parser.add_argument('--page');args=parser.parse_args();BASE=args.base_url.rstrip('/')+'/'
if args.products_only or args.page:
 results[:]=[r for r in json.loads((OUT/'page-qa.json').read_text()) if ('/products/' not in '/'+r['route'] if args.products_only else r['route'] not in [args.page,'en/'+args.page])]
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE','/usr/bin/chromium'),args=['--no-sandbox']);context=await browser.new_context(reduced_motion='reduce');await context.add_init_script("sessionStorage.setItem('shinox-campaign-seen','1')")
  sem=asyncio.Semaphore(3)
  async def capture_pair(width,pair):
   async with sem:
    images=[]
    for lang in ['zh','en']:
     route=pair[lang];page=await context.new_page();await page.set_viewport_size({'width':width,'height':960 if width>600 else 844});errors=[];bad=[]
     page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append([r.status,r.url]) if r.status>=400 else None)
     await page.goto(BASE+route,wait_until='domcontentloaded');await page.evaluate('document.fonts.ready')
     if await page.locator('.campaign-popup[open]').count():await page.locator('.campaign-popup-close').click()
     await page.locator('img').evaluate_all('(images)=>Promise.all(images.map(i=>{i.loading="eager";return i.decode().catch(()=>{})}))')
     r=await page.evaluate('''()=>{const texts=[];const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=walker.nextNode()){const e=n.parentElement;if(!e.closest('script,style,[data-locale-link="zh-Hant"]')&&/[\\u3400-\\u9fff]/.test(n.textContent))texts.push(n.textContent.trim())}return {overflow:document.documentElement.scrollWidth>innerWidth,badImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),chinese:texts,controls:document.querySelectorAll('.ui-control').length,youtube:[...document.querySelectorAll('a.ui-youtube')].map(a=>({href:a.href,target:a.target,rel:a.rel,label:a.textContent})),footerYoutube:document.querySelectorAll('footer a.ui-youtube').length,productVideos:document.querySelectorAll('[data-product-video]').length,heading:document.querySelector('h1')?.textContent}}''')
     r.update({'width':width,'route':route,'errors':errors,'badResponses':bad});results.append(r)
     assert not r['overflow'] and not r['badImages'] and not errors and not bad,r
     assert r['footerYoutube']==1 and r['productVideos']==0,r
     assert all(a['href']=='https://www.youtube.com/@ShinoXwash' and a['target']=='_blank' and set(a['rel'].split())>={'noopener','noreferrer'} for a in r['youtube']),r
     if lang=='en':assert not r['chinese'],r
     if pair['zh'] not in ['404.html','privacy.html']:images.append(Image.open(io.BytesIO(await page.screenshot(full_page=True,type='png'))).convert('RGB'))
     await page.close()
    if images:
     scale=.5 if width==1440 else 1;size=int(width*scale);height=max(int(i.height*scale) for i in images);canvas=Image.new('RGB',(size*2+12,height+36),'#061322');draw=ImageDraw.Draw(canvas);draw.text((12,12),'Traditional Chinese / '+str(width)+'px',fill='white');draw.text((size+24,12),'English / '+str(width)+'px',fill='white')
     for i,im in enumerate(images):canvas.paste(im.resize((size,int(im.height*scale)),Image.Resampling.LANCZOS),(i*(size+12),36))
     canvas.save(OUT/(pair['zh'].replace('/','-').replace('.html','')+'-'+str(width)+'.webp'),quality=82)
    print('Captured',width,pair['zh'],flush=True)
  await asyncio.gather(*(capture_pair(width,pair) for width in [1440,390] for pair in pairs if (not args.products_only or pair['zh'].startswith('products/')) and (not args.page or pair['zh']==args.page)))
  await browser.close()
 (OUT/'page-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 rows=['# 中英文實際網頁對照\n','Chromium 本機實測；左側繁體中文、右側英文。桌機原始寬度 1440px（對照縮至50%），手機390px。減少動畫模式保持畫面可比較；另行測試正常動畫與互動。\n','|頁面|桌機對照|手機對照|','|---|---|---|']
 for pair in pairs:
  if pair['zh'] in ['404.html','privacy.html']:continue
  slug=pair['zh'].replace('/','-').replace('.html','');rows.append(f"|{pair['zh']}|[1440px]({slug}-1440.webp)|[390px]({slug}-390.webp)|")
 (OUT/'README.md').write_text('\n'.join(rows)+'\n');print('ALL PASS',len(results),flush=True)
asyncio.run(main())
