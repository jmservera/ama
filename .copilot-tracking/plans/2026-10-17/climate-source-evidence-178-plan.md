<!-- markdownlint-disable-file -->
# RPI Plan: climate-source-evidence-178

## Task Metadata

* Task ID: 178; slug: climate-source-evidence-178; date: 2026-10-17.
* Status: P01-P04 implementation complete; bounded resolution Review Complete,
  Conformant for rebase only; parent delivery next, then explicit STOP.
* Details: .copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/climate-source-evidence-178-plan-critique.md

## Executive Summary

Current continuation is rebase-only: preserve this narrow partial feature and
all #368/#370 evidence while replaying onto fetched main
4e4a389f53870137a0f0582861766be5983a8f96. No feature expansion, source
adoption or owner approval. Original implementation below remains historical.

Replace the current all-unknown position with a dated official-source comparison,
an explicitly conditional HadUK-Grid recommendation, exact terms/access blockers,
and reproducible Durham monthly temperature statistics. This is evidence delivery,
not a new generator or a completed paired historical weather source.

### What You May Not Know

OGL reuse and download access are separate: CEDA requires login even for the
selected open dataset. HadUK monthly humidity cannot establish replay-scale
extrema. Durham has no humidity; its monthly averages are not daily extremes.
Met Office website terms also restrict automated copying. No further automated
Met Office retrieval or downloader is planned.

### Unresolved Decisions or Blockers

Owner reuse approval UNMET; CEDA record access and representative paired
temperature/RH observations remain blocked. These limit issue acceptance but
not this bounded comparison and temperature-only result.

## User Decisions and Requirements

* 2026-10-17 continuation supersedes the earlier no-rewrite delivery direction
  only for this run-owned topic: fetch/rebase, resolve clear combinations only,
  validate, push with an explicit force-with-lease, update PR #371 with Refs
  #178 and stop. Never rewrite main or claim full issue acceptance.
* Execute Research, Plan, Implement, Review in order with dated committed artifacts
  and explicit completion entries in the session log.
* Read #178/#367 and canonical docs; public official metadata/terms and bounded
  climate records allowed, no content/private-data uploads.
* Preserve owner reuse approval as UNMET. No paid data, account creation or
  acceptance on behalf of owner; no invented dates, RH or replacement source.
* Integrate existing synthesis/register, index and append-only log; immutable
  snapshots and case-study original unchanged.
* No private datasets, support/cohort, 60k regeneration, live DB, Azure, spending,
  network/security changes, #176 stock_fabric.py or #360 infrastructure.
* Resolve GitHub ID/email locally; Conventional Commit with Copilot coauthor;
  push requested topic, open PR with Refs #178 (never Closes), no merge/rewrite;
  stop after PR/final SHA and results/blockers.

## Goals

* Make independently verifiable progress on each original issue criterion.
* Preserve observation/aggregation/model/approval distinctions everywhere.

## Scope and Non-Goals

In scope: existing sensor synthesis/source register, index/log, directly coupled
src/core/README.md climate-status paragraph, one offline
standard-library analysis helper, tiny synthetic unit fixtures, derived JSON
report and tracking evidence. New helper stays in tools, outside app runtime.
Non-goals: bundling raw provider pages/data, a climate downloader, generator
changes, application acceptance, legal approval or operational rules.

## Functional Requirements

* Compare all five issue candidates plus UKCP18/EA leads using W1-W14.
* Recommend exact HadUK-Grid administrative regions v1.3.2.ceda, UUID
  386b3c1ee2054ef5ae0d73060963a9f1, for contextual monthly analysis only,
  record dataset citation/OGL v3, access failure and owner UNMET.
* Parse local historic-station monthly file with exact schema and location.
  Select the 1991-2020 climatology window (360 expected months), report tmax/tmin and arithmetic
  midpoint extrema with dates, source lines, counts and SHA-256. No RH inference.
* Exclude provisional/estimated values per variable, count missing, identify
  absent months and duplicate months, reject malformed/nonfinite values.
  Flag units and monthly statistics rather than raw instantaneous temperature.
* No network in helper; CLI errors explicit/nonzero. JSON stable and no NaN.
* Calendar completeness and each usable-variable coverage are separate.
  Per field: present = valid + provisional + missing + estimated, with that
  exclusion precedence and mutually exclusive counts. Absent = expected - present.
  Midpoint only uses same-row valid pairs. Empty series is explicitly unavailable,
  null extrema, no numeric default; no input rows is a CLI error.

## Non-Functional Requirements

* Python standard library only; no dependency installation expected.
* Input bytes hashed before parsing; CLI requires expected SHA-256 and fails on
  mismatch. Output reproducible from same bytes/date.
* No full external dataset committed; derived numbers and input/output hashes
  retained. Raw 88KB-scale station file stays only in session evidence storage.
* Existing synthetic expectations and runtime behavior byte-unchanged.

## Acceptance Criteria

* AC1: verified material comparison, with remaining exact terms gaps explicit.
* AC2: candidate/retrieval/licence evidence recorded, but owner approval UNMET;
  no claim of adopted source.
* AC3: measured temperature-only monthly sample statistics; humidity and paired
  replay bounds explicitly unmet. No full issue closure.
* Tracking: ordered completion log, plan/details/critique/changes/review/state.
* Delivery: pushed PR, criterion audit, final SHA, validation results and blockers.

## Implementation Context Record

* Research: .copilot-tracking/research/2026-10-17/climate-source-evidence-178-research.md
* Changes: .copilot-tracking/changes/2026-10-17/climate-source-evidence-178-changes.md
* Review: .copilot-tracking/reviews/logs/2026-10-17/climate-source-evidence-178-review.md
* Readiness: Ready; critique execution Complete, verdict Revise, all three
  compatible direct corrections applied without repeating critique.
* Parent continuation: explicit automatic ordered loop; stop after pushed PR.

## Sources

* Research C1/W1-W14, #178 owner comments, merged #367.
* docs/reference/research/iot-sensor-analytics-research-plan.md: existing
  register and acceptance audit own canonical updates.

## Phase Checklist

<!-- rpi:phase id=P04 -->
### [x] P04: Rebase-only integration continuation

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Preserve upstream and feature evidence, validate resolution

Rebase onto pinned fetched main; resolve only additive index/log/core README
conflicts. Preserve all log entries and both source intentions. Check every
upstream non-overlap file against main and every feature-only production file
against f4ea754; verify all upstream added lines remain in shared files.
Run focused climate tests, compileall, retained hash-guarded byte replay,
exact available existing lint/type checks and git diff --check.
Then one bounded resolution Review, update existing artifacts, one lease-push
and PR update. No new critique: original one-pass gate is retained.
Test ownership unchanged; exact removals none; maximum production additions
zero. Only conflict combinations and existing tracking artifacts may change.
Details: P04-T01. Existing human blockers do not prevent history integration.

<!-- rpi:phase id=P01 -->
### [x] P01: Retain reproducible bounded temperature evidence

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Offline parser, synthetic tests and derived JSON

Implement tools/climate_station_bounds.py and tools/test_climate_station_bounds.py.
Generate docs/reference/research/climate-source-evidence-178.json from the already
retrieved Durham file. Preserve complete 1991-2020 window and input hash.
Details: P01-T01.

<!-- rpi:phase id=P02 -->
### [x] P02: Canonical comparison and honest acceptance audit

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Integrate metadata, terms, recommendation and results

Keep dated offline section as history, clearly route current state to 2026-10-17
section. Update synthesis/source register, reference index and append-only log.
Details: P02-T01. Depends on P01-T01 for measured numbers.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and hand off once to Review

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Reconcile scope, tests, report and links

Run focused unittest discovery, real record derivation and independent arithmetic
cross-check; inspect changed Markdown/links/diff and immutable/excluded paths.
Record evidence and plan markers before single post-implementation review.
Details: P03-T01. Depends on P01-T01/P02-T01.

## Dependencies

* Research complete with genuine public Durham record locally retained.
* W5 locator (tracking only):
  /home/azureuser/.copilot/session-state/836a4f13-ad62-4778-8bea-453cc42fe79f/files/climate-178/durhamdata.txt
  Preflight on 2026-10-17: 92,268 readable bytes; SHA-256
  d2c9ff2a443b8502957ce88fe8bfdbbd0d5ac111208eab0842bc574d4d4306f9.
  Actual retrieval date is 2026-10-17, not inferred from modification time.
  Missing/hash-mismatched input blocks numeric output, never triggers download.
* Owner/CEDA authorization is not a dependency for documenting blocked RH.

## Locked Validation and Test Ownership

* Owner: P01 offline helper; new tests tools/test_climate_station_bounds.py.
* Exact removals: none. Maximum additions: one helper, one test module, one
  derived JSON file, nine tracking artifacts; no application tests changed.
* Canonical targets: sensor synthesis, reference index/log and directly coupled
  core README climate-status paragraph. Generated target:
  climate-source-evidence-178.json; no copied provider data.
* Semantic tests: schema/units, numeric/quality handling, missingness/duplicates,
  true monthly extrema, midpoint pairing, provenance/dates/counts, CLI failure.
* Regression: no network or app imports, existing synthetic source unchanged,
  deterministic output and diff/path boundaries.
* Commands: python3 -m unittest discover -s tools -p 'test_climate_station_bounds.py' -v;
  local helper invocation; independent standard-library arithmetic; git diff --check.

## Critique Disposition

| Finding | Owner / disposition | Exact resolving evidence |
| --- | --- | --- |
| PC-001 High | Planner; resolved directly | W5 locator, 92,268-byte/hash preflight above; exact offline command in details; required hash guard |
| PC-002 Medium | Planner; resolved directly | 360 expected months, mutually exclusive count equations, same-row midpoint and unavailable-empty policy in requirements/details/tests |
| PC-003 Medium | Planner; resolved directly | Regional UUID 386b3c1ee2054ef5ae0d73060963a9f1 locked; matching W3 terms/citation and W4 access test; 1km distinct alternative |

No significant/divergent user decision needed. Residual RH/access/reuse gates
retained. One critique only.

## Follow-Up Items

* Owner reviews dataset reuse and automated-access conditions.
* Authorized access/record packet for paired RH/temperature and adequate geography
  precedes cadence-specific bounds and generator adoption; outside this task.

## Handoff

Current handoff: P04 implementation and bounded resolution Review complete.
Research reused with Ready disposition; plan/details/changes reconciled.
Original critique remains complete; do not rerun it or reopen P01-P03.
Delivery commit, one lease-push and PR update remain parent-owned; then STOP.

Original P01-P03 completed their Review with Residual work; that historical
outcome remains unchanged. No new research, deployment, issue ticks or child task.
