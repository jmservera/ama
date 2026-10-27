---
title: Indoor derived bounds implementation evidence
description: Issue 179 changes, checks and acceptance evidence
ms.date: 2026-10-27
---

## Execution and Scope

Task 179 / indoor-derived-bounds-179. Implement P01 and P02 of
.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md.
Research Ready; one critique Complete / Revise, PC-001 directly applied.
Execution: Complete for the full plan. All P01/P02 markers are complete.
Single Review: Complete / Conformant; PR502 published. Earlier checkpoints
and failures below are preserved with their later dispositions.

## Decisions and Boundaries

Shared per-outdoor-record baseline/vapour math, bounded exercise residuals,
physical RH saturation only; version both projection models. No private data,
cloud or whole-stock generation. No heavy gate for this small correction.
Operational/calibration/human approval remains outside this story.

## Validation

Initial uninstalled baseline failed with ModuleNotFoundError. Created an
isolated external session venv and installed core/agents/API editable with pip.
Baseline canonical projection tests: 4 passed.

Combined relevant core check passed: 142 tests, one existing optional SQL skip
(141 executed passes), in 70.926 seconds. This includes ten canonical projection
tests, actual full public history traversal, stock/fault/privacy/provenance,
household/dated effects, historical writer/replay and consumer regressions.
Existing unclosed-file ResourceWarnings were emitted by test_sensor_backfill;
no test failed. API discovery was still running at that checkpoint; final
failure/restoration/retry evidence is recorded below.
Ruff/mypy were absent; installed the project's declared dev extra into the
isolated venv. Initial lint found formatting/import issues in the new code;
the formatting/import corrections are complete. Final changed-file ruff,
format check and strict mypy passed. Final canonical rerun: 10 tests passed
in 5.005 seconds. Dependent resident sensor suite: 9 tests passed.

### Reproduction Commands

Commands use the installed isolated venv's Python (substitute its executable
for `python3`), never a source-package PYTHONPATH:

```bash
cd src/core
PYTHONPATH=tests python3 -m unittest \
  test_indoor_projection test_historical_backfill test_climate_history \
  test_household_conditions test_retrofit_effects test_sensor_backfill \
  test_sensor_stock test_sensor_faults test_sensor_plausibility \
  test_sensor_privacy test_sensor_consumer test_synthetic_provenance -q
python3 -m unittest discover -s tests -p test_resident_sensors.py -q
python3 -m ruff check src/zava_forward/core/synthetic/indoor_projection.py \
  tests/test_indoor_projection.py
python3 -m ruff format --check src/zava_forward/core/synthetic/indoor_projection.py \
  tests/test_indoor_projection.py
python3 -m mypy src/zava_forward/core/synthetic/indoor_projection.py \
  tests/test_indoor_projection.py
cd ../api
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q
```

One skipped core test is the existing opt-in own-local-SQL test in
test_sensor_privacy, gated by ZF_SENSOR112_MSSQL=1. It is not a projection
test; no SQL/platform result is inferred. No heavy gate was run: task-specific
authorization allows --changed only for large changes and forbids --all.
Git diff whitespace review and existence checks for all three newly added
relative links passed. Fetched main/base:
0ded682bab690d24eb59b78e704be82d337bf6cd (same as branch starting HEAD).

### Actual Public-Record Measurement

The same nominal replay was independently measured after the test run.
All rows are SYNTHETIC. Values below are sample extrema, not fixed limits;
every row was checked against its own tighter paired-record envelope.

| Dwelling / path | Rows | Actual T C | Derived overall T envelope C | Actual RH % | Derived overall RH envelope % |
| --- | --- | --- | --- | --- | --- |
| apartments / legacy | 17,544 | 15.42..21.40 | 15.2377..21.7150 | 20.83..100 | 17.0588..100 |
| apartments / composed | 17,544 | 14.53..23.01 | 14.2377..23.5159 | 17.55..100 | 13.3382..100 |
| detached / legacy | 17,544 | 14.81..21.40 | 14.4986..21.7150 | 27.54..100 | 23.5380..100 |
| detached / composed | 17,544 | 13.98..23.01 | 13.4986..23.5159 | 19.46..100 | 15.0733..100 |

These are apartments/detached with pre-1919 age and construction loss 1.15,
seed 183, no faults, UTC 2023-01-01 through 2025-01-01 exclusive. Composed
mode uses explicit conditions and a synthetic Cavity wall completion at
2024-01-01 with exercise loss factor 0.85. Old 15%/98% clips would not describe
these envelopes. The supported-domain cold/dry/tail tests additionally prove
nominal temperature below 8 C and RH below 15%, without scientific claims.

## Completed Work

### P01: Shared derived nominal envelope

Both validated entry points now share noiseless baseline/vapour math and
bounded Gaussian residuals, keeping the original two-draw order. v2 manifests
include the noise/tail parameters and per-pair temperature/RH envelope equations.
The physical saturation domain is 0..100%; 8/15/98 no longer bound projections.
No generator caller/schema/ingestion policy or historical snapshot was changed.

The canonical suite retains and amends both v1 reference/fixed-bound methods,
retains invalid-input/fingerprint tests and adds six test methods (ten total),
within the approved maximum twelve additions. Independent v2 reference
equations, RNG state/call order, forced tails/saturation, complete supported
fabric endpoints and composed extrema supplement 17,544 paired public hourly
records times two dwellings times two generator paths = 70,176 nominal rows.
Each history is also regenerated and compared exactly. The public raw and
metadata are hash-pinned; no external retrieval or private inputs.

### P02-T01: Related documentation

Core README documents v2 inputs/equations, exercise assumptions, derived
envelopes, fault/rounding and versioned-byte boundaries. Existing IoT synthesis
has a prospective three-criterion audit without rewriting original adverse
outcomes; index and append-only log updated. Existing empirical calibration,
OD-43, parent/live PRD and human approval limits remain explicit.

## Amendments and Divergences

None. PC-001 adds explicit composed numeric and RNG-call/state tests within
the approved test budget; it changes no scope or user decision.

## Completion and Review Handoff

### Initial Pre-Review Checkpoint (Historical)

Model, tests and documentation are complete, with core and static checks
passing. Review-ready engineering boundary: P01 and P02-T01, completed
P02-T02 checks and all #179 criteria. Supplemental API discovery remains
running and P02-T02 stays unchecked until its result is known; publication
P02-T03 stays unchecked. No missing engineering evidence is disguised as a
pass. The single independent Review can inspect the completed source/test/
documentation boundary while the read-only supplemental validation finishes.
No further source edits are planned; no material divergence or user decision.
Historical calibration/OD-43/parent/live PRD work remains outside this story.

### Final Validation and Single Review Disposition

API discovery completed with four failed-test import entries because the
isolated venv lacked the API's declared azure-identity dependency:
1,058 entries, 744 passes, 310 skips, four errors, 830.173 seconds.
Installed the API using pip against its unchanged manifest and reran only
test_resident_aoai, test_resident_aoai_sql, test_resident_assistant_api and
test_resident_demo_api: 67 run, 61 passed, six optional SQL skips, zero errors,
37.650 seconds. The failure is retained, not relabelled as a green full suite.
The reconciled actual API test set totals 805 passes / 316 skips over 1,121
tests after replacing the four failed imports with their 67 real test cases.

Retry command from src/api:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest \
  test_resident_aoai test_resident_aoai_sql \
  test_resident_assistant_api test_resident_demo_api -q
```

Independent Review execution Complete; outcome Conformant at the synthetic
exercise boundary, zero findings, all three #179 criteria supported. Canonical
record: .copilot-tracking/reviews/logs/2026-10-27/indoor-derived-bounds-179-review.md.
No source fix or second Review followed. No significant divergence.
Implementation and local validation are complete (P01/P02-T01/P02-T02).
P02-T03 publication remains; owner merge/hosted checks and future live
calibration/OD-43 are separate. Publication may use Closes #179, Refs #177.

## Publication and Final State

P02-T03 complete. Initial implementation and all original RPI evidence were
committed as 3d24537aab944fad5e1812dd819a87b7d5b27b5b with Conventional Commit
and required Copilot co-author trailer. Local privacy-safe author/committer
email resolved from authenticated gh account, not private/global configuration.
Pushed only feat/indoor-derived-bounds-179, without force; one PR to main:
https://github.com/jmservera/ama/pull/502 (Closes #179, Refs #177).

All P01/P02 tasks complete; manual full requested loop ends at Review,
task completed/session stopped. No additional child work is started. Final
evidence-only bookkeeping records publication; model/test fingerprints in the
Review stay unchanged. No second critique/Review, merge, deployment, full gate,
private-data read or unearned approval. Owner review/merge and hosted checks
are the next action. Future real-use calibration/OD-43 stays a distinct
owner-selected follow-up.

## Correction cycle 1 (2026-10-27, PR #502)

Scope P03/P04, new user-authorized ordered loop. Original critique/Review and
validation claims above are historical, not overwritten. Research executed /
Ready, correction plan Ready; one critique Complete / Revise, PC-C1-001
directly applied (isolated stale-version refusal with no downstream effects).

### Versioning decision and causal evidence

The indoor-envelope change deliberately alters new rows. Repository convention
in docs/reference/research/retrofit-synthetic-data/README.md, refresh policy,
requires a containing pack version bump for row changes and exact reproduction
only with the same revision, inputs, runtime and parameters. Old published
bytes must not be overwritten. Restore neither old fixed clips nor unbounded
tails merely to satisfy an obsolete golden.

Hosted run 40577511316: 1,435 run / one failure / 186 skipped. The earlier
selected local suite omitted test_synthetic_determinism, so its original
Conformant review did not prove full core CI. Initial local attempt failed
because core was uninstalled; pip-restored core with its declared dev extra
in an external session venv on Python 3.12.3. Focused reproduction: seven
tests, six pass / exact historical hash failure.

Independent v1 baseline/floor/RH equations, applied only in an ephemeral
measurement with identical inputs and Gaussian draws, reproduced the old
SHA exactly. No old code added to production. Default seed183, stock seed
unchanged, 12 homes, three days, default hourly cadence/start:

| Projection | readings-0000.csv SHA-256 |
| --- | --- |
| Original v1 | `657ff373107807b34bd4bb6720dec534fcef13134292c5d753ef24bdbd723549` |
| Derived-envelope v2 | `25bb5259d89554560e179ae5412f3148595c47a87def9ee2fca61518e18ded5b` |

Both have 861 rows. Exactly one temperature and four humidity fields differ;
all other reading fields and sensors.csv bytes are identical. These differences
are the intended bounds/tail change, not seed, ID, schema, timestamp, fault,
ordering or random-stream drift. No existing dataset is read or refreshed.

Implementation starting: advance default/stock/composed/fault snapshot
versions, preserve component/schema versions, bind new golden to literal
versions and test stale snapshot admission plus current/historical privacy.
All #179 criteria remain to be revalidated before retaining Closes #179.

### P03-T01 implementation

Default/stock/fault/integrated snapshot versions are now v3/v2/v2/v2.
Writers/readers share explicit constants; fault snapshot metadata separately
records the unchanged v1 packet model. Projection equations, RNG, schemas,
truth version and fabric/identity versions are unchanged by this correction.
Privacy auditing recognizes both historical stock-v1 and current stock-v2,
including empty selections; loader admission recognizes only current versions.
The new default golden asserts literal snapshot v3 / model v2. Scale and
sensor-register golden digests remain exactly unchanged.

Two new test methods cover isolated default/stock/composed stale versions
with current revision/payload hashes. Existing manifest tests now assert
literal stock/integrated/fault snapshot versions and unchanged fault schema/
algorithm. Existing privacy regression checks populated/empty stock layouts
under both versions. Existing positive loader/consumer tests remain.
PC-C1-001 is implemented: private verification asserts the specific unsupported
version/provenance error, public admission refuses, and no replay writer,
schema or SQL calls occur. Composed refusal additionally precedes scratch
allocation and consumer processing. The existing legacy loader still allocates
an empty temporary context before validation; this is not replay/output/SQL.
This clarifies the plan's shorthand "no scratch" for the composed path without
an unrelated legacy-loader refactor.

### P03-T02 static validation checkpoint

Exact full-project CI commands from src/core, isolated pip-installed dev extra:
`ruff check . && ruff format --check .` and `mypy`. Final result: all lint checks
passed, 100 files formatted, mypy no issues in 153 source files. Initial mypy
found that a test accessed a non-exported tempfile module through sb; changed
to the existing string-path mock pattern, then formatting and all static
checks passed. This changes no tested behavior. Initial full unit discovery
was already running; its final outcome and final affected-module verification
will be recorded below. State unique-key JSON and Git whitespace checks pass.
No heavy gate, cloud, private dataset or hosted acceptance inference.

### P03 final validation and criterion reconciliation

Final source/test edits are complete. From src/core, Python 3.12.3, isolated
external session venv, pip-installed `-e ./src/core[dev]` with declared pins:

```bash
python -m unittest discover -s tests -v
ruff check . && ruff format --check .
mypy
```

Final exact discovery: **1,437 run, 1,251 passes, 186 existing optional skips,
zero failures/errors**, 433.719 seconds. Final exact lint/format: all checks
passed, 100 files already formatted. Final exact mypy: success, 153 source
files. First full discovery also passed (1,437 / 186 skipped, 421.479 seconds)
but overlapped the test-only typed mock-target edit; the complete final rerun
above removes any candidate ambiguity. No reduced selector is substituted
for the requested CI suite. Full logs remain in the external session files
as core-unit-correction1.log and core-unit-correction1-final.log.

All ten canonical indoor tests pass unchanged, including 70,176 nominal
paired-record rows and exact RNG/envelope tests. Criterion 1 retains
versioned model/parameter/manifest proof and now honest containing snapshot
versions; criterion 2's explicit exercise labels are unchanged; criterion 3's
derived per-row envelopes remain proven at the synthetic-model boundary.
Closes #179 remains justified; no parent/live PRD/OD-43 acceptance is claimed.
The 186 skips are existing opt-in/optional boundaries, not completed live
SQL Server, blob or operational checks. Pre-existing unclosed-file warnings
remain in the output, not failures.

Reconciliation: P03-T01/P03-T02 complete; P04-T01 independent Review and
publication remain. No implementation blocker, extra dependency, schema/
workflow/check-name change, heavy gate or dataset refresh. Upstream rubric-bot
commit a06c2063 was retained by clean fast-forward, not rewritten.

### P04 independent Review and publication handoff

Single independent correction Review execution Complete; outcome Conformant
at the synthetic-model boundary, no RV-C1 findings. Original Review remains
byte-preserved. Reviewer independently reproduced both causal hashes and the
861-row / 1 temperature + 4 RH differences, and passed configured lint/format
and nonincremental mypy. Independent selected tests: 22 methods, 13 passed,
nine errored because the reviewer's checkout-local scratch was refused by the
existing external-output guard. These errors are not passes; all affected
methods were explicitly verified `ok` in the supplied final external full-suite
log. An explicit-path formatting probe also failed on existing excluded files;
the exact configured full-core CI-format command independently passed.
Full details and limitations are appended to the canonical review artifact.

No source or test change follows Review. No material finding remains open.
P04-T01 Review is complete; commit/push/PR evidence update remain. Owner
review/merge, hosted checks, future calibration and OD-43 remain separate.
Task-specific publication direction explicitly forbids --all; no complete
local-gate receipt or independent published-head gate is claimed.
