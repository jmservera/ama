---
title: Plan issue 1837 live r5 2026-11-23
ms.date: 2026-11-23
---

1. Add `test_trusted_proxy_route_write_requires_csrf_header_and_writes_nothing_without_it` to `src/api/tests/test_nomination_api_routes.py`.
2. Run the module and the 66-test affected set; run mypy and ruff on the api tests.
3. Mutation check: disable the server CSRF check temporarily and confirm the test fails, then restore.
4. Record per-criterion table, review, commit.
