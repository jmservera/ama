---
title: Issue 2243 plan r4
ms.date: 2026-11-23
---

Tier FULL (src test change under src/api); no `rpi-checks.py`.

1. Add `test_question_path_follows_zf_demo_expires_at` to `src/api/tests/test_resident_aoai.py`.
2. Run `test_resident_aoai`, mypy, ruff.
3. Research note `issue-2243-live-r4-2026-11-23.md`, index and log entry.

## Critique (single pass)

Verdict: proceed. Test uses the existing fixtures, no new helpers. Risk: none to production code. Image roll is out of scope (firewalled registry); recorded as unproven.
