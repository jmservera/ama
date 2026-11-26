---
title: Issue 2186 live research 2026-11-26
description: Opening research for the full-receipt relaxation gate, issue 2186
ms.date: 2026-11-26
---

Research disposition: executed (reuses the 2026-11-21 to 2026-11-23 evidence, then probes current main).

## Findings

* origin/main is 79937c1cc8. `base_relaxation(inert_only=True)` already relaxes full receipts for `.copilot-tracking/` and `support/`; `docs/` and markdown elsewhere are deliberately excluded because tests read them (`RECEIPT_INERT_PREFIXES`).
* 133 tests in `tools.test_rpi_checks` pass on this head.
* Probe of real history: the newest main move, cc7caafefb..79937c1cc8, touches only `.github/rubric/scores/latest.json`, which is not inert, so a full receipt dies on it. 29 of the first-parent commits since 2026-11-23 are `chore(rubric): record score` commits.
* Consumers of the score files: the rubric workflow and `.github/rubric/scripts/test_*.py` (not in the `rpi-checks.py` matrix) and a path string in `tools/rename-zava-tests.py` (`preserved()` only matches the string, never reads the file).
* `moved_path_blocker` returns "unmapped path would force the full matrix" for the path, so a prefix change alone is not enough.

## Planning Readiness

Ready: add `.github/rubric/scores/` as a receipt-inert prefix, short-circuit it in `moved_path_blocker`, add a test case.
