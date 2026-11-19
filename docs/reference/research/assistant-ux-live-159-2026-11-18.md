---
title: Assistant Panel Keyboard and Announcement Live Proof on the Synthetic Demo (#159)
description: Playwright evidence that the workbench employee assistant is keyboard operable and announces new messages on the live demo, and why screen-reader testing stays unproven
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope

The only unticked criterion of #159 is "Panel is keyboard operable, screen-reader tested, and announces new messages". The other criteria, including the tokenomics box, are ticked and were not reopened. Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure authorised, person-run assistive-technology testing not needed. No source code changed and no Azure resource was created or modified.

## Target

`ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000031`, image digest `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`. Signed in as the staff test user (Retrofit Programme Manager); credentials were read at runtime and never printed. Case `ZF-2025-0122`, desktop viewport 1440 by 900.

## Method

* [login.py](./assistant-ux-live-159-2026-11-18/login.py) signs in and saves a scratch session, deleted after use.
* [probe-keyboard-announce.py](./assistant-ux-live-159-2026-11-18/probe-keyboard-announce.py) uses only keyboard events (Tab, Enter, typed text, Escape) and a MutationObserver on the log and status regions. Raw output: [probe-keyboard-announce.out.json](./assistant-ux-live-159-2026-11-18/probe-keyboard-announce.out.json).
* [shots-keyboard.py](./assistant-ux-live-159-2026-11-18/shots-keyboard.py) takes cropped screenshots of the launcher, header and composer. The conversation log is never captured because answers name synthetic people. Output: [shots-keyboard.out.txt](./assistant-ux-live-159-2026-11-18/shots-keyboard.out.txt).
* [cleanup-own-threads.py](./assistant-ux-live-159-2026-11-18/cleanup-own-threads.py) deleted the single stored thread the probe created (age 1 minute, probe case only).

## Results

| Check | Observed |
| --- | --- |
| Reach the launcher by keyboard | Tab reached "Chat" after 44 stops from page start |
| Open | Enter opens the dialog; `aria-expanded` becomes true; focus lands on the heading "Employee assistant" |
| Dialog semantics | `role=dialog`, `aria-labelledby` the heading |
| Tab order inside the panel | Close chat, About this chat, Chat size, conversation log (tabindex 0), question box, Agent skill, Send; Attach and Voice are disabled and skipped |
| Send | Typing then Enter sent two turns; focus stayed in the question box |
| Log semantics | `role=log`, `aria-live=polite`, `aria-relevant=additions`, label "Employee assistant conversation" |
| New message announcement | Four nodes added to the log (two You, two Assistant); the status region changed to "Asking the assistant." then "Answer added. Check the sources before relying on it." and, for the second turn, "Workflow-only help added. No assistant answer was given. Check the case card for recorded facts." |
| Error region | `role=alert` present and hidden when there is no error |
| Close | Escape hides the panel and returns focus to the launcher |

Screenshots: [launcher focus](./assistant-ux-live-159-2026-11-18/shots/01-launcher-keyboard-focus.png), [dialog heading](./assistant-ux-live-159-2026-11-18/shots/02-dialog-open-heading-focus.png), [composer focus](./assistant-ux-live-159-2026-11-18/shots/03-composer-keyboard-focus.png).

Local cross-check: `test_assistant_panel_a11y_159.py` from `src/api`, 5 tests, observed, raw output not retained, including the browser axtree, live announcement and keyboard turn tests.

## Verdict

| Part of the criterion | Verdict |
| --- | --- |
| Keyboard operable | Proven live on desktop |
| Announces new messages | Proven live as ARIA and DOM behaviour (live region plus status text); what a screen reader speaks is not observed |
| Screen-reader tested | Unproven. It needs a person using a screen reader, which the owner excluded for the demo; the checks above are not a substitute |

The issue box should stay unticked unless the owner accepts the automated evidence for the demo.

## Observations and limits

* Tab from Send leaves the panel to the top of the page; the panel is non-modal and last in the document, so this is expected but was not tested against a user need.
* Rules-only answers carry "Decision model (case rules), no record changed" and not the literal "AI suggestion, not approved". That label is part of an already ticked criterion and was not investigated.
* The probe is a single run on one case and one account; the second turn fell to workflow-only help because the question did not match a case fact.
* A synthetic owner name in the first answer text was redacted by hand in `probe-keyboard-announce.out.json`; the probe script itself prints the first 200 characters of each answer, so rerunning it will show such names in the console.
