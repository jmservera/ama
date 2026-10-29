---
title: PR 508 rebase phase details
description: Task-level integration and validation boundaries
ms.date: 2026-10-29
---

Task ID: pr-508-rebase-2026-10-29. Slug: iot-508-rebase.

## P01

P01-T01 depends on completed research and critique. Execute `git rebase
origin/main` with noninteractive editor; inspect each conflict before resolving.
During rebase ours is main plus replayed history, not the original topic.
Keep both index/log additions without changing older log entries. Preserve
source behavior on both sides; no blanket conflict-side preference.

P01-T02 depends on P01-T01. Compare `.github/rubric` and
`docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`
against main, confirm ancestry and inspect range-diff and aggregate diff.

## P02

P02-T01 depends on P01. In each project use `/tmp/mv/bin/ruff check .`,
`/tmp/mv/bin/ruff format --check .`, `/tmp/mv/bin/mypy`.
Set `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`
for tests. Core selectors include stream, consumer, scenarios, manifest,
historical backfill and dependency rule. API includes IoT, sensor ingestion
and dependency rule. Only synthetic/offline fixtures, no configured/private DB.

Exact core unittest invocation from `src/core`:
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests /tmp/mv/bin/python -m unittest test_sensor_stream test_sensor_consumer test_sensor_scenarios test_scenario_manifest test_historical_backfill test_dependency_rule -q`.
Exact API invocation from `src/api`:
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests /tmp/mv/bin/python -m unittest test_iot_stream test_sensor_ingestion test_dependency_rule -q`.

P02-T02 records command, directory, exit, count/skips and diagnostics. Do not
start full API discovery or a heavy gate without nonblocking lock admission;
do not wait on or disturb another lock owner. No Azure operations.

## P03

P03-T01 depends on P02 reconciliation; fresh independent reviewer gets plan,
research, changes, base/head and the integration diff. Review executes once;
findings route to follow-up rather than silently repeating Review.

P03-T02 depends on Review disposition. Resolve current gh account and repository
local privacy-safe identity; commit implementation/evidence using a Conventional
Commit and required Copilot trailer. Verify clean worktree and main ancestry.
No push. No new PR. Hosted checks and exact-head publication gates are not
claimed passed.

## Implementation reconciliation

P01 and P02 complete. Rebase retained all substantive source changes and main's
new scenarios; rubric-only commits were omitted under the explicit main-copy
policy. Documentation-only reconciliation distinguishes implemented opt-in
SDK/pacing code from unproven live use. Test ownership/removals/additions remain
unchanged. Static checks and 152 selected tests pass, no skips. Final doc
link/anchor, main-log-prefix and diff checks pass. No full API discovery needed.
Only P03 original Review and conventional commit remain.
