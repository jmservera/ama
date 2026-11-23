---
title: Changes issue 1837 live r5 2026-11-23
ms.date: 2026-11-23
---

Base `d23b7c83e8`. Refs #1837. Test-only change; focused tier (no src, workflow, dependency, Dockerfile or gate file touched; basis: the added test patches the provider name on a test instance and changes no write handler). `rpi-checks.py --all` not run. No Azure resource touched; no credential recorded.

Files: `src/api/tests/test_nomination_api_routes.py` (new `test_trusted_proxy_route_write_requires_csrf_header_and_writes_nothing_without_it`), r5 RPI artifacts, `docs/reference/log.md`.

Validation: new test passes (1.5 s); with the server CSRF check disabled the test fails (mutation check, then restored); 67 affected unit tests OK (66 earlier plus 1); `ruff check`, `ruff format --check` and `mypy` (372 files) clean. Browser axe journeys were not re-run: the change touches no web file; the full-module run showed one Playwright wait timeout under load average 8 in an existing browser test, which passed in the 67-test run.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Failing-first coverage, three submissions, valid challenge target | Proven (earlier record) | [failing run at 9da3fcd](../../../docs/reference/research/issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); regression tests pass on main |
| 2 Valid submissions retain records; JSON callers compatible | Proven locally | existing route tests; no live write (adds irreversible shared-demo records) |
| 3 Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven, now with a repeatable CSRF test | new test: missing `X-ZF-CSRF` gives 403 and no write; header gives 200; earlier tests cover 401, 403, 400, cross-case |
| 4 Browser journeys with axe, zero unexpected skips | Proven in earlier records (r2 to r4); not re-run in r5 | no web file changed |
| 5 Independent exact-head review; hosted CI | Unproven | needs a push, which is forbidden here |
| 6 Full-tier receipt | Not applicable | no src change |
