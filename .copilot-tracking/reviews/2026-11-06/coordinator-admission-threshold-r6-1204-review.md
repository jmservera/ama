---
title: Author review, admission threshold correction r6 (issue 1204)
ms.date: 2026-11-06
---

* Task: coordinator-admission-threshold-r6-1204. Review execution: Complete. Outcome: Residual work. Author Review only; not the coordinator's independent exact-head assessment and not human approval.
* Boundary: intake 7ae41593647acc907cfeeaf78450f879e3836c7e; planning d1aa4a060d27d15011585acfc64eba1090fc3627; target commits 4d1cff62 and 72cfd55e0662f819b98ab7e075e68897611c9711 (final blob d471fc61041f9fc73a43564f7bf390a7c7d10cf5); evidence 22c98f830b64a62f1bbe304931f2ed4e99e80b9e.
* Compared: .copilot-tracking/research/2026-11-06/coordinator-admission-threshold-r6-1204-research.md, .copilot-tracking/plans/2026-11-06/coordinator-admission-threshold-r6-1204-plan.md, .copilot-tracking/details/2026-11-06/coordinator-admission-threshold-r6-1204-details.md, .copilot-tracking/plans/2026-11-06/coordinator-admission-threshold-r6-1204-critique.md, .copilot-tracking/changes/2026-11-06/coordinator-admission-threshold-r6-1204-changes.md, .copilot-tracking/hve-builder/2026-11-06/coordinator-behavior-abd6-1204-behavior-report-011.md, .copilot-tracking/sandbox/2026-11-06-coordinator-behavior-010/test-review.md, .copilot-tracking/rpi-sessions/2026-11-06/coordinator-admission-threshold-r6-1204-state.json.
* Preserved: independent partial review (request_changes, 1 High, partial coverage, issue comment 6692489250), reports 009 Revise and 010 simulation Pass (bound to blob acefb44a), all raw traces.

## Evidence classes

| Class | Content |
|---|---|
| Implemented policy | Admission bullet at blob d471fc61: no unconditional 16 to 20 ban; more than 20 enters a recorded drain; drain clears at a confirmed 15 or fewer; gates never relaxed. |
| Static findings | Independent review of intermediate blob aa175c95: Revise (1 Medium, 2 Low), all applied. Final blob not statically re-reviewed. |
| Simulated behavior | Report 011: Pass at simulation grade, 8 scenarios, 0 target defects, 5 Low, 2 Info. |
| Observed native actions | None in this task except the focused gate recorded in the handoff. Native Automatic fidelity Deferred. |
| Unknowns | Live prompt deployment; hosted checks; human approval; behaviour of the 11 prior families against the new blob (not re-run). |

## Findings

| ID | Severity | Finding | Destination |
|---|---|---|---|
| RV-001 | Low | Final blob was not independently re-reviewed after F1 to F3; the grader read it and found no defect. | Coordinator exact-head assessment |
| RV-002 | Low | Prior 11 scenario families not re-run against the new blob; only admission wording changed. | Coordinator assessment, optional later research |
| RV-003 | Low | N-08 wording "admit none and re-read this tick" is ambiguous in the drain-unknown case. | Later implement item, if the coordinator wants it |
| RV-004 | Low | Grader coverage misses (rebuild path, drain write failure, failed merge gate during drain, slot contention). | Later research |
| RV-005 | Info | `pr_drain` key is a scenario convention, not a schema. | None |

## Acceptance mapping

The correction touches only the admission threshold (issue scope: more than 20 triggers draining to 10 to 15). Other criteria are unchanged from the r5 Review and stay unmet pending independent assessment. No box is ticked and the issue is not delivered.

## Remaining gates

Coordinator independent exact-head assessment, hosted CI, human review and closure. PR target main with Refs #1204; publication and merge coordinator-only.
