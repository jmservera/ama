<!-- markdownlint-disable-file -->
---
title: Issue 146 details
description: details
ms.date: 2026-11-04
---

## Details

* `check_monitoring_declaration(declaration, task_enabled)` in `src/core/src/zava_forward/core/monitoring_coverage.py`.
* Six harm indicators need denominator, window and a constructed or named-human-approved threshold, or applicable False with a reason.
* Owners and manual-route status are returned for disabled tasks.
* Tests: `src/core/tests/test_monitoring_coverage.py` DeclarationTests (6 behavioural cases).
