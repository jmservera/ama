<!-- markdownlint-disable-file -->
# RPI Phase Details: Sensor scenarios and documentation

## Metadata

* Task ID: 190
* Task slug: sensor-scenarios-190
* Related plan: .copilot-tracking/plans/2026-10-27/sensor-scenarios-190-plan.md
* Evidence: .copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Scenario inputs and evaluator | Complete; 15 scenario tests and strict scoped checks pass | P01-T01 |
| P02 | Tests and documentation | Complete; source, tests and four KB/guide updates | P02-T01 |
| P03 | Validation and Review preparation | Complete; API 1,121 tests, 314 skips; other evidence in changes | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Scenario inputs and evaluator

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement deterministic packs, separate truth and per-check reports

Reuse `sensor_backfill.readings` with no implicit faults and explicit synthetic
weather, `sensor_faults.observation`, `sensor_identity`, provenance snapshot
helpers. Use fixed 28-day hourly UTC windows, paired weekly noise/cycles for
before/after comparisons and distinct reproducible RNG keys. New scenario IDs are
neutral; source/scenario/schema are common across cases.

Damp targets (exercise): normal/seasonal negative; condensation-prone,
sustained RH and repeated overnight peaks review candidates; stuck and
75%-missing insufficient. Comparator checks finite physical exercise domain,
unique contiguous expected timestamps, units/calibration/synthetic labels,
>=90% coverage and no >=24-hour flatline before classifying. RH persistence
>=12 consecutive hours at >=75% or >=3 nights with >=3 high-RH overnight
samples signals an exercise review candidate, not mould or condensation.
No surface reading, diagnosis or dew-point physical claim is added.

Retrofit overlay targets: +2 C/-10 RH points immediate, zero no change,
+1.5 C/-6 points delayed seven days, -1 C/+8 points adverse. Explicit completion
day 14, delayed activation day 21. Same periodic clean baseline before/after;
first/early/late seven-day means prove direction/size and delay with 0.02
tolerance for serialized values. Neither adverse nor beneficial overlays are
claimed as the calibrated #180 physical model.

Analysis directory holds only common-schema CSV and neutral window metadata.
Truth contains seed/label/expectation/parameters; report consumes comparator
outputs, joins truth afterward and binds input hashes. Reports include
per-check outcomes, confusion cells with eligible/excluded denominators and
70/75/85 RH sensitivity. Output outside repositories and nonsymlink/new/empty;
seed integer >=0, <=2**63-1. Bound all generated data (11*672 nominal slots).

Completion: installed CLI produces repeatable files with exactly these
contracts and independent checks; no general backfill behavior changes.
Unresolved: actual downstream integration is not a fixture acceptance claim.

### Critique-resolved contracts

The observation seed is the common actual pack seed (not an answer code).
Only truth records internal RNG keys. Predictions must ignore seed and identity.
Expected timestamps form [start,end), exact UTC hours, strictly increasing and
unique. Missing slots are allowed only with >=90% coverage in every evaluated
UTC day and the full window. Each overnight is UTC [00:00,06:00) on its calendar
date with >=90% coverage (therefore all six samples); gaps break consecutive
runs. Retrofit baseline [day0,day7), early [day14,day21) and late [day21,day28)
each independently require >=90% coverage per day and overall. Missing/invalid
windows expose counts/reasons and null deltas, never a negative classification.

Confusion uses only the seven damp cases, one trial per case. Fixed truth has
three REVIEW_CANDIDATE, two NO_EXERCISE_SIGNAL and two INSUFFICIENT outcomes.
TP/TN/FP/FN use only binary predictions of binary truth; unexpected insufficient
predictions are separate abstentions and remain in eligible denominator.
Expected-insufficient cases have separate correct/incorrect sufficiency counts.
Rates expose binary-classified denominators and are null for zero denominators.
Sensitivity repeats observations-only analysis against identical fixed truth
at 70/75/85. The four retrofit cases never enter binary confusion.

Before creating output, reject every symlink component, any ancestor with a
.git directory or file (including other worktrees), existing file and nonempty
directory. Truth manifest records generator/evaluator versions, transitive
source fingerprint, Python version, seed/internal keys, start/end/cadence,
synthetic weather identity and relative payload hashes (no absolute/clock data).
Truth-side report binds those hashes and rule configuration. Reuse existing
provenance helpers after the stricter module-local preflight.

<!-- rpi:phase id=P02 -->
## P02: Tests and documentation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add semantic/regression tests and update simulator knowledge

One new test file under core/tests, at most 24 test methods. Test each label,
seed reproducibility and variation, neutral paths/columns, hashes, missing/fault
sufficiency, confusion/misses/false alerts, threshold exactness, delayed boundary
and counterfactual/no-step. Mutate observations and expected output to prove
checks reject bad inputs, not merely assert a success-shaped pack.

Extend core README with a reproducible external CLI command, parameter table,
two-stage status and safe future live prerequisites. Update dictionary's Sensor
data section for composed/fault schemas, package parameters, climate provenance
and new analysis/truth/report fields. Keep source licences historical/qualified.
Integrate bounded R3 exercise evidence in the existing research synthesis;
update KB index and append log without changing memory or original case study.

Completion: docs match executed commands and schemas, limitations trace to
open dependencies, local links resolve. No new public scientific claim.

<!-- rpi:phase id=P03 -->
## P03: Validate and preserve independent Review

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run targeted local tests, lint/types and CLI for Review

Use the isolated pip-installed environment (initial import failed, so install
is justified). Target new tests plus existing sensor, climate, indoor,
household, retrofit, provenance and dependency tests; run API supplied suite
with tests-only PYTHONPATH. New modules must pass scoped ruff/format/mypy.
Record exact commands/counts and byte/hash evidence in changes.

Before Review reconcile all implementation markers, docs, changed files and
remaining acceptance. A fresh independent worker activates rpi-review and writes
only .copilot-tracking/reviews/logs/2026-10-27/sensor-scenarios-190-review.md.
One execution, original outcome preserved; no correction/re-review loop.
Publication claims distinguish bounded engineering completion from residual
#193/#194/#190 integration gaps, owner decisions and unrun hosted checks.
