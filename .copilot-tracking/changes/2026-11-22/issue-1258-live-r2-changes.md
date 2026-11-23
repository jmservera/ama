---
title: Issue 1258 live changes r2
ms.date: 2026-11-22
---

No source change. Tier: focused (docs and evidence only; basis: no `src`, workflow, dependency or infra file touched). Added the research note `docs/reference/research/ranking-archive-ancestor-durability-live-r7-2026-11-22.md`, raw outputs under `docs/reference/research/issue-1258-live-r7-2026-11-22/` and RPI artifacts. Live Azure not used; no resource created.

| Criterion | Status | Basis |
| --- | --- | --- |
| AC1 sync newly created ancestors before confirming | Proven (ticked) | strace order: linkat, then fsync of archive and every ancestor; 110 tests OK |
| AC2 post-link sync failure is committed_unconfirmed | Proven by mocked tests (ticked) | publication tests pass at this head; no real crash |
| AC3 syscall-order regression, red before fix | Partly proven | tests exist and pass; the pre-fix failure was not re-run here |
| AC4 retry, stage, audit, 409/503, original date intact | Proven by tests (ticked) | runner and publication suites OK |
| AC5 original RPI | Proven | dated artifacts in this commit |
| AC5 current FULL receipt and verification | Unproven | no src change; full gate barred for this worker |
| AC5 independent exact-head review | Unproven | needs a separate reviewer of the exact head |
| AC5 hosted checks | Unproven | no push or PR allowed |
| Real crash or live filesystem claim | Not claimed | mocks and one local strace only |
