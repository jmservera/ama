---
title: Issue 212 per-scope precision details
description: Step details
ms.date: 2026-11-03
---

* Step 1: replace `_precision_by_card` with `_precision_by(visible, field)`; `by_card` keeps its shape.
* Step 2: add `by_home_scope` keyed by `home_scope`.
* Step 3: test totals sum to `total` and false positives sum to 1.
* Step 4: README row mentions `by_home_scope`.
