# Independent ShinoX V2 private review Site

User authorized publication of this independent review Site on 2026-10-29 (Asia/Taipei). This is not a replacement for the existing ShinoX website or a main-branch release.

- Live review: https://shinox-v2-review.wld-wash.chatgpt.site
- Audience: owner-private; sign in with the ChatGPT account that owns this Site.
- Site ID: `appgprj_6ae21e864ea88191907e0e9a616cb369`
- Successful deployment: `appgdep_6ae21f9de8ec8191892d6bfcfdf7643e`
- Saved version: `appgprj_6ae21e864ea88191907e0e9a616cb369~appgver_7391b8eb00948191a28c2e3029bfed6c`
- GitHub implementation source: `d66fb8dcc8b06f48a1a3af30e8f4b9ba17d02236` on `shinox-v2-hero`.
- Site source commit: `21d3ba2efa2a7cef9f4ca5bcc9e858e71ce2e0d8`.
- Separate Site checkout: `/workspace/sites/shinox-v2-review`; it owns `.openai/hosting.json`. Do not register a new Site on subsequent edits.

## Scope

The published output is the static `shinox-v2-site/` review build, plus absolute preview-only OG metadata. It includes the approved original Hero, a derived mobile rendition, original logos, five conceptual CGI images, Chinese/English homepages and 30 paired product-detail pages.

No local database, contact records, Python runtime or credentials are packaged. Static `/api/status` explicitly reports persistence unavailable; the hosted form stays disabled with direct phone, email and WhatsApp contact offered. It does not send email or confirm bookings.

Publication was confirmed by the native Sites deployment result (`status: succeeded`). Existing ShinoX production, main and the old website were not modified. Preserve the private audience on future updates unless the user requests otherwise.

## Packaging note

The official Sites scripts were not installed and their bundle download was denied by environment policy even after the supported permissions request. The static publication therefore used the native tool's supported deployment archive contract: exact pushed Site source SHA, `.openai/hosting.json` and `dist/` in a tar archive. The credential was passed through hidden stdin and process-scoped Git configuration, never stored in source or logs.
