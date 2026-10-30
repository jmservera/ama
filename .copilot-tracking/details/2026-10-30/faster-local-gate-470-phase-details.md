---
title: Faster local gate 470 phase details
ms.date: 2026-10-30
---

## Metadata

Task ID: 470. Slug: faster-local-gate-470.
Plan: `.copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md`.
Research: `.copilot-tracking/research/2026-10-30/faster-local-gate-470-research.md`.

## Phase Index

| Phase | Direction | Status |
| --- | --- | --- |
| P01 | Reproducible benchmark procedure | Complete |
| P02 | Existing tests and actual measurement attempts | Blocked, attempt evidence recorded |
| P03 | Independent original Review and local commit | Review Complete / Not accepted; local handoff recorded |

<!-- rpi:phase id=P01 -->
## P01: Preserve merged implementation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Document benchmark

Target `src/README.md`, immediately after the receipt-scope description.
Reuse runner flags, never add a new executor. Fresh external outputs, exact
source/base and lock-held timing are required. No test/source removals or
additions; existing regression contracts own semantics. Completion: reviewed
procedure consistent with the self-locking runner.
PC-001: spell out identical timing boundaries, comparable resource/tool
conditions and effective parallel admission above one worker in the procedure.

<!-- rpi:phase id=P02 -->
## P02: Validate and measure

<!-- rpi:task id=P02-T01 -->
### P02-T01: Existing validation

Run `cd tools && python3 -m unittest -q test_rpi_checks`, using external cache
and bytecode paths. Required API discovery from `src/api`:
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
python3 -m unittest discover -s tests -q`, then project Ruff check,
Ruff format --check and mypy. Tooling uses the runner's isolated E,F,I,B,UP,
py312, 100-column Ruff configuration and strict mypy. Heavy test bundles hold
`flock -w 600 /tmp/ama-rpi-heavy.lock`; installation has already been justified
by actual missing packages. Record all exits, inherited skips and failures.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Full benchmark attempt

Depends on P01 and candidate commit. The runner itself acquires the fixed
heavy lock, so use `--lock-timeout 600` directly, never nested flock.
Use `--all --jobs 1` and `--all --jobs 3`, same candidate/base, new `/mnt`
directories. Preserve complete console/receipt evidence. Record full command
elapsed time separately from lock acquisition; only passing full receipts
support successful full timing. Requested three workers may be capped.
Only compare when both full receipts pass verification, serial admits one,
parallel admits more than one, tool/resource conditions match and both use
identical timing boundaries. Otherwise retain individual observations without
a speedup claim. Do not compare against historical partial timing or hide
cache/order bias. A blocked serial attempt may justify not repeating identical failed
prerequisites, but cannot satisfy timing acceptance.

<!-- rpi:phase id=P03 -->
## P03: Review and handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: One original independent Review

Read-only assessment of the changed guide and current artifact/evidence set.
Write only the dated Review artifact. Distinguish execution from acceptance;
no full-time success, PR publication or human approval without evidence.
After Review, route findings rather than implement or re-review this task.
Commit evidence locally with resolved privacy-safe author/committer identity.
Final receipt must refer to the final commit and current main and stay
external. No push/PR/merge.

## Implementation Disposition

P01-T01 complete: procedure added, PC-001 eligibility requirements included.
P02-T01: gate regressions (35) and gate/API lint/format/types passed. Initial
API discovery ran 1370 tests with 76 missing-Node errors and 318 skips; its
sanitized PATH was corrected, but the corrected complete invocation timed out
waiting for the foreign heavy lock. P02-T01 remains unchecked, not successful.
P02-T02: serial full attempt at a5d483c6/base 9ee48592 timed out before admission
or receipt generation; parallel not launched against the common blocker.
Its checked marker records disposition of the attempt, not AC4 completion.
P03 read-only Review may assess this delivered/blocked boundary without
claiming successful full acceptance. Coordinator must arrange later admission.
Review is now executed Complete / Not accepted, with RV-001/RV-002 distinct
evidence follow-ups and RV-003 coordinator publication residual. Original
findings remain unchanged; no later source correction or repeat Review ran.
