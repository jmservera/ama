---
title: Changes for issue 1258 run 3
ms.date: 2026-11-18
---

No `src` change; tier FOCUSED. Added the note `docs/reference/research/issue-1258-live-r3-2026-11-18.md` with raw evidence, plus index and log entries.

Validation: Core ranking tests 110 OK; API wiring 36 OK; mypy `src/core` clean; ruff format/check clean. `rpi-checks.py --all` not run (FULL tier not triggered).

| Criterion | Status |
| --- | --- |
| 1 Sync ancestors before confirm | Proven (real ext4 strace) |
| 2 Post-link failure `committed_unconfirmed` | Proven (injected EIO) |
| 3 Regression tests, red before fix | Proven offline; pre-fix raw log not retained |
| 4 Retry, stage, audit, 409/503, date | Proven offline |
| 5 FULL receipt, independent review, hosted CI | Unproven; human/CI gates, not provable for the demo |
