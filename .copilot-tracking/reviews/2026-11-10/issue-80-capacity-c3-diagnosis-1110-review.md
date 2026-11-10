---
title: Issue 80 capacity C3 stage-local checker correction, review
description: Native review (not independent) of the C3 checker hunk, written after implement-done
ms.date: 2026-11-10
---

Executed once after the `implement-done` marker, from the diff (`phase80-capacity-c3-evidence-1110/impl.diff`), `browser-run1.log` and the checker's failure listeners (lines 284-325); native author review, not independent. Boundary: the checker hunk (+11) and browser run 1. Outcome: **OPEN FINDINGS**. No new complete web-guidelines review is claimed; no web file changed.

* C3-R1 (High, open, defect in this change by source reading, not run-proven): the new branch in `hold_capacity_read` calls `route.fulfill(status=503, ...)` directly and, unlike `inject`, does not call `expected_failures.add(route.request)`. The `response` listener records every `/api/` response with status >= 400 whose request is not in `expected_failures`, and the `assert not failures` at line 814 follows the scenario. The served retry 503s would therefore very likely be reported as unexpected failures (and may produce unfiltered console errors). Smallest fix for Root to admit: add the request to `expected_failures` in that branch (still exact endpoint, exact 503, flag-scoped). It was not applied here because implement-done is recorded and Review findings route to later work; the edited stage was never reached, so this is unproven at runtime.
* C3-R2 (Medium, open): the one allowed whole `capacity_browser_check --axe` run exited 1 at `capacity_browser_check.py:571`, scenario `initial packages 503/retry` (no `alert` for 60 s; final status "The service is still starting. Trying again, this can take a few seconds."). That stage precedes and is untouched by the edit, and passed in the C2 run; cause UNKNOWN (not retried, no instrumentation, no app-defect claim). Both delayed-401 iterations and the empty-capacity assertion were not reached, so the correction is unexercised and publication stays blocked.
* C3-R3 (Info): focused checks passed: Ruff check 0, format 0, Node syntax on unchanged `ops.js` 0, API 11 OK, static 60 OK. These do not exercise the browser scenario.
* C3-R4 (Info): the earlier diagnosis (one packages focused setup on frozen source) is the only evidence for the correction; workorders and the full original ordering remain unobserved. The edit keeps the delayed 401 release point, assertions, timeout, non-JSON 503 and all app source unchanged.
* C3-R5 (Info): C1 batched implement-start preflight and the C2 early review draft disclosures stay; this chain issued each validation in its own call before each marker.

Ranked follow-ups: 1. Root decides whether to admit the one-line `expected_failures` fix (C3-R1). 2. Root decides whether to diagnose the line-571 failure (C3-R2) before another whole run. 3. Independent exact-head assessment only after a genuine whole-run pass. C2, C4, #73 and owner thresholds remain open.
