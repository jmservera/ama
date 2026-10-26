<!-- markdownlint-disable-file -->
---
title: Issue 349 main c8d16059 integration phase details
description: Steps and validation
ms.date: 2026-10-26
---

* Step 3.1: confirm HEAD e95c0f51 and origin/main c8d16059 unchanged; commit plan artifacts with repo-local noreply identity and Copilot trailer.
* Step 3.2: git merge --no-ff c8d16059. latest.json conflict: take main's version. docs/reference/log.md: verify no line removed versus both parents. Any other conflict: stop.
* Step 3.3: changes record with path summary and ancestry proof.
* Step 4.1: PYTHONDONTWRITEBYTECODE=1 unittest of infra/tests/test_tenant_readiness_preflight.py; git diff --check noting byte-preserved patch archives.
* Step 4.2: one independent bounded review; no gate.
