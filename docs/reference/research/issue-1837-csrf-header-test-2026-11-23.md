---
title: Issue 1837 nomination route CSRF header test, 2026-11-23
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Refs #1837. Base `d23b7c83e8`.

Criterion 3 requires negative tests for same-origin and CSRF boundaries. The write handler (`server.py`) enforces `X-ZF-CSRF` only when the provider is `trusted-proxy`, so the shared-password test server never exercised it. The new unit test `test_trusted_proxy_route_write_requires_csrf_header_and_writes_nothing_without_it` in `src/api/tests/test_nomination_api_routes.py` shows, for `POST /api/cases/ZF-1/resident`:

* no `X-ZF-CSRF` header: HTTP 403 `Missing request header.` and the case record is unchanged;
* with the header: HTTP 200.

Evidence: test passes; with the server check disabled it fails (mutation check, restored); 67 affected unit tests pass; ruff and mypy clean. Not claimed: a new vulnerability, live-demo write, independent review or hosted CI. The per-criterion table is in the [r5 changes record](../../../.copilot-tracking/changes/2026-11-23/issue-1837-live-r5-changes.md).
