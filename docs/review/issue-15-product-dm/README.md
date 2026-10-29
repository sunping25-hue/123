# Issue #15 — Product DM downloads

Base: `84c2890`, isolated branch `codex/issue-15-product-dm`. This change is prepared for PR review only; it has not been merged or deployed.

## Scope

- Eight owner-specified original PDFs from Google Drive, copied unchanged into `shinox-v2-site/downloads/dm/` and served under `/downloads/dm/`.
- Chinese and English homepage product DM cards now provide four language-matched downloads. Chinese copy: 「包含 M9、B2 洗車機，以及九合一控制箱（投幣款、觸控款）專題 DM。」
- Matching download buttons added to B2 (`wash-1`), M9 (`wash-2`) and nine-in-one (`self-3`) product pages in both languages. The control-box pages offer both coin-operated and touchscreen PDFs.
- Both startup-guide cards are byte-identical to the base commit. All other homepage content, product prose, images, navigation and unrelated pages are unchanged; no server or shared CSS changes. The existing DM status rows on the nine-in-one and M9 pages in both languages now say “已提供下載” / “Available to download”, matching the actual download links.

## Source and file checks

Drive metadata was read before each authenticated raw-file fetch. All eight originals are `application/pdf`, begin with `%PDF-`, parse as one-page PDFs, and have sizes matching Drive metadata. Files were neither recreated nor substituted. Detailed Drive IDs, byte sizes and SHA-256 hashes are in [validation.json](validation.json).

The repository's unchanged Python preview server was used on port 3035. Each `/downloads/dm/` URL returned HTTP 200 with `application/pdf`; response bytes matched its original SHA-256. Chromium tests clicked every download button at desktop 1440px and mobile 390px on all eight affected pages, verified the downloaded filenames and original-byte hashes, and checked for horizontal overflow, button overflow and JavaScript errors.

## Existing layout limitation

The English B2/M9 mobile product pages have a pre-existing variant-selector overflow at the 390px viewport: the “Dual arm” button extends to roughly 431px. The same overflow was independently reproduced using the unmodified `84c2890` HTML. New DM buttons remain inside the viewport, with no button-content overflow. This unrelated variant layout is preserved for separate review rather than expanded into the DM task.

## Browser screenshots

Each comparison places Traditional Chinese on the left and English on the right. Desktop screenshots are reduced to 50% in the comparison; originals are retained alongside them.

| Changed region | Desktop 1440px | Mobile 390px |
|---|---|---|
| Homepage downloads, including untouched startup-guide card | [Compare](index-compare-1440.webp) | [Compare](index-compare-390.webp) |
| B2 product hero download button | [Compare](products-wash-1-compare-1440.webp) | [Compare](products-wash-1-compare-390.webp) |
| M9 product hero download button | [Compare](products-wash-2-compare-1440.webp) | [Compare](products-wash-2-compare-390.webp) |
| Nine-in-one product hero, both versions | [Compare](products-self-3-compare-1440.webp) | [Compare](products-self-3-compare-390.webp) |

This local verification does not establish that the formal website is updated. Publication remains outside this PR task.
