---
title: Issue 1259 recovery preparation changes
description: Changes and actual validation results for the unchanged-source recovery preparation
ms.date: 2026-11-09
---

## Changes

* Product source, tests and parent: unchanged (seed `fab9159d9`, tree `95f938b6c56e8a5d400c241f962a8b9c32d660bc`). No merge, rebase, reset, stash, push or remote write. Only tracking records were added.
* Ordering divergence: the validation commands ran before the plan, details and critique files were written (same session, read-only against product source). Disclosed in the plan.

## Actual results (scratch `/home/azureuser/.local/share/ama/gates/g1259-prep-demo-1109`, logs retained externally)

* Environment: fresh venv, non-editable install from `git archive HEAD src` of core, agents and api (pip exit 0); module origin under the venv site-packages; synthetic `ZF_DATA`; external `TMPDIR` and pip cache. Default editable installs point at `/home/azureuser/source/ama` and were not used.
* Core `discover -p 'test_ranking_publication*.py'`: exit 0, Ran 92, OK, no skipped markers in the verbose log (`core.log`).
* Class selector `UnusableArchivePathTests`: exit 0, Ran 6, OK (`core-unusable2.log`). A first attempt with a dotted module name from the wrong directory exited 1 with an ImportError (invocation mistake, `core-unusable.log`, no tests ran) and is preserved.
* API `test_ranking_policy test_ranking_publication_wiring test_ranking_scale`: exit 0, Ran 54, OK (`api.log`); the printed "hard links unsupported" line is expected mocked fault output.
* Agents `test_cohort_ranking_eval`: exit 0, Ran 20, OK (`agents.log`); printed blockers and OQ-018 lines are expected synthetic output, not fairness evidence.
* Scratch red check (pre-fix `6d793bc3a` source files, HEAD tests, `red.log`): exit 1, Ran 6, FAILED (failures=7). This reproduces the retained failing-first result (6 tests, 7 failures) and shows the regressions discriminate the fix. It is a scratch copy only; the worktree is untouched.
* Dry run `git merge-tree --write-tree HEAD 61df23715`: one conflict in `ranking_publication.py` (forecast only; not merged).

## Not performed

Full core discovery, FULL stack receipt, SQL, browser, scanners, independent assessment, hosted checks, human approvals, real stat-failure or crash testing, Blob contract tests (contract not frozen).
