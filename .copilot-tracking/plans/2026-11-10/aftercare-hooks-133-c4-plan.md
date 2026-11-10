<!-- markdownlint-disable-file -->
# Plan and details: aftercare runtime hooks (issue 133, C4)

Date: 2026-11-10. Base a05b7e6b (PR1338 StageA). Research: `.copilot-tracking/research/2026-11-10/aftercare-hooks-133-c4-research.md`. Refs 133, 89, 134. No closing keywords.

## Phases

* [ ] P1 Adapter. New `core/aftercare_store.py`: `DocumentStateStore(store, key="aftercare")` and `UnconfirmedWriteError(PersistenceError)`. Add `"aftercare"` to `SqlStore.DOCS`. No change to `aftercare_intake.py`.
  * `read()` under `store.lock`: canonical JSON of the namespace document, or None.
  * `update(mutator)`: under the store lock call the mutator once; unchanged text returns without a save; else set the namespace document and `store.save()`.
  * Failure classification by reading the persisted value (SQL `meta` row under `dblock`; JSON file key): equal to previous or ConflictError is uncommitted (restore memory, raise PersistenceError "Nothing was saved" or the service ConflictError); equal to attempted, CommittedReloadError, or lock-exit failure after save is committed or unknown (raise UnconfirmedWriteError chained, text "may have been saved; send again with the same request reference"); anything else, including a failed reload, is also unconfirmed. Never rerun the mutator, never swallow the cause.
* [ ] P2 Server. `App` builds the service with `DocumentStateStore(store)`, `homes` and `cohort` and `scenarios` constructed from `retrofit_exercise_scenarios()` (never None). `/api/aftercare[/...]` GET and POST delegate to `service.handle` with a user derived from the session (name, role); the body never supplies the actor. `projection.STAFF_GET` gains kind `aftercare`; POST uses existing gates (CSRF, view-only). Existing 8 MB body limit, audit call per write. 503 for unconfirmed writes keeps the retained request id on the client.
* [ ] P3 Front end. `index.html` script entry through the lazy registry in `app.js`; `workbench.py` navigation link `#/aftercare` for the existing view roles. `api()` copies `data.errors` onto the thrown error. `app.js` route builds the aftercare screens with the shared `api`, in-memory draft state `{requestId, values, unresolved, actor}` kept across validation errors, failures, route changes and session expiry, cleared on sign out or actor change; no browser storage. Evaluator readback uses existing `evaluator`/`concerns` routes only. Quality-note action is not offered as intake. Synthetic and unverified labels remain visible.
* [ ] P4 Tests. Core: adapter contract on JSON Store, SqlStore (SQLite) and owned MSSQL: restart, same-id replay, changed-payload conflict, two instances, precommit failure, committed-but-reload-unknown, lock-exit failure. API: served route tests (roles, 401/403, malformed body, home allowlist, actor from session, unconfirmed 503), endpoint, static asset and navigation inventories, content standard audited files. Browser check: keyboard intake, linked errors and focus, receipt focus, uncertain-save guidance, restart readback.
* [ ] P5 Validate (DEMO targeted tier): affected Core and API tests, mypy Core and API, Ruff check and format, `node --check`, scenario recipe SHA, Core scenario-manifest and needs-inventory checks as applicable, disposable MSSQL under `flock -n /tmp/ama-rpi-heavy.lock` after holder inspection with owned container only. Busy or missing means that validation is blocked and recorded. No full gate.
* [ ] P6 Docs. API and Core component READMEs only. No shared KB index, log or checkpoint.

## Risks

* `DOCS` addition changes seed-merge reports for the new key (only if present in the seed; absent in seeds, so no change expected). Verified by existing store tests.
* Main touches the same files; conflicts are not resolved speculatively. A non-committing merge-tree prediction is recorded after implement-start.
