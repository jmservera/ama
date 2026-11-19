---
title: Issue 1274 audit changes
ms.date: 2026-11-18
---

Docs only; no source, workflow or test edits. Tier FOCUSED docs-only (no src change, no workflow, no gate-tool edit).

## Files

* `docs/reference/research/issue-1274-release-downloads-audit-live-2026-11-18.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)

## Per-criterion proven/unproven

| # | Status | Note |
| --- | --- | --- |
| 1 | Partly observed | 1243 run 42469282088 actionlint 504 observed; raw output not retained; 1271/1273 logs and AWF log not retrieved |
| 2 | Observed for actionlint (raw output not retained), not observed for AWF | installer code and 12 tests; AWF is upstream generated |
| 3 | Partly proven | 12 regressions pass; test_rpi_checks and compiler not re-run; none for AWF |
| 4 | Partly proven | real exact-version verification reproduced (exit 0, 1.7.7, lint 0); AWF scope open |
| 5 | Ticked, consistent | resume route in PR 1275 records |

## Validation

* installer unittest 12 OK; ruff format check 2 files formatted; mypy strict no issues; real installer exit 0; native workflow actionlint exit 0.
* Needed FULL-tier follow-up if code is required: AWF 0.28.23 bootstrap (gh-aw compiler/action upgrade or upstream retry).
