<!-- markdownlint-disable-file -->
# RPI Phase Details: IoT PR 557 main refresh

## Metadata

* Task ID: pr-557-main-refresh-2026-10-29
* Task slug: iot-pr557-main-refresh
* Plan: .copilot-tracking/plans/2026-10-29/iot-pr557-main-refresh-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/iot-pr557-main-refresh-research.md

## Phase Index

| Phase | State | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01 |
| P02 | Complete | P02-T01 |
| P03 | Complete | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Rebase and reconcile

<!-- rpi:task id=P01-T01 -->
### P01-T01: Replay the existing topic on main

Starting worktree was clean before this task's own untracked evidence.
HEAD/remote topic: `7bd71d37866671899ef11fa653d9eace9687069b`.
Reviewed main: `8ee1b77f8983ddf39216da07ae60c63ef66431d6`.
The explicit caller rebase authorizes local history replay, not push.

Use `git rebase origin/main`. For main-owned generated files, restore main's
exact version; a rubric-only replay may become empty and should be skipped
only after checking its entire diff. Preserve both append-only log entries,
both index sections and both infra guide sections, with one canonical YAML
date. Read every conflict before resolution, and continue noninteractively.

Completion: no rebase state/conflict markers, main is ancestor; range-diff
shows no unintended IoT loss, exact main rubric and manifest identities.
No unowned work is moved, discarded or committed.

Completion: rebase finished at `9a712fd3`. Index/log conflicts retain both
monitoring and IoT sections; main's single frontmatter date survived
automatically. Both rubric-only replays became empty after restoring main.
Range-diff shows eight retained commits, seven patch-identical and only the
first documentation context changed; runtime/test patches are unchanged.

<!-- rpi:phase id=P02 -->
## P02: Validate the reconciled contracts

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute targeted static, types and unittest checks

Depends on P01. Tools available: `/tmp/mv/bin/python` 3.12.3, Ruff 0.17.1,
mypy 2.4.0, local `az bicep`. Existing packages are installed; source-first
PYTHONPATH prevents shared editable metadata from selecting another worktree.

From `src/core` run Ruff check, format check, mypy, and unittest modules with
`PYTHONPATH=src:tests:../api/src:../agents/src:../api/tests:../agents/tests`.
Modules: `test_scenario_manifest test_sensor_stream test_sensor_consumer
test_dependency_rule`. From `src/api` use
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`,
Ruff check/format/mypy and `test_iot_stream test_sensor_ingestion
test_sensor_stream test_resident_sensors test_dependency_rule`.
From `infra`, run existing `test_iothub*` and the two Bicep parameter-policy
methods that validate committed parameter examples. Require offline Bicep;
never execute any guide's deployment commands.

Initial `flock -n /tmp/ama-rpi-heavy.lock true` returned success. No full API
suite is planned; no lock is claimed by this brief probe. Independent targeted
static/tests may run without starting heavy integration/browser/SQL work.
Record expected opt-in skips exactly; they are not integration acceptance.

Completion: actual command/exit/count record, corrected coupled failures or
explicit unresolved blockers. No pinned source differs now; still run manifest
test after rebase to detect unexpected drift. Tests are external to packages;
no removals or additions planned.

Completion: core Ruff/format (110 files)/mypy (163 files) passed; 57 selected
tests passed, zero skips. API Ruff/format (59 files)/mypy (112 files) passed;
96 selected tests passed, zero skips. Infra scoped Ruff/format and 24 compiled
IoT/parameter tests passed, zero skips. No full API discovery run. Main fetch
after checks was unchanged; generated files and IoT runtime/test/Bicep blobs
match their intended main/original identities. Full commands/results are in
the changes record. No dependency installation or CI fix was necessary.

<!-- rpi:phase id=P03 -->
## P03: Review and commit locally

<!-- rpi:task id=P03-T01 -->
### P03-T01: Independent Review and durable local handoff

Depends on P02. Reconcile plan/details/changes and give reviewer the baseline,
main SHA, rebased HEAD, command results and exact intended source diff.
Review writes only its one original review artifact. Findings route forward;
do not repeat Review or implement a second fix loop in this task.

After review, use already resolved authenticated identity
`8036360+jmservera@users.noreply.github.com` for local author and committer.
Commit a Conventional Commit with
`Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
Verify clean status, ancestry, generated identities and trailer. No push,
force-push, remote edit or Azure resource operation.

Completion means local maintenance and original RPI evidence are committed.
Hosted CI, final publication receipt, live acceptance and human approval are
not established. Preserve all earlier adverse outcomes. A material Review
finding prevents a clean success claim and is recorded as follow-up/blocker.

Original Review executed once: Complete / Conformant, no substantive findings.
It independently checked complete preservation and ran nine lightweight tests
without skips. Reviewed source boundary is `9a712fd3`; parent now commits only
dated task evidence and performs the planned local identity/cleanliness checks.

Completion: fbb41ac9c5d2f210b70113fefe318e8b4b17bc29 committed all seven
original task artifacts. Author and committer use authenticated noreply identity,
required coauthor trailer is present, immediate status was clean, main is
ancestor, rubric/manifest equal main and source diff from reviewed 9a712fd3 is
empty. Final state/checklist reconciliation is evidence-only; no publication
eligibility or exact-final-head Review is claimed.
