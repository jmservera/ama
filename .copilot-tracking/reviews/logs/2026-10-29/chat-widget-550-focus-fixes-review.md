<!-- markdownlint-disable-file -->
# Review: Chat focus review follow-up

## Scope and Evidence

* Task: 550-focus-fixes, selected later follow-up to 550.
* Review date: 2026-10-29.
* Boundary: full uncommitted follow-up candidate on feat/chat-widget-550,
  HEAD 9658b51b; all seven tracked changed files and the complete untracked
  src/api/tests/test_chat_widget_focus.py were read. This is not a committed
  exact-head publication assessment or another Review of original task 550.
* Compared artifacts: current follow-up research, plan, phase details, preserved
  critique and changes record; original chat-widget-550-review.md, including
  original RV-001/RV-002 and its adverse outcome.
* External evidence root E:
  /home/azureuser/.copilot/session-state/ba136591-973c-4ee0-8900-4f986afd68fb/files.
  Read browser.log, unittest.log, static.log, baseline-negative.log, opt-in.log,
  employee.log, resident.log, chat-focus-browser/results.json,
  employee-browser/axe-results.json and resident-browser/report.json.
  Visually inspected chat-focus-browser/resident-external-focus-320.png and
  chat-focus-browser/employee-320.png.
* Repository context: original case study, addendum, reference index, owner
  memory and Fluent/content/WCAG baselines. No private dataset was inspected.

## Opening Review State

* Interpreted goal: independently assess the entire selected follow-up once,
  including original RV-001/RV-002 resolution.
* Scope: shared widget JS/CSS, employee adapter, three changed browser checkers,
  new Node behavioral unittest, API README and coherent follow-up evidence.
* Evidence readiness: supplied source and external local-validation logs readable.
* Acceptance basis: owner focus-not-obscured, user-driven focus, polite updates,
  retained operations/privacy/session recovery; accepted PC-001 through PC-004.
* First comparison: complete diff and new test against current phase markers,
  then behavioral oracles and external browser evidence.
* Read-only boundary: ONLY this review record may be modified. No wrapper state,
  source, other evidence, commits, dependency changes or nested agents.
* Initial blockers: none to source/evidence assessment. Reviewer cannot perform
  prohibited temporary-directory file operations; recorded parent-runtime checks
  are distinguished from independently executed checks.

## Execution Status

* Review execution: Complete. Exactly one independent implementation Review,
  performed directly with no nested agents.
* Implementation: P01/P01-T01/P01-T02 and P02-T01 executed. P02/P02-T02 correctly
  remain unchecked before parent Review reconciliation and requested local
  commit. This record completes the Review component only, not the commit.
* The changes record's initial "P01 starting" statement is chronological opening
  state, superseded explicitly by its Final Validation and Pre-Review
  Reconciliation sections. No contradictory completed-commit claim was found.

## Plan-to-Change Reconciliation

| Current scope | Actual changes/evidence | Assessment |
| --- | --- | --- |
| P01-T01 external focus | Document focusin calls hide(false); matching removal on disposal | Reconciled; no cancellation, state reset, focus return or geometry reads introduced |
| P01-T01 async ownership | Removed employee setup/finally focusInput; guarded denial recovery | Reconciled; only removed-popup-owned focus recovers to app |
| P01-T01 responsive/live semantics | Removed short-height overlap override; explicit polite atomic errors | Reconciled with PC-001/PC-003 and existing Fluent tokens |
| P01-T02 regressions | One new Node test module; expanded shared browser check; narrow audience migrations | Reconciled; no test removal, backend change or broad fallback |
| P02-T01 validation/docs | README explains hiding, retained work and polite non-refocusing updates; recorded requested local commands | Reconciled, with independent versus supplied evidence separated below |
| P02-T02 Review/commit | One Review now complete; original closure append and local commit belong to parent | Pending parent closeout is not falsely marked complete |
| Follow-Up Items | Original baseline height, human/live acceptance and publication gates | Remain distinct, outside active acceptance |

## Completed Work Assessment

* src/api/src/zava_forward/api/web/chat-widget.js:107-110 dismisses only a
  visible popup when focus is outside popup and launcher. hide(false) at :61-65
  changes visibility/expanded state without focus redirection or cancellation.
  Draft, history, skill and pending busy state survive; listener removal at
  :123-128 prevents disposed roots retaining the document hook.
* src/api/src/zava_forward/api/web/chat-widget.css:1-2 retains the fixed
  launcher's safe-area-aware bottom position and reserves 5.5rem below the
  popup. Removing the old max-height:35rem override removes the overlap rather
  than masking it with a focus trap or production measurements.
* src/api/src/zava_forward/api/web/chat.js:116-138 has no setup/reply refocus.
  Current/session/abort fencing remains at :58 and at each continuation.
  Explicit empty-submit focus and synchronous Send-to-input disabling handoff
  remain user-action-driven, not incoming-reply focus.
* chat.js:59-64 captures ownership before reset removes the popup, then focuses
  app only when necessary to recover that removed focus target. Shared dispose
  no longer briefly hides the surviving launcher. Employee reset/install/deny
  continue to own final admission for signed-out and Contractor users; removing
  shared launcher hiding does not bypass those checks.
* Shared named log/status remain polite; the inline alert at chat-widget.js:56
  now explicitly overrides implicit assertive politeness with aria-live=polite
  and aria-atomic=true, retaining visible errors and described-by selectors.
  DOM/axe checks do not prove actual announcement behavior in every screen reader.
* No changes to resident consent, own-record requests, generation fencing,
  unsupported-intent refusal, human/manual callback authority, stored question
  masking, session isolation or backend authorization were introduced.

## Original Finding Resolution Assessment

| Original finding | Exact correcting evidence | Verification and disposition |
| --- | --- | --- |
| RV-001 [Medium], obscured external focus | chat-widget.js:107-110 and :126; chat-widget.css:1-2; shared checker focused_control_visible at :22-29, short_window_launcher at :42-55, bidirectional exit at :225-247 and signed-out resident reproduction at :570-579 | Resolved in this candidate. Supplied actual-app browser pass covers 320x800 Open/Shift+Tab twice to Sign in with hidden popup and hit-testable focus; both audiences cover forward/reverse exits, retained draft/history and 1280x500 keyboard launcher hit-testing plus one-click close/reopen. Inspected resident screenshot shows clear Sign in focus and no popup. Independently rerun Node lifecycle test proves retained draft/skill/log/busy, no return focus, hidden reply retention and listener disposal. |
| RV-002 [Medium], employee async focus theft | chat.js:116-138 removes both asynchronous focusInput calls; :59-64 protects external/launcher focus on denial; shared checker current_reply_focus at :58-123 and employee_current_focus at :309-399; new test at :144 onward | Resolved in this candidate. Independently rerun behavioral matrix covers four stages (skills/status/thread/ask), four outcomes (success/error/403/404), three deliberate targets (external/launcher/internal heading): 48 combinations. Supplied actual-app evidence additionally covers the same employee matrix and six current reply cases per audience. External focus hides popup; launcher/heading focus keeps it visible, so hiding alone cannot make this regression pass. |

Both independently rerun new tests fail as expected on original baseline copies:
2 tests, 2 failures, 0 errors. In-memory comparison confirmed both external
baseline JS files exactly equal git show 9658b51b bytes before the negative run.
This establishes regression polarity, not only a green candidate test.

The original Review remains Complete / Defects found at its original boundary.
These resolutions justify a dated parent closure-status append referencing this
record; they do not erase or change that historical finding set or imply whole
issue, human accessibility or publication acceptance.

## Implementation-Time Plan and Detail Update Assessment

| Amendment | Trigger/rationale | Assessment |
| --- | --- | --- |
| Narrow CSS correction and 1280x500 oracle | PC-001 launcher exception counterexample | Explicitly incorporated into scope/details; necessary to satisfy unchanged owner intent, not redesign |
| Employee heading-focus oracle | PC-002 obsolete post-setup input-focus expectation | Only that expectation changed; typing subsequently selects input explicitly through fill |
| Resident outside-focus oracles | New intentional dismissal invalidates visible-then-manual-close expectations | Two migrations retain pending completion, focus target, no agenda side effect, draft/consent/session assertions |
| Launcher visibility owned by adapter | Browser denial matrix exposed transient hide/show blur | Details and changes explain refinement; shared disposal clears root/timer/listener/expanded state, adapter admission remains intact |
| Stale-operation route readiness wait | Real route rendering focuses app and would dismiss a replacement opened too early | Waits for destination heading/loading completion; all 12 old success/rejection, no stale request/text/focus/busy assertions remain |
| Hidden retained log/error selectors and browser-chrome traversal handling | Earlier harness failures, honestly recorded | Inspect retained hidden DOM by attributes; wait for an actual page control rather than accepting body as exit evidence; no softened safety boundary |

These are compatible implementation refinements, reflected in current plan,
details and changes before Review. No significant divergent product decision,
unaccepted scope expansion, repeated critique or premature dependent work was
identified.

## Critique and Material Revision Assessment

* PC-001 accepted and satisfied: bounded short-height CSS correction and both
  actual-app 1280x500 launcher visibility/toggle oracles.
* PC-002 accepted and satisfied: one employee oracle migration; both existing
  audience browser checks are mandatory and recorded passing.
* PC-003 accepted and satisfied at DOM/engineering boundary: polite atomic
  errors, retained role selectors, current setup/reply failure and draft/focus
  assertions. Human assistive-technology acceptance remains unperformed.
* PC-004 accepted and satisfied: current 403/404 setup/status/thread/ask tests
  preserve external and surviving launcher focus and recover removed internal
  focus. Existing employee checker still exercises actual API 401 login/session
  transition separately, including hidden launcher and focused app; no attempt
  to preserve a launcher whose session admission has actually ended.
* PC-005 rejected by parent as worker-only runtime restriction absent in parent.
  Accepted as an execution-context disposition, not a product exception or
  permission for this reviewer to violate its own constraints. Parent evidence
  explicitly names the existing /tmp/mv runtime and external outputs. Reviewer
  used existing system Python/Node for memory-only focused validation, did not
  run /tmp/mv, create scratch files, install or substitute dependencies, or claim
  the full requested runtime checks were independently rerun.
* Preserved critique execution Complete / verdict Revise remains historical;
  its dispositions do not retrospectively turn it into a passing critique.

## Test Migration and Boundary Assessment

The complete shared-check diff adds assertions without removing its original
asset-byte equality, real workflow fallback, loading 199/200ms boundary, IME/
Enter/Shift+Enter, collapsed sources, disabled unsupported controls, layout/
reflow, reduced motion, axe, denial, recovery or obsolete-operation assertions.
The controlled employee matrix temporarily wraps api only inside test scope and
restores it before completing the held result; no production API fallback was
added. The standalone employee checker retains six selections, arrived transport,
nine late successes and actual 401/403/404 checks. The resident checker retains
consent-before-request, pending withdrawal/re-consent, cross-session clear,
typed-ahead draft and no automatic agenda/manual booking authority.

The new bounded Node harness executes the actual shared factory and employee
adapter, uses a 30-second subprocess timeout and requires no new package. Its
minimal DOM cannot independently establish CSS visibility or actual browser
focus-loss-on-hide behavior; the supplied actual-app browser matrix covers that
separate boundary. No inappropriate fallback or broad implementation change was
found.

## Web-Guideline Assessment

Canonical source freshly retrieved in full for this Review on 2026-10-29:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Reviewed all applicable rules against changed web files with surrounding context;
not a whole-site audit. Repository plain ASCII/sentence-style content and
owner-selected Fluent conventions take precedence over generic typography and
Title Case preferences. Ephemeral chat visibility/conversation is intentionally
not serialized into URLs; no private text URL state is introduced.

### src/api/src/zava_forward/api/web/chat-widget.js

Pass: changed-scope native keyboard controls/names, polite async regions,
focus ownership/visibility, lifecycle cleanup and retained state. No new
anti-pattern or substantive changed-scope finding.

### src/api/src/zava_forward/api/web/chat-widget.css

Pass: launcher separation, safe areas, bounded flex/overflow layout, native
theme colors, overscroll containment and reduced-motion behavior preserved.
No new substantive changed-scope finding.

### src/api/src/zava_forward/api/web/chat.js

Pass: incoming setup/replies do not autofocus; denial recovery respects focus
ownership, explicit actions retain intentional focus and inline error recovery.
No new substantive changed-scope finding.

All-rule applicability check: accessibility/focus, forms, animation, typography,
content handling, performance, navigation/state, touch/interaction, safe-area
layout, theming, hover and copy were considered. Existing log scroll positioning
and content-visibility handling were not expanded. No new image/media, fonts/
external asset loading, drag/gesture-only action, locale/date/number rendering,
SSR/hydration, destructive action, heading anchor or authentication form was
introduced by these edits; corresponding conditional rules have no new surface.
Browser-check synthetic note/geometry reads are test-only, not production
render-path measurements. Existing unrelated file content is not reclassified
as a defect merely because its file contains this bounded focus correction.

## Findings

No new substantive findings. Complete severity summary: 0 Critical, 0 High,
0 Medium, 0 Low. Original RV-001/RV-002 resolution evidence is recorded above,
not reused as a new finding set. No source fixes or repeated Review are required
by this record.

## Defects and Routed Findings

No new implementation defect, significant decision gap or material evidence gap
within this assessed follow-up. No later rpi-implement, rpi-plan or rpi-research
invocation is recommended for this candidate.

## Plan Follow-Up Assessment and Residual Work

| Distinct follow-up | Why outside this correction | Owner / next action |
| --- | --- | --- |
| Existing 320px case-summary height baseline | Historical unrelated page-layout failure, not caused by focus correction; original oracle remains | Owner-maintained separate baseline investigation |
| Human accessibility and live-service acceptance | DOM, synthetic browser and axe do not establish announcements/usability, voice-control, native zoom or real-service/model acceptance | Owner-led screen-reader, voice, real-user and live-service checks |
| Publication and hosted/human approvals | Candidate uncommitted, no publication authorized; no complete local gate receipt | Future publishing owner runs required external exact-head gate and independent/human/hosted approvals |

These remain outside active P01/P02 implementation completion and are not new
defects, implicit deferrals of required active checks, or issue-closing evidence.

## Validation Evidence

| Check | Status | Evidence boundary |
| --- | --- | --- |
| Focused candidate unittest | Independently passed | PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/api/tests -p test_chat_widget_focus.py -v; 2 tests, including 48-case matrix |
| Negative baseline polarity | Independently confirmed expected failure | Loaded same class in memory, rebound WEB to E/focus-baseline after exact git-show byte comparison; 2 failures/0 errors on 9658b51b |
| Node syntax | Independently passed | node --check for changed chat-widget.js and chat.js |
| Git diff --check | Independently passed | Full current tracked diff; no whitespace error |
| Related unittest modules | Supplied PASS, not independently rerun | E/unittest.log: 196 tests, one existing opt-in skip; exact module command in changes |
| Opt-in test_chat_panel | Supplied PASS, not independently rerun | E/opt-in.log: 38 tests, no skip; expected diagnostic trace does not alter runner OK |
| Ruff check/format and mypy | Supplied PASS, not independently rerun | E/static.log: check passed, 59 formatted files, no typing issue in 111 source files |
| Isolated shared browser lint/format and third JS syntax | Supplied PASS, not independently rerun | E/static.log and exact commands in changes; silent node success recorded there |
| Shared actual-app browser | Supplied PASS, not independently rerun | E/browser.log and results.json; Chromium 156.0.8078.4, both audiences, 48 current and 12 obsolete employee combinations, recovery/consent/layout |
| Existing employee browser | Supplied PASS, not independently rerun | E/employee.log; two recorded axe states, zero violations; actual 401/403/404 and six selections retained |
| Existing resident browser | Supplied PASS, not independently rerun | E/resident.log and report.json; 32 scan states, zero violations, no console errors/external requests; synthetic consent/manual/session flows |
| Screenshot inspection | Independently inspected supplied images | Resident Sign in focus unobscured at 320px; employee bounded popup/composer and separate launcher |
| Human assistive technology, live model/service, full publication gate | Unperformed | Explicitly outside this candidate's demonstrated engineering acceptance, no approval inferred |

Full Python/static/browser suites were not rerun by this reviewer. Existing
recorded parent-runtime evidence plus direct source comparison, focused positive/
negative behavioral runs and screenshot/report inspection support this bounded
verdict. No temporary-directory file operation, dependency installation, Azure
operation, push, rubric edit or commit was performed.

## Blockers and Remaining Work

No blocker to this independent Review or the selected source correction's
engineering verdict. Parent owns P02-T02 closure-status append, marker/state
reconciliation and requested privacy-safe local commit. No source edits were
made here. No whole-issue closing keyword or publication approval is implied.

## Outcome

* Execution: Complete.
* Outcome: Conformant.
* Rationale: original RV-001/RV-002 are resolved within this candidate's bounded
  engineering scope; critique dispositions and implementation refinements
  preserve owner focus, privacy and recovery intent. No new substantive defect
  was identified. Human/live/publication acceptance remains distinct.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No new defect found |
| Decision gap or invalid assumption | None | No unresolved divergent decision |
| Material evidence gap | None within reviewed boundary | Broader acceptance is explicitly separate |
| Non-blocking residual work | Distinct owner follow-ups | Baseline layout, human/live acceptance, future publication gates |

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/chat-widget-550-focus-fixes-plan.md](.copilot-tracking/plans/2026-10-29/chat-widget-550-focus-fixes-plan.md) | Full selected follow-up plan |
| [.copilot-tracking/details/2026-10-29/chat-widget-550-focus-fixes-phase-details.md](.copilot-tracking/details/2026-10-29/chat-widget-550-focus-fixes-phase-details.md) | Lifecycle, test and validation details |
| [.copilot-tracking/research/2026-10-29/chat-widget-550-focus-fixes-research.md](.copilot-tracking/research/2026-10-29/chat-widget-550-focus-fixes-research.md) | Focused research and acceptance rationale |
| [.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-focus-fixes-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-focus-fixes-plan-critique.md) | Preserved critique and five dispositions assessed |
| [.copilot-tracking/changes/2026-10-29/chat-widget-550-focus-fixes-changes.md](.copilot-tracking/changes/2026-10-29/chat-widget-550-focus-fixes-changes.md) | Implementation history and exact local validation commands |
| [.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-review.md](.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-review.md) | Preserved original adverse Review |
| [src/api/tests/test_chat_widget_focus.py](src/api/tests/test_chat_widget_focus.py) | Independently executed behavioral regressions |
| [src/api/README.md](src/api/README.md) | Updated contract and validation limits |
| [.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-focus-fixes-review.md](.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-focus-fixes-review.md) | This single independent Review |

## Next Steps

Return to active parent: the evidence supports appending dated resolution status
for original RV-001/RV-002 while preserving the original adverse Review, then
reconciling P02-T02 and making the owner-requested local commit. No source fix,
repeat Review, user decision, push or publication is authorized by this record.
