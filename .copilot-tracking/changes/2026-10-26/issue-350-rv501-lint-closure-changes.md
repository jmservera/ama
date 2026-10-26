<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-501 lint closure changes
description: Changes record for the coordinator-named targeted static closure
ms.date: 2026-10-26
---

Closure named and attributed by the coordinator after its independent read of d4f19c70 to a93bcf8e and its own 88-test run. Prospective note: `plans/2026-10-26/issue-350-rv501-lint-closure-operation-note.md`, written before the edit. No new research, critique or review was run, as the coordinator directed; the original Non-conformant reviews (RV-501, RV-601, RV-602) are unchanged and not relabelled.

Changes, `tools/test_check_demo_feedback.py` only, no behaviour change: `ruff --fix` removed the unused `ledger` import (F401) and replaced `lru_cache(maxsize=None)` with `functools.cache` (UP033); four docstrings and two long lines were shortened by hand (E501); `ruff format` at the file's established width 88 reflowed my introduced lines and one pre-existing import block. Width 100 was not used for formatting because it would reflow about 40 unrelated pre-existing hunks.

Results: `ruff check --isolated --no-cache --select E,F,I,B,UP --target-version py312 --line-length 100` passes (9 violations before); `ruff format --isolated --check` (width 88) passes; `PYTHONDONTWRITEBYTECODE=1 /home/azureuser/rehearsal-350/venv/bin/python -m unittest tools.test_check_demo_feedback` gives 88 OK. Ruff came from the existing `/mnt/ama-rpi-gates/issue462-helper-correction1/venv`; no environment was changed. No gate, push or live action; a later gate uses `--lock-timeout 0`.
