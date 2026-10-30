---
title: Sensor simulation validation 190 phase details
description: Evidence boundaries and task-level completion checks
ms.date: 2026-10-30
---

## Metadata

Task ID 190; slug sensor-simulation-validation-190.
Plan: .copilot-tracking/plans/2026-10-30/sensor-simulation-validation-190-plan.md.
Research: .copilot-tracking/research/2026-10-30/sensor-simulation-validation-190-research.md.

## Phase Index

| Phase | Status | Task |
| --- | --- | --- |
| P01 | Complete; final 75-test selection passed | P01-T01 |
| P02 | Complete; four added links/anchors and append-only history verified | P02-T01 |
| P03 | Complete; API 1,372 tests/318 skips, static/core/scenario checks passed; ready for original Review | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Cross-stage validation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Annual clean replay and explicit faults

Context: legacy clean seasonal backfill feeds the replay API; existing
two-day/one-home identity overlap does not independently show annual statistical
structure. Use seed 190, origin 2024-01-01 UTC, 365 days and hourly cadence
(35,040 samples). Stock anchors `VALIDATION-1..4` use forms terrace, detached,
detached, apartments. Assert actual derived `(dwelling, age, heating)`:
`(terrace,1945-1979,morning_evening)`,
`(detached,1919-1944,low)`, `(detached,pre-1919,low)`,
`(apartments,1945-1979,all_day)`. Do not supply discarded age/heating fields.
Compare clean backfill after shared observation conversion against replay.
All measurements are constructed, not the retained ERA5 record.

Boundaries: add one test file, at most twelve methods, no removals or runtime
source edits. Share setup once; individual checks for ranges/finiteness,
flatline, seasonal/diurnal structure, exact rows and per-home statistics. Reuse existing fault/count tests.
Use existing replay/observation helpers;
avoid new production abstractions. Keep test-only validation small and
mutation-test bounds/flatlines. Expectations are exercise values; zero-difference
parity is a deterministic contract, not calibrated climate accuracy.

Validation: new module verbose, existing scenario/replay/plausibility/fault/
backfill/stock tests, project Ruff/format/mypy. Completion: explicit test
results with counts, targeted negative controls and no changed model outputs.

| New invariant/population | Channel/statistic | Declared oracle | Negative control |
| --- | --- | --- | --- |
| Derived four-home profile diversity | Tuple identities | Exact profiles above; no authored overrides | Fixed expected profile mismatch fails |
| Annual per-home overlap (8,760 rows each) | Complete 13-field rows; mean, population standard deviation, inclusive quartiles | Exactly equal after canonical conversion; summaries are parity, not independent climate accuracy | Existing suffix mutations retained in stream tests |
| Each stage/home, every sample | Temperature/RH finite and within -10..45 C / 0..100% | Exercise domains, no real-home safety claim | Same guard rejects NaN, infinity, temperature 46 C and RH101% |
| Each stage/home annual distribution | Mean and population standard deviation | Exercise means temperature10..30 C/RH25..95%; spread temperature0.25..10 C/RH1..30 points | Flatline/spread guard rejects constant series |
| Each stage/home, January versus July | Mean RH (all hours) and temperature (UTC midnight only, 31 samples/month) | Exercise July RH > January +5 points; July midnight temperature > January, isolating the unheated schedule without an unsupported seasonal-amplitude claim | Repeating January's temperature or RH into July separately fails the same guard |
| Each stage, all_day profile, January UTC noon/midnight | Mean temperature | Exercise noon > midnight +1 C, 31 samples/group | Nonempty group counts explicitly checked |
| Each stage/home full hourly sequence | Longest identical paired run | Fewer than24 hourly samples; gaps are absent in this clean fixture | Same guard rejects a 24-slot held pair |

Existing-vs-new allocation: new tests cover the annual multi-home horizon,
derived-profile assertion, separate stage plausibility and shared-guard
negative controls. Existing `test_sensor_stream` covers exact nominal suffix,
gap/duplicate/fault counts and pacing. Existing `test_sensor_plausibility`
covers stochastic profile mix/dropout/outlier rates. Reuse those selectors,
do not reimplement their counts.

Unresolved: composed ERA5 continuity is not supplied by this replay; preserve
that limitation rather than generalizing the overlap evidence.

<!-- rpi:phase id=P02 -->
## P02: Documentation reconciliation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Both-stage schemas, run boundaries and child dispositions

Targets: `src/core/README.md`,
`docs/reference/research/retrofit-synthetic-data/data-dictionary.md`,
`docs/reference/research/iot-sensor-analytics-research-plan.md`,
`docs/reference/README.md` and `docs/reference/log.md`.

Context: dictionary's older versions and unavailable-runner claim contradict
current code. Update current sensor versions from actual module constants.
Describe replay descriptor/Frame metadata separately from the closed 13-string
wire payload and actual SQL consumer. Link to existing finite publisher guide;
do not fabricate a live CLI or read credentials. Provide credential-free local
validation command, test output contract and explicit child evidence table.
Climate terms remain their dated evidence, not newly verified legal permission.

Validation: inspect added links/anchors, Markdown and diff; append-only log
prefix preserved. Completion: actual interfaces and command match code, all
remaining parent/downstream/live criteria visible without implied acceptance.

<!-- rpi:phase id=P03 -->
## P03: Validation and review readiness

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute exact local evidence

Use the isolated session venv created only after reproduced missing imports.
Run heavy tests using `flock -w 600 /tmp/ama-rpi-heavy.lock`.

From `src/api`, exact requested command:
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`.
Run project Ruff check, Ruff format --check and mypy for core and API.
Retain full external stdout/stderr and concise tracked results. Run unchanged
scenario CLI in a new external snapshot, verify all manifest hashes and fifteen
individual results. No UI files change; issue-specific Playwright/axe is not
applicable, while full-gate browser checks remain mandatory.

Completion: reconcile all markers, details and changes; one independent Review
records actual outcome and open acceptance. Parent then commits locally with
trailer and attempts `tools/rpi-checks.py --all --base a31048f15fa3120c58bacd22a375d86ae5ab7431`
to a new external directory. The runner owns the heavy lock internally; do not
nest another acquisition around it. No push.

Terminal checklist, owned by parent after the original Review:

* Preserve original Review regardless of outcome; adverse outcomes remain open
  and block a publication-ready claim. Route findings to later work, no repeat.
* Commit all intended implementation/original RPI inputs. Require no remaining
  dirty, untracked or ignored candidate inputs.
* Fetch `origin/main`, compare with approved base
  `a31048f15fa3120c58bacd22a375d86ae5ab7431`; drift blocks the gate/publication,
  not permission to rebase or substitute an unreviewed base.
* Run full gate only at that clean committed identity, with its own 600-second
  lock admission. Missing prerequisites/lock or failed checks remain blocked;
  no cloud fallback, exemption or fabricated success.
* Successful full receipt and verification must bind exact HEAD and current
  approved main. Retain external output; run explicit `--verify-receipt`.
* Keep final gate results external without another candidate commit. A later
  source/evidence/state commit invalidates the gate and requires a new run.
* Coordinator owns required independent exact-head assessment and prepublication
  fetch/verification. This is separate from the one original implementation
  Review, not an instruction to repeat it in this task.
