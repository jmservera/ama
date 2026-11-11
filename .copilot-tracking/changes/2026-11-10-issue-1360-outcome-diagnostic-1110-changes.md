---
title: Issue 1360 served-transfer outcome diagnostic changes
ms.date: 2026-11-10
task_id: 1360-outcome-diagnostic-1110
---

## Status

Implement phase started 2026-11-10 (stub persisted before the implement-start witness seq 4; completed in place). Diagnostic only: no product, test, configuration or documentation change is made. Changes to the worktree are limited to the new original RPI records listed below.

## Diagnostic execution (evidence only, outside the worktree)

Evidence root `E` = `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/phase1360-outcome-diagnostic-evidence-1110/` (scripts `E/diag/driver.py`, `E/diag/run_case.py`; per-case `E/runs/<case>/result.json` and `proof.json`; logs `E/logs/`). Own env `/tmp/zf-1360-1110/venv` was created, used and removed. Editable installs of `src/core` and `src/importer` resolved under this worktree (asserted before any run). `PYTHONDONTWRITEBYTECODE=1`.

| Case | Setup | Raw CLI exit and stderr | Independent reopen and retry |
| --- | --- | --- | --- |
| N1 control | independent real save of `form_schemas` (seq 1 to 2), no injection | exit 0 | refusal and audit retained, seq 3; retry exit 0, `added=0 already_present=1`, audit count 1 |
| C1 OSError | same independent writer; `OSError` raised only in `_sync` called from `save` after a separate read-only connection showed the refusal document, the `recorded_import_refusals` audit entry and seq 3 greater than 1 | exit 2, `Cannot transfer: the served store refused it (synthetic post-commit refresh failure). Nothing was recorded.` | document, `added=1` audit entry, seq 3 and `form_schemas` all retained; retry exit 0, `added=0 already_present=1`, audit count stays 1 |
| C2 ValueError | same as C1 with `ValueError` | exit 2, same text | same retained state; retry exit 0, audit count 1 |
| N2 conflict control | independent writer commits the same `import_exceptions` document; no post-commit injection fires (`injected` false) | exit 2, `another writer changed the stored import refusals first ... rolled back and nothing was recorded` | only the competitor refusal stored; retry adds the transfer's refusal (`added=1`, audit 2) |

For C1 and C2 the ledger database and refused file sha256 values are unchanged before and after (`ledger_and_file_unchanged` true). The proof file records the call order: independent writer commit, then `_sync_post_commit_probe` from `save` with `committed_before_injection` true, then `injected`, and then only a passthrough `_sync` from the product's own `_discard` recovery.

Approach 1 reached the branch; Approach 2 was not needed and was not attempted.

## Validation

* Baseline `python -m unittest tests.test_import_exceptions` (from `src/importer`, own env): 40 tests OK before the diagnostic, and the same 40 tests OK after it, unchanged test file.
* `git status` shows only the new RPI records; `git diff fe59ef56a0084dd975fd7e5c342670bb8f788fb0 -- src docs tools .github infra` is empty.
* Not run: Core suite, typing, lint, hosted checks (no product change, out of scope).

## Limits

* The I/O failure is injected at the post-commit `_sync`, so this shows the message contract defect on a committed outcome; it is not a naturally observed `OSError` and not a data-loss, Critical or High claim.
* The independent writer is a second `SqlStore` in the same process, committed through the real `save`.
* The witness log is local, writable and self-asserted.

## New RPI records (only worktree changes)

* `.copilot-tracking/research/2026-11-10-issue-1360-outcome-diagnostic-1110-research.md`
* `.copilot-tracking/plans/2026-11-10-issue-1360-outcome-diagnostic-1110-plan.md`
* `.copilot-tracking/details/2026-11-10-issue-1360-outcome-diagnostic-1110-details.md`
* `.copilot-tracking/plans/2026-11-10-issue-1360-outcome-diagnostic-1110-critique.md`
* `.copilot-tracking/changes/2026-11-10-issue-1360-outcome-diagnostic-1110-changes.md`
* `.copilot-tracking/reviews/2026-11-10-issue-1360-outcome-diagnostic-1110-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-10/issue-1360-outcome-diagnostic-1110-state.json`
