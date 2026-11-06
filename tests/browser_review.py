"""Optional browser acceptance checks. Run against a local preview only.
Requires Playwright Python and Chromium; no deployment or real contact data.
"""
import argparse
import asyncio
import json
from pathlib import Path
import shutil
from playwright.async_api import async_playwright

async def review(origin, output):
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        executable = shutil.which('chromium') or shutil.which('chromium-browser')
        browser = await p.chromium.launch(**({'executable_path': executable} if executable else {}), args=['--no-sandbox'])
        for language, route in [('zh', '/'), ('en', '/en/index.html')]:
            for width, height in [(1440, 900), (768, 1024), (390, 844)]:
                page = await browser.new_page(viewport={'width': width, 'height': height})
                errors = []
                videos = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('request', lambda req: videos.append(req.url) if '/media/shinox-hero' in req.url else None)
                await page.goto(origin + route)
                await page.wait_for_function('document.querySelector("video").currentTime > 0')
                expected = 'shinox-hero-mobile.mp4' if width < 768 else 'shinox-hero.mp4'
                assert await page.locator('video').evaluate('(v)=>v.muted && v.loop && v.playsInline')
                assert all(url.endswith(expected) for url in videos), videos
                assert videos, 'No video request'
                await page.locator('video').evaluate('(v)=>v.currentTime=v.duration-.3')
                await page.wait_for_function('document.querySelector("video").currentTime<3&&!document.querySelector("video").paused', timeout=20000)
                assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                await page.screenshot(path=str(output / f'{language}-home-{width}.png'))
                if language == 'zh':
                    for key in ['metal', 'energy', 'air', 'water', 'fluid']:
                        await page.locator('#tab-' + key).click()
                        await page.wait_for_function('(key)=>{const v=document.querySelector("#panel-"+key+" video");return v&&v.readyState>=2&&!v.error}', arg=key)
                    await page.locator('#tab-metal').click()
                    await page.locator('#tab-metal').press('End')
                    assert await page.locator('#tab-fluid').get_attribute('aria-selected') == 'true'
                catalog = page
                if language == 'zh':
                    catalog = await browser.new_page()
                    await catalog.goto(origin+'/products.html')
                links = await catalog.locator('a[href*="products/"][href$=".html"]').evaluate_all('(a)=>[...new Set(a.map(x=>x.href))]')
                assert len(links) == 15, len(links)
                for href in links:
                    assert (await page.request.get(href)).status == 200
                if catalog is not page:
                    await catalog.close()
                assert not errors, errors
                print(json.dumps({'language':language,'width':width,'video':expected,'productLinks':len(links),'errors':errors}), flush=True)
                await page.close()
            # No media request with reduced-motion OR browser data saver.
            for setting in ['reduced-motion', 'save-data', 'slow-2g']:
                page = await browser.new_page(reduced_motion='reduce' if setting=='reduced-motion' else 'no-preference')
                if setting != 'reduced-motion':
                    await page.add_init_script('Object.defineProperty(navigator,"connection",{value:{saveData:%s,effectiveType:"%s"}})' % ('true' if setting=='save-data' else 'false', '2g' if setting=='slow-2g' else '4g'))
                videos = []
                page.on('request', lambda req: videos.append(req.url) if '/media/shinox-hero' in req.url else None)
                await page.goto(origin + route)
                await page.wait_for_timeout(300)
                assert not videos, videos
                assert await page.locator('video').evaluate('(v)=>v.paused')
                await page.close()
                print(language, setting, 'poster only', flush=True)
        await browser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin', default='http://127.0.0.1:3005')
    parser.add_argument('--output', type=Path, default=Path('/tmp/shinox-review'))
    args = parser.parse_args()
    asyncio.run(review(args.origin.rstrip('/'), args.output))
