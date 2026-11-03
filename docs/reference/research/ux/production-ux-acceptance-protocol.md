---
title: Production-build assistive-technology, consent and Fluent 2 / WCAG acceptance protocol (chat widget and case view)
description: Criterion-by-criterion status, human test scripts and blank record tables for the production acceptance carried over from issues 550 and 552 into issue 619
ms.date: 2026-11-02
ms.topic: reference
---

## Purpose and status

Issue #619 holds three criteria that the owner descoped from the demonstration
build on 2026-10-31 and required for the production build:

* #550: the resident consent step remains before any data is used.
* #552: the Fluent 2 and WCAG baselines in this folder are preserved.
* Screen reader, keyboard and zoom testing is recorded by a person, and the
  consent step is proven with a real resident journey.

This page is the test protocol and the record. It is not a test result. At
2026-11-02 every record row below is `Not run`. An agent, a unit test or a
browser script cannot fill a row; only a named person can, after doing the run.
Nothing here is a conformance claim, and no real resident was involved.

## Criterion status at 2026-11-02

| Criterion | Engineering evidence that exists | Human gate still open |
| --- | --- | --- |
| Consent before data use (#550) | Resident chat refuses the question without the consent checkbox (`resident_demo/app.py`, `assistant.js`), clears answers when consent is withdrawn, and says it is not consent to works. Covered by `chat_widget_browser_check` and `test_resident_chat_api` on synthetic data | A real resident journey, with DPO and Legal approval for real-resident use (see the [learning record](./resident-chat-learning-record.md)), recorded by a person |
| Fluent 2 and WCAG preserved (#552) | Static baseline in `test_accessibility_baseline.py`; pinned axe-core 4.10.3, 320/390/1280 px overflow and focus checks in `chat_widget_browser_check` and `case_view_ux_browser_check`; see the [design system](./design-system.md) and [WCAG baseline](./wcag-conformance-baseline.md) | Owner confirmation of target level (O-1), and the human runs below |
| Screen reader, keyboard, zoom recorded by a person | Keyboard order, focus visibility, reflow and live-region presence are checked by engineering scripts only | Every row in the record tables below |

Engineering checks do not show what a screen reader announces, and they do not
replace a person. The existing known gaps G-1 to G-4 in the
[WCAG baseline](./wcag-conformance-baseline.md#accessibility-statement-draft)
stay open until the rows below are complete.

## Automated checks on the production configuration (2026-11-03)

Owner decision 2026-11-03: deliver the automated axe-core and keyboard checks now
and keep the person-run criteria open until the production build exists. No
deployed production build exists yet, so `checks.production_config_a11y_browser_check`
runs the employee site from the repository with `ZF_ENV=production`,
`ZF_AUTH=trusted-proxy` and a synthetic ingress principal header. It checks, on
synthetic data and with pinned axe-core 4.10.3 (WCAG 2.0 to 2.2 A and AA tags):

* the case view tab list and tab panel have no axe violations, arrow keys move
  between tabs, and every Tab stop shows a focus indicator;
* the chat launcher has a name and visible focus, Enter opens the chat and moves
  focus into it, the open chat has no axe violations, Tab never lands behind the
  chat or off screen, and Escape closes it and returns focus to the launcher.

Observed 2026-11-03 (local run, Chromium 156.0.8078.4 with Playwright 1.64.1,
not a deployed build): all assertions passed. This is an
engineering result. It does not show what a screen reader announces, it does not
cover zoom to 400 percent, the resident site or the consent journey, and it is not
a conformance claim. Every record row above stays `Not run`. When a production
build exists, re-run the check against it and record the build commit.

## Test set-up

* Build under test: record the exact commit and the deployed or local build.
  Use the production build, with AI enabled, for the resident and employee chat.
* Platforms: NVDA with Firefox on Windows, and VoiceOver with Safari on macOS or
  iOS. Add one more pair if a tester uses another tool, such as JAWS or
  TalkBack.
* Viewports: 1280 px, 390 px and 320 px wide, 200 percent text size, and 400
  percent browser zoom on a 1280 px window.
* Testers: at least one person who uses a screen reader daily and one who
  navigates by keyboard only, where available. Owner confirms testers (O-3).
* Data: synthetic data for employee runs. Real resident data only under the
  approvals in script C.

## Script A: chat widget (resident and employee sites)

Run once per site, each platform, each viewport.

1. Keyboard only: Tab to the launcher. Check it announces its name and that
   Enter or Space opens the chat.
2. Check focus moves into the chat and the chat is announced as a dialog or
   named region. Check Shift+Tab and Tab never lose focus behind the chat.
3. Type a question. Enter sends, Shift+Enter adds a line, the Send button
   works. Check the agent or skill selector (employee) is reachable and
   announces the active value.
4. Check the loading state, the answer, the AI label and the collapsed
   sources list are announced, and that the sources open and close with the
   keyboard.
5. Trigger an error (for example block the endpoint). Check it is announced.
6. Escape or the close control closes the chat and returns focus to the
   launcher.
7. At 320 px, 200 percent text and 400 percent zoom, check no content is lost,
   no two-direction scrolling is needed, and the input and Send stay reachable.
8. Check reduced motion (operating system setting) removes animation.

## Script B: single case view (employee site)

1. Keyboard only: reach the workflow steps, the blocker summary, the tabs and
   the tab panel in a logical order.
2. Check each workflow step announces its text label (icons add no required
   meaning).
3. Check the blocker one-line summary announces, and that the full reason opens
   by keyboard (Enter or Space) and by touch, can be dismissed, and focus
   returns to its trigger.
4. Check the tabs announce as a tab list with the selected tab, move with the
   arrow keys, and the panel is named by its tab.
5. At 320 px, 200 percent text and 400 percent zoom, check the tabs stay
   attached to the panel and reflow without hidden content.

## Script C: resident consent journey (production)

Precondition: the owner and the DPO and Legal owner approve real-resident
testing in writing, the resident is told this is research and that they can
stop, and the resident consents to being observed and recorded as research
participant. That research consent is separate from the chat consent being
tested. Without these approvals, run the script only with a synthetic resident
and record the row as `synthetic only`, which does not meet the criterion.

1. The resident signs in and opens chat. Check the chat explains what will be
   used before any data is used, and that no question is sent or answered with
   own-record details before the consent checkbox is ticked.
2. Ask a question without ticking. Check the refusal is announced and focus
   moves to the checkbox.
3. Tick, ask, and check the answer says whether AI or rules were used.
4. Untick. Check use stops and earlier answers are cleared, as stated.
5. Ask the resident, in their words, whether they understood what they agreed
   to and that it is not consent to works. Record the answer.
6. Check a person can be reached without using chat.

## Record

Each cell holds `Not run`, or tester, date, build commit, browser and assistive
technology versions, criteria checked, result and exceptions. Add rows for
extra platforms. Do not copy a result from another row.

### Script A and B record

| Surface | Keyboard only | NVDA with Firefox | VoiceOver with Safari | 320 px, 200 percent text, 400 percent zoom | Result |
| --- | --- | --- | --- | --- | --- |
| Resident chat widget | Not run | Not run | Not run | Not run | Not run |
| Employee chat widget | Not run | Not run | Not run | Not run | Not run |
| Employee single case view | Not run | Not run | Not run | Not run | Not run |

### Script C record

| Journey | Approvals referenced | Resident type | Tester and date | Result |
| --- | --- | --- | --- | --- |
| Resident chat consent before data use | Not run | Not run | Not run | Not run |

## Closing issue 619

Issue #619 can close when every row above is complete by a named person, any
failure is fixed or recorded as an accepted exception by the owner, and the
owner confirms the target level (O-1) and the Fluent 2 baseline is unchanged.
Until then a pull request refers to the issue and must not use a closing
keyword. Fluent 2 adoption stays partial as stated in the
[design system](./design-system.md).

## Limits

* No screen reader, real resident or person has been involved in this change.
* Engineering scripts, axe-core and unit tests do not establish accessibility
  acceptance or WCAG conformance.
* WCAG 2.2 and any accessibility regulation were not re-retrieved here; check
  the official source before any external statement (O-5).
