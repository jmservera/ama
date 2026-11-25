---
title: Issue 1844 live r9 plan
description: Add a browser-free regression test pinning the narrow-width map summary rule
ms.date: 2026-11-25
---

* Research: harness 436 PASS and live probe on revision 0000072 (see research note).
* Implement: add `src/api/tests/test_map_home_card_narrow_layout.py` (no browser) asserting the base card is absolute, the max-width 600px rule makes it static with auto width, and the expanded dialog keeps a static card.
* Tier: Focused (test only; no src, auth, SQL, infra or dependency change).
* Validate: new test, test_accessibility_baseline, test_content_standard, ruff, mypy.
