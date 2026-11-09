---
title: Issue 81 main 1255 merge changes and author review
description: Changes, local observed evidence and one author Review for the normal merge of main c1a16482 into the parent
ms.date: 2026-11-07
task_slug: issue-81-merge-1255
status: complete-local
---

## Changes

* Start `6cae8cbeef8400392e7d9ab955b97d1799415f22`, tree `5ffea910e77ac1aca65381676b401cdc89f5220e` (ref `refs/ama/issue81-pre-c1a-merge`). PRE commit `32c041a4608055fef580a5551759051e96250c78` holds the plan, critique (Approve, one Non-blocking finding accepted) and Amendment 1.
* One normal `--no-ff` merge `7cdb5afd49065e7a01876fd15bb155e21b70c1fb`, tree `dacc8b2d9bcb7c0832b66d43aace04c315c9c86d`, parents PRE and `c1a164829e77efe45f5f002740bd79699b89b334` (PR #1255). No conflicts. No rebase, force, push, retarget or child change.
* Preservation proof: `git diff --raw PRE HEAD` (17 entries, modes and blob ids) equals `git diff --raw a1d26534 c1a16482`. Outside `.copilot-tracking` the three paths are `src/api/tests/test_assistant_release.py`, `tools/rpi-checks.py` and `tools/test_rpi_checks.py`. Zero raw diff under `src/*/src` and `.github`. `src/core/src` and `test_quality_procurement.py` identical to PRE, so the appointment correction and the child contributions are unchanged. `git diff --check PRE HEAD` clean. The evidence pack and all prior logs are untouched.
* The scorer run 42387247541 for `c1a16482` was still in progress. A later score-only descendant is not merged here and needs a separate admitted amendment.

## Local observed checks

Scratch `/mnt/ama-gates/g81-main1255-preparation-1107`: full `git archive` of the merged head, venv with Python 3.12, ruff 0.17.1, mypy 2.4.0, `env -i`, `PYTHONDONTWRITEBYTECODE=1`, external caches. Non-editable `--no-deps` core, agents and api installs. Origins resolve under the scratch `site-packages/zava_forward/{core,agents,api}`.

| Check | Exit | Result |
| --- | --- | --- |
| `test_backlog_sync` | 0 | 17 OK |
| `test_rpi_checks` | 0 | 86 OK |
| `test_ci_affected` | 0 | OK after `pip install pyyaml` (run 1 failed on the missing module, log kept) |
| ruff check and format over the five tools files, `mypy --strict` rpi-checks files, `mypy --ignore-missing-imports` backlog files | 0 each | clean |
| `test_assistant_release` with `PYTHONPATH=tests:../core/tests:../agents/tests` | 0 | 48 OK, 1 skip (`MssqlUnleasedRevocation`, needs SQL Server). Run 1 without the PYTHONPATH failed on the `release_support` import; log kept |
| core `test_quality_procurement test_gates test_hazard_referral test_resident_preview` | 0 | 233 OK, 1 skip (JSON-only separate-file audit ordering) |

## Review (author, one execution)

* Outcome: the merge is conformant locally; no material finding open.
* Limits: the SQL release-denial test did not run (skip), so there is no SQL claim. No FULL, SQL, browser, scanner, image, queue benchmark or service ran. Receipts for earlier heads stay historical and do not apply to this head, and none survive a child merge. This is author evidence, not independent, hosted, human, resident or legal approval. Hosted SQL does not select the new class. The four #81 criteria and the #440 acceptance stay unticked. #107, real AI, approver and attribution gaps stay open. The original Revise critiques stand.
* Next: align child #86 onto this parent head (no retarget), then a coordinator-chosen non-queued FULL with `--lock-timeout 0` on current main, then independent and hosted review.
