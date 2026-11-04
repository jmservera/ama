# Plan: admin-only landing without 403s (Refs #920)

Slice 1 of 1 (smallest coherent; the issue's remaining criteria are covered by this slice for the known cases).

* [x] `/api/me` reports `services.cases` from `projection.allowed(u, "cases")`.
* [x] `app.js` shows a plain-language status page instead of calling `listView` when `services.cases` is false.
* [x] Unit test for the flag and the retained 403s; browser check asserts no 4xx and no console errors for the admin-only account.

Critique: executed once, self-review. Compatible. Rejected alternative: hiding the 403 in `api()`, which would mask real defects.
Boundaries: no change to authorisation; server still enforces 403. No AI feature touched. Tier: focused (no security, infra, SQL or deployment change).
