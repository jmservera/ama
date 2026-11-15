---
title: Issue 228 procurement and QA screens WCAG research
ms.date: 2026-11-14
---

## Scope

Issue #228 criterion: accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation. Stacked on PR #1639, base 8c943c9b1. Refs #228. Research disposition: executed (local source reading).

## Findings

* Screens live in `src/api/src/zava_forward/api/web/role-screens.js`: `procurement-packages`, `contractor-job-pack`, `quality-queue`.
* Tables already use `table-scroll` regions with `tabindex` 0, `role` region and an `aria-label`; a global `:focus-visible` rule exists in `style.css`. No pointer-only controls exist on these screens.
* Capacity headroom, defect state and handover sign-off were bare values or implied by headings. No insurance or certification expiry was shown anywhere; the package API supplies no such field, so expiry is rendered only from optional `insurance_expiry` and `certification_expiry` and otherwise reads Unknown.
* `test_accessibility_baseline.py` pins 8 `aria-invalid` sites and 13 tables; no new table or `aria-invalid` is needed (a definition list is used).

Planning Readiness: Ready. Whole-issue acceptance stays unproven: no assistive-technology or user evidence.
