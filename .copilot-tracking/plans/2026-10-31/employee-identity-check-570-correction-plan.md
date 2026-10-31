---
title: Employee identity correction plan
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

Task: 570-correction; employee-identity-check-570-correction.
Parent: employee-identity-check-570. Mode: automatic.

## Executive Summary

Correct RV-002 before RV-001 in the existing authenticated-Page adapter.
Prove navigation refusal and actual map render acceptance locally, merge
current main without rewriting history, then require original independent
Review, clean complete gate and exact-head assessment before publication.
Independent Aadi identity is unavailable, so live criterion remains unmet.

## Sources

Correction research C1-C5/W1; original review RV-001 through RV-004;
original changes; src/README.md Local RPI gate; owner request 2026-10-31.

## User Decisions and Requirements

* Continue requested branch; resolve RV-002, then RV-001.
* Merge latest origin/main; keep main's latest rubric and both knowledge log entries.
* Rerun API unit tests, Ruff and tools/test_rpi_checks.py; complete current-base gate.
* Commit with requested Copilot trailer, non-force push and PR to main with RPI artifacts.
* Do not invent independent expected identity or approval; Refs #570 if any criterion unmet.
* Live Aadi sign-in authorized through 2027-01-31, at most two attempts;
  credential files read only inside automation, never printed/logged.
* Pip only, no secrets or Azure changes.

## Goals

Prevent offered-control actions after failed navigation admission and eliminate
map false positives from malformed/error/stale rendering.
Preserve immutable identity authority and original adverse evidence.

## Scope and Non-Goals

Edit runner, owning regression module and API README; dated correction artifacts.
Update knowledge index/log only if material durable documentation warrants it.
Merge upstream tools/infrastructure, but do not modify/deploy them to evade gates.
No sign-in machinery, renderer/UI changes, mapping/roster edits or historical
evidence replacement. Clean external validation worktree avoids touching old
ignored inputs.

## Functional Requirements

Observer callbacks receive an explicit fresh-admission function. Navigations
must call it after transition and before subsequent interaction/observation.
Guard offered controls, including chat sending, with origin and expected-ID
probe. Admission loss leaves current/later stages blocked and no next action.
Keep BINDING unchanged and capture-free fixed boolean/status outputs.
Map acceptance correlates selected-filter response, strict renderer-required
payload and actual matching list/marker/status state; malformed JSON/items,
map alert, page errors and mismatched/stale render refuse acceptance.
Raw data and exception text stay in memory, never output.

## Non-Functional Requirements

Finite existing browser waits; caller owns total watchdog and lifecycle.
No weakening of expected-ID/provider/role/schema admission.
No credential reads/sign-in until independent expectation has provenance.
Preserve reviewer/human/hosted approval boundaries; no force or Azure action.

## Acceptance Criteria

* RV-002 origin-change and session-loss navigation subtests prove zero next actions.
* RV-001 actual Chromium malformed data and renderer-error negatives fail;
  actual valid map points/clusters/empty render succeeds where applicable.
* API discovery, Ruff and gate-tool tests rerun on integrated final source.
* One independent correction Review records execution separately from outcome.
* Candidate/evidence committed; full external receipt verified against fetched
  current main immediately before independent exact-head assessment and push.
* PR names unproven original live criterion and retains original findings.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and integrate

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Gate navigation/action boundaries (RV-002)

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate correlated actual map rendering (RV-001)

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Merge main, update guide and rerun integrated validation

<!-- rpi:phase id=P02 -->
### [ ] P02: Review and publish proven work

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Independent Review and candidate/evidence commit

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Complete clean current-base gate, exact-head assessment, push/PR

## Test Ownership and Locked Boundaries

Owner: src/api/tests/test_employee_acceptance_check.py.
Exact removals: none. Maximum additions: three test methods with focused
negative/positive subtests and fixture composition. Existing tests preserved.
Canonical targets: runner/test/README and correction artifacts; no generated
source targets. Semantic coverage: actual browser observations and action
ordering. Regression coverage: original immutable identity and rosterless
contracts. Required commands: API discovery, runner CLI, Ruff check/format
(explicit isolated formatter for excluded runner), mypy, gate-tool tests and
complete rpi-checks --all with all three Chromium selectors.

## Critique Disposition

One independent critique Complete, verdict Revise; original artifact retained:
.copilot-tracking/reviews/plans/2026-10-31/employee-identity-check-570-correction-plan-critique.md.
PC-001/PC-002/PC-003 applied directly in phase details below; no divergent
decision, no repeated critique. Readiness: Ready after these dispositions.

## Follow-Up Items

Independent private expected tenant/object attestation then eligible live
chat/map/case verification (original RV-004). Not part of local completion.
Hosted checks and owner merge remain separate.

## Handoff

Ready for Implement after one critique and compatible direct dispositions.
Changes path:
.copilot-tracking/changes/2026-10-31/employee-identity-check-570-correction-changes.md.
