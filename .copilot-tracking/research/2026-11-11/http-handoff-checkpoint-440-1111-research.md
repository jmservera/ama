---
title: Personal handoff HTTP guidance checkpoint research (Refs #440 #153)
description: Read-only prospective research for a scoped integrated-main checkpoint after PR 1449 (issue 153 personal pending-handoff HTTP guidance) reaches main; plan-only launch
ms.date: 2026-11-11
---

## Status and disposition

* Research disposition: `executed` (read-only Git, source and GitHub queries on 2026-11-11, around 10:15 UTC). Planning Readiness: `Ready` for a plan-only freeze. Nothing here is an observed result: no test, browser, install, Ruff, Node, push, PR, issue or board write ran, and no source, test, document or canonical pack file changed.
* Trigger, not a new issue: the recurring checkpoint criterion of existing issue #440 after the completed feature wave of PR 1449. It is the same handoff integration surface as the merged waiting-screen checkpoint, not a historical architecture or Quality audit. The latest #440 comment (`issuecomment-6793077295`, 2026-11-11T10:12:12Z) admits only this prospective Research and Plan.
* Reused, not re-derived: the method of the pack section "Handoff waiting screen integrated-main checkpoint (2026-11-11, Refs #440 #83)" (published by PR 1448 and read at `docs/architecture/cutover-evidence-pack.md` lines 7148 to 7211). Its observed results stay dated history. Its unknown historical product-correction balances stay unknown and this work grants none.
* Candidate PR 1449 material is read as policy and source evidence only. It is UNMERGED and EXCLUDED from main acceptance, and is never described as observed on main.

## Identities read (2026-11-11)

| Item | Identity |
| --- | --- |
| Planning base and fresh `origin/main` | `ab44d42faae8dc3e69d2a149a067a29aca59f5e0` (PR 1448 squash merge; a fetch at research time showed no movement). Root tree `ba4a258c6958016288400d25577f32aa527191b6`. This is the actual `origin/main` Root recorded at worktree creation |
| Base per-directory trees | `src` `f6d487b51ce3314d732cab87a91844fe221a6e38`, `docs` `435e0b50828a6928fc0f78cf6ce2a08ac248c5a2`, `infra` `a022907662e2a98374f36d8f641eefd29d0dc798`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `.github` `48577d6868c72b11eb872133064883dc10c63cee` |
| Topic branch | `docs/handoff-http-checkpoint-440-1111`, created at the base, clean at start. The git author email already set repo-locally is `8036360+jmservera@users.noreply.github.com`, equal to the authenticated `gh api user` id and login |
| Last waiting checkpoint | PR 1448, merged; its pack section and the log entry are the previous checkpoint. Observation pin `ef3e00ad05a78c3a0fd3b342b860fb3d43796223` (PR 1444 squash), 86 tests, zero skips there. Immutable canonical record per the #440 comment `issuecomment-6792639329` |
| Candidate `src` tree | `2db08d8e2:src` is `bb7a461f0acc9ccff0cde8ddb16df3717c552c50`; the candidate root tree predates PR 1448 documentation and is expected to differ from main's root tree |
| Candidate PR 1449 (published) | OPEN, not draft, base `main`, MERGEABLE, frozen head `2db08d8e2141d60a52d688b731f192972ca8293b`, tree `e328d3eb18d69cc58293e2200eb9a0b51f377322` (verified with `git rev-parse` in the read-only 153 worktree). Hosted state read live: 15 contexts, six completed and successful at read time, `agent`, `src-namespace`, `mssql`, `src-core` and `src-api` in progress, `rubric/score` pending, and `src-agents`, `src-orchestrator`, `src-importer` successful. No hosted check is called green here |
| Candidate lineage | Planning head `99f01d7b9`; ordinary adoption of `origin/main` at `e5168fe9eaca0d168df010da6e8e8b8eb5dd8270` by `7965d6a38`; implementation `2db08d8e2` ("fix(web): guide HTTP refusals on the personal handoff card"). The candidate predates the merge of PR 1448; `e5168fe9e` to `ab44d42fa` changes only `docs/architecture/cutover-evidence-pack.md`, `docs/reference/log.md` and `.copilot-tracking/` files (verified with `git diff --name-only`), so the candidate's `src`, `infra`, `tools` and `.github` inputs relative to main differ only by the two product-side files below |
| Issue states (read live) | #440 OPEN, #153 OPEN, PR 1449 OPEN. Nothing is ticked, closed or opened here. The 153 candidate state file records its own process history |

## What PR 1449 changes (candidate `2db08d8e2` against base, source and tests only)

`git diff e5168fe9e 2db08d8e2 -- src` lists exactly two paths, and the diff from the current main to the candidate adds nothing else outside `src/api`.

| Path | Candidate blob | Main blob at base | Change |
| --- | --- | --- | --- |
| `src/api/src/zava_forward/api/web/app.js` | `7971ac3a1ab3150fef23ad46e45cb8d0ea0f4e3e` | `7eb700feee7a3ff7fae05646b8b5bbb27713c49d` | New constant `HANDOFF_DENIED` and a `fail` helper in `pendingHandoffs` (personal pending card). A non-array 200 body now paints the fixed `HANDOFF_READ_ERROR` alert instead of hiding the card. The catch keeps abort silent, keeps the existing 401 text, paints `HANDOFF_DENIED` for 403 and the fixed read error for every other error (no server text reaches the page). Success markup, both download links, empty hiding and loading text are unchanged. Six lines in the diff |
| `src/api/tests/test_handoff_read_guidance.py` | `0ac5639b3810bb789d9a1dc46c4892006dae7322` | `9bd12fc235d8e2d8f035f518e6b4d52708f6c1ce` | `HandoffReadGuidanceText` (8 Node cases) and `HandoffReadGuidanceBrowser` (7 opt-in Chromium cases with constructed 403, 500 and malformed route responses), 15 tests in the module; two intended contract changes of old assertions. No API, server, role, schema, CSV, #83 screen or content-standard edit |

Surfaces the change creates for an integrated-main observation: the personal card's consumption of `GET /api/handoffs` (transport, 401, 403, other HTTP, malformed success, empty, rows), the card's coexistence with the unchanged CSV links and the #83 staff screen, and the audited copy in `app.js` (the content-standard audit reads `app.js`).

## Selector resolution (static reads of the candidate tree; counts are expectations, re-derived on actual main)

| Module and class | Tests | Lock ownership read from source |
| --- | --- | --- |
| `tests.test_handoff_read_guidance` (`HandoffReadGuidanceText` 8, `HandoffReadGuidanceBrowser` 7) | 15 | The browser class has no lock in `setUpClass` (it only starts Playwright and Chromium), so it needs an OUTER non-queued shared heavy lock; the 153 candidate ran it under `flock -n /tmp/ama-rpi-heavy.lock` |
| `tests.test_unaccepted_handoff_download_ui` (`UnacceptedDownloadText` 4, `UnacceptedDownloadBrowser` 2) | 6 | `heavy_lock_or_none()` takes `/tmp/ama-rpi-heavy.lock` with a non-blocking `flock` in `setUpClass` and the class skips when busy; NO outer lock (an outer lock forces a skip) |
| `tests.test_handoff_waiting_view` (`WaitingViewText` 6, `WaitingViewBrowser` 4) | 10 | The same `heavy_lock_or_none()` helper; NO outer lock |
| `tests.test_handoff_api` (`HandoffApi`) | 7 | Not browser; no lock |
| `tests.test_unaccepted_handoff_csv_api` (`UnacceptedHandoffCsv`) | 13 | Not browser; no lock |
| `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 24 (14 own plus 10 inherited from `Matrix` in `tests/test_role_matrix.py`) | Not browser; no lock |
| `tests.test_content_standard.CopyAudit` | 18 | Not browser; audits `app.js` copy |

The module `test_handoff_waiting_view` imports `SAM` and `Served` from `test_handoff_read_guidance` and `heavy_lock_or_none` from the download UI module, so all three browser modules share one helper surface. Root's prior counts (7 + 13 + 24) agree with the static counts. The 153 candidate observed, as historical candidate observations only: 149 non-browser tests with 13 opt-in skips, the new module 15 with zero skips under the outer lock, the download UI 6 with zero skips, and the waiting view 10 with zero skips, both without an outer lock.

## Contracts the touched surface relies on

* Role guard and projection for `GET /api/handoffs` (`server.py` route table, `"/api/handoffs": "handoffs"`) and the CSV export `GET /api/handoffs.csv`: unchanged by PR 1449, but the card's new 403 and 500 mapping depends on them. The API tests (7, 13, 24) cover roles, refusal, projection and the inventory.
* Browser 403 and 500 in `HandoffReadGuidanceBrowser` are constructed `page.route` responses, not backend-produced permission statuses and not live acceptance. A real non-staff 500 from an uncaught `PermissionError` in `pending_handoffs` is existing server behaviour left unchanged (candidate Review item R3).

## Document-qualified requirement trace (re-read at base `ab44d42fa`; identifiers collide across documents)

* BRD `BRD-2026-AMA48-001`, `docs/brds/agentic-retrofit-programme-brd.md`, v0.21.0, `draft`, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`.
* PRD `PRD-2026-AMA48-001`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, v0.21.0, `in-review`, blob `c788b917bafaede215f326f0efc71e071a687f1c`.
* ADR 0003 (`docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, blob `d60645397b20fb70ac3d1dc47c7a6c8671201306`) and ADR 0006 (`docs/adrs/0006-src-layout-and-cutover.md`, blob `956da1a3b804c803041fe2e8a312bd9f400273ae`) Accepted; ADR 0007 (`docs/adrs/0007-contractor-intake-staff-mediated-proposal.md`, blob `541e0f72dd2c1b5ae6feb2439a9223331bcdd783`) Proposed and not exercised. No ADR sets a handoff threshold.

| Contract or requirement | Reading for the later record | Class at most |
| --- | --- | --- |
| PRD FR-011, AC-014, AC-036 (`in-review`): distinct handoff states, unknown stays explicit | The card now states unknown (not empty) for a refusal or malformed body; the scope is the personal card only | Local observed, synthetic, only if the listed tests pass |
| PRD FR-004 and the role guard | Existing guarded route and the role endpoint inventory (24); the refusal copy names an internal owner interpretation, not an approved access process | Local observed for the guard; no access process asserted |
| PRD FR-066, AC-120 | Not touched by this wave; urgency, next-update and accountable-reviewer columns stay a recorded gap owned by #83 | Implemented but unverified, partial gap carried forward |
| BRD FR-018, AC-024, BG-010, NFR-009, AC-071 (`draft`) | Manual case paths are retained by the refusal copy; no overdue definition exists | Context; no BRD item approved or met |
| BRD OD-09 (open) | No approved global threshold; nothing in the card sets one | Blocked; unchanged |
| Issue 153 acceptance slice | Refusal and error guidance for the personal card is slice C1 only; the candidate Review routed the named human wording review, universal C3 and C5 as unproved | Wording reviewed by no named human; not a plain-language or conformance claim |

Source-reference drift, already recorded for #83 (BRD FR-009 to FR-011 versus the handoff rows FR-016 to FR-018) is carried forward unchanged and not corrected here. Azure observed stays empty.

## Process history carried forward unchanged

* Candidate #153 native process history (from `.copilot-tracking/changes/2026-11-11-http-handoff-guidance-153-changes.md`): the first browser attempt had five failures from an overbroad test assertion (`Pat Test` legitimately appears in the case list) and the waiting-view browser class skipped because an outer lock wrapped a self-locking module; the native session corrected the test and reran lock, format and `PYTHONPATH` problems without pausing for Root; fresh Root verification is explicitly authorised separately, not retrospective permission.
* Waiting checkpoint (#440) history: the native unauthorized environment retry and the Root publication-sequencing and end-of-file check error stay historical qualified outcomes. This plan does not rewrite them.
* Candidate Root-run counts reported in the launch brief (raw 149 tests with 13 skips, 15 with zero skips, and 16 with zero skips, the last read as the 6 and 10 of the two adjacent modules, not separately derived here) are historical candidate observations, not current-main evidence.

## Planning conclusions

* The smallest justified observation after a merge is the new guidance module, the two adjacent browser modules, the three API, CSV and role selectors, the optional copy audit that reads `app.js` (Root's admission only), and `node --check` plus Ruff on the one changed test. The accessibility baseline (no table or `role` inventory change), the workbench navigation and the whole 149-module set are excluded without new concern.
* Execution dependency: PR 1449 actually merged AND Root's pinned-main amendment.
