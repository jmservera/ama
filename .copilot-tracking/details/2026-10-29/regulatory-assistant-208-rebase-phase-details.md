---
title: Regulatory assistant PR 506 rebase phase details
ms.date: 2026-10-29
---

Task: pr-506-rebase-2026-10-29. Initial readiness: Ready from focused research.
All phases explicitly requested; no automatic follow-up session.

## P01-T01

Fetch already completed against 5653547507f3056f09a726a18516237728da5e5b.
Rebase original clean topic commits using GIT_EDITOR=true. New untracked
evidence belongs to this task and must not be stashed or discarded.
For add/append conflicts read both sides, preserve both entries, and inspect
current-main runtime interfaces before resolving. Main owns .github/rubric/*
and the scenario manifest initial conflict resolution. Record old/new hashes
and conflict paths. Completion: main ancestor, both original commits retained
semantically, no unresolved index entries.

## P02-T01 and P02-T02

From each of core/agents/api run /tmp/mv/bin/ruff check . and format --check .;
run /tmp/mv/bin/mypy in core and api (agents too if useful). Include isolated
CI lint/format of checks/regulatory_ux_check.py because project exemptions
otherwise hide it. From core, PYTHONPATH=src:tests:../agents/src:../agents/tests:
../api/src:../api/tests, run regulatory_chat, regulatory_usage,
regulatory_privacy, rule_engine, rulecards, source_freshness, chatthreads,
chat_privacy, scenario_manifest and dependency_rule. From agents/API use
their own src:tests first, then core and sibling source/test paths; run agents
regulatory_answers/regulatory_gates/dependency_rule and API
regulatory_chat_api/rule_alerts/regulatory_ux_check/dependency_rule.
Validate JS syntax without editing web source. Do not run full API discovery;
it is unnecessary, and the caller requires a successful heavy-lock probe first.
If source pins drift, inspect hash contract and refresh only affected hashes,
never weaken checks or replace main scenarios. Run the exact failed selector
again. Record expected skips and limitations explicitly.

## P03-T01 and P03-T02

Review current integration diff, rebase preservation and validation evidence
once independently. No source fixes or repeated Review after this assessment;
route new findings to later work. Before commit successfully resolve gh api
user, construct {id}+{login}@users.noreply.github.com from its response, and
configure only repository-local user.email. Ensure both author and committer
use that derived address; lookup failure blocks commit, with no fallback.
Include required
coauthor trailer. No amend, push, PR edits, merge or Azure operations.
Completion is local-only; final full gate/receipt and hosted CI remain
publication requirements for coordinator, not silently waived.

## Implementation reconciliation

P01 complete: log/chat conflicts resolved preserving main and topic intent.
P02 complete: core 124, agents 28, API 48 focused tests pass. Main-owned
manifest and rubric unchanged. All three projects pass quality/type checks,
including isolated regulatory browser harness quality.
Current-main case_journey tests and browser mock admission/usage were adapted
to the retained topic endpoint; regulatory browser now selects visible tabs.
Real regulatory browser passes 21 states with axe; actual existing
case_journey chat_cleanup passes all ten pending/reconstruction cases.
No tests added/removed. Original failed attempts remain recorded.
P03 complete: independent Review Complete / Residual work, no confirmed new
integration defects; implementation/evidence committed as be64c291.
Post-commit evidence finalization changes only dated tracking, not reviewed
source. Publication and original human findings remain outside completion.
