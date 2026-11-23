# Issue 2237 live plan (2026-11-23)

Refs #2237. Task `issue-2237-live-20261123T012444Z`. Research: `.copilot-tracking/research/2026-11-23/issue-2237-live-research.md`. Details: `.copilot-tracking/details/2026-11-23/issue-2237-live-details.md`.

Tier: FULL, because `src/` changes (owner instruction: do not run `rpi-checks.py --all`; targeted tests, mypy and ruff only; the coordinator runs gates).

## Objective

Make a busy SQL write lock a diagnosable, retryable condition instead of an anonymous 500, for `/api/retention` and every other handler that reaches `_unhandled`.

## Phases

* [x] Phase 1: research (live logs found the cause).
* [ ] Phase 2: core helper. Add `is_write_lock_busy(exc)` beside `LOCK_FAILED` in `mssqlstore.py`: true for an exception whose text contains `LOCK_FAILED` and whose class is a driver `ProgrammingError`/`DatabaseError`, checked along `__cause__`/`__context__`.
* [ ] Phase 3: API mapping. In `server.py` `_unhandled`, when the helper matches and no response has started, log `http-error <method> <path> status=503 exc=<class> cause=sql-write-lock-busy at=<frame>` at WARNING (no message text) and answer 503 with `Retry-After: 5` and a plain-language error naming owner and next action. Other exceptions keep the 500 path unchanged.
* [ ] Phase 4: tests. Core: helper true/false cases. API: `/api/retention` with `store.audit` patched to raise the lock error returns 503 with `Retry-After` and a secret-free log; an unrelated error still returns 500.
* [ ] Phase 5: validate (targeted unittest, mypy, ruff check and format check) and record changes with the per-criterion table.
* [ ] Phase 6: review once.

## Critique (one pass, final candidate)

Verdict: proceed with amendments, all compatible and applied directly.

* A 503 on a held audit write fails closed and keeps the audit control: accepted. Skipping the audit was already rejected.
* Matching on message text is brittle: mitigated by reusing the single `LOCK_FAILED` constant that `_begin` already matches, and by requiring a driver error class, so an unrelated exception that quotes the text is not reclassified.
* The helper must not import `mssql_python`, which is an optional extra: it identifies the driver error by class name and module prefix, with no import.
* A retry in the request path would add 15 s per attempt: rejected, as in the research note.
* Retention writes that already committed cannot be mislabelled: `retention_due` writes only the audit entry, and a lock timeout means nothing was written. For POST handlers whose own `except` already answers 503 with an outcome note, behaviour is unchanged because only `_unhandled` is touched.
* No change to 403 or other statuses; no web UI change, so the web-UI test and design-guideline gates do not apply.

## Out of scope

Finding the lock holders, shortening write transactions and any Azure change (owner-gated, outside the demo authorisation).
