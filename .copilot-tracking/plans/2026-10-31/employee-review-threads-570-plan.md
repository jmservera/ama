---
title: Employee acceptance review-thread plan
description: Bounded correction plan for the two PR 601 review threads
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: 570-review-threads
* Task slug: employee-review-threads-570
* Status: implementation/validation and independent Review complete; publication pending
* Details: .copilot-tracking/details/2026-10-31/employee-review-threads-570-phase-details.md

## Executive Summary

Repair valid-cluster false rejection with 1e-9 degree absolute containment
slack only for clusters. Keep geographic limits and point containment exact.
Enforce three real hosted Chromium executions through the maintained CLI
after installation, retaining discovery qualification and updating the
workflow pin together. No producer/application behavior changes.

The current caller requires focused checks then publication without waiting
for the full local gate; CI remains pending until hosted execution. Earlier
live identity and full-gate records are not rewritten or relabelled.

## User Decisions and Requirements

* Continue #570 in fix/employee-identity-check-570 and existing open PR #601.
* Merge origin/main first, retaining main's rubric score if conflicted.
* Fix floating-point cluster containment with a producer-derived regression.
* Retain strict point/geographic checks and missing-browser discovery qualification.
* Invoke the acceptance CLI after hosted Chromium install with documented env.
* Update WORKFLOW_HASHES in the same commit as src-ci.yml.
* Validate relevant API tests, Ruff, mypy and the requested gate-tool tests.
* Run exactly one critique and one independent Review; preserve dated artifacts.
* Pip only, no secrets; CI is the gate, no full local gate wait.
* Commit with required Copilot trailer, push non-force (pull --no-rebase on rejection), reply to and resolve both threads.

## Goals

* Accept correct producer clusters without accepting malformed map evidence.
* Prevent hosted success when any maintained browser regression is skipped.

## Scope and Non-Goals

In scope: adapter, its existing test module, browser workflow, gate hash pin,
API acceptance guide, directly related knowledge index/log and dated RPI
artifacts. No removals or generated code.
Out of scope: core producer changes, visual/UI changes, live sign-in, credentials,
Azure changes, old artifact correction, full gate, issue closure and PR merge.

## Functional Requirements

* Apply bounded absolute slack to all four cluster containment edges only.
* Reject point overshoot, out-of-range/nonfinite coordinates and malformed bounds.
* Hosted browser step executes `python -m checks.employee_acceptance_check`.
* Keep CLI exactly-three/zero-skips exit contract and discovery skip unchanged.

## Non-Functional Requirements

* No dependency changes, capture, private fixtures or live calls.
* Geographic limits remain exact; tolerance is 1e-9 degrees, not relative.
* Update workflow digest using SHA-256 of exact bytes in the same commit.

## Acceptance Criteria

* 501 colocated fictional homes passed through real `core.insights.map_view`
  use default cap 500, reproduce centroid overshoot and are accepted.
* All cluster edges allow roundoff within slack and reject beyond slack;
  points still reject tiny overshoot.
* Both modes reject boolean/nonfinite/out-of-range coordinates and malformed
  geographic bounds without relaxing count/schema checks.
* After browser setup the documented CLI runs exactly three tests, no skips.
* Requested API tests, lint/format/type checks and tool tests pass.
* Independent Review records actual scope/outcome; branch is committed and pushed.

## Sources

* .copilot-tracking/research/2026-10-31/employee-review-threads-570-research.md:
  C1-C7/W1-W2, executed and Ready.
* src/api/README.md: existing invocation and non-live boundaries.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct acceptance contracts

Dependencies: research complete; critique dispositions ready.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Cluster-only tolerance and producer/negative regressions

Add at most two test methods in the existing acceptance test module: one
real producer regression, one table-driven containment/range test. Extend
existing malformed cases as needed; remove zero tests. The acceptance module
owns semantic and regression coverage; core remains unchanged. No new harness.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce hosted browser CLI and update workflow pin

Add the documented test-import environment and CLI directly after Chromium
installation. Keep discovery before install. SHA-256 pin is canonical in
tools/rpi-checks.py; no other workflow hashes change. Update API guide.

<!-- rpi:phase id=P02 -->
### [x] P02: Verify and review

Dependencies: P01 complete.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Focused and component validation

Use installed task-owned venv, public fixtures only. Run acceptance and identity
tests, full API discovery, configured API Ruff/format/mypy, isolated changed-adapter checks (retaining
the pre-existing embedded-JavaScript E501 exemption) and
`python3 -m unittest discover -s tools -p 'test_rpi_checks.py' -q`.
Execute maintained Chromium CLI separately; record actual skips without
claiming live acceptance. Check workflow structure and digest. No full local gate.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: One independent Review and evidence reconciliation

Review worker writes only the dated Review artifact. Assess exact source diff
and findings against both threads; original outcomes stay intact. Later work
owns any routed finding, not a repeated Review of this task.

<!-- rpi:phase id=P03 -->
### [ ] P03: Publish and resolve threads

Dependencies: P02 complete and no material publication defect.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Commit, non-force push, thread replies/resolution

Commit implementation, same-commit workflow/hash pin and original RPI evidence
with authenticated privacy-safe author/committer and requested trailer.
`git push -u origin HEAD`; on rejection `git pull --no-rebase` before retry,
preserving main rubric on conflict. Reply to both exact thread IDs with actual
evidence/commit, resolve only addressed findings. Existing PR; no new PR/merge.

## Dependencies

Task-owned venv has missing distributions installed with pip. Chromium must
actually launch for integration acceptance. GitHub access and branch lifecycle
were inspected. No independent live identity is needed for synthetic checks.

## Critique Disposition

One final-candidate critique Complete / Pass, zero findings, at
.copilot-tracking/reviews/plans/2026-10-31/employee-review-threads-570-plan-critique.md.
Disposition: accepted; no changes or user decisions required.

## Follow-Up Items

* Original #570 live employee acceptance still needs independently attested
  identity. Not part of the two selected review-thread repairs.
* Hosted CI and owner merge approval remain separate from local checks.

## Handoff

Changes record: .copilot-tracking/changes/2026-10-31/employee-review-threads-570-changes.md.
Parent continues to authorized P03 publication. No ordinary unresolved choice.
P01 and P02-T01 complete: 18 focused tests, three CLI browser executions,
1441 API discovery tests (320 skipped), 39 gate-tool tests, configured static
checks and workflow structure/pin verification. P03-T01
publication remains unchecked pending execution. One independent Review
Complete / Conformant, zero findings, at
.copilot-tracking/reviews/logs/2026-10-31/employee-review-threads-570-review.md.
