---
title: Issue 572 post-#757 verification details
ms.date: 2026-11-03
---

Phase 1: python3 -m unittest tools.test_rpi_checks. Phase 2: ruff on touched files and mypy with --cache-dir=/tmp/mypy-572 on src/core/tests/test_chat_case_answers.py with MYPYPATH=src/core/src. Phase 3: artifacts, state, commit, PR.
