---
title: Issue 1300 prospective RPI phase witness plan
description: Plan for a local observational helper adopted by coordinator step 5
ms.date: 2026-11-10
---

## Objective

Add the smallest repository-owned observational recorder and adopt it in the maintained coordinator step 5 launch and verification procedure. It observes; it does not replace canonical RPI state or gates, and it is not tamperproof or host attestation.

Research: `.copilot-tracking/research/2026-11-10/issue-1300-phase-evidence-1110-research.md` (Ready). Details: `.copilot-tracking/details/2026-11-10/issue-1300-phase-evidence-1110-details.md`.

## Decisions

* Validation tier: focused (helper unit tests, real launch integration, applicable HVE behavior). No full gate, no `rpi-checks`.
* HVE classification: Major (the coordinator step adds a decision rule and stage gate). Profile selected prospectively: Medium, because no High declaration exists on the artifact and no safety-critical authority changes. Fidelity: native where `hve-builder-tester` can run it, else a disclosed Deferred.
* AC3 genuine native exercise is coordinator-run and recorded Deferred here.

## Checklist

* [x] P1 Research recorded, opening state persisted before substantive work
* [x] P2 Plan, details and one critique persisted
* [x] P3 Implement `tools/rpi_phase_witness.py` and `tools/test_rpi_phase_witness.py`
* [x] P4 Adopt in coordinator step 5 (brief generation, launch, verification) only
* [~] P5 Focused tests done; HVE behavior Deferred; AC3 exercise Deferred to coordinator
* [ ] P6 Review once, handoff, commit with privacy-safe identity

## Out of scope

Application, SQL, infra, CI, dependencies, plugin or global files, receipts, KB, `.github/copilot-instructions.md`, #1296 correction policy, D5, approvals.
