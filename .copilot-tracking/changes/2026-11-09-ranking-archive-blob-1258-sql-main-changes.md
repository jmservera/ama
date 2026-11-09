# Issue 1258 SQL main integration changes (2026-11-09)

Refs #1258. Plan: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-sql-main-plan.md`. Not a sixth cycle; no hand-made source edit.

## Identities

* Prospective commit `25f523b2facd33dacefc5e7f3331bfa85a1c9ca2` (research, plan, details, critique), committed before merge and validation.
* Fetched `origin/main` `8d6f029cac004506953f36606862168bbe9d9412` (PR 1308 squash), re-fetched equal before merging.
* Merge commit `59d8ad8acc872be604f30dcbee1a44418aae74c8`, tree `f3c6ccc450e156461e6c1d76da1f8631870879c6`; author and committer `8036360+jmservera@users.noreply.github.com`, Copilot trailer. Ordinary `git merge --no-ff`, no conflict, no rebase or force.

## Merge delta

Source delta equals the 12 paths of research F1: `api/server.py`, `api/web/app.js`, `api/tests/test_case_journey.py`, `core/README.md`, `core/pyproject.toml`, `core/continuity.py`, `core/mssqlstore.py`, `core/sqlstore.py`, `core/store.py`, `core/tests/sqlguard.py`, `core/tests/test_priority_order.py`, `core/tests/test_resident_decisions.py`, plus main's tracking records. No `infra`, `tools` or `.github` path. Both intents are present in the merged `store.py` (Blob archive selection and `BlobArchiveError` handling beside `_order_unresolved` and `ORDER_NOTE`) and `server.py` (`ArchiveWriteUncertainError` on publish, `CommittedReloadError` on the priority routes). Adapter byte identity with c5 `52f9b61b`: `ranking_archive_blob.py` blob `346784573abf`, `ranking_publication.py` `a6ed0260d6da`, `ranking_publication_runner.py` `805ec28cd07d`, all equal.

## Validation (owner demo-targeted tier)

Scratch directory `/tmp/ama1258-sqlmain.QNzJu6` (owned `mktemp -d`, logs and venv with editable installs from this worktree). Every `ZF_*` and MSSQL environment variable was unset.

| Check | Result |
| --- | --- |
| core `PYTHONPATH=tests python -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents` | Ran 137, OK, exit 0 |
| core `PYTHONPATH=tests python -m unittest test_priority_order test_resident_decisions` | Ran 398, OK, skipped 158 (SQL Server and Azure opt-in classes, none run), exit 0 |
| api `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_ranking_publication_wiring test_case_journey` | Ran 66, OK, exit 0 |
| core `ruff check` on 12 changed source and test files | pass, exit 0 |
| core `mypy` on 9 impacted modules | no issues, exit 0 |
| api `mypy src/zava_forward/api/server.py` | no issues, exit 0 |
| api `ruff check` server.py, test_ranking_publication_wiring.py, test_case_journey.py | exit 1, 10 errors, all in `tests/test_ranking_publication_wiring.py` (9 E501, 1 I001) |
| `git diff --check HEAD^1 HEAD` | exit 2: trailing whitespace only in main's committed SQL evidence `.copilot-tracking/changes/logs/1292-2026-11-08-sql/server-version.txt` (inherited from PR 1308, not edited) |

## Adverse and unresolved

* The ruff finding is PRE-EXISTING. `test_ranking_publication_wiring.py` is byte-identical to `52f9b61b` (blob `c1b7fa96`) and `src/api/pyproject.toml` is unchanged. c5 linted only the adapter, core test and fixture, so this lint gap was never closed. Not fixed: no cycle or source authority. Reported open.
* Not run: SQL Server, Azurite or Azure, browser, `rpi-checks`, full matrix, hosted CI. SQL behaviour is #1292's own evidence; the 158 skips are literal skips, not passes.
* Emulator qualification through #1259 is not Azure, WORM, immutability or managed-identity acceptance.

## Literal unmet criteria carried

Azurite or real account acceptance, Blob container, WORM, role grant, Bicep env, deployment, folder-record migration decision, hosted CI on the final head, independent exact-head Functional closure on this final parent, Minor R-1 policy-name guard, API wiring-test lint. `Refs #1258` only; no full AC claim.
