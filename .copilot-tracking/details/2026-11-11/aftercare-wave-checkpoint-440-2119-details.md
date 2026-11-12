---
title: Aftercare numeric-order integrated-main checkpoint details (Refs #440 #1401 #1402)
description: Step-level details for the bounded aftercare checkpoint record
ms.date: 2026-11-11
---

Plan: [plan](../../plans/2026-11-11/aftercare-wave-checkpoint-440-2119-plan.md).

## Step 1 Preflight

* Command shape (run from the worktree root): `env -i HOME=<owned tmp> PATH=$PATH PYTHONPATH=<wt>/src/core/src:<wt>/src/core/tests:<wt>/src/api/src:<wt>/src/api/tests:<wt>/src/agents/src:<wt>/src/agents/tests python3 -c 'import zava_forward.core.aftercare as m, zava_forward.api.server as s; print(m.__file__, s.__file__)'`. Expected: both under the worktree. Record `git rev-parse HEAD:<path>` blobs for the three core files.
* Capture: pin, tree, Python, Ruff, mypy, Node versions, `ZF_DATA` unset, `ZF_RESIDENT_MSSQL` unset.

## Step 2 Test selectors

* Each selector runs once. Output files: `<name>.log` and `<name>.exit` in the session `files/aftercare-checkpoint-440-2119/` folder. Record Ran, OK and skipped counts per selector from the actual output line.
* A2 expected skips: the MSSQL class (gated by `ZF_RESIDENT_MSSQL`). A3 and A4 skips, if any, are listed.

## Step 3 Static

* `ruff check` and `ruff format --check` on the three owned files; `mypy` with the project configuration from `src/core` on the same files. Record whichever exit codes appear.

## Step 4 Record content

* Section title: `Aftercare numeric-order integrated-main checkpoint (2026-11-11, Refs #440 #1401 #1402 #134)`, appended at the end of the pack.
* Sub-headings: trigger and identities; consumed versus observed evidence; requirement trace (document-qualified); ordering, persistence, intake and human boundaries; commands and results; pending blank-state gap (#1402, PR 1458, unmerged); exclusions; recommendation and affected gates; process record and limits.
* Index entry and log entry follow the existing pattern; append-only; no earlier entry altered.

## Step 5 Verification

* `git diff --check`, link existence check for each relative link added, `git status --short` clean after commit, exact head and tree recorded in the handoff.
