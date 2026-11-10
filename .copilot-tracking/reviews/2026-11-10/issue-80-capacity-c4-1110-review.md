---
title: Issue 80 capacity C4 review
description: Native review (not independent) of the C4 checker hunk, written after implement-done
ms.date: 2026-11-10
---

Executed once after the `implement-done` marker from `impl.diff`, the checker's `inject` and failure listeners, and the two observations; native author review, not independent. Boundary: the 1-line hunk and the diagnostic evidence. Outcome: **OPEN FINDINGS**. No web file changed; no new web-guidelines review is claimed.

* C4-R1 (High, open): no whole `capacity_browser_check --axe` has run on a head that contains the C3 stage correction plus this fix. The delayed-401 iterations (packages and workorders), the empty-capacity zero-anchor assertion and later scenarios remain unobserved, so neither change is proven at runtime. Publication stays blocked.
* C4-R2 (Medium, open): the line-571 failure of the C3 whole run is unexplained. It was not reproduced in 7 isolated runs (observation 1 and the 6 iterations of observation 2, all 503s answered by `inject`, alert after about 5.2 s). Candidate explanations (a hung read, interference from earlier stages, host load) are unevidenced. A whole run could fail there again.
* C4-R3 (Low, closed by source reading): C3-R1 is fixed: `inject(route)` registers the request in `expected_failures` before the same non-JSON 503, so the retry 503s should not be reported by the response, requestfailed or console filters. Unrun.
* C4-R4 (Info): observation 1's `alert_seen:false` is a driver snapshot defect (first `[role=alert]` was an empty region); observation 2 collected all alerts. Both preserved.
* C4-R5 (Info): focused checks passed (Ruff 0/0, Node 0, API 11, static 60); they do not exercise the browser scenario. Each validation ran in its own call before each marker; C1 batching and C2 early-draft disclosures and the C3 adverse records are unchanged.

Ranked follow-ups: 1. Root decides whether to admit one whole run on the committed head. 2. Independent exact-head assessment only after a genuine pass. C2, C4, #73 and owner thresholds remain open.
