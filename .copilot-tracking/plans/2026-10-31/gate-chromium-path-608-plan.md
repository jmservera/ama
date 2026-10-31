<!-- markdownlint-disable-file -->
# RPI Plan: Chromium pathname admission

## Task Metadata

* Task ID: 608
* Task slug: gate-chromium-path-608
* Plan date: 2026-10-31
* Planning status: Ready; one critique executed, Revise directly resolved
* Phase details: .copilot-tracking/details/2026-10-31/gate-chromium-path-608-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/gate-chromium-path-608-plan-critique.md

## Executive Summary

Reject browser-containing gate selections when resolved external output exceeds
58 filesystem-encoded bytes. The owned TMPDIR adds `/tmp`, and Chromium adds
45 bytes for its singleton socket; Linux admits at most 107 bytes plus NUL.
Run this admission before output creation, tool probes, heavy lock or browser
launch, with a Runner constructor backstop. Keep all existing scratch,
cleanup, privacy, source and receipt contracts unchanged.

### What You May Not Know

Ambient TMPDIR is overridden by the gate; changing it cannot help. Browser-free
changed selections retain long outputs. Focused tests do not prove issue
criterion 3; actual full browser/SQL execution is a later CI/full-run gate.

### Unresolved Decisions or Blockers

No implementation blocker. Independent critique and Review are required.

## User Decisions and Requirements

* Full dated Research, Plan, Implement, Review loop for #608.
* Either actionable preflight rejection or legitimately owned short scratch is acceptable.
* Preserve cleanup, output ownership, privacy, receipt identity and source boundaries.
* Do not skip browser/SQL, patch scanner, or provide partial receipt as full evidence.
* Use tools/test_rpi_checks.py, focused unittest and ruff; no heavy-lock full run.
* Use requested branch, commit trailer, non-force push, PR to main, Refs #608.
* WORKFLOW_HASHES changes only accompany workflow changes.

## Goals

* Fail predictable Chromium pathname incompatibility before expensive execution.
* Make the supported Linux bound and recovery action explicit.

## Scope and Non-Goals

* In scope: tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md and dated RPI evidence.
* Non-goals: new scratch location, application/browser/scanner/workflow edits,
  independent allocation lifecycle, receipt schema changes, full local gate.

## Functional Requirements

* Compute prospective socket path from resolved output/tmp and Chromium template.
* Raise GateError for browser-containing selection above 107 socket bytes,
  naming measured lengths, <=58 output / <=62 TMPDIR bounds and short external example.
* Check after trustworthy selection but before tool_identity, output mkdir and lock.
* Resume admission runs inside validate_receipt after integrity/schema/selection/source
  checks and before tool_identity, via an optional new-output argument. Continue
  full parent validation on admitted paths; standalone verification is unchanged.
* Apply the same helper in Runner construction before writing its folders.
* Retain normal CLI outside-source/new-output checks and browser-free long paths.

## Non-Functional Requirements

* Use os.fsencode for filesystem bytes; no character-count approximation.
* Do not create/reuse/delete anything on rejected CLI admission.
* No new permissions, environment, receipt, cleanup or source behavior.
* Simple constants plus shared helper; no new dependency.

## Acceptance Criteria

* Reject 59-byte output and reported ~130-byte output before probes/lock/Runner/verify,
  with no output or receipt; exact 58-byte output admits a real 107-byte Unix socket.
* Reject Unicode output where character length appears valid but byte length is not.
* Resolve symlink aliases before assessing bound and keep source/existing-path rejection.
* Direct Runner rejection occurs before owned scratch creation.
* Browser-free selection retains long output support.
* Existing tools tests and ruff check/format pass; no actual full-run claim.

## Sources

* .copilot-tracking/research/2026-10-31/gate-chromium-path-608-research.md:
  C1-C6 and W1-W3 support formula, ordering and unchanged boundary contracts.

## Test Ownership and Edit Budget

* Canonical tests: tools/test_rpi_checks.py, outside installable packages.
* Exact removals: none.
* Maximum additions: six focused test methods plus necessary imports.
* Canonical source: tools/rpi-checks.py; documentation: src/README.md.
* Generated targets: none.
* Semantic coverage: byte calculation and actual AF_UNIX boundary binding.
* Regression coverage: CLI long paths, symlinks, no writes/probes, Runner,
  browser-free long paths and existing boundary/cleanup/receipt suite.
* Validation: python3 -m unittest tools.test_rpi_checks; ruff check and format
  with existing tooling line length 100.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement bounded admission

* Intent: reject known impossible browser paths without changing scratch.
* Dependencies: finalized plan and one independent critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add selection-aware byte bound

* Expected result: shared helper invoked by CLI and Runner before writes.
* Evidence: research C1-C4, W1-W3.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add tooling regression coverage and documentation

* Dependencies: P01-T01.
* Expected result: exact threshold, early admission, resolved Unicode/symlink
  tests and documented short-output action.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and hand off

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused suite and ruff

* Expected result: durable exact commands, exit codes and evidence; reconcile markers.

## Dependencies

Python and existing ruff; install with pip only after missing-dependency failure.
Independent final-candidate critique and post-implementation Review run once each.

## Critique Disposition

| Run / finding | Disposition | Resolution |
| --- | --- | --- |
| One independent critique: executed, verdict Revise | Preserved original | No second critique |
| PC-001 resume nested probes | Directly resolved in plan | Pass new output to validate_receipt; check recomputed selection after source validation, before tool probes. Test actual fixture receipt path, admitted validation and tamper rejection. |

## Follow-Up Items

* Actual full browser/SQL execution for #608 criterion 3, outside focused scope;
  CI/full-run owner must retain zero-skip full evidence.

## Handoff

* Changes artifact: .copilot-tracking/changes/2026-10-31/gate-chromium-path-608-changes.md
* All P01-P02 tasks complete; independent post-implementation Review next.
* Automatic RPI parent owns continuation; no routine confirmation required.
