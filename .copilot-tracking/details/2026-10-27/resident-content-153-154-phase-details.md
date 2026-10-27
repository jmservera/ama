---
title: Resident content and journey phase details
description: Evidence, boundaries and task completion requirements
ms.date: 2026-10-27
---

## Metadata

Task ID: issues-153-154. Slug: resident-content-153-154.
Plan: .copilot-tracking/plans/2026-10-27/resident-content-153-154-plan.md.
Research: .copilot-tracking/research/2026-10-27/resident-content-153-154-research.md.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Audit/design documentation | Complete, P01-T01/T02 evidenced in changes |
| P02 | Literal copy and local regression | Complete, P02-T01/T02 evidenced in changes |
| P03 | One independent Review and PR | Ready for Review; publication conditional |

<!-- rpi:phase id=P01 -->
## P01: Documentation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Content inventory

C1-C4/C13/W1 establish current copy and stale reviewer appointment. Extend the
existing standard, preserving historical audits and current routine-policy
exception as inactive. Inventory list/case/final checks, draft/AI/proposals,
documents/import, finance/technical/stock, quality/appointments, complaints/
updates, chat/alerts, account/time, law reference and specialist foundations.
Classify raw messages/quotes, stored values and dynamic content as visible,
not magically excluded by tests. Residual reason/owner/action failures need
named responsible role for follow-up, not a fictional live case owner.
Completion: dated coverage and issue #153 criteria matrix with partial rows.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Resident designs

C5-C12/W3/W4 supply requirement intent and gaps. Add a dated section to existing
residents.md, no separate competing journey document. Six text wireframes:
measure choice, pause/withdrawal, visit offer/confirmation, owned update,
handover/aftercare, challenge/complaint/remedy. Each shows candidate plain copy,
controls or assisted prompts, receipt/reference, next owner/date or Unknown,
exception and accessible offline option. Define representative briefing
allowlist, current authority and revocation boundary, interpreter-only and
multiple-authority negative cases. Do not prescribe operational retention.
Support preferences are chosen, never inferred incapacity.
Use role ownership and unconfigured dates/routes visibly, never fake real
contacts or SLAs. Scripts for #155 retain Not run tester/AT/outcomes.
Completion: issue #154 criteria mapped to design evidence and human blockers;
knowledge-base index updated and append-only log entry.

<!-- rpi:phase id=P02 -->
## P02: Small safe copy changes

<!-- rpi:task id=P02-T01 -->
### P02-T01: Literal edits

C4/C5 justify "Review due date (authority unavailable from this date)".
C13 justifies assistant review disclaimer and "Requested using" instead of
"Invocation". The resident draft heading must not imply sending; accompanying
copy requires named human review before resident use. Ordinary "hold the same
role" becomes "have the same role". Do not change values/payloads, exception
handling, safety checks, auth or stored finance options. Repo ASCII/sentence
case and Fluent conventions override generic upstream typography/title-case.
Maximum four new test methods in test_content_standard.py, no removals.
Completion: focused string regressions plus actual browser evidence for the
changed render paths where existing fixture access supports them.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Validation and reconciliation

Use installed src distributions, pip only after a missing-dependency failure.
Run from src/api:
`PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest
test_content_standard test_design_system test_accessibility_baseline
test_resident_api test_assistants -q`, then
`python3 -m checks.design_system_browser_check`.
Before launch set TMPDIR to `.venv/ux153-tmp` under this worktree.
Use a session-only Playwright callback passed to that check's `main(callback)`
for actual case draft/representative panels and constructed assistantProposal/
timeView rendering. The latter two prove copy only, not authority acceptance.
The four-surface mapping in the plan is authoritative. Browser-check sources
and dependency manifests remain unchanged. No private default Store.
Record exact commands, counts/results, skipped/blocked scope and no human
acceptance. Syntax-check four changed JS files. Verify relative doc links and
git diff. Update plan markers/details and changes before Review. No --all;
small change does not justify --changed or heavy-lock acquisition.

<!-- rpi:phase id=P03 -->
## P03: Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Independent Review and PR

Refresh guidelines before independent review of changed web files against all
rules; report file:line residuals without claiming conformance. One fresh
reviewer activates rpi-review, writes the review only and does not implement.
Preserve original findings/outcome and route later work without re-review.
Commit implementation and RPI artifacts together; fetch main first, record
review boundary and no full local gate under explicit owner override.
Resolve gh account and repository-local privacy-safe email before commit.
Push only docs/resident-ux-153, never force; one PR to main, Refs #153/#154.
Publish only when required local checks pass and the one Review accepts the
unchanged source boundary. Adverse/Blocked Review or missing/failed required
check stops publication; preserve evidence and route later work, without
silently correcting/re-reviewing this task. Planned human acceptance remains
Not run and is not inferred from engineering acceptance.
Publication evidence must distinguish actual engineering checks from named
human wording review, usability/AT, external/service approval and hosted gates.
