---
title: Issue 89 parent main-adoption integration research
ms.date: 2026-11-10
---

## Task and boundary

* Task: `issue-89-main-integration-1110`. Prospective, bounded input adoption: bring the published parent branch `feat/demo-quality-workflows-89-1109` (published head a05) and current `origin/main` (a600) together by ordinary merge, preserving both intents. Not new product work, not a correction pool, not a pool of any kind.
* Root selected this independently of held #132. Route evidence: `demo-parent89-and-wave-route-1140.txt` and fresh `issue89/133/132-parent-route-1140.json`. Issue 89 body: Dependencies "None"; open-child and #440 checkpoint criteria gate epic closure, not a partial `Refs #89` publication. #133 comment 6764234616 supersedes the earlier hook serialization wait; #133 does not functionally depend on #132.
* Out of scope and unchanged: whole #89/#133/#132/#134 criteria stay unticked; no #132 C6, #133 C6, #132 consumption, legal, resident, evaluator, model or live approval is granted or inferred; #133 is not retargeted; the frozen #133 candidate (0850565...) is not cherry-picked, merged or touched.
* Research disposition: executed. No integration edit has occurred at the time of writing.

## Source identities (observed)

* Local start head `a8593a7a8670aab27329a81fedee605b4913e7e9` (rubric score commit on main lineage), clean, branch `feat/demo-quality-workflows-89-1109`.
* Published parent `origin/feat/demo-quality-workflows-89-1109` = `a05b7e6b29145e620ca70f69c6f3f5c00be493c2` (`feat(aftercare): stage controlled intake and honest recovery components (#1338)`). Local head is an ancestor of it: 0 ahead, 1 behind, so a fast-forward-only step is possible.
* Main `origin/main` = `a6002219581b983132465e9dd1680f78e6aca542`, tree `c04d01256c3ab69ebc2cb7c747aea05e57315ccf`. It differs from e951c523 (tree `9dad912b361e46d819746d299ee8c663b5b27d76`) only in `.github/rubric/scores/latest.json`. The merge base of a05 and a600 is `a8593a7a8`; main is 30 commits ahead of it and the parent is 1 ahead.

## Delta and overlap (observed with Git)

* Parent-side delta (a8593a7..a05): 28 files. Non-tracking: `src/api/src/zava_forward/api/web/aftercare.js`, `src/api/tests/test_aftercare_screen.py`, `src/api/tests/test_accessibility_baseline.py` (2-line change), `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/tests/test_aftercare_intake.py`, `src/core/README.md`, plus `docs/reference/log.md` (15 lines) and `docs/reference/research/ux/wcag-conformance-baseline.md` (1 line), and tracking artifacts.
* Main-side delta (a8593a7..a600): 478 paths including 419 tracking files and about 59 non-tracking files (API server/progress/web, Core forms/store/sqlstore/resident decisions, importer, agents, tools witness, docs).
* Path overlap of the two sides is exactly `docs/reference/log.md` and `src/core/README.md`. No runtime source file (server, store, route) is touched by the parent side.
* `git merge-tree --write-tree` of a05 and a600 is conflict-free and predicts tree `08fb66ce707518ddedb33dd53ed8362171869284`; `docs/reference/log.md` and `src/core/README.md` auto-merge. The main hunk in `src/core/README.md` is the #1238 pending-supersession paragraph (near line 534); the parent hunk is the Stage A paragraph (near line 4815). They do not intersect.

## Route and risks

* Plan: apply the published parent by fast-forward only, then an ordinary two-parent merge of a600. No rebase, force, reset, amend, history rewrite or hook bypass. No change beyond what the two sides already contain.
* Risk R1: the log is append-only; the auto-merge must keep every entry from both sides. Check by comparing the log blob against both parents (every line of each parent present, order of each preserved).
* Risk R2: `test_accessibility_baseline.py` and the WCAG baseline were edited by Stage A while main changed `app.js`/`role-screens.js`; they must be exercised, not assumed.
* Risk R3: the witness helper treats committed source changes before `implement-start` as a qualification, so `implement-start` is recorded before the fast-forward.
* Risk R4: a base move of main during the work changes the pin: inspect and report, do not chase.
* Any conflict or defect needing design or source repair beyond mechanical preservation is a STOP/HOLD with raw reproduction; no correction is granted.

## Owner demo targeted tier (verification plan)

* Core: `test_aftercare_intake` (Stage A), `test_aftercare`, resident adopted/showcase tests (`test_resident_decisions`, `test_resident_showcase`).
* API: `test_aftercare_screen`, `test_accessibility_baseline`, `test_static_assets`, `test_auth`, `test_role_endpoint_inventory`, `test_role_screens_conformance`, `test_simulator_admin`, `test_live_control`.
* Configured Core and API `ruff check`, `ruff format --check` and `mypy` from each project's own configuration.
* Browser: main-changed progress/workbench browser results recorded at e951 (217 local + 58 browser) are consumed with matching tree identity (a600 tree differs from the e951 tree only in the rubric score file) and not re-run as a campaign. A maintained aftercare browser check does not exist at base Stage A (the screen module is unwired); the hooks that serve it arrive with the child, so this is labelled a baseline unavailable, not a pass.
* Not run: full gate, `--changed`, SQL/MSSQL, four-image, model, cloud, private `ZF_DATA`, assistive-technology tests. Own isolated venv `/tmp/i89-1110`; no shared PYTHONPATH.

## Planning readiness

* Planning Readiness: Ready. Evidence is sufficient: identities pinned, merge predicted conflict-free, overlap known, validation tier defined by the owner.
* Follow-up routing candidates (not started): Root adopts the advanced parent into child #133 explicitly, tests the actual combined tree, publishes the child PR to the parent, then the real parent-to-main PR.
