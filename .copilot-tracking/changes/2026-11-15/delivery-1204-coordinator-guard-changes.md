<!-- markdownlint-disable-file -->
# RPI Changes: Prevent Unsupported Idle Ticks and Stale Coordinator Handoffs (Issue #1204)

## Metadata

* Task ID: issue-1204
* Related plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: All planned phases and tasks (`P01-T01`, `P02-T01`, `P03-T01`) are implemented, validated with Focused-tier unit tests, Ruff lint/format checks, `test_rpi_phase_witness.py` regression checks, AMA Markdown/ASCII checks, and step 6 HVE static/behavior qualification, and reconciled across tracking artifacts.

## Execution Summary

Updated `.github/agents/ama-backlog-delivery-coordinator.agent.md` across `Liveness and stop decision`, `Recurring schedules`, `Stabilization checkpoints`, `Workflow` step 5 check summaries, and `Final report` so scheduled checks cannot claim `"nothing changed"` or pause on an unverified blocker while open issues remain unclassified in the current run, must render an explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before any idle or waiting summary, and must refresh open-issue counts, open-PR counts, active session status, and pinned SHAs from live commands at write time. Created `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` (`10` `unittest` methods with `subTest` contract coverage), verified clean `unittest` and `ruff` execution, and recorded HVE static/behavior assessment evidence.

## Completed Work

### Coordinator Instruction Guardrails for Classification and Live Handoffs

* Related phase or task: `P01`, `P01-T01`
* Files: .github/agents/ama-backlog-delivery-coordinator.agent.md (`sha256: 6bca3f75f222a34d69f389ab82438a75004512fec82e070b12597f6c1d544f4d`)
* What changed and why: Added explicit anti-idle / unverified-blocker / unclassified open-issue guards, added `### Issue-state classification table and live handoff refresh` defining exhaustive five-category membership (`merged` closed on `main`, `active session`, `human-blocked` with link, `dependency-blocked` with link including hosted-CI PR waits and still-open parent-merged stacked children, and `ready to start`) plus the canonical fenced Markdown snapshot/table schema, reordered step 5 `Cover, in this order:` to lead with live-refreshed metrics/SHAs and the classification table, and aligned `Recurring schedules`, `Stabilization checkpoints`, and `Final report`.
* Completion evidence: `python3 tools/check-coordinator-handoff.py` (`0 violations`), `python3 -m unittest tools/test_rpi_phase_witness.py -q` (`33/33 OK`), zero broken links across repository Markdown, and clean ASCII/AMA Markdown style audit.
* Validation: Run and passed.

### Offline Coordinator Handoff and Instruction Validator

* Related phase or task: `P02`, `P02-T01`
* Files: tools/check-coordinator-handoff.py (`sha256: 103774399dd1f371c32452e83962cbbbe09b0f747f688901f71a0d2f71118e3d`)
* What changed and why: Implemented standard-library Python 3.12 validator and CLI checking `.github/agents/ama-backlog-delivery-coordinator.agent.md` contracts and coordinator handoff/status/checkpoint Markdown documents (fence-aware parsing, per-dated-section scoping, five-category enforcement, non-bare-self link verification on `human-blocked` and `dependency-blocked`, table-before-summary ordering, unclassified open-issue and `ready to start` anti-idle/waiting checks honoring session caps and PR drains, targeted blocker-citation verification, and stale count/SHA/timestamp/carry-forward detection).
* Completion evidence: `python3 tools/check-coordinator-handoff.py` (`0 violations`) and clean `ruff check` + `ruff format --isolated --line-length 100 --check`.
* Validation: Run and passed.

### Focused Unit Tests, Ruff Validation, and HVE Qualification

* Related phase or task: `P03`, `P03-T01`
* Files: tools/test_check_coordinator_handoff.py (`sha256: 55a7fa0a7d5effbedee2ecd83f69bcbf823912842f14f28d815d3ae7133ef721`), .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md
* What changed and why: Authored 10 focused `unittest` methods (`<= 16` lock) using `self.subTest(...)` across positive and negative agent, classification, blocker-link, idle/waiting, fence/negation, stale-handoff, and CLI contracts, refined `CITED_BLOCKER_REF_RE` during test verification so queued `#N` mentions after `before launching` are not misread as blocker targets, verified Ruff lint/format cleanliness, and wrote the step 6 HVE static/behavior assessment artifact.
* Completion evidence: `Ran 10 tests in 0.085s OK`, `ruff check` (`All checks passed!`), `ruff format --isolated --line-length 100 --check` (`2 files already formatted`), and `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`.
* Validation: Run and passed.

## Implementation-Time Plan and Detail Updates

None. Local refinement of `CITED_BLOCKER_REF_RE` and Ruff style cleanup stayed within ordinary local implementation judgment under `P02-T01`/`P03-T01`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 tools/check-coordinator-handoff.py` | `P01`, `P02` | Passed | `Coordinator handoff guard check passed (1 target(s), 0 violations).` |
| `python3 -m unittest tools/test_check_coordinator_handoff.py -q` | `P02`, `P03` | Passed | `Ran 10 tests in 0.085s OK` |
| `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` | `P02`, `P03` | Passed | `All checks passed!` |
| `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` | `P02`, `P03` | Passed | `All checks passed!` |
| `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` | `P02`, `P03` | Passed | `2 files already formatted` |
| `python3 -m unittest tools/test_rpi_phase_witness.py -q` | `P01` regression | Passed | `Ran 33 tests in 3.315s OK` |
| `git --no-pager diff --check` + AMA Markdown ASCII/link/style check | `P01`, `P02`, `P03` | Passed | Exit `0`; 0 non-ASCII characters, 0 bold-prefix bullets, 0 broken Markdown links |
| `python3 tools/rpi-checks.py` | Full gate | Skipped | Explicitly prohibited by caller instructions (`Focused` validation tier) |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` all checked and marked `complete`)
* Completed-work evidence and handoff prose: Current (`sha256` source identities and command outputs recorded)
* Validation, blockers, remaining work, and follow-up items: Current (all focused checks passed; zero blockers; zero remaining active-plan markers)
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-plan.md, `## Follow-Up Items`
* Consider wiring `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR if the owner selects full-gate integration (outside immediate Issue #1204 focused scope; owner: backlog triage).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none
* Validation coverage: Focused unit tests (`10/10`), phase-witness adoption tests (`33/33`), repository + isolated 100-char `ruff check` and `ruff format --check`, `check-coordinator-handoff.py`, `git diff --check`, AMA Markdown ASCII/link audit, and step 6 HVE static/behavior assessment all passed; `tools/rpi-checks.py` skipped per caller instructions.
* Blockers: None
* Current plan and detail updates: None beyond completion marker updates
* Planning and critique state: Ready (`PC-001` through `PC-004` resolved directly)
* Follow-up items: Optional future `tools/rpi-checks.py` static-check integration deferred to backlog triage
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (`confirmed automatic RPI Agent`)
