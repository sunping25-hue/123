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
