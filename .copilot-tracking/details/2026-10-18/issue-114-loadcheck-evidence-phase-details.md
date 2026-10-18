<!-- markdownlint-disable-file -->
# RPI Phase Details: issue-114-loadcheck-evidence

## Metadata

* Task ID: 114
* Task slug: issue-114-loadcheck-evidence
* Related plan: .copilot-tracking/plans/2026-10-18/issue-114-loadcheck-evidence-plan.md
* Evidence: .copilot-tracking/research/2026-10-18/issue-114-loadcheck-evidence-research.md C1-C8

## Phase Index

| ID | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Bounded correction and local evidence | Complete | P01-T01, P01-T02 |
| P02 | Original Review and publication | Complete, coordinator acceptance pending | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct and prove bounded evidence contract

Context: empty pct=0.0 and unaccounted thread errors produce false passing evidence.
Boundaries: two canonical files, no runtime store/schema or cloud changes.
Dependencies: Research Ready and one critique dispositions (both satisfied). Unresolved items: none.
Completion: precise source diff plus deterministic evidence recorded in changes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement harness guards and failure accounting

Validate seconds finite and >0, sessions positive integer, writers integer in [1,sessions].
Keep all-writer workloads allowed: existing direct API has no requirement for reader-only sessions.
Validate homes and empty seed before grow and CLI store creation; validate direct run case IDs
before launching workers. Rejecting invalid direct input with ValueError is intentional.
Use explicit static validation messages and argparse.error at CLI; do not serialize arbitrary error text.
RV-001 correction ONE clarifies finite representability: use ordered comparison against
sys.float_info.max, avoiding conversion OverflowError, in both API and pre-file CLI guards.

Missing percentiles are None. Build within from actual nonempty measurements and unrounded p95.
Keep p50/p95/max rounding and report shape otherwise. Do not add sample-count or max-latency gates.
Deadline is monotonic, shared by workers. Capture elapsed request time outside aggregation lock.
Catch request exceptions only at request boundary with type-only kind. Unexpected ordinary session
exceptions at the worker execution boundary must be counted as session failures, never silently
ignored. Do not catch BaseException or hide errors as success-shaped defaults.
Handle documented Thread.start RuntimeError and join only started threads so healthy workers finish.
Preserve existing successful class evidence when another worker fails.

Target: src/core/src/zava_forward/core/synthetic/loadcheck.py.
Completion: guards plus fail-closed report with original valid behavior.
Implementation status: Complete. Focused 16-test run passed before test-only formatting/type
refinement. Canonical source keeps only explicit request/worker exception boundaries and
documented startup RuntimeError accounting; successful classes remain independent.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add focused regressions and run local checks

Target: src/core/tests/test_loadcheck.py, max 16 methods, no test removals or fixture-file additions.
Tests use tiny constructed stores, patched clocks, real workers where concurrency matters.
Control per-thread loop timing, not wall-clock sleeps or external data. Prove missing specific class,
all missing, healthy all-required class, request failure and exact/overlimit raw p95 behavior.
Exercise Thread.start failure and pre-request selection error injection; healthy workers must keep
good observations. Assert sanitized errors omit sentinel private exception text.
Distinguishing timing assertions: make time.time raise if called; script a single shared monotonic
cutoff so late workers contribute nothing and an entered cycle still finishes; use a controlled
aggregation lock that advances a fake perf_counter on acquisition to show that wait is excluded.
Mutate monotonic to wall-clock and move completion measurement inside the lock; both must fail.
CLI tests clear os.environ entirely, create local temporary JSON, mock factory, and invoke main()
to inspect actual emitted JSON and return code. Invalid duration/homes/empty workload must prove
open_store not called. No inherited Azure environment or real store connection.
Run validation with TMPDIR=$PWD/.copilot-tracking/.issue-114-tmp (absolute root from repository).
Within CLI tests patch tempfile.tempdir to the test-owned TemporaryDirectory, independent of
cleared environment; assert ZF_DATA/ZF_STATE are beneath it and removed after main().
Remove the exact scratch directory after all checks, never commit scratch. PC-002's claimed
additional host prohibition is unverified; isolation is adopted on its merits, not that authority.
Add proper canonical function annotations so new tests need no mypy exemption.

Task-local virtualenv exists after actual missing-distribution failure; installed editable core[dev]
with pip. Use its Python/Ruff/mypy. Run focused tests, coupled core suites including queue benchmark,
configured Ruff lint/format and mypy. Record exact commands, failures, skips and reasons in changes.
Run old-base module isolated against new tests (expected red) and targeted runtime mutations
(expected detected), without rewriting checked-out source. Mutation tests are local evidence,
not a new committed test harness. No SQL Docker/nonroot check needed absent contract changes.
Implementation status: Complete. Final 16 focused tests pass, coupled 75-test run passes,
core Ruff lint/format and mypy (124 files) pass. Old source red; 14 targeted mutants detected.
Separate clock-compatible original/fixed goodpath reports match exactly. Scratch removed.
Correction ONE adds oversized positive/negative duration and maximum-representable accepted
subcases within the same 16 methods. Exact final source passes 75 coupled tests and configured
checks; original red/healthy equality and all 16 updated mutants are recorded separately.

<!-- rpi:phase id=P02 -->
## P02: One original independent Review and publication

Boundary: preserve immutable original critique/Review. Review execution and outcome are distinct.
Candidate/source identity must remain reconstructible after artifact-only publication commits.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Preserve original independent Review

Depends on P01. Commit reconciled source, tests and existing task artifacts with safe resolved
identity before independent Review, recording candidate SHA and source hashes in changes/state.
Fresh worker performs one original Review using rpi-review; no source edits, nested review or
second original Review. It writes only .copilot-tracking/reviews/logs/2026-10-18/issue-114-loadcheck-evidence-review.md.
If adverse, keep original unchanged and create separate correction receipt with before/after hashes,
exact finding dispositions and validation. At most two source cycles, no implicit acceptance.
Status: Complete. Original Review executed once on e63426148b5bac564ffef4195a9ba3b1b873d068,
Not accepted with RV-001 Medium. Original bytes unchanged. Caller-selected correction ONE is
locally complete with separate receipt; this is not an independent corrected-head acceptance.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile, commit and publish

Keep publication artifacts descriptive, not retroactive original acceptance. Include exact base,
candidate and source hashes. Resolve gh api user before commits; repository-local noreply email
for both author and committer; required Copilot trailer. Verify git diff --check and tracked artifacts.
Check remote main movement, never integrate it without coordinator authorization.
Commit original Review and remaining task artifacts, push branch and create main PR with Refs #114.
PR records exact delivered head externally (self-hash cannot be in its own commit), ordered RPI paths,
commands/results and unmet live/human gates. Verify PR head/base and branch cleanliness.
Stop automatic session after publication per explicit caller instruction, not follow-up selection.
Status: Complete. Branch pushed, PR #403 OPEN targeting main; initial observed head d55e96c6,
unchanged base f9135316. Separate publication receipt records full identities and final artifact-only
head pinning via PR body. No source integration, second Review or independent corrected acceptance.
