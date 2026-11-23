---
title: Issue 1288 live research
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

* Main: `HEAD..origin/main` empty; HEAD `b11b8259bd`. Live revisions `ca-cutover-test-demo-api--0000054` and `ca-resident-demo--0000026`, 100 percent traffic.
* Focused tests from `src/api`: 92 OK, 9 skipped, 139 s (`.copilot-tracking/evidence/2026-11-23/issue-1288-live10/focused_tests.txt`).
* Live read-only probe (Playwright, Retrofit Programme Manager): seven of twelve homes `ok` with 12 readings, five `consent-withheld`; Home sensors panel and AI tab screenshots; all five assistants refused for the missing approved release record (OQ-017); forecast 200 (503/504 in r9 not reproduced); `rai-metrics` unchanged (`tokens` 0, `consumption` 0).
* No code gap found; criteria 4 and 8 depend on a human release approval. No Azure resource created.

Conclusion: criteria 3, 5, 6, 7 proven as local engineering evidence (6 also seen live); 4 and 8 unproven.
