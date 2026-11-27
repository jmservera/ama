# Issue 1837 research, 2026-11-27

Refs #1837. Synthetic demo, desktop only. Base `b64c6e95dd`.

## Status

The defect is fixed on main: `web/nomination-routes.js` converts the three standalone forms to JSON with the `X-ZF-CSRF` header. Earlier notes (2026-11-18 to 2026-11-25) cover the success journeys, urlencoded refusal, unauthenticated/contractor/array/cross-case refusals and trusted-proxy CSRF.

## Candidate angle

The script's failure branches have no browser test: a server rejection must show the server message in the `-feedback` element, move focus there, re-enable the submit button and write nothing; a network failure must show the offline message. Both are user-visible paths of the repaired transport.
