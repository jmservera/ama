# Plan: regulatory alerts and home chat WCAG 2.2 AA (Issue #215 AC3)

Date: 2026-11-14. Research: [research](../research/2026-11-14-regulatory-alerts-wcag-215-research.md).

* [x] Phase 1: add `regulatoryStateLabel` so the visible status word is always a known state (`chat.js`).
* [x] Phase 2: add an always-visible per-alert `Plain-language summary` (status, safe action, decision owner) and `aria-labelledby` naming each alert article.
* [x] Phase 3: add and update unit tests in `src/api/tests`; run focused tests and ruff.

Critique: executed once on the final candidate; compatible, no conflicts. Constraints: no `role-screens.js`, no push, no new dependency.
