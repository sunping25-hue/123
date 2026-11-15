import asyncio,json
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright,expect
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'docs/review/google-sheets-inquiry';BASE='http://127.0.0.1:3050/'
URL='https://script.google.com/macros/s/AKfycbyIHCL_KxWtDzHB02x0GkkPNAT-rOIi9NbXa6eNyrFvhrFdwITomHPNDqVSYoVbj2G5ow/exec'
EXPECTED_KEYS={'name','phone','email','region','hasSite','model','message','description','location','preferredDate','preferredTime','consent','consentConfirmedAt','privacyPolicyVersion','website','formType','lang','page'}
async def fill(form,index=0):
 for name,value in [('name','ShinoX QA Test'),('phone','0900000000'),('email','qa@example.test'),('region','TEST REGION'),('message','Synthetic QA only; no real personal information.')]:await form.locator('[name='+name+']').fill(value)
 await form.locator('[name=subject]').select_option(index=3)
 await form.locator('[name=hasSite]').nth(index).check()
 await form.locator('[name=consent]').check()
async def main():
 results=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for route in ['index.html','contact.html','en/index.html','en/contact.html']:
   english=route.startswith('en/')
   success='Thank you, we have received your enquiry and will contact you soon.' if english else '已收到，我們會盡快與您聯繫'
   failure='Submission failed. Please contact us via LINE @shinox or call +886 979-666-302.' if english else '送出失敗，請改用 LINE @shinox 或來電 0979-666-302'
   for width in [1440,390]:
    context=await browser.new_context(viewport={'width':width,'height':1000 if width>500 else 844},reduced_motion='reduce')
    await context.add_init_script('''(()=>{const original=window.fetch;window.__sheetFetch=[];window.fetch=async(...args)=>{const item={url:String(args[0]),options:args[1]};if(item.url.startsWith('https://script.google.com/'))window.__sheetFetch.push(item);const response=await original(...args);item.response={type:response.type,status:response.status};return response}})();''')
    calls=[];api=[];mode={'fail':False};errors=[]
    async def post(handler):
     request=handler.request;assert request.url==URL and request.method=='POST'
     payload=json.loads(request.post_data);calls.append({'payload':payload,'headers':request.headers})
     if mode['fail']:await handler.abort('failed');return
     await asyncio.sleep(.2);await handler.fulfill(status=200,body='opaque test response')
    async def local_api(handler):api.append(handler.request.url);await handler.fulfill(json={'mode':'local-preview','acceptingLeads':False,'legalReviewAccepted':False,'emailConfigured':False,'persistence':False})
    await context.route('https://script.google.com/**',post);await context.route('**/api/**',local_api)
    page=await context.new_page();page.set_default_timeout(30000);page.on('pageerror',lambda e:errors.append(str(e)))
    await page.goto(BASE+route,wait_until='domcontentloaded');await page.evaluate('document.fonts.ready')
    if await page.locator('.campaign-popup-close:visible').count():await page.locator('.campaign-popup-close:visible').click()
    form=page.locator('#inquiry-form');button=form.locator('.submit');result=form.locator('#form-result')
    assert not await form.locator('#inquiry-fields').evaluate('(e)=>e.disabled')
    assert (await button.inner_text()).strip().rstrip('↗').strip()==('Send enquiry' if english else '送出洽詢')
    assert await form.locator('[name=hasSite]').count()==3 and await form.locator('[name=hasSite]:checked').count()==0 and not await form.locator('[name=consent]').is_checked()
    labels=await form.locator('.has-site-group label').all_text_contents();assert labels==(['Yes, I have a site','No, still looking','Evaluating'] if english else ['有，已有場地','沒有，還在找','評估中'])
    assert await form.locator('.has-site-group').evaluate('(g)=>Boolean(g.previousElementSibling.querySelector("[name=region]")) && Boolean(g.nextElementSibling.querySelector("[name=subject]"))')
    await form.screenshot(path=str(OUT/f'{route.replace("/","-").replace(".html","")}-{width}.webp'),type='webp',quality=80)
    # Missing site / consent must never send, including synthetic submit events.
    for name,value in [('name','ShinoX QA Test'),('phone','0900000000'),('email','qa@example.test'),('region','TEST REGION')]:await form.locator('[name='+name+']').fill(value)
    await form.evaluate('(f)=>f.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}))');assert not calls
    assert await form.locator('[name=hasSite]').first.evaluate('(e)=>e.validity.valueMissing')
    await form.locator('[name=hasSite]').first.check()
    await form.evaluate('(f)=>f.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}))');assert not calls
    # Lead request and duplicate-click protection.
    await fill(form,index=0);confirmed=await form.locator('[name=consentConfirmedAt]').input_value();assert confirmed
    selected=await form.locator('[name=subject]').input_value();await button.click();await form.evaluate('(f)=>f.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}))')
    await expect(result).to_have_text(success);assert len(calls)==1
    payload=calls[-1]['payload'];assert set(payload)==EXPECTED_KEYS
    assert payload['model']==selected and 'subject' not in payload and payload['formType']=='lead'
    assert payload['hasSite']==labels[0] and payload['consent'] is True and payload['consentConfirmedAt']==confirmed
    datetime.fromisoformat(payload['consentConfirmedAt'].replace('Z','+00:00'))
    assert payload['privacyPolicyVersion']=='2026-10-29.1' and payload['lang']==await page.locator('html').get_attribute('lang') and payload['page']=='/'+route
    assert payload['description']==payload['message'] and payload['location']==payload['preferredDate']==payload['preferredTime']==payload['website']==''
    assert calls[-1]['headers']['content-type']=='text/plain;charset=utf-8'
    fetch=await page.evaluate('window.__sheetFetch[0]');assert fetch['options']['mode']=='no-cors' and fetch['options']['method']=='POST' and fetch['response']['type']=='opaque' and fetch['response']['status']==0
    assert await form.locator('[name=name]').input_value()=='' and not await form.locator('[name=consent]').is_checked() and await form.locator('[name=hasSite]:checked').count()==0 and await form.locator('[name=consentConfirmedAt]').input_value()==''
    # Booking includes its full fields and all three localized radio values are usable.
    await page.locator('[data-form-mode=booking]').click();await fill(form,index=2)
    for name,value in [('location','QA venue'),('preferredDate','2026-11-03'),('preferredTime','QA preferred time')]:await form.locator('[name='+name+']').fill(value)
    await button.click();await expect(result).to_have_text(success);assert len(calls)==2
    booking=calls[-1]['payload'];assert booking['formType']=='booking' and booking['hasSite']==labels[2] and booking['location']=='QA venue' and booking['preferredDate']=='2026-11-03' and booking['preferredTime']=='QA preferred time'
    assert await form.locator('#booking-fields').get_attribute('hidden') is not None
    # Network failure keeps the data and supplies the exact fallback copy.
    mode['fail']=True;await fill(form,index=1);await button.click();await expect(result).to_have_text(failure);assert len(calls)==3
    assert await form.locator('[name=name]').input_value()=='ShinoX QA Test' and await form.locator('[name=hasSite]:checked').input_value()==labels[1] and await form.locator('[name=consent]').is_checked() and await button.is_enabled()
    # Honeypot rejects locally without sending a fourth request.
    await form.locator('[name=website]').evaluate('(e)=>e.value="synthetic-bot.example.test"');await form.evaluate('(f)=>f.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}))');assert len(calls)==3
    await form.locator('[name=consent]').uncheck();assert await form.locator('[name=consentConfirmedAt]').input_value()==''
    assert not api and not errors and not await page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),{'api':api,'errors':errors}
    results.append({'page':route,'width':width,'immediateAvailabilityWithoutLocalApi':'PASS','siteAndConsentRequired':'PASS','allRadioOptions':'PASS','leadAndBookingPayload':'PASS','opaqueNoCorsResponse':'PASS','successAndReset':'PASS','networkFailureAndRecovery':'PASS','honeypot':'PASS','duplicateSubmit':'PASS','oldApiRequests':len(api),'interceptedOnly':True,'requests':calls})
    print('PASS',route,width,flush=True);await context.close()
  await browser.close()
 (OUT/'browser-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print('ALL PASS',len(results),'browser scenarios; all Google requests intercepted, no real data sent')
asyncio.run(main())
