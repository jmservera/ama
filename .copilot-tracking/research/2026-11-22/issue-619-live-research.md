---
title: Research for issue 619 live re-proof (2026-11-22)
ms.date: 2026-11-22
---

* Research disposition: executed (drift check) and reused (2026-11-18 note).
* Main head 3219004e90. Issue 619 carries #550 and #552 criteria; demo is desktop only; person-run AT, DPO and Legal are waived for the demo.
* Existing evidence: docs/reference/research/issue-619-live-at-consent-evidence-2026-11-18.md with drivers in .copilot-tracking/evidence/2026-11-18/issue-619-live/.
* Drift: web files changed since 2026-11-18 (staff case screen redesign #2161, chat agent routing #2199, others). The old axe, keyboard, reflow and consent results may no longer hold, so they need a re-run against the live apps.
* Gap: 200 percent text scaling was never run; only viewport equivalents were.
* Plan: re-run the existing drivers live, add a text-scaling probe, record a per-criterion table. No src change, so focused tier.
* Planning Readiness: Ready.
