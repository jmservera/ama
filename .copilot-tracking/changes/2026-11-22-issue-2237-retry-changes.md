---
title: Issue 2237 retry changes
ms.date: 2026-11-22
---

Changed: docs/reference/research/issue-2237-retention-500-live-2026-11-22.md (retry section) and `retry-2026-11-22T21.json`. No source change; tier focused. Refs #2237.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce | Unproven | 56 of 56 live calls returned 200 on revision 0000053 |
| Find the cause in the demo container logs | Unproven | Current replica log holds no /api/retention error; older replica logs and Log Analytics are inaccessible |
| Fix with a regression test | Not applicable | No cause established; speculative fix rejected in critique |
| Re-prove 200 live | Proven for the demo employee account on revision 0000053 (role unconfirmed) | retry-2026-11-22T21.json |
