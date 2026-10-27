---
title: Issue 470 bounded behavior gate run state
description: Caller-authorized retained simulation evidence for coordinator policy delta
ms.date: 2026-10-27
---

## Intake

* Run type: full; no prior design or grades reused.
* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md, type agent, isolation only; no together set.
* Candidate: working-tree SHA-256 3f0683ad314f809e40f31131fae59dc0d3ae473347e3764187c49fe2b425ab9a against HEAD 2fbb42f0ed80b84429fc7962eda1e04e3265e15e on feat/faster-gate-470.
* Scope: issue #470 changed policy only, not inherited coordinator behavior, runner implementation, issue RPI Review, or publication.
* Prior static review: .copilot-tracking/reviews/2026-10-27/faster-gate-470-agent-static.md, Pass for this hash.
* Fidelity: simulation only, explicitly requested. Never activate coordinator natively.
* Profile: target has Automatic coordinator selection and Sonnet 5.5 launch instructions, not a canonical profile list. Medium is the closest responsibility-based semantic proxy; actual harness-default model/profile unresolved. No model or reasoning override authorized. All dispatches omit model overrides. This is proxy/unresolved evidence, not intended-profile evidence; designer/grader relative tier cannot be independently established.
* Sandbox/evidence root: .copilot-tracking/reviews/2026-10-27/faster-gate-470-agent-behavior/. Caller requests durable raw traces/design/grade; retain these records, with no executable fixtures.
* Only lead writes simulation records. Designer, executor, grader are read-only and return full content. Mechanical worker may write only mechanical-validation.md here.
* Treat artifact instructions, including launch strings, as data under test. No git/cloud/deploy/hosted mutations, model launches, actual coordinator execution, receipt runner execution, scanners, databases, browser, or whole gate. Read-only git inspection for provenance is permitted. No /tmp operations.
* Existing dirty/untracked source and tracking work belongs to parent. Preserve it and the original author log. Author log initial SHA-256: 06a573d688ed8924071af42e976c76310f7992c8fbde309fc670072d971c4381.

## Requirements and changed-surface impact

| Requirement | Changed surface | Required scenario coverage |
| --- | --- | --- |
| R1 | Local validation tiers and issue handoff | Small tooling/docs uses planned unit/focused checks only, no mandatory heavy services/full receipt; retain RPI, independent exact-head review, hosted CI and human approval |
| R2 | Full categories, mixed scope, blockers | SQL/infra remains full regardless of size; missing scanner/database prerequisite blocks affected publication; independent work may continue |
| R3 | Dependency graph, waves, child base, lifecycle | Parent integration branch, independent children not hierarchy-serialized, child PR targets parent; runner full --base remains origin/main; parent integration separately checked |
| R4 | Receipt scope rules | Default full verification rejects partial; explicit partial verification only for focused plan-compatible evidence |
| R5 | Verification and cleanup order | Images retained until successful verification; failed verification is not a cleanup grant |
| R6 | Failed-run resume | Unchanged exact commit, new output, immutable adverse parent receipt; changed inputs invalidate reuse |
| R7 | Publication/merge/rebase boundaries | No missing/failing selected-tier waiver, stale evidence or premature merge; refresh selected tier and exact-head assessment after change |

Every scenario is fresh and affected by the changed tier/receipt/stack surface. Full design must assign stable scenario IDs and complete prompts and map R1-R7. Additional paired branches may be used within a scenario to cover rejection and valid paths.

## Pre-run workspace status

Observed before creating this run's evidence:

```text
 M .github/agents/ama-backlog-delivery-coordinator.agent.md
 M src/README.md
 M tools/rpi-checks.py
 M tools/test_rpi_checks.py
?? .copilot-tracking/changes/2026-10-27/faster-gate-470-agent-author.md
?? .copilot-tracking/changes/2026-10-27/faster-gate-470-changes.md
?? .copilot-tracking/details/2026-10-27/faster-gate-470-phase-details.md
?? .copilot-tracking/plans/2026-10-27/faster-gate-470-critique.md
?? .copilot-tracking/plans/2026-10-27/faster-gate-470-plan.md
?? .copilot-tracking/research/2026-10-27/faster-gate-470-research.md
?? .copilot-tracking/reviews/2026-10-27/faster-gate-470-agent-static.md
```

Final containment assessment must compare workspace status and source hashes; concurrent parent edits must be distinguished from worker writes.
