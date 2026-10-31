# Homepage 02 / About ShinoX — integrated image and HTML overlays

Implemented on `shinox-v2-hero`. The Chinese homepage remains the English design master. The separate 5–20 bay planning image was already published in commit `3a4ef80`.

## Actual browser captures

| Width | Chinese | English |
| --- | --- | --- |
| 1440 | [Desktop](zh-1440.webp) | [Desktop](en-1440.webp) |
| 768 | [Tablet](zh-768.webp) | [Tablet](en-768.webp) |
| 390 | [Mobile](zh-390.webp) | [Mobile](en-390.webp) |

[Previous and updated website captures](before-after.webp) are labelled as such. This comparison is not a copy of the approved design image. The design references were visible inline in the conversation, but their original image files were not available in the filesystem; no pixel-diff against an original reference file is claimed.

## Visual review against the requested overlay composition

| Requested feature | Implementation and visual review |
| --- | --- |
| Background fusion | Owner-supplied architecture is an unframed, full-height background extending to the right edge. Left and bottom navy gradients blend it into the page. Added a top mask on tablet to remove the observed hard sky edge. |
| Text/image proportions | White 59px heading at 1440, 19px body, left reading measure; 31.2px heading and 16px body at 390. Both heading lines are white. |
| CTA hierarchy | 62px cyan/teal primary CTA and dark outline secondary CTA; real SVG play/arrow/external icons. |
| Three overlay cards | Three 24px-radius wide cards in one desktop row; full-card images, left gradient, selectable text, and actual circular link controls. Tablet/mobile stack while retaining overlays. |
| Accurate supplied subjects | Reused the owner's four independently uploaded images. The actual architecture, control cabinet and planning scene differ from the illustrative reference; no invented replacement equipment or fabricated logo was introduced. Globe toned toward titanium using scoped CSS. |

## Validation

- Chromium: Chinese/English at 1920, 1440, 1024, 768, 390 and 375px; four images decoded, no horizontal or text overflow, no page errors or failed requests.
- Real CTA and three card-link navigation, YouTube new tab with `window.opener === null`, hover elevation, keyboard focus, reduced-motion and reveal behavior passed. External YouTube content was intercepted for destination testing; no claim about third-party video playback.
- All other homepage sections have identical DOM to the previous committed homepage. Hero binary, poster, logos, form code/state, legal configuration, calculators and existing process component are unchanged (see `scope-checks.json`).
- `python scripts/build_english.py --check` passed with no drift across 25 page pairs.

## Changed implementation files

- `shinox-v2-site/index.html`, `en/index.html`: real overlay HTML, semantic links and icons.
- `shinox-v2-site/home-about.css`: all new styles scoped to `#about`.
- `shinox-v2-site/locales/en.json`, generated `en.js`: English labels and accessible names.
- Existing `home-about.js` retained for bounded parallax and progressive reveals.

## Separate pending uploads

- Brand mission block: the factory/manufacturer-logo image is visible inline but was not included in the uploaded planning ZIP. It has not been replaced.
- M9: the newly supplied empty-bay image differs from the existing M9-with-car CGI. The new original file is needed; the product hub and detail were not falsely marked complete.
