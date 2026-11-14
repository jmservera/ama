---
title: Epic 149 landmarks, skip link and focus order changes
ms.date: 2026-11-14
---

* Added `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` (14 tests, passing with `test_accessibility_baseline`, 27 total).
* Validation: unittest, ruff check, ruff format --check and mypy clean. Hosted CI not observed; nothing pushed.
* Divergence: no `TestClient` exists, so pages are fetched from a local `ThreadingHTTPServer`.
* Open: `/` and `/law.html` lack a skip link and nav (recorded gaps). Epic #149 criteria stay unmet (`Refs #149` only).
