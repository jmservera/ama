---
title: 891 c1 changes
---

* src/api/tests/test_ai_consumption_api.py: fallback modes now assert one settled ineligible output joined to the root, unjoined_outputs unchanged, cost Unknown; provider-failure keeps unknown_liabilities 1 and coverage incomplete.
* Validation: test_ai_consumption_api (37 OK), test_chat_panel, test_chat_widget_focus, test_content_standard OK; no agents test_consumption exists, core test_ai_consumption OK; ruff check/format and mypy clean.
