---
title: Issue 350 live research r5 (2026-11-19)
description: Opening research for the first unmet demo criterion of issue 350
ms.date: 2026-11-19
---

Disposition: executed. Scope: synthetic demo, desktop, FOCUSED tier unless src changes. Brief: /tmp/brief-common-20261117T1730.md.

First unmet criterion: 1 (anonymous protected API returns 401 for browser-style requests while pages keep the Entra redirect). Prior notes: docs/reference/research/issue-350-live-2026-11-19.md. Hypothesis: the 302 comes from Easy Auth (`RedirectToLoginPage`) before the app sees the request, so the fix is edge configuration in infra, not src.
