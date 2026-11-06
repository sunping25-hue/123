import asyncio,json,argparse,os
from pathlib import Path
from playwright.async_api import async_playwright,expect
OUT=Path(__file__).resolve().parents[1]/'docs/review/bilingual-ui';results=[]
parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://127.0.0.1:3027/');args=parser.parse_args();BASE=args.base_url.rstrip('/')+'/'
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE','/usr/bin/chromium'),args=['--no-sandbox'])
  for width in [1440,768,390,375]:
   for lang in ['','en/']:
    c=await b.new_context(viewport={'width':width,'height':900},reduced_motion='reduce');page=await c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    async def goto(route):
     await page.goto(BASE+lang+route,wait_until='domcontentloaded');await page.wait_for_timeout(180)
     if await page.locator('.campaign-popup[open]').count():await page.locator('.campaign-popup-close').click()
    await goto('business.html');section=page.locator('#biz-process-demo');tabs=section.get_by_role('tab');assert await tabs.count()==6
    await section.scroll_into_view_if_needed()
    for i in range(6):
     await tabs.nth(i).click();assert await tabs.nth(i).get_attribute('aria-selected')=='true';assert await section.locator('[role=tabpanel]:visible').count()==1;assert await section.locator('[role=tabpanel]:visible').get_attribute('id')=='biz-panel-'+str(i+1)
    assert await section.locator('[data-biz-next]').is_disabled()
    await tabs.nth(5).press('Home');assert await tabs.nth(0).get_attribute('aria-selected')=='true';assert await section.locator('[data-biz-previous]').is_disabled()
    await tabs.nth(0).press('ArrowRight');assert await tabs.nth(1).evaluate('(e)=>document.activeElement===e');await tabs.nth(1).press('End');assert await tabs.nth(5).get_attribute('aria-selected')=='true'
    await section.locator('[data-biz-previous]').click();assert await tabs.nth(4).get_attribute('aria-selected')=='true';await section.locator('[data-biz-next]').click();assert await tabs.nth(5).get_attribute('aria-selected')=='true'
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert await section.locator('h2').evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 255, 255)'
    if width<600:assert await section.locator('.biz-process-scroller').evaluate('(e)=>e.scrollWidth>e.clientWidth')
    await tabs.nth(0).click()
    if width in [1440,390]:await section.screenshot(path=str(OUT/('process-'+('en' if lang else 'zh')+'-'+str(width)+'.png')))
    # Optional auto mode is initially stopped, only starts on an explicit request.
    auto=section.locator('[data-biz-auto]');assert await auto.get_attribute('aria-pressed')=='false'
    await auto.click();await page.wait_for_timeout(6400);assert await tabs.nth(1).get_attribute('aria-selected')=='true',await section.evaluate('(e)=>({selected:e.querySelector("[aria-selected=true]").id,playing:e.querySelector("[data-biz-auto]").outerHTML,rect:e.getBoundingClientRect().toJSON(),focus:document.activeElement.outerHTML,hidden:document.hidden})')
    await page.evaluate('window.scrollTo({top:0,behavior:"instant"})');await page.wait_for_timeout(6400);assert await tabs.nth(1).get_attribute('aria-selected')=='true',await section.evaluate('(e)=>({selected:e.querySelector("[aria-selected=true]").id,playing:e.querySelector("[data-biz-auto]").outerHTML,rect:e.getBoundingClientRect().toJSON(),focus:document.activeElement.outerHTML,hidden:document.hidden})')
    await auto.click();assert await auto.get_attribute('aria-pressed')=='false'
    # Official links really open a separate tab. Intercept the external page; never infer a video ID.
    await c.route('https://www.youtube.com/**',lambda route:route.fulfill(status=200,body='<title>Official destination test</title>'))
    yt=page.locator('footer .ui-youtube');assert await yt.count()==1
    async with c.expect_page() as popup_info:await yt.click()
    popup=await popup_info.value;await popup.wait_for_load_state();assert popup.url=='https://www.youtube.com/@ShinoXwash';assert await popup.evaluate('window.opener===null');await popup.close()
    # Keyboard focus and touch targets.
    await page.keyboard.press('Tab');await yt.focus();assert await yt.evaluate('(e)=>e.matches(":focus-visible")');assert await yt.evaluate('(e)=>e.getBoundingClientRect().height')>=44
    assert await yt.evaluate('(e)=>parseFloat(getComputedStyle(e).transitionDuration)')==0
    if width in [1440,390]:await page.locator('footer').screenshot(path=str(OUT/('footer-'+('en' if lang else 'zh')+'-'+str(width)+'.png')))
    # Same-page language route, retained calculator gate, localized dynamic error.
    switch=page.locator('header a[lang]').first
    assert 'business.html' in await switch.get_attribute('href')
    await page.locator('footer [data-calculator-url]').first.click();dialog=page.locator('.calculator-dialog');assert await dialog.is_visible()
    if lang:assert 'Please contact' in await dialog.locator('h2').inner_text()
    else:assert await dialog.locator('h2').inner_text()=='請聯絡業務索取密碼登入'
    await dialog.locator('input').fill('invalid-test-only');await dialog.locator('[type=submit]').click();await page.wait_for_timeout(70)
    assert await dialog.locator('.calculator-error').inner_text()
    if lang:assert not any('\u3400'<=ch<='\u9fff' for ch in await dialog.inner_text())
    await page.keyboard.press('Escape');assert not await dialog.is_visible()
    # Floating controls stay separate and preserve original URLs.
    line=page.locator('.line-float');wa=page.locator('.whatsapp-float');assert await line.get_attribute('href')=='https://line.me/R/ti/p/%40shinox';assert (await wa.get_attribute('href')).startswith('https://wa.me/886979666302')
    a=await line.bounding_box();z=await wa.bounding_box();assert a['y']+a['height']<=z['y'] or z['y']+z['height']<=a['y'];assert a['width']>=44
    # Home owns the same additional channel button; ad image and CTA localize properly.
    await goto('index.html');assert await page.locator('#about .ui-youtube').count()==1
    assert await page.locator('a.ui-youtube').count()==2
    if await page.locator('.campaign-popup').count():
     assert await page.locator('.campaign-popup img').evaluate('(e)=>e.complete&&e.naturalWidth>0')
     if lang:assert '/en/contact.html' in await page.locator('.campaign-popup-cta').get_attribute('href')
    await page.evaluate('window.scrollTo({top:1000,behavior:"instant"})');await page.wait_for_timeout(200);back=page.locator('.ui-backtop');assert await back.is_visible();await back.click();assert await page.evaluate('scrollY')==0;assert await page.locator('h1').evaluate('(e)=>document.activeElement===e')
    # Responsive navigation has one usable menu button, closes with Escape.
    if width<1201:
     toggle=page.locator('.toggle');await toggle.click();assert await toggle.get_attribute('aria-expanded')=='true';await page.keyboard.press('Escape');assert await toggle.get_attribute('aria-expanded')=='false'
    await goto('products.html');assert await page.locator('[data-product-video]').count()==0;assert await page.locator('footer .ui-youtube').count()==1
    await goto('products/wash-2.html');assert await page.locator('[data-product-video]').count()==0
    assert 'wash-2.html' in await page.locator('header a[lang]').first.get_attribute('href')
    await goto('contact.html');assert await page.locator('#inquiry-form').count()==1
    if lang:assert not await page.locator('main').evaluate('(e)=>/[\\u3400-\\u9fff]/.test(e.innerText)')
    assert not errors,errors
    results.append({'width':width,'language':'en' if lang else 'zh','process':'6 tabs, details, previous/next, Home/End/arrows, optional6s auto, offscreen pause PASS','youtube':'official URL, new tab, no opener, exactly one footer PASS','gates':'prompt, invalid entry, Escape, localized dynamic text PASS','controls':'focus, touch target, reduced motion, back-to-top, menu, LINE/WhatsApp gap PASS'})
    await c.close();print('Interactions PASS',width,lang or 'zh',flush=True)
  # Normal-motion hover and reduced-motion switching stop an explicitly running process demo.
  c=await b.new_context(viewport={'width':1440,'height':1000},reduced_motion='no-preference');page=await c.new_page();await page.goto(BASE+'en/business.html',wait_until='networkidle');link=page.locator('#biz-process-demo .ui-youtube');await link.hover();await page.wait_for_timeout(300)
  state=await link.evaluate('(e)=>({transform:getComputedStyle(e).transform,arrow:getComputedStyle(e.querySelector(".ui-arrow")).transform})');assert state['transform']=='matrix(1, 0, 0, 1, 0, -2)' and state['arrow']=='matrix(1, 0, 0, 1, 3, -3)',state
  auto=page.locator('[data-biz-auto]');await auto.click();await page.emulate_media(reduced_motion='reduce');await expect(auto).to_have_attribute('aria-pressed','false',timeout=3000)
  results.append({'normalMotion':state,'motionPreferenceChange':'stops auto PASS'});await c.close();await b.close()
 (OUT/'interaction-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print('ALL INTERACTIONS PASS',flush=True)
asyncio.run(main())
