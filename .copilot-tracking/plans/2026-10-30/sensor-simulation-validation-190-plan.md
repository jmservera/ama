---
title: Sensor simulation validation 190 plan
description: Bounded completion of simulator validation and current documentation
ms.date: 2026-10-30
---

## Task Metadata

* Task ID: 190
* Task slug: sensor-simulation-validation-190
* Planning status: Ready; single critique Complete / Revise, direct corrections applied
* Plan date: 2026-10-30
* Details: .copilot-tracking/details/2026-10-30/sensor-simulation-validation-190-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/sensor-simulation-validation-190-plan-critique.md

## Executive Summary

Retain the already delivered eleven-case damp/retrofit pack and add explicit
annual cross-stage regression checks. Correct the data dictionary's stale
stage-2 availability and snapshot versions, and document a local-only validation
recipe with individual results. No runtime model, schema or UI change is needed.

### What You May Not Know

The existing pack already reports fifteen independent checks. Current stage 2
has finite SDK adapters but no verified live operation. Parent acceptance also
requires actual child closure or accepted deferral; writing a local deferral
proposal does not mutate or resolve those GitHub stories.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review in order with dated artifacts.
* Use supplied topic branch/base, `src/`, pip and tests outside packages.
* Preserve synthetic-only controls; no Azure, deployments, credentials, secrets,
  live sign-in or push.
* Run requested full API discovery and Ruff/format/mypy locally. Hold
  `/tmp/ama-rpi-heavy.lock` with `flock -w 600` for heavy checks.
* Commit locally using privacy-safe identity, `Refs #190` and the supplied trailer.
* State each issue acceptance criterion's actual evidence and residual gap.

## Goals

* Demonstrate current seasonal backfill/replay parity, physical/exercise ranges,
  seasonal/diurnal variation and explicit fault counts without network access.
* Make the dictionary and both-stage validation instructions match actual code.
* Preserve original adverse evidence and avoid unsupported whole-issue approval.

## Scope and Non-Goals

In scope: one new core test module, core README, existing data dictionary,
IoT research synthesis, KB index/log and dated RPI records.
Non-goals: production model changes, schema/version changes, new analytics,
downstream #111/#133 implementation, web changes, live transport and GitHub writes.

## Functional Requirements

* Clean stages use the same synthetic selection, seed, origin and cadence.
* Exact values/identities and per-home means, population spread and quantiles
  agree; bounded replay windows retain original sequence provenance.
* Independent tests check finite values and exercise domains, non-flatline,
  seasonal structure and diurnal structure. Corrupted fixtures demonstrate that
  guards reject invalid/flatline inputs rather than merely testing happy paths.
* Existing fault/rate tests are reused; no redundant fault methods are added.
* Existing seven damp/eight retrofit result shapes stay unchanged.

## Non-Functional Requirements

* At most 100,000 nominal replay samples; deterministic constructed stock only.
* Annual thresholds explicitly exercise-valued; exact replay tolerance zero.
* No broad catches, runtime fallbacks, external data fetch or new dependency.
* Preserve all existing tests, workflow/check names and historical artifacts.

## Acceptance Criteria

* New tests run under existing core CI discovery; each check has its own test
  result and useful failure context.
* Existing scenario CLI retains eleven cases, 6,888 rows and fifteen per-check
  results with fixed truth/confusion and hashes verified.
* README/data dictionary cover actual backfill, replay and opt-in SDK boundaries,
  message/storage types, seeds, limits, climate attribution and synthetic labels.
* Child disposition table distinguishes delivered, proposed deferral and unmet
  owner/downstream acceptance. Parent checkbox is not inferred from local tests.
* Requested API/static checks are run, adverse results retained; full local gate
  is attempted on committed exact head with external evidence, never bypassed.

## Sources

* .copilot-tracking/research/2026-10-30/sensor-simulation-validation-190-research.md
* Existing scenario/replay source/tests and core/API READMEs.
* Issue #190 and children #191-194; original Review remains immutable.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Add cross-stage validation contracts

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add deterministic annual checks and reuse fault coverage

One new `src/core/tests/test_sensor_stage_validation.py`; maximum twelve test
methods, zero removed tests. Canonical source modules stay unchanged.
Use semantic assertions and negative mutations, not generated goldens.

<!-- rpi:phase id=P02 -->
### [x] P02: Reconcile simulator documentation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Correct dictionary and document local validation/dispositions

Update the five named existing Markdown targets. Append only to the KB log.
No new knowledge-base page or stale historical-evidence rewrite.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and prepare independent Review

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run targeted, scenario, API and static checks

Record commands/exits/skips, manifests and per-check results in changes evidence.
Prepare the one independent Review only after plan/details/changes reconcile.
After Review the parent commits the candidate and runs the full external gate;
no source corrections or repeat Review within this loop.

## Dependencies

Existing #177 model and #184 replay suffice for local checks. Actual #184 live
operation and #111/#133 consumer use are separate unresolved acceptance.

## Critique Disposition

Single independent critique Complete / Revise; no repeat.

| Finding | Owner/disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Parent, applied | Details P01-T01 now fixes actual derived profiles, population/statistic definitions, exercise expectations and shared negative guards |
| PC-002 | Parent, applied | Details coverage table allocates annual delta tests and reuses existing transport/rate selectors; no new redundant fault tests |
| PC-003 | Parent, applied | Details terminal checklist requires clean committed candidate, approved current base, successful receipt verification and coordinator exact-head assessment; any drift/failure blocks publication |

No unresolved user decision blocks bounded implementation. Historic adverse
outcomes remain unchanged; current direct dispositions do not close them.

## Follow-Up Items

* #193: integrate with actual #111/#133 tests when those consumers exist.
* #184/#194: independently approved live operation/credential lifecycle evidence.
* #190: coordinator/owner disposition of open child stories; no remote mutation.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-30/sensor-simulation-validation-190-changes.md.
Ready task after critique: P01-T01. Automatic parent owns continuation.
