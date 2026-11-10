# Changes: issue 954 photo flag browser validation (2026-11-09)

Implement phase, after the prospective planning commit fa2e2229b (parent ef28d4da4).

## Chronology and divergence

* The planning commit preceded the checker: its tree contains only tracking records. The checker was recovered afterwards as an uncommitted file (git hash-object 2323623a9a74ce2a93aac0763acd53d0d47387e4).
* Divergence: the 15:50 planning commit was made after the first checker recovery began in scratch; the recovered original is retained at `recovered-original.py` in the evidence directory. No phase was backdated.
* Interrupted run: the original session retried `flock -n` on the shared heavy lock (held by another lane, pid 3001521) in 14, 17 and 120 attempt loops. The coordinator stopped it as a prohibited waiting queue. Attempts 1 to 4 are lock-busy admission evidence (exit 1, no browser executed), not browser results.

## Changes

* Added `src/api/checks/photo_flag_stale_browser_check.py` (adapted to the owner definition of quiet; worktree import binding assertions; per-status receipt from `finally`).
* No product source change. No productive correction spent: count remains 0 of 5.

## Validation (DEMO targeted tier, worktree PYTHONPATH)

* `test_photo_availability` (src/api): 1 test, exit 0.
* Core `test_scenario_manifest`: 8 tests, exit 0. Core `test_needs_inventory`: 11 tests, exit 0. Recipe binding unchanged, no manifest SHA edit.
* ruff check and format on the checker: pass.
* Browser checker, one nonqueued admission at 2026-11-09T16:12Z (lock free): exit 1. All 503 and 403 behavioural assertions passed (one stale-true request, false flag, initials shown, photo hidden, inline role=status, no account error text, false refresh sends no request, true refresh retries once, denials stay 503/403, no full reload). The run then failed `503: no disruptive toast, alert, dialog or modal`.
* Diagnosis from the receipt: the only matched node is the pre-existing empty `<p id="account-error" class="err" role="alert"></p>`, added at workbench entry. It is an empty live region, not a toast; `account-error` text is asserted empty. Native `Failed to load resource` 503 diagnostics were recorded (2) separately; no page error, no dialog.
* This is a checker detector over-match, not a reproduced product bug. The fix (count only disruptive nodes with non-empty text) is NOT applied or claimed: no second admission is authorized. The checker is committed as-is and its failing result is retained as the genuine outcome.

## Skipped

* Browser pass for 403 quiet and receipt classification (aborted by the 503 failure); SQL, live, cloud, model, full gate.
