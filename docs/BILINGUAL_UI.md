# Shared ShinoX design and English publishing

Traditional Chinese HTML in `shinox-v2-site/` and `products/` is the sole design master. The 24 English pages (seven main pages, 15 product details, privacy and 404) are generated; do not maintain separate English HTML/CSS/JS layouts.

1. Edit Chinese master HTML and shared CSS/JS/assets.
2. Add or revise the corresponding exact translations in `shinox-v2-site/locales/en.json`. Preserve brands, model IDs and confirmed specifications.
3. Install build dependency with `python -m pip install -r scripts/requirements.txt` when needed.
4. Run `python scripts/build_english.py`, then `python scripts/build_english.py --check` before publishing. Missing Chinese translations or stale generated output fail the check.

`locales/pages.json` records corresponding routes. The generator preserves page structure, shared asset paths, SVGs, form option values and interaction hooks; only display text, language metadata and relative page links change. `site-locale.js` translates dynamic dialogs, error states and accessibility labels from the same dictionary. `locales/en.js` is generated, never edited separately. Language switches preserve the current page and product. Any Chinese markings physically present on original equipment artwork stay on the shared asset; they are not rewritten into imaginary equipment controls.

Shared controls: `ui-controls.css/js` covers primary, secondary, functional, navigation, tabs, card actions and dynamically inserted dialogs; investment, LINE and WhatsApp retain their approved specialized geometry. Motion is opt-in through hover or an explicit six-stage auto-demo control; reduced-motion is respected.

## Official YouTube

`youtube.css/js` provides a single official footer entry on every page and detects/removes duplicate channel entries. Homepage brand and business process entries use the same component material, red play SVG, external-link semantics, focus and reduced-motion behavior.

`youtube-videos.js` is deliberately empty until a specific product video is verified. Add `{url, verified: true, source}` under the exact product slug only after the owner supplies/approves the matching video; `source` records that confirmation. Only valid HTTPS YouTube video URLs are accepted. A channel URL is never presented as a product's machine demonstration. Current product pages therefore show the official footer channel, with no unverified product-video CTA.

## Six-stage process

`business-process.css/js` and the actual HTML/SVG section in `business.html` are shared by both languages. Native tabs support Arrow Left/Right, Home/End, previous/next, selected details and horizontal mobile scrolling. Auto mode is off initially, advances every six seconds only after explicit activation, pauses outside the viewport or while the document is hidden, and stops when reduced-motion is enabled. Existing consultation links remain in place.

## Review evidence

See [actual paired desktop/mobile screenshots](review/bilingual-ui/README.md), `page-qa.json`, and `interaction-qa.json`. Screenshots use reduced motion for stable visual comparison; normal hover motion is tested separately. Native browser tests validate actual HTML controls and intercepted external destinations without posting form data or asserting that the private static review site sends email or confirms bookings.

To repeat review checks, run the local server with `python server.py --port 3027`, then `python scripts/check_bilingual_assets.py`, `python scripts/qa_bilingual_capture.py` and `python scripts/qa_bilingual_interaction.py`. Browser checks require the existing Chromium executable (override with `CHROMIUM_EXECUTABLE`), Python Playwright and Pillow. `--base-url` selects another preview. The capture script validates 24 language pairs at 1440/390 and stores 44 paired screenshots; interaction checks cover 1440/768/390/375 in both languages. No live form submission or calculator password is needed.

Concurrent business-journey commits were retained in Git history and consolidated into the single accessible `#biz-process-demo` component. The obsolete three-step block and duplicate six-stage markup are absent. Historical `business-journey.css/js` files remain in the source but are not loaded; active behavior uses the shared `business-process.css/js` in both languages.
