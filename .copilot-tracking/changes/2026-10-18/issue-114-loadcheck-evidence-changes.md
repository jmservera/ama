<!-- markdownlint-disable-file -->
# RPI Changes: issue-114-loadcheck-evidence

## Metadata

* Task ID: 114
* Task slug: issue-114-loadcheck-evidence
* Implementation date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-114-loadcheck-evidence-plan.md
* Details: .copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md
* Exact base: f91353169756dc41ebbcca944bdd3f44f7c04b89

## Execution Status

Partial, full-plan scope. P01 and P01-T01/T02 complete.
P02-T01 original Review complete; correction ONE locally complete.
Remaining: P02-T02 publication. Research executed Ready; Plan Ready after exactly one critique.

## Execution Summary

Implemented two-file harness correction and focused offline tests; local validation complete.
Exactly one independent original Review executed, Not accepted; RV-001 locally addressed in
separate correction ONE receipt. No second Review or independent corrected acceptance.
No cloud/data/UI/store-schema/runtime-image changes authorized or needed.

## Completed Work

### Harness correction and initial regression proof

P01-T01: loadcheck.py rejects invalid dimensions and empty cases, represents absent percentiles
as None/nonpassing, uses monotonic shared cutoff, times requests before aggregation wait and
counts sanitized startup/request/session failures. Ordinary Exception is caught only at explicit
request and thread execution boundaries because join does not propagate worker exceptions.
BaseException is not caught; documented startup RuntimeError is distinct. No silent fallback.
Typed public function boundaries use Any for the existing dynamic Store/data contract; no new
Protocol/configuration or mypy exemption.

P01-T02: 16 focused methods passed initially, including actual main() outcomes, real workers,
shared cutoff, injected selection/startup failures and controlled lock wait.

### Research and critique gates

Research C1-C8 verifies false greens. Independent original critique executed, verdict Revise,
SHA-256 6f40180f9bff6315e3a0296310a61ece41092f943c41b1d755dd16d293cd7012.
Original report will not change. PC-001 timing regression criteria and PC-002 scratch isolation
adopted directly in plan/details; PC-002 claimed additional host authority was not verified.

## Implementation-Time Plan and Detail Updates

P01 starts after both direct critique dispositions, no new user decision or second critique.
Source and test ownership remain two files, maximum 16 test methods, no removals.

## Validation Record

Task interpreter: /home/azureuser/.copilot/session-state/619ef4ca-dccb-4a9a-b8db-fb4de739c825/files/loadcheck-venv/bin/python.
Below, `V` denotes that virtualenv directory and `R` the repository root.

| Command/check | Status | Evidence |
| --- | --- | --- |
| python3 --version; python3 -c 'import zava_forward.core.synthetic.loadcheck as m; print(m.__file__)' | Failed | Python 3.12.3; ModuleNotFoundError: zava_forward; subsequent chained tool lookups not run |
| python3 -m venv session-files/loadcheck-venv; V/bin/pip --quiet install -e 'src/core[dev]' | Passed | Actual missing dependency triggered isolated editable installation; no manifest change |
| V/bin/python, constructed Mock-store original probes | Passed as defect reproduction | pct([], .95)=0.0; seconds 0/-1, sessions 0 and expired worker runs all show n=0/within=True/errors=0 |
| cd src/core; V/bin/python -m unittest discover -s tests -p test_loadcheck.py -v; V/bin/ruff check src/zava_forward/core/synthetic/loadcheck.py tests/test_loadcheck.py; V/bin/ruff format --check tests/test_loadcheck.py | Tests/lint passed, format failed | 16 tests OK in 0.165s; formatter requested two line collapses; chained mypy not reached |
| cd src/core; V/bin/ruff format tests/test_loadcheck.py; V/bin/ruff check .; V/bin/ruff format --check .; V/bin/mypy | Format/lint passed, mypy failed | 71 files format clean; 24 new-test errors: strict imported-module exports and untyped empty fixture collection |
| cd src/core/tests; V/bin/python -m unittest test_loadcheck test_sqlreads test_sqlstore test_taskqueues test_sqlqueues test_queue_benchmark -q | Passed | 75 tests, 87.909s, no skips; includes local SQLite/60,000-case structural benchmark, not Azure evidence |
| cd src/core; V/bin/ruff check .; V/bin/ruff format --check . | Lint passed, format failed | After typed test patches, one further line collapse required; chained mypy/tests not reached |
| cd src/core; V/bin/ruff format tests/test_loadcheck.py; V/bin/ruff check .; V/bin/ruff format --check .; V/bin/mypy; V/bin/python -m unittest discover -s tests -p test_loadcheck.py -q | Passed | 71 formatted files; mypy no issues in 124 files; 16 tests OK in 0.077s |
| TMPDIR=$R/.copilot-tracking/.issue-114-tmp V/bin/python session-files/loadcheck_probes.py | Passed | Fixed 16 green; original 16-test run 23 failure/19 error subtest outcomes; 14 mutants detected |
| Same probe with clock-compatible original/fixed goodpath comparison | Passed | Identical reports: list/detail n=5, write n=2, all p50/p95/max=0.125, within=True, errors=0 |
| rmdir .copilot-tracking/.issue-114-tmp; git diff --check | Passed | Exact empty scratch directory removed; no scratch in delivery |
| git ls-remote origin refs/heads/main | Passed | Main still exact base f91353169756dc41ebbcca944bdd3f44f7c04b89 before candidate commit |

Local refinement: patch explicitly imported time/threading objects rather than treating imports
as loadcheck public exports; type invalid CLI fixture collection. No source behavior or scope
change. Formatter fixes are tooling-owned.

### Regression and mutation details

Task-local probe script loads `git show f91353169756dc41ebbcca944bdd3f44f7c04b89:src/core/src/zava_forward/core/synthetic/loadcheck.py`
into a separate in-memory module and points only the isolated test module at it. Checked-out source
is never replaced. Original run's subtest errors include deliberate clock-choice and new invalid
input expectations, not just the original false-green predicate. The separate neutral-clock
comparison verifies preserved good behavior rather than claiming all old-source tests should pass.

All 14 source-string mutants are detected by the existing 16 methods:

| Mutation | Representative detecting test | Failure/error subtest outcomes |
| --- | --- | --- |
| Empty pct returns 0.0 | percentile absence, missing class, CLI | 7/0 |
| Missing p95 passes within | no observations, CLI | 6/0 |
| Allow zero duration (`<=` to `<`) | invalid run/CLI before initialization | 0/3 |
| Allow zero homes (`<=` to `<`) | grow and pre-store CLI | 1/2 |
| Remove session dimension rejection | invalid parameters | 0/2 |
| Remove writer dimension rejection | invalid parameters | 0/5 |
| Remove startup error append | startup retention and CLI | 2/0 |
| Remove session error append | selection retention and CLI | 2/0 |
| Remove request error append | request categories and missing writer | 4/0 |
| Round p95 before acceptance | raw overlimit by 0.00001 | 1/0 |
| Substitute wall clock for monotonic | shared cutoff/real workers/CLI | 18/0 |
| Capture completion after lock acquisition | aggregation wait excluded | 1/0 |
| CLI ignores errors | healthy-class startup/selection failure | 2/0 |
| CLI ignores class results | missing/overlimit run | 2/0 |

Probe rerun repeated fixed-green/original-red/all-mutants-detected with identical source hashes.
This is local engineering evidence, not a performance improvement claim or measured Azure result.

### Validation exclusions

No full repository test suite was needed: focused and existing directly coupled core suites pass.
No new dependency manifest, source layout or import migration, so rename regression not applicable.
Local SQL parity/Docker nonroot checks are not required for this harness-only change; store/schema,
SQL provider and runtime-image contracts are unchanged. Existing SQLite-coupled tests did run.
No Azure load/cost, SQL deployment, backup/restore/deletion, annual ledger, AI or human acceptance
was run or claimed. No idle SQL server started; all fixture storage was task-local and removed.

## Candidate Source Identity

| Canonical file | SHA-256 before original Review |
| --- | --- |
| src/core/src/zava_forward/core/synthetic/loadcheck.py | 7cd7a506e439f0814320cfb7b22e6a3f94b47a18ba255f8eb45dec7e5f581dfb |
| src/core/tests/test_loadcheck.py | b45296f3a9eec3478fb3c68987b85b68a538a22ffad6793c5bfa50ebd01100d2 |

Candidate commit: e63426148b5bac564ffef4195a9ba3b1b873d068, created with authenticated
8036360+jmservera@users.noreply.github.com for author and committer, required Copilot trailer.
This candidate contains source/tests and Research/Plan/details/critique/changes/state artifacts.
Original critique hash remains unchanged. Post-Review source correction cycles used: 1 of 2.

## Original Review and Separate Correction

P02-T01 complete. Original independent Review execution Complete, outcome Not accepted,
RV-001 Medium oversized-duration preflight defect. Original report SHA-256
6510bcd1d1055621b7fb37f73f7ef84426ec5160b65ef1e8bef7bd424017befe is unchanged.
Reviewer independently ran 75 tests, configured checks, original-source replay, four mutations
and goodpath equality; these independent results belong to the original Review, not parent claims.

Caller preauthorized correction of original findings. Separate receipt:
.copilot-tracking/changes/2026-10-18/issue-114-loadcheck-evidence-correction-one.md.
It records exact failing-first reproduction, two-file source/test delta, all commands/failures,
75 final coupled tests, configured Ruff/format/mypy, 16 detected mutants and corrected API/CLI
interfaces before file/store access. All maximum-representable duration subcases pass without
an arbitrary duration policy cap. No second source correction cycle needed or started.

Final corrected SHA-256: source a6bd8d0c4e3ae31484c6248934647b08251af688bf1f3db93a260a9d81fb9858;
tests db30c48bbd9151eee3bb72af4e50dbca8ba8fbaeb2d87a7083fa6c52fdd7affd.
These differ deliberately from the frozen original candidate; no report is retroactively regraded.

Planned validation uses `TMPDIR=$R/.copilot-tracking/.issue-114-tmp`, no inherited service data.
CLI tests clear environment and override tempfile.tempdir; no actual SQL/AI calls.

## Pre-Review Reconciliation

Plan P01 markers, details, completed-work evidence, validation and boundaries reconciled.
Original Review assessed the frozen candidate; P02-T01 now complete. Correction receipt, plan,
details/state and local validation are reconciled for publication. P02-T02 remains unchecked
until actual branch/PR publication is observed. Coordinator exact-head independent acceptance
is pending; original Review Not accepted is not changed to conformant.

## Blockers

None within bounded scope.

## Remaining Work

P02-T02 publication, then stop for coordinator exact-head review.

## Follow-Up Items

Issue #114 real Azure load/latency/cost, annual ledger verification, DH-005 restore/deletion and
human/operational acceptance remain unmet. No issue checkboxes or board changes.

## Return-to-Caller State

Ordered Research -> Plan/one critique -> Implement -> one original independent Review complete.
Parent lifecycle is Follow-up; caller-selected correction ONE is locally complete. Publication
remains active. No second original Review; source acceptance belongs to coordinator at exact head.
