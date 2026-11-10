---
title: Issue 149 coverage parent integration research
description: Prospective research for reconciling the reviewed parent 149 topic with current main by a normal merge, with a focused DEMO-tier qualification and a dated cutover-pack record
ms.date: 2026-11-10
---

## Status

Research executed (disposition `executed`) before the research-open witness record. Planning Readiness: Ready. Scope is parent 149's own integration candidate and #440 checkpoint input. It is not a feature redesign, not epic closure and not acceptance of any child.

## Provenance (read 2026-11-10 09:13Z to 09:18Z)

* Worktree `issue-149-ux-coverage-parent-1110`, branch `feat/demo-ux-coverage-parent-149-1110`, declared target `main`. At intake the tree was clean and the branch was `736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd` (the Root-verified local head and launch HEAD of the witness log).
* Local was an ancestor of the reviewed remote input, so `git merge --ff-only ae4b20007ec9bc1d4bd5dd3eef91445f29f5e50f` ran normally (no reset, stash, move, rebase or force). Input parent head `ae4b20007ec9bc1d4bd5dd3eef91445f29f5e50f`, tree `c3e755d07edf6a486ecd79b4083f193921d6ace4`.
* `git fetch origin` and `git ls-remote origin refs/heads/main` at 09:18Z: main `d52f20a5198de7269f39daf794911545aee01ced` (tree `a817c8480a08e319fcd5466d59ba5e6564af360f`), identical to the brief. No new base difference. Merge base `736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd`. Actual current source is that main.
* Prospective `git merge-tree --write-tree HEAD origin/main`: clean, tree `a9b51381c57eb233e8aae2371a3b8456e23147ab`, no conflict lines.
* Main is 5 commits ahead of the merge base: `1ee56da3a` (#1361 served import refusals with exception register), `fe59ef56a` rubric, `92a5f532b` (#1368 checkpoint), `3d708c588` (#1369 Held form draft download, #96), `d52f20a51` rubric.
* Parent is 5 commits ahead of the merge base `736561ba0`: `b471c56a0` (#1363, #233), `aaec7b0bd` (#1365, #231), `b135ba1d8` (#1366, #230), `5eb38c58f` (#1367, #153) and `ae4b20007` (#1372, #156).

## Delta analysis

Non-tracking paths changed by main since the base (24): `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`, `src/api/README.md`, `src/api/checks/held_form_download_browser_check.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/role-screens.js`, API tests (`test_exception_register`, `test_exception_register_screen`, `test_finance_grants_screens`, `test_form_held_download_api`, `test_form_staging_api`, `test_role_endpoint_inventory`), Core (`exception_register.py`, `import_refusals.py`, `sqlstore.py`, `store.py`, `test_import_refusals.py`) and importer (`README.md`, `pyproject.toml`, `__main__.py`, `exceptions.py`, `test_import_exceptions.py`).

Non-tracking paths changed by the parent (12): `docs/reference/README.md`, `docs/reference/log.md`, `docs/reference/research/ux/atlas-screen-trace.md`, `docs/reference/research/ux/customer-journeys/programme.md`, `docs/reference/research/ux/zava-forward-prototype-profile-review.md`, `src/api/README.md`, `src/api/checks/{atlas_tensions,programme_paging,role_screens}_browser_check.py`, `src/api/src/zava_forward/api/web/app.js`, `src/api/tests/{test_atlas_tensions_checker,test_handoff_read_guidance}.py`.

Overlap: three documents only (`docs/reference/README.md`, `docs/reference/log.md`, `src/api/README.md`); the prospective merge auto-merges them. No source file overlaps: parent owns `app.js` and the three checkers, main owns `role-screens.js`, `server.py` and Core/importer. The parent changes do not touch `docs/architecture/cutover-evidence-pack.md`, so the dated record is a pure addition at the end of the main version.

Source ownership (not reassigned): #153 `app.js`; #96 (main) `role-screens.js` and `server.py` Held download; #233/#231/#230 checkers; #156 design Markdown only. Pending #80 Closed CSV and #216 constructed report are not in main or in this input and are not copied.

## Baseline on the unmerged input (pinned tools, own environment)

Environment: Python 3.12.3, owned venv `/tmp/i149-1110/venv` with editable installs of this worktree's `src/core`, `src/agents`, `src/api[dev]` (ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0 pins; the global 0.17.3, 2.4.1, 1.64.1 and the editable installs pointing at another checkout were not used). Chromium 156.0.8078.4. Raw logs `/tmp/i149-1110/logs/B*.log`.

| Id | Command (from `src/api`) | Exit | Result |
| --- | --- | --- | --- |
| B1 | `unittest` of atlas checker, handoff read guidance, handoff api, role screens (two modules), programme screen, workspace paging, role endpoint inventory, workbench | 0 | 102 run, 4 skipped (the opt-in handoff browser cases, `ZF_BROWSER_TESTS` unset) |
| B5 | `ZF_BROWSER_TESTS=1` `unittest test_handoff_read_guidance` under `flock -n` | 0 | 9 run, 0 skipped: constructed transport rejection, session ended, navigation during pending read, success and empty unchanged |
| B2 | `ruff check .` and `ruff format --check .` | 0 | clean (137 files formatted) |
| B3 | `mypy` with no file selectors (configured `files`) | 0 | no issues in 215 source files |
| B4 | `role_screens_browser_check` default, 230, 231, 231q, 231p, 231qp; `atlas_tensions_browser_check`; `programme_paging_browser_check`, each under one `flock -n /tmp/ama-rpi-heavy.lock` admission with `ZF_AXE_JS` set | all 0 | atlas 362 PASS COMPLETE; paging 89 PASS; axe 4.10.3 ran in the five role-screen stories (the repository check verifies the pinned digest); paging and atlas print that axe is not run |

No baseline failure.

## Prospective commands for the combined merged tree (DEMO targeted tier)

Classification: focused tier. The merge itself changes no workflow, gate tool, dependency manifest (the importer `pyproject.toml` change arrived through main and is not edited here), Dockerfile, permission, secret, schema, SQL, deployment or security control by this candidate; main's already-reviewed content is not re-qualified as a new feature. The record states that basis. No `rpi-checks --all/--changed` run and no receipt, by owner decision.

1. Fresh editable installs of the merged worktree's `src/core`, `src/agents`, `src/api[dev]`; additionally `src/importer` only if an importer suite is selected.
2. API focused unit: B1 selection plus main-affected modules `test_exception_register`, `test_exception_register_screen`, `test_finance_grants_screens`, `test_form_held_download_api`, `test_form_staging_api`, with `PYTHONPATH=tests:../core/tests:../agents/tests`; then handoff browser cases with `ZF_BROWSER_TESTS=1`.
3. Affected Core and importer unit selectors that the merged main delta changed: Core `test_import_refusals` and the exception-register tests, importer `test_import_exceptions`; scenario or needs-manifest tests only if the merged tree changes a registered manifest source (neither parent nor main touches a registered recipe source, checked again at implement).
4. Configured `ruff check .`, `ruff format --check .` and file-less `mypy` from `src/api` with pinned versions. A file-scoped pass does not stand for configured typing.
5. Local synthetic HTTP and Chromium under one nonqueued `flock -n /tmp/ama-rpi-heavy.lock`: the B4 set plus main's `held_form_download_browser_check` (the one check that exercises main's `role-screens.js` and `server.py` change together with the shared shell). Axe classification is recorded per check (runs for the role-screen stories only).
6. Static review of the changed web files against the fetched Web Interface Guidelines (command.md, fetched in full on 2026-11-10 during research); no web source is edited by this candidate.
7. #1362: read-only handoff `handoff-1362-version-diagnostic-1110.md` and the issue 149 record. The constructed checker false positive (dd value masked by a `1` in a timestamp, `10` and duplicate-label misses) has an unknown correction balance and is not a product defect; no checker bypass, skip or weakened assertion; not resolved here. If a required check fails, publication stays blocked and the exact reproduction is returned.

Excluded and unrelated: PR 1371 Core `test_resident_showcase` token collision (separately diagnosed, no product change here, not waived, not fixed here); #80, #216; Azure, SQL Server, scanners, images, model calls; the complete local gate and any receipt.

## Document identities (blob at the input parent head, status as written)

| Document | Blob | Status |
| --- | --- | --- |
| BRD `agentic-retrofit-programme-brd.md` | `34d88395de86` | `draft` (ms.date 2026-10-24) |
| PRD `zava-forward-retrofit-programme-demonstrator.md` | `c788b917bafa` | `in-review` (2026-10-25) |
| Addendum `case_study_48_addendum.md` | `28c1924285ee` | ms.date 2026-11-08 |
| `src/README.md` (stabilization ladder) | `b6e13012a836` | ms.date 2026-10-27 |
| `atlas-screen-trace.md` | `40ad47a4991d` | ms.date 2026-11-10 |
| `customer-journeys/programme.md` | `bb6417d2a201` | `complete-bounded-contribution`; #156 design PROPOSED/PARTIAL/NOT APPROVED, M1 unresolved |
| cutover pack | `abdecf2ee74f` | existing record; sections are additive |

Document-qualified requirement anchors (PRD): SA-001, SA-003, SA-007, AC-034 (scope and reset, #230), AC-036 (owner, reason, receipt, #153), AC-040 (conflict and case rationale, #231 and #233), NFR-001; BRD NFR-008 and NFR-009. These are the only anchors used. None is promoted from draft or in-review.

## Child records read (state files in this tree, not inferred from counts)

* #233 and #231: unit and Chromium coverage, original adverse records and negative controls retained; independent assessments recorded elsewhere; correction authority unknown.
* #230: paging coverage native browser proof; an earlier attempt stopped on a busy lock (preserved as the original).
* #153: transport rejection guidance with no automatic retry and a manual refresh path; old hosted type failure and the PR body Medium preserved; CI D1 repair is additive.
* #156: proposed design only. M1 (empty page versus empty set) is unresolved and is not decided here; M2 was expected local-only context; process D1 witness passed, old d8 witness exit 1 preserved.

## Web guidance

Skill `.github/skills/web-design-guidelines/SKILL.md` read; the source URL fetched in full. Applicable to the changed web files (`app.js` hunk from #153 and `role-screens.js` hunk from #96) as a read-only review. Fluent semantics, content standard, reduced motion, native download or navigation and role boundaries are preserved by not editing them.

## Selected approach

Normal `git merge --no-ff origin/main` (a true merge commit, history and append-only entries preserved), resolve only genuine conflicts (none predicted), then add the dated cutover-pack section and the necessary index and log entries, then run the focused set above. A real defect or unrelated correction found stops the candidate for Root routing.

## Follow-ups

1. Independent exact-head assessment of the final local candidate before publication.
2. #1362 checker correction under a separately granted allowance.
3. #156 M1 owner design decision and named reviews; WCAG, assistive-technology and usability evidence.
