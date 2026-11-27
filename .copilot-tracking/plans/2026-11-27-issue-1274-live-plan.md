---
title: Issue 1274 live plan (2026-11-27)
---

1. Add `http.client.HTTPException` to the retry except clause in `fetch()`.
2. Add a regression test: IncompleteRead on first source retried then recovered; persistent IncompleteRead exhausts with InstallError.
3. Run unittest, ruff, mypy; record per-criterion table.

Tier: focused (tools only, no src, no workflow change).
