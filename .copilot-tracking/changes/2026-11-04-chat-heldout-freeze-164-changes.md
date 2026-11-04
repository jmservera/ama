<!-- markdownlint-disable-file -->
---
title: Issue 164 held-out freeze gate changes
description: Files changed and validation
ms.date: 2026-11-04
---

## Changes

* Added `src/agents/src/zava_forward/agents/chat_heldout.py` and `src/agents/tests/test_chat_heldout.py` (9 behavioural tests using a constructed, non-independent fixture).
* Validation run: `python3 -m unittest tests.test_chat_heldout tests.test_chat_eval` (48 passed), ruff check, ruff format, mypy with `--cache-dir=/tmp/mypy-164`.
* Not run: the gate, benchmarks, full suites, hosted CI.
* Unmet criteria after this slice: held-out set produced and independently labelled; memory poisoning and injection pass before enablement with actual-model evidence; thresholds approved by the owner and reviewer decision; human exercises; owner-authorised actual calls. The gate is a precondition only and ticks none of them.
