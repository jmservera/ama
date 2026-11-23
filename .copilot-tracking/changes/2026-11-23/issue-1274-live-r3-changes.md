---
title: Changes for issue 1274 live run 5
---

Implement start: edit tools/test_install_actionlint.py only (tools test, no src). Tier FOCUSED.

## Changes

* tools/test_install_actionlint.py: `WorkflowWiringTests` (2 tests); 14 tests OK, ruff and mypy --strict clean.
* docs/reference/research/issue-1274-live-evidence-2026-11-23-run5.md, README index, log.

## Per-criterion table

| Criterion | Verdict |
| --- | --- |
| 1 failing endpoints | Proven for actionlint (run 4 note); unproven for AWF and #1273 (logs not retained) |
| 2 bounded fail-closed retrieval | Proven (installer tests) |
| 3 focused regressions | Proven (14 OK) |
| 4 real verification and exact-head hosted CI | Proven for actionlint (run 4); unproven for AWF 0.28.23 and hosted CI (no push) |
| 5 resume route | Proven (#1275) |
