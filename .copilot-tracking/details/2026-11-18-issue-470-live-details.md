---
title: Issue 470 live audit details
ms.date: 2026-11-18
---

* Phase 1: `python3 -m unittest tools.test_rpi_checks -q` (109 tests) is the only command; nothing heavy.
* Phase 2: files touched: the audit note, `docs/reference/README.md`, `docs/reference/log.md`.
* Phase 3: AC4 reasons: brief forbids `--all`; only prior full attempt failed (exit 124); changed tier is not comparable.
