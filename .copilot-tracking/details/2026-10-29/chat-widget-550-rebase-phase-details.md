---
title: Chat widget 550 rebase phase details
description: Integration tasks and verification boundaries
ms.date: 2026-10-29
---

Task 550-rebase, same slug as plan/research/state.

## P01 / P01-T01

Initial clean head 99214901f9297391c023a4781d6c91fa38c0411c; fetched main
ecbb5a80470292c885764c28d6833c0e5ef63dfa. No PR exists. User explicitly
authorizes rebase/history rewrite locally, not force push.
Run git rebase origin/main. README conflict keeps compact case journey,
shared chat and main map additions. Resolve other conflicts by intent.
For rubric and docs/reference/research/retrofit-synthetic-data/scenario-manifest.json,
retain origin/main bytes. Check ancestry, diff hygiene and no legacy code.
Evidence files are new untracked task-owned inputs, not foreign dirty work.
Completed: rebase onto ecbb5a80, only README conflict, both sections retained.
Replayed head cd334e62; protected input equality and ancestry pass.

## P02 / P02-T01

Use /tmp/mv and explicit PYTHONPATH per project: src:tests plus sibling
core/agents source/tests. Core/API run ruff check ., ruff format --check .,
and mypy. Core runs test_scenario_manifest and chat-related modules.
API runs chat/resident, loading, workspace, accessibility/design/content,
case-journey modules; opt-in chat panel separately. Do not run full API
discovery unless flock -n /tmp/ama-rpi-heavy.lock true succeeds, and hold
the lock for any admitted heavy discovery.
Run checks.chat_widget_browser_check, existing employee/resident checks,
and CI checks.case_journey_browser_check with integrity-verified axe 4.10.3.
Run node syntax checks on changed chat modules. Existing checks manage
their own responsive synthetic loopback servers and cleanup. External logs
go under this session's files/ directory, not working data/source.
If web files need edits, first load web guidelines and fetch current rules.
Implementation-time amendment: the existing case-journey Node regression
still addressed the old inline employee composer. Migrate its employee
branch to the shipped shared widget and actual popup submit handler; retain
all ten draft-cleanup scenarios and all semantic assertions. No production
changes, new test files or removal. Fresh guidelines retrieved successfully;
no production web edits were needed. Core/static/manifest checks, shared and
existing browsers pass. Locked full API discovery passes 1,332 tests with 318
skips. Separate opt-in chat panel passes all 38. CI case journey, design-system
and regulatory browsers plus main's compact-case browser all pass.

## P03 / P03-T01

Reconcile all task markers and command results before one fresh independent
Review. Record execution separately from outcome. Do not rerun Review within
this task; route later findings as follow-up. Resolve authenticated GitHub
identity using gh api user and configure repository-local noreply email for
author and committer. Commit Conventional Commit plus specified coauthor.
Verify clean status and main ancestry; never push or create PR/Azure resources.
No full publication/hosted/human acceptance assertion.
Completed by one independent Review, Complete / Conformant, no findings, and
the containing local Conventional Commit. Re-fetched main remains ecbb5a80.
Only evidence/state closeout follows Review; no source changes or second Review.
