<!-- markdownlint-disable-file -->
# Research: bounded aftercare runtime hooks (issue 133, C4)

Date: 2026-11-10. Task slug: aftercare-hooks-133-c4. Parent task: assisted-aftercare-133-c3.
Research disposition: executed. Planning Readiness: Ready.

## Pinned source and exclusions

* Base: reviewed StageA parent a05b7e6b29145e620ca70f69c6f3f5c00be493c2 (PR1338, declared parent branch feat/demo-quality-workflows-89-1109). Worktree clean at launch.
* Current main d52f20a5198de7269f39daf794911545aee01ced is 28 commits ahead and touches server.py, app.js, sqlstore.py, store.py and the role inventory test. Main is NOT adopted. Any merge is a separate planned step after the implement-start observation; none is needed for this binding.
* Excluded: the held 132 candidate (never copied, not accepted, no correction budget transfer), any private dataset, real households, model or cloud calls.

## Authority and the retained wait

* Prior wait (WAIT132): shared 133 hooks wait for 132 C5 review and the parent merge. It is retained as written in the C3 state blocker `hook-continuation`.
* Supersession: the coordinator decided, from source tracing, that AftercareService does not consume 132 procurement or quality-intake contracts, and superseded only the shared-hook serialization for this bounded integration. This is not 132 acceptance. Parent 149 is metadata/docs only; server, app and persistence hunks are assigned to 133 for this loop.
* Budget: C1-C3 of 5 spent (latest comment 01:24, C3/5, two remain; the PR1338 body "C2/three remaining" is superseded). This work is C4, one debit. C5 remains and is NOT automatically authorized. Adverse and partial evidence of C1-C3 is preserved.

## Source findings

* `aftercare_intake.py` defines `StateStore` (`read`, `update(mutator)`), `AftercareService(store, homes, cohort, scenarios, now)` and the pure `handle(method, path, user, body, query)` route contract. Status mapping: validation 400 with `errors`, permission 403, missing 404, conflict 409, state-invalid and persistence 503. Receipt, register and request-id index are one JSON document; replay returns without a write.
* `FileStateStore` is an isolated-check adapter, not a runtime adapter.
* `Store` holds one RLock and `save()` writes the whole data file. `SqlStore` stores named documents (`DOCS`) in the `meta` table, with `_proc_sync` snapshots and a `_proc_write` compare in the save transaction raising ConflictError. A precommit non-conflict failure leaves in-memory documents unrestored. After commit a reload failure becomes `CommittedReloadError`; `_SyncLock` exit can raise after a commit. MssqlStore inherits the mechanism.
* `server.py` auto-registers `aftercare.js` as a static asset; GET kinds are governed by `projection.STAFF_GET` (unlisted paths are "unknown", denied); POST requires the CSRF header on a trusted proxy and is blocked for view-only users. Existing committed-outcome mapping is 409 with `outcome: committed`.
* `app.js` `api()` throws an Error with status, reasons, outcome; it does not copy `data.errors`. Lazy script registry `missingWorkspaceScripts` and `route()` host destinations. `workbench.py` `navigation()` lists links.
* `aftercare.js` submit maps 400/403 to refused and 401/409/other to unconfirmed retaining the request id.

## Design decisions (evidence for the plan)

1. Adapter `DocumentStateStore` over `Store`/`SqlStore`, one namespace `aftercare`, added to `SqlStore.DOCS`. The mutator runs once under the store lock; whole-document replacement. On failure, reconcile from the persisted value: uncommitted (equal to previous or explicit ConflictError) restores memory and reports nothing saved; committed or unknown reports a distinct unconfirmed error that chains the cause. The mutator is never rerun and a refresh error is never swallowed.
2. Composition: constructed allowlist of homes, cohort and scenarios only; never `homes=None`. Existing staff role tuples only. Actor from the session.
3. Server: `/api/aftercare` delegating to `handle`, kind `aftercare` in `projection`, audit convention retained, 503 for unconfirmed writes so the client keeps the request id and resends.
4. Front end: `app.js` copies `data.errors` onto the shared api error, loads `/aftercare.js`, keeps request id, draft and unresolved state in memory across validation errors, failures, route changes and session end; cleared on sign out or actor change. No browser storage.
5. Validation (DEMO targeted tier): Core service/store/SQL contracts, API route/asset/navigation inventories, browser checks, mypy, Ruff, node syntax, and a disposable owned MSSQL under the shared nonqueued heavy lock. SQLite is not a substitute.

## Boundaries

No quality-note action as concern intake, no AI pack, no Finance, procurement, quality, consent or hazard mutation, no new roles or accounts, no real lifecycle acceptance, no closure or ticking of 133, 89 or 134 criteria. Shared KB index, log and checkpoint are untouched (149 owns them).

## Web guidelines

The current Web Interface Guidelines source was fetched on 2026-11-10 (raw command.md, success) and loaded with the redesign skill; they will be re-applied at review.
