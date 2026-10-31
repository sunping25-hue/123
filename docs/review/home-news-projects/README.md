# Homepage 05 / Newsroom and 06 / Selected Projects

The latest instruction uses image A (`202610299.png`) as the real asset source and image B (`霓虹科技洗車品牌案例展示(2).png`) only as the layout reference. Image B was readable inline in the conversation but was not included as a standalone file in the ZIP; no file-based pixel comparison is claimed.

## Source and implementation

- ZIP contains one 8820 × 3749 RGBA PNG. Split at original y=1720; removed excess outer negative space at x<1400 and x>5050 without changing the subject proportions.
- Upper artwork: `lassets/home/newsroom-visual.webp` (1600 × 754) and 800px responsive version.
- Lower artwork: `lassets/home/projects-visual.webp` (1600 × 889) and 800px responsive version.
- Four WebP files total 455,618 bytes; no image was regenerated or replaced by unrelated equipment. Original alpha retained. See `docs/HOME_NEWS_PROJECTS_UPLOAD.json` for original/output SHA256 and exact crop boxes.
- Desktop: shared 20/48/32 columns, left titles, centrally overlapping artwork, right description and native CTA. Image A has different subjects/frame proportions from B; its actual content and proportions are preserved.
- Background `#061626` with scoped edge masks and lighten blending. One subtle divider; no additional glass card or decorative background. Both CTAs retain `contact.html` (English resolves to `en/contact.html`).
- Phone text keeps a right-side safety margin for the existing floating contact icons; their code and positions are unchanged.
- Tablet/mobile <=900px: number/title, full main image, copy, CTA. Image uses proportional dimensions and `object-fit: contain`.
- Shared CSS and JS for Chinese and English. Only HTML text is translated; both versions use the same image files. Embedded equipment/scene signage in the supplied artwork remains unchanged.
- Reveal uses opacity and 12px translation; display-frame artwork floats 5px over 9s; bay camera scales 1 to 1.025 over 20s. Ambient animations pause outside the viewport or while the page is hidden. Reduced-motion disables these animations and reveals content immediately.

## Actual screenshots

| Viewport | Chinese | English |
| --- | --- | --- |
| 1672 (reference view) | [Desktop](zh-1672.webp) | [Desktop](en-1672.webp) |
| 1440 | [Desktop](zh-1440.webp) | [Desktop](en-1440.webp) |
| 768 | [Tablet](zh-768.webp) | [Tablet](en-768.webp) |
| 390 | [Mobile](zh-390.webp) | [Mobile](en-390.webp) |

## Scope

Implementation files: `shinox-v2-site/index.html`, `en/index.html`, `home-editorial.css`, `home-editorial.js`, the four WebP files and English dictionary/generated dictionary. Asset manifests and this review folder record provenance and verification.

No other homepage section, page, Hero/logo, calculator, privacy setting or form-opening state changed. The brand mission 40/60 layout request and M9 replacement still require the separate original files; they are not represented as completed by this homepage update.

## Verification results

- Chromium Chinese/English at 1920, 1672, 1440, 1024, 900, 768, 390 and 375px: 16 viewport/language checks passed. Images decode, no horizontal/text overflow or failed responses/page errors, contain aspect ratios remain proportional, and mobile follows the required order.
- Four actual CTA navigations reach the matching Chinese/English contact page. Hover, keyboard focus, reveal, ambient animation, offscreen pause and reduced-motion checks passed.
- Fixed the observed English title overflow at 1024px. Added phone text clearance after visual review showed the existing floating contacts could cover a long English title.
- At the reference width of 1672px the combined rows are approximately 938px tall, close to the 941px inline reference. Image content remains A rather than a substitute for B's different machinery.
- Chinese and English homepage DOM is unchanged outside the two requested sections and their scoped stylesheet/script tags. Protected asset and form/configuration hashes are recorded in `scope-checks.json`. The online form remains disabled.
- `python scripts/build_english.py --check`: all 25 page pairs are synchronized.
