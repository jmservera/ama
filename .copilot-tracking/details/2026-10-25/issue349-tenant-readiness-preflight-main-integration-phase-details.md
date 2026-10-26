<!-- markdownlint-disable-file -->
---
title: Issue 349 main-integration phase details
description: Steps and validation for the integration
ms.date: 2026-10-25
---

## Phase 3

* Step 3.1: git merge --no-ff origin/main with a Conventional Commit message and Copilot trailer; repo-local noreply identity.
* Step 3.2: On conflict, keep both sides of docs/reference/log.md and take main for rubric generated files; never drop prior entries.
* Step 3.3: Write changes artifact with a reconciled-claims table: 2026-10-24 findings are historical for that app and date; current status is owner-confirmed login working and zero database staff, not re-verified here.

## Phase 4

* Step 4.1: python3 -m unittest discover -s infra/tests -p test_tenant_readiness_preflight.py -q with PYTHONDONTWRITEBYTECODE=1.
* Step 4.2: Review once, independent.
* Step 4.3: tools/rpi-checks.py --all --base ea5577b2 --lock-timeout 0 to a new external dir only if the lock is free; verify receipt. No push; a later push needs coordinator permission and the expected remote SHA 44ba5b77.
