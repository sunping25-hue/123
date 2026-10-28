# ShinoX V2.0 — Codex instructions

Before any work, read `docs/SHINOX_V2_MASTER_PLAN.md` fully. That document is the agreed project brief, not a statement that features are already complete. Use the installed `design-taste-frontend` skill if available, while prioritizing the approved ShinoX direction.

- Work on `shinox-v2-hero` (or an isolated feature branch); never overwrite `main`, the old site or production without explicit authorization.
- The newest user-uploaded 2K MP4 **replaces** the original Hero video. Use the real binary at `media/shinox-hero.mp4`; if missing, explicitly report this. Never silently substitute older media or an AI-generated image.
- Use the exact user-provided official ShinoX logo files; product reference photos are only for understanding equipment shapes and CGI modeling, not direct marketing assets.
- Primary language Traditional Chinese (Taiwan); English export version planned.
- Do not invent specifications, prices, certificates, return projections, case studies, clients or real-time booking slots.
- Check responsive desktop/tablet/mobile preview, autoplay muted playsinline playback, real loop seams, contrast, reduced-motion, page speed, accessible navigation and SEO.
- Critical contact, booking, PDF and email features require actual integrations and tests; never call placeholders complete.
- Provide preview and report test results before any production release. Commit work to a branch and use PR review.

Implementation order: verify assets and existing code; finish Hero; five-elements interactive display; product hub and details; company/entrepreneurship/news/cases/contact; real lead conversion and reservation backend; multilingual and SEO; QA and deployment.

Planning Sheet: https://docs.google.com/spreadsheets/d/1OQnL9o2kBJB9Nz5WMijnB-LU818IIajJMCm401JlJ04/edit

## Landing-page visual asset rules (new)
- **All non-Hero landing-page gallery visuals, illustrations and other relevant visual assets belong in `lassets/`.** Read `lassets/README.md` before image creation or implementation.
- Replace non-Hero imagery with original AI-generated illustrations matching each section's meaning and ShinoX's approved deep-navy / electric-blue / cyan / teal / titanium-silver cinematic CGI direction.
- **Hero exclusion**: keep the user-approved Hero MP4, poster and official ShinoX logos intact; never replace or regenerate these under this asset task.
- The current landing page has no existing non-Hero image gallery yet. Add deliberate section images as part of redesign; do not falsely claim replacement of images that never existed.
- Product/device CGI must faithfully follow approved reference photos, not invented mechanical shapes. No synthetic project photos presented as real case studies.
- Commit generated optimized assets and their actual usage together; verify all image paths resolve, add descriptive alt text and lazy loading for below-fold artwork.
- If executing in Codex Plan mode, review the asset inventory and provide an implementation plan before making changes.


## Required color/material balance — approved visual reference
The user explicitly noted that earlier page mockups underused **teal-green and titanium/silver metallic surfaces** relative to the approved Hero reference. Correct this across all below-Hero illustrations and UI, not by changing the approved Hero itself.
- Visual-emphasis target **45% electric blue (#087CFF), 25% teal/turquoise (#17DDC7), 30% titanium silver/chrome (#C8D7E6 with metallic gradients)** among lit CGI subjects. This is a design guideline **for focal visual subjects**, NOT a whole-page pixel quota. Dark navy/near-black remains the dominant background.
- Make titanium silver tangible and prominent on turbines, machined edges, product enclosures and mechanical structures; use physically plausible glossy gradients and highlights.
- Make luminous teal streams clearly visible next to electric-blue water and energy ribbons. Avoid monochromatic cobalt-blue pages.
- Implement a reusable token set for navy, electric blue, teal, silver, and surface/highlight gradients; check all non-Hero visuals for this palette.
- The last user-provided Hero reference image is the **color/material benchmark**. Preserve its right-side crystalline turbine, visible teal streams, chrome surfaces, luminous flowing water.


## Visual rhythm correction — approved design direction (2026-10-29)
**Important: Do NOT render every image with splashing water, bright cyan/blue, equal contrast and equally dramatic effects.** The user explicitly rejected visual fatigue, monotonous palettes and constant maximum-intensity CGI. The previous 45/25/30 blue/teal/silver focal-color ratio is NOT a per-image requirement. It only describes the available brand palette across the experience.

- Think like premium editorial/art direction: vary brightness, negative space, crop, subject scale, backgrounds, materials and visual density between sections. Establish a quiet → dramatic → quiet rhythm.
- Reserve intense water vortex/splash and dynamic electric-blue + teal energy for **Hero** and select **Water/technology** demonstrations. No arbitrary splashes around control cabinets, brand offices, articles, contact forms or unrelated product cards.
- Give individual sections their own dominant visual character:
  - Hero: approved maximal cinematic electric-blue/teal water, crystalline metallic turbine; **do not change provided movie**.
  - About: spacious architectural graphite/titanium silver, soft directional daylight, calm credible enterprise mood, minimal or no water.
  - News: editorial grid, off-white/light steel-gray or charcoal breathing spaces, real product-related documentary composition, no synthetic fake article thumbnails.
  - Product hub: neutral studio silver machinery, light/dark alternating cards, honest product forms, subtle teal highlight only; accurate device CGI needs user-provided reference.
  - Business: natural architectural daylight/dusk, realistic concrete/steel/site-planning, warm practical lighting; CGI clearly illustrative, not claimed as built case.
  - Projects: restrained documentary presentation of authenticated projects only; do not invent completed client sites.
  - Contact: clean low-contrast, legible minimalist layout, cream/steel-gray or deep-charcoal alternating panel, almost no visual effects.
  - Five elements: Metal=brushed chrome cool-neutral; Energy=limited amber/blue electric glow; Air=soft translucent pale neutral; Water=blue hydraulic fluid; Fluid=teal translucent chemical liquid. The element names remain **Metal, Energy, Air, Water, Fluid** (NOT classical wood/fire/earth).
- Page should alternate **dark / midtone / light** sections when appropriate; most images must have 1 focal subject, lower visual complexity, ample text-safe negative space. Use color and contrast with purpose, not everywhere.
- Maintain unified typography, spacing, geometry and brand identity **without** making every illustration look like the same CGI scene.
- Before generating, write a shot list describing for each image: purpose, unique subject, dominant color/material, brightness, lighting, composition, amount of water (none/subtle/intense), and page placement. Check contact sheet for repetition; reject duplicate water-splash motifs.
- Images are content assets, not finished website screenshots. Don't fabricate site metrics, news headlines, real-world case studies or exact brand/product shapes.


## Approved seven-page visual reference (latest owner decision)
The latest owner-approved board is the **seven-page dark-navy ShinoX storyboard** shown in the ChatGPT conversation (2026-10-29) with panels: Home, About ShinoX, News, Products, Business Solutions, Projects, Contact. The board uses deep navy/black base, rich electric-blue and teal accents, real-looking titanium hardware, crisp card grids, dark cinematic art direction and restrained water splashes. This board supersedes later off-white/light-themed redesigns. Use this as the **layout/art-direction target**, not as evidence of real buildings, product shapes, company metrics, news, launch dates or customer projects.
- Home Hero: preserve latest user-approved real MP4 and official logo; no regeneration.
- Other page artwork: produce separate authentic image assets, not screenshots cut from the collage. Place files in lassets; ensure appropriate variation in intensity so all images aren't splash-heavy.
- Five elements must be Metal, Energy, Air, Water, Fluid (NOT classical Water/Metal/Wood/Fire/Earth as shown on the inspiration board).
- All example performance statistics, projects, article dates, and equipment renders in the inspiration board are conceptual and require verified material before publication.
- Implementation acceptance: real images loaded from lassets, desktop/mobile preview screenshots, no broken assets, deployment preview URL, successful QA. Never mark complete based on screenshot mockups or merely pushing docs.

## Investment calculators and homepage entry popup (approved feature)
- On **first entry to the ShinoX homepage in a browser tab**, show a dismissible promotional dialog with two options: 自助洗車場投資獲利試算 → https://shinox.ai.studio ; 水刀洗車店投資獲利試算 → https://service-carwasher-360.ai.studio. Do not force the whole official site behind a password.
- On selecting a calculator, open a second dialog saying **「請聯絡業務索取密碼登入」**. Current preliminary default access code is set by owner, but **do not print it as page text**. It is a client-side convenience gate, NOT security; secure the actual calculator destinations with server-side authentication if private access is required.
- Business page and homepage business section also contain the two calculator buttons; entry popup must be dismissible (close/ESC/outside/later) and shown once per browser tab via sessionStorage. Ensure keyboard and mobile support.
- Static implementation: `shinox-v2-site/calculator-gate.js`, `calculator-gate.css`, `calculator-welcome.js`, plus markup in homepage/business pages. Check actual published deployment; GitHub commit alone does not prove public site update.
