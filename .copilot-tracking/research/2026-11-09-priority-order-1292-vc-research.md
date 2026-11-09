<!-- markdownlint-disable-file -->
# Research: issue 1292 validation correction (2026-11-09)

Task `1292-vc-1109`, parent `1292-recovery-1109`. Agent: RPI agent, Sonnet 5.5. Research disposition: `executed`. Planning Readiness: `Ready`.

## Identities

* Frozen start: `f4d7b3d5d8c8137c765b6b823b936bcd2860a819` (tree `2885028de9c57c4911e8cbbc7d063a7e8ebb3157`), branch `fix/demo-recovery-1292-1109`, clean.
* Fresh main named by the coordinator: `9814cf6b236be1f2e86c4401973b8e834be927bc` (#1301). Fetched `origin/main` is now `76db469b1` (rubric score chore only; `git diff 9814cf6 origin/main` touches `.github/rubric/scores/latest.json` alone).
* Local merge of `origin/main` (no rebase, no force): head `ba8c3a51cecba0123aa47f3b02964d4368fbc5ad`. The merge brought 92 files of documentation, README and tracking changes and no `src/core` change (`git diff --stat f4d7b3d HEAD -- src` shows `src/README.md` only).
* No sibling #1288 or #184 unmerged code is imported.

## Original adverse evidence (preserved, not cleared)

* Independent "Revise" outcomes on the issue: C2 (5 High, 4 Medium) and C4 (1 High, 11 Medium). Local self-reviews: [C2](../reviews/2026-11-08-priority-order-1292-c2-review.md), [C4](../reviews/2026-11-08-priority-order-1292-c4-review.md); C4 F4 (partial BEGIN) and F8 (fixture admission) were "addressed with fakes/logic only", C4 residual risk 4 records the API-suite import errors. Original SQL logs: [logs/1292-2026-11-08-sql](../changes/logs/1292-2026-11-08-sql/).
* Recovery [review](2026-11-09-priority-order-1292-recovery-review.md) left open: one MSSQL resident failure, seven API import errors, SQL scale, ledger migration, data-owner mechanism, rolling-release fence, full gate, independent review and hosted CI. It did not claim these closed.

## Failure 1: MSSQL `test_challenge_edited_in_case_outside_generation_candidates`

Test: `src/core/tests/test_resident_decisions.py` (`JsonResidentDecisions`, inherited by `SqlResidentDecisions` and `MssqlResidentControls`).

* `setUp` writes seed JSON to `tmp/synthetic.json`, opens the store (seeding the backend) and submits a design for ZF-1.
* The test needs 41 open cases owned by one user so that the 40-case generation cap leaves one case outside the generated candidates (the case-edit and outside-generation semantics). It deep-copies `DATA`, appends 41 `SYN-EDIT-nn` cases, **rewrites a new JSON path** (`tmp/edited-in/synthetic.json`) and calls `open_store()` again, then asserts `len(original["case_ids"]) == 40`.
* On JSON it reads the new file. On SQLite the database path derives from `self.path`, so the new path is an empty database and the new seed loads. On SQL Server the database is chosen by `ZF_SQL_DATABASE`, set once in `MssqlResidentControls.setUp` to a UUID-named database that `setUp` already seeded. `SqlStore._seed` loads the file only when `SELECT COUNT(*) FROM cases` is zero (`sqlstore.py` `_seed`), so the second `MssqlStore` ignores the rewritten JSON and sees the original handful of cases: observed `4 != 40`.
* `SqlStore.save` only UPDATEs existing cases and has no insert path, so test code cannot add cases through `store.cases` plus `save()`. `merge_seed` exists but is SqlStore-only, takes a file and mutates the seed contract, so it is not a backend-neutral fixture helper.
* Classification: a test fixture/setup defect (backend-specific storage identity not re-created when the test supplies a new seed). Production code (`resident_decisions`, `store`, `sqlstore`) is not implicated: the same test passes unchanged on JSON and SQLite, and the assertions after the seed are untouched by the defect. It is tightly coupled to this validation because the owner-selected tier requires the relevant MSSQL resident controls to run with zero skips and failures.

Reproduction control (executed in this task, results in the changes and review records): the one selector on `9814cf6` source and tests, on frozen-start source and tests, then with the correction.

## Failure 2: API broad suite, 7 import errors

* Same 7 errors on the frozen head run in this task (1994 run, 7 errors, 365 skips, 999 s). Every one is `ModuleNotFoundError: No module named 'playwright'` from `src/api/checks/*_browser_check.py`.
* [API README](../../src/api/README.md) (current): "with installed project dev distributions", `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q`. `src/api/pyproject.toml` dev extra is `ruff==0.17.1`, `mypy==2.4.0`, `playwright==1.64.0`. The worktree `.venv` lacked the dev extra (it had ruff 0.17.4, mypy 2.4.1 and no Playwright). Chromium 1248 is already in the user cache.
* Diagnosis: missing installed dev dependency, not an application defect. Correct restore: `pip install -e "src/api[dev]"` in the worktree `.venv` only (no uv, no global install). Directly named modules need `PYTHONPATH=tests:../core/tests:../agents/tests`; the discover command adds `tests` itself.

## Failure 3 (found by the pinned type check)

`cd src/core && mypy` (the configured whole-package command in `src/README.md`) reports `tests/test_priority_order.py:1402: Incompatible types in assignment (SimpleNamespace vs Module)` in the C4 fake-adapter fixture. The earlier recovery ran `mypy src` only, which does not cover tests. The module is this issue's own file, so the fix is in scope: an annotation-level `# type: ignore[assignment]` matching the adjacent `# type: ignore[attr-defined]` convention. No behaviour change.

## Shared resource state

`/tmp/ama-rpi-heavy.lock` is held by a foreign session's `flock -n ... /tmp/e1-sql-run.sh` (PID 2565848, confirmed from `/proc/locks`, not file existence). Nonqueued admission: it is not interrupted, inspected or queued behind; SQL Server work for this task is deferred until a later nonqueued admission succeeds, while lightweight work continues. No container exists for this task before admission.

## Existing-issue dedup

Existing GitHub issues are not hydrated into new drafts here because the correction stays inside #1292's own test fixtures; no separate production fix is needed, so no new issue draft is produced. A follow-up draft is required only if the corrected test then fails for a production reason.

## Correction budget

Default five total scoped cycles for #1292. Used: C1, C2, C3, C4 (all 2026-11-08). The recovery (2026-11-09) made no source change and is not counted as a correction cycle. This task is cycle 5 of 5. The owner's dated additional grant applies only to an issue already demonstrably exhausted and is not invoked. After this cycle no default cycles remain; any further correction needs explicit issue-specific authorization.

## Planning Readiness: Ready

Scope: (1) a backend-neutral `reseed` fixture helper, with an MSSQL override that creates a fresh test-owned UUID database, replacing the JSON-only rewrite; (2) one type-ignore; (3) API dev-dependency restore (environment only). No assertion, expected output, skip or production file changes.
