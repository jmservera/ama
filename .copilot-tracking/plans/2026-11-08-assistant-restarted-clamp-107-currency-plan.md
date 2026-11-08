---
title: Issue 107 restarted clamp currency merge plan
description: Prospective plan for one normal merge of inert incoming main records, with a dated deviation correction
ms.date: 2026-11-08
ms.topic: reference
---

## Research (executed)

* Candidate HEAD `0c11c2681b085008bd296af3ec5a3ef30bdfb8a8`, tree `c3d52a891c67543f5140361c3ee680ca8d3742b7`, ignored-inclusive clean.
* Fresh `origin/main` `0f05e9aae70768def8d1d9c300215f9ee2f11638`, tree `577947cb2d94de5b79f24d38b6f459ebb0aa13a8`.
* `2e0c676ad..origin/main` is 21 added files, all under `.copilot-tracking/` (issue 530 records). No source, tool, workflow or rubric path. `git merge-tree` reports no conflict.
* Production `assistants.py` blob `0f1db5ad5cb0` equals main, confirming the earlier temporary mutation left no byte difference.

## Deviation correction (appended, originals unchanged)

The [original plan](2026-11-08-assistant-restarted-clamp-107-plan.md) said the mutation check would not be done in the tree. The [changes record](../changes/2026-11-08-assistant-restarted-clamp-107-changes.md) shows it was done in this tree: the `min()` clamp in `assistants.py` was temporarily replaced, only the new test failed, and the file was restored with `git checkout`. The original [author review](../reviews/2026-11-08-assistant-restarted-clamp-107-review.md) said the work matched the plan; that is inaccurate for this step. Both originals stay as written as adverse evidence. Final proof of restoration: production blob equals main, and the diff against main outside tracking is the 27-line test only. The mutation is not repeated.

Second deviation, added after critique: the original plan step 2 asked to assert one provider call and task `first` ready after wave one, and `finish()` checks distinct PIDs only inside each single-worker wave. The 27-line test asserts only results and pool row there (the final total of two provider calls and `second` ready are asserted). These are narrower assertions than planned, recorded rather than changed; no test edit is authorized.

Commit rule, added after critique: the changes, review and state records are committed before any FULL, and the ignored-inclusive tree must be clean at admission.

## Plan

1. Commit this plan and its critique alone.
2. One normal `git merge --no-ff origin/main` (0f05e9aae). Stop if anything outside incoming `.copilot-tracking/` records changes or a conflict appears.
3. Prove: the 27-line test diff against main is unchanged; `assistants.py`, the worker helper, `tools/rpi-checks.py`, rubric and store blobs equal main; all original restarted-clamp records are byte-identical.
4. Write a changes record and one author review. No code, test or tool change. No new unit run, since only inert tracking bytes change; original results stay attributed to `0c11c26`.

## Future FULL plan (not admitted; 86 holds the heavy window)

* Preconditions at admission: lock free, resources checked by the runner, shared 4-CPU host not dedicated, fetch main and merge once more if it moved.
* Command: `python3 tools/rpi-checks.py --all --base <current-origin-main> --out <new external path, 58 bytes or fewer> --jobs 2 --lock-timeout 0 < /dev/null`. The runner may derive fewer jobs; report requested against actual. No queueing.
* Selector: `SQL_SELECTORS` already contains `test_assistant_release.MssqlUnleasedRevocation`. Require `test_restarted_processes_keep_partially_used_allowance_and_stop_at_stored_calls`, plus the two earlier process methods, as `ok` in the mssql log, all 17 groups and fresh images.
* Receipt stays external and is verified against current main before independent assessment. No tracked write afterwards.
