<!-- markdownlint-disable-file -->
---
title: Case view review fixes 552 changes
description: Local implementation and validation record for both PR 554 findings
ms.date: 2026-10-29
---

## Metadata

Task ID: 552-pr554-review-fixes. Slug: case-view-review-fixes-552.
Plan: .copilot-tracking/plans/2026-10-29/case-view-review-fixes-552-plan.md.
Details: .copilot-tracking/details/2026-10-29/case-view-review-fixes-552-phase-details.md.
Date: 2026-10-29. Starting HEAD: 4220e7aa1c3557997f7149e997834c7b8b2657f9.

## Execution Status

Scope: full bounded plan. Status: P01/P02 and all tasks complete.
Implementation and original evidence committed locally as 5a3edfe6.
No remaining active task or implementation blocker. One independent Review
completed; original outcome preserved.

## Approved Scope and Critique

Exact selector, explicit nested PNG package-data, one preventive manifest
regression in the existing journey tests, API README and dated RPI artifacts.
No production JS/CSS, PNG byte changes or dependencies. No push, az or manual
rubric changes. Existing source-tree checks are not wheel proof.

One independent critique executed Complete / original Revise. PC-001 disposition
is in the plan: parent successfully uses external outputs; preserve them, embed
concise reviewable result extracts here, explicitly qualify any raw evidence
the reviewer cannot independently inspect. Do not repeat critique or import
worker-specific filesystem restrictions into parent execution.

## Baseline Evidence

Both named failures reproduced before source changes. Pre-fix wheel at
`/tmp/case-552-review-fixes-20261029-wheel-before/` built successfully but ZIP
contained zero journey-icon members. Actual synthetic Playwright journey
failed at the six-term assertion after the first four checks passed. Commands
and C1-C8 evidence are in the research artifact.

## Completed Work

### P01-T01: Exact fixes and preventive packaging regression

* Changed the summary selector to `.case-summary > dl > div > dt`; nested
  popover definition terms remain semantic and no longer affect the assertion.
* Added `web/journey-icons/*.png` to API setuptools package data.
* Added one manifest test to test_case_journey.py, preserving provenance tests.
  It reads actual package data and verifies all six existing source paths are
  covered. Before the fix it failed for all six icons (one test, six subtest
  failures; exit 1), proving it catches this omission.
* API README now explains wheel/container inclusion. No production UI or
  generated icon bytes changed.

### Immediately relevant implementation refinement

P01-T01 uses existing pathlib Path.match, not proposed fnmatch: fnmatch `*`
crosses `/`, so it would falsely treat `web/*` as recursive. Path.match models
the segment-specific package glob for this check. One-test budget and scope
unchanged; plan/details reconciled directly without a new user decision or
repeated critique.

## Validation Record

All commands below use `/tmp/mv`. From `src/api`, tests/browser use exactly:
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.

| Check | Command or scope | Result |
| --- | --- | --- |
| Focused API tests | python -m unittest test_case_journey test_workspace_scripts test_design_system test_accessibility_baseline test_content_standard -q | Exit 0, 55 tests in 6.306s |
| Ruff lint | ruff check checks/case_journey_browser_check.py tests/test_case_journey.py | Exit 0 |
| Explicit legacy file format attempt | ruff format --check checks/case_journey_browser_check.py tests/test_case_journey.py | Exit 1: legacy browser file has existing formatting differences; test file already formatted |
| Baseline format confirmation | git show 4220e7aa:src/api/checks/case_journey_browser_check.py piped to ruff format --check --stdin-filename src/api/checks/case_journey_browser_check.py - | Exit 1, same pre-existing debt |
| Repository-policy format check | ruff format --check --force-exclude checks/case_journey_browser_check.py tests/test_case_journey.py | Exit 0; one file already formatted; checks/*.py uses existing pyproject exclusion |
| JavaScript syntax | node --check src/zava_forward/api/web/case-workspace.js and node --check src/zava_forward/api/web/app.js | Both exit 0 |
| Fresh wheel | python -m pip wheel --no-deps --wheel-dir /tmp/case-552-review-fixes-20261029-wheel-after ./src/api --quiet (root) | Exit 0 |
| ZIP member/byte inspection | zipfile exact six-path set plus equality to each source PNG | Exit 0, six verified |
| Full journey browser | python -m checks.case_journey_browser_check --axe /tmp/ama-526-evidence/axe-4.10.3.min.js --out /tmp/case-552-review-fixes-20261029-journey | Exit 0 |
| Compact view browser | python -m checks.case_view_ux_browser_check --out /tmp/case-552-review-fixes-20261029-compact | Exit 0 |
| Whitespace diff | git diff --check | Exit 0 |

The selector line was wrapped to match formatter output without reformatting
unrelated existing legacy content. No formatter configuration was changed.
Node checks ran successfully in the second lint batch after the first command
chain stopped at the explicit legacy formatting failure.

### Actual wheel output

Wheel: `/tmp/case-552-review-fixes-20261029-wheel-after/zava_forward_api-0.1.0-py3-none-any.whl`.
SHA-256: `45307d065235102fcb8d494c3f946c7fb1b842b5e43e331ff595d8c45f605047`.
Machine evidence: sibling `wheel-evidence.json`. All six paths have prefix
`zava_forward/api/web/journey-icons/`; no other journey-icon entries exist.

| Member | Bytes | SHA-256 | Source bytes equal |
| --- | --- | --- | --- |
| assessment.png | 27112 | cbecff037664e043a446729b1a992dddbce5991faf1cce3f3553cd718c122172 | true |
| contractor.png | 32866 | 3be0d5dda089346613a7b8d4484d6ed26f88d276f08fc36189d854982b4cdf04 | true |
| funding.png | 55487 | 4c7fde72fef9bd8261a31cacea3b82499b853546e6c0196a8e5796ba7eb2592a | true |
| quality.png | 29923 | f4be1e6c6f532148eb6524330337905b9642bdfbbcee0c39544801957ce6029f | true |
| resident.png | 24554 | 5e5cb76dbec297b3b7313f5aabacfb37cba179ef941705077071199f0e3b209b | true |
| survey.png | 28050 | 691d12c8568fa7cff1e4233fb6a2091a794b71e65f18e8f515f6fa0efc2a15e2 | true |

### Browser evidence extracts

Both real synthetic loopback servers were healthy and both harnesses closed
their owned server/browser processes. No private dataset or cloud/model calls.
Chromium 156.0.8078.4 / Playwright 1.64.0.

Journey results: `/tmp/case-552-review-fixes-20261029-journey/results.json`.
Corrected six-summary assertion passed with ZF-1 unconfirmed-funding blockers.
Full mutation/reconstruction/retained-field/keyboard/forced-colour/mobile/zoom
checks passed. Exact aggregate from the `scans` array:

```json
{
  "browser": "156.0.8078.4",
  "axe_version": "4.10.3",
  "scan_count": 87,
  "violation_count": 0,
  "serious_critical_count": 0,
  "incomplete_count": 50,
  "page_errors": [],
  "zoom": "chrome.tabs.setZoom=2; innerWidth<=640"
}
```

Incomplete automated checks remain incomplete; no WCAG acceptance claim.
Screenshots: desktop-1280.png, mobile-320.png, forced-colours.png,
browser-zoom-200.png in the same external directory.

Compact results: `/tmp/case-552-review-fixes-20261029-compact/results.json`.
1280/390/320 widths all had no page overflow. At 1280, heights were
66.390625/66.390625/110.390625/90.390625/66.390625/90.390625; at both narrow
widths ordinary steps were 66.390625 and blocked funding 110.390625, within
132/116px limits. Six decorative deck icons loaded. Keyboard/touch reached
last next action, enlarged text stayed bounded, tabs stayed fixed above panel
scroll, URL/history and fields persisted. Both unavailable-script and deliberate
enhancement-error fallbacks showed nine unbounded panels, usable ordinary
input, reachable safety and zero unexpected errors. Top-level errors: [].
Screenshots and complete JSON stay in that external directory.

## Pre-Review Reconciliation

Ready: P01/P01-T01/P01-T02 marked complete with current details and commands.
Only P02/P02-T01 local persistence remains. No implementation blocker
or divergent user decision. PC-001 disposition, follow-ups and evidence scope
agree across plan/details/state/changes. This task did not edit production web
files; a new design/accessibility review is not claimed or required for this diff.
Review should assess the four-file correction and recorded local evidence,
not certify live deployment or close all issue #552 criteria.

## Original Independent Review

One independent Review executed at
.copilot-tracking/reviews/logs/2026-10-29/case-view-review-fixes-552-review.md.
Execution: Complete. Outcome: Conformant with justified divergence.
No new substantive findings. It independently inspected the full diff, manifest,
source hashes and test budget; it assessed recorded execution results without
accessing raw /tmp wheel/browser outputs or screenshots. That source/record
boundary is sufficient for these two corrections, not wider rendered acceptance.
Inherited RV-001 and incomplete axe checks remain separate. No second Review.

## Local Persistence Preparation

Authenticated GitHub identity resolved with gh api user: id 8036360, login
jmservera. Author and committer must use repository-local
8036360+jmservera@users.noreply.github.com and the requested Copilot trailer.
Commit implementation and original evidence, then record final closeout.
git-commit skill's referenced supplemental commit-message instruction file is
unavailable; follow repository/user Conventional Commit and trailer requirements.
Its get_changed_files tool is unavailable, so use repository-standard Git CLI
for explicit task-only staging and required commit/worktree verification.

## Follow-Up Items

Inherited issue-wide RV-001 remains outside this scoped task and unchanged.
No full publication gate, hosted approval or human acceptance is claimed.

## Local Commit and Final Closeout

Implementation plus original dated RPI evidence committed as
`5a3edfe674368de9a144af137107722434927857`:
`fix(api): scope summary terms and package journey icons`.
The commit contains Refs #552 and the exact requested Copilot co-author
trailer. Author and committer both verified as
jmservera <8036360+jmservera@users.noreply.github.com>. git status --short was
empty afterward. The final closeout updates only plan/details/changes/state
in a separate local documentation commit; no assessed source changes,
amendment, rewritten history or second Review.

Mode: manual, bounded full-loop request complete; session stopped. No push,
az or hand-edit of rubric scores occurred. The rubric remains byte-identical
to pulled 4220e7aa. Full publication gate, deployed container, hosted/human
approval and issue-wide acceptance are not established or waived.
Only inherited RV-001 remains a separate future user-selected work item.
