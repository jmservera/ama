---
title: Issue 184 live run c plan
ms.date: 2026-11-23
---

Plan: add `ReceiveLeakTests` to `src/api/tests/test_iot_credential_hygiene.py`; hostile bodies carrying a marker credential must be refused with stable codes that never contain the marker. Test-only; no src change.

Tier: focused (test file only, no src/workflow/gate change). Local checks: that test file, `test_iot_stream.py`, ruff check and format, mypy in `src/api`.

## Critique (executed once)

Verdict: proceed. Findings applied directly: use real `EventData` with the same properties as `test_iot_stream.py`; cover invalid JSON, duplicate key, oversize body and a well-formed row with a marker in an unknown field; assert on `str`, `repr` and traceback text. Risk: an unknown-field row may be accepted by `preflight`; the test then asserts only that the decoded result is not an error path, so it is dropped if accepted and the refusal cases remain.
