---
title: Issue 1384 main adoption plan
description: Plan for the ordinary merge of origin/main into the held 1384 candidate and targeted validation
ms.date: 2026-11-10
ms.topic: reference
---

## Objective

Integrate `origin/main` `111847191d1fde5e8ea18c30c999e99f33721aff` into branch `fix/demo-workspace-retry-oracles-1384-1110` by an ordinary merge, keep both checker intents, and validate the composition with the original whole browser commands. No new oracle, production or retry-policy logic.

## Phases

* Phase 1: Tracking and witness setup (before any source adoption).
  * [ ] Commit research, plan, details, critique, prospective changes and state as tracking-only.
  * [ ] Witness launch, research-open, plan-done; a separate strict unique-key JSON parse of the state; then a separate implement-start.
* Phase 2: Adoption.
  * [ ] `git merge --no-ff --no-commit origin/main`; resolve only the two additive hunks keeping both sides via apply_patch.
  * [ ] If any other conflict or any semantic interpretation is needed, stop for Root.
* Phase 3: Validation (targeted DEMO tier, own venv, worktree-qualified imports).
  * [ ] Non-heavy: `tests.test_workspace_scripts` (including strict parser and loader-derived totals), other impacted focused units, ruff check and format check, strict mypy, `node --check app.js`, sha256 of `workbench_browser_check.py` equals main's.
  * [ ] Heavy, one execution each under `flock -n /tmp/ama-rpi-heavy.lock` with actual holder reported: whole `workspace_scripts_browser_check`, whole `employee_workspace_browser_check`, and the whole `employee_chat_browser_check` named in the instruction.
* Phase 4: Complete the changes record, witness implement-done, one Review and witness review-done while the merge is still staged and uncommitted, then commit the merge, witness commit-complete, verify, handoff.

## Constraints

* No rebase, reset, amend, force-push, push, PR or GitHub write. Manual edits with apply_patch or the edit tool only.
* Failures preserved with unique raw outputs; no retry until green; no isolated variant substituting a whole run.

## Planned touched paths

* `src/api/checks/workspace_scripts_browser_check.py` (merge resolution of two additive hunks)
* All other paths come from `origin/main` unchanged by the merge (not hand edited).
