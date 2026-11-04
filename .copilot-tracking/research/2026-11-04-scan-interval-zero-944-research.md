---
title: Research for #944 zero scan_interval ZeroDivisionError
ms.date: 2026-11-04
---

* Task: fix/issue-944-followup, Refs #944 (review note from #915).
* Research disposition: executed (code read only).
* Prior delivery check: merged PR #915 added `Assistants.forecast`; no merged PR addresses #944.
* Finding: `Limits` stores a parsed `scan_interval` even when the bounds check marks the configuration invalid (valid requires 5..3600). `forecast` checks only `self.sql`, not `limits.valid`, so `ZF_ASSIST_SCAN_INTERVAL=0` reached `period_seconds // scan_interval` and raised ZeroDivisionError. A negative value gave a meaningless negative forecast.
* Planning Readiness: Ready.
