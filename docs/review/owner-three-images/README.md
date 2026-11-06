# Supplied brand showcase, M9 and 20L chemical images

The uploaded `設備整合品牌展示 英文版.zip` contains all three previously requested original PNGs. Each was inspected and visually matched to the corresponding inline image before implementation. This update resolves all three missing-original items from the prior review checkpoint.

## Completed integration

| Original | Placement | Behavior |
| --- | --- | --- |
| `設備整合品牌展示 英文版.png` (1774 × 887) | `about.html#brand-mission-title` | Left 40% original vision text, right 60% full image, vertically centered. No crop, extra title, frame or card. Mobile text then image; phone clearance for floating contacts. Image opens full resolution in a new tab with noopener/noreferrer. |
| `未來感純水洗車隧道.png` (1672 × 941) | `products.html#product-m9`, `products/wash-2.html` | The exact newly supplied M9 image replaces the pending image region in the hub and adds the full image to the detail page. Contain keeps the whole gantry and wash bay visible; specifications and original hero copy retained. |
| `ShinoX未來感汽車美容化學品展示.png` (1672 × 941) | `products.html#chemical-series` | After the peripheral equipment showcase and before the bottom contact CTA. Full 16:9 contained artwork with all three canisters/labels. Three native HTML introductions and distinct 20L email-draft enquiry subjects. |

Blue: Coating Protection / 車漆鍍膜劑. Orange: Deep Cleaner / 強效去汙劑. Red: High Foam Shampoo / 高濃縮泡沫洗車精. Each is 20L. No additional technical, dilution or performance claims were added.

All images use the supplied pixels, WebP conversion and proportional responsive sizes. The six asset files total 1,389,742 bytes; browsers select responsive variants and below-fold art is lazy-loaded. The M9 detail hero image is eager/high priority. Source and derivative dimensions/hashes are in `docs/OWNER_THREE_IMAGES_UPLOAD.json`.

Chinese and English share the same assets, layout CSS and animation. The PNGs' English labels remain intact; HTML labels and alt text are translated. Brand text/signature, M9 specifications, existing enquiries and all other page sections remain unchanged. The chemical section participates in existing all/peripheral filters; self-service and wash filters hide it.

## Actual browser screenshots

| Section | Chinese desktop | Chinese tablet | Chinese mobile | English desktop | English mobile |
| --- | --- | --- | --- | --- | --- |
| Brand vision | [1440](zh-1440-brand.webp) | [768](zh-768-brand.webp) | [390](zh-390-brand.webp) | [1440](en-1440-brand.webp) | [390](en-390-brand.webp) |
| M9 detail | [1440](zh-1440-m9.webp) | [768](zh-768-m9.webp) | [390](zh-390-m9.webp) | [1440](en-1440-m9.webp) | [390](en-390-m9.webp) |
| 20L series | [1440](zh-1440-chemicals.webp) | [768](zh-768-chemicals.webp) | [390](zh-390-chemicals.webp) | [1440](en-1440-chemicals.webp) | [390](en-390-chemicals.webp) |
| Product hub | [1440](zh-1440-hub.webp) | — | [390](zh-390-hub.webp) | [1440](en-1440-hub.webp) | [390](en-390-hub.webp) |

## Verification and limits

Chromium Chinese/English at 1920, 1440, 1024, 768, 390 and 375px: 36 section/language/width checks. All image paths decode, no horizontal or text overflow/page errors/failed responses. Desktop brand columns are exactly 40/60 and center vertically; mobile stacks correctly. Brand logos and M9 are contained without cropping, and the chemical banner is 16:9 with contained content.

Brand CTA navigation reaches the matching business page. Full-image links open the actual asset in a separate tab without an opener. All six localized chemical enquiry click targets and unique product/capacity email subjects were verified; clicks were intercepted rather than sent to an email application. This verifies draft-link wiring, not SMTP delivery. Existing all/self/wash/peripheral filters, image fade-in, keyboard focus and reduced-motion behavior were checked.

The contact form remains disabled in Chinese and English. Source-scope checks compare original brand narrative and M9 specification DOM; all other brand/hub content, homepage, Hero, logos, form code, API status, legal configuration, calculators and nine-in-one detail are unchanged. See `qa.json` and `scope-checks.json`. No backend or form-opening change was made.

## Implementation files

- `shinox-v2-site/about.html`, `en/about.html`, `brand-mission-visual.css`.
- `shinox-v2-site/products.html`, `en/products.html`, `chemical-series.css`, `chemical-series.js`.
- `shinox-v2-site/products/wash-2.html`, `en/products/wash-2.html`, M9-only additions to `product-imagery.css`, including phone CTA clearance for floating contacts.
- Six optimized assets under `lassets/about/` and `lassets/products/`.
- `locales/en.json` and generated `en.js`; updated asset manifests and this review evidence.

Final phone-control checks at 390/375px in both languages confirm the M9 detail CTA keeps a 44px touch height, remains clear of both floating contact controls, and opens the matching M9 detail page. See `mobile-hub-controls.json`.
