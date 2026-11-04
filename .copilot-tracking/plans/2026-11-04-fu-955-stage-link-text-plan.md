# Plan: issue 955 unique stage link text

Research: [research](../research/2026-11-04/fu-955-stage-link-text-research.md). Details: [details](../details/2026-11-04-fu-955-stage-link-text-details.md).

* [x] Phase 1: link text becomes `<stage>: <screen title>`; unlinked stages keep their plain text.
* [x] Phase 2: test that all stage links are distinct for both roles and that stages 3 and 7 are told apart.
* [x] Phase 3: focused tests, node syntax check, ruff, mypy; log entry.

Critique (single pass, self-run): use visible text (WCAG 2.5.3) rather than aria-label; keep href, order, deferral text and role gating unchanged. Applied.

Disclosure: web-design-guidelines source fetch and a full guideline review were not performed.
