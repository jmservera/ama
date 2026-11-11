---
title: Closure-wave integrated-main checkpoint research (Refs #440)
description: Read-only research for one bounded checkpoint of the merged 1428, 1426, 1423 and 1430 increments on main 8aedb56b
ms.date: 2026-11-11
---

## Status and disposition

* Research disposition: `executed` (read-only git, source and GitHub queries only). Planning Readiness: `Ready` for a plan-only freeze. Nothing in this record is an observed result; no test, probe, pip, browser, Ruff or mypy ran, and no source changed.
* Plan-only launch: implementation and any observation wait for Root's prospective admission.

## Source identities (read 2026-11-11)

* Worktree `/home/azureuser/source/ama-demo-wt/issue-440-closure-wave-main-1111`, branch `docs/demo-closure-wave-checkpoint-440-1111`, HEAD = `origin/main` (fresh fetch) = `8aedb56b5909903abd6c6f84777b49f237c1cbb0`, tree `9e0e8efda1145ea4c990d0208e8cf6d07f0f8af4`, clean at start.
* Trees: `src` `84f7b054e66db107edf5753151dce23912da4bac`, `src/api` `a250906c8258f3a06d391e6f4976b484a9278a89`, `src/core` `075f86fb3a674d4a35cf7d12fd1943dcb118c03d`, `src/importer` `887e665146ca1720dbb1074e79065bcd48c89810`, `src/agents` `a35f7e1d7fa9e7e6b6b4c2c104318f08c2700cf2`, `docs` `f3d6a06c66566ea572d64db16f988da4d2f93fcb`, `docs/architecture` `57611004412bc859a8c7f1303716395ca4ba8b75`.
* First-parent chain on main: `7e2744cf` (rubric only) then `05f11ebe9` (#1428), `01f461dd7` (#1426), `3dbb79e90` (#1423), `8aedb56b5` (#1430, documentary).

| Merged increment | Main commit | Source touched | New or changed existing tests |
| --- | --- | --- | --- |
| #1428 permit timing and server-bound result attribution (issue 144 extension 2) | `05f11ebe9` | `core/ai.py`, `core/ai_consumption.py`, `core/assistants.py` | `api/tests/test_ai_consumption_api.py` (`ConsumptionApi`), `core/tests/test_ai_consumption.py` (`ConsumptionTests`) |
| #1426 truthful committed transfer reload errors (issue 1360 extension) | `01f461dd7` | `core/sqlstore.py` | `core/tests/test_priority_order.py` (`SqliteC4Corrections`), `importer/tests/test_import_exceptions.py` (`TransferFailureTests`) |
| #1423 contextual Capacity CSV downloads with child #1424 and handoff CSV (issues 80 and 1419) | `3dbb79e90` | `api/server.py`, `api/web/app.js`, `api/web/ops.js`, `api/checks/capacity_browser_check.py`, `api/README.md` | `api/tests/test_unaccepted_handoff_csv_api.py`, `test_case_journey.py`, `test_role_endpoint_inventory.py`; UI and guidance browser tests already on main |
| #1430 documentary inventory and staff intake checkpoint | `8aedb56b5` | none (pack, log, tracking) | none |

* Source blobs at the pin: `server.py` `9227eb98`, `app.js` `734aab48`, `ops.js` `4ef77471`, `capacity_browser_check.py` `6a4487eb`, `sqlstore.py` `01a3a44c`, `assistants.py` `7057beae`, `ai.py` `580838fe`, `ai_consumption.py` `4ff3848d` (full ids in the details record).
* Pack `docs/architecture/cutover-evidence-pack.md` (6929 lines, blob `836c1d2c3979de51c13f7fcfea72e4427f1812b6`) and `docs/reference/log.md` (11466 lines, blob `00e81e98ff8769c05898b8f2581ebbbcc919b9eb`) are the append targets later. The last pack section is the 2026-11-11 household inventory and staff intake checkpoint; its added, corrected and follow-up records are original history and stay untouched.

## Documents and status (approved versus proposed)

| Document | Version and status | Blob |
| --- | --- | --- |
| BRD `docs/brds/agentic-retrofit-programme-brd.md` | 0.21.0, `draft` (2026-10-24) | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` | 0.21.0, `in-review`, author-complete-unsigned-pending-review-and-owner-acceptance (2026-10-25) | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0001 Azure architecture | Proposed (non-production demonstrator) | `d42fa5c4615f4107cee83e07555dba6985c1f53e` |
| ADR 0006 src layout and cutover | Accepted 2026-10-15 by the owner | `956da1a3b804c803041fe2e8a312bd9f400273ae` |
| ADR 0007 contractor intake, staff mediated | Proposed 2026-11-04, not accepted | `abb21088a9bb9771234a305b8052c3bcdd181b33` |

Nothing here is approved except ADR 0006. Passing local selectors approves no requirement.

## Document-qualified requirement trace (read; verification classes are planned, not observed)

| Increment | Requirement as cited by the repository (document qualified) | Note |
| --- | --- | --- |
| Handoff CSV (#1419, #1423) | PRD FR-066 and AC-120 (owned staff exception queue including unaccepted handoffs); BRD FR-057 and AC-112 (exception-led queues) | PRD AC-120 reads "Not run" in the pack history; read-only CSV copy is a convenience of the queue, not queue acceptance |
| Capacity downloads and page (#80, #1423) | ADR 0001 (cited by issue 80); PRD FR-008 and AC-010/AC-011 (capacity gate) are the governing capacity gate, not the CSV control; PRD FR-024 (exportable evidence) is a candidate link, to confirm during implementation and not assumed | Excel transition issue 80 stays open; nothing here ticks it |
| Permit timing and attribution (#1428, issue 144) | BRD NFR-012 (AC-100, AC-101 in the BRD) and PRD NFR-017 (AC-109, AC-110) metering, attribution and bounds | AC-100 and AC-101 in the PRD are conversation criteria; the numbers are not interchangeable across documents |
| Shared-store reload error contract (#1426, issue 1360) | Issue 1360 criteria (closed, 4 of 4 ticked); no BRD or PRD requirement is cited by the issue body. Link to PRD FR-066 (failed import exceptions) is candidate only | Contract is a truthful error outcome, not data acceptance |

## Existing selectors (exact names, static method counts from `grep` of the pin)

Static counts come from reading `def test_` lines; actual run counts, skips and subclass inheritance are discovered only at observation and are compared, not assumed.

| Surface | Existing selector (from the named directory) | Static expected | Skip and lock behavior read from source |
| --- | --- | --- | --- |
| Shared-store error contract | `src/core`: `tests.test_priority_order.SqliteC4Corrections` (includes `test_post_commit_reload_exhaustion_is_a_committed_outcome`, `test_post_commit_reload_oserror_or_valueerror_is_a_committed_outcome`, `test_import_refusal_marker_is_cleared_after_a_failed_precommit_write`) | 21 | SQLite store double; the `Mssql*` subclasses are opt-in and not selected |
| Importer transfer failures | `src/importer`: `tests.test_import_exceptions.TransferFailureTests` (includes `test_committed_save_then_oserror_reload_is_not_nothing_recorded`, `test_committed_save_then_valueerror_reload_is_not_nothing_recorded`, `test_real_precommit_failure_still_says_nothing_was_recorded_and_retries_once`) | 8 | none read |
| Importer whole project | `src/importer`: `python -m unittest discover -s tests` (README command; 5 test files) | 82 | none read |
| Permit and consumption, API | `src/api`: `tests.test_ai_consumption_api.ConsumptionApi` (14 permit methods at lines 1717 to 2006 such as `test_permit_reserves_once_marks_and_fences_the_attempt`, `test_permitted_result_binds_attribution_to_the_stored_reservation_root`, `test_result_without_a_permit_closes_the_task_against_a_later_permit`) | 32 | none read |
| Permit and consumption, core | `src/core`: `tests.test_ai_consumption.ConsumptionTests` (adds `test_joined_reservation_window_and_first_completion_inside_one_transaction`) | 34 | `mssql = False` on the port |
| Handoff CSV API | `src/api`: `tests.test_unaccepted_handoff_csv_api.UnacceptedHandoffCsv` | 13 | none read |
| Handoff JSON API, list export | `tests.test_handoff_api.HandoffApi`, `tests.test_list_export_api.ListExportApi` | 7 and 11 | none read |
| Role inventory | `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 24 (14 own plus 10 inherited from `Matrix`) | none read |
| Case journey | `tests.test_case_journey` (one `CaseJourney` class; Node subprocess, no browser) | 31 (prior pack records) | needs `node` on PATH |
| Copy and static assets for changed `app.js` and `ops.js` | `tests.test_content_standard.CopyAudit`, `tests.test_static_assets` | 18 and 5 | none read |
| Capacity checker unit tests | `tests.test_capacity_browser_check` (`CapacityBrowserCheck` 5; one runs a 4-test no-Playwright subprocess) | 5 | none read |
| Handoff download UI | `tests.test_unaccepted_handoff_download_ui` (`UnacceptedDownloadText` 4, `UnacceptedDownloadBrowser` 2); needs `ZF_BROWSER_TESTS=1` | 6 (2 browser) | Browser class takes the lock itself, non-blocking, in `setUpClass`; a busy lock raises `SkipTest` (a skip is not evidence) |
| Handoff read-only guidance | `tests.test_handoff_read_guidance` (`HandoffReadGuidanceText` 5, `HandoffReadGuidanceBrowser` 4); needs `ZF_BROWSER_TESTS=1` | 9 (4 browser) | Browser class takes no lock itself |
| Capacity whole browser and axe | `src/api`: `python -m checks.capacity_browser_check --axe /tmp/axepk/package/axe.min.js` (no `--mssql`) | one run | Takes the lock itself, `LOCK_NB`, and exits `BLOCKED: shared heavy lock busy` when held; clears the environment to PATH, HOME, TMPDIR, LANG, LD_LIBRARY_PATH |

## Lock handling conclusions (read, not run)

* `capacity_browser_check` and `UnacceptedDownloadBrowser` acquire the shared lock `/tmp/ama-rpi-heavy.lock` themselves. Wrapping either in an outer `flock -n` double-locks: the CLI would exit BLOCKED and the test class would skip. They run unwrapped and sequentially.
* `HandoffReadGuidanceBrowser` takes no lock, so it is the only entrypoint that needs one external nonqueued `flock -n`.
* A busy lock, a missing Chromium, Playwright, Node or the axe asset is `blocked`, never a pass, and gives no authority to queue, kill or install a service. The pinned axe asset `/tmp/axepk/package/axe.min.js` exists on this host and was previously read as axe 4.10.3 with sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`; it is re-verified at observation, not here.
* Environment gap read now: venvs `/tmp/ama-440-inventory-venv-1111`, `/tmp/ama-80-stack-venv-1111` and `/tmp/ama-80-audit-venv-1110` exist but hold editable installs of other worktrees, so they cannot prove this tree. A fresh private venv for this worktree needs `pip` after admission; that install is a prerequisite request, not done here.

## Boundaries and exclusions

* Issue states read live 2026-11-11: #1360 CLOSED (4 of 4 ticked), #1419 CLOSED (7 of 7 ticked), #1424 MERGED; #440, #80, #73, #144, #131, #132 and #1420 OPEN. Nothing is ticked, closed or opened here.
* Budgets as directed by Root: #80 C5 stays spent with no C6; #1360 and #144 extensions E1 and E2 are spent with three remaining each; no budget is drawn by this checkpoint.
* The separately admitted #132 forward-adoption candidate is the local, unpublished branch `test/demo-inventory-intake-qa-132-1111`, head `fdf0d3beb` (tree `dce948766fc328f685b328e2eedea756413341f6`), not an ancestor of `origin/main`. It adds one test-only 53-line change to `src/api/tests/test_staff_intake_api.py` on a merge of `3dbb79e90`. It is not merged functionality and not main acceptance; this checkpoint neither duplicates its combined inventory and QA diagnostic nor imports its tests. The combined inventory-managed staff intake to independent QA journey therefore stays unverified on main and is recorded as a gap owned by #132, resume point: #132 candidate disposition by Root, then a main refresh.
* No consent, Legal, identity, QA, live, deployed or accessibility acceptance is inferred from fixtures, SQLite, loopback servers or axe. No SQL Server, Docker, cloud, model, live service or private dataset is used.
* #1420 (resident-choice CSV expansion) waits for this checkpoint's later disposition.
* Original adverse and process records of the merged PRs (withheld or restored Review artifacts, late markers, historical blocked browser runs) are preserved and not re-qualified.

## Failure ownership map

* Capacity or handoff CSV, UI, role or journey failure: preserved raw; owners #80 (open) and #1419 (closed, criteria remain historical), plus #73 for the workbench and #440 for the checkpoint.
* Permit or consumption failure: owner #144 (open); no new extension drawn.
* Shared-store or importer failure: owner #1360 (closed, historical) with #80 for the importer and #440; no new extension drawn.
* A failure opens no new ticket, takes no free budget and gets no source fix, new test or refactor here; Root decides.

## Open questions for Root

* Admit creating a fresh private venv at `/tmp/ama-440-closure-venv-1111` with editable installs of this worktree's `src/core`, `src/agents`, `src/api`, `src/importer` and `playwright==1.64.0` (declared dev pin), with module-origin proof, as the only dependency step.
* Confirm that the 82-test whole importer suite is intended, or restrict it to `TransferFailureTests` plus `tests.test_import_exceptions`.
