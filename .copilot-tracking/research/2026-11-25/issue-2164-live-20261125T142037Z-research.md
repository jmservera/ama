---
title: Research for issue 2164 live r13
ms.date: 2026-11-25
---

Disposition: executed. Planning Readiness: Ready.

## Findings

* Issue #2164 has no checkbox criteria; the criteria are those in earlier records: decide scope inheritance, test view_only with an eligible role, test scope bypass, live proof.
* HEAD `1154ce6058` contains the roster-scope fix in `Assistants.authorize` (bound row re-read, case_ids/areas, revocation, view-only refusal). Code reading found no defect, so no src change.
* Live revision `ca-cutover-test-demo-api--0000069` (created 2026-11-25T14:18:52Z, 100% traffic) was checked read-only with `az containerapp exec`: marker grep counts 4 in `core/assistants.py` and 1 in `core/sensor_review_draft.py`.
* Tests on HEAD: core `tests.test_assistants_identity` and `tests.test_sensor_review_draft` 73 OK (23 skipped); api `tests.test_assistants` and `tests.test_entra_authoritative` 192 OK (65 skipped).
* Live restricted-row behaviour needs a roster edit plus an interactive bound Entra sign-in; the owner decisions exclude production changes, so it stays unproven.

Evidence: docs/reference/research/issue-2164-deployed-code-proof-2026-11-25.md
