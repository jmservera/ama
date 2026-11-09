---
title: Issue 81 main 1253 merge research and plan
description: Prospective research, plan and details for one normal merge of pinned main 39506027 (PR 1253 plus score commit) into the parent
ms.date: 2026-11-07
task_slug: issue-81-merge-1253
parent_task: issue-81-merge-8af3
status: prospective
---

## Research

* Start HEAD `ae54963584181d1b5b4d5a788153f853ec0077b2`, tree `b0dd355f68186af47b733eb5108311019cae50e0`, branch `feat/controlled-lifecycle-integration-81`, ignored-inclusive clean, PR #1240 open. Preservation ref `refs/ama/issue81-pre-95f-merge` set to the start head. Earlier refs unchanged.
* Fetched `origin/main` `3950602754437c21d20e91c49ddc1589426e7d1b`: github-actions score commit ("record score 77/100"), sole parent `95f7600d4` (PR #1253). The scorer has therefore settled; the descendant changes only `.github/rubric/scores/latest.json`. The merge base with the parent is `8af3aea6`.
* Incoming delta `8af3aea6..39506027`: 24 `.copilot-tracking` records for #107, `src/api/tests/test_assistant_release.py` (test only) and `latest.json`. No production, schema or workflow change. `src/core` appointment, gate, procurement and quality source is untouched by main.
* Dry `git merge-tree` is clean (tree `0f54c29edf32b5c3c4ac0b0f3b9dff61ae2f18b4`). The received test file differs from the parent's existing copy only by main's change.
* Open gaps stay explicit: #107 stays open (lease masking, SQL shape, actual approver, attestation, live gaps); no independent, operating or human approval is claimed.

## Plan and details

* One normal `--no-ff` merge of exactly `39506027`; no rebase, force, rewrite, retarget or child touch. Stop on drift (main moves, dirty tree, conflict).
* Proof: parents are PRE (the records commit) and `39506027`; `git diff --raw PRE HEAD` equals `git diff --raw 8af3aea6 39506027` including modes; the file list excluding `.copilot-tracking` is exactly `src/api/tests/test_assistant_release.py` and `latest.json`; blobs under `src/core` and all parent and child-owned source equal PRE; `latest.json` parses; `git diff --check` clean.
* Light checks only, in scratch `/mnt/ama-gates/g81-main1253-preparation-1107`: `env -i`, `PYTHONDONTWRITEBYTECODE=1`, external caches, non-editable `--no-deps` installs from a `git archive` snapshot, import-origin proof; run `test_assistant_release` from `src/api/tests` and the four core modules with unmasked exits; ruff, format and mypy on core. Results are local observed only; nothing is full acceptance. No FULL, services, SQL, browser or lock.
* Resume condition if drift occurs: refetch and re-plan with an amendment.

## Amendment 1 (critique verdict Revise; all accepted)

1. Commit these records as PRE, recheck clean tree and pinned main before merging.
2. Test setup: snapshot via `git archive` of core, agents and api; non-editable `--no-deps` installs of those three into the scratch venv (dependencies only after an actual missing-import failure); helper path `src/core/tests` on PYTHONPATH; prove import origin for each package; run the four core modules (`test_quality_procurement test_gates test_hazard_referral test_resident_preview`) and `test_assistant_release` with exits unmasked.
3. Count correction: the incoming delta is 22 tracking files plus two other files (`test_assistant_release.py`, `latest.json`), not 24.
