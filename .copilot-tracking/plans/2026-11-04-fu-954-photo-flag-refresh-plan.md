# Plan: issue 954 photo flag refresh

Research: [research](../research/2026-11-04/fu-954-photo-flag-refresh-research.md). Details: [details](../details/2026-11-04-fu-954-photo-flag-refresh-details.md).

* [x] Phase 1: `recheckPhotoService` on tab return (throttled), flag flip on 503/403, reload photo when the flag turns true or a previous load failed.
* [x] Phase 2: node-executed regression test of the real `app.js` functions.
* [x] Phase 3: focused tests, node syntax check, ruff, mypy; log entry.

Critique (single pass, self-run): keep initials fallback and status text (non-colour signal, plain language); no new controls so WCAG surface is unchanged; throttle to avoid traffic; do not call the photo endpoint while the flag is false. Applied.

Web guidance disclosure: web-design-guidelines source fetch and a full review of rule list were not performed in this session; no markup or style changed, only status text timing logic.
