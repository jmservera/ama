---
title: Critique of the currency plan for the process race tests (#107, C10)
description: One independent critique executed before the main merge, with dispositions
ms.date: 2026-11-08
---

Execution: one read-only rubber-duck pass over the [currency research and plan](../research/2026-11-08-assistant-process-races-107-currency-research.md). Verdict: Revise. This is the only critique for the task; the 2026-11-07 critique is preserved unchanged.

* Finding 1, blocking, accepted: an optional `--extra-test` selector would run without `ZF_TEST_MSSQL=1` and skip, and the runner rejects integration skips (`tools/rpi-checks.py` lines 1475 and 2528 per the reviewer). The plan text was amended before commit to drop it and to require the two `Mssql...` method lines as `ok` in the runner's SQL log.
* Finding 2, verified: PR 1216 is unrelated; main did not change the coupled release, allowance, SQL-store or runner files nor my two test files; `SQL_SELECTORS` includes the class.
* Finding 3, accepted: the simulated merge preserves both test blobs and main's rubric score; canonical blobs are rechecked after the final record commit.
