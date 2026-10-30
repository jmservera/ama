---
title: Sensor simulation validation 190 changes
description: Current implementation and local evidence with explicit acceptance limits
ms.date: 2026-10-30
---

## Metadata

Task ID 190; slug sensor-simulation-validation-190.
Plan: .copilot-tracking/plans/2026-10-30/sensor-simulation-validation-190-plan.md.
Details: .copilot-tracking/details/2026-10-30/sensor-simulation-validation-190-phase-details.md.

## Execution Status

Full plan P01-P03 Complete. P01/P01-T01, P02/P02-T01 and P03/P03-T01
have completion evidence and are ready for one original Review. One new test module has
nine methods, zero removals and no runtime changes. Documentation remains
within the five named existing files.

## Execution Summary

Research executed / Ready. One independent critique Complete / Revise, all
three direct corrections applied before implementation. Parent acceptance,
live services and actual downstream consumers remain separate.

## Implementation-Time Plan and Detail Updates

No material scope divergence. Critique disposition fixes fixture/profile
oracles, removes duplicate fault additions and makes exact-head publication
fail closed. Original critique and historical adverse Reviews are unchanged.

### Seasonal population correction (P01-T01)

The first locked run executed eight tests in 1.803s, with six seasonal subtest
failures: whole-day January/July temperature means differ by only 0.129,
0.392 and 0.468 C in three profiles. A common absolute >0.5 C monthly-mean
oracle was not justified because heating changes seasonally. Rather than
lowering it to match observed results, restrict the temperature comparison to
UTC midnight, when every existing schedule is unheated. The model's outdoor
summer gain and winter loss then have the same baseline setpoint; retain an
explicit >1 C exercise expectation and exact 31-sample month groups. All-hours
RH seasonality remains independently checked. This is a local test-population
correction, not a model change, new user decision or repeated critique.
Details and test oracle reconcile. Original failing log retained externally as
`stage-tests.log`; corrected results will use a new log.

The second locked run executed 74 tests in 8.346s, with eight seasonal
subtest failures: the unheated-month direction is positive in all four homes
but the invented >1 C amplitude is unsupported by this model. Final oracle
therefore checks the physically intended model direction, not a fitted
amplitude. Separate temperature/RH repeated-month mutations must fail the
same seasonal guard, so a constant/repeated month cannot satisfy it. This
removes the unsupported amplitude claim rather than calibrating it from the
observed sample. Added one negative-control method (nine total, within12).
The original second log is retained as `core-tests-corrected.log`.

Core Ruff check/format and mypy passed (113 formatted files, 166 typed source
files). API Ruff check/format and mypy passed (60 formatted files, 116 typed
source files). The corrected final core check also passed. One wrapper attempt
with `RUFF_NO_CACHE=1` failed argument parsing before checking; corrected to
the tool's supported `true`, not a lint suppression.

The first full API discovery invocation exited 1 without executing tests after
the requested 600-second lock admission timed out. The full command is retried
with verbose flock diagnostics in a separate log; neither timeout nor queued
work is counted as a pass. Corrected core regressions are also queued under
the lock. No other user's lock or process is modified.

Added Markdown links/anchors: four verified, zero errors. The pre-existing
KB log is an exact byte prefix of the updated log. `git diff --check` passes.
Fetched `origin/main` remains the supplied base
`a31048f15fa3120c58bacd22a375d86ae5ab7431`.

## Completed Work

### P01-T01: Annual cross-stage contracts

Added `src/core/tests/test_sensor_stage_validation.py`: asserted actual
four-home profiles, 35,040 hourly samples/stage, exact per-home rows and
mean/population-spread/inclusive-quartile parity, independent exercise domains,
annual means/spreads, RH/midnight seasonal structure, all-day winter diurnal
structure, flatline rejection and separate range/seasonal/flatline mutations.
No new runtime module or schema, no removed tests.

Final core selection: 75 tests / 7.487s, exit0, no skips. All nine new tests
passed along with existing scenario, stream, plausibility, fault, stock and
backfill modules. Existing unclosed-file ResourceWarnings in backfill tests
were not failures and were not changed. Actual `flock --verbose` output:
admission took486.446413 seconds, then executed Python under the lock.
Final source Ruff/format/mypy also passed, 113 formatted/166 typed files.

### P02-T01: Current two-stage documentation

Updated core README, existing dictionary, IoT synthesis and KB index/log.
Dictionary now matches current snapshot versions and distinguishes replay/
Frame/descriptor/evaluator data from the closed13-field wire row and SQL
storage. It links actual opt-in SDK operation without inventing credential-free
live commands. Added annual per-check test recipe and explicit child
dispositions. Original research/Review/license evidence remains unchanged.
Four added local links/anchors and the historical log prefix verified.

### Retained scenario per-check evidence

Installed unchanged CLI generated a new external snapshot at
`/home/azureuser/.copilot/session-state/9929c271-0d06-4d32-b0a7-41707433d2c8/files/scenario-snapshot-batch`.
Verified all14 manifest payload hashes, eleven cases, 6,888 rows and fifteen
independently reported PASS results. No overall pass field.

| Case | Check(s) | Result |
| --- | --- | --- |
| C01 normal | damp_outcome | PASS |
| C02 condensation_prone | damp_outcome | PASS |
| C03 sustained_high_humidity | damp_outcome | PASS |
| C04 repeated_overnight_peaks | damp_outcome | PASS |
| C05 sensor_fault | damp_outcome | PASS, expected INSUFFICIENT |
| C06 missing_data | damp_outcome | PASS, expected INSUFFICIENT |
| C07 seasonal_shift | damp_outcome | PASS |
| C08 improvement | retrofit_early; retrofit_late | PASS; PASS |
| C09 no_change | retrofit_early; retrofit_late | PASS; PASS |
| C10 delayed_effect | retrofit_early; retrofit_late | PASS; PASS |
| C11 adverse_effect | retrofit_early; retrofit_late | PASS; PASS |

Fixed confusion: seven cases, eligible5/classified5, TP3/TN2/FP0/FN0,
abstained0; expected-insufficient2/correct2/incorrect0. These are designed
exercises, not prevalence, diagnostic accuracy or approved R3 acceptance.
Hashes:

* Generator revision `sha256:27a42b5ecd3bc374c8bb470d9abd980c195e6f1d061d96b90ea37c5ebd302e69`.
* Manifest SHA-256 `fce58bcedebd76b77f507e9f7216621ab8d037a89e4968796eb9c36495d63efa`.
* Report SHA-256 `826f099cb4f7b5f01dfbc4e5b5c1f933c64c2db1ebc331dfedfc6c1b92952d70`.

### Setup-output preservation

Before gate preparation, enumerated88 task-generated ignored cache/egg-info/
bytecode files. Archived the full current tracking snapshot and selected
files externally, verified full readback, restored and SHA-256-checked every
selected file, then unlinked only those exact files with pending/removed
journal entries. All protected tracked/nonignored bytes unchanged; no
historical tracking file deleted. Archive, exact selection and restored
copies remain under the external session `files/cache-preservation/`.
Distribution version/import probes passed after cleanup. Subsequent checks
use external caches and `PYTHONDONTWRITEBYTECODE=1`.

The later full API discovery exposed a setup-cleanup defect: empty source
`.egg-info` directories remained, and with API's explicit `PYTHONPATH=src`
they shadowed the installed distribution metadata with version `None`.
The first actual full run executed1,372 tests /484.514s with one failure
(`test_version.VersionTests.test_version_matches_distribution_metadata`) and
318 opt-in skips; no other test failed. This is retained as
`api-tests-batch.log`, not silently relabelled passing.

Removed only empty generated directories derived from the exact preserved
selection, journalled externally. The API-cwd/same-PYTHONPATH metadata probe
then returned0.1.0, matching source. No source change, reinstall or dependency
relaxation. One initial directory-enumeration command was stopped before
pruning after a non-terminating parent walk; the successful bounded
`Path.parents` enumeration is finite and recorded in the existing journal.
Full API discovery is rerun after the focused version test under one lock
reservation; final results below.

The successful locked batch also reran all75 core tests in7.508s and the
scenario CLI, exits0/0. Its lock admission took349.668881 seconds.

## Final Local Validation and Commands

External environment and evidence root:
`/home/azureuser/.copilot/session-state/9929c271-0d06-4d32-b0a7-41707433d2c8/files/`.
Its isolated `venv/bin` is first on PATH. No shared venv was modified.
Final API command first reran `test_version`, then the exact requested
discovery in the same heavy-lock reservation:

```bash
cd src/api
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests \
flock --verbose -w 600 /tmp/ama-rpi-heavy.lock \
  bash -c 'python3 -m unittest -q test_version && python3 -m unittest discover -s tests -q'
```

Final core selection from `src/core`:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests \
flock --verbose -w 600 /tmp/ama-rpi-heavy.lock \
  python3 -m unittest -v test_sensor_stage_validation test_sensor_scenarios \
  test_sensor_stream test_sensor_plausibility test_sensor_faults \
  test_sensor_stock test_sensor_backfill
```

Run in each of `src/core` and `src/api`:
`ruff check .`, `ruff format --check .`, `mypy`.
Final core checks used `RUFF_NO_CACHE=true` and an external `MYPY_CACHE_DIR`;
no lint/type exclusions were changed.

| Check | Actual result | External evidence |
| --- | --- | --- |
| New/related core tests | Exit0; 75 tests, no skips; final7.487s and batch7.508s | `core-tests-final.log`, `core-tests-batch.log` |
| API focused metadata regression | Exit0 after removing empty generated metadata dirs | `api-tests-final.log` |
| API full requested discovery | Exit0; 1,372 discovered, 318 skipped, 474.772s | `api-tests-final.log` |
| Core Ruff/format/mypy | Passed; 113 formatted files, 166 typed files | Tool output; `core-mypy.log` |
| API Ruff/format/mypy | Passed; 60 formatted files, 116 typed files | Tool output; `api-mypy.log` |
| Existing scenario CLI | Exit0; 11 cases/6,888 rows/15 separate matches;14 hashes verified | `scenario-snapshot-batch/`, `scenario-cli-batch.log` |
| Added links/history/diff | Four added targets/anchors verified; original log prefix preserved; diff check passes | Tool output |
| Issue-specific browser/axe | Not applicable: no web files or UI behavior changed | Diff boundary |
| Complete postcommit local gate | Pending parent action after original Review and commit | No receipt claimed |

General-discovery318 opt-in skips are unperformed integration checks, not
passes. They do not prove browser/SQL/cloud or actual sign-in acceptance.
The original API failure and initial lock timeouts remain retained separately.
No Azure command, deployment, live sign-in, credential access, push, remote
mutation or secret output occurred.

## Acceptance Evidence

| Criterion | Proven evidence or remaining gap |
| --- | --- |
| #190 all children closed or deferred | Not proven: #191 closed, #192/#193/#194 open; no owner-accepted deferral supplied or remote state changed |
| #190 per-check reporting | Proven locally: fifteen retained expected/observed scenario checks, nine new named tests and individual existing test outcomes, not one overall pass |
| #192 seed/label/expected outcome, isolation and confusion support | Existing source and tests plus fresh retained snapshot prove all three local scenario criteria |
| #193 improvement/no-change/adverse and labelled direction/size | Proven by unchanged four-profile source, eight fresh per-window delta results and exact activation tests |
| #193 use by actual #133/#111 tests | Not proven; proposed deferral to those consumer workstreams, not an accepted owner deferral |
| #194 README/dictionary both stages, provenance/licence, synthetic boundary | Current corrected docs and linked actual replay/SDK guides support all documentation criteria; underlying source terms remain their dated qualified record, not new legal approval or a live run |

## Pre-Review Reconciliation

All P01-P03/task markers complete. Details, changes, implementation and local
validation agree. Nine additions in one test module, zero removals, five
existing documentation targets, no runtime/UI/schema/version changes.
One critique Complete/Revise retained with PC-001..003 directly resolved.
Ordinary test-oracle and metadata cleanup corrections are recorded; no
material scope divergence or unresolved source blocker.

Review readiness: Ready for the one bounded original Review against supplied
base. Whole-parent acceptance is not claimed. Postcommit full gate and
coordinator exact-head assessment remain separate publication requirements.

## Validation Record

Isolated pip environment restored after system Python reproduced missing
`zava_forward` import. No dependency/pin changes. Planned validation: targeted
core tests, unchanged CLI manifest/per-check verification, full API discovery,
core/API Ruff/format/mypy, links/diff and postcommit complete external gate.

## Blockers and Remaining Work

No remaining active implementation task. Original independent Review is next.
Whole-issue child acceptance and downstream/live criteria are unresolved.
No remote mutation or push is authorized.

## Follow-Up Items

Canonical plan Follow-Up Items: downstream #111/#133 test integration,
approved live #184 evidence and coordinator/owner child dispositions.

## Return-to-Caller State

Full plan Implement Complete; Ready for original Review. Parent owns transition,
local commit and complete external gate. Final gate results must remain external
without another candidate commit, and any failure blocks publication.
