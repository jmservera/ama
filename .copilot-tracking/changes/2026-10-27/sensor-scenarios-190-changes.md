<!-- markdownlint-disable-file -->
# RPI Changes: Sensor scenarios and documentation

## Metadata

* Task ID: 190
* Task slug: sensor-scenarios-190
* Implementation date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md
* Details: .copilot-tracking/details/2026-10-27/sensor-scenarios-190-phase-details.md

## Execution Status

Complete for the full bounded implementation plan P01-P03.
P01/P01-T01, P02/P02-T01 and P03/P03-T01 have completion evidence.
This does not complete whole-issue #190/#193/#194 acceptance.
Approved writes: scenario module, one core test file, existing simulator/KB
documentation and RPI artifacts. No source changes outside this boundary.

## Execution Summary

Research and one independent critique completed. Direct compatible critique
findings reconciled; original Revise retained. No routine approval required
under the explicit full-loop request.

## Completed Work

### Deterministic isolated scenarios and observations-only comparison

P01-T01: added src/core/src/zava_forward/core/synthetic/sensor_scenarios.py,
seven damp cases and four paired retrofit profiles, exact shared 13 fields,
common actual seed and neutral identifiers. Evaluator truth is isolated under
truth/; the comparator never consults it. A stricter preflight rejects symlink
components, repository/worktree outputs, files and nonempty directories.
Source/runtime/weather/parameter provenance and exact relative hashes are
retained separately from analysis.

The installed default CLI produces 11 cases/6,888 rows and 15 independent
checks (seven outcomes, eight early/late deltas), all matched at seed 190.
Confusion: total7, eligible5, classified5, TP3/TN2/FP0/FN0, abstained0,
expected-insufficient2/correct2/incorrect0. At RH85, TP2/FN1, miss rate1/3;
the same truth is used at RH70/75/85. No overall pass or clinical/causal claim.
Initial external report is under the session files sensor-scenarios-190-evidence;
final-source reproduction uses a new destination, not an overwrite.

### Persisted per-check evidence at the final implementation source

External snapshot:
/home/azureuser/.copilot/session-state/4c91dce0-1673-48ca-ada6-d4c8cbdd4e63/files/sensor-scenarios-190-final.
All payload hashes verified against truth/manifest.json.
Generator revision:
`sha256:a55faf55844fab0ccc5c04d9612b0cac9c2f52e8daeddc28e611a032283eda06`.
Manifest SHA-256:
`ce74864f5cac951a425738ce9c6f6896b539717e2b441147b64a0428b959e249`.
Report SHA-256:
`da00b5bced8f5a0a389efc6ad546e94bf4983c789142d5ae97d1c738ecbe2e20`.
These identify engineering evidence, not a local full-gate receipt.

| Case/check | Expected and observed | Per-check result |
| --- | --- | --- |
| C01 normal | NO_EXERCISE_SIGNAL, valid672/672 | PASS |
| C02 condensation-prone | REVIEW_CANDIDATE, valid672/672 | PASS |
| C03 sustained humidity | REVIEW_CANDIDATE, valid672/672 | PASS |
| C04 overnight peaks | REVIEW_CANDIDATE, valid672/672 | PASS |
| C05 sensor fault | INSUFFICIENT, valid672/672, FLATLINE | PASS |
| C06 missing | INSUFFICIENT, valid168/672, DAY/NIGHT/WINDOW_COVERAGE | PASS |
| C07 seasonal shift | NO_EXERCISE_SIGNAL, valid672/672 | PASS |
| C08 improvement early | +2 C/-10 RH points | PASS |
| C08 improvement late | +2 C/-10 RH points | PASS |
| C09 no-change early | 0 C/0 RH points | PASS |
| C09 no-change late | 0 C/0 RH points | PASS |
| C10 delayed early | 0 C/0 RH points | PASS |
| C10 delayed late | +1.5 C/-6 RH points | PASS |
| C11 adverse early | -1 C/+8 RH points | PASS |
| C11 adverse late | -1 C/+8 RH points | PASS |

Every size/window is an exercise value; no case is a real-home finding.
The eight retrofit comparisons have 168/168 valid samples per comparison
window. Insufficient synthetic data never yields a reassuring negative.

### Semantic/mutation tests and simulator knowledge

P02-T01: one new src/core/tests/test_sensor_scenarios.py, 15 test methods,
zero removals. Tests prove default cases, independent false alerts/misses/
abstentions/wrong sufficiency and zero denominators, gap distribution/night/
persistence boundaries, exact retrofit/delay/no-change, retained-reading replay,
bytes/hashes, output refusal and installed CLI exit0/1/2.

Updated src/core/README.md, existing sensor dictionary and IoT R3 synthesis,
KB index and append-only log. Both-stage status is explicit: shared schema/
volume is delivered, live runner is absent. Exact ERA5 attribution, terms
snapshot and synthetic-demo-only approval are preserved; scenario weather is
constructed and does not inherit ERA5 source evidence.

## Implementation-Time Plan and Detail Updates

No material divergence. P03 wording clarified to prepare Review rather than
include Review inside its own prerequisite; the independent lifecycle Review
still executes exactly once afterward. Common actual observation seed preserves schema;
evaluator-only internal RNG keys preserve accurate provenance. The critique's
claimed /tmp prohibition is unsupported and rejected, not worked around.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Installed package import | Current worktree | Initially failed | ModuleNotFoundError with system Python |
| pip environment | /tmp/ama-syn190-venv | Passed | Editable core[dev], agents and API installed after missing dependency failure |
| Heavy/full gate | P01-P03 | Not run | Bounded offline fixture/documentation work; no full gate authorized and no scoped heavy invocation used |
| Core regressions | 17 named sensor/model/provenance/dependency modules | Passed | 173 tests, 1 opt-in local SQL skip; 82.977s |
| New scenario tests, final malformed-window check | src/core/tests/test_sensor_scenarios.py | Passed | 15 tests, 4.806s |
| Ruff check/format | Two new Python files | Passed | All checks pass, formatted |
| Strict mypy | Two new Python files | Passed | No issues in two source files |
| API unit suite | Supplied discovery command with tests-only PYTHONPATH | Passed | 1,121 tests in 904.506s, 314 skips; no Azure deployment/live opt-in checks |
| Initial whole-file link scan | Five changed tracked Markdown files, 735 links | Failed on baseline links | Ten missing historical deck/retired-MVP links, no newly added target identified; validate additions separately |
| Added Markdown links/anchors | 12 new local targets | Passed | Zero errors; pre-existing missing historical targets not changed |
| Final-source installed CLI | 11 cases/6,888 rows/15 checks | Passed per check | Exact hashes and individual observations above |

Initial development failures were corrected before Review: duplicate provenance
source entry caused the first CLI failure, JSON tuple/list representation broke
roundtrip equality, and test ClassVar typing/formatting needed reconciliation.
The source fingerprint now reuses the dependency closure once, report serialization
roundtrips exactly and scoped strict types pass. Malformed retrofit input remains
INSUFFICIENT rather than raising a slicing KeyError. Original critique unchanged.

## Pre-Review Reconciliation

Plan/details P01-P03 markers are complete; source/tests/docs and validation
evidence reconcile. No remaining active-plan task; actual downstream/live
acceptance remains separately visible below. Review ready at staged candidate
based on 0ded682bab690d24eb59b78e704be82d337bf6cd (fetched main).
Human and hosted approval not performed. No full/scoped-heavy receipt claimed.

## Blockers

No independent fixture blocker. Actual #111/#133 test use and runnable #184
remain unmet; no invented owner deferral or approval.

## Remaining Work

None within P01-P03. Independent Review is the next lifecycle phase.

## Follow-Up Items

Canonical plan Follow-Up Items: downstream #111/#133 integration, runnable
#184 documentation and owner disposition of remaining #190 child criteria.

## Return-to-Caller State

Automatic Implement complete, ready for the single independent Review.
No new scope/authority decision. Parent RPI Agent owns advancement.

## Exact local validation commands

External environment: /tmp/ama-syn190-venv, editable core[dev], agents and API.
From src/core, with that environment's Python:

```bash
PYTHONPATH=tests python -m unittest test_sensor_scenarios test_sensor_backfill test_sensor_stock test_sensor_faults test_sensor_plausibility test_historical_backfill test_climate_history test_indoor_projection test_household_conditions test_retrofit_effects test_synthetic_provenance test_synthetic_determinism test_synthetic_output_dir test_dependency_rule test_sensor_consumer test_sensor_privacy test_resident_sensors -q
python -m unittest discover -s tests -p test_sensor_scenarios.py -q
mypy src/zava_forward/core/synthetic/sensor_scenarios.py tests/test_sensor_scenarios.py
```

From src/api:

```bash
PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q
```

From repository root:

```bash
ruff check src/core/src/zava_forward/core/synthetic/sensor_scenarios.py src/core/tests/test_sensor_scenarios.py
ruff format --check src/core/src/zava_forward/core/synthetic/sensor_scenarios.py src/core/tests/test_sensor_scenarios.py
git diff --check
```

Existing API failure-path logging and legacy test ResourceWarnings were observed;
they did not fail the suite. Skips are unperformed checks, not passes.
The commit helper's referenced commit-message instruction file and
get_changed_files tool are unavailable in this host; use the caller's explicit
Conventional Commit/trailer instructions and staged Git evidence, without
claiming that unavailable helper ran.
