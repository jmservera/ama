<!-- markdownlint-disable-file -->
---
title: Resident survey check publication correction plan
description: Fresh validation and gated publication following authorized main merge
ms.date: 2026-10-31
---

## Metadata

Task `571-correction1`, slug `resident-survey-check-571-correction1`; parent
`571` / `resident-survey-check-571`. Automatic continuation, branch
`fix/resident-survey-check-571`, merged main `a75bbdff` at `e2e815e2`.

## Executive Summary

Owner permission settles original RV-001. Main merged without conflicts, with
unchanged main score/workflows/hashes/log and retained seven-line regression.
No runtime/UI/grammar edit or acceptance relaxation is needed. Re-execute the
requested API/Ruff/resident browser checks, independently Review this correction,
commit original dated correction evidence, then execute/verify the full external
exact-head gate and publish a non-forced main PR. Original Review stays immutable.
P01 complete: fresh API 1430 tests (320 explicit skips), Ruff check/format and
complete resident Chromium/axe passed. One correction Review Complete / Residual
work approved the bounded source/merge/evidence with no material defect; Low
acceptance limits remain. Current readiness: eligible for committed full gate after
one critique (Complete / Revise) and direct PC-001
disposition. Publication requires no unresolved material Review defect and an
approving independent exact-head assessment; passing tests cannot waive either.

## User Decisions and Requirements

* Merge latest origin/main; take main score, keep both log histories, update
  runner workflow hashes only if a workflow is changed.
* Run complete correction RPI and required API/Ruff/local Playwright checks.
* Heavy checks wait 1800s for the shared lock, retry admission once; light checks
  need no lock. Full runner uses its native same-path 1800s lock to avoid nesting.
* Pip only, no secrets, private data, Azure, force push or main publication.
* Commit with requested Copilot trailer; `git push -u origin HEAD`; PR to main
  includes original and correction artifacts. Conditional Closes only on reviewed
  evidence proving all three actual issue criteria; otherwise Refs with unmet list.

## Sources

Correction Research C1-C7, original changes/Review, fetched issue 571 criteria,
src/README.md local gate, merged source and main-input diffs.

## Goals

G1 resolve publication ancestry with authorized history-preserving merge.
G2 prove retained positive and fresh refusal regression on current candidate.
G3 publish honest evidence without weakening resident acceptance.

## Scope and Non-Goals

Only current correction artifacts and necessary publication evidence. The merge
is already complete. No source, tests, workflows, tooling pins or runtime changes
planned. Original artifacts immutable. No cloud/live/human approval or issue
checkbox mutation; no historical deletion or receipt committed as current.

## Functional Requirements

FR1 preserve main score/log/workflow inputs and original regression/guide.
FR2 exact fresh API discovery, API Ruff check/format, complete local resident
Chromium/axe path using existing constructed fixtures and pinned asset.
FR3 complete full local gate from clean committed current-main-descended HEAD,
fresh verification, independent exact-head assessment and main PR.

## Non-Functional Requirements

NFR1 isolated existing task-owned pip environment; no shared editable mutation.
NFR2 same global heavy lock, finite admission/retry, no nested self-lock.
NFR3 preserve failures/skips/axe incompletes and direct acceptance limits.
NFR4 privacy-safe authenticated author/committer and required trailer.

## Acceptance Criteria

AC1 ancestry and unchanged protected main inputs independently evidenced.
AC2 all specifically requested validation executed; no failed required result
relabeled pass. API skips and axe incompletes remain explicit.
AC3 one critique and one correction Review, with direct dispositions and
original outcomes preserved.
AC4 committed evidence plus verified full current-head receipt and independent
exact-head assessment precede non-force push and evidence-linked main PR.
Unresolved material Review findings or non-approving exact-head assessment block
publication; human/live limitations outside this bounded scope remain explicit.
AC5 PR wording separates three #571 criteria from broader unexecuted resident
acceptance; Refs names any criterion not proven by reviewed evidence.

## Coverage Lock

Test owner: existing src/api tests/checks. Removals none; maximum additions zero;
no source assertion changes. Canonical targets existing API discovery, Ruff,
resident assistant browser check; generated reports/logs stay external.
Regression evidence is not semantic/human/live/WCAG approval.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Validate merged correction

* [x] P01-T01 verify merge invariants and execute requested checks
* [x] P01-T02 reconcile fresh evidence, plan/details/changes and limitations

<!-- rpi:phase id=P02 -->
### P02: Review and publish

* [x] P02-T01 single independent correction Review (depends on P01-T02)
* [ ] P02-T02 commit evidence, full gate/verify/exact-head assessment, push/PR
  (depends on P02-T01)

## Critique Disposition

Exactly one independent critique executed: Complete / Revise, one Medium PC-001.
Planner applied PC-001 directly: AC4 and P02-T02 now explicitly prohibit publication
with unresolved material Review findings or a non-approving exact-head assessment.
Resolution evidence: these gates and matching phase details. No user decision or
second critique; owner-settled merge direction unchanged.

## Follow-Up Items

Original RV-002 human/AT/live acceptance remains open outside this correction.
Hosted checks/owner merge remain separate after PR publication.

## Handoff

Details: `.copilot-tracking/details/2026-10-31/resident-survey-check-571-correction1-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-31/resident-survey-check-571-correction1-changes.md`.
Parent continues automatically after critique dispositions.

## Review Disposition and Publication State

Correction Review executed once, Complete / Residual work. Low RV-001 retained as
the existing direct-acceptance follow-up, no material defect or decision blocker.
Reviewed evidence supports all three actual #571 criteria; conditional Closes
permitted only after full verified receipt and approving exact-head assessment.
Original Review/outcome unchanged. P02-T02 is planned remaining delivery, not
complete at the evidence commit. Final receipt/status remains external to avoid
a post-gate self-invalidating commit. Hosted/owner approval remains separate.
