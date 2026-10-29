---
title: Sensor scenarios PR 505 rebase phase details
description: Bounded task expectations and evidence ownership
ms.date: 2026-10-29
---

## Metadata

Task ID 505; slug sensor-scenarios-190-rebase; parent 190.
Plan: .copilot-tracking/plans/2026-10-29/sensor-scenarios-190-rebase-plan.md.
Research: .copilot-tracking/research/2026-10-29/sensor-scenarios-190-rebase-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01 |
| P02 | Complete | P02-T01 |
| P03 | Complete; independent lifecycle Review next | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Reconcile ancestry

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase and resolve conflicts

Context: clean original HEAD 2fdf08bba5f3c30969645191aafee8bf8e087036;
two branch commits; fetched base b0364e4b326936715d69ab1d75040c4528282af7.
Current phase artifacts are new untracked files created by this task, not
pre-existing user changes; they must remain safe across rebase.
Resolve index/log/guide conflicts by retaining independent entries rather
than blanket ours/theirs. During rebase, ours means upstream and theirs means
the replayed branch commit. Select explicit origin/main paths for caller-owned
rubric/manifest, not ambiguous side labels.
Completion: no unmerged paths, ancestry verified, main-owned files compared,
original evidence preserved byte-for-byte, source still under src/.

Observed: rebase completed to df760b84 after three documentation conflicts.
Reference index retains both #179 correction and #190 pack; append-only log
retains all main entries then the original scenario entry; dictionary keeps
the feature's later 2026-10-27 date. Main rubric/manifest compare equal.

<!-- rpi:phase id=P02 -->
## P02: Validate merged behavior

<!-- rpi:task id=P02-T01 -->
### P02-T01: Restore local installs and run scoped checks

Missing namespace import was reproduced in /tmp/mv. Install editable core,
agents and API via pip, restoring only required pinned dependencies.
Use core/api project configurations and source/test sibling paths. Inspect
actual failure before editing; preserve upstream indoor projection even if
exercise output shifts. No unrelated static cleanup or exemptions.

Core selectors: test_sensor_scenarios, test_scenario_manifest,
test_sensor_backfill, test_sensor_plausibility, test_sensor_faults,
test_sensor_stock, test_sensor_privacy, test_indoor_projection,
test_historical_backfill, test_synthetic_provenance,
test_synthetic_determinism, test_synthetic_output_dir, test_dependency_rule.
API selectors: test_sensor_ingestion, test_workbench, test_dependency_rule.
Additional tightly coupled selectors only if a failure demonstrates need.
Full API suite deliberately excluded; successful earlier probe is not a
reservation. Full gate acquires and holds its own lock.

Evidence: /tmp external logs; commands, exit codes, test counts/skips and
hash decisions recorded in dated changes. Static commands from each project:
/tmp/mv/bin/ruff check .; /tmp/mv/bin/ruff format --check .;
/tmp/mv/bin/mypy. No new test module, removals or generated source.
Completion: exact expectations verified, skipped integrations identified.

Observed: core static checks passed (106 formatted / 159 mypy files); API
static checks passed (56 formatted / 107 mypy files). Core selected tests:
124, one opt-in SQL skip; API selected tests: 50, zero skips. No new tests
or source corrections required. Shared /tmp/mv editable paths were changed
by another worktree after setup; explicit caller-required PYTHONPATH selects
this checkout for unit runs and CLI. Standalone no-PYTHONPATH CLI failure is
preserved, not concealed by a second shared-environment mutation.

<!-- rpi:phase id=P03 -->
## P03: Prepare Review and commit handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: Record evidence and prepare independent Review

After P01/P02 reconcile plan/details/changes; that is P03 completion.
The wrapper then transitions to the separate lifecycle Review.
Fresh independent reviewer assesses source/doc delta and execution evidence,
preserving original Review. Exactly one Review; findings route to follow-up.
Use authenticated GitHub account's privacy-safe local email for author and
committer. Conventional Commit includes required Co-authored-by trailer and
Refs #190 #192 #193 #194, never closing keywords.

Commit candidate and original RPI evidence before complete gate. Run
python3 tools/rpi-checks.py --all --base <fetched-base> --out <new-external-dir>
only with a successful fresh flock probe, and let runner serialize execution.
If prerequisite failure occurs, retain exact output and publication blocker;
do not fabricate receipt/approval, skip integrations or use cloud fallback.
No remote push, draft change, merge, or branch protection edit.
P03 completion: implementation evidence, plan markers/details and remaining
publication limits reconciled; ready for one independent Review.
Later wrapper handoff: committed local candidate, clean status, ancestry and
main-owned files checked; original and new outcomes retained; no push.

Pre-Review reconciliation: P01-P03 complete, results and unresolved external
publication limits match changes/plan. Migration dependencies restored from
existing requirements only after actual missing-package failure; all 25 tests
then passed. Twelve added local links/anchors and exact main log prefix
verified. Latest main fetch is unchanged; heavy-lock probe still fails.
