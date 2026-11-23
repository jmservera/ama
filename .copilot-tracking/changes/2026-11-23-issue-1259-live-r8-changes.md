---
title: Changes, issue 1259 live run 8
ms.date: 2026-11-23
---

Changed: src/core/tests/test_ranking_publication_runner.py (one real-permission test); docs/reference/research/2026-11-23-ranking-archive-unusable-1259-live-r8.md; docs/reference/README.md index row; docs/reference/log.md entry. Tier FULL for the src edit; `rpi-checks.py --all` not run (coordinator runs gates). No divergence from plan.

Validation: 111 tests OK; ruff check and format pass; mypy shows 3 pre-existing errors outside touched files.

## Per-criterion status

| Criterion | Status |
| --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (local tests incl. real permission denial) |
| Unknown window and unreadable shape, no healthy-empty fallback | Proven (local tests) |
| Preserve absent first run and path-free diagnostics | Proven (local tests) |
| Regression tests plus failure before fix | Proven: 7 failures plus new test fails at cd687abadd^, 111 pass |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven, process-gated: no push, no hosted run, no `--all` receipt |
| Live Azure proof | Not applicable: ranking runner is an operator CLI, no deployed job |
