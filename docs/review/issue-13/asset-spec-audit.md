# Issue #13 read-only asset/spec audit

Audit target: `/workspace/123-issue13`, HEAD `88a3a77`. No code, image or GitHub edits made.

## Original long references

Neither `ShinoX_M9_官網介紹.jpg` nor `ShinoX_B2_官網介紹.jpg` was found in the repository or `/workspace/attachments` filenames / ZIP member inventories. No matching `官網介紹` member found. Issue #13 contains textual instructions and filenames, not original attachment download URLs. Therefore exact image-to-page fidelity cannot be claimed. Existing QA screenshots under `docs/review/` are rendered site screenshots, not those original owner design boards. Do not reconstruct or rasterize the referenced long pages.

## Approved actual asset bytes

All paths below are relative to `shinox-v2-site/`.

| Model | Primary image | Size | Responsive image |
|---|---|---|---|
| B2 | `lassets/products/b2-wash-action.webp` | 1672×941, 294196 bytes | `b2-wash-action-small.webp`, 768×432, 85858 bytes |
| M9 latest owner showcase | `lassets/products/m9-owner-showcase.webp` | 1280×800, 208774 bytes | `m9-owner-showcase-small.webp`, 768×480, 91136 bytes |
| Earlier approved M9 tunnel view | `lassets/products/m9.webp` | 1672×941, 311368 bytes | `m9-small.webp`, 836×471, 93938 bytes |

Evidence: `docs/review/owner-equipment-20261029/assets.json` records original owner RAR sources and exact derivative paths: B2 `霓虹藍光下的泡沫洗車艙.rar`, M9 `ShinoX M9 自動水刀洗車機 CGI 形象圖.rar`. Original preserved sources are `lassets/products/source/b2-owner-20261029.png` (1672×941) and `source/m9-owner-20261029.png` (1280×800). Earlier M9 approval/source is in `docs/OWNER_THREE_IMAGES_UPLOAD.json` (`未來感純水洗車隧道.png`, whole frame retained).

Current four HTML documents already reference B2/M9 correct primary owner assets and derivatives. Chinese B2 uses its image twice; M9 once; English matches. No abstract illustration image URL is used by the current product-editorial.js (it creates DOM text/cards only), product-showcase.js, or their CSS. CSS url() inventories in products.css, product-editorial.css, product-showcase.css and product-imagery.css are empty. Thus no stale abstract *image placeholder* found to replace in these current pages. Main concern is duplicated static/editorial content and any old data disclaimer treatment, not broken abstract asset substitution. Do not swap the correct equipment assets for generic innovation/turbine art.

## Source and numeric classification

Fetched current owner-authored Issue #3 and Issue #13. Issue #3 explicitly labels Section 4 FAQ as confirmed facts, and specifies B2 additional properties. This is owner-supplied product information, not independent laboratory verification. Use approximate language where supplied and avoid performance guarantees.

| Existing editorial value | Evidence | Recommended treatment |
|---|---|---|
| B2 `2:30` | Issue #3 confirmed FAQ: approximately 2 min 30 s per car | Can show `約 2 分 30 秒` / `Approx. 2 min 30 s`; retain cycle/site qualification, not guaranteed maximum |
| B2 `約100 L` | Issue #3 confirmed FAQ | Can show approximate water use per car with clear units and qualification |
| B2 `25–30` | No meaning/unit or confirmation in Issue #3; Issue #13 calls reference | Remove ambiguous numerical stat or replace with `待確認`; do not silently infer cars/hour, pressure, power, etc. |
| B2 `4 × 4 kW` | Issue #3 confirms FOUR blowers, not 4kW each | Show `4 組吹風機` / `4 blowers`; do not assert 4kW motor ratings. Issue #3 separately confirms total power 25kW, which is not this claim |
| M9 `360°` | Not specified as confirmed fact in Issue #3; Issue #13 reference | If retained, identify only as conceptual/reference coverage, pending final model specification; avoid authoritative intro/spec claim until confirmed |
| M9 `2 / 6 min` | Not confirmed in Issue #3; Issue #13 reference | Pending reference cycle, not guaranteed 2-minute / 6-minute product specification; best move from headline KPI to clear pending/reference note or omit values |
| M9 `70–100` | No unit in editorial; not confirmed in Issue #3 | Do not infer bar/MPa; replace with explicit pressure pending confirmation |
| M9 `28 s` | Not confirmed in Issue #3 | Pending reference only, not an achieved drying-time guarantee |

Other confirmed owner facts available from Issue #3: B2 sequence underbody spray → pre-soak → high-pressure rinse → foam waterfall → shine coat → protective coating → four blowers; 6.2m track; total power 25kW; single/dual arm options; one-year warranty; optional side blowing and stainless kit. M9: stronger water/air positioning, single/dual arm options, underbody wash standard, one-year warranty. Neither source confirms all generic optional chips (payment/member/cloud/coating) for every model configuration; keep discussion/optional wording.

The current editorial text calls B2/M9 all stats “reference” and places a broad disclaimer later, but M9 introduction and spec table still assert 360° / cycle values prominently. A distant general disclaimer does not resolve model-specific uncertainty. Prefer per-field evidence/status and units, in both languages, and no fabricated physical capabilities.
