---
title: Resident assistant publication research
ms.date: 2026-10-27
---
<!-- markdownlint-disable-file -->

## Research Brief

Investigate the publication continuation of #469 on
`feat/resident-assistant-aoai`, for the owner and PR reviewers. Output mode:
convergence. Scope is branch reconciliation, local validation, evidence and
non-draft PR publication. No deployment, Azure operations, private migration,
resident credentials, paid inference, ingress edits, merging or main pushes.
The caller explicitly requests the full automatic RPI loop and scoped gate.

## Research Parameters

Focused posture, selected for the bounded internal publication task. Evidence
root: `.copilot-tracking/`. Research edits are evidence/state only. Initial
areas: original AOAI RPI evidence, `src/README.md`, gate runner and branch
ancestry. External area: GitHub branch/issue/PR metadata only. Stop immediately
if the shared lock cannot be acquired with timeout zero. No interaction is
necessary: publication and cleanup are explicitly requested.

## Extension Registry and Provenance

Repository instructions and retention policy selected for all evidence and
cleanup. RPI Research selected for evidence/readiness; Plan/Implement/Review
are parent-owned later phases. No UI source edits or new Azure/pricing claims
are planned, so UI/design and external-domain research extensions are skipped.
Research stays inline because this is one connected publication trace.

## Prior Knowledge Gate

Read original case study, relevant addendum, reference index, owner memory,
sector primer, retention policy, source gate guide, original AOAI state,
changes and Review. Prior-session search found no matching recent session;
the committed artifacts are the recovery source. The similarly named
`resident-assistant-469` artifacts belong to earlier rules-only work and are
not the current AOAI task. Original adverse Review remains immutable.

## Direction Controls and Questions

* Q1: Is the approved branch clean and current, and is publication authorized?
* Q2: Can the existing gate run without deadlocking on our own lock?
* Q3: What evidence is mandatory, and what remains explicitly unmet?
* Preserve USD20 within owner-approved resident USD30; issue body USD5 is
  historical, not current owner direction.
* Keep deliberately open demo ingress unchanged through 2026-12-31.
* No force pushes, deployment, Azure calls, secrets, uv or merge.

## Research Cycle Log

### Cycle 1: Wider

Read branch/PR metadata and original evidence. Working tree is tracked-clean;
three local commits and zero upstream-main commits are outstanding. No PR
exists for this head. Heavy lock acquired with `flock -w 0` in an attached
foreground process. Reflection: this is a publication child task, not a
reopening or regrading of the original implementation Review.

### Cycle 1: Deeper

Inspected the runner's exact lock and receipt contracts. It acquires the same
lock internally, so release the initial reservation immediately before the
foreground runner's own `--lock-timeout 0` acquisition. Never bypass or modify
locking. Python 3.12 and Docker are available; global Python lacks installed
project distributions and pyodbc. Use existing pip-based isolated gate setup,
or install into a new external venv after this observed missing dependency.
Reflection: commit dated original evidence before the exact-head gate;
later evidence commits invalidate receipts and require reruns.

### Cycle 1: Contrarian

Challenge the assumption that scoped validation alone authorizes publication.
The source guide says infrastructure/SQL/security changes require the complete
gate. Original state explicitly retained this prerequisite. Run the requested
`--changed` gate first, inspect coverage, and also run `--all` if it does not
provide complete coverage. Do not equate mocks or unit-discovery skips with
actual SQL cap evidence. Private migration and authenticated MI smoke remain
unmet even if every local gate passes. Reflection: these are live-acceptance
limits, not permission to deploy.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Three local commits, no stale main ancestry after fetch; clean tracked tree; no head PR | Git inspection 2026-10-27; HEAD 8f51686a3fbc4b1ca9a6e258a921b96f4fdeb8a6; main 49c942b33b89100c084d48a91215989e22de5887 |
| C2 | Complete gate required for this SQL/infra feature; partial evidence is explicitly distinct | src/README.md:44 |
| C3 | Runner uses non-reentrant shared flock and verifies exact committed clean inputs | tools/rpi-checks.py:2175; tools/rpi-checks.py:2191 |
| C4 | Original Review not accepted for whole-task/live acceptance; SQL and MI gaps remain | .copilot-tracking/reviews/logs/2026-10-27/resident-assistant-aoai-review.md:44 |
| C5 | USD20 permanent cap inside USD30; MI-only; default disabled; live activation separate | docs/architecture/resident-assistant-prototype.md:9 |
| C6 | Explicit finite archive/restore-backed cleanup required | docs/reference/method/tracking-retention-policy.md:24 |

No external research sources used. GitHub issue metadata confirms #469 remains
open; its older USD5 proposal conflicts with newer recorded owner direction
and is superseded, not silently rewritten.

## Findings, Alternatives and Decision State

Q1 answered by C1: reuse the exact requested branch; no rebase or merge is
needed. Q2 answered by C3: hand off the lock to the unchanged runner with
timeout zero and stop on contention. Q3 answered by C2/C4/C5: preserve the
complete-gate policy, disclose private migration/MI gaps, and retain human
and hosted approval boundaries.

Selected approach: scoped then complete local coverage as necessary, actual
component unit suites, independent publication Review, commit dated evidence,
fresh exact-head gate/verification, independent exact-head assessment and
authorized non-draft PR with `Refs #469` only. Reject skipping the full gate,
lock bypass, deployment and upgrading original Review acceptance.

## Readiness and Self-check

Research disposition: executed. Planning Readiness: Ready.
No further research cycle is needed: the three questions are resolved by
current local contracts. Execution may still be blocked by local prerequisites
or actual tests. Research is complete, not publication or live acceptance.
Parent owns transition to Plan; original AOAI artifacts remain unchanged.
