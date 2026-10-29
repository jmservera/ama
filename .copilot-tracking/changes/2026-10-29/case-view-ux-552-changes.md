<!-- markdownlint-disable-file -->
# RPI Changes: Compact case view

Task ID: 552. Task slug: case-view-ux-552. Date: 2026-10-29.
Scope: full approved plan. Status: locally committed implementation and
validation complete; one independent Review executed Partial / Residual work.

## Plan and Decisions

Plan: .copilot-tracking/plans/2026-10-29/case-view-ux-552-plan.md.
Details: .copilot-tracking/details/2026-10-29/case-view-ux-552-phase-details.md.
Research Ready; one independent critique originally Revise. PC-001/002
incorporated directly, no repeat critique. Owner directs the ordered full
loop and a local-only commit. No automatic-session opt-in is inferred.

## P01-T01: Baseline and Asset Provenance

Real constructed-data baseline:

```bash
cd src/api
PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests \
  /tmp/mv/bin/python -m checks.case_view_ux_browser_check \
  --baseline --out /tmp/case-552-baseline-20261029
```

Passed at 1280/390/320px without page overflow. Baseline results and screenshots
remain in that external directory. The long two-blocker fixture made the
desktop grid 1464.95px per step, and the narrow blocked step 690.11/975.58px.
Other narrow steps were 78.39px.

Extracted these bytes from `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`
slide 4 ZIP media into `src/api/src/zava_forward/api/web/journey-icons/`:

| Step/file | Deck media | SHA-256 |
| --- | --- | --- |
| survey.png | image11.png | 691d12c8568fa7cff1e4233fb6a2091a794b71e65f18e8f515f6fa0efc2a15e2 |
| assessment.png | image6.png | cbecff037664e043a446729b1a992dddbce5991faf1cce3f3553cd718c122172 |
| funding.png | image12.png | 4c7fde72fef9bd8261a31cacea3b82499b853546e6c0196a8e5796ba7eb2592a |
| resident.png | image13.png | 5e5cb76dbec297b3b7313f5aabacfb37cba179ef941705077071199f0e3b209b |
| contractor.png | image14.png | 3be0d5dda089346613a7b8d4484d6ed26f88d276f08fc36189d854982b4cdf04 |
| quality.png | image15.png | f4be1e6c6f532148eb6524330337905b9642bdfbbcee0c39544801957ce6029f |

Generated binary extraction used Python zipfile, not manual image recreation.
Unit coverage verifies the exact tracked deck bytes.

## P01-T02: UI Implementation

Completed: icons with decorative alternatives/dimensions; compact token spacing;
status words retained; one-line first reason with full all-blocker reason,
owner and next action in native auto popovers. Missing owner/action is explicit,
text stays safely escaped and disclosure controls are outside workflow links.
Wrapping tablist is now part of the panel's bordered workspace, outside its
70dvh scrolling panel. URL/manual keyboard activation and mounted draft state
are unchanged. Enhancement failure removes its tab/layout state and restores
all unbounded sections. API README records behaviour and local commands.

No backend, authority, consent, manual task control, independent safety or
existing status-classification changes. P01/P01-T01/P01-T02 complete.

## P02-T01: Validation

Existing regression command (from src/api, same PYTHONPATH as above):

```bash
/tmp/mv/bin/python -m unittest test_case_journey test_workspace_scripts \
  test_design_system test_accessibility_baseline test_content_standard -q
```

First run before updating the intended blocker assertion: 52 tests, seven
subtest failures expecting full reasons in status text. Updated that expectation
to assert concise status and complete `blockers` data; added two shipped-JS/
asset tests. Subsequent run: 54 tests passed (4.301s).

Node syntax: `node --check src/api/src/zava_forward/api/web/case-workspace.js`
and `node --check src/api/src/zava_forward/api/web/app.js` passed.

Browser iteration commands use `python -m checks.case_view_ux_browser_check
--out <new-external-path>` with the same interpreter/source roots as baseline:

| External output | Result |
| --- | --- |
| /tmp/case-552-ui-first-20261029 | Failed: keyboard scroll was measured before native scrolling settled. Added a scroll-completion condition, not a source workaround. |
| /tmp/case-552-ui-second-20261029 | Passed keyboard disclosure, enlarged text, tabs, retained fields, panel scroll and reduced motion. |
| /tmp/case-552-ui-third-20261029 | Failed touch harness: CDP synthesizeScrollGesture did not scroll the native popover. |
| /tmp/case-552-ui-fourth-20261029 | Passed actual dispatched touchStart/touchMove/touchEnd swipes, light dismiss, keyboard, enlarged text, both fallback scenarios and all prior checks. |

Fourth-run collapsed heights: desktop 66.39-110.39px; both narrow widths
66.39px ordinary and 110.39px blocked. Default-size non-blocked narrow steps
are 15.3% shorter; long blocked steps are 84.0%/88.7% shorter at 390/320px.
Every ceiling (desktop <=132px, narrow <=116px) and no-overflow check passed.
At 320x480, keyboard and touch both reached final next action at scrollTop1094,
scrollHeight1548/clientHeight454; enlarged 200% root text reached the end
(scrollTop7808, scrollHeight8238/clientHeight430). Full screenshot/JSON evidence
is external per retention policy; no historical evidence was deleted.

Initial lint found unsorted added import and a long assertion; corrected.
Ruff format then identified the new browser file; formatted it. Initial mypy
found two Any-return annotations; replaced them with typed local dict results.
Ruff and mypy subsequently passed. The first final-assertion run (`/tmp/case-552-ui-final-20261029`) failed because
the focus assertion followed pointer-mode programmatic focus. The check now
uses actual Tab/Shift+Tab and verifies the returned focused control.
The next run (`/tmp/case-552-ui-verified-20261029`) failed the added open-safety
navigation assertion: the synthetic dirty-note discard dialog was auto-dismissed
and an existing fallback message was read before the new case mounted.
The harness now explicitly accepts only its constructed-data dialog and waits
for ZF-4's workspace. No production workaround was required.

Final complete command and outcome:

```bash
cd src/api
/tmp/mv/bin/ruff check checks/case_view_ux_browser_check.py tests/test_case_journey.py
/tmp/mv/bin/ruff format --check checks/case_view_ux_browser_check.py tests/test_case_journey.py
/tmp/mv/bin/mypy checks/case_view_ux_browser_check.py
PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests \
  /tmp/mv/bin/python -m checks.case_view_ux_browser_check \
  --out /tmp/case-552-ui-complete-20261029
```

All passed. Chromium 156.0.8078.4 / Playwright 1.64.0. External `results.json`
records final widths/heights, versions, scroll geometry and fallback results;
screenshots: `case-1280.png`, `case-390.png`, `case-320.png`,
`journey-{1280,390,320}.png`, `popover-keyboard-320.png`,
`popover-touch-320.png`, `popover-200-percent.png`, `attached-tabs-1280.png`.
All final geometric values match the fourth-run figures above. Both fallback
cases also prove the open-safety panel precedes the workspace outside its
scrolling bounds. Disclosure target is >=40px with visible keyboard focus.
Final Node checks passed again; final unittest: 54 tests passed in 3.264s.
No unexpected JavaScript errors. Local processes were stopped by harness cleanup.

### Scoped Web Interface Guidelines review

Source refreshed 2026-10-29:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Reviewed all changed web code against all fetched rules and inspected final
desktop, narrow, enlarged-text and touch screenshots. Existing unrelated
screen copy/controls are outside this slice. Native controls supply activation,
popover dismissal is not hover-only, all full text has a scrolling path,
decorative images have dimensions/alternatives, and layout uses existing tokens.
Repository sentence-case/ASCII content standard takes precedence over the
generic title-case/typography preferences. No new animation or dependencies.

#### src/api/src/zava_forward/api/web/case-workspace.js

Pass: no new material finding.

#### src/api/src/zava_forward/api/web/app.js

Pass: no new material finding.

#### src/api/src/zava_forward/api/web/style.css

Pass: no new material finding.

All runs start a real sanitized loopback server, construct synthetic data,
block nonlocal browser requests and stop their owned server/browser processes.
No default/private ZF_DATA is opened; no cloud/model calls are used.

## Amendments and Divergences

PC-001 long-disclosure reachability and PC-002 fallback scenarios extend the
existing browser check scope, not source/framework scope. Six PNG assets are
generated byte-exact from the available tracked capstone deck because
docs/presentations is absent. This is ordinary evidence-backed local judgment.

## Remaining Work and Limitations

Full publication gate, hosted checks,
human/AT/user acceptance and cross-browser checks are not claimed. A full
publication gate would include prohibited az tooling and is neither run nor
waived; no publication is requested. No push, az, Azure modifications or rubric
score edits.

## Pre-Review Reconciliation

P01/P01-T01/P01-T02 and P02-T01 completion evidence is current. P02-T02 is the
remaining Review/commit task, so P02 is not yet marked complete. Plan/details,
research, original critique, changes and state agree. No implementation blocker
or significant divergence remains. Broader Fluent adoption and cross-browser/
AT/user acceptance remain follow-up boundaries, not completed criteria.
Review-ready for the local web slice; not publication-ready.

## P02-T02: Original Independent Review

Record: .copilot-tracking/reviews/logs/2026-10-29/case-view-ux-552-review.md.
One independent Review executed. Execution: Partial. Outcome: Residual work.
No implementation defect was identified. RV-001 (Medium) is an evidence-access
gap: the reviewer could inspect source/tests/icons/provenance but its own
environment prohibited direct access to the external /tmp browser JSON/PNGs.
Parent directly inspected the final JSON and desktop/narrow/popover screenshots
during implementation, but that is not relabelled as independent acceptance.

RV-001 is routed to a distinct later rpi-research evidence-reconciliation action.
No source correction, second Review, closure verification or waived restriction
is performed inside this task. Original Partial/Residual work remains unchanged.
Do not use a closing keyword on the strength of this review; any later PR uses
`Refs #552` until all criteria have independently sufficient evidence.
Cross-browser/AT/user acceptance and wider Fluent adoption remain separate.

The local source/test/documentation slice is ready to persist, not approved for
publication. A local commit is explicitly owner-authorized and is not a push,
PR creation, Azure change or acceptance of the unresolved review evidence gap.

## Local Commit and Final Handoff

Implementation plus original dated RPI evidence committed as `e130e33f`
(`feat(api): compact case journey and attach section tabs`). Author and committer
both use the authenticated GitHub account's privacy-safe address, and the
requested Copilot co-author trailer is present. The commit uses Refs #552.
Worktree was clean immediately afterward. No push or PR was performed.

P01/P01-T01/P01-T02/P02/P02-T01/P02-T02 execution is complete for this bounded
local task; this does not promote the Partial Review to completed independent
acceptance. This closeout records final plan/detail/state status in a separate
documentation-only commit, preserving the original Review and source boundary.
RV-001 remains open and routed to later evidence work; no closure verification
or second Review is performed here. No full publication gate, hosted approval,
human approval, Azure operation or rubric-score change is claimed.
