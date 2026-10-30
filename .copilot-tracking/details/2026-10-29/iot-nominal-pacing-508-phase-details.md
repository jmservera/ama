<!-- markdownlint-disable-file -->
# RPI Phase Details: Nominal replay pacing

## Metadata

* Task ID: pr-508-nominal-pacing
* Task slug: iot-nominal-pacing-508
* Related plan: .copilot-tracking/plans/2026-10-29/iot-nominal-pacing-508-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/iot-nominal-pacing-508-research.md C1-C5

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Nominal metadata and scheduling | Complete | P01-T01 |
| P02 | Documentation, scoped validation and handoff | Complete; ready for Review | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Preserve nominal scheduling

* Context: nominal slots 3/4 select faulted payload times 16:00 on consecutive
  days, while nominal times are midnight/08:00 on day two.
* Intent: make transport spacing independent of payload anomalies.
* Boundaries: retain wire format, hashes, row order, fault labels, burst/rate and cleanup logic.
* Targets: core sensor_stream Frame/replay and API iot_stream HubPublisher.
* Dependencies: completed research, one critique.
* Completion evidence: exact suffix publisher regression and core semantic assertions.
* Unresolved items: none.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add metadata and regressions

* Append required nominal_at: datetime to Frame; no optional fallback.
* Populate spec.origin + timedelta(minutes=slot * spec.cadence_minutes);
  preserve on duplicates and the publisher's defensive row snapshot.
* Replace only scheduling timestamp source with frame.nominal_at.
* Core generation tests compare metadata to configured slot times, including
  custom origin/cadence, suffixes and all explicit faults; existing comparisons
  establish suffix object equality and duplicate row identity.
* API regression uses existing PublisherTests inert certificate/client setup,
  Replay(fault="out_of_order", first_slot=3, end_slot=5), a 60-second budget,
  real Pacer(speed=1000, clock=virtual_clock), and patched sleep advancing time.
  Initialize virtual clock to real monotonic so supplied-deadline validation
  remains valid without changing production clock code.
* Capture client send instants and payloads; require exactly two sends at
  relative instants 0 and 28.8 seconds, equal to clean rows 2/5, whose payload
  times still differ by 24 hours. Old code must fail under this test.
* Maximum new unittest methods: two total, in existing test files only.
  Removals: none. No generated targets.
* Completion evidence: old-code regression failure, fixed regression pass and
  core module results. One later independent Review assesses the completed work.

<!-- rpi:phase id=P02 -->
## P02: Document and validate

* Context: exact caller checks are narrower than full publication gates.
* Intent: finish bounded local engineering work without implying publish approval.
* Boundaries: no API discovery, Azure, mvp, push, history rewrite or unrelated fixes.
* Targets: component READMEs, rubric origin/main copy, tracking evidence.
* Dependencies: P01.
* Completion evidence: command outcomes, one Review and Conventional Commit.
* Unresolved items: full publication gate remains coordinator-owned.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Scoped checks, review and commit

* README edits explain separate nominal metadata and fault-independent spacing.
* Replace .github/rubric/scores/latest.json using origin/main's tracked copy
  under explicit caller authorization; initial worktree was clean.
* Each component: /tmp/mv/bin/ruff check ., /tmp/mv/bin/ruff format --check .,
  /tmp/mv/bin/mypy.
* Core unittest selector: test_sensor_stream test_sensor_consumer test_dependency_rule.
* API unittest selector: test_iot_stream test_sensor_ingestion test_dependency_rule.
* Both use requested PYTHONPATH; no full API discovery.
* Fresh independent Review reads exact task diff and evidence, writes only
  .copilot-tracking/reviews/logs/2026-10-29/iot-nominal-pacing-508-review.md.
  Review and commit are later lifecycle obligations, not implementation-task
  prerequisites; implementation completion requires scoped checks and reconciliation.
* Reconcile plan markers/details/changes/state before committing; preserve original
  Review outcome. Material in-scope findings block a successful fix handoff and
  remain explicit blockers for a later task; unrelated findings may be deferred.
  Do not repeat Review or return to implementation within this task.
* Identity: gh api user returned id 8036360/login jmservera. Configure local
  8036360+jmservera@users.noreply.github.com for author and committer.
* Commit includes required Co-authored-by trailer. No push.

## Completion Evidence

* P01: exact new publisher test failed on original scheduling with RUN_DEADLINE,
  passed after nominal metadata change; core replay module 12 tests passed.
* P02: Ruff check and format --check passed in both projects; mypy passed
  161 core and 109 API source files; targeted core modules 49 tests and
  API modules 72 tests passed. No full API discovery.
* Requested rubric file equals origin/main. git diff --check passed.
* Original API format failure fixed using existing Ruff formatter, then all
  required API checks rerun and passed. No acceptance or scope divergence.
* Review/commit remain lifecycle actions after completed implementation.
