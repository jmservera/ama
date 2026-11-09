---
title: Issue 440 ranking main currency changes
description: Changes record for the current-main currency continuation
ms.date: 2026-11-08
---

## Changes

* Planning commit dda434ee1194d5f14fc91e42bf58e1accc3c0e79 (currency research, plan, details) precedes the merge and edits.
* Normal merge of origin/main 77fa5d35e915e524af9a5d536e3ae093b69c5807 (merge commit 28be1bfc8922961f3dfc3eadac2ca3813ba45bb0); only .github/rubric/scores/latest.json changed, blob 6741ddd61aba2ff80cd8b7cb2f59e63cb1af7db3, mode 100644, JSON valid.
* docs/architecture/cutover-evidence-pack.md: one appended subsection, additions only. docs/reference/log.md: one appended entry. No other canonical edit; README paragraph unchanged.

## Actual checks (scratch /mnt/ama-gates/c440-currency-r2-1108-checks)

* pip install non-editable of core, agents, api exit 0; pip check exit 0; installed modules byte-equal to worktree sources; synthetic empty ZF_DATA; PYTHONDONTWRITEBYTECODE=1.
* core 76 OK, API 53 OK (SQLite-backed, not SQL Server), cohort 20 OK, retention pytest 37 passed; no skips reported. A first retention attempt failed (pytest missing) because HOME was redirected; rerun with the normal HOME passed. Preserved here.
* git diff --check exit 0; ignored-inclusive status 0 lines.

## Divergences

None. The gate result is deliberately not recorded in tracked files; it lives in the external handoff.
