---
title: Issue 76 live changes 2026-11-19
ms.date: 2026-11-19
---

No source change. Only these RPI artifacts were added.

| Criterion | Status | Basis |
| --- | --- | --- |
| Default view is one list with one status and one next action | Ticked earlier, not reopened | Issue body |
| No perspective picker in user views | Ticked earlier, not reopened | Issue body |
| Queue with visible definitions | Ticked earlier, not reopened | Issue body |
| Blocked steps show reason, owner, next action | Ticked earlier, not reopened | Issue body |
| Hazard and safeguarding items show a clock and named owner | Unproven live; code and tests pass | Hazard: owner named, clock "Unknown" (no awareness timestamp) in the demo data; safeguarding: 0 demo items. 10 api tests and 29 core tests OK today. Live evidence from 2026-11-18 (docs/reference/research/issue-76-live-r2-2026-11-18.md). Fixing it needs demo data writes or a redeploy, outside the authorised scope. |
| Ownership, reason, unknowns agree across views (FR-034) | Ticked earlier, not reopened | Issue body |
| Single reset to default (FR-032) | Ticked earlier, not reopened | Issue body |

Commands: see the research note. Not run: mypy, ruff (no src change), complete gate, hosted CI.
