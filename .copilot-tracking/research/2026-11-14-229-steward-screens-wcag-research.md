---
title: Issue 229 steward and operator screens WCAG slice research
ms.date: 2026-11-14
---

* Criterion: `Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation`. Stacked on PR #1639 (base `c9d4204029692886e26fdf56011c25d2fd180e1a`). `Refs #229`.
* Screen: `data-operator` in `src/api/src/zava_forward/api/web/role-screens.js`, with the exception register contract from `/api/exceptions`.
* Existing: tables sit in focusable named regions with captions; quarantined and fallback AI rows are written distinctly. No panel showed lineage freshness, sensor feed health or AI task enabled state, and no contract field supplies them.
* Constraints: `test_accessibility_baseline` audits `aria-invalid` sites (add none); `#regulatory-alerts` allows one `[role=status]` (add none).
* Planning Readiness: Ready. Research disposition: executed (code inspection only; desk hypothesis, not observed behaviour).
