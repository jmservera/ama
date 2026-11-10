---
title: Issue 133 aftercare Stage A corrective cycle C2 changes
description: Changes, dispositions and divergences for corrective cycle C2 (2 of 5 total)
ms.date: 2026-11-09
---

Refs #133. No closure, push, PR or board write. All of C1-C6 remain unmet. Counter: 2 of 5 used, 3 remain.

## Dispositions

| Finding | Disposition | Change | Evidence |
| --- | --- | --- | --- |
| F1 false "Nothing was saved" | Fixed | `aftercare.js` outcomes saved, replayed, refused (400/403), conflict (409), unconfirmed (network, malformed, 5xx, 401). Unconfirmed keeps the same request ID, says saving could not be confirmed, directs to retry or the concerns list before another or paper record. Refusals after earlier uncertainty keep it. Receipt accepted only with matching `request_id`. | `tests/test_aftercare_screen.py` (12 pass) |
| F2 `[object Object]` fraction | Fixed | `acFraction`: N of M, zero denominator states no proportion, missing, non-numeric or count above denominator is Unknown. Node tests use real `AftercareService` payloads. | screen test |
| F3 replay after `next_update` passed | Fixed | Request lookup and fingerprint inside the atomic transaction before new-record time check. Replay writes nothing (`_txn(writes=...)`), changed payload conflicts. | `ReplayAfterDateTests` |
| F4 sensor-context guard bypass | Fixed | `_context_errors` (key pattern, 10 items, 200 chars, NFKC and zero-width normalised guard) before persistence, merged cap inside the transaction, document unchanged on refusal, value never echoed. Best effort, not privacy proof. | `SensorContextGuardTests` |

## Files

* `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/tests/test_aftercare_intake.py`
* `src/api/src/zava_forward/api/web/aftercare.js`, `src/api/tests/test_aftercare_screen.py`
* `src/core/README.md` (one sentence), `docs/reference/log.md` (appended entry)

## Divergences

* Hook contract unchanged except that a replay returns the unchanged document text, so a store may skip the write.
* `aftercare.js` still reads `error.errors`, which the shared `api()` does not yet copy (paused hook, not admitted).
* `aftercare.py` untouched.

## Validation

Core 65 tests, screen 12 tests, ruff format and check, mypy and `node --check` pass. Logs in `/tmp/issue133-1109/logs/`. Not run: full gate, api suite, static asset tests, served, browser, SQL and persistence restart checks.
