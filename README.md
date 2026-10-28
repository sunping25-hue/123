# ShinoX V2 review build

Development branch: `shinox-v2-hero`. Existing `main` and the old website are preserved.
Read `AGENTS.md`, `docs/SHINOX_V2_MASTER_PLAN.md` and `docs/SHINOX_V2_PROGRESS.md`.

## See the site

For a static local review, open `shinox-v2-site/index.html` in a browser. All official media and visual assets are included. Static review does not send forms.

For local form and media-range testing, run `python server.py --host 127.0.0.1 --port 3004` and open `http://127.0.0.1:3004` **on the same computer**. This is not an Internet preview URL.

Read `docs/PREVIEW_RUNTIME.md` before testing request storage. Use synthetic data only. No email is sent and no appointment is confirmed. The local database is outside this repository and is never published.

## Validate

`python -m unittest discover -s tests -v`

This is a review build, not a production release. Specifications, real product CGI, verified case studies, PDFs, email delivery, confirmed reservations and marketing automation remain pending. No production deployment or main-branch merge is authorized by this source push.

## Browser acceptance review

With Playwright Python + Chromium available, run `python tests/browser_review.py --origin http://127.0.0.1:3005 --output /tmp/shinox-review` against a running local server. This checks both languages at desktop/tablet/mobile widths, approved/compact video selection, loop restart, product routes, reduced-motion and data-saver behavior. It writes only screenshots; no contact data is submitted.
