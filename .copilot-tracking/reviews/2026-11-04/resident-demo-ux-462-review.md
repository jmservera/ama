# Review: resident demo UX redesign, phase 1 (Refs #462)

Execution: executed once (self-review by the implementing agent; independent exact-head review still required).
Outcome: conformant for the slice, with open items routed below.

## Web-design-guidelines

Source fetched 2026-11-04 from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md. Changed files: `demo.js`, `demo.css`, `index.html`.

* Icon-only Account has `aria-label`; decorative SVG icons are `aria-hidden`. Pass.
* Async updates use `role=status` / `aria-live=polite` (`#status`, `#summary-status`). Pass.
* Sticky nav with `scroll-margin-top` on sections. Pass.
* Reduced motion: spinner static, smooth scroll only for no-preference. Pass.
* No `transition: all`, no external CDN, no `outline: none`. Pass.
* Guideline "Title Case for headings" is not applied: the repo plain-language content standard (sentence case) takes precedence.
* `touch-action: manipulation` not added; low value, routed as a follow-up.

## Not verified

Screen-reader testing, copy review (#153), resident usability (#155), live deployment, hosted CI, human approvals, complete local gate, AI-success summary in a browser.

## Routing

Later work: Phase 2 (sensors); human reviews above.

## Phase 2 review

Execution: executed once for phase 2 (self-review). Guidelines source refetched 2026-11-04 from the same URL. Changed web files: `demo.js`, `demo.css`.

* Forecast is distinguished by dash, marker shape and text, not colour alone. Pass.
* Accessible data table lists forecast rows with `Forecast (estimate)` text. Pass.
* Dates use `Intl.DateTimeFormat`; numbers use `Intl.NumberFormat`. Pass.
* Wording is descriptive, not diagnostic; ranges stated as display limits. Pass.

Not verified: T-SQL compile and live sensor data, Azure view apply, screen readers, visual review by a person (no screenshot reviewed), copy review (#153), usability (#155), hosted CI, human approvals.

Routing: owner-gated live view apply and sensor tables; extend sensor backfill past 2026-09-30.
