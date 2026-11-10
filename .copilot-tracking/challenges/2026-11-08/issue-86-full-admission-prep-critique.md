---
title: Issue 86 prospective FULL admission preparation critique
description: One independent read-only critique of the prospective FULL admission plan, with dispositions
ms.date: 2026-11-08
---

Scope: issue #86 only. Reviewer: one `rubber-duck` subagent, read-only, before any other step. Verdict as returned: Revise. The reviewer confirmed the 17 groups, serial no-shard behaviour with `--jobs 1`, the 58-byte output limit, non-queued `--lock-timeout 0` and the observed Main delta.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Neither parent delta covers `gates.py` or `procurement.py`, which are absent from Main. | Accepted. Plan step H adds a Main-versus-final-head review of all named inherited hunks and tests. |
| 2 | Blocking | The post-merge source qualifier rejects the expected rubric change. | Accepted. Details allow the rubric path with its own mode, blob and JSON proof. |
| 3 | Blocking | Hosted checks precede publication of an unpublished head. | Accepted. Plan step H makes publication a separate coordinator step that pushes the exact assessed head, then verifies the hosted head and results before any acceptance action. |
| 4 | Blocking | The Main-delta stop rule compared the wrong endpoints. | Accepted. Plan step B and details use the merge base versus fresh Main, plus a separate merge-result inspection. |
| 5 | Non-blocking | Remote identities must be refreshed at each decision point. | Accepted. Plan step A requires an explicit fetch and re-resolution of the parent ref, PR head and base, and `origin/main` before merge, receipt verification and publication. |
| 6 | Non-blocking | Five, not four, `test_assistants.Mssql*` selectors. | Accepted. Research corrected; proof required for all five. |

No re-critique is run. This critique is prospective and is not independent acceptance of any candidate.
