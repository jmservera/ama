---
title: Resident AI activation 563b review
description: One post-implementation review, Refs #563
ms.date: 2026-10-31
---

## Review

* Execution: complete. Outcome: Conformant for the live acceptance criteria within observed evidence; no material findings open.
* Boundary: Azure resident app, SQL ledger and the sanitized evidence folder.

| Criterion | Result | Evidence |
| --- | --- | --- |
| Consented repair question gets an AI-generated grounded answer, sources collapsed | Met | attempt2-ai-generated.json, screenshot |
| Case-progress question gets an AI answer | Met | same |
| Thin AI label on AI replies; fallback states why | Met | label "AI-generated" and the attempt 1 fallback label |
| Without consent no data reaches the model | Unchanged; server requires use_record true | app.py, earlier tests |
| Authenticated live Playwright evidence | Met | two sign-ins, JSON and PNG |

## Findings

* RV-001 [Low]: AI is intentionally left on under the USD20 cap and expiry at 2026-11-01T00:00Z; roll back with the two variables if desired. Routed to the owner, not to this task.
* RV-002 [Low]: Human resident acceptance (HUMAN-563) stays unchecked.
