---
title: Issue 2243 plan r4
ms.date: 2026-11-23
---

Plan: add `expiry_configured()` to `assistant.py`; in `aoai.py` `_question` and `_answer` raise `AssistantUnavailable("expiry_not_set")` when the clock is past the expiry and the setting is not configured; add the `FALLBACK_REASONS` entry; test in `test_resident_aoai.py`. Details: `.copilot-tracking/details/2026-11-23-issue-2243-live-r4-details.md`.

Critique (one pass, executed): verdict approve. Risk: still fails closed, so no behaviour loosening. A configured-but-past date keeps "expired". The select() path in `assistant.py` is the topic-selector adapter and is left alone (not used by the resident chat). Tier FULL (src change); no `rpi-checks.py --all`.
