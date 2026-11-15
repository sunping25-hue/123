# Issue #10 asset/spec audit — 2026-10-29

Scope: read-only audit of `/workspace/123-issue10` (no code or asset edits). Read AGENTS/master plan and fetched GitHub issue #10 plus comments. Issue is text only, contains no image attachment URL; comments endpoint returns `[]` (0 comments). No original 1–10 nine-in-one reference board found in tracked assets. Existing `docs/review/**` files are QA screenshots, not original owner boards.

## Approved bytes usable now

| Asset | Actual size | Evidence / appropriate use |
|---|---|---|
| `shinox-v2-site/lassets/home/about/home-about-equipment.webp` | 1264×848, 95,220 bytes | `docs/PRODUCT_IMAGES_OWNER_APPROVED.json` explicitly identifies as owner-supplied nine-in-one image; SHA256 `ba79ceb32f4a9beae8285bc521c38dcff77c7f9c8f38d6faaea89be440db3c1f`. Current Chinese + English self-3 detail uses it. Visually inspected: dark/silver rectangular cabinet, coin slots, many physical buttons, existing printed legends. Best accurate product Hero/detail with `contain`; do not replace its control face with invented touchscreen. Image approval does not verify every depicted setting/price as available specification. |
| `shinox-v2-site/lassets/home/about/home-about-equipment-small.webp` | 640×429, 28,128 bytes | Responsive derivative already wired in current page; same product framing. |
| `shinox-v2-site/lassets/home/category-self-service.webp` | 1280×800, 172,698 bytes | `docs/HOME_CATEGORY_IMAGES_UPLOAD.json` H06, source `ShinoX 九合一控制箱 CGI 形象圖 修正版.jpg`; owner-supplied CGI approved specifically for homepage category card. Visually inspected: blue cabinet in wet wash bay, same broad physical face layout. Can remain a clearly labeled owner CGI supporting scene; do NOT call real photo / independently verified blue finish / proof of available options. Safest new product page still uses primary owner-approved detail image. |
| `shinox-v2-site/lassets/business/hero-carwash.webp` | 1920×1080, 359,364 bytes | Owner-supplied banner (`docs/USER_FOUR_BANNERS.json` B01). Visually inspected: exterior dusk multi-bay wash architecture, reflective ground. Suitable broad wet-zone atmospheric background only with explicit architectural/concept label; not a real built case or dry-cleaning demonstration. |

Other conceptual assets exist (`business/site-planning-cgi.webp`, 1536×1024; `contact/showroom-concept.webp`, 1920×650), but neither depicts actual nine-in-one wet/dry functions. Do not repurpose showroom as dry-zone proof. Recommend custom DOM + inline SVG scene for wet and dry function sections with “功能情境示意 / 非實機操作” labels. No new artwork needed to unblock HTML implementation.

## Four finishes

There are NOT four approved, matched product finish photographs. Primary approved detail image is dark/metallic; a separate homepage blue CGI exists, but no verified silver/blue/black/red finish set or availability table. No red variant bytes found. Do not recolor cabinet or imply all four are orderable. Swatch interaction may show proposed finish with explicit pending confirmation and unchanged neutral approved equipment image; unavailable variants must not be presented as true photos.

## Actual confirmed specifications versus requests

`docs/SHINOX_V2_MASTER_PLAN.md` is a brief, not a verified device spec sheet. It lists planning directions (wet: high-pressure rinse, snow foam, low-pressure clean water, dry air gun, German nano coating, glass cleaner; dry: pneumatic wax, wet/dry vacuum) and explicitly requires final nine-function confirmation. Existing self-3 correctly states these are planning topics, not nine standard functions. Issue #10 requests additions but explicitly conditions standard/optional classification. No product specification PDF, model I/O table, payment-provider enablement table, membership/remote-management support matrix or verified four-finish availability document found in root docs. Therefore:

- Treat quick blow-drying / ozone sterilization / 110V socket as unconfirmed integration possibilities, not verified standard features.
- Coin, stored-value card, mobile payment and cloud points require configuration/service activation qualifiers; don't infer provider compatibility from the depicted panel.
- Two external-control cards are conceptual modules, NOT confirmation of exactly two physical ports or any actual compatible model.
- Settings and cloud panels must say interface demo / simulated data / optional, must not claim physical control or save to real hardware.
- Do not copy the visible image's prices/times into factual product specifications.

## Proposed precise missing-asset handoff (requested filenames, not existing files)

These names/dimensions are an implementation handoff recommendation, not supplied originals or a new requirement from issue #10.

| Requested file | Dimensions | Destination / purpose |
|---|---|---|
| `nine-in-one-reference-01-10.png` | Original resolution, minimum 2400px long edge | `docs/references/` — actual owner 1–10 reference board, internal design comparison only; never a page background |
| `nine-in-one-silver.webp` | 1200×1200 | `shinox-v2-site/lassets/products/nine-in-one/` — approved silver finish, matched angle |
| `nine-in-one-blue.webp` | 1200×1200 | same directory — approved blue finish, matched angle |
| `nine-in-one-black.webp` | 1200×1200 | same directory — approved black finish, matched angle |
| `nine-in-one-red.webp` | 1200×1200 | same directory — approved red finish, matched angle |
| `nine-in-one-wet-zone.webp` | 1600×1000 | same directory — authorized true wet-zone use or clearly approved CGI |
| `nine-in-one-dry-zone.webp` | 1600×1000 | same directory — authorized dry-zone use or clearly approved CGI |
| `nine-in-one-confirmed-specs.pdf` | PDF, not raster dimensions | `docs/source/` — verified standard/optional matrix, output interface details, payment/remote/member support and available finishes |

Existing product hero bytes suffice for implementation; all missing visual areas can use meaningful SVG/DOM demonstrations with honest labels. No image generation, source-code change or commit performed in this audit.
