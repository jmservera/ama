---
title: Faster local gate 470 changes
ms.date: 2026-10-30
---

## Metadata

Task ID: 470. Slug: faster-local-gate-470. Declared scope: full plan.
Plan: `.copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md`.
Details: `.copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md`.

## Execution Status

Partial, benchmark blocked. P01-T01 documents the existing runner benchmark.
Write boundary: `src/README.md` and this task's dated tracking evidence only.
No application, runner or test changes. P01/P01-T01 completed; P02-T01 blocked
on corrected API execution, P02-T02 attempt disposed as blocked; P03 completed.

## Execution Summary

Research verified that #475 already implements the requested functionality.
This continuation targets the remaining full timing evidence. Critique PC-001
requires explicit comparability, actual parallel admission and equal timing
boundaries; the planning parent applied it without a second critique.

## Validation Record

External evidence root: `/mnt/ama-rpi-gates/issue470-20261030-validation`.
Actual missing Ruff, mypy and distributions justified creating an external
venv and pip-installing existing core/agents/API dev dependencies. Installation
passed; pinned Ruff 0.17.1 and mypy 2.4.0 are available. Generated local build
outputs will be removed only at their exact task-created paths.

| Check | Result | Evidence |
| --- | --- | --- |
| Gate regressions | Passed, 35 tests in 11.897 s | External `gate-tests.log` |
| Gate Ruff lint/format | Passed, two files already formatted | Ruff 0.17.1, isolated existing runner configuration |
| Gate strict mypy | Passed, two files | mypy 2.4.0 |
| Diff whitespace | Passed | `git diff --check` |
| Required API discovery | Failed: 1370 tests, 76 errors, 318 skips, 345.040 s | External `api.log`; sanitized PATH accidentally excluded installed Node |
| API Ruff lint/format/mypy | Passed | `api.log`: lint=0, format=0, types=0; 60 formatted files and 116 typed files |
| Corrected API bundle | Blocked: flock exited 1 after bounded wait, no tests executed | External `api-with-node.log` remains empty |
| Full serial gate | Blocked: exit 1, Global heavy-resource lock timeout | External `serial-a5d483c6.log`; no receipt, no admitted jobs, no execution interval |

Task-created build directories, egg-info and Ruff cache were moved to exact
external `generated/core`, `generated/agents`, `generated/api` and
`generated/ruff-cache` archives, not deleted or committed.
Pre-admission resource observation caps requested jobs 3 at 1; actual full
admission must still be recorded. This observation is not a parallel benchmark.

## Completed Work

P01-T01: `src/README.md` now documents serial/parallel full commands, internal
lock ownership, requested versus admitted jobs, identical acquired-to-sealed
timing, independent default-full verification, cache/order qualifications and
coordinator-owned PR recording. Existing partial/full rules remain unchanged.

## Implementation-Time Plan and Detail Updates

PC-001 was applied directly before implementation. No divergence, new
requirement, new test ownership or repeated critique was introduced.

### Validation environment correction

The initial sanitized API PATH kept only standard system directories, while
installed Node is `/home/azureuser/.nvm/versions/node/v24.21.0/bin/node`.
The 76 errors are missing-node errors, not attributed to the documentation
delta. Corrected invocation retained the actual PATH behind the external
venv, still with empty inherited environment, synthetic data and external HOME.
That rerun could not acquire the heavy lock within 600 seconds. Preserve both
attempts; no API-success claim is made. This is a local validation-command
correction, not a source change or planning divergence.

### Same-candidate full benchmark admission

Candidate: `a5d483c65b70d249fb93d72f3f7a445eb1b0b934`.
Base: `9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19`.
Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --jobs 1 \
  --lock-timeout 600 --base 9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19 \
  --out /mnt/ama-rpi-gates/issue470-20261030-serial-a5d483c6
```

The runner itself held the admission contract, so no outer flock was nested.
It exited 1 with `BLOCKED: Global heavy-resource lock timeout` before acquiring
the lock or creating a receipt. Requested scope full, jobs 1; actual groups,
admitted jobs, acquired-to-sealed elapsed and receipt identity unavailable.
Parallel attempt was not launched after that common prerequisite failure:
another queued run would repeat the foreign-lock blocker rather than measure
parallelism. Thus no full before/after timing or speedup is claimed.
`resources.json` records four affinity CPUs, then available memory 9,335,900 kB
and effective cgroups; an earlier observation capped jobs 3 to 1. These are
pre-admission observations only, not a full execution/resource comparison.

### Acceptance evidence

| Criterion | Evidence | Current disposition |
| --- | --- | --- |
| AC1 changed-path selection and scope | Existing mapping/closure, unusual-path and receipt tests in 35 passing gate tests | Proven by focused regressions; already merged in #475 |
| AC2 reject partial when full required | `test_partial_scope_is_rejected_by_default_before_live_probes` | Proven by focused regression |
| AC3 bounded independent parallel scheduling | Existing overlap, thread-local logs, shared-environment ordering, nested-cgroup and capacity tests | Proven at regression level; no new successful full parallel run |
| AC4 full before/after measured in PR | Serial admission timeout; parallel not launched; no PR authorized | Not proven |
| AC5 group-selection and scope tests | 35 gate tests pass | Proven |

## Pre-Review Reconciliation

P01 complete; P02-T01 retains an unchecked marker for the blocked corrected API
suite; P02-T02 records its completed attempt disposition, not benchmark success.
Details and this record preserve failed and unperformed checks. Ready for the
one independent Review of the delivered documentation and blocked evidence;
not ready for successful issue acceptance or publication.

## Blockers

Foreign shared-lock ownership blocked full serial admission and the corrected
API suite within their authorized 600-second waits. No foreign resource was
interrupted, inspected for results or reused. Resume requires coordinator
admission after ownership is actually free; unavailable full timing stays open.

## Remaining Work

P02-T01 corrected API run. P03-T01 Review/handoff is complete. A controlled full
benchmark is still unmet despite disposition of P02-T02's attempted execution.
Final exact-head full receipt is absent and publication remains blocked.

## Follow-Up Items

Coordinator-owned PR recording and final exact-head publication gates remain
outside the locally committed handoff.

## Original Independent Review and Local Handoff

P03-T01: Review executed Complete, outcome Not accepted. RV-001 High routes the
full timing evidence gap to distinct later research/evidence work; RV-002
Medium routes corrected API execution separately; RV-003 Low retains the
coordinator-owned publication handoff. No source defect was found. Original
Review and critique outcomes are preserved; no second Review or source fixes.
P02 remains incomplete. Human approval remains unchecked in the Review.

The authenticated account was resolved with `gh api user`; author and
committer use its repository-local privacy-safe noreply address. Local commits
include `Refs #470` and the required Copilot coauthor trailer. No push, PR,
issue update, Azure operation, live sign-in or credential-file read occurred.

External log SHA-256 identities:

| Log | SHA-256 |
| --- | --- |
| gate-tests.log | 19ded687a5a695a92287bb370fb4b9be200196fce12fbb160035f25ca6d53f88 |
| api.log | f97bec0d09a214ecc42985a9468b643a2b76d20f89c155df924f1a95f49909fd |
| api-with-node.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| serial-a5d483c6.log | a61e364435be7c6fffd44ae8f8a2a7359d918b0b5754b4b3f1bb6bf7f802039b |

After committing this handoff, the required final exact-head full gate will
be attempted with the existing self-locking runner, fresh external output
`/mnt/ama-rpi-gates/issue470-20261030-final` and external `final-gate.log`.
Its generated `final-result.json` in the validation root owns the later exit
and HEAD/base facts. No resulting output is a committed final receipt or a
relabelled original Review. Coordinator must inspect actual results and still
satisfy current-main/exact-head verification, independent, human and hosted
approval requirements before any separately authorized publication.

The mandatory final refresh observed `origin/main` move from the supplied
reviewed base 9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19 to
a31048f15fa3120c58bacd22a375d86ae5ab7431. The final gate must therefore refuse
the old reviewed base before heavy execution. Reconciliation/rebase is not
silently authorized by a moving remote: preserve the owner's supplied branch
and base, report the blocker and leave coordinator reconciliation plus a fresh
gate to later work. No stale-base receipt may be promoted as publication proof.
