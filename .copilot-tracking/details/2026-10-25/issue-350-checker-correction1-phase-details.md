<!-- markdownlint-disable-file -->
---
title: Issue 350 checker correction 1 phase details
description: Phase details for the checker correction
ms.date: 2026-10-25
---

* Phase 1: tests `test_runtime_admin_only_response_passes_without_acceptance`, `test_admin_payload_rejects_business_data_or_missing_flag` and `test_excessive_json_nesting_is_blocked_not_raised`. They failed (one failure, one error) before the fix.
* Phase 2: `except RecursionError` before `except ValueError`; admin role accepted only by exact `identity.ADMIN_ROLE_NAME`; no business permission granted.
* Phase 3: 80 of 80 tests pass; the CLI on a 10000-deep file reports blocked and exits 2.
