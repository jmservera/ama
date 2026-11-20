---
title: Review issue 1837 live
ms.date: 2026-11-20
---

Outcome: conformant for the test-only scope. Finding: the new test would pass for any 4xx cause, so the cross-case assertions are status-class only; acceptable as a no-write guard (state snapshot equality). Open: criteria 5 and 6, nomination_browser_check failure at nomination_review, CSRF header negative case.
