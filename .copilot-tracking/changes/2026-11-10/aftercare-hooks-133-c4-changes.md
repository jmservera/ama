<!-- markdownlint-disable-file -->
# Changes: aftercare runtime hooks (issue 133, C4)

Status: implementation complete, validated at the targeted DEMO tier. Base (reviewed StageA parent) a05b7e6b29145e620ca70f69c6f3f5c00be493c2. Refs #133, #89, #134 only. No closing keyword and no criterion ticks.

## Planned input integration

* None performed. Main d52f20a5198de7269f39daf794911545aee01ced is NOT adopted and nothing was merged, rebased or copied from the held 132 candidate. A non-committing merge-tree prediction taken after the implement-start observation (root file c4-merge-tree-prediction.txt) shows a clean merge; it is evidence only.
* The prior WAIT132 shared-hook serialization is retained as history. The coordinator decision supersedes it only for this bounded integration because AftercareService does not consume 132 procurement or quality-intake contracts. This is not 132 acceptance, a correction budget transfer or a 132 repair.
* Budget: C1 to C3 spent and preserved. This is the single C4 debit. C5 remains and is NOT automatically authorized.

## Changes

* src/core/src/zava_forward/core/aftercare_store.py (new): DocumentStateStore, a narrow StateStore adapter over the existing Store/SqlStore document mechanism, one explicit `aftercare` document. Mutator runs once under the store lock and is never rerun. Failure classification re-reads the persisted value: unreadable or committed-unknown is UnconfirmedWriteError (never "not saved"), a different persisted value is a conflict, unchanged and uncommitted is a plain persistence error. Refresh errors are attached, never swallowed.
* src/core/src/zava_forward/core/sqlstore.py: `aftercare` added to DOCS. src/core/src/zava_forward/core/projection.py: `aftercare` added to STAFF_GET.
* src/core/src/zava_forward/core/aftercare_intake.py and aftercare.py: UNCHANGED (reviewed domain, HTTP, error and idempotency controls reused).
* src/api/src/zava_forward/api/server.py: composition, session-only actor, constructed home allowlist from the retrofit exercise scenarios (never homes=None), GET and POST delegation of /api/aftercare to the service, status mapping 201/200/400/403/404/409/503. No separate audit queue write (it would not be atomic with the document write); the service actions log in the document is the audit record.
* src/api/src/zava_forward/api/workbench.py: nav entry `#/aftercare`; checks/workbench-manifest.json lists it for Residents Liaison Officer, Retrofit Coordinator, Project Manager, Programme Support Officer. Existing role tuples only.
* src/api/src/zava_forward/api/web/app.js: api() copies data.errors; lazy `/aftercare.js` entry; route `#/aftercare`; sign-out resets draft. index.html: script tag. aftercare.js: workspace route with actor-keyed in-memory draft, request id and unresolved state preserved through validation errors, failures and route changes; the quality-note action is not offered.
* Tests and checks (new): src/core/tests/test_aftercare_store.py (35), src/api/tests/test_aftercare_served.py (8), src/api/checks/aftercare_browser_check.py. Updated: test_role_endpoint_inventory.py inventories; mypy ignore lists in both pyproject.toml for the two new untyped test modules.
* docs/reference/research/retrofit-synthetic-data/scenario-manifest.json: workbench recipe SHA de523e82... to 65522649...
* READMEs: src/core/README.md and src/api/README.md only. Shared KB index, log and checkpoint not touched (149 owns them).

## Validation (DEMO targeted tier, no full gate, no SQLite substitute for SQL)

* Core: test_aftercare 21, test_aftercare_intake 39, test_aftercare_store 35, test_bulk_edits 39, retrofit scenario consumers and retained store, test_sqlstore 18, test_sqlqueues 14, scenario manifest, needs inventory, generator coverage: all OK. Final targeted rerun: 95 tests OK (13 MSSQL skipped without SQL).
* API: aftercare served 8 and role/endpoint/static/nav inventory 23 OK. Full API suite: 2569 run, 537 skipped, 1 failure and 1 error, both in test_simulator_admin (hardcoded 2026-11-10T10:00:00Z expiry); identical 1 failure and 1 error on a baseline git-archive copy of a05b7e6b. Pre-existing and adverse; not caused by this work.
* Browser: aftercare_browser_check passes (error summary focus, constructed allowlist, uncertain save, draft and request id across route change, receipt focus, Unknown owner and denominator, 320px reflow, contractor no nav); workbench_browser_check passes. employee_workspace_browser_check and workspace_scripts_browser_check FAIL identically on the baseline copy (pre-existing, adverse, preserved logs). Axe and keyboard observations are constructed, not assistive-technology, WCAG or human acceptance.
* Static: Core and API ruff check and format clean; mypy strict Core 286 and API 214 files clean; node --check aftercare.js and app.js OK.
* Disposable MSSQL (heavy lock taken non-queued with flock -n after a fuser holder check showed none; own container, own databases, pinned image mcr.microsoft.com/mssql/server:2022-latest, --pull=never):
  * Attempt 1: launcher exit 0 but 13 errors; sqlguard refused the container because its label was not the guard TASK_LABEL. Preserved at root sql-133-hooks-c4-attempt1-refused-label-1110.
  * Attempt 2: 35 run, 1 error (test used a cursor as iterable on MSSQL, test bug fixed with fetchall). Preserved at root sql-133-hooks-c4-attempt2-test-bug-1110.
  * Attempt 3: 35 tests OK, 0 skipped, exit 0; owned container removed and no leftover databases. Evidence at root sql-133-hooks-c4-evidence-1110.
* Raw logs: root checks-133-hooks-c4-1110.

## Review-relevant limits

* The JSON Store is single-process; a second JSON instance on one file is not protected. Cross-instance protection is SQL only (documented). FileStateStore is not runtime.
* Excluded: optional AI concern pack and model calls, Finance/payment/procurement/quality/consent/hazard mutation, real households, DPO, evaluator, participant and legal approval, lifecycle acceptance, deployment or auth changes, push, PR and merge.
