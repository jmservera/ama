# Research: aftercare integration (PR 1400) current-main observation (2026-11-10, Refs #440 #89 #133 #134)

Disposition: executed. Planning Readiness: Ready. Documentation only; no runtime, test, install, image, SQL, browser, cloud, model, live or private-data run, and no full gate.

## Scope and trigger

* New recurring #440 observation after the aftercare integration PR 1400 reached `main`. It is not the old CSV C6, not a retry, spends no source repair budget, fixes nothing and opens no issue. It is observation of proven source composition and retained evidence, not new runtime acceptance.
* Worktree `issue-440-aftercare-main-1110`, branch `docs/demo-aftercare-main-checkpoint-440-1110`, read at the start: HEAD `64c3f9191a2ffa97ef2dc07245422333ad4d6585` (PR 1400 merge), tree `8fbdaec7d138e360e9e460ad714742cb78b4d621`, status clean. Parent `1290aa557` is the Registry checkpoint (PR 1399) on main.

## Merge identity (read live with `gh`, 2026-11-10)

* PR 1400 `feat(demo): integrate delivery-quality aftercare persistence`, state MERGED at 15:56:55Z, merge commit `64c3f9191`, base `main`, head `feat/demo-quality-workflows-89-1109` at `b7e46b3be3d34734f49f0397c8c8022e920c1781` (tree `06ab5118310b662b57414772f7ba157e7bdec559`), no closing references, no labels. The updated body keeps `Refs #89`, `Refs #133`, `Refs #134`, restates the bounded scope and adds the Root exact-path qualification below.
* All 19 hosted status contexts on the PR read SUCCESS. They are PR-head observations. For main `64c3f9191` the run list read here shows only Graph Update pip in `/src/api, /src/core` completed with success and Capstone Rubric Scorer (push) in progress; nothing further is claimed green for main.
* Actual GitHub authored diff: 77 files, exactly the local authored diff from the merge-base `6cc59776`. The reviewer's cumulative two-dot packet of 98 files and 6,586 lines is a SUPERSET: 21 further paths are main-only documentation that the two-dot comparison shows as removed only because `b7e46b3be` predates later main. They are not authored deletions. The merged tree retains main-only documents, including the 1396 and 1399 checkpoint sections and log entries.
* Issues read live: #89 OPEN (epic; partially-delivered), #133 OPEN, #134 OPEN, #132 OPEN (`status:not-started`), #440 OPEN, #1401 and #1402 OPEN.

## Source identity: direct tree comparison (not inferred from ancestry or CI)

Compared with `git rev-parse <commit>:<path>` on the tested commit `b7e46b3be3d34734f49f0397c8c8022e920c1781` and on actual main `64c3f9191`:

| Subtree | Tested `b7e46b3be` | Actual `64c3f9191` | Equal |
| --- | --- | --- | --- |
| `src` | `c322b0f7a710c7f121fcd75b6685683ff57fa893` | `c322b0f7a710c7f121fcd75b6685683ff57fa893` | yes |
| `src/core`, `src/api`, `src/agents`, `src/orchestrator`, `src/importer` | `bc095465f75d`, `5bc36cda619b`, `a35f7e1d7fa9`, `d06c99144364`, `c6e324d1c3a0` | identical ids | yes |
| `infra` | `f7f31c0934cfe0bafb4505408706e55aa8ab61e7` | `f7f31c0934cfe0bafb4505408706e55aa8ab61e7` | yes |
| `.github` | `220ca5404c8a` | `e2ecbb8ea5b2` | no; `64c3f9191` equals its parent `1290aa557` (current main), so main's workflow and rubric state is preserved |

The dependency manifests live inside `src` (`src/core/pyproject.toml` `663adeb012ba`, `src/api/pyproject.toml` `1ae6604c812f`, identical in both commits). `git diff --name-only b7e46b3be 64c3f9191` outside `docs/` lists only main's tracking records and `.github/rubric/scores/latest.json`; no file under `src`, `infra` or `tools` differs. Source, runtime, test and dependency inputs are therefore exactly the tested tree. Equality of trees is a source identity statement; it does not turn the tests into runs on `64c3f9191`.

Aftercare blobs, equal in both commits: `aftercare_intake.py` `96674907da90`, `aftercare_store.py` `e5bd737c6d9b`, `aftercare.py` `115f639bc782`, `web/aftercare.js` `682457e40fd6`, `test_aftercare_intake.py` `b3f220bb1e11`, `test_aftercare_store.py` `475657d737ee`, `test_aftercare_served.py` `e451745bd707`, `checks/aftercare_browser_check.py` `d961c16af85c`.

PR 1400 against its parent on main (`1290aa557`) changes 77 files: 21 under `src` (`src/api` 13, `src/core` 8), 53 under `.copilot-tracking` and three documentation files (`docs/reference/log.md`, the scenario manifest recipe digest and the WCAG baseline). Source paths: API README, workbench manifest, `pyproject`, `server.py`, `aftercare.js`, `app.js`, `index.html`, `workbench.py` and their tests; Core README, `pyproject`, `aftercare_intake.py`, `aftercare_store.py`, `projection.py`, `sqlstore.py` and tests.

## Retained evidence consumed (Root session folder, not in the repository; read, not re-run)

Sources: `bounded-handoff-1959.md`, `pr89-current-main-qualified-1920.txt`, `handoff-89-current-main-adoption-1110.md`, raw `checks-89-current-main-adoption-1110/` (exit files, outputs, `SHA256SUMS`), and the independent same-reviewer `f73048c6-6054-4afb-9827-226d11ad13cd` report `independent-89-main-final-1913/functional` (`functional-findings.json`, `read-ledger.json`). All ran on the author's candidate `b7e46b3be` (adopted merge `a664e316`, tree `7af3d7fc`), not on `64c3f9191`.

* Core nine targeted modules and API 16 targeted modules, exits recorded per module. Observed counts include aftercare_intake 39, aftercare_store 36 with 13 SQL-gated skips, resident_decisions 371 with 132 skips and handoff read guidance 9 with 4 skips. Skips are not passes.
* First `test_device_registry_azure` run exited 1 (39 tests, 34 failures and 16 errors; SDK missing in the author's own environment). After installing the declared `azure-iot-hub` 2.7.0 and `six` 1.17.0 into that environment only, the single rerun passed 39 tests. Original red and the install log are retained.
* Fresh affected persistence SQL: 36 tests OK, zero skips, disposable MSSQL, image `sha256:cf8f0ab2`, worktree imports and sources hashed, container removed, no leftover databases. Rerun because Core dependency pins changed; not carry-forward.
* Ruff check and format clean; configured Core mypy 294 files and API mypy 223 files clean; `node --check` 15 files clean.
* Browser checks aftercare, workbench, workspace_scripts, employee_workspace, nomination and progress passed (207 PASS lines, 0 FAIL). Progress first failed with `FileExistsError` on the author's existing output directory; one justified rerun with a fresh output directory passed. Both outputs retained.
* Independent Functional verdict `approve_with_comments`: 0 Critical, 0 High, 2 Medium inherited and OPEN, no further blocker. Scope is the bounded synthetic demo, not release, high-volume use or closure. No infrastructure or `.github` candidate delta; the three baseline infrastructure mypy diagnostics are not introduced defects.
* Witness for the source run: seven records, verify exit 0, log hash `1a43156483ef5f21dc252244496818ff3f8b71a0eba82fd304f434ca80bbee9f`; a local writable record, not host or model attestation.
* Not run: infrastructure tests of main's delta, full Core or API discovery, full gate, `--changed`, images, provider, cloud, private data. Unknown: results of any check on `64c3f9191` itself, and hosted CI of main beyond the one completed run read.

## Requirement trace (document-qualified)

Documents at `64c3f9191`: BRD Agentic Retrofit Programme 0.21.0 `draft`, blob `34d88395de86`; PRD Zava Forward Retrofit Programme Workbench `in-review`, `exercise_status: author-complete-unsigned-pending-review-and-owner-acceptance`, blob `c788b917bafa`. Status is not approval; nothing was approved or decided here. The older PRD "Proper Warm" (0.13.0, `f7f9b7675e60`) is a separate document and is not the traced one.

* PRD FR-049 and AC-063 (closure independence; Not run): implemented in `AftercareRegister.record_closure` and the intake service closure actions; handover and financial closure never change a concern or remedy; unresolved concerns stay visible. Local observed for the constructed fixture only. Age bands owned by Housing/Complaints stay Unknown until set; lease evidence and leasehold text are not implemented in this surface.
* BRD FR-047 and AC-089 (closure cannot close a remedy); BRD FR-029, FR-030, RULE-013 (reopen, defect record, independent closure): the aftercare register keeps remedy status separate and completion needs evidence; the defect reopening workflow is a separate, earlier delivery and is not re-observed. BRD RULE-014: a sensor reading is context only and is never a basis or a dismissal (register and store restore refusals).
* PRD FR-014 and AC-017: concern types, owner, accessible and non-digital routes (phone, in person, paper, assisted visit) and representative basis are recorded; contact is not consent. A synthetic scenario owner is labelled as such and a missing owner is Unknown.
* PRD FR-036: the `aftercare-concern-pack` task is registered unapproved and disabled with a manual route; no model route is delivered.
* #133 criteria (all unticked): the staff-assisted intake, owner/outcome/remedy/closure view and neutral wording exist for synthetic data; the household or representative self-service route, evaluator role access, the DPO position on outcome data and a model concern pack are not delivered.
* #134 criteria: the perspective walkthroughs and AC-034 to AC-043 are unticked; three items are ticked in the issue as read (same-home journey, sibling and building isolation, constructed-fixture wording); this record does not attribute them to PR 1400. PR 1400 adds one staff screen route and its browser check; it does not claim any eleven-perspective acceptance.

## Boundaries observed at `64c3f9191` (static read)

* Contract: `AftercareService.handle(method, path, user, body, query)` is the route contract; `/api/aftercare` in `server.py` delegates through `_aftercare`, GET and POST only, with 201, 200 replay, 400, 403, 404, 409 and 503 as documented.
* Package boundary: Core owns the register, service and `DocumentStateStore`; API owns the route, the screen (`web/aftercare.js`), the workbench manifest entry and the endpoint inventory. `aftercare` is the only document added to `SqlStore.DOCS` and `projection.STAFF_GET`; Agents, Orchestrator and Importer are unchanged by this wave.
* Roles and human decisions: existing staff role tuples only; the Residents Liaison Officer and Retrofit Coordinator record, the other listed roles read, contractors and the Quality Inspector receive 403; owner actions are limited to the named synthetic owner; closure is manager-only. The actor comes from the session, never the request body. No new evaluator or resident account, portal, consent change or approval is created.
* Persistence and recovery: one validated JSON document per update, one atomic save; the mutator runs once; failure is classified by re-reading under the same lock; unconfirmed writes raise `UnconfirmedWriteError`, never "not saved"; a client retries with the same `request_id` and the service replays the receipt, a changed payload under that id is a conflict. The JSON `Store` is single-process; cross-instance protection is SQL only.
* Refusal, manual and recovery: field errors link to inputs; the draft, request id and unconfirmed state survive route changes and clear on sign-out; a late reply after sign-out or route change does not render or take focus; a `beforeunload` guard protects the in-memory draft; the paper and phone routes are the manual path; AI is off.

## Inherited open findings (read from the actual issues)

* #1401, Medium, OPEN: `aftercare_intake.py:378-379` sorts JSON keys, so `AC-1000` precedes `AC-101`, and restoration in `aftercare.py:195-198` relies on insertion order and sequential identifiers; the register cannot be restored at 1,000 concerns (StateInvalid, 503). The adapter also sorts (`aftercare_store.py:40-41`).
* #1402, Medium, OPEN: `aftercare_intake.py:267-269` treats an existing blank or whitespace `FileStateStore` document as a fresh register, so a later write could restart identifiers. Scope is the standalone `FileStateStore`, which the runtime does not use; the connected adapter is not shown to behave the same.
* Both bodies state source-repair execution is BLOCKED pending a finite owner grant (minimum remaining UNKNOWN, 0), no fresh five, and that the synthetic demo may continue only under the recorded nonblocking finding. This record neither waives them nor claims a fix. Their reproductions in the issue text are static reads of the cited lines and the reviewer's report; this task did not run them.

## Exclusions

Unmerged #109 and #111 sensor-draft parent (child PR 1395 merged only to the parent branch `bd2a649`; local #109 integration still running), the #144 legacy worker, #132 contractor job pack and fieldwork evidence capture (OPEN, not delivered, separately blocked), real-provider activation, actual Azure dispatch, and actual resident or professional acceptance. #89 acceptance does not depend on #132.

## Findings

* No new confirmed defect and no confirmed refactoring; the two inherited Mediums are already deduplicated into #1401 and #1402. No new issue is needed.
* Limits for the recommendation: constructed synthetic data; no accessibility-tool, WCAG, assistive-technology or human acceptance; no image, live, model, release or high-volume proof.

## Planning readiness

Ready: one dated section in the existing evidence pack, an index paragraph and an append-only log entry. The earlier checkpoints, historical records and original adverse results stay unchanged.
