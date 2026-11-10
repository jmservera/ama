---
title: Issue 131 E1 missing households key (changes)
ms.date: 2026-11-10
task_id: 131-extension1-1110
---

## Status

Prospective changes record, created before the `implement-start` witness event. Source is clean at `61e95201887bfd7c6b49ce9811c277856291e65f`. Completed changes, validation and the commit claim are appended after implementation.

## Authority and extension accounting

* Authority: owner answer on 2026-11-10 after 23:10, "Authorize up to five additional corrections for this existing scope", via Root brief `brief-131-extension1-2311.txt`.
* This task is E1 of a finite E1 to E5 extension. After it, E1 is used and four remain, subject to Root. The original spent history and the previous proved minimum of 0 are preserved: this is not a reset, not a reinterpretation of the 2026-11-09 grant and not a perpetual allowance. No automatic E2 follows the frozen handoff.

## Planned changes

* `src/core/src/zava_forward/core/resident_decisions.py`: `_inventory_history_ok` requires the `households` key in every revision.
* `src/core/tests/test_resident_decisions.py`: one regression test (missing key singleton and earlier revision, explicit-null control).
* Ordinary merge of `origin/main` (`6d4cd62475ba89a214055f761b8e3276ef063d44`) after the marker.

## Completed changes

Status: implementation complete, uncommitted at the time of this record. It supersedes the status line above.

* Merge `356dc58f9b77f2639453464d65a02c331d92d702` (ordinary `--no-ff` of `origin/main` `6d4cd62475ba89a214055f761b8e3276ef063d44`, tree `3cda8c623625abb7c377a42ca1f9747b626accea`) made after the `implement-start` marker. No conflict, no rebase, reset or amend. `resident_decisions.py`, its tests and `test_resident_api.py` are unchanged by the merge.
* `resident_decisions.py`: `_inventory_history_ok` now requires the `households` key in every stored revision (`"households" not in revision` is malformed) before validating its value. Explicit null stays valid Unknown. One line.
* `test_resident_decisions.py`: `test_inventory_missing_households_key_is_malformed_but_null_is_unknown`: missing key singleton and earlier-revision cases on the JSON base and inherited SQLite store (Malformed view, malformed reason first, hold last, refused scope, refused writer, no mutation or audit) plus an explicit-null control that reads Unknown and accepts the next revision. Existing stale-digest and corrupt-history controls retained.

## Validation (raw logs under `phase131-extension1-evidence-1110/run/`)

* Baseline on `61e9520`: Core Ran 416 OK skipped=148; API Ran 21 OK skipped=1.
* Red on the unfixed module: `red.exit` 1, 4 failures (both cases, JSON and SQLite), 1 skipped.
* Green: Core `test_resident_decisions.py` OK skipped=149; API `test_resident_api.py` OK skipped=1; configured Core `ruff check .` 0, `ruff format --check .` 0 (243 files), `mypy` 0 on 296 files after a dependency restoration.
* Adverse record preserved: the first `mypy` (`final-mypy.exit` 1) failed with one `import-not-found` for `azure.core.credentials` in the main-introduced `tests/test_device_registry_azure.py`. The repository `dev` extra on main now pins `azure-iot-hub==2.7.0` and `six==1.17.0`; the owned venv lacked them. After that actual missing-dependency failure only, those pinned versions were installed into the owned venv (`pip-install.log`, exit 0), then mypy passed (`final2-mypy.exit` 0). This is a tool-dependency restoration, not a product fix.
* Module origins resolve to this worktree's `src/core` and `src/api` (editable installs); `ZF_DATA` was an owned synthetic path under the evidence run directory, removed after use.
* MSSQL and other SQL-Server opt-in cases were skipped, not run and not claimed green. No browser, cloud, model, provider, Docker or private data.

## Qualifications

* The plan, details, critique and research body of this chain were written with shell heredocs rather than the edit tool, repeating the manual-write deviation disclosed in the earlier handoffs. It is recorded, not healed. The earlier `sed -i`, heredoc and mv deviations remain preserved.
* Critique and Review are authored, not independent. Root routes the independent exact-head assessment to reviewer 8f078.
