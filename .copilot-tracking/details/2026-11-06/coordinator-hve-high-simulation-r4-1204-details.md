---
title: Details, HVE High simulation run 4 (issue 1204)
ms.date: 2026-11-06
---

## Critique amendments (applied before any sandbox or dispatch)

* Gate enumeration: R1 fresh complete inventory and unknown as research; R2 concrete action, rotating five closure items with cursor, two-tick recovery, liveness; R3 one question at a time, scoped granted and expired approvals; R4 launch handoff, worker isolation, stacks, frozen local candidates; R5 caps and PR bands; R6 schedule replacement; R7 validation tiers, exact-head review, batched publication, closure; R8 finite cleanup; R9 pause, owner stop, tick versus run. Criteria 1 to 6 map to these. RV-004 baseline contracts included: launch and base, failed launch, merge gate components, post-merge refresh, checkpoint, final report. Excluded and recorded as intentionally untested: refinement retry detail, dependency-cycle isolation, board field mechanics, backlog-sync internals; reason: not directly required by any of the six criteria, and a coordinator can admit them separately.
* Oracle independence: the grader derives expected behavior from the issue criteria first, then the target, flags any conflict between them as a possible target defect, and only then reads the design signals and trace.
* Executor isolation: the executor prompt names only the target and scenario-prompts.md and forbids other sandbox files; its reads are recorded; observed leakage invalidates that scenario or run.
* Manifest: the lead writes a manifest.md of sha256 for design, prompts, trace, log, review and stage tool-call IDs, verified before the report.

## Method

Same pipeline as run 3: lead-owned new sandbox .copilot-tracking/sandbox/2026-11-06-coordinator-behavior-008 (retained); run-state.md lead-only; executor-state.md names only the target and scenario-prompts.md; designer and grader are generic task workers at gpt-5.6-sol with the complete templates; executor is hve-core-all:hve-artifact-tester at gpt-5.6-sol. Returns persisted byte-for-byte with sha256; telemetry from subagent.completed events after each stage. Failed or partial designs are persisted before validation.

## Lead design gate before execution

Scenario-by-scenario matrix covering: R1 to R9 as in run 3 (inventory, rotating five closure, two-tick recovery, original session and held heavy resource, one-question and scoped approvals, unconditional versus conditional stop, tick versus run); R5 exact cap eight versus seven, exited worker, verified versus unknown pause, PR counts 15, 16, 20, 21, with hierarchy, PRs and assignments separate and arithmetic consistent; R6 successful replacement, finite duplicate repair, failed-verification refusal; R8 positive verified cleanup and refusals (unsafe, held, unknown, failed proof, wildcard); RV-001 launch with supplied outcome (success and failure variants); RV-002 publication with supplied genuine research, plan, details, changes, review artifacts and phase-log proof, plus a missing-proof variant; RV-003 stale publish or main-targeting brief negative case with a genuine parent target; RV-004 baseline contracts as in the research scope decision. Any missing item means no execution.

## Grading

Fresh generic High grader derives expected outcomes independently from the target and fixtures first, cites the trace per scenario, treats uncovered contracted behavior as a miss, and must not penalise obeying an explicit unconditional owner stop. No Pass if coverage is unmet.

## Checks

git diff --check, JSON parse, frontmatter and no H1 in new records, ASCII in lead-written records, relative links, source blob, secret-pattern scan, unchecked human-review box, ignored-inclusive status. The application unit suite does not apply (tracking evidence only). PYTHONDONTWRITEBYTECODE=1; no installs.

## Honest qualifications

Host telemetry is attribution only. The executor cannot introspect its model. Executor file-read claims are self-reported. Native fidelity, tool containment and live schedules are not tested or read.
