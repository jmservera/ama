---
title: Research for issue 619 automated accessibility slice
ms.date: 2026-11-03
---

## Disposition

Research disposition: reused (2026-11-02 research) plus executed gap check. Planning Readiness: Ready.

## Evidence

* Merged PR #760 delivered the human protocol and blank record. No merged PR delivered automated checks on a production configuration.
* Existing axe and keyboard checks (`case_view_ux_browser_check`, `chat_widget_browser_check`) run only with `ZF_ENV=development` and the shared-password provider. Production refuses that provider (`auth.make_provider`), so no automated accessibility evidence existed for the production configuration.
* Owner decision 2026-11-03: deliver automated axe and keyboard checks now; leave the manual assistive-technology criterion open until a production build exists. Use Refs.

## Slice

Add a check that starts the employee site with `ZF_ENV=production`, trusted-proxy auth and a synthetic principal header, then runs pinned axe-core and keyboard checks on the case view and employee chat widget. Resident site, zoom and consent stay unmet.
