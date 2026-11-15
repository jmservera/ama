---
title: Safety screens WCAG textual state and keyboard research
ms.date: 2026-11-14
---

Issue #227 (stacked on #1639, base c9d4204029692886e26fdf56011c25d2fd180e1a), unmet criterion: accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation.

Research disposition: executed. Planning readiness: Ready.

Findings in src/api/src/zava_forward/api/web/role-screens.js (hazardScreen, hazardQueue):

* Severity (priority), source and referral steps were already text.
* Gaps: SLA clock showed only a bare timestamp; stop-work status lacked an explicit label; state was a bare value; the screen sections had no keyboard jump route.
* Global :focus-visible (style.css) and the skip link (index.html) already exist.
* test_safety_screens forbids buttons, so jump links must be anchors.
* No aria-invalid and no extra [role=status] inside #regulatory-alerts are involved.
