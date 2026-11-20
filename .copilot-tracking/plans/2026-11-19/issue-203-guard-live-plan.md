---
title: Issue 203 guard live plan
ms.date: 2026-11-19
---

Critique (once): proceed. Widen `RECORD_PATTERN` in `tools/check-legacy-references.py` to accept date-first issue notes (`DATE-issue-N-...`), add a test case in `tools/test_check_legacy_references.py`, run the checker and its tests, ruff format and check. Tier FOCUSED (tooling only, no gate semantics, workflow or src change; the checker is not a gate in rpi-checks). Out of scope: criterion 5.
