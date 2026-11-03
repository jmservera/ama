---
title: Regulatory alert and home chat acceptance kit (assistive technology by role and staff comprehension)
description: Human test scripts, frozen answer key and blank record tables for the two unmet #215 criteria. Preparation only; every row is Not run
ms.date: 2026-11-03
ms.topic: reference
---

## Purpose and status

Issue #215 has two unmet criteria that need people, not automation:

| Criterion | Status | What this kit adds |
| --- | --- | --- |
| WCAG 2.2 AA: no colour-only status, keyboard operable, plain-language mode | Partial. Automated axe (21 states, zero violations and incompletes) and scripted keyboard checks exist | Per-role keyboard and screen-reader scripts and a blank record table |
| Comprehension tested with repairs, housing and grants staff before use | Not run | Task cards, a frozen answer key, critical-error definitions and a scoring tool |

Nothing here is a result. No participant has been tested, no assistive-technology
session has been run and no conformance or comprehension claim is made. Both
criteria stay unmet until the records below are completed by authorised people
and the owner reviews them. The existing
[comprehension protocol](../../../../src/api/README.md#staff-comprehension-protocol-not-run-unmet)
sets consent, privacy, group sizes and success thresholds; this kit does not change them.

## Preconditions

* Owner authorisation and privacy review for participants, as the protocol requires.
* Fictional homes, sources and exercise identities only. The synthetic app is run
  locally per the [API README](../../../../src/api/README.md#regulatory-alert-and-home-chat-ux-215).
* AI unavailable is part of the test: run every task once with the chat service
  disabled so the manual and card paths are exercised.
* Participants may stop at any time and may use a non-digital route.

## Assistive-technology and keyboard script by role

Run each script as a person who uses that role, on the alert panel and the home
chat, at 100 percent, 200 percent text size and 320 px width. Use keyboard only
(no pointer), then one screen reader (NVDA with Firefox or Chrome on Windows,
VoiceOver with Safari on macOS or iOS). Record the version used.

| Role | Task to perform | Pass when |
| --- | --- | --- |
| Repairs and intake | Find the alert, say what was noticed, then use the doubt route with chat unavailable | Hazard intake route is reachable in no more than the same steps as normal intake; nothing depends on chat |
| Building Safety | Read a source-and-status line for a hazard alert and identify the clock | Status is announced as words, not colour; the clock and owner are read in order |
| Assessor and coordinator | Open a cited answer, follow the provision link, return | Focus returns to the question after the answer; link purpose is clear out of context |
| Programme | Distinguish a future or unknown source from an active control | Future and unknown are announced differently from active |
| Finance and grants | Meet a missing grant or contract source state | The no-source state is announced and no terms are invented; manual route offered |
| Data handlers | Switch plain-language mode on and off with the keyboard | Space toggles; state is announced; content is not lost on switching |
| Suppliers | Read the static guidance and take the human route | No interactive chat; human contact route is announced |

Record for every cell: pass, fail or blocked; the barrier in words; the
success criterion it relates to (WCAG 2.2 AA numbers only where clear); and
whether a manual workaround exists. A single failure is a finding to route, not
a reason to ignore the passing cells.

### Blank record table

| Session code | Role | Tool and version | Task | Result | Barrier and criterion | Workaround |
| --- | --- | --- | --- | --- | --- | --- |
| Not run | | | | | | |

## Comprehension task cards and frozen answer key

The five tasks follow the protocol. Reviewers score each answer as correct,
incorrect or critical error against this key before seeing the participant group.
Reviewers must not coach on law. Where a source is not held, the only correct
answer is that it is not held and the doubt route applies.

| Task | Participant is asked to | Correct answer contains | Critical error (stop and explain the safe route) |
| --- | --- | --- | --- |
| 1 Hazard while chat is unavailable | Say what to do about an urgent hazard card with chat off | Use the normal hazard intake route now; do not wait for chat, a doubt receipt or an owner reply | Delays or defers hazard intake pending chat or a reply |
| 2 Alert fields | Name what was noticed, source, status, safe action, owner and clock on a card | All six, read from the card, in the participant's own words | Names an action not on the card |
| 3 Future or unknown versus active | Say which of two cards is a control in force | Only the one whose status says it is in force; future and unknown are not duties yet | Treats a future or unknown item as an active duty |
| 4 Missing grant or contract source | Say what the term is when no source is held | Not held; record the doubt and ask the named owner; no term is stated | Invents a term, approval or consent |
| 5 Doubt receipt | Say what sending a doubt does and does not do | It records the question for the owner; it does not approve, decide compliance or replace professional judgement | Says a receipt establishes compliance or approval |

Use deterministic cards with provision links and the chat on equivalent fictional
tasks, and counterbalance the order across participants. Record completion time,
assistance, accessibility barriers and confidence per task on a separate sheet.

### Scoring

Scorers record one anonymous JSON record per participant and task, for example
`{"participant": "P01", "group": "repairs", "task": 1, "correct": true, "critical_error": false}`.
Two reviewers score independently and reconcile disagreements with written
reasons before this step. Then run:

```bash
python3 src/api/checks/regulatory_comprehension_score.py records.json
```

The tool applies only the predeclared thresholds: at least 90 percent correct
overall, at least 80 percent in each of repairs, housing and grants, zero
critical errors, at least three participants per group and complete records. It
reports denominators. Meeting them is not acceptance. A small formative round
cannot establish general staff comprehension; the human owner reviews results,
failures and group differences before any staff-use decision.

### Blank results table

| Group | Participants | Correct / answers | Critical errors | Owner decision |
| --- | --- | --- | --- | --- |
| Repairs | Not run | | | |
| Housing | Not run | | | |
| Grants | Not run | | | |

## Boundaries

* No legal-currentness check, real-data approval or operational activation follows from this kit.
* Human approval, resident consent and named owner boundaries in
  [regulatory literacy](./regulatory-literacy-for-journeys.md) are unchanged.
* Design language follows the [design system](./design-system.md) and
  [content standard](./content-standard.md); findings that need copy changes route
  to those documents.
