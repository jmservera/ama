---
title: Issue 1360 extension E1 review (one pass, self-run, not independent)
ms.date: 2026-11-10
task_id: 1360-extension1-1110
---

## Execution and outcome

Review executed once, by the implementing session, after implement-done. It is not independent and does not substitute for Root's exact-head review. Outcome: conformant with limits, no open material finding. It is not an operational, production or human approval.

Assessed boundary: three source and test files over merged base `307ba870a` (main `6d4cd624`), plus the new `.copilot-tracking` records.

## Checks against the plan and owner rules

* One-line core change only; no CLI, importer, doc, workflow, dependency or config edit. Transfer semantics, permissions, consent, actions and state unchanged. No catch-all and no default: only `OSError` and `ValueError` join the existing `RuntimeError`, and only around the post-commit `_sync`.
* Durable commit plus post-commit failure is reported truthfully: real SQLite, real `SqlStore`, actual CLI, injection only in the reload after a read-only probe proved the commit. Exit 2, no "Nothing was recorded", "may be recorded" present, no traceback, no invented count.
* Pre-commit failure still says "Nothing was recorded" and stores nothing; retry then adds one.
* Retry after the committed case exits 0 with `added=0 already_present=1`, one refusal and one audit entry. Ledger and source hashes unchanged.
* Existing conflict, `CommittedReloadError`, partial and driver tests stay unchanged and green.
* Original adverse findings preserved: the original diagnostic (`0c77f18f`) was self-reviewed; C1 to C5 spent and D2 zero history stand; E1 is a new owner grant, not a reset.

## Residual risk and limits

* Shared path: every `SqlStore.save` caller now sees `CommittedReloadError` instead of a raw `OSError` or `ValueError` from the post-commit reload. Existing API handlers for it already report a committed outcome; unhandled routes fail as before (500) but with a truthful message. Root should weigh this when reviewing.
* A corrupt-row `ValueError` is chained as `__cause__` and `_seq = -1` forces the next reload; the corruption itself is not addressed.
* `sqlite3.Error` from the reload keeps the existing "not known whether" arm. The MSSQL store and the MSSQL copy of the new core test were not observed (skipped, opt-in).
* No hosted CI, independent review, full local gate or browser check was run. Core `sqlstore.py` formatting already differs from the formatter before this change.
* Merge order against 1419, 132, 131 and 80 is Root's; none edits the owned hunk. Shared dependency is `sqlstore.py`.

## Routing

No finding requires another Implement or Review in this task. Follow-ups: Root independent exact-head assessment before any publication; E1 used, four left, none started.
