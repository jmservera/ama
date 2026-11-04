---
title: Changes - client-side proof for hidden callback form (#1053)
ms.date: 2026-11-04
---

* Added `src/api/tests/test_resident_callbacks_page.py` (2 tests).
* Validation run: the new tests, test_resident_demo_api, test_resident_chat_api (96 OK); ruff check and format; mypy with --cache-dir=/tmp/mypy-530 reports 4 errors only in tests/test_ai_consumption_api.py (missing zava_forward.agents.dispatch in this environment's installed agents package; not touched here), none in the new file.
* Not run: RPI gate, full suites, benchmarks, browser or live checks.
