---
title: Changes, issue 1259 live run 7
ms.date: 2026-11-23
---

Planned: add docs/reference/research/2026-11-23-ranking-archive-unusable-1259-live-r7.md, an index row in docs/reference/README.md and a log.md entry. No src change; tier FOCUSED.

## Per-criterion status

| Criterion | Status |
| --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (ticked, local tests) |
| Unknown window and unreadable shape, no healthy-empty fallback | Proven (ticked, local tests) |
| Preserve absent first run and path-free diagnostics | Proven (ticked, local tests) |
| Regression tests plus failure before fix | Proven: 7 failures at cd687abadd^, 110 pass on main; stat failure is mocked |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven and owner/process-gated: no src change, nothing pushed |
| Live revisions 0000054 and 0000026 | Not applicable: ranking runner is an operator CLI, no ranking job deployed |
