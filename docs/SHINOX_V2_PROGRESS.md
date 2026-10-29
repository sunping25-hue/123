# ShinoX V2 implementation report — 2026-10-28

This report describes implemented source and verified behavior, not production completion.

## Implemented and reviewed
- Approved original Hero MP4, poster, three official logos, unchanged binary files.
- Responsive Chinese homepage: seven approved primary navigation items, language/download links, three product categories and fifteen working product routes.
- Five original AI concept images (432×724 WebP, ~227KB total); click, swipe and keyboard tabs. These are abstract conceptual CGI, not real equipment photos.
- Fifteen differentiated product pages, four extended product topics, related links, phone/email/WhatsApp inquiry routes.
- Chinese brand/business content, planning process, honest pending news/cases/download states.
- English export landing with translated product list and international contact; Chinese detail-page links explicitly labeled.
- Original poster fallback, paused video under reduced-motion, save-data/2G fallback and manual video playback controls.
- Local preview server with media byte ranges, validated SQLite inquiry/request persistence, consent, origin checks and rate limits. Never sends email or confirms bookings.
- Privacy notice, separate service consent (no marketing opt-in), 404 page, unique page titles/descriptions, preview noindex.

## Verification
- Chromium: 1440×900, 768×1024, 390×844 homepage. All five images load; all 15 product links return 200; no horizontal overflow, JS errors or HTTP errors. Mobile navigation opens/closes.
- Keyboard element tabs, single visible panel, product representative pages and English/privacy responsive checks passed.
- Reduced-motion: homepage does not request the video; poster remains visible.
- Seven Python HTTP integration tests pass: validation, consent, persistence, request-not-booking-confirmation, cross-origin rejection, rate limit, media byte ranges.
- Previous build verified video loop restart; human review of visual loop seam remains pending.

## Still pending / required source inputs
- Actual product CGI requires approved reference images; current abstract CGI is not a product rendering.
- Verified product specifications, product DM, startup PDF and real authorized news/cases.
- Email provider, business notification, actual demonstration locations/availability/confirmation backend, privacy review, unsubscribe and consented campaigns.
- English product detail pages and complete per-page international SEO; production domain is not yet configured.
- Mobile-specific video encode, physical iOS/Android review, Core Web Vitals and low-speed network review.
- User-accessible remote preview requires separately authorized hosting; localhost is not a delivered remote preview.

Production site and main remain untouched. Review source is kept on shinox-v2-hero; no automatic production deployment configured.

Remote changes through 1229321 were merged without overwriting project instructions. The reusable navy / electric blue / teal / titanium-silver material tokens now follow the newly approved below-Hero palette. Original Hero files are unchanged.

Final browser checks: actual Hero video loop restart passed on desktop and mobile (waited for playback after seek, not a fixed sleep); playback control and fixed LINE button do not overlap. Form browser submission with synthetic preview data persisted and displayed the explicit local-only / not-notified response. All five official media files compared byte-for-byte equal to the user's original ZIP. Review screenshots are in docs/review/.

## Next milestone — 2026-10-29 (Taiwan)
- Added all 15 English product detail pages with translated inquiry preparation and matching Chinese/English product switches. All 30 detail pages have paired language metadata and preview noindex.
- Derived a 960×548 / 24fps H.264 mobile rendition (~2.7MB, ~79% smaller) from the approved original, whose binary is unchanged. Shared playback controller selects one rendition on initial load; no duplicate desktop download on mobile.
- Chinese and English homepage both avoid video requests under reduced-motion, data saver or 2G; manual play remains available.
- Fixed actual custom 404 rendering, HEAD/Range edge cases, cache policies and malformed origin validation. Local service now has 12 passing integration checks.
- Aligned form maxlength and server error messages; documented that 30-day local test retention is purged at server startup.
- Browser acceptance checks are saved as tests/browser_review.py: six homepage language/viewport combinations, video source selection/loop, product links, plus both language motion/data-saver checks.
- User subsequently authorized publishing an independent private review Site. Existing production and main remain unchanged. Static publication excludes local database and Python runtime; inquiry submission remains unavailable on the hosted review, with direct phone/email/WhatsApp contact available.

Independent owner-private review Site was successfully published after explicit authorization: https://shinox-v2-review.wld-wash.chatgpt.site . See docs/REVIEW_SITE.md for deployment provenance. This supersedes the earlier remote-preview blocker; original ShinoX production/main remain unchanged.

## Shared bilingual UI, six-stage process and official YouTube — 2026-10-29

This milestone supersedes the older English-layout and remote-preview blockers above; it does not declare the whole master plan finished.

- Traditional Chinese is now the sole design master. All 24 English routes are generated from it with shared CSS, JavaScript, SVGs and media, professional display translations and corresponding-page language switches. Removed unused separate English theme files. Generation fails on missing translations or stale output.
- Shared titanium/dark-glass controls establish primary, secondary, navigation, tab, card and functional levels, one-shot edge highlights, 2px hover lift, press/focus/disabled states and reduced-motion support. SVG arrows fix missing English symbol glyphs; related-product cards reserve space for longer titles.
- Added actual six-stage HTML/SVG process before the business consultation CTA: detailed selectable tabs, previous/next, keyboard navigation, mobile horizontal scrolling, optional six-second auto display, visibility pause and motion preference handling. Heading is white.
- Official YouTube is centralized at `https://www.youtube.com/@ShinoXwash`: one deduplicated footer button per page, a homepage brand video button and a business-process video button. Real anchors, red play SVG, dark-glass/silver material, focus, touch and external-tab semantics are shared in both languages.
- No specific product video has been supplied/confirmed. Product video registry remains empty; machine-specific video CTAs are intentionally absent. Existing LINE, WhatsApp and calculator destinations/password logic are retained.
- Acceptance: 96 browser page/viewport combinations (24 pairs at 1440/390), identical static body structure, resolved local assets/anchors, no broken images/horizontal overflow/JS errors, 44 paired main/product screenshots. Interaction matrix passed 1440/768/390/375 in both languages; normal hover is 2px up and arrow 3px up/right. Reduced-motion change stops auto presentation.
- Evidence and repeatable checks: `docs/BILINGUAL_UI.md`, `docs/review/bilingual-ui/README.md`, browser QA JSON and scripts. Native publishing status and current source provenance are recorded in GitHub Issue #2 after publication.

Still requires owner-provided/verified product imagery/specifications/DM, authorized news/cases and production email/booking integrations. The private static review has direct contact alternatives and does not send emails or confirm bookings. Existing ShinoX production and main remain untouched.

Follow-up synchronization: fast-forwarded owner commits through `20cdc4b`, consolidated the duplicate six-stage insertion into the existing accessible shared component, and preserved removal of the old three-step block. Regenerated English and refreshed the business-page comparison screenshots.

## 2026-10-29｜共用雙流程、政策及資源封面

- 品牌／事業完整原文與產品／案例導言已更新，英文同步；前批提交8f76f89。
- 保留原本六階段橫向流程，並在「正在規劃5–20格」旁新增同一元件的3×2排版。桌機左文案右流程；手機上下排列。HTML內容只維護一份，複製元件自動分配獨立ID與ARIA，兩處互動狀態獨立。深色純底、亮青藍漸層、800／700／500字重及柔光，沒有水花背景。手機／平板控制鈕預留右側，避免浮動聯絡鈕遮住操作。
- 兩張使用者上傳的創業指南／產品DM封面已上架首頁與聯絡頁資源區，中文英文同檔。沒有提供PDF，文件仍顯示編製狀態。
- 建立真正獨立的/privacy、/terms及英文頁，保留.html入口；全站法律頁尾、可閱讀的長文與目錄。
- 依實際程式說明SQLite、SMTP、sessionStorage與外部服務；公司／營運者、權利窗口、正式資料庫／Email／備份保留規則仍待確認，未假造資料或認證。
- 政策及表單未驗收，legal-config reviewAccepted=false。正式與一般預覽API預設拒絕收件；只有合成資料單元測試明確開放測試模式。表單不預勾選、不含行銷訂閱，驗收後的程式會記錄政策版本及瀏覽器／伺服器確認時間。
- 25組中英結構／資源檢查、24項Python合成測試與60筆瀏覽器驗收通過，另補驗雙流程控制鈕及最終截圖。證據：docs/review/legal-resources-shared-process/README.md。

尚未開放正式個資收件、真實寄信或即時預約。私人靜態驗收站發布結果另記Issue #2；未變更main、舊站或正式ShinoX網站。
