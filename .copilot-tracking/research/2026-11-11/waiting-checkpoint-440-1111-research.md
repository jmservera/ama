---
title: Handoff waiting screen feature-wave checkpoint research (Refs #440 #83)
description: Read-only prospective research for the integrated-main checkpoint after PR 1444 (issue 83 staff handoff waiting screen) reaches main; plan-only launch
ms.date: 2026-11-11
---

## Status and disposition

* Research disposition: `executed` (read-only Git, source, diff and GitHub queries on 2026-11-11). Planning Readiness: `Ready` for a plan-only freeze. Nothing here is an observed result: no test, browser, install, Ruff, mypy, Node, push, PR, issue or board write ran, and no source, test, fixture, configuration or canonical pack file changed.
* Prospective and known trigger, not a new issue: existing issue 440 criterion "recurring checkpoints after every completed feature wave" and the dated issue 440 comment admitting this preparation. It is not a generic audit and does not repeat the earlier Quality campaign.
* Reused, not re-derived: the method of the pack section "Keyboard probe compatibility integrated-main checkpoint (2026-11-11, Refs #440 #132 #134)" (merged by PR 1440 at `b7d66e425310f3b0b051025bff580b8dca3879dd`, with decision-record child PR 1441) and the resident-choice and closure-wave prospective plans. Their observed results stay dated history. Their unknown or zero correction authorities stay unknown or zero.
* Candidate PR 1444 material is read as policy and source evidence only. It is UNMERGED and EXCLUDED from main acceptance. It is never described as observed on main.

## Identities read (2026-11-11)

| Item | Identity |
| --- | --- |
| Planning base and fresh `origin/main` | `7880b95b19525ff465cab27870ba9d55b57110a3` (a fetch at research time showed no movement). Trees: `src` `b78627c004af2117469b1aac5a30e538395145af`, `docs` `03a986b07689c46ac3f21fdadbf95b7e61ea32f3`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `.github` `0fc8e7647628658093899f132499e08e8ec4df7d` |
| Last keyboard compatibility checkpoint | PR 1440 merged at `b7d66e425310f3b0b051025bff580b8dca3879dd`, an ancestor of the base (verified with `git merge-base --is-ancestor`). Decision-record child PR 1441 (MERGED into the PR 1440 topic) amended ADR 0007, whose blob at the base is `541e0f72dd2c1b5ae6feb2439a9223331bcdd783`, still Proposed. The pack section sits in `docs/architecture/cutover-evidence-pack.md` (blob `304b4cde76151b37ca44ec480df17ea60115d722` at the base), after the closure-wave and resident-choice sections |
| Topic branch | `docs/handoff-waiting-checkpoint-440-1111`, created at the base, clean at start |
| Dependency PR 1444 (published) | OPEN, base `main`, MERGEABLE, 19 status contexts, published head `dd3c32910c3c5205a2cbedbe74608411c6f9f341`, 4 commits. The hosted API job `run 42984858029 / job 130403684801` ran 2850 tests with one failure and 603 opt-in skips (the table inventory expected 12 and found 13). Other 18 contexts passed per the issue 83 thread. A pass or failure is read live at admission, never inherited from this note |
| Unpublished local candidate | `441fd7edf8597972f79c8100caafc39d9afcd844`, tree `513c3f9d8f7ae7c0c78672aa9f1650e23f7451cd` (verified with `git rev-parse`), merge-base with the base equal to the base, four commits ahead (`8196c6e53` feature, `dd3c32910` original review, `7b30f4fde` D1 table inventory, `441fd7edf` D1 review). NOT published, NOT merged, NOT main. Tree ids of the candidate: `src` `f82975dfc345f1a3705d62e08819383f6dd7bfd5`, `docs` `8a9d7693f8b3e880e84614fb40a8a88dcccc9c78`; `infra`, `tools` and `.github` equal the base |
| Candidate blobs | `app.js` `7eb700feee7a3ff7fae05646b8b5bbb27713c49d` (base `734aab48bbf32292fb5d6668cbecfe7fff8b757a`); `test_handoff_waiting_view.py` `db0e3c64e17047a0eaccd8d38fb072bde595c23b` |
| Excluded planned work | Issue 153 HTTP-guidance planning commit `99f01d7b9dd9f9affba7bd2952f2e191de753332` (a plan only, no implementation; it also edits `app.js` and is gated on 1444 merging). Not read beyond its identity, not consumed |
| Issue states (read live) | #440 OPEN (criteria 7 and 8 unticked); #83 OPEN (criterion 3 unticked); #81 OPEN (parent epic; its checkpoint criterion unticked); #153 OPEN; PR 1444 OPEN; PR 1440 and PR 1441 MERGED. Nothing is ticked, closed or opened here |

## Latest issue 440 comments read as data

* The admission comment (dated 2026-11-11, `issuecomment-6791287080`) names PR 1444, the 441f exclusion, a pack update only after 1444 merges and the coordinator admits pinned merged-main execution, and no new issue, Quality campaign, full gate or acceptance tick.
* The keyboard wave delivery comment (`issuecomment-6788149810`) records the merged tree `a0c9931dcfc9daf52ea3bd13dcac8b356bae6784`, ADR 0007 blob `541e0f72...` Proposed, "continue only within bounded documentary limits", the unpublished connected-walk checker excluded with no remaining correction authority, and the issue staying open.
* The issue 83 comment dated 2026-11-11 records the D1 admission (one bounded test-metadata continuation, product JS/API/CSS/store/permissions byte-identical, the unknown historical product-correction allowance not reset). That unknown stays unknown; this plan grants none.

## What PR 1444 changes (candidate `441fd7ed`, from the local diff against the base)

Nine product-side paths and the original RPI records; `src/api` and documentation only. No Core, API, permission, store, CSV or schema file.

| Path in the candidate | Change | Surface it creates for a checkpoint |
| --- | --- | --- |
| `src/api/src/zava_forward/api/web/app.js` | New route `#/handoff-waiting` calling `handoffWaitingView`; `waitingRows` validator; fixed `WAITING_READ_ERROR` and `WAITING_DENIED` copy; "Handoff waiting times" link in both case-list headers; `route()` status text for the new hash | Client route and projection-consumption authority; navigation semantics |
| `src/api/tests/test_handoff_waiting_view.py` (new) | `WaitingViewText` (6, Node source cases) and `WaitingViewBrowser` (4, opt-in Chromium, behind the heavy lock) | Primary selector |
| `src/api/tests/test_accessibility_baseline.py` | Table inventory `12` to `13`, comment | D1 coupling the hosted run exposed |
| `docs/reference/research/ux/wcag-conformance-baseline.md` | Inventory 13 audit note, no conformance claim | Context |
| `src/api/README.md` | One section describing the screen and its limits | Documentation |
| `docs/reference/README.md`, `docs/reference/log.md` | Index and log entries | Knowledge base |

Behaviour read from the diff (candidate only, not observed on main):

* One read-only `GET /api/handoffs/unaccepted` with no `max_age_hours` query, so `approved_limit_hours` must be `null` in every row (the validator rejects a non-null value as malformed). No approved global waiting threshold is invented. Age alone is not lateness; the escalation column shows only server-supplied state (`escalated`, `needs_escalation`, `reasons`). Nothing is escalated automatically and no mutation exists.
* Failure semantics: `AbortError` and `401` render nothing beyond the loading status (the route is being replaced or the session ended); `403` renders the fixed denied alert naming a programme owner; every other error and any malformed payload renders the fixed read-error alert with no table and no raw server text. A valid empty array is a distinct state: scope text, "No unaccepted handoffs are visible to your role." and the recheck button, no table, no as-of line. A `Check again` button re-runs the view in all non-abort states.
* Distinct from the personal card: the "Handoffs waiting for you" card (`pendingHandoffs`, `GET /api/handoffs`) hides when empty and has its own `HANDOFF_READ_ERROR`; the new screen does not depend on it and states that it is not that list.
* Manual paths: each row links to `#/case/<id>` (percent-encoded); the screen says "Open the case to chase, escalate or withdraw". Existing CSV anchors (`/api/handoffs.csv` and `/api/handoffs/unaccepted.csv`) stay on the personal card and were not changed.

## Guarded route and projection authority on main (read at the base)

* Server: `/api/handoffs` returns `pending_handoffs(u)`; `/api/handoffs/unaccepted` and `.csv` share one branch that parses `max_age_hours` (400 on a bad value), calls `unaccepted_handoffs(u, max_age_hours=...)` and maps `PermissionError` to 403. Core `handoff_ageing` sets `approved_limit_hours=max_age_hours` and `limit_note="Approved escalation time not set (OD-09)"` when none is given. Role map: both paths are assigned the `handoffs` kind in `server.py`.
* Existing API tests (base): `test_handoff_api.HandoffApi` covers `sam` (200, rows), `rex` (200, empty), `kim` (403), a bad limit (400) and a POST (404). `test_role_endpoint_inventory` lists both routes and the CSV in its role matrix. No file of this guard layer is touched by PR 1444 (verified in the diff stat).

## Existing selectors derived from source (candidate for the new module, base for the rest)

Static counts come from an AST read of `def test*` methods per class on the candidate tree. They are expectations to compare with actual runs, not marks to force. No test was run.

| Id | Selector (existing, `src/api`) | Static expectation | Affected-surface reason |
| --- | --- | --- | --- |
| W1 | `tests.test_handoff_waiting_view` (`WaitingViewText` 6, `WaitingViewBrowser` 4) | 10 ran; browser 4 need `ZF_BROWSER_TESTS=1`, Chromium and the free heavy lock, otherwise skipped (not a pass) | The new screen: route, validator, zero versus failure states, recheck |
| W2 | `tests.test_handoff_read_guidance` (`HandoffReadGuidanceText` 5, `HandoffReadGuidanceBrowser` 4; `Served` 0) | 9 ran; browser 4 need `ZF_BROWSER_TESTS=1` and Chromium only. This class does NOT take the heavy lock (critique WC-01), so a busy lock will not skip it and only the preflight lock and memory check protects the machine | The personal pending card the screen must stay distinct from; also the home of the shared `Served` helper that W1 imports |
| W3 | `tests.test_unaccepted_handoff_download_ui` (`UnacceptedDownloadText` 4, `UnacceptedDownloadBrowser` 2) | 6 ran; browser 2 need `ZF_BROWSER_TESTS=1`, Chromium and the free heavy lock (the class takes it non-blocking and skips when busy) | Existing CSV links on the personal card; W1 imports its lock helper |
| W4 | `tests.test_unaccepted_handoff_csv_api` (`UnacceptedHandoffCsv` 13) | 13 ran | CSV serialization of the same projection |
| W5 | `tests.test_handoff_api` (`HandoffApi` 7) | 7 ran | Role guards, empty and refusal semantics of the projection |
| W6 | `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 24 ran (14 own plus 10 inherited from `Matrix` in `tests/test_role_matrix.py`; re-derive at the admitted main) | Route inventory by role |
| W7 | `tests.test_accessibility_baseline` (`Wcag22Baseline` 12), the whole module | 12 ran | The 13-table inventory coupling that failed on hosted CI; whole module because the original D1 requires the whole baseline |
| W8 | `tests.test_workbench.WorkbenchNavigation` | 5 ran | `route()` and header navigation changed in `app.js` |
| W9 | `tests.test_content_standard.CopyAudit` | 18 ran | `app.js` is an audited copy file; the new fixed alerts and scope copy sit there. Optional, see plan |

Reconciliation with the Root-reported figure: W1 to W5 total 45; W6 adds 24 for 69 (the PR 1444 body figure), and W7 adds 12 for 81 (the Root-reported figure with the whole accessibility baseline). That is one static reading that reproduces both Root figures; another reading using `test_role_screens` (8) and `test_role_screens_conformance` (11) in place of W6 also reaches 69. Root's exact command list is not available to this research, so the composition is NOT asserted. The admission amendment must carry Root's exact list. Root's 81 pass, JS, Ruff and mypy results are Root-reported candidate observations on `441fd7ed`, not read or reproduced here, and are not main evidence.

Not selected, with reasons: whole API suite, full gate, SQL Server, Docker, scanners, services, cloud, provider, model, default or private datasets (owner scope: no heavy gate). `test_role_screens` and `test_role_screens_conformance`: they scan `role-screens.js`, which PR 1444 does not change; included only if Root's own 81 composition requires them. `test_unaccepted_handoff_download_ui` stays in because it guards the CSV and the personal-card link copy that sits in the same `app.js` region.

## Source-qualified requirement, architecture and contract links

Revisions and status read at the base `7880b95b`. Identifiers collide across documents, so each is qualified by path, version, status and blob.

* BRD `BRD-2026-AMA48-001`, `docs/brds/agentic-retrofit-programme-brd.md`, v0.21.0, status `draft`, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`.
* PRD `PRD-2026-AMA48-001`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, v0.21.0, status `in-review` (`author-complete-unsigned-pending-review-and-owner-acceptance`), blob `c788b917bafaede215f326f0efc71e071a687f1c`. A second document, `docs/prds/proper-warm-retrofit-programme-demonstrator.md` (same `prd_id`, v0.13.0), reuses FR and AC numbers and is not cited.
* ADR 0003 Accepted with amendment (2026-10-15), blob `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 Accepted (2026-10-15), blob `956da1a3b804c803041fe2e8a312bd9f400273ae`; ADR 0007 Proposed (2026-11-04, amended 2026-11-11), blob `541e0f72dd2c1b5ae6feb2439a9223331bcdd783`. No ADR sets a handoff waiting threshold. ADR 0007 concerns staff-mediated contractor intake, stays Proposed and is context only. Re-read every blob at the admitted main.

Cross-feature contract and trace rows (proposed links for human confirmation, not owner-approved traceability):

| Anchor (document, status) | Statement summary | Relation to the screen, with limits |
| --- | --- | --- |
| PRD FR-011, AC-014, AC-036 (`in-review`) | Distinct handoff states; owner, destination, proposed or confirmed receiver and chase owner shown separately; unknown stays explicit; receipt is not acceptance | The screen shows proposed receiver and chase owner with "Unassigned" for absent values; partial, constructed fixtures only; confirmed receiver and destination are not columns |
| PRD FR-066, AC-120 (`in-review`) | Owned staff exception queue for unaccepted handoffs: reason, urgency, case, due or next-update time, accountable reviewer or chase owner | Partial. The screen has case, status, waiting time, due, chase owner and server reasons; it has no urgency and no next-update column and no accountable-reviewer column. This is a documented gap, not a defect claim: the owner has not said the screen must carry them |
| PRD FR-004 (`in-review`) | Shared work queue identifies unowned handoffs with visible definitions | Context; owner is #76 |
| BRD FR-018, AC-024 (`draft`) | A handoff completes only on named human acceptance; unowned and overdue cases are reported | Reporting is partial (age and due-based flag); no approved overdue definition |
| BRD BG-010 (`draft`, `Proposed`) | 100 percent accepted or escalated within approved times; baseline Unknown | Needs OD-09; not met or measured |
| BRD OD-09 (open) | Exception teams, response targets and out-of-hours routes; owner Housing and repairs leads | No approved time exists; the screen must not invent one. This is the deciding fact for the unticked #83 criterion |
| BRD NFR-009, AC-071 (`draft`) | Journey service-time measures with escalation and tested manual alternatives | Context; manual case links are the existing manual path |
| BRD FR-016, FR-017, AC-022, AC-023 (`draft`) | Exception handoff contents | Context only |

Contradiction flagged, not resolved: issue 83 cites "BRD FR-009 to FR-011" as its source references. In BRD v0.21.0 those numbers mean AI output labelling (FR-009), professional approvals (FR-010) and resident-record distinctions (FR-011); the handoff rows of the BRD are FR-016, FR-017 and FR-018 (AC-022 to AC-024). The PRD's FR-009 to FR-011 do match issue 83's intent. This is a source-reference drift in the issue text, owned by #83, not a product defect and not corrected here.

## Open owner issues compared before claiming any bug

* #83 owns the screen, OD-09 and operational acceptance (criterion 3 unticked). #81 is its parent epic and holds its own checkpoint criterion. #76 owns the shared work queue. #153 owns copy (planning-only candidate `99f01d7`, excluded). #149 and #233 own UX and role-journey acceptance. #134 owns the connected journey checker (unpublished candidate excluded in the last checkpoint, still excluded). #440 owns the cadence. No open issue owns large-queue performance, pagination or the urgency and next-update columns; those remain recorded residuals and are not new issues from this plan.
* A targeted search for open issues mentioning OD-09, waiting time, pagination or large queue returned only #83, #184, #220 and #360 (the last three are unrelated). No duplicate exists.

## Boundaries and residuals the checkpoint must keep

* No API, store, permission, architecture, ADR or requirement change. No actual OD-09 times, operational acceptance, manual assistive-technology test, reflow or zoom check, or large-queue performance measurement exists. The table renders every row (no pagination or virtualisation); responsiveness is unmeasured.
* Not proved by any local run: Azure or provider behaviour, real identity (the tests use fixture roles `sam`, `rex`, `kim`), human or resident acceptance, root #83 criterion 3, whole #81 or whole #440.
* The earlier initial Chromium run that selected the primary checkout and the later minute-precision negative age validator rejection are original adverse history in PR 1444 and stay unaltered.
* The unknown historical correction balance stays unknown, and no new correction batch is granted by this checkpoint. A failure found at admission returns to Root, not to a fix here.

## Planning hazards found

* `W1` imports `Served` from `test_handoff_read_guidance` and `heavy_lock_or_none` from `test_unaccepted_handoff_download_ui`; those module imports must resolve from the worktree path. The earlier host problem (editable installs pointing at the primary checkout) means a module origin proof is a preflight step.
* Browser cases skip, not fail, when `ZF_BROWSER_TESTS` is unset, and the W1 and W3 classes also skip when the heavy lock is busy (they take it non-blocking themselves). The W2 browser class takes no lock. A nonzero skip count in W1 to W3 must be treated as not-a-pass for browser evidence.
* If PR 1444 merges by squash, the merged `src` tree must be compared with the candidate `src` tree `f82975df` before any candidate observation is read as the same code. PR 1444 may also gain commits (it already moved from `dd3c3291` to a local `441fd7ed`) and main may move for other reasons; any such movement is recorded before the first test.
