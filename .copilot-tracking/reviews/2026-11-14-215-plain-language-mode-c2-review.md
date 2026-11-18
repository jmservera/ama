---
title: Issue 215 plain-language mode correction cycle 2 review
---

* Review executed once against the three blocking findings. Outcome: all three addressed; open items remain.
* Finding 1: the flag reaches the API and the reply gains `plain_summary` with unchanged `reply`, citations and provenance (`test_home_chat_api.py`, `test_regulatory_chat_api.py`). Finding 2: the mode toggle no longer touches the status paragraph (`test_accessibility_baseline.py`). Finding 3: the baseline sentence is corrected.
* Open items: the summary is fixed wording by outcome, not a model rewrite; no Playwright, screen-reader or staff comprehension evidence; `chat_fixture` import errors are environmental.
* Routed follow-up: run `checks/regulatory_ux_check.py` in a browser environment. No `aria-invalid` added; no push performed.
