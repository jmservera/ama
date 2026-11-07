---
title: Issue 73 workbench integration research (exception screen child 135)
ms.date: 2026-11-07
---

* Task: `issue73-workbench-integration`. Parent epic: #73. Child: #135 (its actual GitHub parent is #73, not #123; confirmed by `gh api issues/135/parent`).
* Worktree `/home/azureuser/source/ama-wt/parent-73-demo`, branch `feat/workbench-integration-73-demo`, HEAD and base `23b26a7f3a4693cd20dcf0447303d97491096cb3`. `origin/main`, fetched read-only on 2026-11-07, is the same commit.
* Research disposition: executed (documents, GitHub issue metadata and git objects only). No browser, server, SQL, model, network-write or heavy check was run, and the child worktree was not read or touched.
* Planning Readiness: Ready for a plan whose implementation is blocked on the child gate (see Gate state). Whole epic #73 remains unproven.
* Native CLI session UUID for same-loop continuation: `5e422939-d4f9-4204-b326-9d199592fa1f`.

## Evidence read

* Required knowledge base: `docs/reference/README.md` (index), `docs/reference/memory.md` (context only, not evidence), `docs/case_study_48_original.md` and `docs/case_study_48_addendum.md` (framing; no addendum change planned).
* Actual issue bodies via `gh`: #73 (OPEN, labels epic, brd, prd, area:case-workbench, status:partially-delivered) and #135 (OPEN, feature, status:not-started label). #73 sub-issues: #74, #76, #79, #80, #135 open; #78 closed. #135 blocked_by: none recorded as GitHub dependencies; its body lists #80, #84, #122 as dependencies (text only).
* Source at base: `src/api/src/zava_forward/api/web/role-screens.js` (host `roleScreensView`, `registerRoleScreen`, `screenManagers`, data-operator screen at lines 854 to 861), `src/api/src/zava_forward/api/server.py` (route at line 620), `src/core/src/zava_forward/core/exception_register.py`, `src/core/README.md` (exception register section, lines 4572 to 4592), `src/api/tests/test_exception_register.py` (classes `Register`, `Config`, `Endpoint`), existing `src/api/checks/data_operator_browser_check.py` (#229 case-derived screen, not `/api/exceptions`).
* Frozen child candidate read from shared git objects only: commit `26ce7c711ebffb37129fe0ca24b7b94c0d8356e1`, tree `ccf89ee645b2cb00c9662ae6d42ded586e4ea9c7`, parent is this base. Diff: `role-screens.js` (+96/-1), `test_data_operator_screen.py` (+8), new `test_exception_register_screen.py` (+221) and the child's dated RPI evidence. No server, store, auth, schema, model or infrastructure file.
* Current open PRs (observed 2026-11-07): #1239 (ranking publication runner, touches `src/core/.../store.py` and core tests), #1240 (controlled lifecycle integration, touches core `store.py`, gates, quality, procurement), #1222, #1141, #1243, #1242, #1235, #1216. None touches `role-screens.js`. `Store` is the host of `exception_register`, so #1239 and #1240 are potential dependents (see Risks).

## Document-qualified identifiers (do not mix)

* Issue #73 cites BRD BG-011, BRD FR-001 to FR-007, FR-032, FR-034, NFR-003 and PRD FR-001 to FR-007, FR-032, FR-034, SA-001 to SA-010. Cite as `BRD::FR-034` and `PRD::FR-034`; the numbers do not name the same text across documents.
* Issue #135 cites PRD FR-029 and AC-040 (PRD FR-029 is the import contract; AC-040 is the source-conflict comparison). Neither FR-029 nor AC-040 is in #73's requirement list. The only direct overlap with #73 is PRD FR-034 (queue, case, history, source trace and suggestion views agree on ownership, reason, evidence and explicit unknowns) and PRD SA-003 (blocked steps show reason, named owner and next action), which are mapping observations by this research, not proven acceptance.
* #73's body wording "The mvp/ application already delivers ..." is historical. The current source is `src/`; the legacy directories were retired (ADR 0006, archive `v0.21.0`). Nothing is recreated under legacy paths.

## What the existing producer and view authority establishes (source-observed at base, not re-run here)

* `GET /api/exceptions` calls `Store.exception_register(user, staff_from_env(env))`; `PermissionError` becomes 403 `{error}`.
* With no `ZF_EXCEPTION_STAFF`, only `MANAGER_ROLES` can read; the state is `roles_not_named` with empty items. With staff configured, only named emails can read. Every view and refusal is audited (`viewed_exception_register`), so a GET is read-only for domain data but not free of a ledger entry.
* Items are rebuilt on each read; nothing is persisted. Recovery is `null`; eligibility is always `Unknown`.
* Feeds delivered: source conflicts (both values with source, date, version), failed or quarantined AI runs and stranded tasks. Not delivered: failed-import producer connection, integration and identity-conflict producers, durable queue and recovery, health check (banner is `unknown`), named operational stewards and approved runbooks.
* Workflow-only (deliberate rules-and-template) processing raises nothing, so an empty list is neither an all-clear nor evidence of a model result. Failure or quarantine is a recorded exception; workflow-only is neither.

## What the child adds (frozen candidate, not yet accepted)

* One explicit link on the existing `data-operator` screen; the register is requested only when the hash carries `exceptions=1`, so the default screen load writes no audit entry.
* Renders state, banner, access, sources, unrouted, items and conflicts exactly as returned, with plain Unknown handling, placeholder runbook labelled as not approved, no winner among conflicting values, denied (403 server text), unavailable and malformed panels that never show prior rows, and `signal.aborted` rethrow so stale loads never render.
* Child evidence: 40 unit and static tests passed and the new tests fail without the feature. Child review (self, adverse items preserved) is Conformant for the slice with open items F1 to F6.

## Gate state (truthful)

* Running now in the child, NOT accepted: focused real-feature browser check, existing `Register` and `Endpoint` authority classes and native `--changed` gate. Independent exact-head assessment and merge into this topic have not happened.
* Shared heavy lock is reserved for #135; this launch starts no heavy, service or browser check and no duplicate of those checks.
* Child gate output is an input to this plan. It is not final parent integrated acceptance.

## Integration seams in the existing workbench

* Host: `roleScreensView` (`#/screens`) lazily loads `/role-screens.js` (app.js lines 344 and 423). The data-operator screen is registered for `screenManagers` (Retrofit Programme Manager, Programme Support Officer), which equals the roles that can see the `roles_not_named` view. A named non-manager steward is refused by the screen host before the API is reached (child F3, owner decision pending, no widening planned).
* Host contract change: `overview` now receives `(signal, rows, c)`. Existing `overview(signal)` implementations at lines 503 and 701 ignore the extra arguments; the child's conformance tests pass with them, but only a current-source run after merge proves it on the integrated head.
* Scope: the entry link uses `screenHref("data-operator", null)` so the `scope` query is kept and the case parameter is dropped; selecting a home drops `exceptions=1` (child F4). A refresh or back navigation with `exceptions=1` re-requests and re-audits.
* No parent change is required by research to make the child work in the existing workbench. Parent implementation is therefore verification and evidence of integration, plus at most a bounded browser-check extension and directly related documentation.

## Risks and limits (adverse, preserved)

* R1: child browser and authority results may fail or require child changes; the parent plan then waits and is refreshed, not bypassed.
* R2: if #1239 or #1240 merge first, `src/core/.../store.py` moves under `exception_register`; refreshed `Register` and `Endpoint` classes and the API suite must actually run on the integrated head, not be assumed from a rubric score.
* R3: the `ZF_EXCEPTION_STAFF` owner value is configuration, not an appointment. The screen says so; no named steward or approved runbook exists.
* R4: any need for backend, auth, store, schema, model, infrastructure or new dependency change reclassifies the work out of the focused tier. Stop and seek coordinator instruction; do not downgrade silently.
* R5: no human or assistive-technology acceptance exists (#151 and #155 are separate). Keyboard and narrow reflow are engineering observations only, not a conformance claim.
* R6: no legal, consent, financial, human or AT approval is implied by this work.

## Criteria status (all unproven for epic closure)

* #73 criterion 1 (scoped stabilization #440): UNPROVEN, not addressed by this loop.
* #73 criterion 2 (all children closed or owner-deferred): UNPROVEN. #74, #76, #79, #80 and #135 are open.
* #73 criterion 3 (each requirement has a passing acceptance check or recorded deferral): UNPROVEN.
* #135 criteria 1 to 5 stay unchecked. This slice contributes read-only display of conflict values and of failed or quarantined AI runs only; it does not prove an owned queue for failed imports or stranded tasks end to end, controlled audited recovery, preserved eligibility beyond Unknown, scoped operator access acceptance or live outage honesty.
* #80, #84, #122 foundations have bounded shipped engineering, not closed whole criteria.

## Follow-ups (current, evidence-grounded)

* Child gate completion and independent assessment (child owner).
* Owner decision on screen access for named non-manager stewards (child F3).
* Missing producers, durable recovery, named stewards and runbooks, role acceptance, human and AT observations (whole #135).
* Stabilization #440 and traceability before any epic closure.

## Refresh 2026-11-07 (post-child merge; supersedes the Gate state section only, earlier text is the preserved prospective record)

* Research disposition: executed again (source, git objects, GitHub PR metadata). Light local reading only; no browser, server, SQL, Docker, scanner or rpi-checks gate was run, and none is queued.
* Planning Readiness: Ready.
* Fetched 2026-11-07: `origin/main` = `23b26a7f3a4693cd20dcf0447303d97491096cb3` (unchanged from the prospective base). `origin/feat/workbench-integration-73-demo` = `d17aee537ec267162af106e14056440274ae589d`, tree `38ebb2da6b0499ffadcf29fd8ddfe675afdc564c`. The local topic was fast-forwarded to it (`git merge --ff-only`); the four owned untracked planning files were not in the incoming diff and are preserved byte-for-byte.
* Child gate input: PR #1257 (`feat/operator-exception-api-screen-135` into this topic, not `main`) merged 2026-11-07T17:59:43Z as squash `d17aee537ec267162af106e14056440274ae589d`; child original head `819022f858b3fdc4dfe20357304a5754221d5ed8`. Coordinator-reported: all 10 hosted checks passed, partial receipt reverified, functional review Pass and a coordinator all-rules web review with 2 low, 0 blocking findings. Those are inputs reported by the coordinator, not re-observed here, and not parent integrated acceptance.
* Merged diff against the prospective base: 15 files, +671/-1. `role-screens.js` blob `55f503d5952942d0fbed84deac38f9273cc06b23` (+97/-1), `test_exception_register_screen.py` blob `b05482b28f8dc94148423f1b882e090062762f94` (+233), `test_data_operator_screen.py` blob `e74271e3e89bdc8fb0bd2be6c8aa48cacbfa183a` (+8), plus the child's original and `r2-quarantine-label` RPI evidence (research, plans, details, changes, reviews, state). No server, store, auth, schema, model, infrastructure or dependency file.
* r2 correction in the merged child: quarantine detection is case-insensitive; a failed-AI item with no reason is labelled "How it failed is Unknown" instead of a fallback; a non-quarantined item with a reason is labelled a fallback (inferred from the feed contract, child finding R2-3).
* Host seam verified in source: `roleScreensView` line 81 calls `screen.overview(signal, data.items, c)`; the data-operator `overview(signal, rows, c)` (line 947) requests `/api/exceptions` only when the hash has `exceptions=1`, and `summarise` is reached through `this`. The other two `overview(signal)` screens (lines 503 and 701) ignore the extra arguments.
* Integration gap found: the child's renderer tests call `overview(signal, [], null)` directly on a fake DOM. Nothing exercises the real host path (`roleScreensView` role filter, `/api/cases` page load, `overview`, `show`) end to end, so a regression in host argument passing, the manager-only filter, the explicit-request rule or stale-navigation handling would pass the child's tests. One focused host-level node regression is justified.
* Sole actual FULL heavy holder is original #1231 (PID 591136) on ranking head 4ec plus parent fd57 over base 23b. This task starts no additional gate, browser, server, Docker, image, SQL, scanner or stress job and does not queue for the lock.
* Not edited: web source. Only a test and documents change, so the Web Interface Guidelines refresh is not required before edits; the Review records that the web file is unchanged from the child's reviewed head.

### Limitations carried forward (unchanged, open)

* #135: no failed-import, integration or stranded-task producers wired to intake; no durable controlled recovery; names, roles, runbooks and human, resident, professional, assistive-technology and live acceptance unproven.
* F3 manager-only host; F4 re-audit on refresh and back navigation; F5 provenance strings and no `translate="no"`; F6 placeholder guidance; more than 50 rows are rendered unbounded (`Infinity` limit) with no reproduced latency defect, a low follow-up.
* Child browser story: original UI helper expectation failures retained; the final 74-step PASS exited 0, but the intentional held-request abort printed a `CancelledError` on stderr and `pageerrors` was 0, which is not an all-console or pristine-harness proof.
* No actual model result was observed; fallback, quarantine and workflow-only are never successful AI.
* #73 and #135 criteria, #440 stabilization, #74, #76, #79, #80 remain open; no epic closure, tick or approval is implied.
