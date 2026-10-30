<!-- markdownlint-disable-file -->
# Changes: resident-live-acceptance

Task ID: resident-live-acceptance-2026-10-30. Date: 2026-10-30.
Declared scope: full bounded evidence plan, no application changes.
Execution: full RPI loop and bounded local persistence complete; gate blocked.
Critique: executed once, original Revise,
PC-001 rejected with parent-context rationale; PC-002/003 applied.

## Plan and Evidence Pointers

* Research: .copilot-tracking/research/2026-10-30/resident-live-acceptance-research.md
* Plan: .copilot-tracking/plans/2026-10-30/resident-live-acceptance-plan.md
* Details: .copilot-tracking/details/2026-10-30/resident-live-acceptance-phase-details.md
* Critique: .copilot-tracking/plans/2026-10-30/resident-live-acceptance-critique.md

## P01: Live Execution

E1: .copilot-tracking/changes/2026-10-30/resident-live-acceptance/evidence.json,
2026-10-30 10:31:45-10:31:59 UTC, Chromium 156.0.8078.4, Playwright 1.64.0.
Actual form login POST /demo/login returned HTTP 200 on the only submitted
attempt. Authenticated content became visible. Both fields were masked,
credential lines trimmed only inside automation and cleared after submit.
No screenshots, trace, HAR, video or storage-state export. Context/browser
closed; literal-credential exclusion passed within automation. No private
case/account payload, request body/header, cookie or identity was emitted.

E2: .copilot-tracking/changes/2026-10-30/resident-live-acceptance/acceptance.py,
exact executed final source SHA-256
f90d23e0bc05df7871be88da6d0354a7880b311402ed238c8c0a2c74205131ad.
E1 records matching before/after hashes. No edits to E2 after this run.

The earlier sibling Review's 401 remains unchanged historical evidence.
Today's 200 does not identify that earlier denial's cause or prove an
operator repaired it. No Azure/vault/Container App inspection occurred.

### Resident observations

* Bottom-right native Chat button, 16px right/bottom gaps, opens role=dialog.
* Initially unconsented. Enter on the question produced the visible error
  "Agree to use your own record for this question first." and no assistant POST.
  Checking permission preceded actual assistant requests at 10:31:50.872767
  and 10:31:55.233480 UTC. This is client ordering, not backend-only evidence.
* Enter sent the rat question; an honest inability and housing-officer route
  replaced the unwanted home summary. E1 preserves that non-secret reply.
* Send sent a second status question. Both sends left chat open; four ordered
  user/assistant/user/assistant messages survived Escape/reopen. The log had
  role=log, aria-live=polite, overflow=auto, scrollTop 479, clientHeight 269,
  scrollHeight 748 (exact end). The composer was below the independent log
  at all measured widths. No direct manual scroll/pin interaction was exercised.
* Shift+Enter inserted a newline without a request. Send was present.
* Input-area selector was present with the sole option "Resident assistant".
  No resident alternative or skill-changing behavior is claimed; README
  specifies employee skills separately.
* Attach/Voice were disabled with a visible unsupported reason. The actual
  replies were labelled "Summary by rules - workflow only, no AI used" and
  "Summary by rules". First Sources details were initially collapsed.
  No actual AI-generated response or thin AI-label geometry was established.
* Popup widths were 448/358/288 at 1280/390/320 CSS px, contained in the
  viewport without document horizontal overflow. Question focus had a 3px
  solid outline; Escape closed and returned focus. Motion token changed from
  150ms to 0s under reduced-motion emulation. No native screen reader, full
  contrast/zoom/touch/axe/conformance assessment was performed.

## P02-T01: Complete Criterion Matrix

These are faithful compound summaries of W1-W3, retrieved 2026-10-30.
"Proven" is limited to the requested resident portion, not both-site or
whole-issue acceptance. "Unmet" includes out-of-resident-scope and missing
proof, not necessarily a diagnosed product defect. Any missing required
compound subpart prevents a whole-criterion pass.

| ID | Criterion | Outcome | Evidence and remaining boundary |
| --- | --- | --- | --- |
| 550-01 | Both sites share one component, bottom-right icon opens popup | Unmet | E1 proves resident launcher, gaps and dialog only; employee and shared rendered use untested |
| 550-02 | Persistent scrolling thread, newest bottom, pinned input, remains open | Unmet, compound proof incomplete | E1 ordered four-message log, exact bottom/independent overflow, composer below log at three widths, stays open and reopens with history; direct scroll/pinned-input behavior and employee untested |
| 550-03 | Enter sends, Shift+Enter newline, send button | Proven, resident scope | E1 Enter caused one request/reply, newline caused none, second question sent with Send |
| 550-04 | Compact input-area employee selector changes agent/skill, active one shown | Unmet | Employee-only change obligation outside scope; resident selector observed, only fixed Resident assistant option |
| 550-05 | Attach/Voice present or disabled with reason | Proven, resident scope | E1 both disabled with visible unsupported reason; employee untested |
| 550-06 | AI content has thin label and collapsed sources | Unmet | Both E1 replies rules-only, first Sources collapsed; actual AI output/AI label and thin styling not proven |
| 550-07 | Resident consent precedes data use | Unmet, compound proof incomplete | E1 proves client consent error/no assistant request then explicit permission before two requests; server-only data/model ordering not observed |
| 550-08 | Rat-like free text gets relevant answer or honest inability/contact, not home summary | Proven, resident scope | E1 actual question received "I cannot answer that" plus housing-officer route, no home summary |
| 550-09 | Loading after 200ms, errors shown, keyboard/screen-reader semantics, reduced motion | Unmet | E1 actual chat consent error, native keyboard/log/live/focus/Escape and motion; exact threshold, generated/loading/error/AT coverage incomplete |
| 551-01 | Compact header filters at top of expanded map | Unmet, outside resident scope | No employee map reached or substituted from resident cards |
| 551-02 | Filter updates markers and header state consistently | Unmet, outside resident scope | No employee map interaction |
| 551-03 | Keyboard operation, non-colour selected state, narrow readability | Unmet, outside resident scope | No employee map interaction or narrow-map proof |
| 551-04 | Browser/unit coverage of filter behavior | Unmet in this run | C1 earlier Review records source-only coverage; not newly inspected/executed or upgraded to live proof |
| 552-01 | Presentation icons and text on workflow steps | Unmet, outside resident scope | No employee single-case workflow or icon-provenance check |
| 552-02 | Visibly thinner steps, reduced vertical space | Unmet, outside resident scope | No case geometry or trusted comparative baseline |
| 552-03 | One-line blocker and full keyboard/touch tooltip/popover | Unmet, outside resident scope | No employee blocker or touch test |
| 552-04 | Attached tabs/panel outside inner scroll, panel below scrolls | Unmet, outside resident scope | No employee case tabs or panel scroll test |
| 552-05 | Fluent 2 and WCAG baselines preserved | Unmet | Resident basics only, no case/whole-workflow or full Fluent/WCAG acceptance |
| 552-06 | Desktop and narrow browser evidence of case view | Unmet, outside resident scope | E1 resident chat at three widths does not substitute for employee case |

Parent outcome: three resident-scope criteria proven, sixteen whole-compound
criteria unmet/inapplicable/incomplete in this run. No whole issue accepted.
The owner's extra resident agent-dropdown check is proven as present/fixed,
not as switchable agent selection. No actual model execution claimed.

## Amendments and Divergences

One login attempt planned, immediate 401 stop. No product/source modifications.
The complete 19-entry baseline and initial-consent branch were added before
execution as direct critique dispositions, not a second planning cycle.

The first browser launch timed out during initial navigation before the
credential read or any login submission. Its original sanitized record is
preserved as prelogin-timeout-evidence.json (10:30:33-10:30:53 UTC).
A separate public-only MCP inspection returned HTTP 200 and the expected
sign-in form. No credentials were used in MCP. The automation navigation
wait changed from networkidle to domcontentloaded with 60s navigation timeout,
and now separates wait_signin_form as a stage. This is a safe ordinary local
browser-load adjustment, not an auth retry or changed acceptance criterion.
The original timeout JSON binds its own script hash; the final script is not
claimed as the exact failed-run bytes. Budget amended for that preserved JSON.

Before the rerun, /tmp/mv/bin/python failed to import Playwright, despite its
earlier successful use. No credential read or login occurred during that
import failure. Restored pinned playwright==1.64.0 only after this observed
missing dependency, into this task's external session-owned
files/resident-runtime venv. No repository manifests or shared runtime were
changed. This supersedes the initially selected shared interpreter, not any
acceptance/safety boundary.

## Validation and Remaining Work

Automation syntax passed before execution; E1 final-script hash matches E2.
Final E1 is valid JSON, browser contexts closed and credentials excluded by
the automation. The original pre-login timeout and its hash are preserved.
Post-run assertions verified the exact script hash; one HTTP-200 login;
masking/no recordings/cleanup; permission-before-request timestamps; rat
inability/contact; 16px launcher gaps; exact log bottom; three viewport
widths/no overflow/contained composer/focus; motion 150ms-to-0s; and exactly
19 criterion rows. All assertions passed. Git diff whitespace check passed.
Web Interface Guidelines were fetched afresh before Review. No changed web
application files exist; browser basics are scoped observations, not a fresh
whole-source guidelines audit or axe/conformance result.
P01 and P02-T01 completed. Independent original Review is Complete with
outcome Residual work. Local commit and external full gate attempt are recorded below. Human approval
remains unchecked and unclaimed.

## P02-T02: Original Independent Review

.copilot-tracking/reviews/logs/2026-10-30/resident-live-acceptance-review.md
records the one original independent Review, Complete / Residual work.
It independently verified exact final script hash, parsed both JSON records
as inert data and reconciled all 19 outcomes (3 scoped Proven, 16 Unmet).
No product defect established. RV-001 Medium and RV-002/003/004 Low are
retained and ranked in the session state for later work, not current repairs.
The Review's publication/commit-pending statements describe its assessed
boundary and will not be rewritten after parent closeout.

Parent transition: task completed at Follow-up, automatic session running,
no child started. Review findings remain later work, not product repairs.

## P02-T03: Local Persistence and Blocked Full Gate

Original implementation and dated original critique/Review were committed
locally as bb74275c1c547ccccde558aa6c9a7d4413681964, with message
"test(resident): record authenticated live acceptance (Refs #550, Refs #551,
Refs #552)", privacy-safe authenticated GitHub ID+login noreply email for both
author and committer, and Copilot trailer. No push, PR, issue edit or closing
keyword was used.

Full gate command: python3 tools/rpi-checks.py --all --base current-origin-main
--lock-timeout 0 --out new-external-directory. Original external output roots:

* /home/azureuser/.copilot/session-state/1b96c3f3-ccca-4548-9de0-0b49b74e18c7/files/resident-gate-original
* /home/azureuser/.copilot/session-state/1b96c3f3-ccca-4548-9de0-0b49b74e18c7/files/resident-gate-clean

Their sibling .log files preserve exact runner output. The first attempt
returned "BLOCKED: Candidate has ignored inputs; move all scratch outside
the checkout". The only ignored file was this run's public-only MCP console
log. It was moved intact to external session files/resident-public-console.log;
before/after SHA-256 was
5249c18e489dcd9a6eee4673e5b332d3726321606efc6aae774286a01e5cc839.
No historical artifacts or foreign files were removed.

The clean-input retry returned "BLOCKED: Candidate does not descend from the
reviewed main base". A fresh read-only fetch confirmed current origin/main
7c13115631a163061038d69754a8feb2732daca6; candidate merge-base remains
63422cdf9fd477dd8892a27ac8b11487bc3a2429. Main advanced concurrently with
the demo-redeployment PR #561. This run's evidence is its dated live snapshot,
not proof of parity or behavior after a later deployment.

The actual shared heavy-lock holder was separately observed as PID 1623817
(python3); no duplicate queued gate or interference occurred. The runner
stopped at earlier guards, so no successful full receipt or completed scanner,
SQL, browser, image or full-suite result is claimed.

This parent closeout is a second local commit and therefore invalidates
any earlier exact-head gate evidence. A final same-command nonqueued attempt
uses the new external files/resident-gate-final output root and sibling .log.
No passing receipt can be verified; publication remains blocked pending
separately authorized ancestry reconciliation and a clean exact-head full gate.
No rebase, merge, force-push, Azure fallback or protection change was performed.

## Follow-Up Items

* Establish actual enabled-model response and thin AI label/sources, and exact
  loading/error threshold evidence, only under separate authorized execution.
* Independent employee map/case/shared-component acceptance is outside this
  resident-only task, not implicitly delivered by these observations.
* Human screen-reader, zoom/contrast/touch and complete accessibility acceptance
  remain separate gates; no conformance follows from browser basics.
