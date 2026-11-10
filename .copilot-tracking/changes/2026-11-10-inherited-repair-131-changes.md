---
title: Issue 131 inherited correction batch for the household inventory primitive (changes)
ms.date: 2026-11-10
task_id: 131-inherited-repair-1110
---

## Status

Prospective changes record, created before the `implement-start` witness event. No source, test or README change exists yet and the source is clean at `9f9f66fc287c54421668140987add1d891d913f8`. The completed changes, validation, divergences and commit claim are appended after implementation.

## Authority and budget debit (Root-recorded)

* Authority: Root brief `brief-131-inherited-repair-1342.txt` after the dated D2 audit `handoff-131-dated-budget-audit-1336.md`. Exactly one inherited correction batch.
* Debit: this batch consumes ONE cycle of the issue 131 allowance. Before it: exact balance not provable, proved lower bound at least 1 (pre-grant debits 2 to 5 give 3, 2, 1, or 5 after the one-time five on 2026-11-09 08:02:51Z in the exhausted case). After it: the conservative proved minimum is 0. No fresh five, no reset, no second automatic cycle, no self-retry. The initial inventory slice `7f8af9b`, the read-only D1 diagnostics `9f9f66f` and the D2 audit are not source corrective debits.
* Dated chronology (full table in the D2 handoff): two certain historic corrective cycles on PR 1154 (`d41b7bf10`, `9e1442173`, 2026-11-04); three possible CASE debits (PR 509 fix cycle 1 `0a378b63d` 2026-10-29, PR 903 format repair `8e58a2eca` 2026-11-03, PR 1034 format repair `43a0c160a` 2026-11-04), all before 2026-11-09 and left uncertain; no charged event after the grants.
* This resolves the prior numerical admission hold only. It grants no human, Legal or hold-release authority.

## Planned changes

* `src/core/src/zava_forward/core/resident_decisions.py`: shared history validator; view and writer use it; two count-only refusal reasons.
* `src/core/tests/test_resident_decisions.py`: two regression tests, one updated expectation, three typing fixes and the format fix.
* `src/core/README.md`: one bounded sentence.
* Ordinary merge of `origin/main` (`c9e15acbf4c0893358818e562d034d62321ea6d4`) after the marker.

## Completed changes

Status: implementation complete, uncommitted at the time of this record. The status line above is superseded by this section.

* Merge `6ecb920265d0719fa0ff97b0445c6a5c3b943d4e` (ordinary `--no-ff` of `origin/main` `c9e15acbf`, tree `418f118c32541d89b2c0476a25b27abb36b4ce2d`), made after the `implement-start` marker. No rebase, reset or amend. The merge did not touch `resident_decisions.py` or its tests.
* `resident_decisions.py`: `_household_ref_ok`, `_history_rows_ok` and `_inventory_history_ok` validate every stored revision (exact int version equal to position, case id, row shape, reference rules, uniqueness, link and digest pairing). `_inventory_fill` raises on any invalid history so the view reads Malformed. The writer refuses an invalid or empty stored history, or malformed reports, before the version check, with no mutation or audit. Two count-only refusal reasons (unresolved or ambiguous identity; missing or invalid decision route) sit between the unverified and open-trigger reasons. They contain no reference, owner, source or digest.
* `test_resident_decisions.py`: two regression tests (corrupt history malformed and never extended with 7 injected corruptions and a valid control; identity and route count-only reasons with a canary check), one updated expectation (refreshed-data identity reason), removal of the writer-guard escape for the empty-list history, and typing fixes (three prior mypy errors plus one new return annotation) plus `ruff format`. The strict-input tuple is intact.
* `src/core/README.md`: one bounded paragraph on corrupt history and the permanent identity reason.

## Validation (raw logs under the Root evidence `run/`)

* Red against the unfixed module: `red.exit` 1, 20 failures across JSON and SQLite stores, 4 skipped. This is the expected failing-before evidence.
* Green after the fix: inventory selector 45 tests OK (16 skipped); full Core `test_resident_decisions.py` OK (148 skipped, SQL-store cases skipped where no server is configured); API `test_resident_api.py` OK (1 skipped).
* Configured Core, no selectors: `ruff check .` exit 0; `ruff format --check .` exit 0 (235 formatted; baseline was 1 file to reformat); `mypy` exit 0, 288 files (baseline on candidate: 3 errors). One extra no-any-return in the test helper surfaced after formatting and was fixed with a typed local, not a cast or suppression.
* `git diff --check` clean. MSSQL not run and not claimed. No browser, cloud, model or private data.

## Behaviour notes and divergences

* No divergence from the plan. Historical stored digests are not compared with current reports in the history check, so a legitimately stale revision stays Declared and is refused by the stale reason, not as malformed.
* Identity stays fail closed: no action updates `identity_state`, so a linked inventory always lists the identity reason. Documented, not changed.
* Nothing releases or permits scope; `TENURE_HOLD` remains last in every refusal.
