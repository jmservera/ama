<!-- markdownlint-disable-file -->
# Review: aftercare runtime hooks (issue 133, C4)

Executed once after implementation by the same worker (no nested agents). This is not the independent exact-head review; root performs that before publication.

Boundary: base a05b7e6b29145e620ca70f69c6f3f5c00be493c2 to the working tree of branch feat/demo-aftercare-hooks-133-1110.

Outcome: Conformant to the plan at the targeted DEMO tier, with open adverse items routed below. No finding is claimed closed beyond the evidence in the changes artifact.

## Plan conformance

* Adapter: one `aftercare` document in DOCS, whole-document update, single mutator run, unconfirmed and conflict mapping, refresh error attached. Contract tests pass on JSON, SQLite and a disposable MSSQL server (35 run, 0 skipped).
* Server: session-only actor, constructed home allowlist, existing staff roles, existing body limits and response conventions. Reviewed intake service and register unchanged.
* Front end: script served and routed, data.errors on the shared api() error, draft, request id and unresolved state preserved, no quality-note substitute.
* Inventories: endpoint, static asset and nav inventories updated; workbench manifest and scenario recipe SHA updated and Core manifest and needs checks pass.

## Web Interface Guidelines review (fetched 2026-11-10, retrieval succeeded)

Files: aftercare.js (workspace route, lines 298-373), app.js (lines 81, 345, 441, 1696), index.html (line 52).

* aftercare.js:72-73 - autocomplete off and spellcheck false on free-text fields: pass.
* aftercare.js:298-373 - labels and linked field errors via the existing form builder, focus moves to the error summary or status on failure, submit disabled only while the request runs, then re-rendered: pass.
* aftercare.js:332 - action is a `<button>` with a specific label: pass.
* aftercare.js:325 - draft is kept in memory across routes; no unsaved-change `beforeunload` guard. Low: a full page reload loses the draft (accepted, documented in the browser check).
* app.js:81 - errors copied onto the shared error: pass. No new transitions, outline removal, paste blocking or zoom restriction were added.
* Title Case guidance for buttons and headings conflicts with the repository plain-language standard (sentence case); the repository standard was kept.

Axe and constructed keyboard observations are engineering evidence only, not actual assistive-technology, WCAG or human acceptance.

## Findings and routing

* Pre-existing failures also present on baseline a05b7e6b: test_simulator_admin (1 failure, 1 error), employee_workspace_browser_check, workspace_scripts_browser_check. Routed to a separate follow-up; not caused by this change.
* MSSQL attempts 1 and 2 failed (guard label, test bug) and are preserved; attempt 3 passed after fixes.
* JSON Store is single-process, second-instance protection is SQL only. Documented limit.
* Not performed: full gate, independent review, hosted CI, push or PR, human, DPO, evaluator, participant or legal approvals, actual assistive-technology testing.
