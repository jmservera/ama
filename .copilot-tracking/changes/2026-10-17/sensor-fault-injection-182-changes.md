---
title: Sensor fault injection changes and execution evidence
description: Full-plan implementation record for issue 182
ms.date: 2026-10-17
---

## Scope and State

Full plan: .copilot-tracking/plans/2026-10-17/sensor-fault-injection-182-plan.md.
Details: .copilot-tracking/details/2026-10-17/sensor-fault-injection-182-phase-details.md.
Research Complete/Ready committed 5088a42; Plan Complete/Ready committed 2d967aa.
One critique: Revise, PC-001/PC-002 directly incorporated, no repeat.
P01-T01 active: fail-before tests then typed packet helper.

## Environment and Safeguards

Clean matching topic at intake; origin/main abaca7881e2a4a77eacf865fe235d4af9196643f.
No open PR at intake. gh api user returned authenticated identity; configured
repository-local verified privacy-safe noreply email. No private data read.
Missing core, ruff and mypy confirmed before pip-only restoration:
python3 -m venv SESSION/files/venv; venv/bin/python -m pip install -q -e 'src/core[dev]'.
Venv: /home/azureuser/.copilot/session-state/59e0d542-5cea-4a8b-81b3-f62001748b60/files/venv.
All Python/tool commands below use this venv.

## P01: Implementation Evidence

Fail-before: from src/core, python -m unittest discover -s tests
-p test_sensor_faults.py -q failed with ImportError for absent sensor_faults,
before helper or writer edits. Feature was genuinely missing.

P01-T01: typed sensor_faults helper implements canonical validated exclusive
packet rates, independent seed/sensor RNG, every named corruption, clean copies
and no embedded labels. Ten new test methods initially cover helper and writer.
P01-T02: existing writer/estimate/CLI share packet injector; opt-in output goes
to analysis/ plus evaluator truth/ with complete shard positions and hashes.
Legacy loader refuses new schema/root before DB writes. Legacy code path kept.
New test uses existing migrated untyped-call allowance, not ignore_errors.

## P02: Validation Evidence

Initial sensor suite: 37 passed (1.677s), two existing ResourceWarnings from
test_sensor_backfill unclosed fixture files. Initial Ruff: three new-test long
lines failed; mypy passed 102 source files. Ruff format on new helper/test
corrected them. Re-run: Ruff check and format passed (49 formatted files),
mypy passed (102); historical determinism suite 7 passed (0.112s), including
unchanged exact historical sensor CSV hashes.

Final command/result record (cwd src/core unless stated):

| Command | Actual result |
| --- | --- |
| python -m unittest discover -s tests -p test_sensor_faults.py -q before source changes | Fail-before ImportError for absent feature |
| python -m unittest discover -s tests -p 'test_sensor*.py' -q | 37 passed; final run 1.604s |
| python -m unittest discover -s tests -p test_synthetic_determinism.py -q | 7 passed; final run 0.101s; exact golden CSV hashes retained |
| python -m unittest discover -s tests -q | 546 run, 545 passed, 1 skipped, 195.426s |
| ruff check .; ruff format --check . | Passed; 49 files already formatted |
| mypy | Final pass, 102 source files |
| python SESSION/files/validate_sensor_182.py | Focused baseline 10 passed; all 15 mutants killed by assertion failures, zero mutant test errors; tiny CLI experiment passed |
| git diff --check; git status --short | Passed; intended core/docs/tracking only |

The full suite's one skip is the existing ZF_RESIDENT_AZURE_TEST opt-in:
no live resident/Azure test authorized. Existing full-suite performance tests
construct disposable fictional 60,000-case benchmarks; they do not read,
generate or replace the owner's private 60,000-home file. No live IoT/SQL/AI
or Azure was exercised. Two existing ResourceWarnings remain, unrelated to
the new tests. API/other-component suites were not run: only core tooling
and a synthetic-only opt-in writer/schema changed.

Final typed API annotations exposed mypy's inferred object type for the mixed
invalid-rate test fixtures. Added a precise list[dict[str, float]] annotation;
no casts, broad suppression or production fallback. Re-ran targeted suites and
all three tooling gates successfully after this test-only correction.

### Focused Mutation Evidence

The session-owned script executes changed module source in memory, runs the
same ten focused tests, requires assertion failures and zero test errors, then
restores the original module in finally. Source files never contain mutants.
The named replacements below make the experiment reproducible from committed
source and tests, without a new test runner dependency.

| Mutant | Deliberate change | Assertion failures |
| --- | --- | --- |
| ignored_rates | Force label valid instead of config.choose(rng) | 12 |
| constant_fault_seed | Replace seed/sensor RNG key with constant | 1 |
| missing_outlier | Add 0 instead of 25 C | 1 |
| missing_stuck | Hold each own temperature instead of first | 1 |
| missing_drift | Replace 0.05 factor with 0 | 1 |
| missing_gap | Make gap branch unreachable | 2 |
| missing_duplicate | Make duplicate branch unreachable | 2 |
| missing_reversal | Do not reverse emitted rows | 2 |
| mapped_instead | Retain mapped sensor identity | 1 |
| wrong_unit_not_converted | Keep Celsius value despite degF declaration | 1 |
| missing_clock_skew | Shift by zero days | 1 |
| calibration_not_changed | Keep calibrated=true | 1 |
| truth_leak | Add injected_fault=ANSWER to input schema | 11 |
| lost_gap_truth | Remove nominal clean packet from gap truth | 1 |
| sensor_counter_reset | Reset emitted counter inside each sensor, not each shard | 1 |

PC-001 resolved by canonical config order, 2,000-packet class-sequence oracle
(duplicate=0.2/gap=0.3/valid=0.5, +/-0.04), explicit seed/sensor variation,
equivalent option ordering and sampling/sharding invariance. Constant-seed
mutant fails independently of indoor values.
PC-002 resolved by three granted sensors and two-sensor shards, total emitted
position coverage exactly once for valid/gap/duplicate/reversed packets, exact
CSV-to-clean joins, no gap rows and correct duplicate identities. Counter-reset
mutant fails the integrated reconciliation.

### Tiny Installed-Module CLI Experiment

Temporary fictional CSV: five homes, three granted, one declined, one unknown.
Invoked installed module via subprocess:

```bash
python -m zava_forward.core.synthetic.sensor_backfill \
  --register TEMP/fictional.csv --homes 5 --days 4 --cadence 60 \
  --seed 7 --as-of 2026-10-17 \
  --fault-rate outlier=0.08 --fault-rate stuck=0.08 \
  --fault-rate drift=0.08 --fault-rate gap=0.08 \
  --fault-rate duplicate=0.08 --fault-rate out_of_order=0.08 \
  --fault-rate unmapped=0.08 --fault-rate wrong_unit=0.08 \
  --fault-rate clock_skewed=0.08 --fault-rate uncalibrated=0.08 \
  --out TEMP/a
```

Repeat to TEMP/b: every file byte-identical. --estimate-only agrees with
analysis/estimate.json and 292 actual delivered rows. 144 truth packets:
valid 24, outlier 17, stuck 7, drift 13, gap 7, duplicate 9,
out_of_order 13, unmapped 17, wrong_unit 14, clock_skewed 14,
uncalibrated 9. Every output position accounted once; gaps zero, duplicates
four per packet. Existing nonempty destination returns CLI exit 2 unchanged.
Temporary output removed by TemporaryDirectory; no stock baseline retained.

| Payload | SHA-256 |
| --- | --- |
| analysis/estimate.json | 702e81c84bbd89a5623c336ec410a0b06125b5784aa0e5a86f73a5cc68a3f696 |
| analysis/manifest.json | 0f8fa9f1fdcb9bdf59b79dd69141d157d5722f83f0f7765a3f3217f6cc1eceb5 |
| analysis/readings-0000.csv | 966ed350d02690d438b3047aa7967ad42561091bb272e9f4440fd07a71c1e942 |
| analysis/sensors.csv | 92af309fb2cf9d6e65bcf9322cfd46a47d9e44ec4746cfba92bb5481ffccf8e0 |
| analysis/stock-fabric.csv | dbff4acc00b999bf6590d4c958e9c2fc5770109d646cb4b98aa697a16e2f1929 |
| truth/manifest.json | e042efa37c9deb68a9a3d8a609c01f388ce871759d978fc1a75926bddf101ca9 |
| truth/truth-0000.jsonl | 1dd5581ac03e5191001a1eb0a48af545c597db19bb56513d2edf7f1e57b2d24b |

### Documentation and Reconciliation

Updated core README with exact interface, packet probabilities and even-window
restriction, all exercise magnitudes, paths, row-position contract, no-leakage
limits and legacy-loader refusal. Updated existing synthesis/index and appended
reference log; original/addendum/memory/immutable snapshots untouched.
P01/P02 complete, plan/details aligned; no remaining implementation blocker.
Ready for exactly one post-implementation Review.

## Review and Publication Receipts

One post-implementation Review completed: execution Complete, outcome Residual
work for RV-001 (separate consumer/live acceptance) and RV-002 (separate source/
method/owner approval). No bounded implementation defect identified; no repeat
Review or child delivery loop. Review and phase log committed eda570d.

| Publication command | Actual result |
| --- | --- |
| gh api user; repository-local git identity configuration | Verified privacy-safe noreply author and committer on all commits |
| git commit: research / plan / implementation / Review | 5088a42 / 2d967aa / 7562515 / eda570d; Conventional Commits and requested Copilot trailer |
| pr-reference/scripts/generate.sh --base-branch origin/main --merge-base --output SESSION/files/sensor-182-pr-reference.xml | Passed; 1,994-line XML outside repository |
| git push --set-upstream origin feat/sensor-fault-injection-182 | Passed; remote topic created at eda570d625b2fc0120ffb7e2a43ebe36c793edf8 |
| gh pr create --repo jmservera/ama --base main --head feat/sensor-fault-injection-182 --title 'feat(core): add seeded sensor fault injection and separate truth (Refs #182)' --body-file SESSION/files/sensor-182-pr-body.md | Passed: https://github.com/jmservera/ama/pull/373 |
| gh pr view --json number,url,state,baseRefName,headRefName,headRefOid,statusCheckRollup | #373 OPEN, main base, exact requested topic head; no checks reported at initial observation |

The optional pull-request helper referenced instruction and citation-policy
files unavailable in the checkout/installed plugin. Searched for both and
attempted the declared path; no unavailable host tool or policy was invented.
Used generated native-git PR reference and gh CLI instead. No extra review
fan-out or nested loop was started after the single completed RPI Review.

The PR body contains the exact three-criterion audit, actual validation,
source/prior-art boundaries, artifact paths, restrictions and residual work.
No issue-state edits, completion keyword, merge, rebase, force push or main push.
No remote CI success is inferred from an initially empty check list.

This receipt/state update is a normal final commit, not an amendment. Publish
it to the same topic and verify local HEAD, remote branch and PR head agree,
with a clean worktree. The final head is the commit containing this receipt;
its own hash is intentionally not self-embedded. After verification, stop as
explicitly requested. CI and merge remain owner-controlled; no follow-up starts.

## Amendments, Divergences and Follow-Ups

No material divergence. Packet rates and even >=2 nominal slot restriction are
explicit exercise interface choices. #183/#110 live consumer and #178-#181
source/method evidence remain outside the implementation.
