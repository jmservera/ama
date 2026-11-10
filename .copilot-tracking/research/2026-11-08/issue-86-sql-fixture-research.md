---
title: Issue 86 resident-control SQL fixture failure research
description: Root-cause research for the failing MSSQL resident test, prospective and read-only
ms.date: 2026-11-08
---

Scope: issue #86 only. Prospective, read-only. No test, helper, production or tools byte is changed here. Head `f024a965`, tree `0b4bbe9e`, Main `0f05e9aa`, parent ref `c5edb320`.

## Captured failure (preserved)

Core `MssqlResidentControls` run (evidence `/home/azureuser/.local/share/ama/gates/g86-focused-sql-1108/core-sql.err`): 108 tests, 1 failure, 1 JSON-only skip. The failure is `test_challenge_edited_in_case_outside_generation_candidates`, `test_resident_decisions.py:1262`, `4 != 40`. The earlier "288/103 ok" figures are parsed `... ok` line counts, not framework totals; synthetic log lines split some headers, so they are not a success count. The author Medium finding and its "identical to Main, pre-existence unproven" wording stay as written. The interrupted FULL stays failed. The owner CI-first position (08:15) does not waive an actual captured failure, and no Core class is added to broad CI or tool selectors in this slice.

## Root cause (static, to be proven by a baseline)

* The method is defined once on `JsonResidentDecisions` (line 1247) and inherited by `SqlResidentDecisions` and `MssqlResidentControls`.
* It builds a JSON seed with 41 extra cases, points `self.path` at a new file and calls `open_store()`.
* JSON store reads that file. SQLite builds a new `.sqlite` beside the new path and `_seed` fills the empty database from it, so 41 cases appear and the test passes.
* `MssqlStore` ignores the path for state: `_open` uses the connection string, the database was already seeded in `setUp`, and `_seed` only seeds when `SELECT COUNT(*) FROM cases` is 0. The extra cases are never loaded, so only 4 candidates exist.
* So this is a fixture assumption (per-path seeding) that holds for JSON and SQLite and not for a shared database. The product proposal selection (40 candidates) is not implicated by this reading; if the baseline contradicts it, stop and report.

## Existing backend helpers

* `SqlStore.merge_seed(data_path, apply=True)` (`sqlstore.py:452`) is a public insert-only seed merge used by `src/core/tests/test_seed_merge.py`. `MssqlStore` inherits it. It needs `cases` with `documents` and `funding` defaulted, appends one `seed_merge` audit entry and bumps `seq`; a later `open_store()` loads the rows. The JSON `Store` has no such method.
* Other tests in the file that call `open_store()` re-open the same path and are unaffected.
* Unproven: `merge_seed` has no MSSQL test in `test_seed_merge.py` (SQLite fixture only). The fixed test would be its first MSSQL use, so the MSSQL regression run is also its proof. Audit-chain and ledger-table behaviour on MSSQL are the risk; a failure there is reported, not worked around with private SQL.

## Candidate correction (not applied)

Add one small test helper on `JsonResidentDecisions`, for example `seed_extra_cases(count)`, that deep-copies `self.store.cases["ZF-1"]`, assigns ids `SYN-EDIT-nn`, and then branches on backend: JSON/SQLite keep the existing write-new-file-and-reopen flow; MSSQL writes a seed file containing only the new cases and calls `self.store.merge_seed(seed, apply=True)` then reopens. The 40-candidate assertion, the outside-candidate selection, challenge, version and provenance assertions, and skips stay exactly as they are. The production proposal algorithm is not touched. A backend flag (`sql`, `MssqlResidentControls`) already exists to select; a class attribute or an overridable method is preferred over `isinstance` checks.

## Baseline design (for the later admission)

* B1, true Main baseline: `git archive origin/main` into a new directory; new venv; install Main `src/core`, `src/agents`, `src/api` as non-editable distributions with the hash-locked API requirements; run Main's own `tests.test_resident_decisions.MssqlResidentControls.test_challenge_edited_in_case_outside_generation_candidates` from the Main tree. Prove import origins are the new venv and that file hashes equal Main. This is the only evidence that can show the failure exists on Main.
* B2, candidate reproduction: the same single method from a candidate archive with candidate packages; expected failure `4 != 40`.
* B3, mixed (candidate test file on Main packages) is attempted only if the module imports; an ImportError is recorded and not substituted.

## Regression design

After the correction: the single method on `JsonResidentDecisions`, `SqlResidentDecisions` and `MssqlResidentControls`; then `-k challenge` over the same three classes as nearby cases; plus `test_seed_merge` (SQLite) because the helper uses `merge_seed`. Skips are counted by name; no SQL skip is introduced.

## Lifecycle requirements for a future admission

New evidence directory under `/home/azureuser/.local/share/ama/gates/`; one container, label with a unique owner token, `--memory=3g --cpus=2`, loopback port, created inside `flock -n /tmp/ama-rpi-heavy.lock` held through setup, all runs and cleanup; owned-endpoint checks before tests; database created per test by the test itself; no pull, no global prune; synthetic data only; `PYTHONDONTWRITEBYTECODE=1`; no `PYTHONPATH` of repository source directories beyond the test directory. Not admitted now: Current107 ORIGINAL29d holds the heavy window, so no SQL, Docker, browser or probe runs in this preparation.

## Non-claims

No production bug is claimed. No FULL, no approvals, tick, closure or publication.
