---
title: Employee single case view changes
ms.date: 2026-10-30
---

## Scope and Status

Task ID 552, slug employee-single-case-view-552; full plan scope.
Plan/details/critique/research use the same slug and 2026-10-30 date.
P01-T01 and P02-T01 complete; single Review complete. Runtime already delivered by merged PR #554;
no unsupported source redesign planned.

## Plan and Critique Reconciliation

Original critique Complete / Revise preserved. PC-001 parent /tmp restriction
premise rejected: no such restriction applies to parent; user explicitly
requires the shared /tmp lock. Fresh reviewer evidence uses external session
files/case-552-browser, not /tmp. No second critique.

## Implementation

Updated src/api/checks/case_view_ux_browser_check.py to require pinned axe for
normal verification, reuse the existing journey scanner and reject all
violations. Reports preserve violations/incomplete results, completion state
and axe hash. Added shared-surface/adjacency/non-scrolling-tab ancestry and
actual keyboard panel scrolling assertions at all three widths, plus per-width
screenshots. Existing keyboard/touch, safe-content, enlarged-text and fallback
checks remain. README documents invocation and evidence limits.
No new unit methods, test removals, dependencies, runtime edits or generated
source. This preserves the already delivered issue scope rather than inventing
a second redesign.

## Validation

Heavy checks use the required flock -w 600 shared lock.

| Check | Result | Evidence |
| --- | --- | --- |
| Full API unittest discovery | Passed: 1379 tests, 483.427s, 320 skips | External session files/case-552-api-checks.log; exact requested PYTHONPATH, /tmp/mv/bin on PATH |
| ruff check . | Passed | Same locked command/log |
| ruff format --check . | Passed: 61 files already formatted | Same locked command/log |
| mypy | Passed: 117 source files | Same locked command/log |
| node --check case-workspace.js | Passed | Parent direct execution |
| git diff --check | Passed | Parent direct execution |
| Missing axe and invalid hash | Passed negative checks: exit 2 / exit 1, no output directory created or app startup | External session files/case-552-input-check.log |
| First browser attempt | Not run: shared-lock wait reached 600s, exit 1, empty log and absent output directory | External session files/case-552-browser.log |
| Browser retry | Passed under the same required lock, never bypassed | External session files/case-552-browser-retry.log and files/case-552-browser/results.json |

API command from src/api:
`PATH=/tmp/mv/bin:$PATH PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`
then `flock -w 600 /tmp/ama-rpi-heavy.lock bash -c 'python3 -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy'`.
Skips are not executed integration evidence. No live sign-in was attempted;
authentication log lines in this suite are synthetic fixture tests.

### Browser Evidence and Acceptance Mapping

External root:
/home/azureuser/.copilot/session-state/efa3c0ae-28bb-4df9-acfd-bd663c72eec3/files/case-552-browser.
Normal mode completed=true; Chromium 156.0.8078.4 / Playwright 1.64.0.
Pinned axe SHA-256:
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
Command from src/api, same PATH/PYTHONPATH:
`flock -w 600 /tmp/ama-rpi-heavy.lock python3 -m checks.case_view_ux_browser_check --axe /tmp/ama-533-correction2-20261029/axe-4.10.3.min.js --out <external-root>`.
App starts its own constructed-data loopback server and proves responsiveness;
blocks external requests, exits and cleans up its own process. No real account,
dataset, credentials or model calls.

| Issue criterion | Current local evidence | Boundary |
| --- | --- | --- |
| 1: presentation icons and labels | Six loaded decorative images, correct six visible labels at all widths; full API regressions verify exact deck bytes and package inclusion | Runtime already delivered by #554, not a new icon implementation |
| 2: thinner layout | 1280px heights 66.39/66.39/110.39/90.39/66.39/90.39px; 390/320px ordinary steps 66.39px, blocked step 110.39px; no page overflow; ceilings 132/116px pass | Historical Review's pre-redesign figures remain historical, not freshly rerun before/after evidence |
| 3: blocker disclosure | Single-line summary at all widths; keyboard Enter/Space/Escape and focus return; actual touch swipes/light dismissal; complete missing-owner/action recovery. At 320x480 final item visible, scrollTop 1094 / scrollHeight 1548 / clientHeight 454; 200% root text final item visible, scrollTop 7808 / height 8238 / clientHeight 430 | Chromium engineering, not screen-reader or physical-device acceptance |
| 4: attached tabs/panel | Shared surface, adjacent boundaries, no tablist/surface inner scrolling, actual panel keyboard scrolling and identical before/after tablist bounds at 1280/390/320; retained note and URL/back/manual tab keys | Narrow tablist wraps to 421px; content scroll remains separate, no redesign implied |
| 5: Fluent/WCAG preservation | No runtime source changes; baseline design/content/accessibility regressions pass; nine axe states have zero violations; reduced-motion token remains zero; both enhancement failures preserve nine visible unbounded sections, safety and manual input | Three scrolled Resident scans each retain color-contrast incomplete for the clipped offscreen Resident heading and Notes field; not full WCAG/AT or full Fluent adoption |
| 6: desktop/narrow evidence | Current results.json plus journey/case/attached-tab 1280/390/320 screenshots and keyboard/touch/enlarged-text popovers | Parent and independent reviewer directly inspected raw JSON and representative desktop/narrow/popup images |

Axe overview and open-blocker scans have no incomplete checks at all three
widths. Scrolled Resident incomplete findings are retained in full, with reason
"background color could not be determined because it's partially obscured by
another element"; these offscreen targets are not silently counted as passes.
Actual attached tablist bounds before/after: 1280 x17/y110.171875/w1246/h109;
390 x17/y379.1875/w356/h421; 320 x17/y378.984375/w286/h421.
Recorded scrollTop is positive at all widths (70/157/168); the script asserts
scrolling, not arrival at the end for these panel checks. Popover checks
separately assert final-item visibility. All unexpected JS error lists empty.

## Pre-Review Reconciliation

P01/P01-T01 complete; P02-T01 complete. P02/P02-T02 intentionally remain
unchecked until the one Review and local commit. Plan/details and current
changes agree; no implementation blockers or open runtime defects. Review is
ready for this scoped evidence increment, with publication/full gate blocked
as recorded below. No repeated critique and no source changes after Review.

## Independent Review Outcome and Routing

Exactly one Review executed, Complete / Residual work:
.copilot-tracking/reviews/logs/2026-10-30/employee-single-case-view-552-review.md.
Independent reviewer directly inspected new raw JSON, logs and representative
desktop/narrow/disclosure screenshots, compared exact icon bytes with the deck
and refreshed the complete Web Interface Guidelines. No introduced defect.
All six criteria have bounded local engineering support; criterion 5 is not
full accessibility acceptance.

* RV-001 High: full publication gate unavailable under no-Azure instruction.
  Coordinator owns execution-boundary resolution and unchanged complete gate
  before publication. No source fix or second Review.
* RV-002 Medium: three scrolled-Resident contrast incomplete entries/six node
  observations require named human assessment with targets visible. Accessibility
  owner follow-up, not an observed contrast failure or source-fix mandate.
* RV-003 Low: inherited app.js form name/autocomplete and stylesheet
  non-compositor transition debt. Distinct API/design-system maintenance;
  unchanged runtime is not silently relabelled guideline-clean.

Original Review/critique outcomes remain unchanged. No routed finding is
implemented or closure-verified within this completed one-pass assessment.

## Final Local Persistence Boundary

Scoped implementation/validation and Review finished; full-plan validation is
Partial because P02/P02-T02 retains its unmet complete-gate requirement.
The enclosing local commit persists source, README and dated original evidence.
Authenticated GitHub identity resolved as jmservera, id 8036360; repository-local
noreply email is used for both author and committer, with requested Copilot
trailer. No push, issue mutation or hosted/human approval. Commit success and
clean worktree are verified separately by the parent, not fabricated here.

## Known Publication Blocker

Full gate not executed: tools/rpi-checks.py preflight mandates
az bicep version; infrastructure mandates az bicep build/lint. The user prohibits
Azure. Do not patch the runner, invoke prohibited commands or fabricate a
receipt. Focused success cannot establish complete gate/publication readiness.
No push, live sign-in, secrets or cloud operations.

## Remaining Work

RV-001 complete gate remains blocked; no full receipt exists. RV-002 manual
contrast/AT/platform assessment, RV-003 inherited UX maintenance and #150
Fluent integration remain distinct follow-ups. Original 2026-10-29 Partial
Review is not rewritten. No further source work or remote action is authorized.
