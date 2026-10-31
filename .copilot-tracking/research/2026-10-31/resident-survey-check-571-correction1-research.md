<!-- markdownlint-disable-file -->
---
title: Resident survey check publication correction research
description: Authorized current-main reconciliation and validation contracts for issue 571
ms.date: 2026-10-31
---

## Research Brief

Task `571-correction1`, slug `resident-survey-check-571-correction1`, parent
`571` / `resident-survey-check-571`. Focused internal convergence research
for the owner-authorized publication correction. Scope: original RV-001,
main merge, existing resident regression, fresh validation and eligible PR.
Non-goals: runtime/grammar/approval changes, Azure, secrets, paid inference,
private data, historical deletion, force push or changing workflow protections.
Research root: `.copilot-tracking/research/2026-10-31/`.

## Research Parameters and Direction Controls

Explicit 2026-10-31 continuation authorizes merging latest origin/main, taking
main rubric score, keeping both log histories, unchanged workflow hashes unless
a workflow is changed, pip-only recovery, API/Ruff/browser validation, 1800s
heavy-lock admission with one retry, commit/trailer and push/PR.
Questions: Q1 does the merge resolve ancestry without losing evidence?
Q2 which fresh checks establish this candidate? Q3 what prevents closure?
Original automatic mode is retained. No interaction is needed or available.

## Extension Registry and Provenance

Repository guidance selected: project framing, privacy-safe git identity,
history preservation, full external receipt and independent Review.
RPI research selected for the bounded correction; specialists skipped because
this is one tightly coupled low-volume trace. Web implementation/design skills
not selected: no UI or runtime source edits, only existing browser validation.
The original README acceptance limitations remain authoritative boundaries.

## Prior Knowledge and Participation

Original Research, changes, evidence and Review were read; original Review is
Complete / Residual work and remains immutable. RV-001 is a publication/base
decision, not a source defect; RV-002 retains human/AT/live limitations.
No new company/regulatory claim. Owner direction settles the merge decision.

## Research Cycle Log

### Cycle 1 Wider

Read issue criteria, branch/PR lifecycle, original state and review. Issue is
open with three criteria; branch has no existing PR and clean tracked input.
Main moved from original `1330869e` to `a75bbdff`. Reflection: owner permission
now resolves the previously missing decision; historical receipt remains failed.

### Cycle 1 Deeper

Parent performed the expressly requested merge first, using privacy-safe
author/committer identity. Merge `e2e815e22432441887597e5ab7e97bcb4282ca0f`
incorporates main `a75bbdffa51ae34b1fcf779250f1f553d566ee93`, with no conflicts.
Diffs against main for score, workflows, runner and knowledge log are empty.
The complete original seven-line regression and five-line guide survive.
Existing task-owned pip environment passes pip check; Python 3.12, browser/axe,
Docker and scanner/lint tools are present. Reflection: no source correction or
WORKFLOW_HASHES update is justified.

### Cycle 1 Contrarian

Read actual runner locking and receipt contracts. An outer flock around the
self-locking runner deadlocks on its separately opened descriptor. Use the
runner's own same-path lock with `--lock-timeout 1800`; run standalone browser
under literal `flock -w 1800 /tmp/ama-rpi-heavy.lock`. Light API/Ruff checks
need no lock by current owner direction. Receipt must follow committed Review
evidence and bind current main, clean candidate, tools/images and full checks.
Passing synthetic evidence does not establish resident/human/AT/live approval.
Reflection: no weaker tier, stale-base substitution, self-lock bypass or closure
inferred from original review is acceptable.

## Evidence Log and Findings Mapped to Questions

| ID | Source | Finding |
| --- | --- | --- |
| C1 | `.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-review.md:146` | RV-001 needs owner base direction; original outcome retained |
| C2 | `.copilot-tracking/changes/2026-10-31/resident-survey-check-571-changes.md:127` | Actual original full gate rejected ancestry before checks |
| C3 | `src/api/checks/resident_assistant_browser_check.py:332` | Recognized positive questions assert Survey facts |
| C4 | `src/api/checks/resident_assistant_browser_check.py:380` | Fresh obsolete replies require refusal/human help/rules and no leaked facts |
| C5 | `tools/rpi-checks.py:2273` | Runner independently opens and owns exclusive heavy lock |
| C6 | `src/README.md:83` | Full committed-candidate gate and external verification required |
| C7 | `src/api/README.md:1199` | Original #573 correction distinct from this negative regression |

Q1 answered by merge ancestry and empty main-input diffs; Q2 by C3-C6 and
fresh API/Ruff/resident browser then committed full gate; Q3 by issue criteria,
original RV-002 and explicit retained boundaries.

## Alternatives and Decision State

Selected owner-directed merge, not rebase or cherry-pick. Rejected outer
self-locking full gate because it cannot acquire itself; native same-lock
1800s wait preserves scheduling and safety without runner modification.
No workflow edit or hash refresh. Preserve original artifacts and create a
distinct child correction with exactly one critique and one Review.
Use `Refs #571` unless independent reviewed evidence proves all three issue
criteria; name any evidence limitation explicitly in the PR.

## Risks, Further Research and Readiness

Main may move during full validation; fetch/verify immediately before push and
reconcile only if it actually does. Missing prerequisites or failed required
checks block publication; preserve adverse attempts and recover only declared
dependencies or narrowly evidenced correction. Human/AT/live acceptance remains
separate, not a new source task. No further research needed: one complete focused
cycle covers all decision-changing questions.

Research disposition: executed. Planning Readiness: Ready.
Artifact self-check: identities, scope, three waves, source pointers, alternatives,
decisions, residual limits and readiness recorded; no external research required.
