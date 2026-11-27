---
title: Issue 1274 live critique (2026-11-27)
---

Executed once. Verdict: proceed. Catching `http.client.HTTPException` alongside OSError is the smallest fix; it keeps fail-closed behaviour (no bytes returned, exhaustion raises InstallError). Alternative of catching Exception rejected as too broad. Applied directly.
