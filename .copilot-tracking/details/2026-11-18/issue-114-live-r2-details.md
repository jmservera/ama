---
title: Issue 114 rerun phase details
ms.date: 2026-11-18
---

* Phase 1: job `job-114-r2-probe` via ARM PUT (command override, existing identity and env); read-only; deleted after use.
* Phase 2: `PYTHONPATH=src:tests python3 -m unittest tests.test_recovery tests.test_sqlstore tests.test_ledger_digest_blob` in `src/core`.
* Phase 3: Conventional Commit `docs(evidence): ...`, repo-local noreply email, no push.
