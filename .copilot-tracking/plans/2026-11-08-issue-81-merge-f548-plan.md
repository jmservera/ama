---
title: Issue 81 main f548b65f merge research, plan and details
description: Prospective research, plan and details for one normal merge of current main f548b65f into the parent (light preparation)
ms.date: 2026-11-08
task_slug: issue-81-merge-f548
parent_task: issue-81-merge-score-23b
status: prospective
---

## Research

* Start HEAD `34729c4f11e19757154b08e7a35df12b3ddf6a8d`, tree `d52dcb86259820926015409c1c57332a9da3faea`, branch `feat/controlled-lifecycle-integration-81`, ignored-inclusive clean, PR #1240 open to `main`. Preservation ref `refs/ama/issue81-pre-f548-merge` is set to the start head.
* Fetched `origin/main` `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (coordinator-declared checkpoint head, ranking #1239 and checkpoint #1267). Merge base `23b26a7f`. Incoming delta: 363 files, mostly `.copilot-tracking` records, plus ranking publication core and runner modules and tests, `store.py` (+46/-5), `server.py`, `role-screens.js`, API tests, `src/core/README.md`, `pyproject.toml`, `docs/reference/README.md` and `log.md`, the scenario manifest, the rubric score and `cutover-evidence-pack.md`.
* Dry `git merge-tree` shows exactly one conflict: `docs/architecture/cutover-evidence-pack.md`. Both sides changed the front matter `ms.date` to the same `2026-11-07` and both appended new sections after the same last line (main: #73 and ranking checkpoints; parent: the #81 alignment checkpoint with its re-alignment addendum). `store.py` auto-merges: the parent changed 8 lines (appointment area) and main 51 lines, disjoint.
* The merge-base evidence pack and the parent's own checkpoint section are append-only history.

## Plan and details

* Commit these records as PRE, recheck clean state and pinned main, then one `--no-ff` merge. No rebase, amend, reset, force, push or retarget; child #86 (local `43c9f466`) not merged or touched.
* Conflict resolution: keep the shared `2026-11-07` front matter unchanged to avoid inventing a date change; keep main's appended sections first byte-for-byte, then the parent's #81 section byte-for-byte. No text deleted. Verify the result equals main's file plus the parent's appended block.
* Proof: parents are PRE and `f548b65f`; every non-conflicting path blob equals main's (or the parent's where main did not change it); the rubric JSON blob and mode equal main's and parse; parent-owned `appointments.py` and `test_quality_procurement.py` blobs unchanged; `store.py` contains both sides' hunks; `git diff --check` clean; all prior `.copilot-tracking` files unchanged.
* Light checks only, in `/mnt/ama-gates/g81-main-f548-preparation-1108`: full `git archive` snapshot, scratch venv, own-source non-editable installs with import-origin proof, synthetic `ZF_DATA`, `PYTHONDONTWRITEBYTECODE=1`, external caches. Run unmasked: four core modules `test_quality_procurement test_gates test_hazard_referral test_resident_preview`, `test_ranking_publication` and `test_ranking_publication_runner` (excluding the 60,000-case queue benchmark, SQL and Azure), `test_assistant_release` with the documented PYTHONPATH, and strict mypy, ruff check and format as in CI for core. Installs only after a missing-import failure. No FULL, SQL, browser, Docker, scanner or model services.
* Final tier remains FULL. Light results are local observed only and are not acceptance. Original owner-blocked #1238 Pending/supersession policy is not implemented.
* One independent read-only critique before mutation; it is not acceptance.

## Amendment 1 (critique verdict Revise: one Blocking, two Non-blocking, all accepted)

1. `store.py` and `cutover-evidence-pack.md` are exempt from the blob-equality rule. For `store.py` prove that `git diff 23b26a7f HEAD` hunks and `git diff 23b26a7f f548b65f` hunks both appear in the merge (diff of merge against each parent equals the other side's delta). Every other path equals main's blob, or the parent's where main did not change it.
2. Use `git diff --check PRE HEAD`.
3. Python 3.12 venv with ruff 0.17.1 and mypy 2.4.0; run `ruff check .`, `ruff format --check .` and `mypy` from `src/core`, as in `.github/workflows/src-ci.yml`.
